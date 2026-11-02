"""Tests for tools/exp/stub_llm.py. Standard library only; loopback only; no model, no key.

Run from the repository root:

    uv run python -m unittest tools/exp/test_stub_llm.py
"""

from __future__ import annotations

import json
import sys
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import stub_llm as sl  # noqa: E402


def post(url: str, payload: dict) -> tuple[int, bytes, str]:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, r.read(), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers.get("Content-Type", "")


class StubTests(unittest.TestCase):
    def test_chat_reports_usage_that_matches_what_was_counted_and_recorded(self) -> None:
        with sl.Stub(lambda call: "hello there") as stub:
            status, body, _ = post(stub.base_url + "/chat/completions",
                                   {"model": "m", "messages": [{"role": "user", "content": "count these words please"}]})
            data = json.loads(body)
            self.assertEqual(status, 200)
            self.assertEqual(data["choices"][0]["message"]["content"], "hello there")
            call = stub.calls[0]
            self.assertEqual(data["usage"]["prompt_tokens"], call.prompt_tokens)
            self.assertEqual(data["usage"]["completion_tokens"], call.completion_tokens)
            self.assertGreater(call.prompt_tokens, 0)
            self.assertEqual(data["usage"]["total_tokens"], call.prompt_tokens + call.completion_tokens)

    def test_responder_can_return_a_tool_call_message(self) -> None:
        msg = {"content": None, "tool_calls": [{"id": "1", "type": "function",
                                               "function": {"name": "f", "arguments": "{}"}}]}
        with sl.Stub(lambda call: msg) as stub:
            _, body, _ = post(stub.base_url + "/chat/completions", {"model": "m", "messages": []})
            choice = json.loads(body)["choices"][0]
            self.assertEqual(choice["finish_reason"], "tool_calls")
            self.assertEqual(choice["message"]["tool_calls"][0]["function"]["name"], "f")

    def test_embeddings_are_deterministic_unit_vectors_of_the_requested_size(self) -> None:
        with sl.Stub(lambda call: "") as stub:
            url = stub.base_url + "/embeddings"
            _, b1, _ = post(url, {"model": "e", "input": ["a", "b"], "dimensions": 12})
            _, b2, _ = post(url, {"model": "e", "input": ["a", "b"], "dimensions": 12})
            d1 = json.loads(b1)["data"]
            self.assertEqual(b1, b2)
            self.assertEqual([len(x["embedding"]) for x in d1], [12, 12])
            self.assertAlmostEqual(sum(v * v for v in d1[0]["embedding"]), 1.0, places=9)
            self.assertNotEqual(d1[0]["embedding"], d1[1]["embedding"])
            self.assertEqual(stub.summary()["embedding_inputs"], 4)

    def test_streaming_sends_events_a_done_marker_and_usage_when_asked(self) -> None:
        with sl.Stub(lambda call: "streamed") as stub:
            status, body, ctype = post(stub.base_url + "/chat/completions", {
                "model": "m", "stream": True, "stream_options": {"include_usage": True},
                "messages": [{"role": "user", "content": "x"}]})
            text = body.decode()
            self.assertEqual(status, 200)
            self.assertIn("text/event-stream", ctype)
            self.assertTrue(text.rstrip().endswith("data: [DONE]"))
            self.assertIn('"usage"', text)
            self.assertIn("streamed", text)

    def test_unknown_route_is_404_and_still_recorded(self) -> None:
        with sl.Stub(lambda call: "") as stub:
            status, _, _ = post(stub.base_url + "/nothing", {})
            self.assertEqual(status, 404)
            self.assertEqual(stub.summary()["other_calls"], 1)

    def test_parallel_calls_are_all_recorded_with_distinct_sequence_numbers(self) -> None:
        with sl.Stub(lambda call: "ok") as stub:
            failures: list[BaseException] = []

            def hit() -> None:
                try:
                    post(stub.base_url + "/chat/completions",
                         {"model": "m", "messages": [{"role": "user", "content": "p"}]})
                except BaseException as exc:  # noqa: BLE001 - a refused connection must fail the test, not vanish
                    failures.append(exc)

            threads = [threading.Thread(target=hit) for _ in range(60)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            self.assertEqual(failures, [])
            self.assertEqual(stub.summary()["chat_calls"], 60)
            self.assertEqual(len({c.seq for c in stub.calls}), 60)

    def test_jsonl_dump_leaves_the_text_out_unless_asked(self) -> None:
        import tempfile
        with sl.Stub(lambda call: "ok") as stub:
            post(stub.base_url + "/chat/completions", {"model": "m", "messages": [{"role": "user", "content": "SECRET-ARTICLE"}]})
            with tempfile.TemporaryDirectory() as d:
                plain, full = Path(d) / "a.jsonl", Path(d) / "b.jsonl"
                stub.dump_jsonl(str(plain))
                stub.dump_jsonl(str(full), with_text=True)
                self.assertNotIn("SECRET-ARTICLE", plain.read_text())
                self.assertIn("SECRET-ARTICLE", full.read_text())

    def test_pseudo_vector_is_stable_across_calls(self) -> None:
        self.assertEqual(sl.pseudo_vector("same", 8), sl.pseudo_vector("same", 8))
        self.assertNotEqual(sl.pseudo_vector("same", 8), sl.pseudo_vector("other", 8))


if __name__ == "__main__":
    unittest.main()
