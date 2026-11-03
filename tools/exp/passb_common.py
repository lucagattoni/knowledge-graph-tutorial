"""Pass B (the paid pilot): the hosted setup the four pass-A runners share. Plan item F2.

Pass A pointed a builder at the metering gateway and the gateway at a local Ollama, where every price is zero. Pass B keeps
that shape and changes two things: the CHAT model is served by a hosted provider (the gateway holds its key and caps the
spend), and the EMBEDDING model stays on the local server. A runner gets the hosted setup with `--hosted-profile PATH`:

    from passb_common import load_profile, make_gateway
    profile = load_profile("pilot-profile.json")
    with make_gateway(profile, workdir / "gateway", "http://127.0.0.1:11434/v1", [chat_model, embed_model], repo_root,
                      request_defaults={chat_model: {"seed": 7}}) as gw:
        ...                       # point the builder at gw.base_url with a dummy key, exactly as in pass A
        calls = gw.calls()        # the records THIS run added, with request and response from the body log
        block = gw.hosted_block() # what the result JSON records about the hosted side

What stays true by construction (and is tested in test_passb_common.py):

* **The key never reaches the runner or the builder.** The profile holds the PATH of a key file, never a key. The gateway is
  started with the environment `{"PATH": "/usr/bin:/bin"}` and no key on its command line; its config names the file and the
  gateway opens it itself. No code here opens that file, and no message or result names its path.
* **One ledger across stages.** The profile's `ledger_dir` holds `meter.jsonl` (and its body log and manifests), shared by
  every stage and run. A log that already holds records is continued with `--resume`. The profile's `allowance_usd` is what
  THIS run may spend: the gateway's cap is the spend already in the ledger plus the allowance, so a run can never take the
  ledger past what the owner allowed it, and a run whose allowance is used up is refused by the gateway (429) while the
  provider sees nothing. `calls()` returns only the records this run added, so a runner's counts are never polluted by an
  earlier stage.
* **Two upstreams.** `hosted`: the provider (OpenAI protocol, key from the file, `request_defaults` allowed because the owner
  says so in the profile). `local`: the runner's `--upstream-url` (Ollama, `dry_run`), used only for the embedding model at
  price 0. A chat model priced at zero, or an embedding call sent to the provider, would be a defect and is tested for.

One thing is not guarded here: two runs that share a ledger must not run at the same time. The cap is computed from the
ledger when the gateway starts, and a second writer would make that number stale. The plan runs builders one at a time.

Standard library only; money is Decimal throughout.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Context, Decimal, DivisionByZero, InvalidOperation, Overflow, Inexact, Rounded, localcontext
from pathlib import Path
from typing import Any, Iterable, Mapping
from urllib.parse import urlsplit

sys.dont_write_bytecode = True  # importing must not leave .pyc files in the repository
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import passa_common as pc  # noqa: E402

CURRENCY = "USD"
HOSTED = "hosted"
LOCAL = "local"
DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_TIMEOUT_S = 900
GATEWAY_ENV = {"PATH": "/usr/bin:/bin"}          # the gateway subprocess gets this and nothing else
LEDGER_LOG = "meter.jsonl"
LEDGER_BODIES = "meter.jsonl.bodies.jsonl"
NAME_RE = re.compile(r"^[A-Za-z0-9._:/-]{1,100}$")           # the gateway's model-name rule
DATE_RE = re.compile(r"^\d{8} \d{2}:\d{2}$")
KEY_LIKE_RE = re.compile(r"^[A-Za-z0-9_-]{20,}$")             # the gateway refuses a key_file that looks like this
MONEY_RE = re.compile(r"^\d+(\.\d+)?$")
MAX_DIGITS = 18                                                # the gateway refuses a decimal with more digits
# Fields the gateway refuses in request_defaults: they decide what is asked for and how much output is reserved.
PROTECTED_REQUEST_FIELDS = frozenset({"model", "messages", "input", "stream", "stream_options", "n",
                                      "max_tokens", "max_completion_tokens"})
ALLOWED_KEYS = ("base_url", "key_file", "ledger_dir", "allowance_usd", "upstream_timeout_s", "input_per_mtok",
                "output_per_mtok", "cached_input_per_mtok", "cache_write_per_mtok", "source_url", "read_at",
                "output_limit_default", "request_defaults", "translate_max_tokens")
REQUIRED_KEYS = ("key_file", "ledger_dir", "allowance_usd", "input_per_mtok", "output_per_mtok", "source_url", "read_at",
                 "output_limit_default", "request_defaults")
_EXACT = Context(prec=60, traps=[InvalidOperation, DivisionByZero, Overflow, Inexact, Rounded])


class ProfileError(pc.PassAError):
    """The profile is missing something or holds something odd. A message names the field, never its value."""


# ---- money ------------------------------------------------------------------------------------------------------
def money_text(value: Decimal) -> str:
    """Plain decimal text without exponent or trailing zeros: Decimal('0.60') -> '0.6', 0 -> '0'."""
    with localcontext(_EXACT):
        return format(value.normalize(), "f")


def sum_costs(records: Iterable[Mapping[str, Any]]) -> Decimal:
    """The sum of the records' `cost` (a decimal string), exactly. A record without a readable cost is an error: a
    ledger that cannot be summed cannot give a cap."""
    total = Decimal(0)
    with localcontext(_EXACT):
        for rec in records:
            try:
                total += Decimal(str(rec["cost"]))
            except (KeyError, ArithmeticError, ValueError):
                raise pc.PassAError("a ledger record has no readable cost") from None
    return total


def cost_usd(calls: Iterable[Mapping[str, Any]]) -> str:
    """The summed `cost` of the gateway's records, as text. Used for a run's total and for each checkpoint."""
    return money_text(sum_costs(calls))


# ---- the profile ------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Profile:
    """The owner's hosted setup, read from a JSON file. Two fields are paths that must never be written into a result;
    they are left out of repr() so a log line or a traceback cannot show them."""

    key_file: str = field(repr=False)
    ledger_dir: str = field(repr=False)
    allowance_usd: Decimal
    input_per_mtok: Decimal
    output_per_mtok: Decimal
    source_url: str
    read_at: str
    output_limit_default: int
    request_defaults: Mapping[str, Any]
    base_url: str = DEFAULT_BASE_URL
    upstream_timeout_s: int = DEFAULT_TIMEOUT_S
    cached_input_per_mtok: Decimal | None = None
    cache_write_per_mtok: Decimal | None = None
    translate_max_tokens: bool = False     # the gateway drops a null max_tokens and renames a set one (a departure; see hosted_block)

    def redact(self, text: str) -> str:
        """Replace the key file's path and the ledger's path in a text (longest first, so a path inside the other is safe)."""
        for value, label in sorted(((self.key_file, "<key_file>"), (self.ledger_dir, "<ledger>")), key=lambda t: -len(t[0])):
            text = text.replace(value, label)
        return text


def _reject_constant(name: str) -> Any:
    raise ProfileError(f"profile: {name} is not a number JSON allows")


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ProfileError(f"profile: the key {key!r} is given twice")
        out[key] = value
    return out


def _money(profile: Mapping[str, Any], key: str, *, positive: bool, optional: bool = False) -> Decimal | None:
    if key not in profile or profile[key] is None:
        if optional:
            return None
        raise ProfileError(f"profile: {key} is required")
    value = profile[key]
    if isinstance(value, bool):
        raise ProfileError(f"profile: {key} must be a number")
    if isinstance(value, str):
        if not MONEY_RE.match(value):
            raise ProfileError(f"profile: {key} must be a plain decimal such as \"0.10\"")
        number = Decimal(value)
    elif isinstance(value, (int, Decimal)):
        number = Decimal(value)
    else:
        raise ProfileError(f"profile: {key} must be a number or a decimal string")
    if not number.is_finite() or number < 0 or (positive and number == 0):
        raise ProfileError(f"profile: {key} must be {'greater than' if positive else 'at least'} zero")
    if len(number.as_tuple().digits) > MAX_DIGITS:
        raise ProfileError(f"profile: {key} has more than {MAX_DIGITS} digits")
    if number and not -9 <= number.adjusted() <= 6:       # nothing real is below 1e-9 or above 10 million (a misread unit)
        raise ProfileError(f"profile: {key} is outside the range 0.000000001 to 9999999")
    return number


def _whole(profile: Mapping[str, Any], key: str, *, default: int | None = None, maximum: int | None = None) -> int:
    if key not in profile:
        if default is None:
            raise ProfileError(f"profile: {key} is required")
        return default
    value = profile[key]
    if isinstance(value, Decimal) and value == value.to_integral_value():
        value = int(value)
    if isinstance(value, bool) or not isinstance(value, int) or value < 1 or (maximum is not None and value > maximum):
        raise ProfileError(f"profile: {key} must be a whole number of at least 1" + (f" and at most {maximum}" if maximum else ""))
    return value


def _flag(profile: Mapping[str, Any], key: str) -> bool:
    value = profile.get(key, False)
    if not isinstance(value, bool):
        raise ProfileError(f"profile: {key} must be true or false")
    return value


def _path(profile: Mapping[str, Any], key: str) -> str:
    value = profile.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ProfileError(f"profile: {key} is required and must be a path")
    if KEY_LIKE_RE.match(value) or value.startswith("sk-"):
        raise ProfileError(f"profile: {key} looks like a key, not a path (the profile holds the path of a file)")
    if any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise ProfileError(f"profile: {key} holds a control character")
    if not os.path.isabs(value) or not Path(value).name:
        raise ProfileError(f"profile: {key} must be an absolute path to a file or directory (not the root)")
    return value


def _base_url(profile: Mapping[str, Any]) -> str:
    value = profile.get("base_url", DEFAULT_BASE_URL)
    if not isinstance(value, str) or not value.strip():
        raise ProfileError("profile: base_url must be a URL")
    parts = urlsplit(value.strip())
    if parts.scheme not in ("http", "https") or not parts.hostname or parts.query or parts.fragment or "@" in parts.netloc:
        raise ProfileError("profile: base_url must be an http(s) URL without credentials, query or fragment")
    if parts.scheme == "http" and parts.hostname not in ("127.0.0.1", "localhost", "::1"):
        raise ProfileError("profile: base_url may use plain http only towards a loopback host (the key would travel in clear)")
    return value.strip().rstrip("/")


def _request_defaults(profile: Mapping[str, Any]) -> dict[str, Any]:
    value = profile.get("request_defaults")
    if not isinstance(value, dict):
        raise ProfileError("profile: request_defaults is required and must be an object (it may be empty)")
    out: dict[str, Any] = {}
    for name, item in value.items():
        if not pc.KEY_RE.match(name):
            raise ProfileError("profile: a request_defaults name is made of letters, digits, _ and - only")
        if name in PROTECTED_REQUEST_FIELDS:
            raise ProfileError(f"profile: request_defaults may not set {name} (the gateway refuses it)")
        try:
            pc.toml_value(item)
        except pc.PassAError:
            raise ProfileError(f"profile: request_defaults.{name} must be a boolean, number, string or object of those") from None
        out[name] = item
    return out


def load_profile(path: str | Path) -> Profile:
    """Read and validate a profile. Refuses anything missing, unknown or odd, and never echoes a value of any field."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ProfileError(f"profile: cannot read {Path(path).name} ({type(exc).__name__})") from None
    try:
        raw = json.loads(text, parse_float=Decimal, parse_constant=_reject_constant, object_pairs_hook=_no_duplicates)
    except json.JSONDecodeError:
        raise ProfileError("profile: not valid JSON") from None
    if not isinstance(raw, dict):
        raise ProfileError("profile: must be a JSON object")
    unknown = sorted(set(raw) - set(ALLOWED_KEYS))
    if unknown:
        raise ProfileError(f"profile: unknown key(s) {', '.join(map(repr, unknown))} (a typo would otherwise be ignored)")
    missing = [k for k in REQUIRED_KEYS if k not in raw]
    if missing:
        raise ProfileError(f"profile: missing {', '.join(missing)}")
    source_url = raw["source_url"]
    if not isinstance(source_url, str) or not re.match(r"^https?://\S+$", source_url):
        raise ProfileError("profile: source_url must be the http(s) URL of the page the prices were read from")
    read_at = raw["read_at"]
    if not isinstance(read_at, str) or not DATE_RE.match(read_at):
        raise ProfileError("profile: read_at must be UTC like \"20261102 20:20\"")
    return Profile(
        key_file=_path(raw, "key_file"),
        ledger_dir=_path(raw, "ledger_dir"),
        allowance_usd=_money(raw, "allowance_usd", positive=True),
        # a hosted model is not free: a zero here would make every call cost nothing and the cap meaningless
        input_per_mtok=_money(raw, "input_per_mtok", positive=True),
        output_per_mtok=_money(raw, "output_per_mtok", positive=True),
        cached_input_per_mtok=_money(raw, "cached_input_per_mtok", positive=False, optional=True),
        cache_write_per_mtok=_money(raw, "cache_write_per_mtok", positive=False, optional=True),
        source_url=source_url,
        read_at=read_at,
        output_limit_default=_whole(raw, "output_limit_default"),
        request_defaults=_request_defaults(raw),
        base_url=_base_url(raw),
        upstream_timeout_s=_whole(raw, "upstream_timeout_s", default=DEFAULT_TIMEOUT_S, maximum=86400),
        translate_max_tokens=_flag(raw, "translate_max_tokens"),
    )


