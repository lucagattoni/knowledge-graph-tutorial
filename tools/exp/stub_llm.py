"""A stub OpenAI-compatible model server for rehearsals. Loopback only, no key, no network beyond 127.0.0.1.

A rehearsal points a third-party builder at this server instead of a model. The server records every call and
answers with whatever a *responder* function returns, so the builder's structure (how many calls per document, how
large each prompt) can be counted without spending anything.

What it can and cannot show. Prompt sizes and the number of calls that do not depend on what the model says are
exact for the given input. Anything driven by the model's output (gleaning loops, retries, summaries that trigger
only when descriptions grow) depends on the responder you supply, so a count taken here is a count *for that
responder's answers*. Token counts are made with tiktoken's cl100k_base when it is importable and with
characters/4 otherwise (see `Stub.tokenizer`); neither is any provider's own tokenizer.

    from stub_llm import Stub
    def responder(call):               # chat: return a str, or a dict used as the assistant message
        return "..."
    with Stub(responder) as stub:
        base_url = stub.base_url       # e.g. http://127.0.0.1:PORT/v1
        ...                            # run the builder with OPENAI_BASE_URL=base_url and OPENAI_API_KEY=dummy
        print(stub.summary())

Embeddings are answered with deterministic pseudo-vectors (a function of the input text and `dimensions`).
Standard library only; tiktoken is optional.
"""

from __future__ import annotations

import hashlib
import json
import math
import struct
import threading
import time
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable


def make_counter() -> tuple[str, Callable[[str], int]]:
    """(tokenizer name, count function)."""
    try:
        import tiktoken

        enc = tiktoken.get_encoding("cl100k_base")
        return "tiktoken:cl100k_base", lambda s: len(enc.encode(s, disallowed_special=()))
    except Exception:  # noqa: BLE001 - any failure to load means "fall back", and the name says so
        return "characters/4 (tiktoken unavailable)", lambda s: (len(s) + 3) // 4


def message_text(message: dict) -> str:
    content = message.get("content")
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    parts = []
    for part in content:
        parts.append(part.get("text", "") if isinstance(part, dict) else str(part))
    return "\n".join(parts)


def pseudo_vector(text: str, dims: int) -> list[float]:
    """A deterministic unit vector derived from the text. Same text and dims, same vector, on any machine."""
    out: list[float] = []
    counter = 0
    while len(out) < dims:
        block = hashlib.sha256(f"{counter}:{text}".encode("utf-8")).digest()
        out.extend(v / 2**31 for v in struct.unpack(">8i", block))
        counter += 1
    out = out[:dims]
    norm = math.sqrt(sum(v * v for v in out)) or 1.0
    return [v / norm for v in out]


class _Server(ThreadingHTTPServer):
    # The default listen queue is 5, so a burst of concurrent builder calls gets connections refused and a rehearsal
    # would silently undercount. test_parallel_calls_... guards this.
    request_queue_size = 256
    daemon_threads = True


@dataclass
class Call:
    seq: int
    ts: float
    path: str
    model: str
    stream: bool
    messages: list
    inputs: list
    prompt_text: str
    prompt_tokens: int
    completion_tokens: int = 0
    raw: dict = field(default_factory=dict, repr=False)


