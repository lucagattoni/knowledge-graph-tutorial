"""Tests for tools/metering_gateway.py. Standard library only, fake upstreams on 127.0.0.1, no network, no real key.

Run from the repository root:

    uv run python -m unittest tools/test_metering_gateway.py

Every price below is invented (currency "FAKE-USD"); every key is a made-up string.
"""

from __future__ import annotations

import contextlib
import hashlib
import http.client
import io
import json
import re
import socket
import sys
import tempfile
import threading
import time
import unittest
import unittest.mock
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import metering_gateway as mg  # noqa: E402

REAL_OPENAI_KEY = "fake-real-openai-key-0123456789abcdef"
REAL_ANTHROPIC_KEY = "fake-real-anthropic-key-fedcba9876543210"
DUMMY_KEY = "dummy-client-key-not-real-xyz"
PROMPT_SENTINEL = "SENTINEL-PROMPT-TEXT"
ENVIRON = {"FAKE_OPENAI_KEY": REAL_OPENAI_KEY, "FAKE_ANTHROPIC_KEY": REAL_ANTHROPIC_KEY}


# --------------------------------------------------------------------------- fake upstreams


def send_json(h: BaseHTTPRequestHandler, status: int, obj, headers=()) -> None:
    body = json.dumps(obj).encode()
    h.send_response(status)
    h.send_header("Content-Type", "application/json")
    h.send_header("Content-Length", str(len(body)))
    for name, value in headers:
        h.send_header(name, value)
    h.send_header("Connection", "close")
    h.end_headers()
    h.wfile.write(body)


def send_sse(h: BaseHTTPRequestHandler, chunks: list[bytes], pause: float = 0.0) -> None:
    h.send_response(200)
    h.send_header("Content-Type", "text/event-stream")
    h.send_header("Connection", "close")
    h.end_headers()
    for chunk in chunks:
        h.wfile.write(chunk)
        h.wfile.flush()
        if pause:
            time.sleep(pause)


def send_chunked(h: BaseHTTPRequestHandler, status: int, content_type: str, parts: list[bytes],
                 finish: bool = True) -> None:
    """Answer with Transfer-Encoding: chunked, as a real provider's streaming endpoint does."""
    h.send_response(status)
    h.send_header("Content-Type", content_type)
    h.send_header("Transfer-Encoding", "chunked")
    h.send_header("Connection", "close")
    h.end_headers()
    for part in parts:
        h.wfile.write(f"{len(part):x}\r\n".encode() + part + b"\r\n")
        h.wfile.flush()
    if finish:
        h.wfile.write(b"0\r\n\r\n")


def pieces(data: bytes, size: int) -> list[bytes]:
    return [data[i:i + size] for i in range(0, len(data), size)]


def hang_up(h: BaseHTTPRequestHandler) -> None:
    """Close the connection without writing a single byte of response."""
    h.connection.shutdown(socket.SHUT_RDWR)


class FakeUpstream:
    """A loopback HTTP server that records every request and answers with `responder(req, handler)`."""

    def __init__(self, responder):
        self.responder = responder
        self.requests: list[dict] = []
        self.release = threading.Event()  # lets a held responder go at the end of a test
        lock = threading.Lock()
        outer = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *args):
                pass

            def do_POST(self):
                body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
                req = {"path": self.path, "headers": {k.lower(): v for k, v in self.headers.items()}, "body": body}
                with lock:
                    outer.requests.append(req)
                    req["n"] = len(outer.requests)
                self.close_connection = True
                outer.responder(req, self)

        class Server(ThreadingHTTPServer):
            daemon_threads = True
            request_queue_size = 256

        self.server = Server(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True)
        self.thread.start()

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.server.server_address[1]}/v1"

    @property
    def count(self) -> int:
        return len(self.requests)

    def close(self) -> None:
        self.release.set()
        self.server.shutdown()
        self.server.server_close()


def openai_chat_body(prompt=100, completion=50, cached=None, model="fake-small-2026-11"):
    usage = {"prompt_tokens": prompt, "completion_tokens": completion, "total_tokens": prompt + completion}
    if cached is not None:
        usage["prompt_tokens_details"] = {"cached_tokens": cached}
    return {"id": "c1", "object": "chat.completion", "model": model,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "hi"}, "finish_reason": "stop"}],
            "usage": usage}


def sse_data(obj) -> bytes:
    return b"data: " + json.dumps(obj).encode() + b"\n\n"


def openai_sse(prompt=700, completion=40, model="fake-small-2026-11", with_usage=True):
    chunk = {"id": "c1", "object": "chat.completion.chunk", "model": model, "usage": None}
    events = [sse_data({**chunk, "choices": [{"index": 0, "delta": {"content": word}}]}) for word in ("a", "b")]
    if with_usage:
        events.append(sse_data({**chunk, "choices": [], "usage": {
            "prompt_tokens": prompt, "completion_tokens": completion, "total_tokens": prompt + completion}}))
    events.append(b"data: [DONE]\n\n")
    return events


def anthropic_body(inp=500, out=120, read=None, write=None, model="fake-claude-2026-11"):
    usage = {"input_tokens": inp, "output_tokens": out}
    if read is not None:
        usage["cache_read_input_tokens"] = read
    if write is not None:
        usage["cache_creation_input_tokens"] = write
    return {"id": "m1", "type": "message", "role": "assistant", "model": model,
            "content": [{"type": "text", "text": "hi"}], "stop_reason": "end_turn", "usage": usage}


def anthropic_sse(inp=321, out=77, model="fake-claude-2026-11", with_delta=True):
    def event(name, obj):
        return f"event: {name}\n".encode() + b"data: " + json.dumps(obj).encode() + b"\n\n"

    events = [
        event("message_start", {"type": "message_start", "message": {
            "id": "m1", "type": "message", "role": "assistant", "model": model, "content": [],
            "usage": {"input_tokens": inp, "output_tokens": 1}}}),
        event("ping", {"type": "ping"}),
        event("content_block_delta", {"type": "content_block_delta", "index": 0,
                                      "delta": {"type": "text_delta", "text": "hi"}}),
    ]
    if with_delta:
        events.append(event("message_delta", {"type": "message_delta", "delta": {"stop_reason": "end_turn"},
                                              "usage": {"output_tokens": out}}))
    events.append(event("message_stop", {"type": "message_stop"}))
    return events


def answer(body):
    """A responder that always returns `body` as JSON with status 200."""
    return lambda req, h: send_json(h, 200, body)


# --------------------------------------------------------------------------- config and rig


def toml_config(log_file: str, openai_url: str, anthropic_url: str, *, cap="10", dry_run=False,
                gateway_extra="", models_extra="") -> str:
    q = json.dumps
    return f"""
[gateway]
currency = "FAKE-USD"
cap = {cap}
log_file = {q(log_file)}
{gateway_extra}

[upstreams.fake-openai]
protocol = "openai"
base_url = {q(openai_url)}
key_env = "FAKE_OPENAI_KEY"
dry_run = {str(dry_run).lower()}

[upstreams.fake-anthropic]
protocol = "anthropic"
base_url = {q(anthropic_url)}
key_env = "FAKE_ANTHROPIC_KEY"
dry_run = {str(dry_run).lower()}

[models."fake-small"]
upstream = "fake-openai"
input_per_mtok = 0.15
output_per_mtok = 0.60
cached_input_per_mtok = 0.075
source_url = "https://example.invalid/pricing/fake-small"
read_at = "20261102 10:00"

[models."fake-embed"]
upstream = "fake-openai"
input_per_mtok = 0.02
output_per_mtok = 0
source_url = "https://example.invalid/pricing/fake-embed"
read_at = "20261102 10:00"

[models."fake-dime"]
upstream = "fake-openai"
input_per_mtok = 100
output_per_mtok = 0
source_url = "https://example.invalid/pricing/fake-dime"
read_at = "20261102 10:00"

[models."fake-claude"]
upstream = "fake-anthropic"
input_per_mtok = 1.00
output_per_mtok = 5.00
cached_input_per_mtok = 0.10
cache_write_per_mtok = 1.25
source_url = "https://example.invalid/pricing/fake-claude"
read_at = "20261102 10:00"
{models_extra}
"""


