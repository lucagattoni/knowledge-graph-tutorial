"""Watchdog for the paid pilot (plan item F7): stops the runner and the gateway the moment a stop rule fires.

It runs beside a paid stage. Every few seconds it reads what the metering gateway has appended to its two logs, and when
one of the pre-registered stop rules (kb-kg/experiments/x2-index-cost/pass-b-plan.md, "Stop rules") fires it writes a
report, sends SIGTERM to the process groups and pids it was given, waits, and sends SIGKILL to any that are still alive.

    python passb_watchdog.py --gateway-dir DIR --stop-at-usd 0.09 --kill-pgid RUNNER --kill-pid GATEWAY --report PATH

Inputs, both in the gateway directory and both read incrementally (a file offset is kept; a partial last line is left
until it is complete; a file that does not exist yet is not an error):

    meter.jsonl                  one record per finished call (tools/metering_gateway.md, "The log")
    meter.jsonl.bodies.jsonl     {call_id, request, response} per call, raw text; needs `log_bodies = true`

The eight rules, in this order. Counts are over the calls read so far (a record is "seen" once its line is complete).

    1 provider_error      http_status >= 400 and refusal null. A 429 or a 5xx is tolerated `tolerated_retryable` time(s)
                          per run; a further one trips. Any other 4xx trips at once.
    2 gateway_refusal     any record whose refusal is not null.
    3 usage_missing       any record with usage_missing true.
    4 reasoning_tokens    any chat response body with usage.completion_tokens_details.reasoning_tokens > 0.
    5 length_stops        among chat answers (a chat record whose body parses as JSON with a non-empty `choices`), the
                          share with choices[0].finish_reason == "length" exceeds `length_share`, once at least
                          `min_sample` chat answers are seen.
    6 repeated_requests   the share of records whose request_sha256 was already seen exceeds `repeat_share`, once at
                          least `min_sample` records are seen. Only records in the repeat window count (`repeat_since`,
                          below); without one, every record does.
    7 voided_calls        more than `voided_max` records with voided true.
    8 spend               the sum of the records' cost (Decimal, never float) exceeds `stop_at_usd`.

Choices that go beyond the rules as written, each one for a reason:

* A record whose cost cannot be read as a finite number trips `spend` (the spend is then unknown, and a guard on money
  does not guess). The gateway always writes a decimal string, so this only fires on a damaged line.
* `watchdog_error`: if reading the logs fails with an error other than "file missing" three polls in a row, the watchdog
  stops everything. A guard that cannot see is not a guard. Only the exception's class name is kept.
* `since` (CLI `--since`, `--from-now`): the plan keeps ONE ledger for the whole pilot, so a stage's watchdog would
  otherwise count the earlier stages' calls (their spend, their voided calls). Records whose `ts` is before `since` are
  ignored. A record without a readable `ts` is not ignored.
* `repeat_since` (CLI `--repeat-since`): the repeat rule looks for a retry loop, not for a second run. Stage C is run twice
  on the same documents, so the second run's requests are the first run's, byte for byte (found by the dress rehearsal of
  the ladder, where the second run tripped this rule within a second). Records stamped before `repeat_since` still count for
  every other rule, but their hashes are not remembered and they are not in the repeat share's denominator. A record without
  a readable `ts` is in the window. Without `repeat_since` every record is.
* Chat records whose body never arrives (the gateway was started without `log_bodies`), and bodies that are not JSON
  (streams), cannot be checked by rules 4 and 5. They are counted (`chat_records_without_body`, `unparsed_bodies`) and
  appear in the report, not guessed at. Rules 4 and 5 are blind without bodies: start the gateway with `log_bodies = true`.
  The CLI prints a one-line summary when it ends and a WARNING on stderr when chat calls have no body.
* A record whose `http_status` is not an integer (the gateway writes an integer or null) is not read as an error.

Nothing from a request or a response body is ever kept in a Trip, the report or the output: only counts, rule names and
call ids. The kill step signals what it is given: `--kill-pgid` signals a whole process group with `os.killpg` (start the
runner in its own session, so its group id is its pid, and its child processes go with it), `--kill-pid` signals single
processes (the gateway). Groups get SIGTERM before pids, so the runner stops sending first; one grace period (10 s) covers
all of them, then SIGKILL to what is left. A pgid at most 1, or the watchdog's own group, and a pid at most 1 or the
watchdog's own, are refused (exit 2). The report holds the outcome per pid under "kill" and per group under "kill_groups".

Exit status of the CLI: 3 when a rule tripped, 0 when `--max-seconds` ran out (`0` means "read once") or the watchdog was
interrupted quietly, 2 on a usage error. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

METER_NAME = "meter.jsonl"
BODIES_NAME = "meter.jsonl.bodies.jsonl"
RULE_ORDER = ("provider_error", "gateway_refusal", "usage_missing", "reasoning_tokens", "length_stops",
              "repeated_requests", "voided_calls", "spend")
SAFE_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
MAX_IDS = 5
MAX_POLL_ERRORS = 3
EXIT_TRIPPED = 3


def _decimal(value: Any) -> Decimal | None:
    """A finite Decimal from a Decimal, int or numeric string; None for anything else (bool, None, NaN, text)."""
    if isinstance(value, bool):
        return None
    try:
        if isinstance(value, Decimal):
            out = value
        elif isinstance(value, (int, float)):
            out = Decimal(str(value))
        elif isinstance(value, str):
            out = Decimal(value.strip())
        else:
            return None
    except InvalidOperation:
        return None
    return out if out.is_finite() else None


@dataclass(frozen=True)
class Rules:
    """The thresholds. `stop_at_usd` is the stage's "stop at" (spend of the calls the watchdog reads, not the ledger)."""
    stop_at_usd: Decimal
    length_share: Decimal = Decimal("0.05")
    repeat_share: Decimal = Decimal("0.05")
    voided_max: int = 3
    min_sample: int = 20
    tolerated_retryable: int = 1

    def __post_init__(self) -> None:
        for name in ("stop_at_usd", "length_share", "repeat_share"):
            value = _decimal(getattr(self, name))
            if value is None or value < 0:
                raise ValueError(f"{name}: a non-negative number is required, got {getattr(self, name)!r}")
            object.__setattr__(self, name, value)
        for name in ("length_share", "repeat_share"):
            if getattr(self, name) > 1:
                raise ValueError(f"{name}: a share between 0 and 1 is required")
        for name, low in (("voided_max", 0), ("min_sample", 1), ("tolerated_retryable", 0)):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < low:
                raise ValueError(f"{name}: an integer of at least {low} is required, got {value!r}")

    def as_dict(self) -> dict[str, Any]:
        return {"stop_at_usd": str(self.stop_at_usd), "length_share": str(self.length_share),
                "repeat_share": str(self.repeat_share), "voided_max": self.voided_max,
                "min_sample": self.min_sample, "tolerated_retryable": self.tolerated_retryable}


