"""Shared pieces for the local rehearsal ("pass A"): a builder is pointed at the metering gateway, the gateway at a local Ollama.

The stub rehearsals counted what a builder sends. Pass A lets a real local model answer, so output tokens, retries and
the calls that depend on the model's text become measurable. Tokens are then the provider's own (Ollama reports them in
the usage field of each response); the gateway writes them to one log whatever the builder.

    from passa_common import LocalGateway, preflight, probe_speed
    facts = preflight("http://127.0.0.1:11434", "my-model-16k", min_ctx=16384)
    with LocalGateway(workdir, "http://127.0.0.1:11434/v1", ["my-model-16k", "my-embedding"], repo_root) as gw:
        ...                       # point the builder at gw.base_url (http://127.0.0.1:PORT/v1) with a dummy key
        calls = gw.calls()        # one dict per call: usage from the log, request and response from the body log

Prices are zero (a local model costs nothing), so the cap can never refuse. The gateway's job here is the uniform record.
The body log holds third-party article text: keep the working directory outside the repository and never commit it.

A finished run can be read back with `python passa_common.py facts WORKDIR/gateway`.

Standard library only.
"""

from __future__ import annotations

import json
import math
import re
import subprocess
import sys
import time
from collections import Counter
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

CONFIG_TEMPLATE = """[gateway]
currency = "LOCAL-ZERO"
cap = 1
default_max_output_tokens = 4096
input_bytes_per_token = 2
upstream_timeout_s = {timeout}
port = 8089
log_file = "{log}"
log_bodies = true

[upstreams.local]
protocol = "openai"
base_url = "{upstream}"
key_env = "PASSA_UNUSED_KEY"
dry_run = true
"""

MODEL_TEMPLATE = """
[models."{name}"]
upstream = "local"
input_per_mtok = 0
output_per_mtok = 0
source_url = "{source}"
read_at = "{read_at}"
"""


class PassAError(RuntimeError):
    pass