def add_hosted_argument(parser: Any) -> None:
    """The `--hosted-profile PATH` option the four pass-B runners share."""
    parser.add_argument("--hosted-profile", metavar="PATH",
                        help="pass B: serve the CHAT model (--model) from the hosted provider described in this JSON profile "
                             "(see passb_profile.example.json); --upstream-url and --embed-model stay the LOCAL embedding "
                             "upstream; the key is read by the gateway alone, from the file the profile names")


def profile_from_args(args: Any) -> Profile | None:
    path = getattr(args, "hosted_profile", None)
    return load_profile(path) if path else None


# ---- the ledger -------------------------------------------------------------------------------------------------
def read_ledger(path: Path, *, strict: bool, start: int = 0) -> list[dict]:
    """The JSON objects of a gateway log from byte `start` on, in order. `strict` (at start, with no gateway writing)
    refuses a line that is not JSON, as the gateway would; not strict (while a gateway may be writing), an unfinished last
    line is left for later. A run reads its own lines only (`start` is the file's size when the run began), so an earlier
    stage's lines, even a damaged one, are never parsed again."""
    try:
        with open(path, "rb") as handle:
            handle.seek(start)
            data = handle.read()
    except FileNotFoundError:
        return []
    lines = data.split(b"\n")
    if lines[-1] == b"":
        lines.pop()
    elif not strict:
        lines.pop()                      # a write still in progress
    out = []
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            raise pc.PassAError(f"the ledger's line {number} is not valid JSON; the gateway would refuse to continue it") from None
        if not isinstance(obj, dict):
            raise pc.PassAError(f"the ledger's line {number} is not a JSON object")
        out.append(obj)
    return out