@dataclass(frozen=True)
class Trip:
    """A rule that fired. `message` and `counts` hold numbers only; `call_ids` are at most five ids of the calls involved."""
    rule: str
    message: str
    counts: Mapping[str, Any]
    call_ids: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {"rule": self.rule, "message": self.message, "counts": dict(self.counts), "call_ids": list(self.call_ids)}


@dataclass(frozen=True)
class BodyFacts:
    """What a response body says, with no text kept. kind: "answer" (JSON with a non-empty choices list), "json" (any other
    JSON object, for example an error body or embeddings), "unparsed" (not JSON, not an object, or absent: a stream)."""
    kind: str
    finish_reason: Any = None
    reasoning: bool = False


def body_facts(response: Any) -> BodyFacts:
    if isinstance(response, str):
        try:
            obj = json.loads(response)
        except (ValueError, RecursionError):
            return BodyFacts("unparsed")
    else:
        obj = response
    if not isinstance(obj, dict):
        return BodyFacts("unparsed")
    usage = obj.get("usage")
    details = usage.get("completion_tokens_details") if isinstance(usage, dict) else None
    reasoning_tokens = _decimal(details.get("reasoning_tokens")) if isinstance(details, dict) else None
    reasoning = reasoning_tokens is not None and reasoning_tokens > 0
    choices = obj.get("choices")
    if isinstance(choices, list) and choices and isinstance(choices[0], dict):
        return BodyFacts("answer", choices[0].get("finish_reason"), reasoning)
    return BodyFacts("json", None, reasoning)


