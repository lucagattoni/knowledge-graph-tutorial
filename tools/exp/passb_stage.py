"""Pass B (the paid pilot): the stage driver. It runs ONE stage of the ladder (B, C or D) for the builders you name, one
after another, with the free pre-flight before each and the watchdog beside each. Plan: kb-kg/experiments/x2-index-cost/
pass-b-plan.md ("The ladder", items F4 and F7 wired together). It is the only thing to run for stages B, C and D.

    python tools/exp/passb_stage.py --stage B --builder lightrag --builder fast --builder ms --builder nano \\
        --profile PROFILE.json --builders-config BUILDERS.json --out-dir OUT_DIR              # a DRY RUN: starts nothing
    python tools/exp/passb_stage.py ... --send                                                 # the real thing

Stage C is run twice by the coordinator, with `--run-label r1` and then `--run-label r2` (the plan's pre-registered second run).
A run label that already has a directory under OUT_DIR is refused, so a stage is never repeated by accident.

**Without `--send` nothing is started and nothing is written**: the program prints the pre-flight table for each builder
(projected, as if each earlier builder spent its central estimate), each runner's command line, the environment it would get,
the key file's path as given, the allowance and the stop-at, and exits 0 (1 when the pre-flight would refuse). `--send` is
required to start any process. The key file is never opened by this program; only the gateway, started by the runner, reads it.

What `--send` does, per builder, in the order given (stage -> runner checkpoints: B `1`, C `5`, D `20`):

 1. Pre-flight (`passb_preflight.check`, with the profile's prices): the ledger's spend (`ledger_dir/meter.jsonl`) and this
    stage's spend so far, which is the ledger's spend now minus `spent_start` in the state file `ledger_dir/stage_<STAGE>.json`
    (`{"started_utc", "spent_start", "runs"}`, written when the stage's first runner starts). A refusal is written to the stage
    report and the program exits 1 BEFORE anything starts. The profile's own `allowance_usd` is not used: the pre-flight's
    allowance replaces it.
 2. The run profile `OUT_DIR/<label>/profile.json` (mode 600): the stage profile with `allowance_usd` set to the pre-flight's
    allowance; `key_file` and `ledger_dir` unchanged. `<label>` is `<STAGE>-<run label>-<builder>`, for example `C-r2-nano`.
 3. The runner, in its OWN SESSION (its process-group id is its pid, so the watchdog can stop it and everything it started),
    with exactly the environment of the builders config plus `PATH`, never the parent's; `--hosted-profile` the run profile,
    `--workdir OUT_DIR/<label>/work` (must not exist), `--out OUT_DIR/<label>/result.json`, the stage's checkpoints and the
    config's extra arguments. Its stdout and stderr go to files in `OUT_DIR/<label>/` (mode 600).
 4. The watchdog beside it: `--gateway-dir LEDGER --stop-at-usd STOP_AT --since STAGE_STARTED --kill-pgid RUNNER_PID --report
    OUT_DIR/<label>/watchdog.json --poll-s 5` (`--poll-s` of this program changes the 5; the tests use 0.2). `--since` makes the
    stage's spend and counts cumulative across its runs while ignoring earlier stages. `--repeat-since` is THIS RUN's start:
    the repeat rule looks for a retry loop, and stage C's second run sends the first run's requests again by design (found by
    the dress rehearsal: without it the second run was stopped within a second).
 5. Wait for the runner. The runner's exit gives the watchdog its last read: the live watchdog is stopped, any process the
    runner left behind in its group is terminated, and the whole stage's log is read ONCE more with the same rules
    (`passb_watchdog.py --max-seconds 0`), so a call written in the last seconds before the runner exited cannot slip past a
    poll. A rule that fired (exit status 3 of the watchdog, live or last read): the next builder is NOT started, the report is
    written, the program exits 3. A runner that exits non-zero with no trip is the builder's own failure: it is recorded as a
    result and the next builder runs. The watchdog ending by itself while the runner lives (an unguarded run) kills the runner
    and counts as a trip (outcome `guard_failed`, exit 3).
 6. The state file and `OUT_DIR/stage_report.json` are updated: stage, label, builder, exit status, tripped rules (names and
    counts only), allowance, stop-at, spend of this run (the ledger's delta, exact), the result file's name, UTC times. No path
    outside OUT_DIR and no text from any request or response appears in a report.

Exit status: 0 every builder ran (own failures allowed, recorded); 1 refused by the pre-flight, or a usage or config error
(nothing started), or a runner that could not be started; 3 a watchdog trip or a guard failure; 128+N the program was stopped by
signal N (SIGINT, SIGTERM): the runner's group and the watchdog are stopped first. Two stage drivers on one ledger would make the
gateway's cap stale; a lock (`ledger_dir/stage.lock`, `flock`, released when the program ends) refuses the second.

The builders config is a JSON file outside the repository (`passb_builders.example.json` shows its shape with placeholders):
`repo_root`, `corpus`, `documents`, `local_upstream_url` (Ollama, for the embedding model), `embed_model`, `chat_model` and
`builders`: per builder (`lightrag`, `fast`, `ms`, `nano`) `python` (the interpreter of its throwaway environment), `runner` (a
file name in `tools/exp`), `isolated` (pass `-I`), `env` (the ONLY environment the runner gets; `PATH` is added, so it may not be
given; a name that looks like a credential is refused), `tiktoken_cache` and `extra_args` (the concurrency and timeout flags;
none of the flags the driver sets itself). An unknown or missing key, a duplicate key, a path that does not exist and a profile,
config, ledger or out directory inside the repository are refused.

Known limits. Stages must be run in order; if a later stage's window were open, an earlier stage's spend would be overstated (safe
side). After a trip the stage's window stays open, so running the stage again counts the tripped run's calls again and trips at
once. To repeat a stage after a fault (the plan allows one, with the cause fixed and written down) move `ledger_dir/stage_<STAGE>.json`
aside, for example to `stage_B.json.tripped-1`: with no state file the next invocation opens a new window at the ledger's spend
then, so the stage limit and the watchdog's counts start again while the total cap still counts everything. Use a new `--run-label`.
SIGKILL of this program cannot be caught:
the runner and the watchdog then go on, the watchdog still guarding the runner.

Standard library only; money is Decimal throughout.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import shlex
import signal
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit

sys.dont_write_bytecode = True  # importing must not leave .pyc files in the repository
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import passa_common as pc  # noqa: E402
import passb_common as pb  # noqa: E402
import passb_preflight as pf  # noqa: E402
import passb_watchdog as wd  # noqa: E402

STAGE_CHECKPOINTS = {"B": "1", "C": "5", "D": "20"}
BUILDERS = pf.BUILDER_ORDER                       # lightrag, fast, ms, nano
RUNNER_PATH = "/usr/bin:/bin:/opt/homebrew/bin"   # added to every runner's environment
HELPER_ENV = {"PATH": "/usr/bin:/bin"}            # the watchdog needs Python and `ps`, nothing else
EXIT_OK, EXIT_REFUSED, EXIT_TRIPPED = 0, 1, wd.EXIT_TRIPPED
LOCK_NAME = "stage.lock"
REPORT_NAME = "stage_report.json"
DEFAULT_POLL_S = 5.0
LABEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,31}$")
ENV_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,63}$")
RUNNER_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+\.py$")
CREDENTIAL_WORDS = frozenset({"KEY", "TOKEN", "SECRET", "PASSWORD", "PASSWD", "CREDENTIAL", "CREDENTIALS", "AUTH", "APIKEY"})
# What the driver sets itself; a config may not set them again in `extra_args`.
OWNED_FLAGS = frozenset({"--corpus", "--documents", "--repo-root", "--upstream-url", "--model", "--embed-model",
                         "--hosted-profile", "--workdir", "--out", "--checkpoints", "--tiktoken-cache", "--stub-shape"})
BUILDER_KEYS = ("python", "runner", "isolated", "env", "tiktoken_cache", "extra_args")
CONFIG_KEYS = ("repo_root", "corpus", "documents", "local_upstream_url", "embed_model", "chat_model", "builders")
KNOWN_RULES = frozenset(wd.RULE_ORDER) | {"watchdog_error"}
KILL_WORDS = frozenset({"terminated", "killed", "already_gone", "signal_failed", "survived", "pending"})
COUNT_VALUE_RE = re.compile(r"^-?\d+(\.\d+)?$")
COUNT_NAME_RE = re.compile(r"^[a-z_]{1,40}$")
TRIP_WAIT_S = 30.0           # a watchdog that has written its report is given this long to finish stopping the group
GROUP_GRACE_S = 10.0         # SIGTERM to SIGKILL for a group this program stops itself
STOP_WAIT_S = 15.0           # how long a runner may take to go once its group was signalled, before it is killed by itself


class ConfigError(pc.PassAError):
    """A usage or config error: nothing was started. A message names a key, never a value."""


class Interrupted(BaseException):
    """SIGINT or SIGTERM reached this program."""

    def __init__(self, signum: int):
        super().__init__(signum)
        self.signum = signum


# ---- small helpers -------------------------------------------------------------------------------------------------
def utc_stamp() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"


def label_for(stage: str, run_label: str, builder: str) -> str:
    return f"{stage}-{run_label}-{builder}"


def write_json_atomic(path: Path, payload: Any) -> None:
    tmp = path.with_name(path.name + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, indent=1, sort_keys=True) + "\n")
    os.replace(tmp, path)


def _private_file(path: Path, *, append: bool = False):
    flags = os.O_WRONLY | os.O_CREAT | (os.O_APPEND if append else os.O_EXCL)
    return os.fdopen(os.open(path, flags, 0o600), "ab")


def _inside(path: Path, root: Path) -> bool:
    try:
        return path.resolve().is_relative_to(root.resolve())
    except OSError:
        return False


# ---- the builders config -------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class BuilderConfig:
    python: str
    runner: str
    isolated: bool
    env: Mapping[str, str]
    tiktoken_cache: str
    extra_args: tuple[str, ...]


@dataclass(frozen=True)
class Config:
    repo_root: str
    corpus: str
    documents: str
    local_upstream_url: str
    embed_model: str
    chat_model: str
    builders: Mapping[str, BuilderConfig]


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ConfigError(f"builders config: the key {key!r} is given twice")
        out[key] = value
    return out


def _only(obj: Any, required: Sequence[str], where: str) -> dict:
    if not isinstance(obj, dict):
        raise ConfigError(f"{where}: must be a JSON object")
    unknown = sorted(set(obj) - set(required))
    if unknown:
        raise ConfigError(f"{where}: unknown key(s) {', '.join(map(repr, unknown))} (a typo would otherwise be ignored)")
    missing = [k for k in required if k not in obj]
    if missing:
        raise ConfigError(f"{where}: missing {', '.join(missing)}")
    return obj


def _text(obj: Mapping[str, Any], key: str, where: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{where}.{key}: a non-empty text is required")
    if any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise ConfigError(f"{where}.{key}: holds a control character")
    return value


def _abs(obj: Mapping[str, Any], key: str, where: str, *, kind: str | None = None) -> str:
    value = _text(obj, key, where)
    if not os.path.isabs(value):
        raise ConfigError(f"{where}.{key}: an absolute path is required")
    if value.startswith("sk-") or pb.KEY_LIKE_RE.match(value):
        raise ConfigError(f"{where}.{key}: looks like a key, not a path")
    if kind == "dir" and not os.path.isdir(value):
        raise ConfigError(f"{where}.{key}: not a directory")
    if kind == "file" and not os.path.isfile(value):
        raise ConfigError(f"{where}.{key}: not a file")
    return value


def _env(value: Any, where: str) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ConfigError(f"{where}.env: must be a JSON object of text values")
    out: dict[str, str] = {}
    for name, item in value.items():
        if not ENV_NAME_RE.match(name):
            raise ConfigError(f"{where}.env: a variable name is letters, digits and _ only")
        if name == "PATH":
            raise ConfigError(f"{where}.env: PATH is set by the driver and may not be given")
        if CREDENTIAL_WORDS & set(name.upper().split("_")):
            raise ConfigError(f"{where}.env: {name} looks like a credential; the runner never gets one")
        if not isinstance(item, str) or len(item) > 1000 or any(ord(c) < 32 or ord(c) == 127 for c in item):
            raise ConfigError(f"{where}.env.{name}: a text of at most 1000 characters without control characters is required")
        if item.startswith("sk-") or pb.KEY_LIKE_RE.match(item):
            raise ConfigError(f"{where}.env.{name}: looks like a key")
        out[name] = item
    return out


def _extra_args(value: Any, where: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ConfigError(f"{where}.extra_args: must be a list of texts")
    for item in value:
        if not isinstance(item, str) or not item or any(ord(c) < 32 or ord(c) == 127 for c in item):
            raise ConfigError(f"{where}.extra_args: every item is a non-empty text without control characters")
        if item.split("=", 1)[0] in OWNED_FLAGS:
            raise ConfigError(f"{where}.extra_args: {item.split('=', 1)[0]} is set by the driver itself")
        if item.startswith("sk-"):
            raise ConfigError(f"{where}.extra_args: an item looks like a key")
    return tuple(value)


def _loopback_url(value: str, where: str) -> str:
    parts = urlsplit(value.strip())
    if parts.scheme not in ("http", "https") or parts.hostname not in ("127.0.0.1", "localhost", "::1") \
            or parts.query or parts.fragment or "@" in parts.netloc:
        raise ConfigError(f"{where}: a loopback http(s) URL without credentials is required (the embedding server is local)")
    return value.strip()


def load_config(path: str | Path) -> Config:
    """Read and validate the builders config. Refuses anything unknown, missing, duplicated or odd; names keys, never values."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ConfigError(f"builders config: cannot read {Path(path).name} ({type(exc).__name__})") from None
    try:
        raw = json.loads(text, object_pairs_hook=_no_duplicate_keys)
    except json.JSONDecodeError:
        raise ConfigError("builders config: not valid JSON") from None
    raw = _only(raw, CONFIG_KEYS, "builders config")
    repo_root = _abs(raw, "repo_root", "config", kind="dir")
    if not os.path.isfile(os.path.join(repo_root, "tools", "metering_gateway.py")):
        raise ConfigError("config.repo_root: tools/metering_gateway.py is not there")
    corpus = _abs(raw, "corpus", "config", kind="file")
    documents = _abs(raw, "documents", "config", kind="file")
    url = _loopback_url(_text(raw, "local_upstream_url", "config"), "config.local_upstream_url")
    chat, embed = _text(raw, "chat_model", "config"), _text(raw, "embed_model", "config")
    for key, name in (("chat_model", chat), ("embed_model", embed)):
        if not pb.NAME_RE.match(name):
            raise ConfigError(f"config.{key}: a model name may hold only letters, digits and . _ : / -")
    if chat == embed:
        raise ConfigError("config: chat_model and embed_model must differ")
    builders_raw = raw["builders"]
    if not isinstance(builders_raw, dict) or not builders_raw:
        raise ConfigError("config.builders: a non-empty JSON object is required")
    unknown = sorted(set(builders_raw) - set(BUILDERS))
    if unknown:
        raise ConfigError(f"config.builders: unknown builder(s) {', '.join(map(repr, unknown))}; choose from {', '.join(BUILDERS)}")
    builders: dict[str, BuilderConfig] = {}
    for name in BUILDERS:
        if name not in builders_raw:
            continue
        where = f"builders.{name}"
        item = _only(builders_raw[name], BUILDER_KEYS, where)
        python = _abs(item, "python", where, kind="file")
        if not os.access(python, os.X_OK):
            raise ConfigError(f"{where}.python: not executable")
        runner = _text(item, "runner", where)
        if not RUNNER_NAME_RE.match(runner):
            raise ConfigError(f"{where}.runner: a file name in tools/exp (letters, digits, _ . - and .py)")
        if not os.path.isfile(os.path.join(repo_root, "tools", "exp", runner)):
            raise ConfigError(f"{where}.runner: not a file in tools/exp")
        if not isinstance(item["isolated"], bool):
            raise ConfigError(f"{where}.isolated: true or false is required")
        builders[name] = BuilderConfig(python, runner, item["isolated"], _env(item["env"], where),
                                       _abs(item, "tiktoken_cache", where, kind="dir"), _extra_args(item["extra_args"], where))
    return Config(repo_root, corpus, documents, url, embed, chat, builders)