def _size(path: Path) -> int:
    try:
        return Path(path).stat().st_size
    except FileNotFoundError:
        return 0


# ---- the gateway ------------------------------------------------------------------------------------------------
class HostedGateway(pc.LocalGateway):
    """The metering gateway as a subprocess with two upstreams: the hosted provider for the chat model and the local server
    for the embedding model. The same API as `passa_common.LocalGateway`; see this module's docstring for what is promised.
    `models` is `[chat_model, embedding_model]`, in that order."""

    def __init__(self, workdir: str | Path, upstream_base_url: str, models: Iterable[str], repo_root: str | Path,
                 *, profile: Profile, source_url: str = "https://ollama.com/library",
                 request_defaults: Mapping[str, Mapping[str, Any]] | None = None):
        names = list(models)
        if len(names) != 2 or names[0] == names[1]:
            raise pc.PassAError("a hosted gateway serves exactly two different models: the chat model, then the embedding model")
        for name in names:
            if not NAME_RE.match(name):
                raise pc.PassAError("a model name may hold only letters, digits and . _ : / -")
        given = {m: dict(d) for m, d in (request_defaults or {}).items() if d}
        unknown = sorted(set(given) - set(names))
        if unknown:
            raise pc.PassAError(f"request defaults given for models the gateway does not serve: {unknown}")
        chat, embed = names
        merged = {chat: {**profile.request_defaults, **given.get(chat, {})}}   # a command-line option wins over the profile
        if embed in given:
            merged[embed] = given[embed]
        protected = sorted(set(merged[chat]) & PROTECTED_REQUEST_FIELDS)
        if protected:
            raise pc.PassAError(f"request defaults may not set {protected}")
        super().__init__(workdir, upstream_base_url, names, repo_root, timeout_s=profile.upstream_timeout_s,
                         source_url=source_url, request_defaults={m: d for m, d in merged.items() if d})
        self.profile = profile
        self.chat_model, self.embed_model = chat, embed
        self.ledger_dir = Path(profile.ledger_dir)
        try:
            inside = self.ledger_dir.resolve().is_relative_to(self.repo_root.resolve())
        except OSError:
            inside = False
        if inside:
            raise pc.PassAError("the ledger directory is inside the repository; its body log holds article text")
        self.log_path = self.ledger_dir / LEDGER_LOG
        self.body_path = self.ledger_dir / LEDGER_BODIES
        self.records_before: int | None = None
        self.log_offset = self.body_offset = 0       # where this run's lines begin in the shared log and body log
        self.spent_before: Decimal | None = None
        self.cap: Decimal | None = None
        self.resumed: bool | None = None
        self.gateway_started = False        # True once the gateway has printed that it is listening

    # -- config ------------------------------------------------------------------------------------------------
    def write_config(self) -> Path:
        p = self.profile
        if self.cap is None:
            raise pc.PassAError("the cap is computed from the ledger when the gateway starts")
        self.workdir.mkdir(parents=True, exist_ok=True)
        j = json.dumps
        lines = [
            "[gateway]",
            f"currency = {j(CURRENCY)}",
            f"cap = {money_text(self.cap)}",
            "default_max_output_tokens = 4096",
            "input_bytes_per_token = 2",
            f"upstream_timeout_s = {p.upstream_timeout_s}",
            "port = 8089",
            f"log_file = {j(str(self.log_path))}",
            "log_bodies = true",
            "",
            f"[upstreams.{HOSTED}]",
            'protocol = "openai"',
            f"base_url = {j(p.base_url)}",
            f"key_file = {j(p.key_file)}",
            "allow_request_defaults = true",
            "",
            f"[upstreams.{LOCAL}]",
            'protocol = "openai"',
            f"base_url = {j(self.upstream)}",
            'key_env = "PASSA_UNUSED_KEY"',
            "dry_run = true",
            "",
            f"[models.{j(self.chat_model)}]",
            f"upstream = {j(HOSTED)}",
            f"input_per_mtok = {money_text(p.input_per_mtok)}",
            f"output_per_mtok = {money_text(p.output_per_mtok)}",
        ]
        if p.cached_input_per_mtok is not None:
            lines.append(f"cached_input_per_mtok = {money_text(p.cached_input_per_mtok)}")
        if p.cache_write_per_mtok is not None:
            lines.append(f"cache_write_per_mtok = {money_text(p.cache_write_per_mtok)}")
        lines += [f"output_limit_default = {p.output_limit_default}",
                  f"source_url = {j(p.source_url)}",
                  f"read_at = {j(p.read_at)}"]
        if p.translate_max_tokens:
            lines.append("translate_max_tokens = true")
        if self.request_defaults.get(self.chat_model):
            lines += ["", f"[models.{j(self.chat_model)}.request_defaults]"]
            lines += [f"{k} = {pc.toml_value(v)}" for k, v in self.request_defaults[self.chat_model].items()]
        lines += ["", f"[models.{j(self.embed_model)}]",
                  f"upstream = {j(LOCAL)}",
                  "input_per_mtok = 0",
                  "output_per_mtok = 0",
                  f"source_url = {j(self.source_url)}",
                  f"read_at = {j(datetime.now(timezone.utc).strftime('%Y%m%d %H:%M'))}"]
        if self.request_defaults.get(self.embed_model):
            lines += ["", f"[models.{j(self.embed_model)}.request_defaults]"]
            lines += [f"{k} = {pc.toml_value(v)}" for k, v in self.request_defaults[self.embed_model].items()]
        cfg = self.workdir / "gateway.toml"
        cfg.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return cfg

    # -- life cycle --------------------------------------------------------------------------------------------
    def _redact(self, text: str) -> str:
        return self.profile.redact(text)

    def start(self) -> "HostedGateway":
        self.ledger_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        existing = read_ledger(self.log_path, strict=True)
        self.records_before = len(existing)
        self.log_offset, self.body_offset = _size(self.log_path), _size(self.body_path)
        self.spent_before = sum_costs(existing)
        cap = self.spent_before + self.profile.allowance_usd
        if len(cap.as_tuple().digits) > MAX_DIGITS:
            raise pc.PassAError(f"the cap would have more than {MAX_DIGITS} digits; the gateway refuses such a number")
        self.cap = cap
        self.resumed = self.log_offset > 0       # the gateway's own test for "the log holds records": a file that is not empty
        cfg = self.write_config()
        command = [sys.executable, str(self.repo_root / "tools" / "metering_gateway.py"), "--config", str(cfg), "--port", "0"]
        if self.resumed:
            command.append("--resume")
        self.proc = subprocess.Popen(command, cwd=self.workdir, env=dict(GATEWAY_ENV), stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, text=True)
        deadline = time.time() + 60
        while time.time() < deadline:
            line = self.proc.stdout.readline()
            self.output += line
            m = re.search(r"listening on http://127\.0\.0\.1:(\d+)", line)
            if m:
                self.port = int(m.group(1))
                self.gateway_started = True
                # The banner goes on with one line per upstream, in the same flush. Read them now: a later communicate()
                # cannot see what readline() has already pulled into its buffer, and `output` is scanned for leaks.
                for _ in range(2):
                    self.output += self.proc.stdout.readline()
                return self
            if not line and self.proc.poll() is not None:
                break
        self.stop()
        raise pc.PassAError(f"the gateway did not start: {self._redact(self.output.strip())[-300:]}")

    def __enter__(self) -> "HostedGateway":
        return self.start()

    # -- what this run did -------------------------------------------------------------------------------------
    def run_records(self) -> list[dict]:
        """The log records this run added (not the earlier stages'), in arrival order, without bodies."""
        if self.records_before is None:
            raise pc.PassAError("the gateway was not started")
        return read_ledger(self.log_path, strict=False, start=self.log_offset)

    def calls(self) -> list[dict]:
        """One dict per call THIS run made, in arrival order: the log record, plus the request and response from the body log."""
        return self._with_bodies(self.run_records())

    def _with_bodies(self, records: list[dict]) -> list[dict]:
        wanted = {r.get("call_id") for r in records}
        bodies = {b["call_id"]: b for b in read_ledger(self.body_path, strict=False, start=self.body_offset)
                  if b.get("call_id") in wanted}
        out = []
        for r in records:
            b = bodies.get(r.get("call_id"), {})
            out.append({**r, "request": pc._maybe_json(b.get("request")), "response": pc._maybe_json(b.get("response"))})
        return out

    def hosted_block(self) -> dict:
        """What a runner's result JSON records about the hosted side. It holds no key, no key-file path and no ledger path."""
        p = self.profile
        block: dict[str, Any] = {
            "chat_upstream": HOSTED, "embedding_upstream": LOCAL, "chat_model": self.chat_model,
            "embedding_model": self.embed_model, "hosted_base_url": p.base_url, "currency": CURRENCY,
            "key_file": "set", "ledger": "shared",
            "allowance_usd": money_text(p.allowance_usd),
            "prices": {"unit": "per million tokens", "input_per_mtok": money_text(p.input_per_mtok),
                       "output_per_mtok": money_text(p.output_per_mtok),
                       "cached_input_per_mtok": None if p.cached_input_per_mtok is None else money_text(p.cached_input_per_mtok),
                       "cache_write_per_mtok": None if p.cache_write_per_mtok is None else money_text(p.cache_write_per_mtok),
                       "source_url": p.source_url, "read_at": p.read_at},
            "output_limit_default": p.output_limit_default,
            "translate_max_tokens": p.translate_max_tokens,
            "departures_from_the_builders_requests": (
                ["max_tokens: null is dropped and a set max_tokens is sent as max_completion_tokens (the model rejects both)"]
                if p.translate_max_tokens else []),
            "request_defaults_names": sorted(self.request_defaults.get(self.chat_model, {})),
            "request_defaults": dict(self.request_defaults.get(self.chat_model, {})),
            "upstream_timeout_s": p.upstream_timeout_s,
        }
        if self.records_before is None or not self.gateway_started:
            block["started"] = False
            return block
        records = self.run_records()
        calls = self._with_bodies(records)
        chat = [c for c in calls if str(c.get("route", "")).endswith("chat/completions")]
        block.update({
            "started": True,
            "resumed_an_existing_ledger": self.resumed,
            "model_reported": dict(Counter(str(c.get("model_reported")) for c in chat)),
            "cost_usd": cost_usd(calls),
            "spent_before_usd": money_text(self.spent_before),
            "cap_usd": money_text(self.cap),
            "ledger_records_before": self.records_before,
            "ledger_records_after": self.records_before + len(calls),
            "calls_in_this_run": len(calls),
            "run_records_sha256": hashlib.sha256(
                "\n".join(json.dumps(r, sort_keys=True) for r in records).encode("utf-8")).hexdigest(),
            "response_facts": pc.response_facts(calls),
        })
        return block