def _parse_ts(text: Any) -> datetime | None:
    if not isinstance(text, str):
        return None
    try:
        parsed = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _status(record: Mapping[str, Any]) -> int | None:
    value = record.get("http_status")
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    return value


class State:
    """Counters over every call read so far. Feed it records and body-log entries in any order and in pieces: a chat record
    and its body are joined by call_id whichever arrives first. `trips()` is a pure function of the counters."""

    def __init__(self, rules: Rules, since: str | datetime | None = None, repeat_since: str | datetime | None = None):
        self.rules = rules
        self.since = _parse_ts(since) if isinstance(since, str) else since
        if isinstance(since, str) and self.since is None:
            raise ValueError("since: not a readable ISO timestamp")
        self.repeat_since = _parse_ts(repeat_since) if isinstance(repeat_since, str) else repeat_since
        if isinstance(repeat_since, str) and self.repeat_since is None:
            raise ValueError("repeat_since: not a readable ISO timestamp")
        self.records = 0
        self.repeat_records = 0
        self.errors_retryable = 0
        self.errors_other = 0
        self.refusals = 0
        self.usage_missing = 0
        self.voided = 0
        self.repeats = 0
        self.spend = Decimal(0)
        self.cost_unreadable = 0
        self.chat_records = 0
        self.chat_answers = 0
        self.length_stops = 0
        self.reasoning_bodies = 0
        self.unparsed_bodies = 0
        self.bad_records = 0
        self.skipped_before_since = 0
        self.poll_errors = 0
        self.last_error: str | None = None
        self._ids: dict[str, list[str]] = {name: [] for name in RULE_ORDER}
        self._seen_call_ids: set[str] = set()
        self._seen_hashes: set[str] = set()
        self._pending_chat: set[str] = set()
        self._chat_without_id = 0
        self._body_facts: dict[str, BodyFacts] = {}

    # -- ingestion

    def _note(self, rule: str, record_id: Any) -> None:
        ids = self._ids[rule]
        if isinstance(record_id, str) and SAFE_ID.match(record_id) and len(ids) < MAX_IDS:
            ids.append(record_id)

    def add_record(self, record: Any) -> None:
        if not isinstance(record, dict):
            self.bad_records += 1
            return
        call_id = record.get("call_id")
        ts = _parse_ts(record.get("ts"))
        if self.since is not None and ts is not None and ts < self.since:
            self.skipped_before_since += 1
            return
        if isinstance(call_id, str):
            if call_id in self._seen_call_ids:
                return
            self._seen_call_ids.add(call_id)
        self.records += 1

        status = _status(record)
        refusal = record.get("refusal")
        if refusal is not None:
            self.refusals += 1
            self._note("gateway_refusal", call_id)
        elif status is not None and status >= 400:
            if status == 429 or status >= 500:
                self.errors_retryable += 1
            else:
                self.errors_other += 1
            self._note("provider_error", call_id)
        if record.get("usage_missing") is True:
            self.usage_missing += 1
            self._note("usage_missing", call_id)
        if record.get("voided") is True:
            self.voided += 1
            self._note("voided_calls", call_id)

        if self.repeat_since is None or ts is None or ts >= self.repeat_since:    # in the repeat window
            self.repeat_records += 1
            sha = record.get("request_sha256")
            if isinstance(sha, str) and sha:
                if sha in self._seen_hashes:
                    self.repeats += 1
                    self._note("repeated_requests", call_id)
                else:
                    self._seen_hashes.add(sha)

        cost = _decimal(record.get("cost"))
        if cost is None:
            self.cost_unreadable += 1
            self._note("spend", call_id)
        else:
            self.spend += cost

        route = record.get("route")
        facts = self._body_facts.pop(call_id, None) if isinstance(call_id, str) else None
        if isinstance(route, str) and route.endswith("chat/completions"):
            self.chat_records += 1
            if facts is not None:
                self._apply_chat_body(call_id, facts)
            elif isinstance(call_id, str):
                self._pending_chat.add(call_id)
            else:
                self._chat_without_id += 1

    def add_body(self, entry: Any) -> None:
        if not isinstance(entry, dict):
            self.bad_records += 1
            return
        call_id = entry.get("call_id")
        if not isinstance(call_id, str):
            return
        facts = body_facts(entry.get("response"))
        if call_id in self._pending_chat:
            self._pending_chat.discard(call_id)
            self._apply_chat_body(call_id, facts)
        elif call_id not in self._seen_call_ids:
            self._body_facts[call_id] = facts

    def _apply_chat_body(self, call_id: Any, facts: BodyFacts) -> None:
        if facts.reasoning:
            self.reasoning_bodies += 1
            self._note("reasoning_tokens", call_id)
        if facts.kind == "answer":
            self.chat_answers += 1
            if facts.finish_reason == "length":
                self.length_stops += 1
                self._note("length_stops", call_id)
        elif facts.kind == "unparsed":
            self.unparsed_bodies += 1

    # -- evaluation

    def trips(self) -> list[Trip]:
        r = self.rules
        out: list[Trip] = []

        def add(rule: str, message: str, counts: Mapping[str, Any]) -> None:
            out.append(Trip(rule, message, dict(counts), tuple(self._ids[rule])))

        if self.errors_other > 0 or self.errors_retryable > r.tolerated_retryable:
            add("provider_error",
                f"{self.errors_other} provider error(s) that are not retryable and {self.errors_retryable} retryable "
                f"(429 or 5xx; {r.tolerated_retryable} tolerated)",
                {"errors_not_retryable": self.errors_other, "errors_retryable": self.errors_retryable,
                 "tolerated_retryable": r.tolerated_retryable})
        if self.refusals > 0:
            add("gateway_refusal", f"{self.refusals} call(s) refused by the gateway", {"refusals": self.refusals})
        if self.usage_missing > 0:
            add("usage_missing", f"{self.usage_missing} call(s) with usage missing", {"usage_missing": self.usage_missing})
        if self.reasoning_bodies > 0:
            add("reasoning_tokens", f"{self.reasoning_bodies} chat response(s) with reasoning tokens above 0",
                {"responses_with_reasoning_tokens": self.reasoning_bodies})
        if self.chat_answers >= r.min_sample and Decimal(self.length_stops) > r.length_share * self.chat_answers:
            add("length_stops",
                f"{self.length_stops} of {self.chat_answers} chat answers ended by the output limit (more than {r.length_share} allowed)",
                {"length_stops": self.length_stops, "chat_answers": self.chat_answers, "length_share": str(r.length_share)})
        if self.repeat_records >= r.min_sample and Decimal(self.repeats) > r.repeat_share * self.repeat_records:
            add("repeated_requests",
                f"{self.repeats} of {self.repeat_records} requests repeated an earlier one (more than {r.repeat_share} allowed)",
                {"repeats": self.repeats, "records": self.repeat_records, "repeat_share": str(r.repeat_share)})
        if self.voided > r.voided_max:
            add("voided_calls", f"{self.voided} voided call(s) (more than {r.voided_max} allowed)",
                {"voided": self.voided, "voided_max": r.voided_max})
        if self.cost_unreadable > 0:
            add("spend", f"{self.cost_unreadable} record(s) with a cost that cannot be read, so the spend is unknown",
                {"cost_unreadable": self.cost_unreadable, "spent_usd": str(self.spend), "stop_at_usd": str(r.stop_at_usd)})
        elif self.spend > r.stop_at_usd:
            add("spend", f"spent USD {self.spend} is above the stop at USD {r.stop_at_usd}",
                {"spent_usd": str(self.spend), "stop_at_usd": str(r.stop_at_usd), "cost_unreadable": 0})
        return out

    def counters(self) -> dict[str, Any]:
        return {
            "records": self.records, "spent_usd": str(self.spend), "errors_retryable": self.errors_retryable,
            "errors_not_retryable": self.errors_other, "refusals": self.refusals, "usage_missing": self.usage_missing,
            "voided": self.voided, "repeats": self.repeats, "repeat_records": self.repeat_records,
            "cost_unreadable": self.cost_unreadable,
            "chat_records": self.chat_records, "chat_answers": self.chat_answers, "length_stops": self.length_stops,
            "responses_with_reasoning_tokens": self.reasoning_bodies, "unparsed_bodies": self.unparsed_bodies,
            "chat_records_without_body": len(self._pending_chat) + self._chat_without_id,
            "unreadable_lines": self.bad_records, "skipped_before_since": self.skipped_before_since,
            "poll_errors": self.poll_errors, "last_error_class": self.last_error,
        }