# ---- the plan: what this invocation will do ------------------------------------------------------------------------
@dataclass(frozen=True)
class Plan:
    stage: str
    builders: tuple[str, ...]
    run_label: str
    out_dir: Path
    poll_s: float

    def label(self, builder: str) -> str:
        return label_for(self.stage, self.run_label, builder)

    def label_dir(self, builder: str) -> Path:
        return self.out_dir / self.label(builder)


def make_plan(args: argparse.Namespace, config: Config, profile: pb.Profile) -> Plan:
    stage = args.stage
    builders = tuple(args.builder)
    if len(set(builders)) != len(builders):
        raise ConfigError("a builder is named twice; a second run of a stage is a separate invocation with its own --run-label")
    for name in builders:
        if name not in config.builders:
            raise ConfigError(f"builder {name!r} is not in the builders config")
    if not LABEL_RE.match(args.run_label):
        raise ConfigError("--run-label: letters, digits, . _ - only (at most 32, starting with a letter or digit)")
    if not args.poll_s > 0:
        raise ConfigError("--poll-s must be positive")
    repo = Path(config.repo_root)
    out_dir = Path(args.out_dir).expanduser().absolute()
    for what, path in (("--out-dir", out_dir), ("--profile", Path(args.profile)), ("--builders-config", Path(args.builders_config)),
                       ("the profile's ledger_dir", Path(profile.ledger_dir))):
        if _inside(path, repo):
            raise ConfigError(f"{what} is inside the repository; it holds local paths or article text, so it must be outside")
    return Plan(stage, builders, args.run_label, out_dir, float(args.poll_s))


