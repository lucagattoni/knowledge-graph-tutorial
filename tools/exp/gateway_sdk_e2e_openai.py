"""End-to-end check of tools/metering_gateway.py with the REAL openai SDK and a recording fake upstream.

    uv run --no-project --with openai python tools/exp/gateway_sdk_e2e_openai.py ABSOLUTE_REPO_ROOT SCRATCH_DIR

No real key and no network beyond loopback: the gateway is started as a subprocess with a fake key, and a small
fake provider records what it receives. It covers what the gateway's own unit tests cannot: that the SDK's real
requests (chat, streaming, embeddings) work through it, that the client's dummy key is replaced by the gateway's
key, that costs are exact, and that the cap refuses a call without forwarding it. It does not cover TLS or a
real provider's responses. Exit status 0 means every check passed.
"""
import json
import os
import re
import subprocess
import sys
import threading
import time
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import openai

W, work = Path(sys.argv[1]), Path(sys.argv[2])
work.mkdir(parents=True, exist_ok=True)
REAL = "sk-fake-REALKEY-0123456789abcdef"
seen: list[dict] = []
lock = threading.Lock()


class Up(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        return

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(n) or b"{}")
        with lock:
            seen.append({"path": self.path, "auth": self.headers.get("Authorization"), "stream": bool(body.get("stream")),
                         "include_usage": (body.get("stream_options") or {}).get("include_usage")})
        model = body.get("model")
        if self.path.endswith("/embeddings"):
            payload = {"object": "list", "model": model, "data": [{"object": "embedding", "index": 0, "embedding": [0.1, 0.2]}],
                       "usage": {"prompt_tokens": 7, "total_tokens": 7}}
        else:
            payload = {"id": "x", "object": "chat.completion", "created": 1, "model": model,
                       "choices": [{"index": 0, "message": {"role": "assistant", "content": "hi"}, "finish_reason": "stop"}],
                       "usage": {"prompt_tokens": 1000, "completion_tokens": 200, "total_tokens": 1200}}
        if body.get("stream"):
            usage = {"prompt_tokens": 1000, "completion_tokens": 200, "total_tokens": 1200}
            chunks = [
                {"id": "x", "object": "chat.completion.chunk", "created": 1, "model": model,
                 "choices": [{"index": 0, "delta": {"role": "assistant", "content": "hi"}, "finish_reason": None}]},
                {"id": "x", "object": "chat.completion.chunk", "created": 1, "model": model, "choices": [], "usage": usage},
            ]
            data = ("".join(f"data: {json.dumps(c)}\n\n" for c in chunks) + "data: [DONE]\n\n").encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
        else:
            data = json.dumps(payload).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


class UpServer(ThreadingHTTPServer):
    request_queue_size = 128
    daemon_threads = True


up = UpServer(("127.0.0.1", 0), Up)
threading.Thread(target=up.serve_forever, daemon=True).start()
up_port = up.server_address[1]