def evaluate(records: Iterable[Any], bodies: Iterable[Any] | Mapping[str, Any], rules: Rules,
             *, since: str | datetime | None = None, repeat_since: str | datetime | None = None) -> list[Trip]:
    """The trips for a whole set of records and body-log entries, with no files or processes.

    `bodies` is a list of `{call_id, request, response}` entries (as the body log holds them, `response` raw text or already
    parsed) or a mapping call_id -> such an entry. A chat record with no body is counted as without one, not guessed at.
    """
    state = State(rules, since, repeat_since)
    body_entries = bodies.values() if isinstance(bodies, Mapping) else bodies
    # bodies first or records first gives the same counters; feeding bodies first exercises the "body arrived first" join
    for entry in body_entries:
        state.add_body(entry)
    for record in records:
        state.add_record(record)
    return state.trips()


class JsonlTail:
    """Reads the complete new lines of a growing JSONL file on each call. Missing file: nothing. A last line without its
    newline is left for the next call. A file that got shorter is read again from the start (records are de-duplicated
    by call_id in State, so this cannot double-count)."""

    def __init__(self, path: Path, *, decimal_floats: bool = False):
        self.path = Path(path)
        self.offset = 0
        self.bad_lines = 0
        self.shrank = 0
        self._parse_float = Decimal if decimal_floats else None

    def read_new(self) -> list[Any]:
        try:
            with open(self.path, "rb") as handle:
                size = os.fstat(handle.fileno()).st_size
                if size < self.offset:
                    self.offset = 0
                    self.shrank += 1
                handle.seek(self.offset)
                data = handle.read()
        except (FileNotFoundError, NotADirectoryError):
            return []
        end = data.rfind(b"\n")
        if end < 0:
            return []
        self.offset += end + 1
        out: list[Any] = []
        for line in data[:end].split(b"\n"):
            if not line.strip():
                continue
            try:
                out.append(json.loads(line.decode("utf-8", "replace"), parse_float=self._parse_float))
            except (ValueError, RecursionError):
                self.bad_lines += 1
        return out


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _write_json_atomic(path: str | Path, payload: Mapping[str, Any]) -> None:
    path = Path(path)
    tmp = path.with_name(path.name + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, indent=1, sort_keys=True) + "\n")
    os.replace(tmp, path)