# ---- the stage window ----------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class StageState:
    started_utc: str
    spent_start: Decimal
    runs: tuple


def state_path(profile: pb.Profile, stage: str) -> Path:
    return Path(profile.ledger_dir) / f"stage_{stage}.json"


def read_state(profile: pb.Profile, stage: str) -> StageState | None:
    """The stage's window, or None when no runner of the stage has started. A damaged file is an error, never a guess."""
    path = state_path(profile, stage)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except (OSError, UnicodeDecodeError):
        raise ConfigError(f"the stage state file {path.name} cannot be read") from None
    try:
        raw = json.loads(text)
        started = raw["started_utc"]
        datetime.fromisoformat(started.replace("Z", "+00:00"))
        spent_start = Decimal(str(raw["spent_start"]))
        runs = raw.get("runs", [])
        if not spent_start.is_finite() or spent_start < 0 or not isinstance(runs, list):
            raise ValueError
    except (ValueError, KeyError, TypeError, AttributeError, InvalidOperation):
        raise ConfigError(f"the stage state file {path.name} is damaged (it needs started_utc and spent_start); "
                          "the stage's spend is unknown, so nothing was started") from None
    return StageState(started, spent_start, tuple(runs))


def write_state(profile: pb.Profile, stage: str, state: StageState) -> None:
    write_json_atomic(state_path(profile, stage), {"started_utc": state.started_utc, "spent_start": pb.money_text(state.spent_start),
                                                   "stage": stage, "runs": list(state.runs)})


