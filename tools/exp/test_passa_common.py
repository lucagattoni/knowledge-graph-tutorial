"""Tests for tools/exp/passa_common.py. Standard library only; loopback only; no model and no key.

A fake Ollama (native endpoints) and the stub model server from stub_llm.py stand in for the real thing.

Run from the repository root:

    uv run python -m unittest tools/exp/test_passa_common.py
"""

from __future__ import annotations

import json
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import passa_common as pc  # noqa: E402
import stub_llm  # noqa: E402

REPO = HERE.parents[1]


class FakeOllama:
    """The native endpoints preflight and probe_speed use, with settings a test can change."""

    def __init__(self) -> None:
        self.tags = ["granite-test-16k:latest", "embed-test:latest"]
        self.parameters = "num_ctx 16384\ntemperature 0.2"
        outer = self

        class H(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *a: object) -> None:
                return

            def _send(self, obj: dict) -> None:
                data = json.dumps(obj).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self) -> None:  # noqa: N802
                if self.path == "/api/tags":
                    self._send({"models": [{"name": n} for n in outer.tags]})
                elif self.path == "/api/version":
                    self._send({"version": "0.0.0-test"})
                else:
                    self.send_error(404)

            def do_POST(self) -> None:  # noqa: N802
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
                if self.path == "/api/show":
                    self._send({"parameters": outer.parameters, "details": {"family": "test"}, "capabilities": ["completion"]})
                elif self.path == "/api/chat":
                    if (body.get("options") or {}).get("num_predict") == 1:
                        self._send({"prompt_eval_count": 1500, "prompt_eval_duration": 3_000_000_000, "load_duration": 2_500_000_000})
                    else:
                        self._send({"eval_count": 120, "eval_duration": 4_000_000_000})
                else:
                    self.send_error(404)

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.server.daemon_threads = True
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()


class ParametersTests(unittest.TestCase):
    def test_parses_modelfile_parameter_lines_and_keeps_the_last_of_a_repeated_name(self) -> None:
        text = {"parameters": "num_ctx                        8192\nstop    \"<end>\"\nnum_ctx 16384\n\n"}
        self.assertEqual(pc.parameters_of(text), {"num_ctx": "16384", "stop": '"<end>"'})

    def test_no_parameters_is_an_empty_dict(self) -> None:
        self.assertEqual(pc.parameters_of({}), {})
        self.assertEqual(pc.parameters_of({"parameters": None}), {})


class PreflightTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fake = FakeOllama()
        self.addCleanup(self.fake.close)

    def test_a_model_with_an_explicit_large_enough_context_passes_and_reports_facts(self) -> None:
        facts = pc.preflight(self.fake.url, "granite-test-16k", min_ctx=16384, embed_model="embed-test")
        self.assertEqual(facts["num_ctx"], 16384)
        self.assertEqual(facts["ollama_version"], "0.0.0-test")
        self.assertEqual(facts["model"], "granite-test-16k")

    def test_a_missing_chat_model_or_embedding_model_is_refused_and_named(self) -> None:
        with self.assertRaisesRegex(pc.PassAError, "not installed.*nope"):
            pc.preflight(self.fake.url, "nope", min_ctx=16384)
        with self.assertRaisesRegex(pc.PassAError, "not installed.*no-embed"):
            pc.preflight(self.fake.url, "granite-test-16k", min_ctx=16384, embed_model="no-embed")

    def test_a_model_without_an_explicit_context_is_refused(self) -> None:
        self.fake.parameters = "temperature 0.2"
        with self.assertRaisesRegex(pc.PassAError, "no explicit num_ctx"):
            pc.preflight(self.fake.url, "granite-test-16k", min_ctx=16384)

    def test_a_context_below_the_minimum_is_refused_and_exactly_the_minimum_passes(self) -> None:
        self.fake.parameters = "num_ctx 4096"
        with self.assertRaisesRegex(pc.PassAError, "below"):
            pc.preflight(self.fake.url, "granite-test-16k", min_ctx=16384)
        self.fake.parameters = "num_ctx 16384"
        self.assertEqual(pc.preflight(self.fake.url, "granite-test-16k", min_ctx=16384)["num_ctx"], 16384)

    def test_an_unreachable_server_is_a_clear_error(self) -> None:
        with self.assertRaises(pc.PassAError):
            pc.preflight("http://127.0.0.1:9", "m", min_ctx=1)


class ProbeTests(unittest.TestCase):
    def test_rates_come_from_the_timing_fields_exactly(self) -> None:
        fake = FakeOllama()
        self.addCleanup(fake.close)
        r = pc.probe_speed(fake.url, "granite-test-16k")
        self.assertEqual(r["prompt_tokens_per_second"], 500.0)       # 1500 tokens in 3 s
        self.assertEqual(r["generation_tokens_per_second"], 30.0)    # 120 tokens in 4 s
        self.assertEqual(r["load_seconds_first_call"], 2.5)