class Stub:
    def __init__(
        self,
        responder: Callable[[Call], Any],
        *,
        port: int = 0,
        default_dims: int = 1536,
        latency_s: float = 0.0,
    ) -> None:
        self.responder = responder
        self.default_dims = default_dims
        self.latency_s = latency_s
        self.tokenizer, self._count = make_counter()
        self.calls: list[Call] = []
        self._lock = threading.Lock()
        self._seq = 0
        handler = self._make_handler()
        self._server = _Server(("127.0.0.1", port), handler)
        self._thread: threading.Thread | None = None

    # ---- lifecycle -------------------------------------------------------------------------------------------
    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self._server.server_address[1]}/v1"

    def start(self) -> "Stub":
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        if self._thread:
            self._thread.join(timeout=5)

    def __enter__(self) -> "Stub":
        return self.start()

    def __exit__(self, *exc: object) -> None:
        self.stop()

    # ---- records ---------------------------------------------------------------------------------------------
    def reset(self) -> None:
        with self._lock:
            self.calls.clear()

    def summary(self) -> dict:
        with self._lock:
            calls = list(self.calls)
        chat = [c for c in calls if c.path.endswith("/chat/completions")]
        emb = [c for c in calls if c.path.endswith("/embeddings")]
        return {
            "tokenizer": self.tokenizer,
            "chat_calls": len(chat),
            "chat_prompt_tokens": sum(c.prompt_tokens for c in chat),
            "chat_completion_tokens": sum(c.completion_tokens for c in chat),
            "embedding_calls": len(emb),
            "embedding_inputs": sum(len(c.inputs) for c in emb),
            "embedding_tokens": sum(c.prompt_tokens for c in emb),
            "other_calls": len(calls) - len(chat) - len(emb),
        }

    def dump_jsonl(self, path: str, *, with_text: bool = False) -> None:
        """One line per call. Text is left out unless asked: it can hold third-party article text."""
        with self._lock:
            calls = list(self.calls)
        with open(path, "w", encoding="utf-8") as fh:
            for c in calls:
                row = {
                    "seq": c.seq,
                    "ts": c.ts,
                    "path": c.path,
                    "model": c.model,
                    "stream": c.stream,
                    "n_messages": len(c.messages),
                    "n_inputs": len(c.inputs),
                    "prompt_tokens": c.prompt_tokens,
                    "completion_tokens": c.completion_tokens,
                    "prompt_sha256": hashlib.sha256(c.prompt_text.encode("utf-8")).hexdigest(),
                }
                if with_text:
                    row["prompt_text"] = c.prompt_text
                fh.write(json.dumps(row) + "\n")

    # ---- HTTP ------------------------------------------------------------------------------------------------
    def _record(self, path: str, body: dict) -> Call:
        messages = body.get("messages") or []
        raw_in = body.get("input")
        if raw_in is None:
            inputs: list = []
        elif isinstance(raw_in, list):
            inputs = [x if isinstance(x, str) else json.dumps(x) for x in raw_in]
        else:
            inputs = [raw_in if isinstance(raw_in, str) else json.dumps(raw_in)]
        if messages:
            text = "\n".join(message_text(m) for m in messages)
        else:
            text = "\n".join(inputs)
        with self._lock:
            self._seq += 1
            call = Call(
                seq=self._seq,
                ts=time.time(),
                path=path,
                model=str(body.get("model", "")),
                stream=bool(body.get("stream")),
                messages=messages,
                inputs=inputs,
                prompt_text=text,
                prompt_tokens=self._count(text),
                raw=body,
            )
            self.calls.append(call)
        return call

    def _make_handler(self) -> type[BaseHTTPRequestHandler]:
        stub = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *args: object) -> None:  # silence the default stderr line per request
                return

            def _send_json(self, status: int, payload: dict) -> None:
                data = json.dumps(payload).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self) -> None:  # noqa: N802
                if self.path.rstrip("/").endswith("/models"):
                    self._send_json(200, {"object": "list", "data": [{"id": "stub-model", "object": "model"}]})
                else:
                    self._send_json(404, {"error": {"message": "not found", "type": "stub"}})

            def do_POST(self) -> None:  # noqa: N802
                length = int(self.headers.get("Content-Length") or 0)
                try:
                    body = json.loads(self.rfile.read(length) or b"{}")
                except json.JSONDecodeError:
                    self._send_json(400, {"error": {"message": "bad json", "type": "stub"}})
                    return
                path = self.path.split("?")[0]
                if stub.latency_s:
                    time.sleep(stub.latency_s)
                if path.endswith("/chat/completions"):
                    self._chat(path, body)
                elif path.endswith("/embeddings"):
                    self._embeddings(path, body)
                else:
                    stub._record(path, body)
                    self._send_json(404, {"error": {"message": f"stub has no route {path}", "type": "stub"}})

            def _chat(self, path: str, body: dict) -> None:
                call = stub._record(path, body)
                answer = stub.responder(call)
                message = answer if isinstance(answer, dict) else {"role": "assistant", "content": str(answer)}
                message.setdefault("role", "assistant")
                text = message_text(message)
                call.completion_tokens = stub._count(text) if text else 0
                usage = {
                    "prompt_tokens": call.prompt_tokens,
                    "completion_tokens": call.completion_tokens,
                    "total_tokens": call.prompt_tokens + call.completion_tokens,
                }
                finish = "tool_calls" if message.get("tool_calls") else "stop"
                base = {"id": f"stub-{call.seq}", "created": int(call.ts), "model": call.model or "stub-model"}
                if call.stream:
                    chunks = [
                        {**base, "object": "chat.completion.chunk",
                         "choices": [{"index": 0, "delta": message, "finish_reason": None}]},
                        {**base, "object": "chat.completion.chunk",
                         "choices": [{"index": 0, "delta": {}, "finish_reason": finish}]},
                    ]
                    if (body.get("stream_options") or {}).get("include_usage"):
                        chunks.append({**base, "object": "chat.completion.chunk", "choices": [], "usage": usage})
                    payload = "".join(f"data: {json.dumps(c)}\n\n" for c in chunks) + "data: [DONE]\n\n"
                    data = payload.encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/event-stream")
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                    return
                self._send_json(200, {
                    **base, "object": "chat.completion", "usage": usage,
                    "choices": [{"index": 0, "message": message, "finish_reason": finish}],
                })

            def _embeddings(self, path: str, body: dict) -> None:
                call = stub._record(path, body)
                dims = int(body.get("dimensions") or stub.default_dims)
                data = [
                    {"object": "embedding", "index": i, "embedding": pseudo_vector(text, dims)}
                    for i, text in enumerate(call.inputs)
                ]
                self._send_json(200, {
                    "object": "list", "model": call.model or "stub-embedding", "data": data,
                    "usage": {"prompt_tokens": call.prompt_tokens, "total_tokens": call.prompt_tokens},
                })

        return Handler