# ---- the pre-flight ------------------------------------------------------------------------------------------------
def preflight(stage: str, builder: str, profile: pb.Profile, spent_total: Decimal, spent_in_stage: Decimal,
              unreadable: int) -> tuple[bool, str, pf.Result | None]:
    """(ok, reason, result). Refuses when the pre-flight does, when the ledger has a line whose cost cannot be read, and
    when there is no allowance left (a run profile needs a positive one)."""
    try:
        result = pf.check(stage, [builder], spent_total, spent_in_stage, pf.TOTAL_CAP, profile.input_per_mtok, profile.output_per_mtok)
    except ValueError as exc:
        return False, str(exc), None
    reasons = []
    if unreadable:
        reasons.append(f"the ledger has {unreadable} line(s) whose cost cannot be read, so the spend is unknown")
    if not result.ok:
        reasons.append(result.reason)
    elif result.allowance is None or result.allowance <= 0:
        reasons.append("no allowance is left for this run")
    return (not reasons), ("; ".join(reasons) if reasons else result.reason), result


# ---- command lines -------------------------------------------------------------------------------------------------
def runner_command(config: Config, builder: str, stage: str, label_dir: Path) -> list[str]:
    b = config.builders[builder]
    return [b.python, *(["-I"] if b.isolated else []), os.path.join(config.repo_root, "tools", "exp", b.runner),
            "--corpus", config.corpus, "--documents", config.documents, "--repo-root", config.repo_root,
            "--upstream-url", config.local_upstream_url, "--model", config.chat_model, "--embed-model", config.embed_model,
            "--hosted-profile", str(label_dir / "profile.json"), "--workdir", str(label_dir / "work"),
            "--out", str(label_dir / "result.json"), "--checkpoints", STAGE_CHECKPOINTS[stage],
            "--tiktoken-cache", b.tiktoken_cache, *b.extra_args]


def runner_env(config: Config, builder: str) -> dict[str, str]:
    return {"PATH": RUNNER_PATH, **config.builders[builder].env}