class Rig:
    """A gateway on a free loopback port in front of two fake upstreams, with a temporary log directory."""

    def __init__(self, tc: unittest.TestCase, *, openai=None, anthropic=None, handler=mg.Handler, **config_kwargs):
        self.tmp = tempfile.TemporaryDirectory()
        tc.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.openai = openai or FakeUpstream(answer(openai_chat_body()))
        self.anthropic = anthropic or FakeUpstream(answer(anthropic_body()))
        self.log_path = self.dir / "meter.jsonl"
        environ = config_kwargs.pop("environ", ENVIRON)
        self.text = toml_config(str(self.log_path), self.openai.base_url, self.anthropic.base_url, **config_kwargs)
        self.cfg = mg.parse_config(self.text, environ)
        self.gw = mg.Gateway(self.cfg)
        self.server = mg.GatewayServer(self.gw, 0, handler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True)
        self.thread.start()
        tc.addCleanup(self.close)

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.gw.close()
        self.openai.close()
        self.anthropic.close()

    def request(self, method, path, body=None, headers=None, **kwargs):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=30)
        try:
            conn.request(method, path, body=body, headers=headers or {}, **kwargs)
            resp = conn.getresponse()
            return resp.status, dict(resp.getheaders()), resp.read()
        finally:
            conn.close()

    def post(self, path, payload=None, *, raw=None, headers=None):
        data = raw if raw is not None else json.dumps(payload).encode()
        sent = {"Content-Type": "application/json", "Authorization": "Bearer " + DUMMY_KEY,
                "x-api-key": DUMMY_KEY}
        sent.update(headers or {})
        return self.request("POST", path, data, sent)

    def chat(self, payload=None, **kwargs):
        return self.post("/v1/chat/completions", payload or chat_req(), **kwargs)

    def messages(self, payload=None, *, headers=None, **kwargs):
        sent = {"anthropic-version": "2023-06-01"}
        sent.update(headers or {})
        return self.post("/v1/messages", payload or claude_req(), headers=sent, **kwargs)

    def records(self) -> list[dict]:
        if not self.log_path.exists():
            return []
        return [json.loads(line) for line in self.log_path.read_text().splitlines() if line.strip()]

    def wait_records(self, n: int, timeout: float = 10.0) -> list[dict]:
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            records = self.records()
            if len(records) >= n:
                return records
            time.sleep(0.02)
        return self.records()

    def summary(self) -> dict:
        status, _, body = self.request("GET", "/_meter/summary")
        assert status == 200, status
        return json.loads(body)


def chat_req(model="fake-small", max_tokens=1000, **extra) -> dict:
    payload = {"model": model, "messages": [{"role": "user", "content": PROMPT_SENTINEL + " hello"}],
               "max_tokens": max_tokens}
    payload.update(extra)
    return payload


def claude_req(model="fake-claude", max_tokens=1000, **extra) -> dict:
    payload = {"model": model, "messages": [{"role": "user", "content": PROMPT_SENTINEL + " hello"}],
               "max_tokens": max_tokens}
    payload.update(extra)
    return payload


def encoded(payload) -> bytes:
    return json.dumps(payload).encode()