def hosted_block_for(gw: Any) -> dict:
    """The `hosted` block of a result JSON, or just the name of the error when it cannot be built. Never raises: a result
    file must still be written when the ledger cannot be read."""
    try:
        return gw.hosted_block()
    except Exception as exc:  # noqa: BLE001 - recorded by name only
        return {"error": type(exc).__name__}


def make_gateway(profile: Profile | None, workdir: str | Path, upstream_url: str, models: Iterable[str],
                 repo_root: str | Path, *, timeout_s: int | None = None,
                 request_defaults: Mapping[str, Mapping[str, Any]] | None = None) -> pc.LocalGateway:
    """The gateway a runner uses: `LocalGateway` exactly as in pass A without a profile, `HostedGateway` with one. In hosted
    mode the profile's `upstream_timeout_s` replaces the runner's own timeout (one setting serves both upstreams)."""
    if profile is None:
        extra = {} if timeout_s is None else {"timeout_s": timeout_s}
        return pc.LocalGateway(workdir, upstream_url, models, repo_root, request_defaults=request_defaults, **extra)
    return HostedGateway(workdir, upstream_url, models, repo_root, profile=profile, request_defaults=request_defaults)


# ---- the embedding upstream -------------------------------------------------------------------------------------
def embedding_preflight(upstream_url: str, embed_model: str, mode: str = "auto") -> dict:
    """Pass B has no chat model in Ollama, so only the embedding model is checked: is it installed (`/api/tags`)?
    `auto`: check when the server answers like Ollama, record a skip when it does not; `require`: an error when it does
    not answer; `skip`: nothing. Raises PassAError when the server answers and the model is not installed."""
    if mode not in ("auto", "require", "skip"):
        raise pc.PassAError(f"preflight mode {mode!r}: use auto, require or skip")
    if mode == "skip":
        return {"mode": "skip"}
    root = re.sub(r"/v1/?$", "", upstream_url.rstrip("/"))
    try:
        tags = pc._http_json(f"{root}/api/tags", timeout=10)
        models = tags.get("models") if isinstance(tags, dict) else None
        if not isinstance(models, list):
            raise pc.PassAError("no model list")
    except pc.PassAError:
        if mode == "require":
            raise pc.PassAError("--preflight require, but the embedding upstream does not answer Ollama's /api/tags") from None
        return {"mode": mode, "ollama": False, "skipped": "no Ollama-style answer at /api/tags",
                "chat_model_checked": False}
    names = {m.get("name") or m.get("model") for m in models if isinstance(m, dict)}
    if embed_model not in names and f"{embed_model}:latest" not in names:
        raise pc.PassAError(f"not installed in Ollama: {embed_model}; installed: {sorted(n for n in names if n)}")
    return {"mode": mode, "ollama": True, "embed_model": embed_model, "embedding_model_installed": True,
            "chat_model_checked": False, "note": "the chat model is hosted; its context is the provider's"}