def watchdog_command(profile: pb.Profile, stop_at: Decimal, since: str, pgid: int | str, label_dir: Path, poll_s: float,
                     repeat_since: str) -> list[str]:
    return [sys.executable, "-I", str(HERE / "passb_watchdog.py"), "--gateway-dir", profile.ledger_dir,
            "--stop-at-usd", pb.money_text(stop_at), "--since", since, "--repeat-since", repeat_since, "--kill-pgid", str(pgid),
            "--report", str(label_dir / "watchdog.json"), "--poll-s", f"{poll_s:g}"]


def run_profile_text(profile: pb.Profile, allowance: Decimal) -> str:
    """The stage profile with `allowance_usd` replaced; built from the validated Profile, so nothing unchecked is carried over."""
    data: dict[str, Any] = {
        "base_url": profile.base_url, "key_file": profile.key_file, "ledger_dir": profile.ledger_dir,
        "allowance_usd": pb.money_text(allowance), "upstream_timeout_s": profile.upstream_timeout_s,
        "input_per_mtok": pb.money_text(profile.input_per_mtok), "output_per_mtok": pb.money_text(profile.output_per_mtok),
        "source_url": profile.source_url, "read_at": profile.read_at, "output_limit_default": profile.output_limit_default,
        "request_defaults": dict(profile.request_defaults), "translate_max_tokens": profile.translate_max_tokens}
    if profile.cached_input_per_mtok is not None:
        data["cached_input_per_mtok"] = pb.money_text(profile.cached_input_per_mtok)
    if profile.cache_write_per_mtok is not None:
        data["cache_write_per_mtok"] = pb.money_text(profile.cache_write_per_mtok)
    return json.dumps(data, indent=2, sort_keys=True, default=lambda d: float(d) if isinstance(d, Decimal) else str(d)) + "\n"


# ---- the report ----------------------------------------------------------------------------------------------------
class Report:
    """`OUT_DIR/stage_report.json`: {"entries": [...]}, appended to across invocations, rewritten atomically."""

    def __init__(self, path: Path):
        self.path = path
        self.entries: list[dict] = []
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            entries = raw["entries"]
            if not isinstance(entries, list):
                raise TypeError
            self.entries = entries
        except FileNotFoundError:
            pass
        except (OSError, ValueError, KeyError, TypeError):
            raise ConfigError(f"{path.name} exists and is not a stage report; move it away first") from None

    def append(self, entry: dict) -> None:
        self.entries.append(entry)
        write_json_atomic(self.path, {"entries": self.entries})


def _safe_counts(counts: Any) -> dict:
    if not isinstance(counts, dict):
        return {}
    out = {}
    for name, value in counts.items():
        if isinstance(name, str) and COUNT_NAME_RE.match(name):
            if isinstance(value, int) and not isinstance(value, bool):
                out[name] = value
            elif isinstance(value, str) and COUNT_VALUE_RE.match(value):
                out[name] = value
    return out


def read_trips(report_path: Path) -> tuple[list[dict], list[str]]:
    """(tripped rules with their counts, the kill outcomes) from the watchdog's report: names and numbers only."""
    try:
        raw = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return [], []
    if not isinstance(raw, dict):
        return [], []
    trips = [{"rule": t["rule"], "counts": _safe_counts(t.get("counts"))}
             for t in raw.get("trips", []) if isinstance(t, dict) and isinstance(t.get("rule"), str) and t["rule"] in KNOWN_RULES] \
        if isinstance(raw.get("trips"), list) else []
    groups = raw.get("kill_groups")
    kills = sorted({v for v in groups.values() if isinstance(v, str) and v in KILL_WORDS}) if isinstance(groups, dict) else []
    return trips, kills


# ---- processes -----------------------------------------------------------------------------------------------------
def _group_has_members(pgid: int) -> bool:
    """True while a process of the group is alive and not a zombie (the watchdog's own test, which reads `ps`: macOS answers
    EPERM to a signal sent to a group that holds only zombies)."""
    return wd._group_alive(pgid)


def stop_group(pgid: int, grace_s: float = GROUP_GRACE_S) -> None:
    """SIGTERM to a whole process group, then SIGKILL to what is left after the grace period. Never this program's own group
    (a runner that was not given its own session would otherwise take the driver and the shell with it) and never 0 or 1."""
    if pgid > 1 and pgid != os.getpgrp() and _group_has_members(pgid):
        wd.terminate_groups([pgid], grace_s=grace_s)


def stop_runner(runner: subprocess.Popen) -> None:
    """Stop the runner's whole group; if the runner is still there after the grace period (the group kill did not take), the
    runner itself. Returns once the runner is gone."""
    stop_group(runner.pid)
    if _wait(runner, STOP_WAIT_S) is None:
        runner.kill()
    runner.wait()


def stop_process(proc: subprocess.Popen | None, grace_s: float = 5.0) -> None:
    if proc is None or proc.poll() is not None:
        return
    for sig, wait in ((signal.SIGTERM, grace_s), (signal.SIGKILL, 5.0)):
        try:
            proc.send_signal(sig)
        except ProcessLookupError:
            break
        try:
            proc.wait(timeout=wait)
            break
        except subprocess.TimeoutExpired:
            continue


def _wait(proc: subprocess.Popen, seconds: float) -> int | None:
    try:
        return proc.wait(timeout=seconds)
    except subprocess.TimeoutExpired:
        return None