class LocalGatewayTests(unittest.TestCase):
    def test_usage_comes_from_the_upstream_and_bodies_are_joined_by_call_id(self) -> None:
        with stub_llm.Stub(lambda call: "hello") as stub, tempfile.TemporaryDirectory() as d:
            with pc.LocalGateway(d, stub.base_url, ["chat-test", "embed-test"], REPO) as gw:
                def post(path: str, payload: dict) -> dict:
                    req = urllib.request.Request(gw.base_url + path, data=json.dumps(payload).encode(),
                                                 headers={"Content-Type": "application/json", "Authorization": "Bearer dummy"})
                    with urllib.request.urlopen(req, timeout=30) as r:
                        return json.loads(r.read())
                chat = post("/chat/completions", {"model": "chat-test", "messages": [{"role": "user", "content": "say something"}]})
                emb = post("/embeddings", {"model": "embed-test", "input": ["a", "b"]})
                calls = gw.calls()
            self.assertEqual(len(calls), 2)
            first, second = calls
            self.assertEqual(first["input_tokens"], chat["usage"]["prompt_tokens"])
            self.assertEqual(first["output_tokens"], chat["usage"]["completion_tokens"])
            self.assertEqual(first["request"]["messages"][0]["content"], "say something")
            self.assertEqual(first["response"]["choices"][0]["message"]["content"], "hello")
            self.assertEqual(second["route"].split("/")[-1], "embeddings")
            self.assertEqual(second["input_tokens"], emb["usage"]["prompt_tokens"])
            self.assertEqual(second["request"]["input"], ["a", "b"])                    # each call gets its own body
            self.assertEqual(len(second["response"]["data"]), 2)
            self.assertNotEqual(first["request"], second["request"])
            self.assertEqual(first["cost"] if "cost" in first else "0", "0")

    def test_a_streamed_response_is_kept_as_text_and_its_usage_is_still_logged(self) -> None:
        with stub_llm.Stub(lambda call: "streamed words") as stub, tempfile.TemporaryDirectory() as d:
            with pc.LocalGateway(d, stub.base_url, ["chat-test"], REPO) as gw:
                req = urllib.request.Request(gw.base_url + "/chat/completions", data=json.dumps(
                    {"model": "chat-test", "stream": True, "messages": [{"role": "user", "content": "go"}]}).encode(),
                    headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    r.read()
                (call,) = gw.calls()
            self.assertIsInstance(call["response"], str)
            self.assertIn("data: ", call["response"])
            self.assertIn("streamed words", call["response"])
            self.assertTrue(call["streamed"])
            self.assertGreater(call["output_tokens"], 0)

    def test_a_model_that_was_not_listed_is_refused_and_nothing_is_forwarded(self) -> None:
        with stub_llm.Stub(lambda call: "x") as stub, tempfile.TemporaryDirectory() as d:
            with pc.LocalGateway(d, stub.base_url, ["only-this"], REPO) as gw:
                req = urllib.request.Request(gw.base_url + "/chat/completions", data=json.dumps(
                    {"model": "something-else", "messages": [{"role": "user", "content": "hi"}]}).encode(),
                    headers={"Content-Type": "application/json"})
                with self.assertRaises(urllib.error.HTTPError) as ctx:
                    urllib.request.urlopen(req, timeout=30)
                self.assertEqual(ctx.exception.code, 400)
            self.assertEqual(stub.summary()["chat_calls"], 0)

    def test_stopping_ends_the_process_and_base_url_then_raises(self) -> None:
        with stub_llm.Stub(lambda call: "x") as stub, tempfile.TemporaryDirectory() as d:
            gw = pc.LocalGateway(d, stub.base_url, ["m"], REPO).start()
            proc = gw.proc
            gw.stop()
            self.assertIsNotNone(proc.poll())
            self.assertIsNone(gw.proc)

    def test_summarize_groups_by_the_classifier_and_marks_calls_without_a_body(self) -> None:
        calls = [
            {"http_status": 200, "input_tokens": 10, "output_tokens": 5, "latency_ms": 100, "request": {"k": "a"}},
            {"http_status": 200, "input_tokens": 20, "output_tokens": 7, "latency_ms": 50, "request": {"k": "a"}},
            {"http_status": 500, "input_tokens": 0, "output_tokens": 0, "latency_ms": 5, "request": {"k": "b"}, "voided": True},
            {"http_status": 200, "input_tokens": 1, "output_tokens": 1, "latency_ms": 1, "request": None},
        ]
        s = pc.summarize(calls, lambda c: c["request"]["k"])
        self.assertEqual(s["by_kind"]["a"], {"calls": 2, "ok": 2, "input_tokens": 30, "output_tokens": 12, "latency_ms": 150})
        self.assertEqual(s["by_kind"]["b"]["ok"], 0)
        self.assertEqual(s["by_kind"]["no_body"]["calls"], 1)
        self.assertEqual(s["total"]["calls"], 4)


if __name__ == "__main__":
    unittest.main()