cfg = work / "gateway.toml"
cfg.write_text(f"""
[gateway]
currency = "FAKE-USD"
cap = 0.0100
default_max_output_tokens = 1024
input_bytes_per_token = 2
log_file = "meter.jsonl"

[upstreams.up]
protocol = "openai"
base_url = "http://127.0.0.1:{up_port}/v1"
key_env = "GATEWAY_OPENAI_KEY"

[models."fake-small"]
upstream = "up"
input_per_mtok = 0.15
output_per_mtok = 0.60
source_url = "https://example.invalid/pricing"
read_at = "20261102 10:00"

[models."fake-embed"]
upstream = "up"
input_per_mtok = 0.02
output_per_mtok = 0
source_url = "https://example.invalid/pricing"
read_at = "20261102 10:00"
""")
env = {"PATH": os.environ.get("PATH", ""), "HOME": os.environ.get("HOME", ""), "GATEWAY_OPENAI_KEY": REAL}
proc = subprocess.Popen(["uv", "run", str(W / "tools" / "metering_gateway.py"), "--config", str(cfg), "--port", "0"],
                        cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
banner = ""
port = None
t0 = time.time()
while time.time() - t0 < 60:
    line = proc.stdout.readline()
    banner += line
    m = re.search(r"listening on http://127\.0\.0\.1:(\d+)", line)
    if m:
        port = int(m.group(1))
        break
assert port, f"gateway did not start: {banner}"

ok = True


def check(label: str, cond: bool, detail: str = "") -> None:
    global ok
    ok = ok and cond
    print(("PASS  " if cond else "FAIL  ") + label + (f"   [{detail}]" if detail else ""), flush=True)


client = openai.OpenAI(base_url=f"http://127.0.0.1:{port}/v1", api_key="dummy-client-key", max_retries=0)
msg = [{"role": "user", "content": "say hi"}]

r = client.chat.completions.create(model="fake-small", messages=msg, max_tokens=300)
check("chat completion through the real SDK", r.choices[0].message.content == "hi" and r.usage.prompt_tokens == 1000)

s = client.chat.completions.create(model="fake-small", messages=msg, max_tokens=300, stream=True)
text = "".join((c.choices[0].delta.content or "") for c in s if c.choices)
check("streaming through the real SDK", text == "hi")
check("gateway injected stream_options.include_usage", seen[-1]["include_usage"] is True, f"upstream saw {seen[-1]['include_usage']}")

e = client.embeddings.create(model="fake-embed", input="hello")
check("embeddings through the real SDK", len(e.data[0].embedding) == 2)

check("upstream saw the real key on every call and never the client's dummy",
      all(x["auth"] == f"Bearer {REAL}" for x in seen), str({x["auth"] is not None for x in seen}))

summary = json.loads(subprocess.run(["curl", "-s", f"http://127.0.0.1:{port}/_meter/summary"], capture_output=True, text=True).stdout)
log = [json.loads(l) for l in (work / "meter.jsonl").read_text().splitlines() if l.strip()]
chat = [x for x in log if x["route"].endswith("chat/completions")]
check("log: two chat records with the upstream's usage", len(chat) == 2 and all(x["input_tokens"] == 1000 and x["output_tokens"] == 200 for x in chat),
      str([(x["input_tokens"], x["output_tokens"], x["cost"]) for x in chat]))
check("log: chat cost is exact (1000*0.15 + 200*0.60 per million = 0.00027)", all(Decimal(x["cost"]) == Decimal("0.00027") for x in chat))
emb = [x for x in log if x["route"].endswith("embeddings")]
check("log: embedding cost is exact (7*0.02 per million = 0.00000014)", len(emb) == 1 and Decimal(emb[0]["cost"]) == Decimal("0.00000014"), str(emb and emb[0]["cost"]))
check("summary endpoint total equals the sum of the log", Decimal(str(summary.get("spent"))) == sum(Decimal(x["cost"]) for x in log), str(summary.get("spent")))

before = len(seen)
try:
    client.chat.completions.create(model="fake-small", messages=msg, max_tokens=40000)
    check("a call whose reservation alone exceeds the cap is refused", False, "no error raised")
except openai.RateLimitError as exc:
    body = getattr(exc, "body", None) or {}
    code = (body.get("error", body) or {}).get("code") if isinstance(body, dict) else None
    check("a call whose reservation alone exceeds the cap is refused with 429", exc.status_code == 429, f"code={code}")
    check("the refused call was not forwarded", len(seen) == before, f"upstream calls {before} -> {len(seen)}")

oks = refused = 0
for _ in range(80):
    try:
        client.chat.completions.create(model="fake-small", messages=msg, max_tokens=300)
        oks += 1
    except openai.RateLimitError:
        refused += 1
        break
final = json.loads(subprocess.run(["curl", "-s", f"http://127.0.0.1:{port}/_meter/summary"], capture_output=True, text=True).stdout)
check("sequential calls hit the cap and the next one is refused", refused == 1 and oks > 20, f"{oks} calls accepted before the first refusal")
check("spend never passed the cap", Decimal(str(final["spent"])) <= Decimal("0.0100"), f"spent {final['spent']} of 0.0100")
check("upstream count equals accepted calls (nothing forwarded after the refusal)", len(seen) == before + oks, f"{len(seen)} vs {before + oks}")

proc.terminate()
try:
    tail = proc.communicate(timeout=20)[0]
except subprocess.TimeoutExpired:
    proc.kill()
    tail = proc.communicate()[0]
allout = banner + tail
files = [p for p in work.iterdir() if p.is_file()]
leaked = [p.name for p in files if REAL in p.read_text(errors="replace")]
check("the real key is in no file the gateway wrote", not leaked, str(leaked))
check("the real key is not in the gateway's own output", REAL not in allout)
check("the client's dummy key reached no file", not any("dummy-client-key" in p.read_text(errors="replace") for p in files))
print("\nALL PASS" if ok else "\nSOME FAILED")
sys.exit(0 if ok else 1)