def last_read(profile: pb.Profile, stop_at: Decimal, since: str, label_dir: Path, repeat_since: str) -> int:
    """The whole stage's log read once with the watchdog's rules (the same report file); its exit status."""
    command = [sys.executable, "-I", str(HERE / "passb_watchdog.py"), "--gateway-dir", profile.ledger_dir,
               "--stop-at-usd", pb.money_text(stop_at), "--since", since, "--repeat-since", repeat_since,
               "--report", str(label_dir / "watchdog.json"), "--max-seconds", "0"]
    with _private_file(label_dir / "watchdog.stdout.log", append=True) as out, \
            _private_file(label_dir / "watchdog.stderr.log", append=True) as err:
        try:
            return subprocess.run(command, cwd=label_dir, env=dict(HELPER_ENV), stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                  timeout=120).returncode
        except (OSError, subprocess.SubprocessError):
            return 2


# ---- one builder ---------------------------------------------------------------------------------------------------
@dataclass
class Context:
    plan: Plan
    config: Config
    profile: pb.Profile
    report: Report


def _entry(ctx: Context, builder: str, outcome: str, **fields: Any) -> dict:
    return {"stage": ctx.plan.stage, "run_label": ctx.plan.run_label, "label": ctx.plan.label(builder), "builder": builder,
            "outcome": outcome, **fields}


def run_builder(ctx: Context, builder: str, result: pf.Result, state: StageState, spent_before: Decimal) -> tuple[dict, bool]:
    """Run one builder under the watchdog. Returns (the report entry, halt): halt is True when the next builder must not start."""
    plan, profile = ctx.plan, ctx.profile
    ldir = plan.label_dir(builder)
    ldir.mkdir(mode=0o700)                                           # fails if the label already exists
    allowance, stop_at = result.allowance, result.stop_at
    started_utc = utc_stamp()
    base = {"allowance_usd": pb.money_text(allowance), "stop_at_usd": pb.money_text(stop_at), "started_utc": started_utc}
    profile_path = ldir / "profile.json"
    with _private_file(profile_path) as handle:
        handle.write(run_profile_text(profile, allowance).encode("utf-8"))
    pb.load_profile(profile_path)                                    # the file the runner will read must itself be valid
    runner = watch = None
    files = []
    try:
        try:
            out, err = (_private_file(ldir / "runner.stdout.log"), _private_file(ldir / "runner.stderr.log"))
            files += [out, err]
            runner = subprocess.Popen(runner_command(ctx.config, builder, plan.stage, ldir), cwd=ldir,
                                      env=runner_env(ctx.config, builder), stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                      start_new_session=True)
        except OSError as exc:
            return _entry(ctx, builder, "start_failed", exit_status=None, error=type(exc).__name__, finished_utc=utc_stamp(),
                          **base), True
        pgid = runner.pid
        print(f"passb_stage: {plan.label(builder)} started (runner process group {pgid})", flush=True)
        try:
            wout, werr = (_private_file(ldir / "watchdog.stdout.log"), _private_file(ldir / "watchdog.stderr.log"))
            files += [wout, werr]
            watch = subprocess.Popen(watchdog_command(profile, stop_at, state.started_utc, pgid, ldir, plan.poll_s, started_utc), cwd=ldir,
                                     env=dict(HELPER_ENV), stdin=subprocess.DEVNULL, stdout=wout, stderr=werr,
                                     start_new_session=True)
        except OSError:
            stop_runner(runner)
            return _entry(ctx, builder, "guard_failed", exit_status=runner.returncode, finished_utc=utc_stamp(), **base), True

        guard_rc = None
        while True:                                                  # wait for the runner, and for the guard to stay up
            try:
                runner.wait(timeout=0.2)
                break
            except subprocess.TimeoutExpired:
                pass
            guard_rc = watch.poll()
            if guard_rc is not None:
                break
        report_path = ldir / "watchdog.json"
        if guard_rc is not None and runner.poll() is None:           # the watchdog ended while the runner lives
            if guard_rc == EXIT_TRIPPED:                             # it is stopping the group; give it time
                if _wait(runner, TRIP_WAIT_S) is None:
                    stop_runner(runner)
            else:                                                    # anything else: the run is unguarded, stop it
                stop_runner(runner)
            runner.wait()
        elif guard_rc is None:                                       # the runner ended first: the live watchdog's turn
            guard_rc = watch.poll()
            if guard_rc is None and report_path.exists():            # a trip is being carried out: let it finish
                guard_rc = _wait(watch, TRIP_WAIT_S)
        stop_process(watch)
        left_processes = _group_has_members(pgid)                    # what the runner left behind in its group
        if left_processes:
            stop_group(pgid)
        tripped = guard_rc == EXIT_TRIPPED or bool(read_trips(report_path)[0])
        guard_died = guard_rc is not None and guard_rc != EXIT_TRIPPED   # it ended by itself and did not trip: no guard
        if not tripped:                                              # the last read: every call up to the runner's exit
            final = last_read(profile, stop_at, state.started_utc, ldir, started_utc)
            tripped = final == EXIT_TRIPPED
            guard_died = guard_died or final not in (0, EXIT_TRIPPED)
        trips, kills = read_trips(report_path) if tripped else ([], [])
        if tripped and not trips:
            trips = [{"rule": "unreadable_report", "counts": {}}]
        spent_after, unreadable = pf.ledger_spent(profile.ledger_dir)
        outcome = "tripped" if tripped else "guard_failed" if guard_died else "completed" if runner.returncode == 0 else "builder_failed"
        extra: dict[str, Any] = {"tripped_rules": trips, "watchdog_kill": kills, "left_processes": left_processes}
        if unreadable:
            extra["ledger_unreadable_lines"] = unreadable
        entry = _entry(ctx, builder, outcome, exit_status=runner.returncode, spent_usd=pb.money_text(spent_after - spent_before),
                       spent_in_stage_usd=pb.money_text(spent_after - state.spent_start),
                       result_file=f"{plan.label(builder)}/result.json" if (ldir / "result.json").exists() else None,
                       finished_utc=utc_stamp(), **extra, **base)
        return entry, outcome in ("tripped", "guard_failed")
    except BaseException as exc:
        stop_process(watch)
        if runner is not None:
            stop_runner(runner)
        if isinstance(exc, Interrupted):
            spent_after, _ = pf.ledger_spent(profile.ledger_dir)
            ctx.report.append(_entry(ctx, builder, "interrupted", exit_status=runner.returncode if runner else None,
                                     signal=exc.signum, spent_usd=pb.money_text(spent_after - spent_before),
                                     finished_utc=utc_stamp(), **base))
        raise
    finally:
        for handle in files:
            handle.close()