KEY_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def toml_value(value: Any) -> str:
    """A JSON-style value (bool, number, string, nested dict of those) as a TOML value for the gateway config."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float) and math.isfinite(value):
        return repr(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, dict) and all(isinstance(k, str) and KEY_RE.match(k) for k in value):
        return "{ " + ", ".join(f"{k} = {toml_value(v)}" for k, v in value.items()) + " }" if value else "{}"
    raise PassAError(f"cannot write {value!r} as a request default (use booleans, numbers, strings and tables of them)")


def add_chat_default_argument(parser: Any) -> None:
    """The `--chat-default NAME=VALUE` option the four pass-A runners share (repeatable)."""
    parser.add_argument("--chat-default", action="append", default=[], metavar="NAME=VALUE",
                        help="a field the gateway adds to every chat request that lacks it, for example reasoning_effort=none; "
                             "VALUE is read as JSON when it parses (7, true, {\"a\": 1}) and as a plain string otherwise")


def chat_defaults(args: Any) -> dict[str, Any]:
    """The `--chat-default` options as {name: value}. A name given twice keeps the last."""
    out: dict[str, Any] = {}
    for item in args.chat_default:
        name, sep, raw = item.partition("=")
        if not sep or not KEY_RE.match(name):
            raise PassAError(f"--chat-default {item!r}: write NAME=VALUE, the name made of letters, digits, _ and -")
        try:
            out[name] = json.loads(raw)
        except json.JSONDecodeError:
            out[name] = raw
    return out


def _http_json(url: str, payload: dict | None = None, timeout: float = 60.0) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"} if data else {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise PassAError(f"{url}: {type(exc).__name__}: {exc}") from None


def parameters_of(show: dict) -> dict[str, str]:
    """The Modelfile PARAMETER lines in an /api/show answer, as {name: value}. A name given twice keeps the last."""
    out: dict[str, str] = {}
    for line in str(show.get("parameters") or "").splitlines():
        parts = line.split(None, 1)
        if len(parts) == 2:
            out[parts[0]] = parts[1].strip()
    return out


def preflight(ollama_url: str, model: str, *, min_ctx: int, embed_model: str | None = None) -> dict:
    """Refuse to start unless the model exists and its context length is explicitly at least min_ctx.

    Ollama's default context depends on memory (4k under 24 GiB of video memory, 32k from 24 to 48 GiB, per its docs read
    20261102 14:01 UTC) and the OpenAI-compatible endpoint cannot set it per request, so a model without an explicit
    `PARAMETER num_ctx` could silently truncate a long prompt. Returns the facts to record.
    """
    base = ollama_url.rstrip("/")
    names = {m.get("name") or m.get("model") for m in _http_json(f"{base}/api/tags").get("models", [])}
    facts: dict[str, Any] = {"ollama_version": _http_json(f"{base}/api/version").get("version")}
    wanted = [model] + ([embed_model] if embed_model else [])
    missing = [m for m in wanted if m not in names and f"{m}:latest" not in names]
    if missing:
        raise PassAError(f"not installed in Ollama: {missing}; installed: {sorted(n for n in names if n)}")
    show = _http_json(f"{base}/api/show", {"model": model})
    params = parameters_of(show)
    if "num_ctx" not in params:
        raise PassAError(f"{model}: no explicit num_ctx in its Modelfile; create a derived model with PARAMETER num_ctx {min_ctx}")
    if int(params["num_ctx"]) < min_ctx:
        raise PassAError(f"{model}: num_ctx {params['num_ctx']} is below the {min_ctx} the builders' prompts need")
    facts.update({
        "model": model,
        "num_ctx": int(params["num_ctx"]),
        "parameters": params,
        "details": show.get("details"),
        "capabilities": show.get("capabilities"),
    })
    return facts


def probe_speed(ollama_url: str, model: str, *, long_words: int = 1500, gen_tokens: int = 120) -> dict:
    """Prompt-processing and generation speed from Ollama's own timing fields (nanoseconds), two small calls.

    The prompt is synthetic filler, not article text. Rates are tokens per second as Ollama reports them for this
    machine and this model at this moment; they say nothing about another model or about contention with other work.
    """
    base = ollama_url.rstrip("/")
    filler = " ".join(f"word{i % 97}" for i in range(long_words))
    prompt = _http_json(f"{base}/api/chat", {"model": model, "stream": False, "options": {"num_predict": 1, "temperature": 0},
                                              "messages": [{"role": "user", "content": filler}]}, timeout=900)
    gen = _http_json(f"{base}/api/chat", {"model": model, "stream": False, "options": {"num_predict": gen_tokens, "temperature": 0},
                                           "messages": [{"role": "user", "content": "Count from one upward in words, one per line."}]}, timeout=900)

    def rate(count: Any, ns: Any) -> float | None:
        return round(count / (ns / 1e9), 2) if count and ns else None

    return {
        "prompt_tokens": prompt.get("prompt_eval_count"),
        "prompt_tokens_per_second": rate(prompt.get("prompt_eval_count"), prompt.get("prompt_eval_duration")),
        "generated_tokens": gen.get("eval_count"),
        "generation_tokens_per_second": rate(gen.get("eval_count"), gen.get("eval_duration")),
        "load_seconds_first_call": round((prompt.get("load_duration") or 0) / 1e9, 2),
    }


class LocalGateway:
    """The metering gateway as a subprocess, pointed at a local OpenAI-compatible server."""

    def __init__(self, workdir: str | Path, upstream_base_url: str, models: Iterable[str], repo_root: str | Path,
                 *, timeout_s: int = 1800, source_url: str = "https://ollama.com/library",
                 request_defaults: Mapping[str, Mapping[str, Any]] | None = None):
        self.workdir = Path(workdir)
        self.request_defaults = {m: dict(d) for m, d in (request_defaults or {}).items() if d}
        self.repo_root = Path(repo_root)
        self.upstream = upstream_base_url
        self.models = list(models)
        self.timeout_s = timeout_s
        self.source_url = source_url
        self.proc: subprocess.Popen | None = None
        self.port: int | None = None
        self.log_path = self.workdir / "meter.jsonl"
        self.body_path = self.workdir / "meter.jsonl.bodies.jsonl"
        self.output = ""

    @property
    def base_url(self) -> str:
        if self.port is None:
            raise PassAError("the gateway is not running")
        return f"http://127.0.0.1:{self.port}/v1"

    def write_config(self) -> Path:
        self.workdir.mkdir(parents=True, exist_ok=True)
        read_at = datetime.now(timezone.utc).strftime("%Y%m%d %H:%M")
        text = CONFIG_TEMPLATE.format(timeout=self.timeout_s, log=self.log_path.as_posix(), upstream=self.upstream)
        for m in self.models:
            text += MODEL_TEMPLATE.format(name=m, source=self.source_url, read_at=read_at)
            if self.request_defaults.get(m):
                text += f'\n[models."{m}".request_defaults]\n'
                text += "".join(f"{k} = {toml_value(v)}\n" for k, v in self.request_defaults[m].items())
        unknown = sorted(set(self.request_defaults) - set(self.models))
        if unknown:
            raise PassAError(f"request defaults given for models the gateway does not serve: {unknown}")
        cfg = self.workdir / "gateway.toml"
        cfg.write_text(text)
        return cfg

    def start(self) -> "LocalGateway":
        cfg = self.write_config()
        self.proc = subprocess.Popen(
            [sys.executable, str(self.repo_root / "tools" / "metering_gateway.py"), "--config", str(cfg), "--port", "0"],
            cwd=self.workdir, env={"PATH": "/usr/bin:/bin"}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        deadline = time.time() + 60
        while time.time() < deadline:
            line = self.proc.stdout.readline()
            self.output += line
            m = re.search(r"listening on http://127\.0\.0\.1:(\d+)", line)
            if m:
                self.port = int(m.group(1))
                return self
            if not line and self.proc.poll() is not None:
                break
        self.stop()
        raise PassAError(f"the gateway did not start: {self.output.strip()[-300:]}")

    def stop(self) -> None:
        if self.proc is None:
            return
        self.proc.terminate()
        try:
            self.output += self.proc.communicate(timeout=30)[0] or ""
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.output += self.proc.communicate()[0] or ""
        self.proc = None

    def __enter__(self) -> "LocalGateway":
        return self.start()

    def __exit__(self, *exc: object) -> None:
        self.stop()

    def calls(self) -> list[dict]:
        """One dict per call, in arrival order: the log record, plus the request and response from the body log."""
        return calls_in(self.workdir)


def calls_in(gateway_dir: str | Path) -> list[dict]:
    """The same list from a finished run's gateway directory (`meter.jsonl` and its body log)."""
    gateway_dir = Path(gateway_dir)
    records = _read_jsonl(gateway_dir / "meter.jsonl")
    bodies = {b["call_id"]: b for b in _read_jsonl(gateway_dir / "meter.jsonl.bodies.jsonl")}
    out = []
    for r in records:
        b = bodies.get(r["call_id"], {})
        out.append({**r, "request": _maybe_json(b.get("request")), "response": _maybe_json(b.get("response"))})
    return out


