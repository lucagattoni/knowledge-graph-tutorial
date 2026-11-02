"""Pass B, stage A: the first time the metering gateway meets a real provider. Plan item F3.

Stage A is at most 12 calls and USD 0.10 (kb-kg/experiments/x2-index-cost/pass-b-plan.md, "The ladder"). Two subcommands,
standard library only:

    python tools/exp/passb_stage_a.py extract --pass-a-dirs lightrag=DIR fast=DIR ms=DIR [nano=DIR] --out FILE
    python tools/exp/passb_stage_a.py run --profile PROFILE.json --requests FILE --out-dir DIR [--send]

`extract` (free, local, no network) picks one recorded request of each kind from pass A's gateway directories and adds the
shapes pass A never logged, written from the builders' own source with innocuous dummy data and no article text. The result
is a mode-600 JSON list of `{name, route, body}`, at most 10 entries. It holds article text: keep it OUTSIDE the repository
and NOT in a scratch directory (a session's scratch area does not outlive the session). Writing it inside the repository, or
over a file that exists, is refused.

`run` sends those requests through a real `HostedGateway` (passb_common.py) at the provider the profile names. WITHOUT
`--send` it prints the plan (names, byte sizes, the worst-case cost by the gateway's own reservation formula, the caps) and
exits 0, having started nothing and written nothing. WITH `--send`, in this order:

  1. Refuse to start unless the profile's allowance is within the stage cap (USD 0.10) and the pilot cap (USD 3 less what the
     ledger already holds), the worst-case cost fits the allowance, and the requests file is private and outside the
     repository. Start the gateway and read its `/_meter/summary` back: the cap it loaded must be the one computed here.
  2. Send each request once as a plain HTTP POST to the gateway (dummy Authorization header; the key is read by the gateway
     alone, and this program never opens the key file). Stop sending at once on a 401 or 403 (key or account), on a 429 or
     5xx that is still there after one retry, on any gateway refusal, on a missing usage object, on any other unexpected
     status, on a rejected ping, or when the gateway's spend passes USD 0.10. A 400 or 422 on any request after the ping is a
     RESULT, not a fault: it is recorded as "rejected_incompatible" and the run goes on. Nothing is retried or altered.
  3. The refusal test: stop that gateway; start a second one on a throwaway ledger under `--out-dir` with an allowance of
     USD 0.0001 and send the LARGEST request. It must be answered 429 `gateway_budget_exceeded`, and the throwaway ledger
     must hold one record, a refusal with no tokens, zero cost and not voided (a call that had been forwarded would show
     tokens, a cost or a voided flag). That gateway's upstream is a loopback port nothing listens on, so even a broken
     refusal could not reach the provider: it would show as a 502, not as a refusal. The throwaway body log, which holds
     that request's text, is deleted after the check.
  4. Write `stage-a-result.json` (mode 600) in `--out-dir`: per call, the status, the model the provider reports, the finish
     reason, the token counts (reasoning tokens included), the NAMES of the usage fields, the gateway's cost and the fields it
     added, and for a rejection the error type, code and parameter name and the message LENGTH; then the stage's gates as
     booleans. No request or response text, no key, and no path is in it.

What the program cannot do: read the provider's console. Its usage page is the only check that is independent of the
gateway (the gateway's tokens are the provider's own `usage`), so the result tells the coordinator to compare the two by hand.

Exit status of `run`: 0 when every request was sent, the refusal test passed and no stop rule fired; 3 when a stop rule
fired or the refusal test did not pass (the result file says which); 2 when it refused to start or on a usage error.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import socket
import stat
import sys
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import replace
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

sys.dont_write_bytecode = True  # importing must not leave .pyc files in the repository
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import passa_common as pc  # noqa: E402
import passb_common as pb  # noqa: E402

STAGE_CAP = Decimal("0.10")             # the plan's stage-A limit and "stop at"
PILOT_CAP = Decimal("3")                # the whole pilot (decision 2)
REFUSAL_ALLOWANCE = Decimal("0.0001")   # the throwaway gateway's allowance in the refusal test
MAX_REQUESTS = 10                       # the requests file; with the refused call and one retry the stage stays within 12
MAX_CALLS = 12                          # the plan's limit on calls in the stage, the refused one included
MAX_ATTEMPTS = MAX_CALLS - 1            # forwarded attempts, retries included; the refusal test is the twelfth call
ROUTE = "/chat/completions"             # relative to the gateway's base URL, which ends in /v1
MODEL_PLACEHOLDER = "MODEL-IS-SET-AT-RUN-TIME"
DEFAULT_MODEL = "gpt-6-luna"            # the owner's choice (plan, "Decided so far"); --model overrides
DEFAULT_EMBED_MODEL = "stage-a-unused-embedding"      # served by the local upstream, which this stage never calls
DEFAULT_LOCAL_URL = "http://127.0.0.1:11434/v1"
RESULT_NAME = "stage-a-result.json"
RETRY_WAIT_S = 5.0
DUMMY_AUTHORIZATION = "Bearer dummy-not-a-key"
PING_NAME = "ping"
REQUIRED_DIRS = ("lightrag", "fast", "ms")
OPTIONAL_DIRS = ("nano",)
NAME_RE = re.compile(r"^[a-z][a-z0-9_]{0,39}$")
TOKEN_RE = re.compile(r"^[A-Za-z0-9_.\[\]-]{1,64}$")     # a field name or a code, never prose
CONSOLE_NOTE = ("Compare by hand: the provider console's usage page for this key's project must show {n} requests and a "
                "total equal to USD {total} to rounding. The refused call must not appear in it. This program cannot read "
                "the console, and it is the only check not made of the gateway's own numbers.")


class StageAError(pc.PassAError):
    """Refusal to start or a defect in an input. A message never holds request text, a key or a path."""


# ---- where files may live -------------------------------------------------------------------------------------------
def repository_roots(root: Path = REPO_ROOT) -> list[Path]:
    """The repository this script is in and, when it is a git worktree, the primary checkout that holds the worktree's
    git directory. Article text must not be written under either."""
    roots = [Path(root).resolve()]
    git = Path(root) / ".git"
    try:
        if git.is_file():
            match = re.match(r"gitdir:\s*(.+)", git.read_text(encoding="utf-8", errors="replace").strip())
            if match:
                gitdir = Path(match.group(1).strip())
                gitdir = (gitdir if gitdir.is_absolute() else Path(root) / gitdir).resolve()
                if gitdir.parent.name == "worktrees":              # <primary>/.git/worktrees/<name>
                    roots.append(gitdir.parent.parent.parent.resolve())
    except OSError:
        pass
    return roots


def inside_repository(path: str | Path, roots: Iterable[Path] | None = None) -> bool:
    target = Path(path).resolve()
    return any(target.is_relative_to(r) for r in (repository_roots() if roots is None else roots))


def looks_like_scratch(path: str | Path) -> bool:
    """True for a path under a system temp directory or a directory called scratchpad (which does not outlive a session)."""
    text = str(Path(path).resolve())
    markers = {tempfile.gettempdir(), str(Path(tempfile.gettempdir()).resolve()), "/tmp", "/private/" + "tmp", "/var/folders"}
    return any(text == m or text.startswith(m.rstrip("/") + "/") for m in markers) or "scratchpad" in text.split("/")


def write_private(path: Path, text: str) -> None:
    """A new file, mode 600, never over an existing one."""
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise StageAError(f"{path.name} already exists; this program does not overwrite a file") from None
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)


# ---- the shapes pass A never logged: synthesised from the builders' source, with dummy data -------------------------
# Wording is compressed, not copied; the fields and the layout follow the builders (both MIT, per their LICENSE files).
# Sources, read 20261102 22:15 UTC from the installed packages:
#   nano-graphrag 0.0.8.2: `_op.py` line 145 `use_llm_func(use_prompt, max_tokens=summary_max_tokens)` with
#     `graphrag.py` line 76 `entity_summary_to_max_tokens = 500`; `base.py` line 28 / `graphrag.py` lines 98-99
#     `special_community_report_llm_kwargs = {"response_format": {"type": "json_object"}}`; one user message in both
#     (`_llm.py`: a system message only when a system prompt is given); `prompt.py` lines 63 and 297 for the two prompts.
#   fast-graphrag 0.0.5: `_policies/_graph_upsert.py` lines 15-55 `summarize_entity_description(..., max_tokens=None)` sends
#     `max_tokens=max_tokens` (None, so JSON null) with `response_model=TEntityDescription`; instructor 1.12.0
#     `providers/openai/utils.py` `handle_json_modes` (Mode.JSON) adds `response_format: json_object` and a system message
#     carrying the schema, which pass A's fast-graphrag log shows on every call (checked with boolean probes only).
def ping_request() -> dict:
    return {"name": PING_NAME, "route": ROUTE, "body": {
        "model": MODEL_PLACEHOLDER, "messages": [{"role": "user", "content": "Reply with the single word OK."}]}}


def nano_entity_summary_request() -> dict:
    prompt = ("You are a helpful assistant that writes one comprehensive description from a list of descriptions of the "
              "same entity. Cover every description, resolve any contradiction, write in the third person and name the "
              "entities.\n\n#######\n-Data-\nEntities: ALPHA WIDGET\n"
              "Description List: ['Alpha Widget is a made-up part that exists only in a test.', "
              "'Alpha Widget is also called the sample widget.']\n#######\nOutput:\n")
    return {"name": "nano_entity_summary", "route": ROUTE, "body": {
        "model": MODEL_PLACEHOLDER, "messages": [{"role": "user", "content": prompt}], "max_tokens": 500}}


def nano_community_report_request() -> dict:
    prompt = ("You are an AI assistant that helps an analyst with general information discovery.\n\n# Goal\n"
              "Write a report of a community, given the entities that belong to it and their relationships. Include a title, "
              "a summary, an impact rating, an explanation of the rating and a list of findings.\n\n"
              "Return output as a well-formed JSON-formatted string with the following format:\n"
              '{"title": <report_title>, "summary": <executive_summary>, "rating": <impact_severity_rating>, '
              '"rating_explanation": <rating_explanation>, "findings": [{"summary": <insight_summary>, '
              '"explanation": <insight_explanation>}]}\n\n# Grounding Rules\n'
              "Do not include information where the supporting evidence for it is not provided.\n\n# Real Data\n\n"
              "Text:\n```\nEntities:\n```csv\nid,entity,type,description\n"
              "0,ALPHA WIDGET,part,A made-up part\n1,BETA GADGET,device,A made-up device\n```\n"
              "Relationships:\n```csv\nid,source,target,description\n"
              "0,ALPHA WIDGET,BETA GADGET,Alpha Widget is a made-up part of Beta Gadget\n```\n```\nOutput:\n")
    return {"name": "nano_community_report", "route": ROUTE, "body": {
        "model": MODEL_PLACEHOLDER, "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}}}


def fast_summary_request() -> dict:
    schema = {"properties": {"description": {"title": "Description", "type": "string"}}, "required": ["description"],
              "title": "TEntityDescription", "type": "object"}
    system = ("Understand the content and return the parsed object in json that matches the following json_schema:\n\n"
              + json.dumps(schema, indent=2) + "\n\nReturn an instance of the JSON, not the schema itself.")
    prompt = ("You are a helpful assistant that summarises the data below. Given the current description, remove redundant "
              "and generic information, resolve any contradiction and give one coherent summary. Write in the third "
              "person and include the entity names.\n\nCurrent:\nAlpha Widget is a made-up part that exists only in a "
              "test. Alpha Widget is also called the sample widget.\n\nUpdated:\n")
    return {"name": "fast_summary", "route": ROUTE, "body": {
        "model": MODEL_PLACEHOLDER, "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}, "max_tokens": None}}


def synthesised_requests() -> list[dict]:
    return [ping_request(), fast_summary_request(), nano_entity_summary_request(), nano_community_report_request()]


# ---- picking recorded requests --------------------------------------------------------------------------------------
def _messages(body: Any) -> list[dict]:
    msgs = body.get("messages") if isinstance(body, dict) else None
    return [m for m in msgs if isinstance(m, dict)] if isinstance(msgs, list) else []


def _roles(body: Any) -> list[Any]:
    return [m.get("role") for m in _messages(body)]


def _format_type(body: Any) -> str | None:
    rf = body.get("response_format") if isinstance(body, dict) else None
    return rf.get("type") if isinstance(rf, dict) and isinstance(rf.get("type"), str) else None


def _is_continuation(body: Any) -> bool:
    """A gleaning call. Every builder asks for a second pass by sending the first prompt again, then the model's own first
    answer as an `assistant` message, then a short user message that asks for more. So the test is the presence of an
    `assistant` turn (message count alone would also match a few-shot prompt)."""
    return "assistant" in _roles(body)


def _is_strict_schema(body: Any) -> bool:
    rf = body.get("response_format") if isinstance(body, dict) else None
    schema = rf.get("json_schema") if isinstance(rf, dict) else None
    return _format_type(body) == "json_schema" and isinstance(schema, dict) and schema.get("strict") is True


def _is_lightrag_extraction(body: Any) -> bool:
    return not _is_continuation(body) and _format_type(body) is None and _roles(body) == ["system", "user"]


def _is_lightrag_gleaning(body: Any) -> bool:
    return _is_continuation(body) and _format_type(body) is None


def _is_fast_extraction(body: Any) -> bool:
    return not _is_continuation(body) and _format_type(body) == "json_object"


def _is_ms_extraction(body: Any) -> bool:
    # Microsoft GraphRAG sends one user message per call and no system message. Its first call is a 49-character greeting
    # that checks the model, then come the extraction calls, then the description summaries. What tells the extraction
    # prompt apart is the tuple delimiter `<|>` it spells out (the summaries and the greeting never do).
    msgs = _messages(body)
    return (not _is_continuation(body) and _format_type(body) is None and _roles(body) == ["user"]
            and "<|>" in str(msgs[0].get("content")))


def _is_nano_extraction(body: Any) -> bool:
    return not _is_continuation(body) and _format_type(body) is None and _roles(body) == ["user"]


PICKS: tuple[tuple[str, str, Any, bool], ...] = (       # name, directory, test, required
    ("lightrag_extraction", "lightrag", _is_lightrag_extraction, True),
    ("lightrag_gleaning", "lightrag", _is_lightrag_gleaning, True),
    ("fast_extraction", "fast", _is_fast_extraction, True),
    ("ms_extraction", "ms", _is_ms_extraction, True),
    ("ms_community_report", "ms", _is_strict_schema, True),
    ("nano_extraction", "nano", _is_nano_extraction, False),
)


def _chat_bodies(directory: Path) -> list[tuple[int, dict]]:
    try:
        calls = pc.calls_in(directory)
    except (OSError, ValueError, KeyError) as exc:
        raise StageAError(f"cannot read a pass-A gateway directory ({type(exc).__name__})") from None
    out = []
    for index, call in enumerate(calls):
        body = call.get("request")
        if (str(call.get("route", "")).endswith("/chat/completions") and call.get("http_status") == 200
                and isinstance(body, dict) and _messages(body) and body.get("stream") is not True):
            out.append((index, body))
    return out


def extract_requests(dirs: Mapping[str, str | Path]) -> list[dict]:
    """The requests file's entries, in the order they will be sent, plus where each recorded one came from (`_source`, a
    position in the pass-A log; the caller removes it before writing)."""
    unknown = sorted(set(dirs) - set(REQUIRED_DIRS) - set(OPTIONAL_DIRS))
    missing = [d for d in REQUIRED_DIRS if d not in dirs]
    if unknown or missing:
        raise StageAError(f"--pass-a-dirs takes {', '.join(REQUIRED_DIRS)} and optionally {', '.join(OPTIONAL_DIRS)}; "
                          f"unknown {unknown or 'none'}, missing {missing or 'none'}")
    for name, path in dirs.items():
        if not Path(path).is_dir():
            raise StageAError(f"the {name} pass-A directory does not exist")
    bodies = {name: _chat_bodies(Path(path)) for name, path in dirs.items()}
    picked: dict[str, dict] = {}
    for name, directory, test, required in PICKS:
        if directory not in bodies:
            continue
        found = next(((i, b) for i, b in bodies[directory] if test(b)), None)
        if found is None:
            if required:
                raise StageAError(f"no recorded request of kind {name} in the {directory} directory")
            continue
        body = copy.deepcopy(found[1])
        body["model"] = MODEL_PLACEHOLDER
        picked[name] = {"name": name, "route": ROUTE, "body": body, "_source": f"{directory} log, call {found[0]}"}
    synth = {r["name"]: r for r in synthesised_requests()}
    order = [PING_NAME, "lightrag_extraction", "lightrag_gleaning", "fast_extraction", "fast_summary", "ms_extraction",
             "ms_community_report", "nano_extraction", "nano_entity_summary", "nano_community_report"]
    out = []
    for name in order:
        if name in picked:
            out.append(picked[name])
        elif name in synth:
            out.append({**synth[name], "_source": "synthesised"})
    if len(out) > MAX_REQUESTS:
        raise StageAError(f"more than {MAX_REQUESTS} requests")
    return out


def body_shapes(body: Mapping[str, Any]) -> list[str]:
    shapes = []
    kind = _format_type(body)
    if kind in ("json_object", "json_schema"):
        shapes.append(kind)
    if "max_tokens" in body:
        shapes.append("max_tokens_null" if body["max_tokens"] is None else "max_tokens")
    return shapes


def request_bytes(entry: Mapping[str, Any]) -> int:
    return len(json.dumps(entry["body"]).encode("utf-8"))


def _json_word_note(entry: Mapping[str, Any]) -> str:
    if _format_type(entry["body"]) != "json_object":
        return ""
    text = " ".join(str(m.get("content")) for m in _messages(entry["body"])).lower()
    return "" if "json" in text else "json_object but the word json is absent (the provider will reject it)"


def print_table(entries: Sequence[Mapping[str, Any]], out: Any) -> None:
    """Name, bytes, shape and origin of each request. Never a word of a request."""
    print(f"{'name':<22}{'bytes':>8}  {'shape':<30}origin", file=out)
    for e in entries:
        shape = ",".join(body_shapes(e["body"])) or "plain"
        note = _json_word_note(e)
        print(f"{e['name']:<22}{request_bytes(e):>8}  {shape:<30}{e.get('_source', '')}" + (f"  NOTE {note}" if note else ""),
              file=out)


# ---- the requests file ----------------------------------------------------------------------------------------------
def load_requests(path: str | Path) -> list[dict]:
    """Read and validate a requests file. A message names the defect, never a value."""
    path = Path(path)
    try:
        info = path.stat()
    except OSError as exc:
        raise StageAError(f"cannot read the requests file ({type(exc).__name__})") from None
    if not stat.S_ISREG(info.st_mode):
        raise StageAError("the requests file is not a regular file")
    if stat.S_IMODE(info.st_mode) & 0o077:
        raise StageAError("the requests file can be read by others (it holds article text); use mode 600")
    if inside_repository(path):
        raise StageAError("the requests file is inside the repository; it holds article text and must live outside it")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise StageAError("the requests file is not valid JSON") from None
    if not isinstance(data, list) or not 1 <= len(data) <= MAX_REQUESTS:
        raise StageAError(f"the requests file must be a JSON list of 1 to {MAX_REQUESTS} entries")
    seen: set[str] = set()
    for number, entry in enumerate(data, 1):
        if not isinstance(entry, dict) or set(entry) != {"name", "route", "body"}:
            raise StageAError(f"entry {number}: must hold exactly name, route and body")
        name = entry["name"]
        if not isinstance(name, str) or not NAME_RE.match(name) or name in seen:
            raise StageAError(f"entry {number}: the name must be unique, lower case, letters, digits and _")
        seen.add(name)
        if entry["route"] != ROUTE:
            raise StageAError(f"entry {number}: the route must be {ROUTE}")
        body = entry["body"]
        if not isinstance(body, dict) or not _messages(body) or not isinstance(body.get("model"), str):
            raise StageAError(f"entry {number}: the body needs a model and messages")
        if body.get("stream") is True:
            raise StageAError(f"entry {number}: a streamed request is not part of stage A")
    return data


# ---- the plan: what a run would do, without doing it ------------------------------------------------------------------
def forwarded_body(profile: pb.Profile, body: Mapping[str, Any], model: str) -> dict:
    """The body the gateway would forward: the client's, plus the output-limit field when the client sent none and then
    the profile's request defaults for fields the client did not send (the order the gateway applies them)."""
    out = dict(body)
    out["model"] = model
    if out.get("max_tokens") is None and out.get("max_completion_tokens") is None:
        out["max_completion_tokens"] = profile.output_limit_default
    for key, value in profile.request_defaults.items():
        out.setdefault(key, value)
    return out