# ---- the commands --------------------------------------------------------------------------------------------------
def _rows(rows: Sequence[tuple[str, str]], indent: str = "  ") -> str:
    width = max(len(k) for k, _ in rows)
    return "\n".join(f"{indent}{k.ljust(width)}  {v}" for k, v in rows)


def dry_run(plan: Plan, config: Config, profile: pb.Profile) -> int:
    """Print what --send would do. Reads the ledger and the stage's state file; starts nothing and writes nothing."""
    total, unreadable = pf.ledger_spent(profile.ledger_dir)
    state = read_state(profile, plan.stage)
    in_stage = total - (state.spent_start if state else total)
    since = state.started_utc if state else "<STAGE_START_UTC>"
    refused = bool(unreadable)
    print(f"pass-B stage driver: DRY RUN (nothing is started and nothing is written; add --send to run)\n"
          f"  stage {plan.stage}, checkpoints {STAGE_CHECKPOINTS[plan.stage]}, run label {plan.run_label}, "
          f"builders {', '.join(plan.builders)}")
    print(_rows([("out dir", str(plan.out_dir)), ("ledger", profile.ledger_dir),
                 ("key file", f"{profile.key_file}  (given as is; this program never opens it)"),
                 ("stage window", f"opened {state.started_utc}, ledger spend when it opened USD {pf.money(state.spent_start)}" if state
                  else "not open yet: it opens when the first runner of the stage starts"),
                 ("spent in the ledger", f"USD {pf.money(total)} of a total cap of USD {pf.money(pf.TOTAL_CAP)}"
                                         + (f"; {unreadable} line(s) with an unreadable cost" if unreadable else "")),
                 ("spent in this stage", f"USD {pf.money(in_stage)}")]))
    for index, builder in enumerate(plan.builders, 1):
        label_dir = plan.label_dir(builder)
        ok, reason, result = preflight(plan.stage, builder, profile, total, in_stage, unreadable)
        taken = label_dir.exists()
        refused = refused or not ok or taken
        rows = [("expected tokens", "unknown" if result is None or result.estimate is None else
                 "input %s  output %s" % tuple(f"{v:,.0f}" for v in pf.run_tokens(plan.stage, [builder])))]
        rows += [("estimate for this run", "unknown" if result is None or result.estimate is None else f"USD {pf.money(result.estimate)}"),
                 ("stop at", "unknown" if result is None or result.stop_at is None else f"USD {pf.money(result.stop_at)}"),
                 ("allowance", "unknown" if result is None or result.allowance is None else f"USD {pf.money(result.allowance)}"
                  "  (written to the run profile in place of the stage profile's)"),
                 ("cap for the gateway", "unknown" if result is None or result.cap_for_gateway is None
                  else f"USD {pf.money(result.cap_for_gateway)}  (the ledger's spend + the allowance)"),
                 ("verdict", ("OK, " if ok else "REFUSED: ") + reason)]
        if taken:
            rows.append(("label", f"REFUSED: {label_dir.name} already exists in the out dir"))
        print(f"\nbuilder {index}: {builder}   label {plan.label(builder)}"
              + ("" if index == 1 else "   (projected: each earlier builder spends its central estimate)"))
        print(_rows(rows))
        print(_rows([("runner", shlex.join(runner_command(config, builder, plan.stage, label_dir))),
                     ("environment", " ".join(f"{k}={shlex.quote(v)}" for k, v in runner_env(config, builder).items())),
                     ("watchdog", shlex.join(watchdog_command(profile, result.stop_at if result and result.stop_at is not None
                                                              else Decimal(0), since, "<RUNNER_PID>", label_dir, plan.poll_s,
                                                              "<RUN_START_UTC>"))),
                     ("files", "profile.json (600), work/, result.json, runner.stdout.log, runner.stderr.log, "
                               "watchdog.json, watchdog.stdout.log, watchdog.stderr.log")]))
        if result is not None and result.estimate is not None:
            total += result.estimate
            in_stage += result.estimate
    print("\n" + ("REFUSED: at least one builder would be refused; nothing was started." if refused
                  else "OK: nothing was started; add --send to run."))
    return EXIT_REFUSED if refused else EXIT_OK


