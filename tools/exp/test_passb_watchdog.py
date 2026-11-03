"""Tests for tools/exp/passb_watchdog.py. Standard library only; no network, no model, no key.

The gateway directory is a fake one written by the tests (records and body-log entries in the gateway's formats); the
processes the watchdog stops are real `sleep` and Python children.

Run from the repository root:

    uv run python -m unittest tools/exp/test_passb_watchdog.py
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from decimal import Decimal
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import passb_watchdog as wd  # noqa: E402

SCRIPT = HERE / "passb_watchdog.py"
SENTINEL = "ZEBRA-QUILL-7731-distinctive-body-text"
BIG = Decimal("1000")
CHAT = "/v1/chat/completions"
EMBED = "/v1/embeddings"


def rules(**kw) -> wd.Rules:
    return wd.Rules(**{"stop_at_usd": BIG, **kw})


def rec(i: int, **kw) -> dict:
    """A gateway record (tools/metering_gateway.md, "The log") for a clean chat call; keyword arguments override fields."""
    base = {
        "ts": "2026-11-02T21:00:00.000Z", "call_id": f"call{i:04d}", "route": CHAT, "upstream": "openai-main",
        "model_requested": "m", "model_reported": "m", "http_status": 200, "input_tokens": 10, "output_tokens": 5,
        "cached_input_tokens": None, "cost": "0.001", "currency": "USD", "reserve": "0.002", "voided": False,
        "usage_missing": False, "streamed": False, "latency_ms": 5, "request_sha256": f"sha{i:04d}", "bytes_in": 10,
        "bytes_out": 10, "refusal": None, "error": None, "reserve_exceeded": False,
        "cache_creation_input_tokens": None, "request_defaults_applied": [],
    }
    base.update(kw)
    return base


def chat_body(i: int, finish: str = "stop", reasoning=None, text: str = "hello", with_details: bool = True) -> dict:
    usage: dict = {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
    if with_details:
        usage["completion_tokens_details"] = {"reasoning_tokens": reasoning}
    answer = {"id": f"chatcmpl-{i}", "object": "chat.completion", "model": "m", "usage": usage,
              "choices": [{"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": finish}]}
    return {"call_id": f"call{i:04d}", "request": json.dumps({"messages": [{"role": "user", "content": text}]}),
            "response": json.dumps(answer)}


def names(trips) -> list[str]:
    return [t.rule for t in trips]


class GatewayDir:
    """A fake gateway directory: appends to meter.jsonl and its body log the way the gateway does (one line per write)."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

    def raw(self, name: str, data: bytes) -> None:
        with open(self.path / name, "ab") as handle:
            handle.write(data)
            handle.flush()

    def record(self, record: dict) -> None:
        self.raw(wd.METER_NAME, json.dumps(record, separators=(",", ":")).encode() + b"\n")

    def body(self, entry: dict) -> None:
        self.raw(wd.BODIES_NAME, json.dumps(entry, separators=(",", ":")).encode() + b"\n")