def reasoning_tokens_of(resp: Any) -> int:
    """`usage.completion_tokens_details.reasoning_tokens` of one parsed chat answer; 0 when any link of the chain is absent
    or is not a whole number (a provider that does not report it, or an error body)."""
    usage = resp.get("usage") if isinstance(resp, dict) else None
    details = usage.get("completion_tokens_details") if isinstance(usage, dict) else None
    value = details.get("reasoning_tokens") if isinstance(details, dict) else None
    return value if isinstance(value, int) and not isinstance(value, bool) and value > 0 else 0


def response_facts(calls: Iterable[dict]) -> dict:
    """What the chat answers looked like, from the body log: why each stopped, whether any carried reasoning text, the
    longest, and how many reasoning tokens the provider says it generated. A `length` stop means the model hit the output
    cap (its answer is cut off); reasoning text means the model thought before answering; `reasoning_tokens_total` is
    the sum of `usage.completion_tokens_details.reasoning_tokens` over the parsed chat answers (an absent field counts 0,
    and a streamed body is not parsed, so it adds nothing). Streamed or unparsable bodies are counted apart, not guessed at."""
    finish: Counter = Counter()
    reasoning = unparsed = chat = longest = reasoning_tokens = 0
    for c in calls:
        if not str(c.get("route", "")).endswith("chat/completions"):
            continue
        chat += 1
        resp = c.get("response")
        reasoning_tokens += reasoning_tokens_of(resp)
        choices = resp.get("choices") if isinstance(resp, dict) else None
        if not choices:
            unparsed += 1
            continue
        finish[str(choices[0].get("finish_reason"))] += 1
        message = choices[0].get("message") or {}
        reasoning += 1 if (message.get("reasoning") or message.get("reasoning_content")) else 0
        longest = max(longest, c.get("output_tokens") or 0)
    return {"chat_calls": chat, "finish_reasons": dict(finish), "answers_with_reasoning_text": reasoning,
            "reasoning_tokens_total": reasoning_tokens, "unparsed_or_streamed": unparsed,
            "longest_answer_output_tokens": longest}


def _maybe_json(text: Any) -> Any:
    """The body log keeps raw HTTP bodies as text: a parsed object when it is JSON, the text itself when it is not
    (a streamed response is event-stream text), None when there is no body."""
    if not isinstance(text, str):
        return text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def summarize(calls: Iterable[dict], classify) -> dict:
    """Totals by kind. classify(call) -> a short label (it reads the request body); unclassified calls say so."""
    kinds: dict[str, dict[str, int]] = {}
    for c in calls:
        kind = classify(c) if c.get("request") is not None else "no_body"
        k = kinds.setdefault(kind, {"calls": 0, "ok": 0, "input_tokens": 0, "output_tokens": 0, "latency_ms": 0})
        k["calls"] += 1
        k["ok"] += 1 if c.get("http_status") == 200 and not c.get("voided") else 0
        k["input_tokens"] += c.get("input_tokens") or 0
        k["output_tokens"] += c.get("output_tokens") or 0
        k["latency_ms"] += c.get("latency_ms") or 0
    total = {key: sum(v[key] for v in kinds.values()) for key in ("calls", "ok", "input_tokens", "output_tokens", "latency_ms")}
    return {"by_kind": kinds, "total": total}


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "facts":
        print(json.dumps(response_facts(calls_in(sys.argv[2])), indent=1))
    else:
        sys.exit("usage: python passa_common.py facts WORKDIR/gateway   (why each chat answer stopped, reasoning text, longest answer)")