def acquire_lock(ledger_dir: Path) -> int:
    fd = os.open(ledger_dir / LOCK_NAME, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        os.close(fd)
        raise ConfigError("another stage run holds this ledger (two runs on one ledger would make the gateway's cap stale)") from None
    return fd


def send(plan: Plan, config: Config, profile: pb.Profile) -> int:
    ledger_dir = Path(profile.ledger_dir)
    try:
        ledger_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    except OSError as exc:
        raise ConfigError(f"the ledger directory cannot be created ({type(exc).__name__})") from None
    lock = acquire_lock(ledger_dir)
    try:
        taken = [plan.label(b) for b in plan.builders if plan.label_dir(b).exists()]
        if taken:
            raise ConfigError(f"already in the out dir: {', '.join(taken)}; a run label is used once (use another --run-label)")
        plan.out_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        ctx = Context(plan, config, profile, Report(plan.out_dir / REPORT_NAME))
        for index, builder in enumerate(plan.builders):
            spent_total, unreadable = pf.ledger_spent(profile.ledger_dir)
            state = read_state(profile, plan.stage)
            spent_in_stage = spent_total - (state.spent_start if state else spent_total)
            ok, reason, result = preflight(plan.stage, builder, profile, spent_total, spent_in_stage, unreadable)
            if not ok:
                ctx.report.append(_entry(ctx, builder, "refused", exit_status=None, reason=reason,
                                         not_started=list(plan.builders[index:]), finished_utc=utc_stamp()))
                print(f"passb_stage: REFUSED before starting {plan.label(builder)}: {reason}", file=sys.stderr)
                return EXIT_REFUSED
            if state is None:                                        # the stage's window opens now, with the first runner
                state = StageState(utc_stamp(), spent_total, ())
                write_state(profile, plan.stage, state)
            entry, halt = run_builder(ctx, builder, result, state, spent_total)
            ctx.report.append(entry)
            write_state(profile, plan.stage, StageState(state.started_utc, state.spent_start, state.runs + (
                {"label": entry["label"], "outcome": entry["outcome"], "finished_utc": entry["finished_utc"],
                 "spent_usd": entry.get("spent_usd")},)))
            tripped = ", ".join(t["rule"] for t in entry.get("tripped_rules", []))
            print(f"passb_stage: {entry['label']}: {entry['outcome']}, runner exit {entry['exit_status']}, spent USD "
                  f"{entry.get('spent_usd', '?')}" + (f", tripped {tripped}" if tripped else ""), flush=True)
            if entry["outcome"] == "start_failed":
                return EXIT_REFUSED
            if halt:
                print("passb_stage: STOPPED, the remaining builders were not started: "
                      f"{', '.join(plan.builders[index + 1:]) or 'none'}", file=sys.stderr)
                return EXIT_TRIPPED
        return EXIT_OK
    finally:
        os.close(lock)


def _install_handlers() -> dict:
    fired = []

    def handler(signum: int, frame: Any) -> None:
        if fired:                       # a second signal must not cut the clean-up short
            return
        fired.append(signum)
        raise Interrupted(signum)

    previous = {}
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            previous[sig] = signal.signal(sig, handler)
        except ValueError:              # not the main thread
            pass
    return previous


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="passb_stage.py",
        description="Run ONE stage (B, C or D) of the paid pilot for the named builders, one after another, with the free "
                    "pre-flight before and the watchdog beside each. Without --send it only prints what it would do. Exit "
                    "status: 0 every builder ran; 1 refused or a usage/config error; 3 a watchdog trip.")
    p.add_argument("--stage", required=True, choices=sorted(STAGE_CHECKPOINTS), help="B (1 document), C (5), D (20)")
    p.add_argument("--builder", action="append", required=True, choices=BUILDERS, metavar="NAME",
                   help=f"a builder ({', '.join(BUILDERS)}); repeat for several, run in the order given")
    p.add_argument("--profile", required=True, help="the stage's hosted profile (JSON); its allowance_usd is replaced")
    p.add_argument("--builders-config", required=True, help="the builders config (JSON), outside the repository")
    p.add_argument("--out-dir", required=True, help="where the run directories and stage_report.json go, outside the repository")
    p.add_argument("--run-label", default="r1", help="stage C is run twice: r1, then r2 (default r1); used once per stage")
    p.add_argument("--send", action="store_true", help="really start the runners (without it: a dry run that starts nothing)")
    p.add_argument("--poll-s", type=float, default=DEFAULT_POLL_S, help=argparse.SUPPRESS)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config = load_config(args.builders_config)
        profile = pb.load_profile(args.profile)
        plan = make_plan(args, config, profile)
        if not args.send:
            return dry_run(plan, config, profile)
    except pc.PassAError as exc:
        print(f"passb_stage: {exc}", file=sys.stderr)
        return EXIT_REFUSED
    previous = _install_handlers()
    try:
        return send(plan, config, profile)
    except pc.PassAError as exc:
        print(f"passb_stage: {exc}", file=sys.stderr)
        return EXIT_REFUSED
    except Interrupted as exc:
        print(f"passb_stage: stopped by signal {exc.signum}; the runner's process group and the watchdog were stopped",
              file=sys.stderr)
        return 128 + exc.signum
    finally:
        for sig, old in previous.items():
            signal.signal(sig, old)


if __name__ == "__main__":
    sys.exit(main())
