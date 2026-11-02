"""End-to-end check of tools/metering_gateway.py's Anthropic route with the REAL anthropic SDK and a recording fake upstream.

    uv run --no-project --with anthropic python tools/exp/gateway_sdk_e2e_anthropic.py ABSOLUTE_REPO_ROOT SCRATCH_DIR

Same idea and same limits as gateway_sdk_e2e_openai.py: loopback only, a fake key, a fake provider that records the
x-api-key it receives and answers in the Messages API's JSON and event-stream shapes. Exit status 0 means every
check passed.
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

import anthropic

W, work = Path(sys.argv[1]), Path(sys.argv[2])
work.mkdir(parents=True, exist_ok=True)
# A fake key, assembled at run time so the public-safety gate does not flag a key-shaped literal in the repository.
REAL = "sk-" + "ant-" + "fake-REALKEY-0123456789abcdef"
seen: list[dict] = []
lock = threading.Lock()


def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


class Up(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        return

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(n) or b"{}")
        with lock:
            seen.append({"path": self.path, "x_api_key": self.headers.get("x-api-key"), "auth": self.headers.get("Authorization"),
                         "stream": bool(body.get("stream")), "max_tokens": body.get("max_tokens")})
        model = body.get("model")
        if body.get("stream"):
            msg = {"id": "m1", "type": "message", "role": "assistant", "model": model, "content": [], "stop_reason": None,
                   "stop_sequence": None, "usage": {"input_tokens": 1000, "output_tokens": 1}}
            payload = (sse("message_start", {"type": "message_start", "message": msg})
                       + sse("content_block_start", {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}})
                       + sse("content_block_delta", {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "hi"}})
                       + sse("content_block_stop", {"type": "content_block_stop", "index": 0})
                       + sse("message_delta", {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence": None},
                                               "usage": {"output_tokens": 200}})
                       + sse("message_stop", {"type": "message_stop"})).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
        else:
            payload = json.dumps({"id": "m1", "type": "message", "role": "assistant", "model": model,
                                  "content": [{"type": "text", "text": "hi"}], "stop_reason": "end_turn", "stop_sequence": None,
                                  "usage": {"input_tokens": 1000, "output_tokens": 200}}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


class UpServer(ThreadingHTTPServer):
    request_queue_size = 128
    daemon_threads = True


up = UpServer(("127.0.0.1", 0), Up)
threading.Thread(target=up.serve_forever, daemon=True).start()

(work / "gateway.toml").write_text(f"""
[gateway]
currency = "FAKE-USD"
cap = 0.0100
default_max_output_tokens = 1024
input_bytes_per_token = 2
log_file = "meter.jsonl"

[upstreams.ant]
protocol = "anthropic"
base_url = "http://127.0.0.1:{up.server_address[1]}/v1"
key_env = "GATEWAY_ANTHROPIC_KEY"

[models."fake-claude"]
upstream = "ant"
input_per_mtok = 1.00
output_per_mtok = 5.00
cached_input_per_mtok = 0.10
cache_write_per_mtok = 1.25
source_url = "https://example.invalid/pricing"
read_at = "20261102 10:00"
""")
proc = subprocess.Popen(["uv", "run", str(W / "tools" / "metering_gateway.py"), "--config", str(work / "gateway.toml"), "--port", "0"],
                        cwd=work, env={"PATH": os.environ["PATH"], "HOME": os.environ["HOME"], "GATEWAY_ANTHROPIC_KEY": REAL},
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
banner, port, t0 = "", None, time.time()
while time.time() - t0 < 60:
    line = proc.stdout.readline()
    banner += line
    m = re.search(r"listening on http://127\.0\.0\.1:(\d+)", line)
    if m:
        port = int(m.group(1))
        break
assert port, banner

ok = True


def check(label, cond, detail=""):
    global ok
    ok = ok and cond
    print(("PASS  " if cond else "FAIL  ") + label + (f"   [{detail}]" if detail else ""), flush=True)


client = anthropic.Anthropic(base_url=f"http://127.0.0.1:{port}", api_key="dummy-client-key", max_retries=0)
msgs = [{"role": "user", "content": "say hi"}]

r = client.messages.create(model="fake-claude", max_tokens=300, messages=msgs)
check("messages.create through the real Anthropic SDK", r.content[0].text == "hi" and r.usage.input_tokens == 1000)

with client.messages.stream(model="fake-claude", max_tokens=300, messages=msgs) as stream:
    text = "".join(stream.text_stream)
    final = stream.get_final_message()
check("messages.stream through the real Anthropic SDK", text == "hi" and final.usage.output_tokens == 200)

check("upstream saw the real key in x-api-key on every call, never the client's dummy",
      all(x["x_api_key"] == REAL for x in seen), str([x["x_api_key"] is not None for x in seen]))
check("no Authorization header from the client reached the upstream", all(not x["auth"] for x in seen), str([x["auth"] for x in seen]))

log = [json.loads(l) for l in (work / "meter.jsonl").read_text().splitlines() if l.strip()]
check("log: two records with the upstream's usage (1000 in, 200 out), streamed and not",
      len(log) == 2 and all(x["input_tokens"] == 1000 and x["output_tokens"] == 200 for x in log) and {x["streamed"] for x in log} == {True, False},
      str([(x["input_tokens"], x["output_tokens"], x["streamed"], x["cost"]) for x in log]))
check("log: cost is exact (1000*1.00 + 200*5.00 per million = 0.002)", all(Decimal(x["cost"]) == Decimal("0.002") for x in log))

before = len(seen)
try:
    client.messages.create(model="fake-claude", max_tokens=20000, messages=msgs)
    check("a call whose reservation alone exceeds the cap is refused", False, "no error raised")
except anthropic.RateLimitError as exc:
    check("a call whose reservation alone exceeds the cap is refused with 429", exc.status_code == 429, str(getattr(exc, "body", ""))[:100])
    check("the refused call was not forwarded", len(seen) == before)

oks = refused = 0
for _ in range(20):
    try:
        client.messages.create(model="fake-claude", max_tokens=300, messages=msgs)
        oks += 1
    except anthropic.RateLimitError:
        refused += 1
        break
final_sum = json.loads(subprocess.run(["curl", "-s", f"http://127.0.0.1:{port}/_meter/summary"], capture_output=True, text=True).stdout)
check("calls hit the cap and the next one is refused", refused == 1 and oks >= 1, f"{oks} accepted, then refused")
check("spend never passed the cap", Decimal(str(final_sum["spent"])) <= Decimal("0.0100"), f"spent {final_sum['spent']}")
check("upstream count equals accepted calls", len(seen) == before + oks, f"{len(seen)} vs {before + oks}")

proc.terminate()
try:
    tail = proc.communicate(timeout=20)[0]
except subprocess.TimeoutExpired:
    proc.kill()
    tail = proc.communicate()[0]
files = [p for p in work.iterdir() if p.is_file()]
check("the real key is in no file and not in the gateway's output",
      not [p.name for p in files if REAL in p.read_text(errors="replace")] and REAL not in banner + tail)
print("\nALL PASS" if ok else "\nSOME FAILED")
sys.exit(0 if ok else 1)