def worst_case_usd(profile: pb.Profile, body: Mapping[str, Any], model: str) -> Decimal:
    """The gateway's reservation for this request (tools/metering_gateway.md, "How the cap works"): every input byte
    pessimistically costs half a token at the dearer of the input and cache-write prices, and the output is the full limit."""
    forward = forwarded_body(profile, body, model)
    limits = [forward[k] for k in ("max_completion_tokens", "max_tokens")
              if isinstance(forward.get(k), int) and not isinstance(forward.get(k), bool)]
    input_tokens = -(-len(json.dumps(forward).encode("utf-8")) // 2)
    price_in = max(profile.input_per_mtok, profile.cache_write_per_mtok or Decimal(0))
    return (Decimal(input_tokens) * price_in + Decimal(max(limits)) * profile.output_per_mtok) / Decimal(1_000_000)


def ledger_spent(profile: pb.Profile) -> tuple[int, Decimal]:
    """(records, spend) already in the pilot's ledger, read-only; a ledger that does not exist yet holds nothing."""
    try:
        records = pb.read_ledger(Path(profile.ledger_dir) / pb.LEDGER_LOG, strict=True)
        return len(records), pb.sum_costs(records)
    except (OSError, pc.PassAError) as exc:
        raise StageAError(f"the ledger cannot be read ({profile.redact(str(exc))[:120]})") from None


def make_plan(profile: pb.Profile, entries: Sequence[Mapping[str, Any]], model: str) -> dict:
    records, spent = ledger_spent(profile)
    allowed = min(STAGE_CAP, PILOT_CAP - spent)
    rows = [{"name": e["name"], "bytes": request_bytes(e), "shapes": body_shapes(e["body"]),
             "worst_case_usd": worst_case_usd(profile, e["body"], model)} for e in entries]
    total = sum((r["worst_case_usd"] for r in rows), Decimal(0))
    largest = max(rows, key=lambda r: r["bytes"])
    problems = []
    if not pb.NAME_RE.match(model):
        problems.append("--model may hold only letters, digits and . _ : / -")
    if profile.allowance_usd > allowed:
        problems.append(f"the profile's allowance USD {pb.money_text(profile.allowance_usd)} is above what stage A may load: "
                        f"the lower of the stage cap USD {pb.money_text(STAGE_CAP)} and the pilot cap USD "
                        f"{pb.money_text(PILOT_CAP)} less USD {pb.money_text(spent)} already in the ledger")
    if total > min(profile.allowance_usd, STAGE_CAP):
        problems.append(f"the worst-case cost USD {pb.money_text(total)} is above the allowance (check the prices and the "
                        "output limit in the profile)")
    if largest["worst_case_usd"] <= REFUSAL_ALLOWANCE:
        problems.append("the largest request could not exceed the refusal test's allowance, so that test would prove nothing")
    if len(entries) + 1 > MAX_CALLS:
        problems.append(f"more than {MAX_CALLS} calls")
    return {"rows": rows, "worst_case_total_usd": total, "largest": largest["name"], "ledger_records": records,
            "spent_before_usd": spent, "allowed_usd": allowed, "problems": problems,
            "gateway_cap_usd": spent + profile.allowance_usd}


def print_plan(profile: pb.Profile, plan: Mapping[str, Any], model: str, out: Any) -> None:
    print(f"stage A plan: {len(plan['rows'])} request(s) to {model}, one call each, plus the refusal test "
          f"({len(plan['rows']) + 1} of at most {MAX_CALLS} calls)", file=out)
    print(f"{'name':<22}{'bytes':>8}  {'shape':<30}{'worst case USD':>16}", file=out)
    for r in plan["rows"]:
        print(f"{r['name']:<22}{r['bytes']:>8}  {(','.join(r['shapes']) or 'plain'):<30}{pb.money_text(r['worst_case_usd']):>16}",
              file=out)
    print(f"worst case, all requests (the gateway's reservation formula): USD {pb.money_text(plan['worst_case_total_usd'])}", file=out)
    print(f"prices per million tokens: input {pb.money_text(profile.input_per_mtok)}, output {pb.money_text(profile.output_per_mtok)}"
          f" (read {profile.read_at}, {profile.source_url}); output limit {profile.output_limit_default}; "
          f"request defaults {sorted(profile.request_defaults)}", file=out)
    print(f"caps: stage USD {pb.money_text(STAGE_CAP)}; this run's allowance USD {pb.money_text(profile.allowance_usd)}; "
          f"ledger holds {plan['ledger_records']} record(s), USD {pb.money_text(plan['spent_before_usd'])}; the gateway "
          f"would load a cap of USD {pb.money_text(plan['gateway_cap_usd'])}", file=out)
    print(f"refusal test: the largest request ({plan['largest']}) against an allowance of USD {pb.money_text(REFUSAL_ALLOWANCE)}",
          file=out)


# ---- talking to the gateway -----------------------------------------------------------------------------------------
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))      # a system proxy must never see loopback traffic