def validate_pids(pids: Iterable[int]) -> list[int]:
    """Refuse pids that signal more than one process or this process: 0 and negatives address process groups or everything."""
    out: list[int] = []
    for pid in pids:
        if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 1:
            raise ValueError(f"kill pid {pid!r}: a process id above 1 is required")
        if pid == os.getpid():
            raise ValueError("kill pid: the watchdog's own pid")
        if pid not in out:
            out.append(pid)
    return out


def validate_pgids(pgids: Iterable[int]) -> list[int]:
    """Refuse process-group ids that would signal everything (0, 1, negatives) or the watchdog's own group."""
    out: list[int] = []
    for pgid in pgids:
        if isinstance(pgid, bool) or not isinstance(pgid, int) or pgid <= 1:
            raise ValueError(f"kill pgid {pgid!r}: a process-group id above 1 is required")
        if pgid == os.getpgrp():
            raise ValueError("kill pgid: the watchdog's own process group")
        if pgid not in out:
            out.append(pgid)
    return out


def _alive(pid: int) -> bool:
    """True while the process exists and is not a zombie (a child that exited and was not yet waited for still answers
    signal 0 on macOS and Linux, so its state is read with ps; macOS answers EPERM for a zombie, so that is read with ps too)."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    try:
        state = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return True
    return not state.startswith("Z")


def _group_alive(pgid: int) -> bool:
    """True while some member of the process group exists that is not a zombie (the leader, if it is our child and was not
    yet waited for, stays in the group as a zombie, and macOS answers EPERM to signal 0 for a group that holds only zombies;
    ps lists every process with its group and state)."""
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    try:
        listing = subprocess.run(["ps", "-A", "-o", "pgid=", "-o", "stat="], capture_output=True, text=True,
                                 timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return True
    rows = [line.split() for line in listing.splitlines() if len(line.split()) >= 2]
    if not rows:
        return True  # ps told us nothing: do not claim the group is gone
    return any(row[0] == str(pgid) and not row[1].startswith("Z") for row in rows)


Target = tuple[str, int]  # ("pid", n) or ("pgid", n)


def _send(target: Target, sig: int) -> None:
    kind, ident = target
    if kind == "pgid":
        os.killpg(ident, sig)
    else:
        os.kill(ident, sig)


def _target_alive(target: Target) -> bool:
    kind, ident = target
    return _group_alive(ident) if kind == "pgid" else _alive(ident)


def _terminate_targets(targets: Sequence[Target], grace_s: float, step_s: float) -> dict[Target, str]:
    """SIGTERM to every target at once, one shared grace period, then SIGKILL to what is left (a pgid target is signalled
    with killpg, so its children go with it)."""
    outcome: dict[Target, str] = {}
    for target in targets:
        try:
            _send(target, signal.SIGTERM)
            outcome[target] = "terminated"
        except ProcessLookupError:
            outcome[target] = "already_gone"
        except OSError:  # macOS answers EPERM when only zombies are left: that is gone, not refused
            outcome[target] = "signal_failed" if _target_alive(target) else "already_gone"
    waiting = [t for t in targets if outcome[t] == "terminated"]
    deadline = time.monotonic() + grace_s
    while waiting:
        waiting = [t for t in waiting if _target_alive(t)]
        if not waiting or time.monotonic() >= deadline:
            break
        time.sleep(min(step_s, max(0.0, deadline - time.monotonic())))
    for target in waiting:
        try:
            _send(target, signal.SIGKILL)
            outcome[target] = "killed"
        except ProcessLookupError:
            pass
        except OSError:
            outcome[target] = "signal_failed"
    for target in waiting:
        if outcome[target] == "killed":
            end = time.monotonic() + 2.0
            while _target_alive(target) and time.monotonic() < end:
                time.sleep(step_s)
            if _target_alive(target):
                outcome[target] = "survived"
    return outcome


def terminate_all(pids: Sequence[int] = (), pgids: Sequence[int] = (), grace_s: float = 10.0,
                  step_s: float = 0.1) -> tuple[dict[int, str], dict[int, str]]:
    """Stop process groups and single processes together, one grace period for all: SIGTERM first to every group
    (`os.killpg`: the runner and the children it started), then to every pid (the gateway), up to `grace_s` seconds for them
    to go, then SIGKILL to the groups and pids still there. Returns (outcome per pid, outcome per pgid), each one of:
    terminated, killed, already_gone, signal_failed (not permitted), survived (still there after SIGKILL)."""
    targets: list[Target] = [("pgid", g) for g in pgids] + [("pid", p) for p in pids]
    outcome = _terminate_targets(targets, grace_s, step_s)
    return ({p: outcome[("pid", p)] for p in pids}, {g: outcome[("pgid", g)] for g in pgids})


def terminate(pids: Sequence[int], grace_s: float = 10.0, step_s: float = 0.1) -> dict[int, str]:
    """SIGTERM to every pid, up to `grace_s` seconds for them to go, then SIGKILL to the survivors.
    Outcome per pid: terminated, killed, already_gone, signal_failed (not permitted), survived (still there after SIGKILL)."""
    return terminate_all(pids, (), grace_s, step_s)[0]


def terminate_groups(pgids: Sequence[int], grace_s: float = 10.0, step_s: float = 0.1) -> dict[int, str]:
    """The same for process groups, signalled with `os.killpg`. Outcome per pgid as for `terminate`."""
    return terminate_all((), pgids, grace_s, step_s)[1]


def _report(trips: Sequence[Trip], state: State, rules: Rules, kill: Mapping[str, str] | str,
            kill_groups: Mapping[str, str] | str = "no pgids given") -> dict[str, Any]:
    return {
        "tripped_at_utc": _now_utc(),
        "tripped_rules": [t.rule for t in trips],
        "trips": [t.as_dict() for t in trips],
        "counters": state.counters(),
        "rules": rules.as_dict(),
        "kill": kill,
        "kill_groups": kill_groups,
        "note": "counts and call ids only; no request or response text is kept here",
    }


def watch(gateway_dir: str | Path, rules: Rules, kill_pids: Iterable[int] = (), poll_s: float = 5.0,
          report_path: str | Path | None = None, stop_event: threading.Event | None = None, *,
          max_seconds: float | None = None, since: str | datetime | None = None, grace_s: float = 10.0,
          max_poll_errors: int = MAX_POLL_ERRORS, state: State | None = None,
          kill_pgids: Iterable[int] = (), repeat_since: str | datetime | None = None) -> list[Trip]:
    """Poll the gateway directory until a rule trips, `stop_event` is set or `max_seconds` has passed.

    On the first trip: the report is written, every process group in `kill_pgids` (a runner started in its own session
    has pgid = pid; `os.killpg` takes its children with it) and every pid in `kill_pids` (the gateway) gets SIGTERM,
    survivors get SIGKILL after `grace_s`, the report is rewritten with the outcome, and the trips are returned. A quiet end
    returns []. The first poll happens at once. It does not raise on a missing or half-written file; a pid, a pgid (at most
    1, or the watchdog's own group) or a threshold that is invalid raises ValueError before anything is read. A caller that wants the counters afterwards passes its own `state` (built with the
    same `rules`; then `since` and `repeat_since` are the state's, not these arguments').
    """
    pids = validate_pids(kill_pids)
    pgids = validate_pgids(kill_pgids)
    if poll_s <= 0:
        raise ValueError("poll_s must be positive")
    gateway_dir = Path(gateway_dir)
    state = state if state is not None else State(rules, since, repeat_since)
    meter = JsonlTail(gateway_dir / METER_NAME, decimal_floats=True)
    bodies = JsonlTail(gateway_dir / BODIES_NAME)
    stop_event = stop_event if stop_event is not None else threading.Event()
    deadline = None if max_seconds is None else time.monotonic() + max_seconds
    consecutive_errors = 0
    ending = False
    while True:
        trips: list[Trip] = []
        try:
            for entry in bodies.read_new():
                state.add_body(entry)
            for record in meter.read_new():
                state.add_record(record)
            state.bad_records += meter.bad_lines + bodies.bad_lines
            meter.bad_lines = bodies.bad_lines = 0
            consecutive_errors = 0
            trips = state.trips()
        except Exception as exc:  # noqa: BLE001 - the loop must not die; the class name is all that is kept
            consecutive_errors += 1
            state.poll_errors += 1
            state.last_error = type(exc).__name__
            if consecutive_errors >= max_poll_errors:
                trips = [Trip("watchdog_error",
                              f"the logs could not be read {consecutive_errors} polls in a row ({state.last_error})",
                              {"consecutive_poll_errors": consecutive_errors})]
        if trips:
            _stop_everything(trips, state, rules, pids, pgids, report_path, grace_s)
            return trips
        if ending or stop_event.is_set():
            return []
        wait_s = poll_s if deadline is None else min(poll_s, deadline - time.monotonic())
        if wait_s <= 0:
            return []
        if stop_event.wait(wait_s):
            ending = True


def _stop_everything(trips: Sequence[Trip], state: State, rules: Rules, pids: Sequence[int], pgids: Sequence[int],
                     report_path: str | Path | None, grace_s: float) -> None:
    def write(kill: Mapping[str, str] | str, kill_groups: Mapping[str, str] | str) -> None:
        if report_path is None:
            return
        try:
            _write_json_atomic(report_path, _report(trips, state, rules, kill, kill_groups))
        except OSError as exc:
            print(f"watchdog: the report could not be written ({type(exc).__name__})", file=sys.stderr)

    write("pending" if pids else "no pids given", "pending" if pgids else "no pgids given")
    pid_outcome, pgid_outcome = terminate_all(pids, pgids, grace_s=grace_s)
    if pids or pgids:
        write({str(pid): how for pid, how in pid_outcome.items()} if pids else "no pids given",
              {str(pgid): how for pgid, how in pgid_outcome.items()} if pgids else "no pgids given")


def _decimal_arg(text: str) -> Decimal:
    value = _decimal(text)
    if value is None or value < 0:
        raise argparse.ArgumentTypeError(f"{text!r}: a non-negative number is required")
    return value


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="passb_watchdog.py",
        description="Stop the runner and the gateway the moment a pass-B stop rule fires. Exit 3 when it tripped, 0 when "
                    "--max-seconds ran out (0 reads once), 2 on a usage error.")
    p.add_argument("--gateway-dir", required=True, help="the directory holding meter.jsonl and meter.jsonl.bodies.jsonl")
    p.add_argument("--stop-at-usd", required=True, type=_decimal_arg, help="the stage's 'stop at', in USD")
    p.add_argument("--kill-pid", action="extend", nargs="+", type=int, default=[], metavar="PID",
                   help="SIGTERM these pids on a trip, SIGKILL after 10 s (the gateway)")
    p.add_argument("--kill-pgid", action="extend", nargs="+", type=int, default=[], metavar="PGID",
                   help="SIGTERM these whole process groups (os.killpg) on a trip, SIGKILL after 10 s: a runner started in "
                        "its own session has pgid = pid, and its children go with it; at most 1 and the watchdog's own "
                        "group are refused")
    p.add_argument("--report", help="where to write the JSON report on a trip (counts and call ids only)")
    p.add_argument("--poll-s", type=float, default=5.0)
    p.add_argument("--max-seconds", type=float, help="stop watching after this long, quietly; 0 reads the logs once")
    p.add_argument("--length-share", type=_decimal_arg, default=Decimal("0.05"))
    p.add_argument("--repeat-share", type=_decimal_arg, default=Decimal("0.05"))
    p.add_argument("--voided-max", type=int, default=3)
    p.add_argument("--min-sample", type=int, default=20)
    p.add_argument("--tolerated-retryable", type=int, default=1)
    p.add_argument("--since", help="ignore records stamped before this UTC time (ISO, e.g. 2026-11-02T21:00:00Z): "
                                   "the ledger is shared by all stages, a stage counts only its own calls")
    p.add_argument("--from-now", action="store_true", help="same as --since with the current time")
    p.add_argument("--repeat-since", help="the repeat rule remembers requests only from this UTC time on (ISO): a stage run a "
                                          "second time on the same documents repeats the first run's requests, which is not a "
                                          "retry loop; every other rule still counts all calls since --since")
    return p


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not Path(args.gateway_dir).is_dir():
        parser.error(f"--gateway-dir {args.gateway_dir!r} is not a directory (a typo would leave the stage unguarded)")
    if args.poll_s <= 0:
        parser.error("--poll-s must be positive")
    if args.max_seconds is not None and args.max_seconds < 0:
        parser.error("--max-seconds must not be negative")
    if args.since and args.from_now:
        parser.error("give --since or --from-now, not both")
    since = _now_utc() if args.from_now else args.since
    try:
        rules = Rules(args.stop_at_usd, args.length_share, args.repeat_share, args.voided_max, args.min_sample,
                      args.tolerated_retryable)
        State(rules, since, args.repeat_since)
        pids = validate_pids(args.kill_pid)
        pgids = validate_pgids(args.kill_pgid)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"watchdog: watching the gateway directory, stop at USD {rules.stop_at_usd}, "
          f"kill pids {pids or 'none'}, kill process groups {pgids or 'none'}, polling every {args.poll_s} s"
          + (f", only calls since {since}" if since else "")
          + (f", repeats looked for since {args.repeat_since}" if args.repeat_since else ""), flush=True)
    state = State(rules, since, args.repeat_since)
    try:
        trips = watch(args.gateway_dir, rules, pids, args.poll_s, args.report, max_seconds=args.max_seconds, state=state,
                      kill_pgids=pgids)
    except KeyboardInterrupt:
        print("watchdog: interrupted, nothing tripped", file=sys.stderr)
        return 0
    finally:
        c = state.counters()
        print(f"watchdog: read {c['records']} call(s), spent USD {c['spent_usd']}, {c['chat_answers']} chat answer(s) "
              f"checked, {c['unparsed_bodies']} body(ies) not JSON, {c['unreadable_lines']} unreadable line(s)", flush=True)
        if c["chat_records_without_body"]:
            print(f"watchdog: WARNING {c['chat_records_without_body']} chat call(s) have no body in the body log, so the "
                  "reasoning-token and length-stop rules could not check them (is log_bodies on?)", file=sys.stderr, flush=True)
    for trip in trips:
        print(f"watchdog: TRIPPED {trip.rule}: {trip.message}", file=sys.stderr)
    return EXIT_TRIPPED if trips else 0


if __name__ == "__main__":
    sys.exit(main())