def expect_reserve(body_len: int, in_price: str, out_price: str, max_out: int, bytes_per_token: int = 2) -> Decimal:
    """The reservation worked out again here, not by calling the module."""
    tokens = -(-body_len // bytes_per_token)
    return (Decimal(tokens) * Decimal(in_price) + Decimal(max_out) * Decimal(out_price)) / 1000000


# --------------------------------------------------------------------------- 1. usage is what the upstream reported


class UsageLoggedTests(unittest.TestCase):
    def check_common(self, rec, *, route, upstream, requested, reported, status=200):
        self.assertEqual(rec["route"], route)
        self.assertEqual(rec["upstream"], upstream)
        self.assertEqual(rec["model_requested"], requested)
        self.assertEqual(rec["model_reported"], reported)
        self.assertEqual(rec["http_status"], status)
        self.assertEqual(rec["currency"], "FAKE-USD")
        self.assertIs(rec["voided"], False)
        self.assertIs(rec["usage_missing"], False)
        self.assertIsNone(rec["refusal"])
        self.assertRegex(rec["ts"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$")
        self.assertRegex(rec["call_id"], r"^[0-9a-f]{32}$")
        self.assertIsInstance(rec["latency_ms"], int)

    def test_openai_chat_non_streaming_with_cached_tokens(self):
        rig = Rig(self, openai=FakeUpstream(answer(openai_chat_body(prompt=1200, completion=300, cached=200))))
        payload = chat_req()
        status, _, body = rig.chat(payload)
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["usage"]["prompt_tokens"], 1200)
        (rec,) = rig.records()
        self.check_common(rec, route="/v1/chat/completions", upstream="fake-openai", requested="fake-small",
                          reported="fake-small-2026-11")
        self.assertEqual((rec["input_tokens"], rec["output_tokens"], rec["cached_input_tokens"]), (1200, 300, 200))
        # 1000 plain x 0.15 + 200 cached x 0.075 + 300 out x 0.60, per million: 0.00015 + 0.000015 + 0.00018
        self.assertEqual(rec["cost"], "0.000345")
        self.assertIs(rec["streamed"], False)
        sent = encoded(payload)
        self.assertEqual(rec["request_sha256"], hashlib.sha256(sent).hexdigest())
        self.assertEqual((rec["bytes_in"], rec["bytes_out"]), (len(sent), len(body)))

    def test_openai_chat_streaming_and_stream_options_injected(self):
        events = openai_sse(prompt=700, completion=40)
        rig = Rig(self, openai=FakeUpstream(lambda req, h: send_sse(h, events)))
        status, _, body = rig.chat(chat_req(stream=True))
        self.assertEqual(status, 200)
        self.assertEqual(body, b"".join(events), "the stream must reach the client unchanged")
        (rec,) = rig.records()
        self.check_common(rec, route="/v1/chat/completions", upstream="fake-openai", requested="fake-small",
                          reported="fake-small-2026-11")
        self.assertEqual((rec["input_tokens"], rec["output_tokens"], rec["cached_input_tokens"]), (700, 40, None))
        self.assertEqual(rec["cost"], "0.000129")  # 700 x 0.15 + 40 x 0.60, per million
        self.assertIs(rec["streamed"], True)
        self.assertEqual(rec["bytes_out"], len(body))
        forwarded = json.loads(rig.openai.requests[0]["body"])
        self.assertEqual(forwarded["stream_options"], {"include_usage": True})
        # the hash is of what the client sent, not of what the gateway forwarded
        self.assertEqual(rec["request_sha256"], hashlib.sha256(encoded(chat_req(stream=True))).hexdigest())

    def test_stream_options_the_client_set_are_kept_and_an_explicit_false_is_respected(self):
        rig = Rig(self, openai=FakeUpstream(lambda req, h: send_sse(h, openai_sse())))
        rig.chat(chat_req(stream=True, stream_options={"include_obfuscation": False}))
        self.assertEqual(json.loads(rig.openai.requests[0]["body"])["stream_options"],
                         {"include_obfuscation": False, "include_usage": True})
        rig.chat(chat_req(stream=True, stream_options={"include_usage": False}))
        self.assertEqual(json.loads(rig.openai.requests[1]["body"])["stream_options"], {"include_usage": False})
        # an upstream that obeys the explicit false sends no usage chunk
        rig2 = Rig(self, openai=FakeUpstream(lambda req, h: send_sse(h, openai_sse(with_usage=False))))
        rig2.chat(chat_req(stream=True, stream_options={"include_usage": False}))
        self.assertIs(rig2.records()[0]["usage_missing"], True)

    def test_anthropic_non_streaming_with_cache_fields(self):
        rig = Rig(self, anthropic=FakeUpstream(answer(anthropic_body(inp=500, out=120, read=2000, write=400))))
        status, _, body = rig.messages()
        self.assertEqual(status, 200)
        (rec,) = rig.records()
        self.check_common(rec, route="/v1/messages", upstream="fake-anthropic", requested="fake-claude",
                          reported="fake-claude-2026-11")
        # total input = input + cache read + cache creation
        self.assertEqual((rec["input_tokens"], rec["output_tokens"], rec["cached_input_tokens"]), (2900, 120, 2000))
        self.assertEqual(rec["cache_creation_input_tokens"], 400)
        # 500 x 1.00 + 2000 x 0.10 + 400 x 1.25 + 120 x 5.00, per million
        self.assertEqual(rec["cost"], "0.0018")
        self.assertEqual(rec["bytes_out"], len(body))

    def test_anthropic_streaming_takes_input_from_start_and_output_from_the_last_delta(self):
        events = anthropic_sse(inp=321, out=77)
        rig = Rig(self, anthropic=FakeUpstream(lambda req, h: send_sse(h, events)))
        status, _, body = rig.messages(claude_req(stream=True))
        self.assertEqual(body, b"".join(events))
        (rec,) = rig.records()
        self.check_common(rec, route="/v1/messages", upstream="fake-anthropic", requested="fake-claude",
                          reported="fake-claude-2026-11")
        self.assertEqual((rec["input_tokens"], rec["output_tokens"], rec["cached_input_tokens"]), (321, 77, None))
        self.assertEqual(rec["cost"], "0.000706")  # 321 x 1.00 + 77 x 5.00, per million
        self.assertIs(rec["streamed"], True)

    def test_embeddings_have_input_tokens_only(self):
        body = {"object": "list", "model": "fake-embed-v1", "data": [{"index": 0, "embedding": [0.1]}],
                "usage": {"prompt_tokens": 5000, "total_tokens": 5000}}
        rig = Rig(self, openai=FakeUpstream(answer(body)))
        status, _, _ = rig.post("/v1/embeddings", {"model": "fake-embed", "input": "text"})
        self.assertEqual(status, 200)
        (rec,) = rig.records()
        self.assertEqual((rec["input_tokens"], rec["output_tokens"]), (5000, 0))
        self.assertEqual(rec["cost"], "0.0001")  # 5000 x 0.02 per million
        self.assertEqual(rec["model_reported"], "fake-embed-v1")

    def test_urls_headers_and_query_reach_the_upstream_correctly(self):
        rig = Rig(self)
        rig.messages(claude_req(), headers={"Accept-Encoding": "gzip", "Cookie": "session=abc"})
        rig.chat(headers={"x-trace": "t-1"})
        rig.post("/v1/messages?beta=true", claude_req(), headers={"anthropic-version": "2023-06-01"})
        self.assertEqual(rig.anthropic.requests[0]["path"], "/v1/messages")
        self.assertEqual(rig.anthropic.requests[1]["path"], "/v1/messages?beta=true")
        self.assertEqual(rig.openai.requests[0]["path"], "/v1/chat/completions")
        self.assertEqual(rig.anthropic.requests[0]["headers"]["anthropic-version"], "2023-06-01")
        self.assertEqual(rig.openai.requests[0]["headers"]["x-trace"], "t-1")
        self.assertNotIn("cookie", rig.anthropic.requests[0]["headers"])
        self.assertEqual(rig.anthropic.requests[0]["headers"].get("accept-encoding"), "identity")

    def test_chunked_request_body_is_accepted(self):
        rig = Rig(self)
        data = encoded(chat_req())
        status, _, _ = rig.request("POST", "/v1/chat/completions", iter([data[:15], data[15:]]),
                                   {"Content-Type": "application/json", "Transfer-Encoding": "chunked"},
                                   encode_chunked=True)
        self.assertEqual(status, 200)
        self.assertEqual(rig.openai.requests[0]["body"], data)

    def test_usage_is_logged_when_the_client_hangs_up_mid_stream(self):
        release = threading.Event()
        events = openai_sse(prompt=700, completion=40)  # [text, text, usage, DONE]
        filler = [sse_data({"choices": [{"index": 0, "delta": {"content": "x"}}], "usage": None}) for _ in range(8)]

        def responder(req, h):
            send_sse(h, events[:1])
            release.wait(10)
            # several writes land on the dead socket before the usage chunk: the gateway must keep reading
            send_sse_rest(h, filler + events[2:])

        def send_sse_rest(h, rest):
            try:
                for chunk in rest:
                    h.wfile.write(chunk)
                    h.wfile.flush()
                    time.sleep(0.05)
            except OSError:
                pass

        rig = Rig(self, openai=FakeUpstream(responder))
        sock = socket.create_connection(("127.0.0.1", rig.port), timeout=10)
        data = encoded(chat_req(stream=True))
        sock.sendall(b"POST /v1/chat/completions HTTP/1.1\r\nHost: 127.0.0.1\r\nContent-Type: application/json\r\n"
                     + f"Content-Length: {len(data)}\r\n\r\n".encode() + data)
        got = b""
        while b"chat.completion.chunk" not in got:
            got += sock.recv(4096)
        sock.close()
        release.set()
        (rec,) = rig.wait_records(1)
        self.assertEqual((rec["input_tokens"], rec["output_tokens"]), (700, 40))
        self.assertIs(rec["usage_missing"], False)
        self.assertEqual(rec["cost"], "0.000129")

    def test_sse_reader_survives_any_chunk_boundary(self):
        for events, protocol, kind, expected in (
            (openai_sse(prompt=11, completion=22), "openai", "chat", (11, 22)),
            (anthropic_sse(inp=33, out=44), "anthropic", "messages", (33, 44)),
        ):
            reader = mg.SseUsage(protocol, kind)
            for byte in b"".join(events).replace(b"\n", b"\r\n"):  # CRLF line ends are legal too
                reader.feed(bytes([byte]))
            usage = reader.result()
            self.assertEqual((usage.input_tokens, usage.output_tokens), expected)

    def test_anthropic_stream_later_cumulative_fields_replace_earlier_ones(self):
        reader = mg.SseUsage("anthropic", "messages")
        reader.feed(b'data: {"type":"message_start","message":{"model":"m","usage":{"input_tokens":10,"output_tokens":1}}}\n')
        reader.feed(b'data: {"type":"message_delta","usage":{"input_tokens":25,"output_tokens":9,"cache_read_input_tokens":4}}\n')
        usage = reader.result()
        self.assertEqual((usage.input_tokens, usage.output_tokens, usage.cached_input_tokens), (29, 9, 4))


# --------------------------------------------------------------------------- 2. the cap


class CapTests(unittest.TestCase):
    def cap_for(self, body_len, first_cost, *, in_price, out_price, max_out):
        """A cap that fits the first call's reservation but not the second call after the first one settles."""
        reserve = expect_reserve(body_len, in_price, out_price, max_out)
        return reserve, reserve + Decimal(first_cost) / 2

    def test_the_call_that_would_cross_the_cap_is_refused_and_nothing_is_forwarded_openai(self):
        payload = chat_req()
        reserve, cap = self.cap_for(len(encoded(payload)), "0.000045", in_price="0.15", out_price="0.60", max_out=1000)
        rig = Rig(self, cap=format(cap, "f"), openai=FakeUpstream(answer(openai_chat_body(100, 50))))
        self.assertEqual(rig.chat(payload)[0], 200)
        self.assertEqual(rig.openai.count, 1)
        status, _, body = rig.chat(payload)
        self.assertEqual(status, 429)
        self.assertIn("gateway_budget_exceeded", body.decode())
        self.assertEqual(json.loads(body)["error"]["code"], "gateway_budget_exceeded")
        self.assertEqual(rig.openai.count, 1, "a refused call must not reach the upstream")
        ok, refused = rig.records()
        self.assertEqual(ok["cost"], "0.000045")
        self.assertEqual(Decimal(ok["reserve"]), reserve)
        self.assertEqual((refused["refusal"], refused["http_status"], refused["cost"]), ("gateway_budget_exceeded", 429, "0"))
        self.assertIs(refused["voided"], False)
        summary = rig.summary()
        self.assertEqual((summary["calls"], summary["refused"], summary["spent"]), (1, 1, "0.000045"))

    def test_the_call_that_would_cross_the_cap_is_refused_and_nothing_is_forwarded_anthropic(self):
        payload = claude_req()
        reserve, cap = self.cap_for(len(encoded(payload)), "0.000706", in_price="1.00", out_price="5.00", max_out=1000)
        rig = Rig(self, cap=format(cap, "f"), anthropic=FakeUpstream(answer(anthropic_body(inp=321, out=77))))
        self.assertEqual(rig.messages(payload)[0], 200)
        status, _, body = rig.messages(payload)
        self.assertEqual(status, 429)
        self.assertEqual(json.loads(body)["error"]["type"], "gateway_budget_exceeded")  # Anthropic-shaped error
        self.assertEqual(rig.anthropic.count, 1)

    def test_a_reservation_that_reaches_the_cap_exactly_is_allowed(self):
        payload = chat_req()
        reserve = expect_reserve(len(encoded(payload)), "0.15", "0.60", 1000)
        rig = Rig(self, cap=format(reserve, "f"), openai=FakeUpstream(answer(openai_chat_body(100, 50))))
        self.assertEqual(rig.chat(payload)[0], 200, "spend + reserve == cap is not past the cap")
        self.assertEqual(Decimal(rig.records()[0]["reserve"]), reserve)

    def test_a_single_call_whose_reservation_alone_exceeds_the_cap_is_refused(self):
        rig = Rig(self, cap="0.0001")
        status, _, _ = rig.chat(chat_req(max_tokens=100000))
        self.assertEqual(status, 429)
        self.assertEqual(rig.openai.count, 0)

    def test_reservation_formula_and_output_bound_rules(self):
        payload = chat_req(max_tokens=1000)
        rig = Rig(self)
        rig.chat(payload)
        self.assertEqual(Decimal(rig.records()[0]["reserve"]), expect_reserve(len(encoded(payload)), "0.15", "0.60", 1000))
        # n choices multiply the output bound; the legacy and the new name both count; no limit uses the default
        n3 = chat_req(max_tokens=1000, n=3)
        rig.chat(n3)
        self.assertEqual(Decimal(rig.records()[1]["reserve"]), expect_reserve(len(encoded(n3)), "0.15", "0.60", 3000))
        no_limit = {"model": "fake-small", "messages": [{"role": "user", "content": "x"}]}
        rig.chat(no_limit)
        self.assertEqual(Decimal(rig.records()[2]["reserve"]), expect_reserve(len(encoded(no_limit)), "0.15", "0.60", 1024))
        both = chat_req(max_tokens=10, max_completion_tokens=500)
        rig.chat(both)
        self.assertEqual(Decimal(rig.records()[3]["reserve"]), expect_reserve(len(encoded(both)), "0.15", "0.60", 500))
        emb = {"model": "fake-embed", "input": "text"}
        rig.post("/v1/embeddings", emb)
        self.assertEqual(Decimal(rig.records()[4]["reserve"]), expect_reserve(len(encoded(emb)), "0.02", "0", 0))
        claude = claude_req(max_tokens=2000)
        rig.messages(claude)
        self.assertEqual(Decimal(rig.records()[5]["reserve"]), expect_reserve(len(encoded(claude)), "1.25", "5.00", 2000))

    def test_a_cost_above_the_reservation_is_recorded_truthfully_and_flagged(self):
        rig = Rig(self, openai=FakeUpstream(answer(openai_chat_body(prompt=1234567, completion=7654321))))
        rig.chat()
        (rec,) = rig.records()
        self.assertEqual(rec["cost"], "4.77777765")
        self.assertIs(rec["reserve_exceeded"], True)
        self.assertGreater(Decimal(rec["cost"]), Decimal(rec["reserve"]))

    def test_bad_output_limits_are_rejected_before_any_forwarding(self):
        rig = Rig(self)
        for bad in ({"max_tokens": "100"}, {"max_tokens": 0}, {"max_tokens": True}, {"n": 0}, {"n": 500}):
            status, _, body = rig.chat(chat_req(**bad))
            self.assertEqual(status, 400, bad)
            self.assertIn("gateway_bad_request", body.decode())
        self.assertEqual(rig.openai.count, 0)


# --------------------------------------------------------------------------- 3. upstream failures count zero


class VoidedTests(unittest.TestCase):
    def check_voided(self, rig, status_expected):
        (rec,) = rig.records()
        self.assertIs(rec["voided"], True)
        self.assertEqual(rec["cost"], "0")
        self.assertEqual(rec["http_status"], status_expected)
        self.assertIsNone(rec["input_tokens"])
        self.assertIs(rec["usage_missing"], False)
        self.assertIsNone(rec["refusal"])
        summary = rig.summary()
        self.assertEqual((summary["spent"], summary["voided"], summary["open_reservations"]), ("0", 1, "0"))
        self.assertEqual(rig.gw.ledger.open, 0)
        self.assertEqual(rig.gw.ledger.spent, 0)

    def test_upstream_401_is_passed_through_and_counts_zero(self):
        error = {"error": {"message": "Incorrect API key", "type": "invalid_request_error"}}
        rig = Rig(self, openai=FakeUpstream(lambda req, h: send_json(h, 401, error)))
        status, _, body = rig.chat()
        self.assertEqual((status, json.loads(body)), (401, error))
        self.check_voided(rig, 401)

    def test_upstream_500_is_passed_through_and_counts_zero(self):
        rig = Rig(self, anthropic=FakeUpstream(lambda req, h: send_json(h, 500, {"type": "error", "error": {"type": "api_error"}})))
        status, _, body = rig.messages()
        self.assertEqual((status, json.loads(body)["error"]["type"]), (500, "api_error"))
        self.check_voided(rig, 500)

    def test_upstream_429_rate_limit_counts_zero_and_keeps_its_headers(self):
        rig = Rig(self, openai=FakeUpstream(lambda req, h: send_json(h, 429, {"error": {"type": "rate_limit"}},
                                                                    headers=[("Retry-After", "7")])))
        status, headers, _ = rig.chat()
        self.assertEqual((status, headers.get("Retry-After")), (429, "7"))
        self.check_voided(rig, 429)

    def test_closed_connection_counts_zero(self):
        rig = Rig(self, openai=FakeUpstream(lambda req, h: hang_up(h)))
        status, _, body = rig.chat()
        self.assertEqual(status, 502)
        self.assertIn("gateway_upstream_unreachable", body.decode())
        self.check_voided(rig, 502)

    def test_connection_refused_counts_zero(self):
        rig = Rig(self)
        rig.openai.close()  # nothing listens on the upstream port any more
        status, _, _ = rig.chat()
        self.assertEqual(status, 502)
        self.check_voided(rig, 502)

    def test_timeout_counts_zero(self):
        upstream = FakeUpstream(lambda req, h: req_wait(h))

        def req_wait(h):
            upstream.release.wait(5)

        rig = Rig(self, openai=upstream, gateway_extra="upstream_timeout_s = 0.4")
        started = time.monotonic()
        status, _, body = rig.chat()
        self.assertLess(time.monotonic() - started, 4)
        self.assertEqual(status, 504)
        self.assertIn("gateway_upstream_timeout", body.decode())
        self.check_voided(rig, 504)

    def test_a_voided_call_frees_its_reservation_for_the_next_call(self):
        payload = chat_req()
        reserve = expect_reserve(len(encoded(payload)), "0.15", "0.60", 1000)
        answers = [lambda req, h: send_json(h, 500, {"error": "boom"}), answer(openai_chat_body(100, 50))]
        rig = Rig(self, cap=format(reserve, "f"), openai=FakeUpstream(lambda req, h: answers[req["n"] - 1](req, h)))
        self.assertEqual(rig.chat(payload)[0], 500)
        self.assertEqual(rig.chat(payload)[0], 200, "the failed call must not keep eating the cap")


# --------------------------------------------------------------------------- 4. concurrency


class SlowLedger(mg.Ledger):
    """Yields to other threads between the cap check and the reservation, the one place a missing lock would bite.

    CPython only switches threads at call boundaries, so the plain check-then-add rarely interleaves by luck;
    this forces it. With the lock held the pause is harmless; without it every caller sees the same free room.
    """

    pause = 0.02

    def _committed(self):
        value = super()._committed()  # read the room first, then let every other thread read the same room
        time.sleep(self.pause)
        return value


class ConcurrencyTests(unittest.TestCase):
    def test_ledger_never_passes_the_cap_under_a_hammer(self):
        reserve = Decimal("1")
        ledger = SlowLedger(cap=Decimal("5.5"))
        errors = []
        start = threading.Barrier(16)

        def worker():
            start.wait()  # every thread meets the first check together
            for _ in range(2):
                if ledger.try_reserve(reserve):
                    time.sleep(0.05)  # hold the reservation while the other threads are still checking
                    ledger.settle(reserve, Decimal(0))

        threads = [threading.Thread(target=worker) for _ in range(16)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(errors, [])
        self.assertLessEqual(ledger.peak, Decimal("5.5"), "spend plus open reservations passed the cap")
        self.assertEqual(ledger.open, 0, "a reservation was lost or double-counted")
        self.assertEqual(ledger.spent, 0)

    def test_sixty_concurrent_calls_against_a_cap_that_fits_twenty(self):
        payload = chat_req()
        reserve = expect_reserve(len(encoded(payload)), "0.15", "0.60", 1000)
        cap = reserve * Decimal("20.5")
        refused_needed = 40
        rig_box = {}

        def responder(req, h):
            # hold every admitted call in flight until the other 40 have been refused
            end = time.monotonic() + 15
            while rig_box["rig"].gw.totals.refused < refused_needed and time.monotonic() < end:
                time.sleep(0.01)
            send_json(h, 200, openai_chat_body(100, 50))

        rig = Rig(self, cap=format(cap, "f"), openai=FakeUpstream(responder))
        rig.gw.ledger = SlowLedger(cap)
        rig_box["rig"] = rig
        statuses = []
        lock = threading.Lock()

        def client():
            status, _, _ = rig.chat(payload)
            with lock:
                statuses.append(status)

        threads = [threading.Thread(target=client) for _ in range(60)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(60)
        records = rig.wait_records(60)
        refused = [r for r in records if r["refusal"] == "gateway_budget_exceeded"]
        forwarded = rig.openai.count
        self.assertEqual(len(statuses), 60)
        self.assertEqual(forwarded + len(refused), 60, "every call was either forwarded or refused, none lost")
        self.assertEqual(statuses.count(429), len(refused))
        self.assertEqual(forwarded, 20)
        self.assertEqual(len(refused), 40)
        spent = sum(Decimal(r["cost"]) for r in records)
        self.assertEqual(spent, Decimal("0.0009"))  # 20 x 0.000045
        self.assertLessEqual(spent, cap)
        self.assertLessEqual(rig.gw.ledger.peak, cap, "spend plus open reservations passed the cap")
        self.assertEqual(rig.gw.ledger.peak, reserve * 20)
        self.assertEqual(rig.gw.ledger.open, 0)

    def test_log_lines_from_concurrent_calls_do_not_interleave(self):
        rig = Rig(self)
        threads = [threading.Thread(target=rig.chat) for _ in range(30)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(30)
        lines = rig.log_path.read_text().splitlines()
        self.assertEqual(len(lines), 30)
        for line in lines:
            json.loads(line)


# --------------------------------------------------------------------------- 5. the key stays secret


class KeySecrecyTests(unittest.TestCase):
    def echo_headers_500(self, req, h):
        send_json(h, 500, {"error": "failed", "you_sent": req["headers"]},
                  headers=[("X-Echo-Authorization", req["headers"].get("authorization", ""))])

    def test_the_real_key_is_sent_upstream_and_the_clients_credentials_are_not(self):
        rig = Rig(self)
        rig.chat(headers={"authorization": "Bearer lowercase-" + DUMMY_KEY})
        rig.messages()
        sent_openai, sent_anthropic = rig.openai.requests[0]["headers"], rig.anthropic.requests[0]["headers"]
        self.assertEqual(sent_openai["authorization"], "Bearer " + REAL_OPENAI_KEY)
        self.assertEqual(sent_anthropic["x-api-key"], REAL_ANTHROPIC_KEY)
        for headers in (sent_openai, sent_anthropic):
            self.assertNotIn(DUMMY_KEY, json.dumps(headers))
        self.assertNotIn("x-api-key", sent_openai)
        self.assertNotIn("authorization", sent_anthropic)

    def test_the_key_is_in_no_file_no_summary_and_no_error_body_even_when_the_upstream_echoes_it(self):
        rig = Rig(self, openai=FakeUpstream(self.echo_headers_500), gateway_extra="log_bodies = true")
        captured_out, captured_err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(captured_out), contextlib.redirect_stderr(captured_err):
            status, headers, body = rig.chat()
            summary_text = json.dumps(rig.summary())
        self.assertEqual(status, 500)
        self.assertNotIn(REAL_OPENAI_KEY.encode(), body)
        self.assertIn(b"[redacted]", body, "the echoed key should be replaced, and the rest of the body passed through")
        self.assertIn(b"you_sent", body)
        self.assertNotIn(REAL_OPENAI_KEY, json.dumps(headers))
        self.assertEqual(headers.get("X-Echo-Authorization"), "Bearer [redacted]")
        self.assertNotIn(REAL_OPENAI_KEY, summary_text)
        self.assertNotIn(REAL_OPENAI_KEY, captured_out.getvalue() + captured_err.getvalue())
        files = [p for p in rig.dir.iterdir() if p.is_file()]
        self.assertTrue(any(".bodies" in p.name for p in files), "log_bodies = true should write a body log")
        self.assertTrue(any("manifest" in p.name for p in files))
        for path in files:
            data = path.read_bytes()
            for secret in (REAL_OPENAI_KEY, REAL_ANTHROPIC_KEY, DUMMY_KEY):
                self.assertNotIn(secret.encode(), data, f"{secret[:12]}... found in {path.name}")
        self.assertNotIn(REAL_OPENAI_KEY, repr(rig.cfg))
        self.assertNotIn(REAL_OPENAI_KEY, repr(rig.gw.cfg.upstreams["fake-openai"].key))

    def test_a_key_echoed_in_a_successful_body_is_replaced_too_and_usage_still_counted(self):
        body = openai_chat_body(100, 50)
        body["choices"][0]["message"]["content"] = "key is " + REAL_OPENAI_KEY
        rig = Rig(self, openai=FakeUpstream(answer(body)))
        status, _, received = rig.chat()
        self.assertEqual(status, 200)
        self.assertNotIn(REAL_OPENAI_KEY.encode(), received)
        self.assertEqual(rig.records()[0]["cost"], "0.000045")

    def test_bodies_are_not_logged_unless_asked(self):
        rig = Rig(self)
        rig.chat()
        everything = b"".join(p.read_bytes() for p in rig.dir.iterdir() if p.is_file())
        self.assertNotIn(PROMPT_SENTINEL.encode(), everything)
        self.assertFalse(any(".bodies" in p.name for p in rig.dir.iterdir()))

    def test_bodies_are_logged_to_a_separate_file_when_asked(self):
        rig = Rig(self, gateway_extra="log_bodies = true")
        rig.chat()
        self.assertNotIn(PROMPT_SENTINEL, rig.log_path.read_text())
        bodies = (rig.dir / "meter.jsonl.bodies.jsonl").read_text()
        self.assertIn(PROMPT_SENTINEL, bodies)
        self.assertEqual(json.loads(bodies)["call_id"], rig.records()[0]["call_id"])

    def test_a_key_pasted_into_key_env_is_refused_without_printing_it(self):
        text = toml_config("x.jsonl", "http://127.0.0.1:1/v1", "http://127.0.0.1:1/v1").replace(
            'key_env = "FAKE_OPENAI_KEY"', f'key_env = "{REAL_OPENAI_KEY.replace("-", "")}"', 1)
        environ = dict(ENVIRON, SOMETHING=REAL_OPENAI_KEY.replace("-", ""))
        with self.assertRaises(mg.ConfigError) as ctx:
            mg.parse_config(text, environ)
        self.assertNotIn(REAL_OPENAI_KEY.replace("-", ""), str(ctx.exception))


# --------------------------------------------------------------------------- 6. loopback only


class FakePeerHandler(mg.Handler):
    def peer(self):
        return "192.0.2.7"  # a documentation address, not loopback


class LoopbackTests(unittest.TestCase):
    def test_is_loopback_function(self):
        for host in ("127.0.0.1", "127.9.9.9", "::1"):
            self.assertTrue(mg.is_loopback(host), host)
        for host in ("192.0.2.7", "10.0.0.5", "0.0.0.0", "::", "2001:db8::1", "::ffff:192.0.2.7", "", "localhost", "garbage"):
            self.assertFalse(mg.is_loopback(host), host)

    def test_host_header_must_name_this_machine(self):
        for value in ("127.0.0.1", "127.0.0.1:8089", "localhost", "LOCALHOST:80", "[::1]:8089", "127.5.5.5"):
            self.assertTrue(mg.host_allowed(value), value)
        for value in (None, "", "attacker.example", "attacker.example:8089", "127.0.0.1.attacker.example",
                      "192.0.2.7:8089", "[2001:db8::1]:80", "localhost.attacker.example"):
            self.assertFalse(mg.host_allowed(value), value)

    def test_a_rebound_host_name_is_refused_and_nothing_is_forwarded_or_logged(self):
        rig = Rig(self)
        for method, path in (("POST", "/v1/chat/completions"), ("GET", "/_meter/summary")):
            status, _, body = rig.request(method, path, encoded(chat_req()) if method == "POST" else None,
                                          {"Content-Type": "application/json", "Host": "attacker.example:8089"})
            self.assertEqual(status, 403, (method, path))
            self.assertIn("gateway_forbidden_host", body.decode())
        self.assertEqual((rig.openai.count, rig.records()), (0, []))
        self.assertEqual(rig.request("POST", "/v1/chat/completions", encoded(chat_req()),
                                     {"Content-Type": "application/json", "Host": "localhost:9"})[0], 200)

    def test_only_json_content_type_is_accepted_so_a_web_page_cannot_post_across_origins(self):
        rig = Rig(self)
        for media in ("text/plain", "application/x-www-form-urlencoded", "multipart/form-data"):
            status, _, body = rig.request("POST", "/v1/chat/completions", encoded(chat_req()), {"Content-Type": media})
            self.assertEqual(status, 415, media)
            self.assertIn("gateway_unsupported_media_type", body.decode())
        self.assertEqual(rig.request("POST", "/v1/chat/completions", encoded(chat_req()), {})[0], 415)
        self.assertEqual(rig.openai.count, 0)
        for media in ("application/json", "Application/JSON; charset=utf-8"):
            status, _, _ = rig.request("POST", "/v1/chat/completions", encoded(chat_req()), {"Content-Type": media})
            self.assertEqual(status, 200, media)

    def test_a_non_loopback_peer_is_refused_and_nothing_is_forwarded_or_logged(self):
        rig = Rig(self, handler=FakePeerHandler)
        for method, path in (("POST", "/v1/chat/completions"), ("GET", "/_meter/summary"), ("POST", "/unknown")):
            status, _, body = rig.request(method, path, encoded(chat_req()) if method == "POST" else None,
                                          {"Content-Type": "application/json"})
            self.assertEqual(status, 403, (method, path))
            self.assertIn("gateway_forbidden_peer", body.decode())
        self.assertEqual(rig.openai.count, 0)
        self.assertEqual(rig.records(), [])

    def test_a_loopback_peer_is_served(self):
        self.assertEqual(Rig(self).chat()[0], 200)

    def test_the_server_binds_127_0_0_1_only(self):
        rig = Rig(self)
        self.assertEqual(rig.server.server_address[0], "127.0.0.1")
        self.assertEqual(mg.BIND_HOST, "127.0.0.1")
        with self.assertRaises(TypeError):
            mg.GatewayServer(rig.gw, 0, mg.Handler, "0.0.0.0")  # type: ignore[call-arg]

    def test_unknown_routes_are_404_and_not_logged(self):
        rig = Rig(self)
        for method, path in (("POST", "/v1/unknown"), ("GET", "/v1/chat/completions"), ("POST", "/"),
                             ("POST", "/v1/messages/count_tokens"), ("DELETE", "/_meter/summary")):
            status, _, body = rig.request(method, path, b"{}" if method == "POST" else None, {"Content-Type": "application/json"})
            self.assertEqual(status, 404, (method, path))
        self.assertEqual(rig.records(), [])
        self.assertEqual(rig.openai.count + rig.anthropic.count, 0)


# --------------------------------------------------------------------------- 7. fail closed


class FailClosedTests(unittest.TestCase):
    def good(self, **kwargs) -> str:
        return toml_config("meter.jsonl", "https://api.example.invalid/v1", "https://api.example.invalid/v1", **kwargs)

    def assertRejected(self, text, fragment="", environ=ENVIRON):
        with self.assertRaises(mg.ConfigError) as ctx:
            mg.parse_config(text, environ)
        self.assertIn(fragment, str(ctx.exception))

    def test_a_model_with_no_price_is_refused_and_nothing_is_forwarded(self):
        rig = Rig(self)
        for payload in ({"model": "fake-unpriced", "messages": []}, {"messages": []}, {"model": 7}):
            status, _, body = rig.post("/v1/chat/completions", payload)
            self.assertEqual(status, 400)
            self.assertIn("gateway_model_not_priced", body.decode())
        self.assertEqual(rig.openai.count, 0)
        self.assertEqual({r["refusal"] for r in rig.records()}, {"gateway_model_not_priced"})
        self.assertTrue(all(r["cost"] == "0" for r in rig.records()))

    def test_a_model_routed_to_the_wrong_protocol_is_refused(self):
        rig = Rig(self)
        status, _, body = rig.post("/v1/chat/completions", claude_req())
        self.assertEqual(status, 400)
        self.assertIn("gateway_route_mismatch", body.decode())
        self.assertEqual(rig.openai.count + rig.anthropic.count, 0)

    def test_bad_json_and_non_object_bodies_are_refused(self):
        rig = Rig(self)
        self.assertEqual(rig.post("/v1/chat/completions", raw=b"{not json")[0], 400)
        self.assertEqual(rig.post("/v1/chat/completions", raw=b"[1, 2]")[0], 400)
        sock = socket.create_connection(("127.0.0.1", rig.port), timeout=10)
        sock.sendall(b"POST /v1/chat/completions HTTP/1.1\r\nHost: 127.0.0.1\r\nContent-Type: application/json\r\n\r\n")
        self.assertTrue(sock.recv(4096).startswith(b"HTTP/1.1 411"), "no Content-Length and no chunking: 411")
        sock.close()
        self.assertEqual(rig.openai.count, 0)

    def test_config_without_a_cap_does_not_start(self):
        text = self.good().replace("cap = 10\n", "")
        self.assertRejected(text, "cap is required")
        self.assertRejected(self.good(cap="0"), "greater than zero")
        self.assertRejected(self.good(cap="-1"), "greater than zero")
        self.assertRejected(self.good(cap='"ten"'), "decimal")

    def test_main_returns_2_and_starts_nothing_for_a_config_without_a_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "gw.toml"
            log = Path(tmp) / "meter.jsonl"
            path.write_text(toml_config(str(log), "http://127.0.0.1:1/v1", "http://127.0.0.1:1/v1").replace("cap = 10\n", ""))
            err = io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()), \
                    unittest.mock.patch.object(mg.GatewayServer, "serve_forever", side_effect=KeyboardInterrupt):
                code = mg.main(["--config", str(path)], ENVIRON)
            self.assertEqual(code, 2)
            self.assertIn("cap", err.getvalue())
            self.assertFalse(log.exists(), "a refused start must not create the log")

    def test_config_without_prices_does_not_start(self):
        text = self.good()
        self.assertRejected(text[: text.index('[models."fake-small"]')], "missing table [models]")
        self.assertRejected(text.replace("output_per_mtok = 0.60\n", "", 1), "output_per_mtok is required")
        self.assertRejected(text.replace("input_per_mtok = 0.15\n", "", 1), "input_per_mtok is required")
        self.assertRejected(text.replace('source_url = "https://example.invalid/pricing/fake-small"\n', "", 1), "source_url")
        self.assertRejected(text.replace('read_at = "20261102 10:00"', 'read_at = "yesterday"', 1), "read_at")
        self.assertRejected(text.replace("input_per_mtok = 0.15", "input_per_mtok = -0.15", 1), "at least zero")
        self.assertRejected(text.replace('upstream = "fake-openai"', 'upstream = "nowhere"', 1), "not configured")

    def test_an_unset_key_variable_stops_startup_unless_the_upstream_is_a_dry_run(self):
        self.assertRejected(self.good(), "not set", environ={})
        mg.parse_config(self.good(dry_run=True), {})  # a dry-run upstream needs no key
        with self.assertRaises(mg.ConfigError):
            mg.parse_config(self.good(), {"FAKE_OPENAI_KEY": REAL_OPENAI_KEY})  # the Anthropic one is still unset

    def test_a_malformed_key_is_refused_without_printing_it(self):
        for bad in (REAL_OPENAI_KEY + "\n", REAL_OPENAI_KEY + " " + REAL_ANTHROPIC_KEY, REAL_OPENAI_KEY * 2, "",
                    "caf\u00e9-key"):
            environ = dict(ENVIRON, FAKE_OPENAI_KEY=bad)
            with self.assertRaises(mg.ConfigError) as ctx:
                mg.parse_config(self.good(), environ)
            self.assertNotIn(REAL_OPENAI_KEY, str(ctx.exception))

    def test_typos_and_unsafe_settings_are_refused(self):
        self.assertRejected(self.good(gateway_extra="cap_usd = 5"), "unknown key")
        self.assertRejected(self.good().replace('protocol = "openai"', 'protocol = "gemini"', 1), "protocol")
        self.assertRejected(self.good().replace("https://api.example.invalid/v1", "http://api.example.invalid/v1", 1), "loopback")
        self.assertRejected(self.good(gateway_extra="log_bodies = true\nbody_log_file = \"meter.jsonl\""), "different from log_file")
        self.assertRejected("not [valid toml", "TOML")

    def test_an_existing_log_needs_resume_and_resume_restores_the_spend(self):
        rig = Rig(self, openai=FakeUpstream(answer(openai_chat_body(100, 50))))
        rig.chat()
        rig.gw.close()
        with self.assertRaises(mg.ConfigError):
            mg.Gateway(rig.cfg)
        again = mg.Gateway(rig.cfg, resume=True)
        self.addCleanup(again.close)
        self.assertEqual(again.ledger.spent, Decimal("0.000045"))
        self.assertEqual(again.summary()["calls"], 1)
        with tempfile.TemporaryDirectory() as tmp:
            fresh = mg.parse_config(rig.text.replace(str(rig.log_path), str(Path(tmp) / "new.jsonl")), ENVIRON)
            with self.assertRaises(mg.ConfigError):
                mg.Gateway(fresh, resume=True)  # nothing to resume


# --------------------------------------------------------------------------- 8. usage missing


class UsageMissingTests(unittest.TestCase):
    def check_whole_reservation(self, rig, payload, prices):
        (rec,) = rig.records()
        reserve = expect_reserve(len(encoded(payload)), *prices)
        self.assertIs(rec["usage_missing"], True)
        self.assertIs(rec["voided"], False)
        self.assertEqual(Decimal(rec["cost"]), reserve)
        self.assertEqual(rec["cost"], rec["reserve"])
        self.assertIsNone(rec["input_tokens"])
        self.assertEqual(rig.gw.ledger.spent, reserve)
        self.assertEqual(rig.gw.ledger.open, 0)
        self.assertEqual(rig.summary()["usage_missing"], 1)

    def test_200_without_a_usage_object(self):
        body = openai_chat_body()
        del body["usage"]
        rig = Rig(self, openai=FakeUpstream(answer(body)))
        payload = chat_req()
        self.assertEqual(rig.chat(payload)[0], 200)
        self.check_whole_reservation(rig, payload, ("0.15", "0.60", 1000))

    def test_200_with_unusable_usage_numbers(self):
        for bad in ({"prompt_tokens": "12", "completion_tokens": 5},
                    {"prompt_tokens": 12},
                    {"prompt_tokens": -1, "completion_tokens": 5},
                    {"prompt_tokens": 10, "completion_tokens": 5, "prompt_tokens_details": {"cached_tokens": 99}},
                    {"prompt_tokens": True, "completion_tokens": 5}):
            body = openai_chat_body()
            body["usage"] = bad
            rig = Rig(self, openai=FakeUpstream(answer(body)))
            rig.chat()
            self.assertIs(rig.records()[0]["usage_missing"], True, bad)

    def test_200_that_is_not_json(self):
        rig = Rig(self, openai=FakeUpstream(lambda req, h: send_sse(h, [b"plain text, not json"])))
        rig.chat(chat_req())
        self.assertIs(rig.records()[0]["usage_missing"], True)

    def test_openai_stream_without_a_usage_chunk(self):
        rig = Rig(self, openai=FakeUpstream(lambda req, h: send_sse(h, openai_sse(with_usage=False))))
        payload = chat_req(stream=True)
        self.assertEqual(rig.chat(payload)[0], 200)
        (rec,) = rig.records()
        self.assertIs(rec["usage_missing"], True)
        self.assertIs(rec["streamed"], True)
        self.assertEqual(rec["cost"], rec["reserve"])

    def test_anthropic_stream_cut_before_its_final_delta(self):
        rig = Rig(self, anthropic=FakeUpstream(lambda req, h: send_sse(h, anthropic_sse(with_delta=False))))
        rig.messages(claude_req(stream=True))
        (rec,) = rig.records()
        self.assertIs(rec["usage_missing"], True)
        self.assertEqual(rec["cost"], rec["reserve"])

    def test_anthropic_200_without_usage(self):
        body = anthropic_body()
        del body["usage"]
        rig = Rig(self, anthropic=FakeUpstream(answer(body)))
        payload = claude_req()
        rig.messages(payload)
        self.check_whole_reservation(rig, payload, ("1.25", "5.00", 1000))


# --------------------------------------------------------------------------- 9. money is exact


class MoneyTests(unittest.TestCase):
    PRICE = mg.Price(Decimal("0.15"), Decimal("0.60"), None, None, "https://example.invalid/p", "20261102 10:00")

    def test_prices_read_from_toml_are_exact_decimals(self):
        cfg = mg.parse_config(toml_config("m.jsonl", "https://x.example.invalid/v1", "https://x.example.invalid/v1"), ENVIRON)
        price = cfg.models["fake-small"].price
        self.assertIsInstance(price.input_per_mtok, Decimal)
        self.assertEqual(str(price.input_per_mtok), "0.15")
        self.assertEqual(str(price.output_per_mtok), "0.60")
        self.assertEqual(cfg.cap, Decimal(10))

    def test_cost_to_the_last_digit(self):
        usage = mg.Usage(1234567, 7654321, None, None)
        # 1234567 x 0.15 / 1e6 = 0.18518505 ; 7654321 x 0.60 / 1e6 = 4.5925926 ; sum 4.77777765
        self.assertEqual(mg.money_text(mg.cost_of(usage, self.PRICE)), "4.77777765")
        self.assertEqual(mg.money_text(mg.tokens_cost(1, Decimal("0.15"))), "0.00000015")
        self.assertEqual(mg.money_text(mg.cost_of(mg.Usage(0, 0, None, None), self.PRICE)), "0")

    def test_cost_through_the_gateway_and_in_the_summary(self):
        rig = Rig(self, openai=FakeUpstream(answer(openai_chat_body(prompt=1234567, completion=7654321))))
        rig.chat()
        self.assertEqual(rig.records()[0]["cost"], "4.77777765")
        self.assertEqual(rig.summary()["spent"], "4.77777765")
        self.assertEqual(rig.summary()["remaining"], "5.22222235")  # 10 - 4.77777765, no open reservations left

    def test_many_small_costs_add_up_without_float_drift(self):
        rig = Rig(self, openai=FakeUpstream(answer(openai_chat_body(prompt=1000, completion=0))))
        for _ in range(10):
            rig.chat(chat_req(model="fake-dime", max_tokens=10))
        self.assertEqual({r["cost"] for r in rig.records()}, {"0.1"})
        self.assertEqual(rig.summary()["spent"], "1")  # 0.1 added ten times as floats is 0.9999999999999999
        self.assertEqual(rig.gw.ledger.spent, Decimal(1))

    def test_cached_price_of_zero_is_a_price_not_a_missing_one(self):
        price = mg.Price(Decimal("1"), Decimal("1"), Decimal("0"), None, "https://example.invalid/p", "20261102 10:00")
        self.assertEqual(mg.money_text(mg.cost_of(mg.Usage(1000000, 0, 1000000, None), price)), "0")


# --------------------------------------------------------------------------- summary and command line


class SummaryTests(unittest.TestCase):
    def test_live_summary_and_log_summary_agree(self):
        answers = [answer(openai_chat_body(100, 50, cached=20)), lambda req, h: send_json(h, 500, {"e": 1}),
                   lambda req, h: send_json(h, 200, {"no": "usage"})]
        rig = Rig(self, openai=FakeUpstream(lambda req, h: answers[req["n"] - 1](req, h)))
        rig.chat()
        rig.chat()
        rig.chat()
        rig.chat(chat_req(model="not-priced"))
        live = rig.summary()
        self.assertEqual((live["requests"], live["calls"], live["ok"], live["voided"], live["usage_missing"], live["refused"]),
                         (4, 3, 1, 1, 1, 1))
        self.assertEqual((live["input_tokens"], live["output_tokens"], live["cached_input_tokens"]), (100, 50, 20))
        self.assertEqual(live["cap"], "10")
        self.assertEqual(live["currency"], "FAKE-USD")
        self.assertEqual(live["by_model"]["fake-small"]["calls"], 3)
        self.assertEqual(mg.summary_from_log(str(rig.log_path)), live)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(mg.main(["--summary", str(rig.log_path)]), 0)
        self.assertEqual(json.loads(out.getvalue()), live)

    def test_the_manifest_records_prices_sources_and_the_names_of_key_variables(self):
        rig = Rig(self)
        manifest = json.loads(Path(rig.gw.manifest_path).read_text())
        model = manifest["models"]["fake-small"]
        self.assertEqual((model["source_url"], model["read_at"], model["input_per_mtok"], model["output_per_mtok"]),
                         ("https://example.invalid/pricing/fake-small", "20261102 10:00", "0.15", "0.6"))
        self.assertEqual(manifest["upstreams"]["fake-openai"]["key_env"], "FAKE_OPENAI_KEY")
        self.assertEqual((manifest["cap"], manifest["currency"]), ("10", "FAKE-USD"))
        self.assertEqual(manifest["config_sha256"], hashlib.sha256(rig.text.encode()).hexdigest())

    def test_summary_is_not_reachable_with_post_and_has_no_secrets(self):
        rig = Rig(self)
        self.assertEqual(rig.request("POST", "/_meter/summary", b"{}", {"Content-Type": "application/json"})[0], 404)


# --------------------------------------------------------------------------- robustness


class BrokenWriter:
    def write(self, obj):
        raise OSError("disk full")

    def close(self):
        pass


class RobustnessTests(unittest.TestCase):
    def test_a_key_echoed_inside_a_stream_stays_out_of_the_body_log(self):
        # A 2xx stream is passed through byte for byte (documented), but the body log must never hold the key.
        events = openai_sse()
        events.insert(0, sse_data({"choices": [{"delta": {"content": "key is " + REAL_OPENAI_KEY}}]}))
        rig = Rig(self, openai=FakeUpstream(lambda req, h: send_sse(h, events)), gateway_extra="log_bodies = true")
        rig.chat(chat_req(stream=True))
        bodies = (rig.dir / "meter.jsonl.bodies.jsonl").read_text()
        self.assertNotIn(REAL_OPENAI_KEY, bodies)
        self.assertIn("[redacted]", bodies)

    def test_when_the_log_cannot_be_written_the_gateway_stops_accepting_calls(self):
        rig = Rig(self)
        self.addCleanup(rig.gw.log.close)
        rig.gw.log = BrokenWriter()
        self.assertEqual(rig.chat()[0], 200)  # this call already happened upstream; it is answered
        self.assertEqual(rig.openai.count, 1)
        status, _, body = rig.chat()
        self.assertEqual(status, 503)
        self.assertIn("gateway_log_failure", body.decode())
        self.assertEqual(rig.openai.count, 1, "nothing may be forwarded once spending can no longer be recorded")

    def test_an_internal_error_after_forwarding_counts_the_whole_reservation(self):
        rig = Rig(self)
        with unittest.mock.patch.object(mg, "cost_of", side_effect=RuntimeError("bug")):
            status, _, _ = rig.chat()
        self.assertEqual(status, 500)
        (rec,) = rig.records()
        self.assertEqual(rig.openai.count, 1)
        self.assertIs(rec["usage_missing"], True)
        self.assertEqual(rec["cost"], rec["reserve"])
        self.assertEqual(rec["error"], "internal_error:RuntimeError")
        self.assertEqual((rig.gw.ledger.open, rig.gw.ledger.spent), (0, Decimal(rec["reserve"])))

    def test_an_internal_error_before_forwarding_counts_nothing(self):
        rig = Rig(self)
        with unittest.mock.patch.object(mg, "reserve_amount", side_effect=RuntimeError("bug")):
            status, _, _ = rig.chat()
        self.assertEqual(status, 500)
        (rec,) = rig.records()
        self.assertEqual(rig.openai.count, 0)
        self.assertEqual((rec["refusal"], rec["cost"]), ("gateway_internal_error", "0"))
        self.assertEqual((rig.gw.ledger.open, rig.gw.ledger.spent), (0, 0))

    def test_an_oversize_body_is_refused_before_it_is_read(self):
        rig = Rig(self)
        sock = socket.create_connection(("127.0.0.1", rig.port), timeout=10)
        sock.sendall(b"POST /v1/chat/completions HTTP/1.1\r\nHost: 127.0.0.1\r\nContent-Type: application/json\r\n"
                     b"Content-Length: 99999999999\r\n\r\n")
        self.assertTrue(sock.recv(4096).startswith(b"HTTP/1.1 413"))
        sock.close()
        self.assertEqual(rig.openai.count, 0)


# --------------------------------------------------------------------------- chunked upstream bodies (the seam)


class ChunkedUpstreamTests(unittest.TestCase):
    """Real providers answer with Transfer-Encoding: chunked; the other fakes use Content-Length or close."""

    def test_chunked_openai_stream_split_at_odd_places(self):
        events = b"".join(openai_sse(prompt=700, completion=40))
        rig = Rig(self, openai=FakeUpstream(lambda req, h: send_chunked(h, 200, "text/event-stream", pieces(events, 7))))
        status, _, body = rig.chat(chat_req(stream=True))
        self.assertEqual((status, body), (200, events))
        (rec,) = rig.records()
        self.assertEqual((rec["input_tokens"], rec["output_tokens"], rec["cost"]), (700, 40, "0.000129"))
        self.assertIs(rec["streamed"], True)

    def test_chunked_anthropic_json_body(self):
        data = json.dumps(anthropic_body(inp=321, out=77)).encode()
        rig = Rig(self, anthropic=FakeUpstream(lambda req, h: send_chunked(h, 200, "application/json", pieces(data, 5))))
        status, _, body = rig.messages()
        self.assertEqual((status, body), (200, data))
        self.assertEqual(rig.records()[0]["cost"], "0.000706")

    def test_a_stream_cut_after_its_usage_chunk_still_counts_its_usage(self):
        events = b"".join(openai_sse(prompt=700, completion=40)[:3])  # text, text, usage; no [DONE], no final chunk
        rig = Rig(self, openai=FakeUpstream(lambda req, h: send_chunked(h, 200, "text/event-stream",
                                                                      pieces(events, 40), finish=False)))
        rig.chat(chat_req(stream=True))
        (rec,) = rig.records()
        self.assertEqual((rec["input_tokens"], rec["output_tokens"]), (700, 40))
        self.assertIs(rec["usage_missing"], False)
        self.assertEqual(rec["error"], "stream_interrupted")

    def test_a_stream_cut_before_its_usage_chunk_counts_the_whole_reservation(self):
        events = b"".join(openai_sse()[:2])  # two text chunks only
        rig = Rig(self, openai=FakeUpstream(lambda req, h: send_chunked(h, 200, "text/event-stream",
                                                                      pieces(events, 40), finish=False)))
        rig.chat(chat_req(stream=True))
        (rec,) = rig.records()
        self.assertIs(rec["usage_missing"], True)
        self.assertEqual(rec["cost"], rec["reserve"])
        self.assertEqual(rec["error"], "stream_interrupted")


# --------------------------------------------------------------------------- request defaults


LOCAL_MODELS = """
[models."fake-local"]
upstream = "fake-openai"
input_per_mtok = 1
output_per_mtok = 2
source_url = "https://example.invalid/pricing/fake-local"
read_at = "20261102 10:00"

[models."fake-local".request_defaults]
reasoning_effort = "none"
seed = 7

[models."fake-claude-local"]
upstream = "fake-anthropic"
input_per_mtok = 0
output_per_mtok = 0
source_url = "https://example.invalid/pricing/fake-claude-local"
read_at = "20261102 10:00"

[models."fake-claude-local".request_defaults]
thinking = { type = "disabled" }
"""


class RequestDefaultsTests(unittest.TestCase):
    def rig(self, **kwargs):
        return Rig(self, dry_run=True, models_extra=LOCAL_MODELS, **kwargs)

    def test_a_default_fills_a_missing_field_and_the_call_record_names_it(self):
        rig = self.rig()
        client = chat_req(model="fake-local")
        status, _, _ = rig.chat(client)
        self.assertEqual(status, 200)
        forwarded = json.loads(rig.openai.requests[0]["body"])
        self.assertEqual(forwarded["reasoning_effort"], "none")
        self.assertEqual(forwarded["seed"], 7)
        self.assertEqual({k: v for k, v in forwarded.items() if k not in ("reasoning_effort", "seed")}, client)
        (rec,) = rig.records()
        self.assertEqual(rec["request_defaults_applied"], ["reasoning_effort", "seed"])
        # the hash and the size are of what the client sent, and the reservation is of what was forwarded
        self.assertEqual(rec["request_sha256"], hashlib.sha256(encoded(client)).hexdigest())
        self.assertEqual(rec["bytes_in"], len(encoded(client)))
        self.assertEqual(Decimal(rec["reserve"]), expect_reserve(len(rig.openai.requests[0]["body"]), "1", "2", 1000))

    def test_a_model_without_defaults_is_forwarded_byte_for_byte_and_its_record_says_none(self):
        rig = self.rig()
        client = encoded(chat_req())
        rig.chat(raw=client)
        self.assertEqual(rig.openai.requests[0]["body"], client)
        self.assertEqual(rig.records()[0]["request_defaults_applied"], [])

    def test_a_field_the_client_sent_wins_and_only_the_missing_ones_are_added(self):
        rig = self.rig()
        rig.chat(chat_req(model="fake-local", reasoning_effort="high"))
        rig.chat(chat_req(model="fake-local", reasoning_effort="low", seed=1))
        rig.chat(chat_req(model="fake-local", seed=0))
        first, second, third = (json.loads(r["body"]) for r in rig.openai.requests)
        self.assertEqual((first["reasoning_effort"], first["seed"]), ("high", 7))
        self.assertEqual((second["reasoning_effort"], second["seed"]), ("low", 1))
        self.assertEqual((third["reasoning_effort"], third["seed"]), ("none", 0))  # a falsy value the client sent still wins
        self.assertEqual([r["request_defaults_applied"] for r in rig.wait_records(3)],
                         [["seed"], [], ["reasoning_effort"]])

    def test_defaults_and_the_injected_stream_options_both_reach_the_upstream(self):
        events = openai_sse(prompt=700, completion=40)
        rig = self.rig(openai=FakeUpstream(lambda req, h: send_sse(h, events)))
        status, _, body = rig.chat(chat_req(model="fake-local", stream=True))
        self.assertEqual(status, 200)
        self.assertEqual(body, b"".join(events))
        forwarded = json.loads(rig.openai.requests[0]["body"])
        self.assertEqual(forwarded["stream_options"], {"include_usage": True})
        self.assertEqual((forwarded["reasoning_effort"], forwarded["seed"]), ("none", 7))
        self.assertEqual(rig.records()[0]["request_defaults_applied"], ["reasoning_effort", "seed"])

    def test_a_nested_default_works_on_the_anthropic_protocol(self):
        rig = self.rig()
        status, _, _ = rig.messages(claude_req(model="fake-claude-local"))
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(rig.anthropic.requests[0]["body"])["thinking"], {"type": "disabled"})
        self.assertEqual(rig.records()[0]["request_defaults_applied"], ["thinking"])

    def test_the_body_log_keeps_what_the_client_sent_and_the_manifest_keeps_the_defaults(self):
        rig = self.rig(gateway_extra="log_bodies = true")
        client = chat_req(model="fake-local")
        rig.chat(client)
        (entry,) = (json.loads(line) for line in Path(rig.cfg.body_log_file).read_text().splitlines())
        self.assertEqual(json.loads(entry["request"]), client)
        manifest = json.loads(Path(rig.gw.manifest_path).read_text())
        self.assertEqual(manifest["models"]["fake-local"]["request_defaults"], {"reasoning_effort": "none", "seed": 7})
        self.assertEqual(manifest["models"]["fake-small"]["request_defaults"], {})

    def test_a_refused_call_records_no_defaults(self):
        rig = self.rig()
        rig.chat({"model": "fake-unpriced", "messages": []})
        self.assertEqual(rig.records()[0]["request_defaults_applied"], [])

    @staticmethod
    def local_model(extra: str) -> str:
        return ("\n[models.\"fake-local\"]\nupstream = \"fake-openai\"\ninput_per_mtok = 1\noutput_per_mtok = 2\n"
                "source_url = \"https://example.invalid/pricing/fake-local\"\nread_at = \"20261102 10:00\"\n" + extra)

    def parse(self, models_extra: str, *, dry_run: bool):
        text = toml_config("m.jsonl", "https://api.example.invalid/v1", "https://api.example.invalid/v1", dry_run=dry_run,
                           models_extra=models_extra)
        return mg.parse_config(text, ENVIRON)

    def test_defaults_are_refused_on_a_paid_upstream_and_an_empty_table_is_not(self):
        with_defaults = self.local_model("\n[models.\"fake-local\".request_defaults]\nseed = 7\n")
        with self.assertRaisesRegex(mg.ConfigError, "only on a dry_run upstream"):
            self.parse(with_defaults, dry_run=False)
        self.assertEqual(self.parse(with_defaults, dry_run=True).models["fake-local"].request_defaults, {"seed": 7})
        empty = self.local_model("\n[models.\"fake-local\".request_defaults]\n")
        self.assertEqual(self.parse(empty, dry_run=False).models["fake-local"].request_defaults, {})

    def test_defaults_may_not_set_a_field_that_decides_the_request_or_its_reservation(self):
        self.assertEqual(mg.PROTECTED_REQUEST_FIELDS, {"model", "messages", "input", "stream", "stream_options", "n",
                                                       "max_tokens", "max_completion_tokens"})
        for name in sorted(mg.PROTECTED_REQUEST_FIELDS):
            text = self.local_model(f"\n[models.\"fake-local\".request_defaults]\n{name} = 5\n")
            with self.assertRaisesRegex(mg.ConfigError, f"may not set.*{name}"):
                self.parse(text, dry_run=True)

    def test_defaults_must_be_a_table_of_json_values(self):
        with self.assertRaisesRegex(mg.ConfigError, "must be a table"):
            self.parse(self.local_model("request_defaults = 3\n"), dry_run=True)
        dated = self.local_model("\n[models.\"fake-local\".request_defaults]\nwhen = 2026-11-02T10:00:00Z\n")
        with self.assertRaisesRegex(mg.ConfigError, "JSON values"):
            self.parse(dated, dry_run=True)


# --------------------------------------------------------------------------- the documentation stays true


class DocumentationTests(unittest.TestCase):
    DOC = (Path(__file__).resolve().parent / "metering_gateway.md").read_text()

    def test_the_config_example_parses(self):
        blocks = re.findall(r"```toml\n(.*?)```", self.DOC, re.S)
        self.assertEqual(len(blocks), 1)
        cfg = mg.parse_config(blocks[0], {"GATEWAY_OPENAI_KEY": REAL_OPENAI_KEY, "GATEWAY_ANTHROPIC_KEY": REAL_ANTHROPIC_KEY})
        self.assertEqual(set(cfg.models), {"fake-small", "fake-embed", "fake-claude"})
        self.assertEqual(cfg.cap, Decimal("2.5"))
        self.assertEqual(cfg.currency, "FAKE-USD")

    def test_every_log_field_is_documented_and_nothing_else(self):
        section = self.DOC.split("## The log", 1)[1].split("Other files", 1)[0]
        documented = set()
        for line in section.splitlines():
            if line.startswith("| `"):
                documented |= set(re.findall(r"`([a-z_0-9]+)`", line.split("|")[1]))
        real = set(mg.Call("id", 0.0, "ts", "/v1/x").record("FAKE-USD"))
        self.assertEqual(documented, real)

    def test_every_gateway_error_code_is_documented(self):
        source = (Path(__file__).resolve().parent / "metering_gateway.py").read_text()
        codes = set(re.findall(r'"(gateway_[a-z_]+)"', source))
        missing = sorted(code for code in codes if code not in self.DOC)
        self.assertEqual(missing, [], "error codes the documentation does not name")


if __name__ == "__main__":
    unittest.main()