def _http(url: str, payload: dict | None, timeout: float) -> tuple[int | None, bytes]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json", "Authorization": DUMMY_AUTHORIZATION} if data is not None else {}
    try:
        with OPENER.open(urllib.request.Request(url, data=data, headers=headers), timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        try:
            return exc.code, exc.read()
        finally:
            exc.close()
    except (urllib.error.URLError, OSError):         # TimeoutError is an OSError
        return None, b""


def verify_cap_loaded(gw: pb.HostedGateway) -> None:
    """Nothing is sent before the gateway says it holds the cap this run computed (ledger spend plus the allowance)."""
    status, raw = _http(f"http://127.0.0.1:{gw.port}/_meter/summary", None, 10)
    try:
        cap = Decimal(str(json.loads(raw)["cap"]))
    except (ValueError, KeyError, TypeError, ArithmeticError):
        cap = None
    if status != 200 or cap is None or cap != gw.cap:
        raise StageAError("the gateway did not report the cap this run computed; nothing was sent")


def _int(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _token(value: Any) -> str | None:
    return value if isinstance(value, str) and TOKEN_RE.match(value) else None


def usage_names(usage: Any, prefix: str = "", depth: int = 0) -> list[str]:
    """The NAMES in a usage object, nested ones joined by dots: `completion_tokens_details.reasoning_tokens`."""
    names: list[str] = []
    if isinstance(usage, dict):
        for key, value in usage.items():
            if isinstance(key, str) and TOKEN_RE.match(key):
                names.append(prefix + key)
                if depth < 3:
                    names += usage_names(value, prefix + key + ".", depth + 1)
    return names


def describe_error(obj: Any, raw: bytes) -> dict:
    err = obj.get("error") if isinstance(obj, dict) else None
    err = err if isinstance(err, dict) else {}
    message = err.get("message")
    return {"type": _token(err.get("type")), "code": _token(err.get("code")), "param": _token(err.get("param")),
            "message_length": len(message) if isinstance(message, str) else len(raw)}


def describe_call(entry: Mapping[str, Any], attempt: int, status: int | None, raw: bytes, record: Mapping[str, Any] | None) -> dict:
    """Everything recorded about one call, none of it text: numbers, field names, short codes."""
    body = entry["body"]
    try:
        obj = json.loads(raw) if raw else None
    except ValueError:
        obj = None
    obj = obj if isinstance(obj, dict) else None
    record = record or {}
    usage = obj.get("usage") if obj else None
    usage = usage if isinstance(usage, dict) else None
    details = usage.get("completion_tokens_details") if usage else None
    choices = obj.get("choices") if obj else None
    first = choices[0] if isinstance(choices, list) and choices and isinstance(choices[0], dict) else {}
    applied = record.get("request_defaults_applied")
    applied = [a for a in applied if isinstance(a, str)] if isinstance(applied, list) else []
    limit = "none"
    if "max_tokens" in body:
        limit = "max_tokens=null" if body["max_tokens"] is None else f"max_tokens={body['max_tokens']}"
    null_limit = None
    if "max_tokens" in body and body["max_tokens"] is None:
        null_limit = "max_completion_tokens" in applied
    model_reported = obj.get("model") if obj else None
    call: dict[str, Any] = {
        "request": entry["name"], "attempt": attempt, "http_status": status,
        "model_reported": model_reported if isinstance(model_reported, str) and pb.NAME_RE.match(model_reported) else None,
        "finish_reason": _token(first.get("finish_reason")),
        "prompt_tokens": _int(usage.get("prompt_tokens")) if usage else None,
        "completion_tokens": _int(usage.get("completion_tokens")) if usage else None,
        "reasoning_tokens": _int(details.get("reasoning_tokens")) if isinstance(details, dict) else None,
        "usage_fields": sorted(set(usage_names(usage))),
        "cost_usd": record.get("cost") if isinstance(record.get("cost"), str) else None,
        "cached_input_tokens": _int(record.get("cached_input_tokens")),
        "cache_creation_input_tokens": _int(record.get("cache_creation_input_tokens")),
        "request_defaults_applied": applied, "client_limit": limit, "null_max_tokens_with_injected_limit": null_limit,
        "gateway_refusal": _token(record.get("refusal")), "voided": record.get("voided") is True,
        "usage_missing": record.get("usage_missing") is True, "latency_ms": _int(record.get("latency_ms")),
        "error": None,
    }
    if status is not None and status != 200:
        call["error"] = describe_error(obj, raw)
    return call


def judge(call: Mapping[str, Any], *, is_ping: bool) -> str:
    """What the run does after a call: ok, incompatible (a recorded result, the run goes on), retry (once), or a stop reason."""
    status = call["http_status"]
    if status is None:
        return "stop:gateway_unreachable"
    if call["gateway_refusal"] is not None:
        return "stop:gateway_refusal"
    if status == 200:
        return "stop:usage_missing" if call["usage_missing"] else "ok"
    if status in (401, 403):
        return "stop:auth"
    if status == 429 or status >= 500:
        return "retry"
    if status in (400, 422):
        return "stop:ping_rejected" if is_ping else "incompatible"
    return "stop:unexpected_status"


def outcome_of(call: Mapping[str, Any], verdict: str) -> str:
    return {"ok": "ok", "incompatible": "rejected_incompatible", "retry": "retryable_error"}.get(verdict, verdict[5:])


# ---- the gates ------------------------------------------------------------------------------------------------------
def compute_gates(entries: Sequence[Mapping[str, Any]], calls: Sequence[Mapping[str, Any]], not_sent: Sequence[str],
                  refusal: Mapping[str, Any], total_cost: Decimal) -> dict:
    """The plan's stage-A gates as booleans, plus the lists a reader needs to see why. `calls` are all attempts in order;
    a request's final attempt decides whether it was accepted."""
    final = {c["request"]: c for c in calls}
    answers = [c for c in final.values() if c["http_status"] == 200]
    rejected = [c for c in final.values() if c["outcome"] == "rejected_incompatible"]
    shapes: dict[str, dict[str, list[str]]] = {}
    for entry in entries:
        call = final.get(entry["name"])
        if call is None:
            continue
        for shape in body_shapes(entry["body"]):
            slot = shapes.setdefault(shape, {"accepted": [], "rejected": []})
            if call["http_status"] == 200:
                slot["accepted"].append(entry["name"])
            elif call["outcome"] == "rejected_incompatible":
                slot["rejected"].append(entry["name"])
    sent_calls = [c for c in calls if c["http_status"] is not None]
    reasoning_values = [c["reasoning_tokens"] for c in answers]
    reported = bool(answers) and all(v is not None for v in reasoning_values)
    zero = bool(answers) and all(v == 0 for v in reasoning_values)
    no_limit = [c for c in sent_calls if c["client_limit"] in ("none", "max_tokens=null")]
    null_calls = [c for c in final.values() if c["null_max_tokens_with_injected_limit"] is not None]
    usage_names_seen = sorted({n for c in calls for n in c["usage_fields"]})
    reasoning_accepted = (bool(answers) and bool(sent_calls)
                          and all("reasoning_effort" in c["request_defaults_applied"] for c in sent_calls)
                          and not any(c["error"] and c["error"]["param"] == "reasoning_effort" for c in sent_calls))
    return {
        "every_call_200_or_recorded_incompatible": bool(final) and all(
            c["http_status"] == 200 or c["outcome"] == "rejected_incompatible" for c in final.values()),
        "no_request_left_unsent": not not_sent,
        "reasoning_effort_accepted": reasoning_accepted,
        "reasoning_tokens_reported_on_every_answer": reported,
        "reasoning_tokens_zero_on_every_answer": zero,
        "reasoning_off_ok": reasoning_accepted and reported and zero,
        "output_limit_injected_wherever_the_client_set_none": bool(no_limit) and all(
            "max_completion_tokens" in c["request_defaults_applied"] for c in no_limit),
        "null_max_tokens_with_injected_limit": (None if not null_calls else {
            "calls": len(null_calls), "all_accepted": all(c["http_status"] == 200 for c in null_calls),
            "all_carried_the_injected_field": all(c["null_max_tokens_with_injected_limit"] for c in null_calls)}),
        "usage_present_on_every_answer": bool(answers) and all(
            c["prompt_tokens"] is not None and c["completion_tokens"] is not None and not c["usage_missing"] for c in answers),
        "usage_has_a_cache_write_field": any(re.search(r"cache.*(write|creat)|(write|creat).*cache", n, re.I)
                                             for n in usage_names_seen),
        "refusal_test_passed": refusal.get("passed") is True,
        "total_cost_within_stage_cap": total_cost <= STAGE_CAP,
        "shapes": shapes,
        "rejected_requests": [c["request"] for c in rejected],
        "usage_field_names": usage_names_seen,
        "answers_ended_by_the_output_limit": sum(1 for c in answers if c["finish_reason"] == "length"),
    }


# ---- the refusal test -----------------------------------------------------------------------------------------------
def refusal_proof(records: Sequence[Mapping[str, Any]], status: int | None, raw: bytes) -> dict:
    """Did the throwaway gateway refuse the call and forward nothing? Read from its own ledger: a refusal record, status
    429, no tokens, zero cost, not voided, no usage flag and no model reported. A call that reached an upstream would show
    one of those (tokens, a cost, voided, a reported model) or no refusal at all."""
    try:
        code = (json.loads(raw).get("error") or {}).get("code")
    except (ValueError, AttributeError):
        code = None
    one = records[0] if len(records) == 1 else {}
    try:
        zero_cost = Decimal(str(one.get("cost"))) == 0
    except ArithmeticError:
        zero_cost = False
    nothing_forwarded = (len(records) == 1 and one.get("refusal") == "gateway_budget_exceeded" and one.get("http_status") == 429
                         and one.get("input_tokens") is None and one.get("output_tokens") is None and zero_cost
                         and one.get("voided") is False and one.get("usage_missing") is False
                         and one.get("model_reported") is None)
    seen_429 = status == 429 and code == "gateway_budget_exceeded"
    return {"client_http_status": status, "client_error_code": _token(code), "ledger_records": len(records),
            "nothing_forwarded": nothing_forwarded, "passed": seen_429 and nothing_forwarded}


def free_loopback_url() -> str:
    """A loopback URL that nothing listens on: a call forwarded to it fails as a 502 and cannot reach any provider."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    return f"http://127.0.0.1:{port}/v1"


def run_refusal_test(profile: pb.Profile, entries: Sequence[Mapping[str, Any]], out_dir: Path, *, model: str, embed_model: str,
                     local_url: str, upstream_url: str | None, allowance: Decimal, timeout: float) -> dict:
    largest = max(entries, key=request_bytes)            # the first of equally large ones
    ledger = out_dir / "refusal-ledger"
    second = replace(profile, ledger_dir=str(ledger), allowance_usd=allowance, base_url=upstream_url or free_loopback_url())
    gw = pb.HostedGateway(out_dir / "gateway-refusal", local_url, [model, embed_model], REPO_ROOT, profile=second)
    with gw:
        verify_cap_loaded(gw)
        status, raw = _http(gw.base_url + ROUTE, {**largest["body"], "model": model}, timeout)
        records = gw.run_records()
    removed = False
    try:                                                  # the throwaway body log holds the largest request's text
        (ledger / pb.LEDGER_BODIES).unlink()
        removed = True
    except FileNotFoundError:
        removed = True
    except OSError:
        pass
    proof = refusal_proof(records, status, raw)
    return {"request": largest["name"], "request_bytes": request_bytes(largest), "allowance_usd": pb.money_text(allowance),
            "upstream": "a URL given by the caller" if upstream_url else "a loopback port nothing listens on",
            **proof, "throwaway_body_log_removed": removed}


# ---- the run --------------------------------------------------------------------------------------------------------
def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d %H:%M")


def _send_with_retry(gw: pb.HostedGateway, entry: Mapping[str, Any], model: str, timeout: float, calls: list[dict],
                     not_sent: list[str], attempts: int, out: Any) -> tuple[int, dict | None]:
    """Send one request through the gateway: once, and once more after a 429 or 5xx from the provider. Appends one dict per
    attempt to `calls` and returns (forwarded attempts so far, the stop that ended the run or None). A 400 or 422 is a result
    and is neither retried nor altered."""
    attempt = 0
    while True:
        if attempts >= MAX_ATTEMPTS:
            not_sent.append(entry["name"])
            return attempts, {"reason": "attempt_limit", "at_request": entry["name"], "http_status": None}
        attempt += 1
        attempts += 1
        before = len(gw.run_records())
        status, raw = _http(gw.base_url + ROUTE, {**entry["body"], "model": model}, timeout)
        fresh = gw.run_records()[before:]
        call = describe_call(entry, attempt, status, raw, fresh[0] if len(fresh) == 1 else None)
        verdict = judge(call, is_ping=entry["name"] == PING_NAME)
        if len(fresh) != 1 and not verdict.startswith("stop:"):
            verdict = "stop:ledger_mismatch"                 # one call must add exactly one record
        if verdict == "retry" and attempt >= 2:
            verdict = "stop:provider_unavailable_after_retry"
        call["outcome"] = outcome_of(call, verdict)
        calls.append(call)
        print(f"  {entry['name']:<22} attempt {attempt}  http {call['http_status']}  {call['outcome']}"
              f"  tokens {call['prompt_tokens']}/{call['completion_tokens']}  cost {call['cost_usd']}", file=out, flush=True)
        if verdict == "retry":
            time.sleep(RETRY_WAIT_S)
            continue
        if verdict.startswith("stop:"):
            return attempts, {"reason": verdict[5:], "at_request": entry["name"], "http_status": call["http_status"]}
        if pb.sum_costs(gw.run_records()) > STAGE_CAP:
            return attempts, {"reason": "spend_above_stage_cap", "at_request": entry["name"], "http_status": call["http_status"]}
        return attempts, None


def run_stage(profile: pb.Profile, entries: Sequence[Mapping[str, Any]], out_dir: Path, *, model: str = DEFAULT_MODEL,
              embed_model: str = DEFAULT_EMBED_MODEL, local_url: str = DEFAULT_LOCAL_URL, out: Any = None,
              refusal_upstream_url: str | None = None, refusal_allowance: Decimal = REFUSAL_ALLOWANCE) -> tuple[dict, int]:
    """Send the requests, then run the refusal test. Returns (result, exit status). Raises StageAError before anything is sent."""
    out = out if out is not None else sys.stdout
    plan = make_plan(profile, entries, model)
    if plan["problems"]:
        raise StageAError("; ".join(plan["problems"]))
    out_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(out_dir, 0o700)
    timeout = float(profile.upstream_timeout_s) + 60
    started = _now()
    calls: list[dict] = []
    not_sent: list[str] = []
    stop: dict | None = None
    attempts = 0
    gw = pb.HostedGateway(out_dir / "gateway-main", local_url, [model, embed_model], REPO_ROOT, profile=profile)
    current = ""
    with gw:
        verify_cap_loaded(gw)
        try:
            for entry in entries:
                current = entry["name"]
                if stop is not None:
                    not_sent.append(entry["name"])
                    continue
                attempts, stop = _send_with_retry(gw, entry, model, timeout, calls, not_sent, attempts, out)
        except (KeyboardInterrupt, Exception) as exc:      # noqa: BLE001 - recorded by class name; the ledger keeps the calls
            stop = {"reason": "interrupted" if isinstance(exc, KeyboardInterrupt) else f"harness_error_{type(exc).__name__}",
                    "at_request": current, "http_status": None}
            done = {c["request"] for c in calls}
            not_sent.extend(e["name"] for e in entries if e["name"] not in done and e["name"] not in not_sent)
    records = pb.read_ledger(gw.log_path, strict=True, start=gw.log_offset)
    total = pb.sum_costs(records)
    refusal: dict[str, Any]
    if stop is None:
        print("refusal test: a second gateway with a throwaway ledger and an allowance of "
              f"USD {pb.money_text(refusal_allowance)}", file=out, flush=True)
        try:
            refusal = run_refusal_test(profile, entries, out_dir, model=model, embed_model=embed_model, local_url=local_url,
                                       upstream_url=refusal_upstream_url, allowance=refusal_allowance, timeout=timeout)
        except (KeyboardInterrupt, pc.PassAError) as exc:
            refusal = {"skipped": "interrupted" if isinstance(exc, KeyboardInterrupt) else f"failed to run ({type(exc).__name__})",
                       "passed": False}
    else:
        refusal = {"skipped": f"stopped earlier ({stop['reason']})", "passed": False}
    gates = compute_gates(entries, calls, not_sent, refusal, total)
    models = sorted({c["model_reported"] for c in calls if c["model_reported"]})
    result = {
        "stage": "A", "started_utc": started, "finished_utc": _now(), "model_requested": model, "models_reported": models,
        "caps_usd": {"stage_cap": pb.money_text(STAGE_CAP), "allowance": pb.money_text(profile.allowance_usd),
                     "gateway_cap": pb.money_text(gw.cap), "ledger_spent_before": pb.money_text(gw.spent_before)},
        "requests": [{"name": r["name"], "bytes": r["bytes"], "shapes": r["shapes"],
                      "worst_case_usd": pb.money_text(r["worst_case_usd"])} for r in plan["rows"]],
        "calls": calls, "not_sent": not_sent, "stopped": stop, "refusal_test": refusal, "gates": gates,
        "totals": {"forwarded_attempts": attempts, "gateway_cost_usd": pb.money_text(total), "gateway_records": len(records)},
        "console_check": CONSOLE_NOTE.format(n=attempts, total=pb.money_text(total)),
        "hosted": pb.hosted_block_for(gw),
        "note": "numbers, field names and short codes only: no request or response text, no key and no path is kept here",
    }
    write_private(out_dir / RESULT_NAME, json.dumps(result, indent=1, sort_keys=True) + "\n")
    complete = stop is None and refusal.get("passed") is True
    return result, 0 if complete else 3


def print_result(result: Mapping[str, Any], out: Any) -> None:
    gates = result["gates"]
    print(f"stage A: {result['totals']['forwarded_attempts']} forwarded attempt(s), gateway cost USD "
          f"{result['totals']['gateway_cost_usd']}, models reported {result['models_reported'] or 'none'}", file=out)
    if result["stopped"]:
        print(f"STOPPED: {result['stopped']['reason']} at {result['stopped']['at_request']}; not sent: "
              f"{', '.join(result['not_sent']) or 'none'}", file=out)
    refusal = result["refusal_test"]
    print("refusal test: " + (refusal["skipped"] if "skipped" in refusal else
                              f"{'PASSED' if refusal['passed'] else 'FAILED'} (client saw {refusal['client_http_status']} "
                              f"{refusal['client_error_code']}; ledger records {refusal['ledger_records']}; nothing forwarded "
                              f"{refusal['nothing_forwarded']})"), file=out)
    for name, value in gates.items():
        if isinstance(value, bool):
            print(f"  gate {name}: {'yes' if value else 'NO'}", file=out)
    for shape, slot in gates["shapes"].items():
        print(f"  shape {shape}: accepted {slot['accepted'] or 'none'}; rejected {slot['rejected'] or 'none'}", file=out)
    print(f"  usage fields: {', '.join(gates['usage_field_names']) or 'none'}", file=out)
    print(result["console_check"], file=out)
    print(f"result written to {RESULT_NAME} in --out-dir (mode 600)", file=out)


# ---- command line ---------------------------------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="passb_stage_a.py", description="Pass B stage A: extract the requests, then replay them "
                                "through the metering gateway against the real provider (see the module docstring).")
    sub = p.add_subparsers(dest="command", required=True)
    e = sub.add_parser("extract", help="free and local: pick the requests and write the mode-600 requests file")
    e.add_argument("--pass-a-dirs", nargs="+", required=True, metavar="NAME=DIR",
                   help="pass-A gateway directories (each holds meter.jsonl and its .bodies.jsonl): lightrag=, fast=, ms= "
                        "and optionally nano=")
    e.add_argument("--out", required=True, help="the requests file to create; outside the repository, not in a scratch directory")
    r = sub.add_parser("run", help="the dry run by default; --send makes the paid calls")
    r.add_argument("--profile", required=True, help="the hosted profile (passb_profile.example.json)")
    r.add_argument("--requests", required=True, help="the requests file `extract` wrote")
    r.add_argument("--out-dir", required=True, help="a new or empty directory outside the repository for the result and the gateways")
    r.add_argument("--send", action="store_true", help="send the requests; without it nothing is started or written")
    r.add_argument("--model", default=DEFAULT_MODEL, help=f"the chat model name (default {DEFAULT_MODEL})")
    r.add_argument("--embed-model", default=DEFAULT_EMBED_MODEL, help="a local embedding model name the gateway needs but never calls")
    r.add_argument("--local-upstream-url", default=DEFAULT_LOCAL_URL, help="the local upstream the gateway is configured with; never called")
    return p


def _parse_dirs(items: Sequence[str]) -> dict[str, str]:
    dirs: dict[str, str] = {}
    for item in items:
        name, sep, path = item.partition("=")
        if not sep or not name or not path or name in dirs:
            raise StageAError("--pass-a-dirs takes NAME=DIR, each name once")
        dirs[name] = path
    return dirs


def command_extract(args: argparse.Namespace) -> int:
    out_path = Path(args.out)
    if inside_repository(out_path):
        raise StageAError("--out is inside the repository; the file holds article text and must live outside it")
    if out_path.exists():
        raise StageAError(f"{out_path.name} already exists; this program does not overwrite a file")
    entries = extract_requests(_parse_dirs(args.pass_a_dirs))
    print_table(entries, sys.stdout)
    write_private(out_path, json.dumps([{k: v for k, v in e.items() if k != "_source"} for e in entries], indent=1) + "\n")
    print(f"wrote {len(entries)} request(s) to {out_path.name} (mode 600)")
    print("WARNING: that file holds article text. Keep it outside the repository and do NOT leave it in a scratch directory "
          "(a session's scratch area does not outlive the session); never commit, paste or mail it.")
    if looks_like_scratch(out_path):
        print("WARNING: the file you just wrote is under a temporary or scratch directory. Move it to a durable private place.")
    return 0


def command_run(args: argparse.Namespace) -> int:
    profile = pb.load_profile(args.profile)
    entries = load_requests(args.requests)
    out_dir = Path(args.out_dir)
    if inside_repository(out_dir):
        raise StageAError("--out-dir is inside the repository; its throwaway ledger and logs hold article text")
    plan = make_plan(profile, entries, args.model)
    if out_dir.exists() and (not out_dir.is_dir() or any(out_dir.iterdir())):
        plan["problems"].append("--out-dir must be new or empty (nothing is overwritten)")
    print_plan(profile, plan, args.model, sys.stdout)
    if plan["problems"]:
        for problem in plan["problems"]:
            print(f"REFUSED: {problem}", file=sys.stderr)
        return 2
    if not args.send:
        print("DRY RUN: nothing was started and nothing was written. Add --send to make the calls.")
        return 0
    result, status = run_stage(profile, entries, out_dir, model=args.model, embed_model=args.embed_model,
                               local_url=args.local_upstream_url)
    print_result(result, sys.stdout)
    return status


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return command_extract(args) if args.command == "extract" else command_run(args)
    except (StageAError, pb.ProfileError) as exc:
        print(f"passb_stage_a: {exc}", file=sys.stderr)
        return 2
    except pc.PassAError as exc:
        print(f"passb_stage_a: {type(exc).__name__}: {str(exc)[:300]}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