class TmpDirCase(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.gw = GatewayDir(self.tmp / "gateway")

    def spawn(self, *argv: str, **kw) -> subprocess.Popen:
        proc = subprocess.Popen(list(argv), env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, **kw)

        def reap() -> None:
            if proc.poll() is None:
                proc.kill()
            proc.wait()
            if proc.stdout:
                proc.stdout.close()

        self.addCleanup(reap)
        return proc

    def spawn_group(self, ignore_sigterm: bool = False) -> tuple[subprocess.Popen, int]:
        """A runner in a session of its own (its process-group id is its pid) that has started a `sleep` child.
        Returns (the runner, the child's pid). With `ignore_sigterm` both ignore SIGTERM (the disposition is inherited)."""
        code = ("import signal, subprocess, time\n"
                + ("signal.signal(signal.SIGTERM, signal.SIG_IGN)\n" if ignore_sigterm else "")
                + "child = subprocess.Popen(['sleep', '60'])\nprint(child.pid, flush=True)\ntime.sleep(60)\n")
        leader = self.spawn(sys.executable, "-c", code, stdout=subprocess.PIPE, text=True, start_new_session=True)

        def kill_group() -> None:
            try:
                os.killpg(leader.pid, signal.SIGKILL)
            except OSError:
                pass

        self.addCleanup(kill_group)
        return leader, int(leader.stdout.readline())

    def assert_gone(self, pid: int, within_s: float = 3.0) -> None:
        end = time.monotonic() + within_s
        while wd._alive(pid) and time.monotonic() < end:
            time.sleep(0.05)
        self.assertFalse(wd._alive(pid), f"process {pid} is still there")


class ProviderErrorRule(unittest.TestCase):
    def test_one_retryable_error_is_tolerated_and_a_second_trips(self):
        for status in (429, 500, 502, 503, 599):
            with self.subTest(status=status):
                one = [rec(1, http_status=status, voided=True)]
                self.assertEqual(wd.evaluate(one, [], rules()), [])
                two = one + [rec(2, http_status=status, voided=True)]
                trips = wd.evaluate(two, [], rules())
                self.assertEqual(names(trips), ["provider_error"])
                self.assertEqual(trips[0].counts["errors_retryable"], 2)
                self.assertEqual(trips[0].counts["errors_not_retryable"], 0)
                self.assertEqual(trips[0].call_ids, ("call0001", "call0002"))

    def test_a_429_and_a_500_together_are_two_retryable_errors(self):
        trips = wd.evaluate([rec(1, http_status=429, voided=True), rec(2, http_status=500, voided=True)], [], rules())
        self.assertEqual(names(trips), ["provider_error"])

    def test_any_other_4xx_trips_at_once(self):
        for status in (400, 401, 403, 404, 408, 422, 499):
            with self.subTest(status=status):
                trips = wd.evaluate([rec(1, http_status=status, voided=True)], [], rules())
                self.assertEqual(names(trips), ["provider_error"])
                self.assertEqual(trips[0].counts["errors_not_retryable"], 1)

    def test_the_tolerated_count_is_a_parameter(self):
        zero = rules(tolerated_retryable=0)
        self.assertEqual(names(wd.evaluate([rec(1, http_status=429, voided=True)], [], zero)), ["provider_error"])
        two = rules(tolerated_retryable=2)
        calls = [rec(i, http_status=503, voided=True) for i in (1, 2)]
        self.assertEqual(wd.evaluate(calls, [], two), [])
        self.assertEqual(names(wd.evaluate(calls + [rec(3, http_status=503, voided=True)], [], two)), ["provider_error"])

    def test_success_and_redirect_statuses_are_not_errors(self):
        for status in (200, 204, 301):
            self.assertEqual(wd.evaluate([rec(1, http_status=status)], [], rules()), [])

    def test_a_gateway_refusal_is_not_a_provider_error(self):
        trips = wd.evaluate([rec(1, http_status=429, refusal="gateway_budget_exceeded")], [], rules())
        self.assertEqual(names(trips), ["gateway_refusal"])
        trips = wd.evaluate([rec(1, http_status=400, refusal="gateway_model_not_priced")], [], rules())
        self.assertEqual(names(trips), ["gateway_refusal"])


class SimpleRules(unittest.TestCase):
    def test_gateway_refusal_trips_on_one(self):
        self.assertEqual(wd.evaluate([rec(1, refusal=None)], [], rules()), [])
        trips = wd.evaluate([rec(1), rec(2, http_status=429, refusal="gateway_budget_exceeded")], [], rules())
        self.assertEqual(names(trips), ["gateway_refusal"])
        self.assertEqual(trips[0].counts["refusals"], 1)
        self.assertEqual(trips[0].call_ids, ("call0002",))

    def test_usage_missing_trips_on_one(self):
        self.assertEqual(wd.evaluate([rec(1, usage_missing=False)], [], rules()), [])
        trips = wd.evaluate([rec(1), rec(2, usage_missing=True)], [], rules())
        self.assertEqual(names(trips), ["usage_missing"])
        self.assertEqual(trips[0].counts["usage_missing"], 1)

    def test_voided_calls_trip_above_the_maximum(self):
        three = [rec(i, voided=True) for i in range(3)]
        self.assertEqual(wd.evaluate(three, [], rules()), [])
        trips = wd.evaluate(three + [rec(9, voided=True)], [], rules())
        self.assertEqual(names(trips), ["voided_calls"])
        self.assertEqual(trips[0].counts["voided"], 4)
        self.assertEqual(names(wd.evaluate(three[:1], [], rules(voided_max=0))), ["voided_calls"])
        self.assertEqual(wd.evaluate([], [], rules(voided_max=0)), [])

    def test_spend_trips_only_above_the_stop_at(self):
        r = rules(stop_at_usd=Decimal("0.09"))
        calls = [rec(i, cost="0.03") for i in range(3)]
        self.assertEqual(wd.evaluate(calls, [], r), [])  # exactly at the stop at
        trips = wd.evaluate(calls + [rec(9, cost="0.0000001")], [], r)
        self.assertEqual(names(trips), ["spend"])
        self.assertEqual(trips[0].counts["spent_usd"], "0.0900001")
        self.assertEqual(trips[0].counts["stop_at_usd"], "0.09")

    def test_spend_is_summed_as_decimal_not_float(self):
        r = rules(stop_at_usd=Decimal("0.3"))
        self.assertEqual(wd.evaluate([rec(1, cost="0.1"), rec(2, cost="0.2")], [], r), [])
        self.assertEqual(wd.evaluate([rec(i, cost="0.1") for i in range(3)], [], r), [])

    def test_a_cost_that_cannot_be_read_trips_spend(self):
        for bad in (None, "abc", "NaN", "Infinity", True, [1]):
            with self.subTest(cost=bad):
                trips = wd.evaluate([rec(1, cost=bad)], [], rules())
                self.assertEqual(names(trips), ["spend"])
                self.assertEqual(trips[0].counts["cost_unreadable"], 1)
        record = rec(1)
        del record["cost"]
        self.assertEqual(names(wd.evaluate([record], [], rules())), ["spend"])

    def test_several_trips_come_in_rule_order(self):
        calls = [rec(1, http_status=400, voided=True), rec(2, usage_missing=True), rec(3, refusal="gateway_bad_request"),
                 rec(4, cost="5"), rec(5, voided=True), rec(6, voided=True), rec(7, voided=True)]
        trips = wd.evaluate(calls, [], rules(stop_at_usd=Decimal("1")))
        self.assertEqual(names(trips), ["provider_error", "gateway_refusal", "usage_missing", "voided_calls", "spend"])
        self.assertEqual(names(trips), sorted(names(trips), key=wd.RULE_ORDER.index))


class ReasoningRule(unittest.TestCase):
    def test_reasoning_tokens_above_zero_trip(self):
        calls = [rec(1)]
        self.assertEqual(wd.evaluate(calls, [chat_body(1, reasoning=0)], rules()), [])
        self.assertEqual(wd.evaluate(calls, [chat_body(1, reasoning=None)], rules()), [])
        self.assertEqual(wd.evaluate(calls, [chat_body(1, with_details=False)], rules()), [])
        trips = wd.evaluate(calls, [chat_body(1, reasoning=1)], rules())
        self.assertEqual(names(trips), ["reasoning_tokens"])
        self.assertEqual(trips[0].counts["responses_with_reasoning_tokens"], 1)
        self.assertEqual(trips[0].call_ids, ("call0001",))

    def test_a_json_body_without_choices_is_still_read_for_reasoning(self):
        body = {"call_id": "call0001", "request": "{}",
                "response": json.dumps({"usage": {"completion_tokens_details": {"reasoning_tokens": 4}}})}
        self.assertEqual(names(wd.evaluate([rec(1)], [body], rules())), ["reasoning_tokens"])

    def test_a_numeric_string_count_is_read_too(self):
        self.assertEqual(names(wd.evaluate([rec(1)], [chat_body(1, reasoning="3")], rules())), ["reasoning_tokens"])
        self.assertEqual(wd.evaluate([rec(1)], [chat_body(1, reasoning="zero")], rules()), [])

    def test_an_embeddings_body_is_not_a_chat_response(self):
        body = chat_body(1, reasoning=9)
        self.assertEqual(wd.evaluate([rec(1, route=EMBED)], [body], rules()), [])

    def test_bodies_may_arrive_before_or_after_their_records(self):
        record, body = rec(1), chat_body(1, reasoning=2)
        for order in ("record first", "body first"):
            with self.subTest(order):
                state = wd.State(rules())
                if order == "record first":
                    state.add_record(record)
                    self.assertEqual(state.trips(), [])
                    self.assertEqual(state.counters()["chat_records_without_body"], 1)
                    state.add_body(body)
                else:
                    state.add_body(body)
                    state.add_record(record)
                self.assertEqual(names(state.trips()), ["reasoning_tokens"])
                self.assertEqual(state.counters()["chat_records_without_body"], 0)

    def test_the_body_of_a_call_is_counted_once(self):
        state = wd.State(rules())
        state.add_record(rec(1))
        state.add_body(chat_body(1, finish="length"))
        state.add_body(chat_body(1, finish="length"))
        state.add_record(rec(1))
        self.assertEqual((state.records, state.chat_answers, state.length_stops), (1, 1, 1))


def answered(n: int, length: int, **kw) -> tuple[list[dict], list[dict]]:
    """n clean chat calls with their bodies, the first `length` of them ended by the output limit."""
    calls = [rec(i, **kw) for i in range(n)]
    bodies = [chat_body(i, "length" if i < length else "stop") for i in range(n)]
    return calls, bodies


class LengthStopRule(unittest.TestCase):
    def test_trips_when_the_share_passes_five_percent(self):
        for n, length, expected in ((20, 1, []), (20, 2, ["length_stops"]), (40, 2, []), (40, 3, ["length_stops"]),
                                    (100, 5, []), (100, 6, ["length_stops"])):
            with self.subTest(answers=n, length_stops=length):
                calls, bodies = answered(n, length)
                self.assertEqual(names(wd.evaluate(calls, bodies, rules())), expected)

    def test_the_counts_are_in_the_trip(self):
        calls, bodies = answered(20, 3)
        trip = wd.evaluate(calls, bodies, rules())[0]
        self.assertEqual((trip.counts["length_stops"], trip.counts["chat_answers"]), (3, 20))
        self.assertEqual(trip.call_ids, ("call0000", "call0001", "call0002"))

    def test_nothing_is_evaluated_below_min_sample(self):
        calls, bodies = answered(19, 19)
        self.assertEqual(wd.evaluate(calls, bodies, rules()), [])
        calls, bodies = answered(20, 20)
        self.assertEqual(names(wd.evaluate(calls, bodies, rules())), ["length_stops"])
        calls, bodies = answered(4, 4)
        self.assertEqual(wd.evaluate(calls, bodies, rules(min_sample=5)), [])
        calls, bodies = answered(5, 1)
        self.assertEqual(names(wd.evaluate(calls, bodies, rules(min_sample=5))), ["length_stops"])

    def test_the_share_is_a_parameter(self):
        r = rules(length_share=0.5)
        self.assertEqual(wd.evaluate(*answered(20, 10), r), [])
        self.assertEqual(names(wd.evaluate(*answered(20, 11), r)), ["length_stops"])

    def test_only_chat_answers_count(self):
        calls, bodies = answered(19, 0)
        calls.append(rec(50))
        bodies.append({"call_id": "call0050", "request": "{}", "response": json.dumps({"id": "no choices here"})})
        calls += [rec(60 + i, route=EMBED) for i in range(30)]
        bodies += [{"call_id": f"call{60 + i:04d}", "request": "{}", "response": json.dumps({"choices": [{"finish_reason": "length"}]})}
                   for i in range(30)]
        state = wd.State(rules())
        for b in bodies:
            state.add_body(b)
        for c in calls:
            state.add_record(c)
        self.assertEqual(state.chat_answers, 19)
        self.assertEqual(state.trips(), [])


class RepeatRule(unittest.TestCase):
    def test_trips_when_the_share_passes_five_percent(self):
        calls = [rec(i) for i in range(20)]
        calls[19]["request_sha256"] = calls[0]["request_sha256"]
        self.assertEqual(wd.evaluate(calls, [], rules()), [])  # 1 of 20 is exactly 5%
        calls[18]["request_sha256"] = calls[1]["request_sha256"]
        trips = wd.evaluate(calls, [], rules())
        self.assertEqual(names(trips), ["repeated_requests"])
        self.assertEqual((trips[0].counts["repeats"], trips[0].counts["records"]), (2, 20))
        self.assertEqual(trips[0].call_ids, ("call0018", "call0019"))

    def test_a_third_copy_is_a_second_repeat(self):
        calls = [rec(i, request_sha256="same") for i in range(3)]
        self.assertEqual(wd.State(rules()).counters()["records"], 0)
        state = wd.State(rules(min_sample=1))
        for c in calls:
            state.add_record(c)
        self.assertEqual(state.repeats, 2)

    def test_nothing_is_evaluated_below_min_sample(self):
        self.assertEqual(wd.evaluate([rec(i, request_sha256="same") for i in range(19)], [], rules()), [])
        self.assertEqual(names(wd.evaluate([rec(i, request_sha256="same") for i in range(20)], [], rules())),
                         ["repeated_requests"])
        self.assertEqual(names(wd.evaluate([rec(i, request_sha256="same") for i in range(5)], [], rules(min_sample=5))),
                         ["repeated_requests"])

    def test_records_without_a_hash_are_never_repeats(self):
        self.assertEqual(wd.evaluate([rec(i, request_sha256=None) for i in range(30)], [], rules()), [])

    def test_the_share_is_a_parameter(self):
        calls = [rec(i) for i in range(20)]
        for i in range(10, 20):
            calls[i]["request_sha256"] = calls[i - 10]["request_sha256"]
        self.assertEqual(wd.evaluate(calls, [], rules(repeat_share=0.5)), [])
        calls.append(rec(20, request_sha256=calls[0]["request_sha256"]))  # 11 repeats of 21 records
        self.assertEqual(names(wd.evaluate(calls, [], rules(repeat_share=0.5))), ["repeated_requests"])


class BodyHandling(unittest.TestCase):
    def test_a_stream_is_counted_as_unparsed_and_not_guessed_at(self):
        stream = 'data: {"choices":[{"delta":{"content":"hi"},"finish_reason":"length"}]}\n\ndata: [DONE]\n'
        bodies = [{"call_id": f"call{i:04d}", "request": "{}", "response": stream} for i in range(25)]
        state = wd.State(rules())
        for b in bodies:
            state.add_body(b)
        for i in range(25):
            state.add_record(rec(i, streamed=True))
        self.assertEqual(state.trips(), [])
        counters = state.counters()
        self.assertEqual((counters["unparsed_bodies"], counters["chat_answers"], counters["length_stops"]), (25, 0, 0))

    def test_other_unreadable_bodies_are_unparsed(self):
        for response in ('{"choices": [{"finish_reason": "len', "[1, 2]", '"text"', "", None, 7):
            with self.subTest(response=response):
                state = wd.State(rules())
                state.add_record(rec(1))
                state.add_body({"call_id": "call0001", "request": "{}", "response": response})
                self.assertEqual(state.counters()["unparsed_bodies"], 1)
                self.assertEqual(state.trips(), [])

    def test_chat_records_without_any_body_are_counted(self):
        state = wd.State(rules())
        for i in range(3):
            state.add_record(rec(i))
        state.add_record(rec(9, route=EMBED))
        self.assertEqual(state.counters()["chat_records_without_body"], 3)

    def test_bodies_may_be_a_mapping_or_already_parsed(self):
        body = chat_body(1, reasoning=1)
        as_mapping = {"call0001": body}
        self.assertEqual(names(wd.evaluate([rec(1)], as_mapping, rules())), ["reasoning_tokens"])
        parsed = {**body, "response": json.loads(body["response"])}
        self.assertEqual(names(wd.evaluate([rec(1)], [parsed], rules())), ["reasoning_tokens"])

    def test_junk_entries_do_not_raise(self):
        state = wd.State(rules())
        for junk in (None, 3, "x", [], {}, {"call_id": 5}):
            state.add_record(junk)
            state.add_body(junk)
        self.assertEqual(state.records, 2)  # the two dicts are records with nothing to say, and with no readable cost
        self.assertEqual(state.counters()["unreadable_lines"], 8)  # the four non-objects, each as a record and as a body
        self.assertEqual(names(state.trips()), ["spend"])


class StatusHandling(unittest.TestCase):
    def test_a_status_that_is_not_an_integer_is_not_an_error_and_does_not_raise(self):
        for status in ("500", 500.0, None, True, [500]):
            with self.subTest(status=status):
                self.assertEqual(wd.evaluate([rec(1, http_status=status)], [], rules()), [])


class SinceFilter(unittest.TestCase):
    def test_records_before_since_are_ignored_with_their_bodies(self):
        old = rec(1, ts="2026-11-02T20:59:59.999Z", cost="50", refusal="gateway_budget_exceeded", voided=True)
        old_body = chat_body(1, reasoning=5)
        new = rec(2, ts="2026-11-02T21:00:00.000Z", cost="0.01")
        state = wd.State(rules(stop_at_usd=Decimal("1")), since="2026-11-02T21:00:00Z")
        state.add_record(old)
        state.add_body(old_body)
        state.add_record(new)
        state.add_body(chat_body(2))
        self.assertEqual(state.trips(), [])
        self.assertEqual((state.records, state.skipped_before_since, state.spend), (1, 1, Decimal("0.01")))
        self.assertEqual(state.counters()["chat_records_without_body"], 0)

    def test_a_record_without_a_readable_time_is_not_ignored(self):
        for ts in (None, "yesterday", 5):
            state = wd.State(rules(), since="2026-11-02T21:00:00Z")
            state.add_record(rec(1, ts=ts, refusal="gateway_bad_request"))
            self.assertEqual(names(state.trips()), ["gateway_refusal"])

    def test_evaluate_takes_since_and_a_bad_since_is_refused(self):
        calls = [rec(1, ts="2026-11-01T00:00:00.000Z", usage_missing=True)]
        self.assertEqual(wd.evaluate(calls, [], rules(), since="2026-11-02T00:00:00Z"), [])
        self.assertEqual(names(wd.evaluate(calls, [], rules())), ["usage_missing"])
        with self.assertRaises(ValueError):
            wd.State(rules(), since="not a time")


class RepeatWindow(unittest.TestCase):
    """`repeat_since`: stage C's second run sends the first run's requests again, which is not a retry loop. The dress
    rehearsal with the real LightRAG and the real driver found it stopped within a second."""
    OLD, NEW, BOUND = "2026-11-02T21:00:00.000Z", "2026-11-02T22:00:00.000Z", "2026-11-02T21:30:00Z"

    def two_runs(self):
        first = [rec(i, ts=self.OLD) for i in range(25)]
        second = [rec(100 + i, ts=self.NEW, request_sha256=first[i]["request_sha256"]) for i in range(25)]
        return first, second

    def test_a_second_run_that_repeats_the_first_is_not_a_retry_loop_but_the_rule_would_have_fired_without_the_window(self):
        first, second = self.two_runs()
        self.assertEqual(names(wd.evaluate(first + second, [], rules())), ["repeated_requests"])
        self.assertEqual(wd.evaluate(first + second, [], rules(), repeat_since=self.BOUND), [])

    def test_a_repeat_inside_the_window_still_trips_and_the_share_is_of_the_windows_records(self):
        first, second = self.two_runs()
        for i in range(1, 7):                                          # 6 of the second run's 25 repeat its own first request
            second[i]["request_sha256"] = second[0]["request_sha256"]
        trips = wd.evaluate(first + second, [], rules(), repeat_since=self.BOUND)
        self.assertEqual(names(trips), ["repeated_requests"])
        self.assertEqual((trips[0].counts["repeats"], trips[0].counts["records"]), (6, 25))
        second[6]["request_sha256"] = "sha-unique"                      # 5 of 25 is exactly 20%: still above 5%
        self.assertEqual(names(wd.evaluate(first + second, [], rules(), repeat_since=self.BOUND)), ["repeated_requests"])
        for i in range(1, 5):
            second[i]["request_sha256"] = f"sha-unique-{i}"
        self.assertEqual(wd.evaluate(first + second, [], rules(), repeat_since=self.BOUND), [])      # 1 of 25 is 4%

    def test_the_share_and_the_minimum_sample_are_of_the_windows_records_not_the_stages(self):
        old = [rec(i, ts=self.OLD) for i in range(30)]
        window = [rec(100 + i, ts=self.NEW) for i in range(25)]
        window[1]["request_sha256"] = window[2]["request_sha256"] = window[0]["request_sha256"]
        # 2 repeats of 25 in the window is 8%, though only 2 of the stage's 55 records (3.6%)
        self.assertEqual(names(wd.evaluate(old + window, [], rules(), repeat_since=self.BOUND)), ["repeated_requests"])
        # a window of 10 records is below the minimum sample of 20, though the stage holds 40
        few = [rec(200 + i, ts=self.NEW, request_sha256="same") for i in range(10)]
        self.assertEqual(wd.evaluate(old + few, [], rules(), repeat_since=self.BOUND), [])

    def test_every_other_rule_still_counts_the_whole_stage_window(self):
        first, second = self.two_runs()
        for c in first[:4]:
            c["voided"] = True
        state = wd.State(rules(stop_at_usd=Decimal("0.04")), repeat_since=self.BOUND)
        for c in first + second:
            state.add_record(c)
        counters = state.counters()
        self.assertEqual((counters["records"], counters["repeat_records"], counters["repeats"]), (50, 25, 0))
        self.assertEqual(counters["spent_usd"], "0.050")
        self.assertEqual(names(state.trips()), ["voided_calls", "spend"])

    def test_the_boundary_is_inclusive_and_a_hash_from_before_it_is_not_remembered(self):
        state = wd.State(rules(min_sample=1), repeat_since="2026-11-02T21:30:00.000Z")
        state.add_record(rec(1, ts="2026-11-02T21:29:59.999Z", request_sha256="x"))
        state.add_record(rec(2, ts="2026-11-02T21:30:00.000Z", request_sha256="x"))
        self.assertEqual((state.repeats, state.repeat_records), (0, 1))
        state.add_record(rec(3, ts="2026-11-02T21:30:00.000Z", request_sha256="x"))
        self.assertEqual((state.repeats, state.repeat_records), (1, 2))

    def test_a_record_without_a_readable_time_is_inside_the_window(self):
        for ts in (None, "yesterday", 5):
            with self.subTest(ts=ts):
                state = wd.State(rules(min_sample=1), repeat_since=self.BOUND)
                state.add_record(rec(1, ts=ts, request_sha256="x"))
                state.add_record(rec(2, ts=ts, request_sha256="x"))
                self.assertEqual((state.repeats, state.repeat_records), (1, 2))

    def test_without_a_window_every_record_is_in_it_and_a_bad_window_is_refused(self):
        state = wd.State(rules())
        for c in (rec(1), rec(2, request_sha256=None)):
            state.add_record(c)
        self.assertEqual((state.records, state.repeat_records), (2, 2))
        with self.assertRaises(ValueError):
            wd.State(rules(), repeat_since="not a time")
        self.assertEqual(wd.State(rules(), repeat_since=wd._parse_ts(self.BOUND)).repeat_since, wd._parse_ts(self.BOUND))

    def test_the_window_is_independent_of_since(self):
        first, second = self.two_runs()
        state = wd.State(rules(), since="2026-11-02T20:00:00Z", repeat_since=self.BOUND)
        for c in first + second:
            state.add_record(c)
        self.assertEqual((state.records, state.repeat_records, state.skipped_before_since), (50, 25, 0))
        state = wd.State(rules(), since=self.BOUND, repeat_since=self.BOUND)
        for c in first + second:
            state.add_record(c)
        self.assertEqual((state.records, state.repeat_records, state.skipped_before_since), (25, 25, 25))


class ReaderTests(TmpDirCase):
    def test_a_missing_file_reads_as_nothing(self):
        tail = wd.JsonlTail(self.tmp / "nope" / "meter.jsonl")
        self.assertEqual(tail.read_new(), [])
        (self.tmp / "afile").write_text("x")
        self.assertEqual(wd.JsonlTail(self.tmp / "afile" / "meter.jsonl").read_new(), [])

    def test_a_partial_last_line_waits_until_it_is_complete(self):
        tail = wd.JsonlTail(self.gw.path / "meter.jsonl")
        one = json.dumps({"a": 1}).encode() + b"\n"
        two = json.dumps({"b": "caf\u00e9"}, ensure_ascii=False).encode() + b"\n"
        cut = two.index("\u00e9".encode()) + 1  # inside the two bytes of the accented letter
        self.gw.raw("meter.jsonl", one + two[:cut])
        self.assertEqual(tail.read_new(), [{"a": 1}])
        self.assertEqual(tail.offset, len(one))
        self.assertEqual(tail.read_new(), [])
        self.gw.raw("meter.jsonl", two[cut:])
        self.assertEqual(tail.read_new(), [{"b": "caf\u00e9"}])
        self.assertEqual(tail.read_new(), [])
        self.assertEqual(tail.bad_lines, 0)

    def test_a_complete_line_that_is_not_json_is_counted_and_skipped(self):
        tail = wd.JsonlTail(self.gw.path / "meter.jsonl")
        self.gw.raw("meter.jsonl", b'{"a": 1}\nthis is not json\n\n{"b": 2}\n')
        self.assertEqual(tail.read_new(), [{"a": 1}, {"b": 2}])
        self.assertEqual(tail.bad_lines, 1)

    def test_a_shorter_file_is_read_again_without_double_counting(self):
        path = self.gw.path / "meter.jsonl"
        state = wd.State(rules())
        tail = wd.JsonlTail(path)
        self.gw.record(rec(1))
        self.gw.record(rec(2))
        for r in tail.read_new():
            state.add_record(r)
        path.write_bytes(json.dumps(rec(1)).encode() + b"\n")
        for r in tail.read_new():
            state.add_record(r)
        self.assertEqual((tail.shrank, state.records), (1, 2))

    def test_money_in_a_json_number_is_read_exactly(self):
        tail = wd.JsonlTail(self.gw.path / "meter.jsonl", decimal_floats=True)
        self.gw.raw("meter.jsonl", b'{"cost": 0.1}\n')
        self.assertEqual(tail.read_new()[0]["cost"], Decimal("0.1"))


class LoopTests(TmpDirCase):
    def run_watch(self, *args, **kw) -> tuple[threading.Thread, dict]:
        out: dict = {}

        def target() -> None:
            out["trips"] = wd.watch(*args, **kw)
            out["done_at"] = time.monotonic()

        thread = threading.Thread(target=target, daemon=True)
        thread.start()
        return thread, out

    def test_a_bad_record_trips_it_within_one_poll(self):
        poll = 0.3
        thread, out = self.run_watch(self.gw.path, rules(), poll_s=poll, max_seconds=30)
        time.sleep(0.5)
        self.assertTrue(thread.is_alive())
        self.gw.record(rec(1))
        time.sleep(0.4)
        self.assertTrue(thread.is_alive())
        appended_at = time.monotonic()
        self.gw.record(rec(2, http_status=429, refusal="gateway_budget_exceeded"))
        thread.join(timeout=5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(names(out["trips"]), ["gateway_refusal"])
        self.assertLess(out["done_at"] - appended_at, poll + 1.0)

    def test_records_appended_in_pieces_are_read_when_complete(self):
        thread, out = self.run_watch(self.gw.path, rules(), poll_s=0.1, max_seconds=30)
        for i in range(3):
            self.gw.record(rec(i, voided=True))
        line = json.dumps(rec(3, voided=True), separators=(",", ":")).encode() + b"\n"
        self.gw.raw(wd.METER_NAME, line[:40])
        time.sleep(0.5)
        self.assertTrue(thread.is_alive(), "three voided calls and half a line must not trip")
        self.gw.raw(wd.METER_NAME, line[40:])
        thread.join(timeout=5)
        self.assertEqual(names(out["trips"]), ["voided_calls"])

    def test_a_body_that_lands_after_its_record_is_still_checked(self):
        thread, out = self.run_watch(self.gw.path, rules(), poll_s=0.1, max_seconds=30)
        self.gw.record(rec(1))
        time.sleep(0.4)
        self.assertTrue(thread.is_alive())
        self.gw.body(chat_body(1, reasoning=3))
        thread.join(timeout=5)
        self.assertEqual(names(out["trips"]), ["reasoning_tokens"])

    def test_a_stage_with_a_shared_ledger_counts_only_its_own_calls(self):
        for i in range(10):
            self.gw.record(rec(i, ts="2026-11-02T19:00:00.000Z", cost="1", voided=True))
        trips = wd.watch(self.gw.path, rules(stop_at_usd=Decimal("0.5")), poll_s=0.1, max_seconds=0,
                         since="2026-11-02T20:00:00Z")
        self.assertEqual(trips, [])
        self.assertEqual(names(wd.watch(self.gw.path, rules(stop_at_usd=Decimal("0.5")), poll_s=0.1, max_seconds=0)),
                         ["voided_calls", "spend"])

    def test_json_number_costs_are_summed_exactly_from_the_file(self):
        self.gw.raw(wd.METER_NAME, json.dumps(rec(1, cost=0.1)).encode() + b"\n")
        self.gw.raw(wd.METER_NAME, json.dumps(rec(2, cost=0.2)).encode() + b"\n")
        self.assertEqual(wd.watch(self.gw.path, rules(stop_at_usd=Decimal("0.3")), max_seconds=0), [])

    def test_a_missing_directory_does_not_raise(self):
        started = time.monotonic()
        trips = wd.watch(self.tmp / "no" / "such" / "dir", rules(), poll_s=0.1, max_seconds=0.4)
        self.assertEqual(trips, [])
        self.assertGreaterEqual(time.monotonic() - started, 0.3)

    def test_an_empty_directory_ends_quietly_when_the_time_is_up(self):
        self.assertEqual(wd.watch(self.gw.path, rules(), poll_s=0.1, max_seconds=0.3), [])

    def test_the_stop_event_ends_it_quietly_and_at_once(self):
        event = threading.Event()
        thread, out = self.run_watch(self.gw.path, rules(), poll_s=30, stop_event=event)
        time.sleep(0.3)
        self.assertTrue(thread.is_alive())
        stopped_at = time.monotonic()
        event.set()
        thread.join(timeout=5)
        self.assertEqual(out["trips"], [])
        self.assertLess(out["done_at"] - stopped_at, 2)

    def test_one_last_poll_follows_the_stop_event(self):
        event = threading.Event()
        thread, out = self.run_watch(self.gw.path, rules(), poll_s=30, stop_event=event)
        time.sleep(0.3)
        self.gw.record(rec(1, usage_missing=True))
        event.set()
        thread.join(timeout=5)
        self.assertEqual(names(out["trips"]), ["usage_missing"])

    def test_unreadable_logs_stop_it_after_three_polls_in_a_row(self):
        (self.gw.path / wd.METER_NAME).mkdir()  # reading a directory fails with something other than "missing"
        started = time.monotonic()
        trips = wd.watch(self.gw.path, rules(), poll_s=0.05, max_seconds=30)
        self.assertEqual(names(trips), ["watchdog_error"])
        self.assertEqual(trips[0].counts["consecutive_poll_errors"], 3)
        self.assertIn("IsADirectoryError", trips[0].message)
        self.assertLess(time.monotonic() - started, 3)

    def test_bad_arguments_are_refused_before_anything_is_read(self):
        for pid in (0, 1, -1, -500, os.getpid(), True, "12"):
            with self.subTest(pid=pid), self.assertRaises(ValueError):
                wd.watch(self.gw.path, rules(), [pid], max_seconds=0)
        with self.assertRaises(ValueError):
            wd.watch(self.gw.path, rules(), poll_s=0, max_seconds=0)


class ReportTests(TmpDirCase):
    def trip_with_sentinel(self) -> list:
        self.gw.record(rec(1))
        self.gw.body(chat_body(1, reasoning=7, text=SENTINEL))
        self.gw.record(rec(2, streamed=True))
        self.gw.body({"call_id": "call0002", "request": SENTINEL, "response": f"data: {SENTINEL}\n\ndata: [DONE]\n"})
        self.gw.record(rec(3, http_status=400, voided=True))
        self.gw.body({"call_id": "call0003", "request": SENTINEL,
                      "response": json.dumps({"error": {"message": SENTINEL, "type": "invalid_request_error"}})})
        return wd.watch(self.gw.path, rules(), report_path=self.tmp / "report.json", max_seconds=0)

    def test_the_report_holds_counts_and_no_body_text(self):
        trips = self.trip_with_sentinel()
        self.assertEqual(names(trips), ["provider_error", "reasoning_tokens"])
        text = (self.tmp / "report.json").read_text()
        self.assertNotIn(SENTINEL, text)
        self.assertNotIn(SENTINEL, repr(trips))
        report = json.loads(text)
        self.assertEqual(report["tripped_rules"], ["provider_error", "reasoning_tokens"])
        self.assertRegex(report["tripped_at_utc"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$")
        self.assertEqual(report["counters"]["records"], 3)
        self.assertEqual(report["counters"]["unparsed_bodies"], 1)
        self.assertEqual(report["counters"]["responses_with_reasoning_tokens"], 1)
        self.assertEqual(report["rules"]["stop_at_usd"], "1000")
        self.assertEqual(report["kill"], "no pids given")
        self.assertEqual(oct((self.tmp / "report.json").stat().st_mode & 0o777), "0o600")
        self.assertEqual(sorted(p.name for p in self.tmp.iterdir() if p.name.startswith("report")), ["report.json"])

    def test_the_report_is_not_needed_and_a_bad_path_does_not_stop_the_kill(self):
        self.gw.record(rec(1, refusal="gateway_budget_exceeded"))
        sleeper = self.spawn("sleep", "60")
        with contextlib.redirect_stderr(io.StringIO()) as complaint:
            trips = wd.watch(self.gw.path, rules(), [sleeper.pid], report_path=self.tmp / "no-dir" / "r.json",
                             max_seconds=0, grace_s=5)
        self.assertIn("could not be written", complaint.getvalue())
        self.assertEqual(names(trips), ["gateway_refusal"])
        self.assertEqual(sleeper.wait(timeout=5), -signal.SIGTERM)
        self.assertEqual(names(wd.watch(self.gw.path, rules(), max_seconds=0)), ["gateway_refusal"])


class KillTests(TmpDirCase):
    def test_it_terminates_a_real_process_and_returns(self):
        self.gw.record(rec(1, usage_missing=True))
        sleeper = self.spawn("sleep", "60")
        other = self.spawn("sleep", "60")
        started = time.monotonic()
        trips = wd.watch(self.gw.path, rules(), [sleeper.pid, other.pid], poll_s=0.1,
                         report_path=self.tmp / "report.json", max_seconds=10)
        elapsed = time.monotonic() - started
        self.assertEqual(names(trips), ["usage_missing"])
        self.assertLess(elapsed, 5, "a process that has exited must not hold the watchdog for the whole grace period")
        self.assertEqual(sleeper.wait(timeout=5), -signal.SIGTERM)
        self.assertEqual(other.wait(timeout=5), -signal.SIGTERM)
        report = json.loads((self.tmp / "report.json").read_text())
        self.assertEqual(report["kill"], {str(sleeper.pid): "terminated", str(other.pid): "terminated"})

    def test_a_process_that_ignores_sigterm_is_killed_after_the_grace_period(self):
        code = ("import signal, time\nsignal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
                "print('ready', flush=True)\ntime.sleep(60)\n")
        stubborn = self.spawn(sys.executable, "-c", code, stdout=subprocess.PIPE, text=True)
        self.assertEqual(stubborn.stdout.readline().strip(), "ready")
        self.gw.record(rec(1, usage_missing=True))
        started = time.monotonic()
        trips = wd.watch(self.gw.path, rules(), [stubborn.pid], poll_s=0.1, report_path=self.tmp / "report.json",
                         max_seconds=10, grace_s=0.6)
        elapsed = time.monotonic() - started
        self.assertEqual(names(trips), ["usage_missing"])
        self.assertEqual(stubborn.wait(timeout=5), -signal.SIGKILL)
        self.assertGreaterEqual(elapsed, 0.5, "SIGKILL must wait for the grace period")
        self.assertEqual(json.loads((self.tmp / "report.json").read_text())["kill"], {str(stubborn.pid): "killed"})

    def test_a_process_that_is_already_gone_is_reported_and_does_not_raise(self):
        done = subprocess.Popen(["true"])
        done.wait()
        self.assertEqual(wd.terminate([done.pid], grace_s=1), {done.pid: "already_gone"})

    def test_pids_are_signalled_in_the_order_given_and_each_once(self):
        self.assertEqual(wd.validate_pids([5, 6, 5, 7]), [5, 6, 7])

    def test_nothing_is_killed_when_nothing_trips(self):
        self.gw.record(rec(1))
        sleeper = self.spawn("sleep", "60")
        self.assertEqual(wd.watch(self.gw.path, rules(), [sleeper.pid], poll_s=0.1, max_seconds=0.4), [])
        self.assertIsNone(sleeper.poll())


class KillGroupTests(TmpDirCase):
    def test_a_trip_stops_the_runner_and_the_child_it_started(self):
        leader, child = self.spawn_group()
        self.assertEqual(os.getpgid(child), leader.pid)
        self.gw.record(rec(1, usage_missing=True))
        started = time.monotonic()
        trips = wd.watch(self.gw.path, rules(), poll_s=0.1, report_path=self.tmp / "report.json", max_seconds=10,
                         kill_pgids=[leader.pid], grace_s=5)
        elapsed = time.monotonic() - started
        self.assertEqual(names(trips), ["usage_missing"])
        self.assertEqual(leader.wait(timeout=5), -signal.SIGTERM)
        self.assert_gone(child)
        self.assertLess(elapsed, 4, "a group that has exited must not hold the watchdog for the whole grace period")
        report = json.loads((self.tmp / "report.json").read_text())
        self.assertEqual(report["kill_groups"], {str(leader.pid): "terminated"})
        self.assertEqual(report["kill"], "no pids given")

    def test_a_group_that_ignores_sigterm_is_killed_after_the_grace_period(self):
        leader, child = self.spawn_group(ignore_sigterm=True)
        self.gw.record(rec(1, usage_missing=True))
        started = time.monotonic()
        wd.watch(self.gw.path, rules(), poll_s=0.1, report_path=self.tmp / "report.json", max_seconds=10,
                 kill_pgids=[leader.pid], grace_s=0.6)
        self.assertGreaterEqual(time.monotonic() - started, 0.5, "SIGKILL must wait for the grace period")
        self.assertEqual(leader.wait(timeout=5), -signal.SIGKILL)
        self.assert_gone(child)
        self.assertEqual(json.loads((self.tmp / "report.json").read_text())["kill_groups"], {str(leader.pid): "killed"})

    def test_groups_and_single_pids_are_stopped_together_under_one_grace_period(self):
        leader, child = self.spawn_group()
        gateway = self.spawn("sleep", "60")
        self.gw.record(rec(1, refusal="gateway_budget_exceeded"))
        started = time.monotonic()
        wd.watch(self.gw.path, rules(), [gateway.pid], poll_s=0.1, report_path=self.tmp / "report.json", max_seconds=10,
                 kill_pgids=[leader.pid], grace_s=5)
        self.assertLess(time.monotonic() - started, 4)
        self.assertEqual(leader.wait(timeout=5), -signal.SIGTERM)
        self.assertEqual(gateway.wait(timeout=5), -signal.SIGTERM)
        self.assert_gone(child)
        report = json.loads((self.tmp / "report.json").read_text())
        self.assertEqual(report["kill"], {str(gateway.pid): "terminated"})
        self.assertEqual(report["kill_groups"], {str(leader.pid): "terminated"})

    def test_every_group_gets_sigterm_before_any_single_pid(self):
        sent = []
        with mock.patch.object(wd, "_send", lambda target, sig: sent.append((target, sig))),                 mock.patch.object(wd, "_target_alive", lambda target: False):
            outcome = wd.terminate_all([111, 112], [221, 222], grace_s=0)
        self.assertEqual(sent, [(("pgid", 221), signal.SIGTERM), (("pgid", 222), signal.SIGTERM),
                                (("pid", 111), signal.SIGTERM), (("pid", 112), signal.SIGTERM)])
        self.assertEqual(outcome, ({111: "terminated", 112: "terminated"}, {221: "terminated", 222: "terminated"}))

    def test_nothing_is_killed_when_nothing_trips(self):
        leader, child = self.spawn_group()
        self.gw.record(rec(1))
        self.assertEqual(wd.watch(self.gw.path, rules(), poll_s=0.1, max_seconds=0.4, kill_pgids=[leader.pid]), [])
        self.assertIsNone(leader.poll())
        self.assertTrue(wd._alive(child))

    def test_a_group_that_is_already_gone_is_reported_and_does_not_raise(self):
        done = subprocess.Popen(["true"], start_new_session=True)
        done.wait()
        self.assertEqual(wd.terminate_groups([done.pid], grace_s=1), {done.pid: "already_gone"})

    def test_a_group_that_holds_only_a_zombie_is_gone_not_refused(self):
        leader, child = self.spawn_group()
        os.kill(child, signal.SIGKILL)
        leader.kill()
        deadline = time.monotonic() + 3
        while wd._group_alive(leader.pid) and time.monotonic() < deadline:
            time.sleep(0.05)
        # macOS answers EPERM to a signal sent to such a group; that must not read as "not permitted"
        self.assertIn(wd.terminate_groups([leader.pid], grace_s=1)[leader.pid], ("already_gone", "terminated"))
        leader.wait()

    def test_bad_group_ids_are_refused_before_anything_is_read(self):
        # no trip is possible here (an empty directory), so even a validation that failed could not signal anything
        for pgid in (0, 1, -1, -500, os.getpgrp(), True, "12", None):
            with self.subTest(pgid=pgid), self.assertRaises(ValueError):
                wd.watch(self.gw.path, rules(), kill_pgids=[pgid], max_seconds=0)
        with self.assertRaises(ValueError):
            wd.validate_pgids([os.getpgrp()])
        self.assertEqual(wd.validate_pgids([5, 6, 5, 7]), [5, 6, 7])

    def test_the_group_check_does_not_mistake_a_zombie_leader_for_a_living_group(self):
        leader, child = self.spawn_group()
        self.assertTrue(wd._group_alive(leader.pid))
        os.kill(child, signal.SIGKILL)
        leader.kill()
        deadline = time.monotonic() + 3
        while wd._group_alive(leader.pid) and time.monotonic() < deadline:
            time.sleep(0.05)
        self.assertFalse(wd._group_alive(leader.pid))  # the leader is a zombie until the test waits for it
        leader.wait()


class RulesTests(unittest.TestCase):
    def test_defaults_are_the_plans_numbers(self):
        r = wd.Rules(Decimal("0.09"))
        self.assertEqual((r.length_share, r.repeat_share, r.voided_max, r.min_sample, r.tolerated_retryable),
                         (Decimal("0.05"), Decimal("0.05"), 3, 20, 1))

    def test_floats_become_exact_decimals(self):
        r = wd.Rules(0.09, length_share=0.05, repeat_share=0.1)
        self.assertEqual((r.stop_at_usd, r.length_share, r.repeat_share), (Decimal("0.09"), Decimal("0.05"), Decimal("0.1")))

    def test_nonsense_is_refused(self):
        for kw in ({"stop_at_usd": -1}, {"stop_at_usd": "x"}, {"length_share": 1.5}, {"repeat_share": -0.1},
                   {"voided_max": -1}, {"min_sample": 0}, {"tolerated_retryable": -1}, {"voided_max": 1.5},
                   {"min_sample": True}):
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                wd.Rules(**{"stop_at_usd": 1, **kw})


def run_cli(*args: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env=env, timeout=60)


class CliTests(TmpDirCase):
    def test_exit_3_and_a_report_when_a_rule_trips(self):
        self.gw.record(rec(1, refusal="gateway_budget_exceeded", http_status=429))
        self.gw.body(chat_body(1, text=SENTINEL))
        done = run_cli("--gateway-dir", str(self.gw.path), "--stop-at-usd", "0.09", "--report", str(self.tmp / "r.json"),
                       "--max-seconds", "0")
        self.assertEqual(done.returncode, 3, done.stderr)
        self.assertIn("TRIPPED gateway_refusal", done.stderr)
        self.assertEqual(json.loads((self.tmp / "r.json").read_text())["tripped_rules"], ["gateway_refusal"])
        self.assertNotIn(SENTINEL, done.stdout + done.stderr + (self.tmp / "r.json").read_text())

    def test_exit_0_when_the_time_limit_ends_it_quietly(self):
        self.gw.record(rec(1))
        self.gw.body(chat_body(1))
        done = run_cli("--gateway-dir", str(self.gw.path), "--stop-at-usd", "0.09", "--max-seconds", "0.3", "--poll-s", "0.1")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("watching", done.stdout)
        self.assertEqual(done.stderr, "")

    def test_the_summary_line_and_the_warning_about_missing_bodies(self):
        self.gw.record(rec(1))
        self.gw.record(rec(2))
        self.gw.body(chat_body(1))
        base = ["--gateway-dir", str(self.gw.path), "--stop-at-usd", "1", "--max-seconds", "0"]
        done = run_cli(*base)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("read 2 call(s)", done.stdout)
        self.assertIn("1 chat answer(s) checked", done.stdout)
        self.assertIn("WARNING 1 chat call(s) have no body", done.stderr)
        self.gw.body(chat_body(2))
        done = run_cli(*base)
        self.assertIn("2 chat answer(s) checked", done.stdout)
        self.assertEqual(done.stderr, "")

    def test_thresholds_can_be_changed_on_the_command_line(self):
        for i in range(2):
            self.gw.record(rec(i, voided=True))
        args = ["--gateway-dir", str(self.gw.path), "--stop-at-usd", "1", "--max-seconds", "0"]
        self.assertEqual(run_cli(*args).returncode, 0)
        self.assertEqual(run_cli(*args, "--voided-max", "1").returncode, 3)
        self.assertEqual(run_cli("--gateway-dir", str(self.gw.path), "--stop-at-usd", "0.0005", "--max-seconds", "0").returncode, 3)

    def test_since_and_from_now(self):
        self.gw.record(rec(1, ts="2026-11-02T10:00:00.000Z", refusal="gateway_bad_request"))
        base = ["--gateway-dir", str(self.gw.path), "--stop-at-usd", "1", "--max-seconds", "0"]
        self.assertEqual(run_cli(*base).returncode, 3)
        self.assertEqual(run_cli(*base, "--since", "2026-11-02T11:00:00Z").returncode, 0)
        self.assertEqual(run_cli(*base, "--from-now").returncode, 0)

    def test_repeat_since(self):
        for i in range(25):
            self.gw.record(rec(i, ts="2026-11-02T21:00:00.000Z"))
        for i in range(25):
            self.gw.record(rec(100 + i, ts="2026-11-02T22:00:00.000Z", request_sha256=f"sha{i:04d}"))
        base = ["--gateway-dir", str(self.gw.path), "--stop-at-usd", "1", "--max-seconds", "0"]
        self.assertEqual(run_cli(*base).returncode, 3)
        done = run_cli(*base, "--repeat-since", "2026-11-02T21:30:00Z")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("repeats looked for since 2026-11-02T21:30:00Z", done.stdout)
        self.assertEqual(run_cli(*base, "--repeat-since", "2026-11-02T22:30:00Z").returncode, 0)      # no record in it at all

    def test_usage_errors_exit_2(self):
        base = ["--gateway-dir", str(self.gw.path), "--stop-at-usd", "0.09"]
        cases = {
            "nothing": [],
            "no stop at": ["--gateway-dir", str(self.gw.path)],
            "stop at is not a number": ["--gateway-dir", str(self.gw.path), "--stop-at-usd", "lots"],
            "stop at is negative": ["--gateway-dir", str(self.gw.path), "--stop-at-usd", "-1"],
            "not a directory": ["--gateway-dir", str(self.tmp / "typo"), "--stop-at-usd", "0.09"],
            "pid 0": base + ["--kill-pid", "0"],
            "pid 1": base + ["--kill-pid", "1"],
            "pid not a number": base + ["--kill-pid", "abc"],
            "pgid 0": base + ["--max-seconds", "0", "--kill-pgid", "0"],
            "pgid 1": base + ["--max-seconds", "0", "--kill-pgid", "1"],
            "pgid negative": base + ["--max-seconds", "0", "--kill-pgid", "-7"],
            "pgid is the watchdog's own group": base + ["--max-seconds", "0", "--kill-pgid", str(os.getpgrp())],
            "pgid not a number": base + ["--max-seconds", "0", "--kill-pgid", "abc"],
            "poll 0": base + ["--poll-s", "0"],
            "negative time": base + ["--max-seconds", "-1"],
            "share above 1": base + ["--length-share", "2"],
            "since and from now": base + ["--since", "2026-11-02T11:00:00Z", "--from-now"],
            "bad since": base + ["--since", "later"],
            "bad repeat since": base + ["--repeat-since", "later"],
            "min sample 0": base + ["--min-sample", "0"],
        }
        for label, args in cases.items():
            with self.subTest(label):
                self.assertEqual(run_cli(*args).returncode, 2)

    def test_it_stops_the_pids_it_is_given(self):
        self.gw.record(rec(1, usage_missing=True))
        first, second = self.spawn("sleep", "60"), self.spawn("sleep", "60")
        done = run_cli("--gateway-dir", str(self.gw.path), "--stop-at-usd", "0.09", "--kill-pid", str(first.pid),
                       "--kill-pid", str(second.pid), "--report", str(self.tmp / "r.json"), "--poll-s", "0.1")
        self.assertEqual(done.returncode, 3, done.stderr)
        self.assertEqual(first.wait(timeout=5), -signal.SIGTERM)
        self.assertEqual(second.wait(timeout=5), -signal.SIGTERM)
        report = json.loads((self.tmp / "r.json").read_text())
        self.assertEqual(report["kill"], {str(first.pid): "terminated", str(second.pid): "terminated"})

    def test_it_stops_a_whole_process_group(self):
        leader, child = self.spawn_group()
        self.gw.record(rec(1, usage_missing=True))
        gateway = self.spawn("sleep", "60")
        done = run_cli("--gateway-dir", str(self.gw.path), "--stop-at-usd", "0.09", "--kill-pgid", str(leader.pid),
                       "--kill-pid", str(gateway.pid), "--report", str(self.tmp / "r.json"), "--poll-s", "0.1")
        self.assertEqual(done.returncode, 3, done.stderr)
        self.assertEqual(leader.wait(timeout=5), -signal.SIGTERM)
        self.assertEqual(gateway.wait(timeout=5), -signal.SIGTERM)
        self.assert_gone(child)
        report = json.loads((self.tmp / "r.json").read_text())
        self.assertEqual(report["kill_groups"], {str(leader.pid): "terminated"})
        self.assertEqual(report["kill"], {str(gateway.pid): "terminated"})

    def test_several_groups_after_one_flag_and_the_flag_repeated(self):
        first, first_child = self.spawn_group()
        second, second_child = self.spawn_group()
        self.gw.record(rec(1, usage_missing=True))
        done = run_cli("--gateway-dir", str(self.gw.path), "--stop-at-usd", "0.09", "--kill-pgid", str(first.pid),
                       "--kill-pgid", str(second.pid), "--max-seconds", "0")
        self.assertEqual(done.returncode, 3, done.stderr)
        for leader, child in ((first, first_child), (second, second_child)):
            self.assertEqual(leader.wait(timeout=5), -signal.SIGTERM)
            self.assert_gone(child)

    def test_several_pids_after_one_flag(self):
        self.gw.record(rec(1, usage_missing=True))
        first, second = self.spawn("sleep", "60"), self.spawn("sleep", "60")
        done = run_cli("--gateway-dir", str(self.gw.path), "--stop-at-usd", "0.09", "--kill-pid", str(first.pid),
                       str(second.pid), "--max-seconds", "0")
        self.assertEqual(done.returncode, 3, done.stderr)
        self.assertEqual(first.wait(timeout=5), -signal.SIGTERM)
        self.assertEqual(second.wait(timeout=5), -signal.SIGTERM)


if __name__ == "__main__":
    unittest.main()
