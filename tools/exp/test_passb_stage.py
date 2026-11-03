"""Tests for tools/exp/passb_stage.py. Standard library only; loopback only; no model, no provider, no real key.

The "provider" is a fake OpenAI-style server written here (a copy of the one in test_passb_common.py: it records every request
with its Authorization header and answers with a `usage` that includes `completion_tokens_details.reasoning_tokens`); the
"local" upstream is a second fake. The gateway is the real one (`tools/metering_gateway.py`), started by a FAKE RUNNER: a small
script written to a temporary repository that accepts the real runners' command line, builds a `HostedGateway` from
`--hosted-profile`, makes a few chat calls through it, writes a minimal result JSON and exits with the code the test chose,
optionally leaving a child `sleep` behind. The stage driver, the pre-flight and the watchdog are the real ones. The key is a
made-up string assembled at run time from pieces and written to a mode-600 file in a temporary directory.

Run from the repository root:

    uv run python -m unittest tools/exp/test_passb_stage.py
"""

from __future__ import annotations

import builtins
import contextlib
import copy
import fcntl
import io
import json
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.request
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import passb_common as pb  # noqa: E402
import passb_preflight as pf  # noqa: E402
import passb_stage as ps  # noqa: E402

SCRIPT = HERE / "passb_stage.py"
CANARY = "sk-" + "canary" + "-" + "Zr4Kq9" + "Lm2Xv7Tj"      # assembled here: the file holds no key-shaped literal
CHAT, EMBED = "gpt-6-luna", "embed-test"
RUNNER_PATH = "/usr/bin:/bin:/opt/homebrew/bin"
REAL_RUNNERS = ("x2_passa_lightrag.py", "x2_passa_fast_graphrag.py", "x2_passa_microsoft_graphrag.py", "x2_passa_nano_graphrag.py")
REAL_FLAGS = {"lightrag": ["--llm-max-async", "4", "--llm-timeout", "1800"], "fast": ["--llm-concurrency", "4", "--llm-timeout-s", "3600"],
              "ms": ["--concurrency", "4", "--request-timeout-s", "3600", "--child-timeout-s", "43200"],
              "nano": ["--max-async", "4", "--client-timeout-s", "3600"]}
CALL_COST = Decimal("0.00027")           # 1200 input and 300 output tokens at USD 0.10 and 0.50 per million
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))

FAKE_RUNNER = r'''
import argparse, json, os, subprocess, sys, time, urllib.request
sys.dont_write_bytecode = True                   # importing the real modules must leave no .pyc in the repository
sys.path.insert(0, {tools_exp!r})
import passb_common as pb

ap = argparse.ArgumentParser()
for name in ("--corpus", "--documents", "--repo-root", "--upstream-url", "--model", "--embed-model", "--hosted-profile",
             "--workdir", "--out", "--checkpoints", "--tiktoken-cache", "--fake-marker"):
    ap.add_argument(name)
ap.add_argument("--fake-calls", type=int, default=2)
ap.add_argument("--fake-exit", type=int, default=0)
ap.add_argument("--fake-sleep", type=float, default=0.0)
ap.add_argument("--fake-child", action="store_true")
ap.add_argument("--fake-hang", action="store_true")
ap.add_argument("--fake-nowrite", action="store_true")
ap.add_argument("--fake-body", choices=("unique", "same_across_runs", "constant"), default="unique")
args, rest = ap.parse_known_args()
if args.fake_marker:
    with open(args.fake_marker, "a") as handle:
        handle.write(str(os.getpid()) + "\n")
if os.path.exists(args.workdir):
    sys.exit(2)                                  # the real runners want a workdir that does not exist yet
os.makedirs(args.workdir)
profile = pb.load_profile(args.hosted_profile)
opener = urllib.request.build_opener(urllib.request.ProxyHandler({{}}))
child_pid = None
with pb.make_gateway(profile, os.path.join(args.workdir, "gateway"), args.upstream_url, [args.model, args.embed_model],
                     args.repo_root) as gw:
    if args.fake_child:
        child_pid = subprocess.Popen(["sleep", "60"]).pid
    with open(os.path.join(args.workdir, "pids.json"), "w") as handle:
        json.dump({{"pid": os.getpid(), "pgid": os.getpgrp(), "sid": os.getsid(0), "child": child_pid}}, handle)
    for i in range(args.fake_calls):
        who = os.getpid() if args.fake_body == "unique" else 0               # same_across_runs: a second run repeats the first
        n = 0 if args.fake_body == "constant" else i                         # constant: every call of a run is the same request
        body = json.dumps({{"model": args.model, "messages": [{{"role": "user", "content": "hello %d %d" % (who, n)}}]}})
        req = urllib.request.Request(gw.base_url + "/chat/completions", data=body.encode(),
                                     headers={{"Content-Type": "application/json", "Authorization": "Bearer dummy-not-a-key"}})
        with opener.open(req, timeout=60) as reply:
            reply.read()
        time.sleep(args.fake_sleep)
    if args.fake_hang:
        time.sleep(60)                           # long enough to be stopped; finite, so a regression fails instead of hanging
    block = gw.hosted_block()
if args.fake_nowrite:
    sys.exit(args.fake_exit)                     # dies without writing a result file
with open(args.out, "w") as handle:
    json.dump({{"hosted": block, "argv": sys.argv[1:], "environ": dict(os.environ), "isolated": sys.flags.isolated,
               "pid": os.getpid(), "pgid": os.getpgrp(), "cwd": os.getcwd(), "rest": rest}}, handle)
sys.exit(args.fake_exit)
'''


class _Server(ThreadingHTTPServer):
    request_queue_size = 64
    daemon_threads = True


class FakeProvider:
    """A loopback server that plays a provider (or the local Ollama): records requests, answers chat and embeddings."""

    def __init__(self) -> None:
        self.prompt_tokens, self.completion_tokens, self.reasoning_tokens = 1200, 300, 0
        self.echo_authorization = False
        self.requests: list[dict] = []
        self._lock = threading.Lock()
        outer = self

        class H(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *a: object) -> None:
                return

            def _send(self, status: int, obj: dict) -> None:
                data = json.dumps(obj).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self) -> None:  # noqa: N802
                with outer._lock:
                    outer.requests.append({"method": "GET", "path": self.path, "body": None,
                                           "authorization": self.headers.get("Authorization")})
                self._send(200, {"models": [{"name": f"{EMBED}:latest"}]} if self.path == "/api/tags" else {"error": "not found"})

            def do_POST(self) -> None:  # noqa: N802
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
                with outer._lock:
                    outer.requests.append({"method": "POST", "path": self.path, "body": body,
                                           "authorization": self.headers.get("Authorization")})
                if self.path.endswith("/chat/completions"):
                    usage = {"prompt_tokens": outer.prompt_tokens, "completion_tokens": outer.completion_tokens,
                             "total_tokens": outer.prompt_tokens + outer.completion_tokens,
                             "completion_tokens_details": {"reasoning_tokens": outer.reasoning_tokens}}
                    text = (self.headers.get("Authorization") or "") if outer.echo_authorization else "ok"
                    self._send(200, {"id": "chatcmpl-test", "object": "chat.completion", "model": "gpt-6-luna-test-1",
                                     "choices": [{"index": 0, "finish_reason": "stop",
                                                  "message": {"role": "assistant", "content": text}}], "usage": usage})
                elif self.path.endswith("/embeddings"):
                    inputs = body.get("input") if isinstance(body.get("input"), list) else [body.get("input")]
                    self._send(200, {"object": "list", "model": "embed-fake",
                                     "usage": {"prompt_tokens": 3 * len(inputs), "total_tokens": 3 * len(inputs)},
                                     "data": [{"object": "embedding", "index": i, "embedding": [0.25, 0.5, 0.75]}
                                              for i in range(len(inputs))]})
                else:
                    self._send(404, {"error": "not found"})

        self.server = _Server(("127.0.0.1", 0), H)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base_url = f"http://127.0.0.1:{self.server.server_address[1]}/v1"

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()

    def chat_requests(self) -> list[dict]:
        return [r for r in self.requests if r["path"].endswith("/chat/completions")]


class PopenSpy:
    """Stands in for subprocess.Popen: records every call (the argument list as given, the keywords, the process) and starts
    the real thing. `override` may replace an argument list before the start (to make a helper misbehave)."""

    def __init__(self, override=None) -> None:
        self.real = subprocess.Popen
        self.override = override
        self.calls: list[dict] = []

    def __call__(self, args, *a, **kw):
        argv = self.override(list(args)) if self.override else list(args)
        proc = self.real(argv, *a, **kw)
        self.calls.append({"argv": list(args), "kwargs": kw, "proc": proc})
        return proc

    def runners(self) -> list[dict]:
        return [c for c in self.calls if "--hosted-profile" in c["argv"]]

    def watchdogs(self) -> list[dict]:
        return [c for c in self.calls if "--kill-pgid" in c["argv"]]

    def final_reads(self) -> list[dict]:
        return [c for c in self.calls if "--max-seconds" in c["argv"]]


class OpenSpy:
    """Records every path opened through open(), io.open() and os.open() while active."""

    def __init__(self) -> None:
        self.opened: list[str] = []
        self._patches: list = []

    def __enter__(self) -> "OpenSpy":
        real_open, real_io_open, real_os_open = builtins.open, io.open, os.open

        def note(target: object) -> None:
            try:
                self.opened.append(os.fspath(target))
            except TypeError:
                pass

        def spy_open(file, *a, **k):
            note(file)
            return real_open(file, *a, **k)

        def spy_io_open(file, *a, **k):
            note(file)
            return real_io_open(file, *a, **k)

        def spy_os_open(path, *a, **k):
            note(path)
            return real_os_open(path, *a, **k)

        self._patches = [mock.patch.object(builtins, "open", spy_open), mock.patch.object(io, "open", spy_io_open),
                         mock.patch.object(os, "open", spy_os_open)]
        for p in self._patches:
            p.start()
        return self

    def __exit__(self, *exc: object) -> None:
        for p in reversed(self._patches):
            p.stop()


class Outcome:
    def __init__(self, rc: int, out: str, err: str, spy: PopenSpy) -> None:
        self.rc, self.out, self.err, self.spy = rc, out, err, spy


def opt(argv: list[str], flag: str) -> str:
    return argv[argv.index(flag) + 1]


def alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    state = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return bool(state) and not state.startswith("Z")


def wait_for(predicate, timeout: float = 30.0, interval: float = 0.1) -> bool:
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        if predicate():
            return True
        time.sleep(interval)
    return predicate()


def snapshot(root: Path) -> dict:
    return {str(p.relative_to(root)): (p.stat().st_size, p.stat().st_mtime_ns, p.is_dir()) for p in sorted(root.rglob("*"))}


class StageCase(unittest.TestCase):
    """A temporary world: a fake repository with the real gateway and a fake runner, a key file, a profile, a builders config."""

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.paid, self.local = FakeProvider(), FakeProvider()
        self.addCleanup(self.paid.close)
        self.addCleanup(self.local.close)
        self.repo = self.root / "repo"
        (self.repo / "tools" / "exp").mkdir(parents=True)
        shutil.copy(REPO / "tools" / "metering_gateway.py", self.repo / "tools" / "metering_gateway.py")
        (self.repo / "tools" / "exp" / "fake_runner.py").write_text(FAKE_RUNNER.format(tools_exp=str(HERE)))
        self.keydir = self.root / "secret"
        self.keydir.mkdir(mode=0o700)
        self.key_file = self.keydir / "provider.key"
        self.key_file.write_text(CANARY + "\n")
        self.key_file.chmod(0o600)
        (self.root / "corpus.json").write_text("{}")
        (self.root / "documents.tsv").write_text("url\n")
        for name in ("tiktoken", "home"):
            (self.root / name).mkdir()
        self.ledger, self.out = self.root / "ledger", self.root / "out"
        self.markers = self.root / "markers"
        self.markers.mkdir()
        self.extra = {name: [*REAL_FLAGS[name], "--fake-calls", "2"] for name in ps.BUILDERS}
        self.isolated = {"lightrag": True, "fast": False, "ms": True, "nano": False}
        self.profile_over: dict = {}
        self.config_over: dict = {}
        self.addCleanup(self.reap)
        self.write_all()

    # -- files ---------------------------------------------------------------------------------------------------------
    def profile_dict(self) -> dict:
        d = {"base_url": self.paid.base_url, "key_file": str(self.key_file), "ledger_dir": str(self.ledger),
             "allowance_usd": "0.05", "upstream_timeout_s": 900, "input_per_mtok": "0.10", "output_per_mtok": "0.50",
             "cached_input_per_mtok": "0.01", "cache_write_per_mtok": "0.125",
             "source_url": "https://pricing.example.invalid/page", "read_at": "20261102 20:20", "output_limit_default": 6144,
             "request_defaults": {"reasoning_effort": "none"}}
        d.update(self.profile_over)
        return {k: v for k, v in d.items() if v is not ...}

    def config_dict(self) -> dict:
        builders = {}
        for name in ps.BUILDERS:
            env = {"HOME": str(self.root / "home"), "TIKTOKEN_CACHE_DIR": str(self.root / "tiktoken")}
            if name == "fast":
                env["PYTHONDONTWRITEBYTECODE"] = "1"
            builders[name] = {"python": sys.executable, "runner": "fake_runner.py", "isolated": self.isolated[name], "env": env,
                              "tiktoken_cache": str(self.root / "tiktoken"), "extra_args": list(self.extra[name])}
        d = {"repo_root": str(self.repo), "corpus": str(self.root / "corpus.json"), "documents": str(self.root / "documents.tsv"),
             "local_upstream_url": self.local.base_url, "embed_model": EMBED, "chat_model": CHAT, "builders": builders}
        d.update(self.config_over)
        return {k: v for k, v in d.items() if v is not ...}

    def write_all(self) -> None:
        self.profile_path = self.root / "stage-profile.json"
        self.profile_path.write_text(json.dumps(self.profile_dict()))
        self.cfg_path = self.root / "builders.json"
        self.cfg_path.write_text(json.dumps(self.config_dict()))

    def marker(self, name: str) -> Path:
        return self.markers / name

    def seed_ledger(self, cost: str, *, ts: str = "2026-01-01T00:00:00.000Z", name: str = "earlier") -> None:
        """A record of an earlier stage in the shared ledger, in the gateway's format (what --resume needs)."""
        self.ledger.mkdir(mode=0o700, exist_ok=True)
        record = {"ts": ts, "call_id": name, "route": "/v1/chat/completions", "upstream": "hosted", "model_requested": CHAT,
                  "model_reported": CHAT, "http_status": 200, "input_tokens": 1, "output_tokens": 1, "cached_input_tokens": None,
                  "cost": cost, "currency": "USD", "voided": False, "usage_missing": False, "refusal": None, "error": None,
                  "request_sha256": name}
        with open(self.ledger / "meter.jsonl", "a") as handle:
            handle.write(json.dumps(record) + "\n")

    # -- running -------------------------------------------------------------------------------------------------------
    def argv(self, builders, *, stage: str = "B", label: str = "r1", send: bool = True, poll: str = "0.2") -> list[str]:
        out = ["--stage", stage]
        for b in builders:
            out += ["--builder", b]
        out += ["--profile", str(self.profile_path), "--builders-config", str(self.cfg_path), "--out-dir", str(self.out),
                "--run-label", label, "--poll-s", poll]
        return out + (["--send"] if send else [])

    def drive(self, builders, *, override=None, **kw) -> Outcome:
        spy = PopenSpy(override)
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(subprocess, "Popen", spy), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = ps.main(self.argv(builders, **kw))
        for call in spy.calls:
            self.addCleanup(self.kill_if_alive, call["proc"])
        return Outcome(rc, out.getvalue(), err.getvalue(), spy)

    @staticmethod
    def kill_if_alive(proc: subprocess.Popen) -> None:
        if proc.poll() is None:
            with contextlib.suppress(OSError):
                if os.getpgid(proc.pid) == proc.pid and proc.pid != os.getpgrp():      # a group leader of its own
                    os.killpg(proc.pid, signal.SIGKILL)
            with contextlib.suppress(OSError):
                proc.kill()
            proc.wait()

    def report(self) -> list[dict]:
        return json.loads((self.out / "stage_report.json").read_text())["entries"]

    def state(self, stage: str = "B") -> dict:
        return json.loads((self.ledger / f"stage_{stage}.json").read_text())

    def pids(self, label: str) -> dict:
        return json.loads((self.out / label / "work" / "pids.json").read_text())

    def result(self, label: str) -> dict:
        return json.loads((self.out / label / "result.json").read_text())

    def run_profile(self, label: str) -> dict:
        return json.loads((self.out / label / "profile.json").read_text())

    def reap(self) -> None:
        for path in self.out.glob("*/work/pids.json") if self.out.exists() else []:
            try:
                info = json.loads(path.read_text())
            except ValueError:
                continue
            for pid in (info.get("child"),):
                if pid:
                    with contextlib.suppress(OSError):
                        os.kill(pid, signal.SIGKILL)
            if info["pgid"] not in (0, 1, os.getpgrp()):                    # never this test run's own group
                with contextlib.suppress(OSError):
                    os.killpg(info["pgid"], signal.SIGKILL)

    def nothing_was_started_or_written(self, outcome: Outcome) -> None:
        self.assertEqual(outcome.spy.runners(), [])
        self.assertEqual(outcome.spy.watchdogs(), [])
        self.assertFalse(self.out.exists())
        self.assertEqual(self.paid.requests, [])


class DryRunTests(StageCase):
    def test_without_send_nothing_is_started_and_nothing_is_written_and_the_plan_is_printed(self) -> None:
        before = snapshot(self.root)
        with OpenSpy() as spy:
            outcome = self.drive(["lightrag", "ms"], send=False)
        self.assertEqual(outcome.rc, 0, outcome.err)
        self.nothing_was_started_or_written(outcome)
        self.assertFalse(self.ledger.exists())                             # not even the ledger directory
        self.assertEqual(snapshot(self.root), before)                      # the whole tree is as it was
        self.assertEqual(self.local.requests, [])
        self.assertNotIn(str(self.key_file), spy.opened)                   # the key file is never opened
        text = outcome.out
        for needle in ("DRY RUN", "stage B", "lightrag", "ms", "B-r1-lightrag", "B-r1-ms", "--hosted-profile", "--checkpoints 1",
                       "--llm-max-async", "--concurrency", "stop at", "USD 0.09", "allowance", "USD 0.20", "PATH=" + RUNNER_PATH,
                       str(self.key_file), "passb_watchdog.py", "--since", "--repeat-since", "--stop-at-usd 0.09",
                       "nothing was started"):
            self.assertIn(needle, text)
        self.assertNotIn(CANARY, text)
        self.assertLess(text.index("builder 1: lightrag"), text.index("builder 2: ms"))      # the order given

    def test_the_dry_run_with_a_ledger_in_place_changes_nothing_and_reads_the_stage_window(self) -> None:
        self.seed_ledger("0.01")
        self.ledger.joinpath("stage_B.json").write_text(json.dumps({"started_utc": "2026-11-02T20:00:00.000Z", "spent_start": "0.004"}))
        self.out.mkdir()
        before = snapshot(self.root)
        outcome = self.drive(["fast"], send=False)
        self.assertEqual(outcome.rc, 0, outcome.err)
        self.assertEqual(snapshot(self.root), before)
        self.assertEqual(outcome.spy.calls, [])
        self.assertIn("USD 0.006", outcome.out)                              # 0.010 in the ledger - 0.004 at the window's start
        self.assertIn("2026-11-02T20:00:00.000Z", outcome.out)
        self.assertEqual(self.drive(["fast"], send=False).rc, 0)

    def test_a_dry_run_says_refused_and_exits_1_when_the_pre_flight_would_refuse(self) -> None:
        self.seed_ledger("2.999")
        outcome = self.drive(["lightrag"], send=False)
        self.assertEqual(outcome.rc, 1)
        self.assertIn("REFUSED", outcome.out)
        self.assertEqual(outcome.spy.calls, [])
        self.assertFalse(self.out.exists())

    def test_the_dry_run_projects_later_builders_on_the_central_estimates_of_the_earlier_ones(self) -> None:
        outcome = self.drive(["lightrag", "fast", "ms", "nano"], stage="D", send=False)
        self.assertEqual(outcome.rc, 0, outcome.err)
        self.assertIn("projected", outcome.out)
        self.assertEqual(len(re.findall(r"verdict\s+OK,", outcome.out)), 4)

    def test_the_command_line_without_send_is_a_dry_run_and_the_file_runs_as_a_script(self) -> None:
        proc = subprocess.run([sys.executable, "-B", str(SCRIPT), *self.argv(["lightrag"], send=False)], capture_output=True,
                              text=True, env={"PATH": "/usr/bin:/bin"}, timeout=120)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("DRY RUN", proc.stdout)
        self.assertFalse(self.out.exists())
        self.assertFalse(self.ledger.exists())
        self.assertEqual(self.paid.requests, [])
        bad = subprocess.run([sys.executable, "-B", str(SCRIPT), "--stage", "A", "--builder", "lightrag", "--profile", "x",
                              "--builders-config", "y", "--out-dir", "z"], capture_output=True, text=True,
                             env={"PATH": "/usr/bin:/bin"}, timeout=120)
        self.assertEqual(bad.returncode, 2)                                  # stage A is not this program's


class RefusalTests(StageCase):
    def test_a_refusal_by_the_pre_flight_comes_before_anything_starts_and_is_reported(self) -> None:
        self.seed_ledger("2.999")                                            # 0.001 under the total cap of 3
        outcome = self.drive(["lightrag", "fast"])
        self.assertEqual(outcome.rc, 1)
        self.assertEqual(outcome.spy.calls, [])                              # no runner, no watchdog, no last read
        self.assertEqual(self.paid.requests, [])
        self.assertEqual([p.name for p in self.out.iterdir()], ["stage_report.json"])      # no run directory
        (entry,) = self.report()
        self.assertEqual((entry["outcome"], entry["builder"], entry["stage"], entry["label"]), ("refused", "lightrag", "B", "B-r1-lightrag"))
        self.assertEqual(entry["not_started"], ["lightrag", "fast"])
        self.assertIn("total", entry["reason"])
        self.assertIn("REFUSED", outcome.err)
        self.assertFalse((self.ledger / "stage_B.json").exists())            # a refused stage opens no window

    def test_a_stage_that_has_spent_its_stop_at_is_refused_too(self) -> None:
        self.seed_ledger("0.0899")
        self.ledger.joinpath("stage_B.json").write_text(json.dumps({"started_utc": "2026-01-01T00:00:00.000Z", "spent_start": "0"}))
        outcome = self.drive(["lightrag"])
        self.assertEqual(outcome.rc, 1)
        self.assertEqual(outcome.spy.calls, [])
        self.assertIn("stop at USD 0.09", self.report()[0]["reason"])

    def test_a_refusal_in_the_middle_keeps_the_first_result_and_starts_nothing_more(self) -> None:
        self.paid.completion_tokens = 2_900_000                              # 1.45 USD for one call: under D's 1.5, the first builder spends it
        self.extra["lightrag"] = ["--fake-calls", "1"]
        self.write_all()
        outcome = self.drive(["lightrag", "fast"], stage="D")
        self.assertEqual(outcome.rc, 1, outcome.err)
        self.assertEqual(len(outcome.spy.runners()), 1)
        first, second = self.report()
        self.assertEqual((first["outcome"], second["outcome"]), ("completed", "refused"))
        self.assertEqual(second["not_started"], ["fast"])
        self.assertFalse((self.out / "D-r1-fast").exists())

    def test_a_ledger_line_whose_cost_cannot_be_read_and_a_damaged_state_file_refuse(self) -> None:
        self.ledger.mkdir(mode=0o700)
        (self.ledger / "meter.jsonl").write_text('{"cost": "0.001"}\n{"cost": "oops"}\n')
        outcome = self.drive(["lightrag"])
        self.assertEqual(outcome.rc, 1)
        self.assertIn("cannot be read", self.report()[0]["reason"])
        self.assertEqual(outcome.spy.calls, [])
        shutil.rmtree(self.out)
        (self.ledger / "meter.jsonl").unlink()
        (self.ledger / "stage_B.json").write_text("not json")
        outcome = self.drive(["lightrag"])
        self.assertEqual(outcome.rc, 1)
        self.assertIn("damaged", outcome.err)
        self.assertEqual(outcome.spy.calls, [])
        for text in ('{"started_utc": "2026-11-02T20:00:00.000Z", "spent_start": "-1"}',
                     '{"started_utc": "not a time", "spent_start": "0"}', '{"started_utc": "2026-11-02T20:00:00.000Z"}'):
            (self.ledger / "stage_B.json").write_text(text)
            outcome = self.drive(["lightrag"], label="r2")
            self.assertEqual((outcome.rc, outcome.spy.calls), (1, []), text)
            self.assertIn("damaged", outcome.err)

    def test_a_poll_interval_that_is_not_positive_is_refused_before_anything_starts(self) -> None:
        for poll in ("0", "-1"):
            with self.subTest(poll=poll):
                outcome = self.drive(["lightrag"], poll=poll)
                self.assertEqual(outcome.rc, 1)
                self.assertIn("--poll-s", outcome.err)
                self.nothing_was_started_or_written(outcome)

    def test_a_run_label_that_already_exists_is_refused_before_anything_starts(self) -> None:
        (self.out / "B-r1-fast").mkdir(parents=True)
        outcome = self.drive(["lightrag", "fast"])
        self.assertEqual(outcome.rc, 1)
        self.assertEqual(outcome.spy.calls, [])
        self.assertIn("B-r1-fast", outcome.err)
        self.assertFalse((self.out / "B-r1-lightrag").exists())             # not even the builder before it
        self.assertEqual(self.paid.requests, [])
        dry = self.drive(["lightrag", "fast"], send=False)
        self.assertEqual(dry.rc, 1)
        self.assertIn("already exists", dry.out)

    def test_a_label_used_by_an_earlier_invocation_cannot_be_used_again(self) -> None:
        self.assertEqual(self.drive(["lightrag"]).rc, 0)
        again = self.drive(["lightrag"])
        self.assertEqual(again.rc, 1)
        self.assertEqual(again.spy.calls, [])
        self.assertEqual(len(self.report()), 1)
        self.assertEqual(self.drive(["lightrag"], label="r2").rc, 0)           # another label is another run

    def test_a_second_driver_on_the_same_ledger_is_refused_by_the_lock(self) -> None:
        self.ledger.mkdir(mode=0o700)
        fd = os.open(self.ledger / "stage.lock", os.O_RDWR | os.O_CREAT, 0o600)
        self.addCleanup(os.close, fd)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        outcome = self.drive(["lightrag"])
        self.assertEqual(outcome.rc, 1)
        self.assertIn("another stage run", outcome.err)
        self.assertEqual(outcome.spy.calls, [])
        self.assertFalse(self.out.exists())
        fcntl.flock(fd, fcntl.LOCK_UN)
        self.assertEqual(self.drive(["lightrag"]).rc, 0)                       # the lock is not left behind by a refused run

    def test_a_builder_that_is_named_twice_or_not_configured_is_refused(self) -> None:
        self.assertEqual(self.drive(["lightrag", "lightrag"]).rc, 1)
        config = self.config_dict()
        config["builders"] = {"fast": config["builders"]["fast"]}
        self.cfg_path.write_text(json.dumps(config))
        outcome = self.drive(["lightrag"])
        self.assertEqual(outcome.rc, 1)
        self.assertIn("not in the builders config", outcome.err)
        self.assertEqual(outcome.spy.calls, [])


class ConfigTests(StageCase):
    def refused(self, config: dict, needle: str, **kw) -> None:
        self.cfg_path.write_text(json.dumps(config) if not isinstance(config, str) else config)
        for send in (False, True):
            with self.subTest(needle=needle, send=send):
                outcome = self.drive(["lightrag"], send=send, **kw)
                self.assertEqual(outcome.rc, 1, outcome.out)
                self.assertIn(needle, outcome.err)
                self.assertEqual(outcome.spy.calls, [])
                self.assertFalse(self.out.exists())
                for secret in (CANARY, str(self.key_file)):
                    self.assertNotIn(secret, outcome.err)

    def test_unknown_keys_missing_keys_and_duplicates_are_refused_at_every_level(self) -> None:
        base = self.config_dict()
        self.refused({**base, "chat_modle": "x"}, "chat_modle")                                   # a typo is not ignored
        c = copy.deepcopy(base)
        c["builders"]["lightrag"]["isolated_"] = True
        self.refused(c, "isolated_")
        for key in ps.CONFIG_KEYS:
            self.refused({k: v for k, v in base.items() if k != key}, key)
        for key in ps.BUILDER_KEYS:
            c = copy.deepcopy(base)
            del c["builders"]["lightrag"][key]
            self.refused(c, key)
        c = copy.deepcopy(base)
        c["builders"]["gemini"] = c["builders"]["lightrag"]
        self.refused(c, "gemini")
        self.refused(json.dumps(base).replace('"chat_model"', '"chat_model": "a", "chat_model"', 1), "twice")
        self.refused("{not json", "not valid JSON")
        self.refused([1], "JSON object")

    def test_odd_values_are_refused(self) -> None:
        base = self.config_dict()

        def changed(path: str, value: object) -> dict:
            c = copy.deepcopy(base)
            node = c
            *parents, last = path.split(".")
            for p in parents:
                node = node[p]
            node[last] = value
            return c

        L = "builders.lightrag."
        cases = [
            ("repo_root", "relative/dir", "absolute"), ("repo_root", str(self.root / "nowhere"), "not a directory"),
            ("repo_root", str(self.root), "metering_gateway"), ("corpus", str(self.root / "nowhere.json"), "not a file"),
            ("local_upstream_url", "https://api.example.com/v1", "loopback"), ("local_upstream_url", "http://u:p@127.0.0.1/v1", "loopback"),
            ("chat_model", EMBED, "differ"), ("chat_model", "bad name!", "model name"),
            (L + "python", str(self.root / "no-python"), "not a file"), (L + "python", str(self.root / "documents.tsv"), "not executable"),
            (L + "runner", "../fake_runner.py", "file name"), (L + "runner", "missing.py", "not a file in tools/exp"),
            (L + "isolated", "yes", "true or false"), (L + "isolated", 1, "true or false"),
            (L + "tiktoken_cache", str(self.root / "nowhere"), "not a directory"),
            (L + "env", ["HOME"], "JSON object"), (L + "env", {"PATH": "/bin"}, "PATH"),
            (L + "env", {"OPENAI_API_KEY": "x"}, "credential"), (L + "env", {"MY_TOKEN": "x"}, "credential"),
            (L + "env", {"HOME": "sk-" + "a" * 30}, "looks like a key"), (L + "env", {"HOME": 5}, "text"),
            (L + "env", {"bad name": "x"}, "variable name"),
            (L + "extra_args", "--llm-max-async 4", "list"), (L + "extra_args", ["--llm-max-async", 4], "non-empty text"),
            (L + "extra_args", ["--hosted-profile", "x"], "set by the driver"), (L + "extra_args", ["--workdir=/x"], "--workdir"),
            (L + "extra_args", ["--checkpoints", "20"], "--checkpoints"), (L + "extra_args", ["--tiktoken-cache", "x"], "--tiktoken-cache"),
            (L + "extra_args", ["sk-" + "a" * 30], "looks like a key"),
        ]
        for path, value, needle in cases:
            self.refused(changed(path, value), needle)
        c = copy.deepcopy(base)
        c["builders"]["lightrag"]["env"]["TIKTOKEN_CACHE_DIR"] = str(self.root / "tiktoken")      # TOKEN inside TIKTOKEN is no credential
        self.cfg_path.write_text(json.dumps(c))
        self.assertEqual(ps.load_config(self.cfg_path).builders["lightrag"].env["TIKTOKEN_CACHE_DIR"], str(self.root / "tiktoken"))

    def test_a_bad_profile_a_bad_label_and_paths_inside_the_repository_are_refused(self) -> None:
        self.profile_over = {"allowence_usd": "1"}
        self.write_all()
        outcome = self.drive(["lightrag"])
        self.assertEqual((outcome.rc, outcome.spy.calls), (1, []))
        self.assertIn("allowence_usd", outcome.err)
        self.profile_over = {}
        self.write_all()
        for label in ("../x", "", "a b", "x" * 40, ".hidden"):
            self.assertEqual(self.drive(["lightrag"], label=label, send=False).rc, 1, label)
        inside = self.repo / "profile.json"
        inside.write_text(self.profile_path.read_text())
        self.profile_path = inside
        outcome = self.drive(["lightrag"], send=False)
        self.assertEqual(outcome.rc, 1)
        self.assertIn("inside the repository", outcome.err)
        self.write_all()
        self.out = self.repo / "out"
        outcome = self.drive(["lightrag"], send=False)
        self.assertIn("inside the repository", outcome.err)
        self.out = self.root / "out"
        self.profile_over = {"ledger_dir": str(self.repo / "ledger")}
        self.write_all()
        self.assertIn("inside the repository", self.drive(["lightrag"], send=False).err)

    def test_the_example_holds_placeholders_only_and_runs_once_they_are_filled(self) -> None:
        example = HERE / "passb_builders.example.json"
        text = example.read_text()
        for forbidden in ("/Users", "/private", "/home/", "sk-", "@"):
            self.assertNotIn(forbidden, text)
        raw = json.loads(text)
        self.assertEqual(set(raw), set(ps.CONFIG_KEYS))
        self.assertEqual(set(raw["builders"]), set(ps.BUILDERS))
        self.cfg_path.write_text(text)
        with self.assertRaises(ps.ConfigError):                               # as it stands it cannot run
            ps.load_config(self.cfg_path)
        flags = {"lightrag": ("--llm-max-async", "--llm-timeout"), "fast": ("--llm-concurrency", "--llm-timeout-s"),
                 "ms": ("--concurrency", "--request-timeout-s", "--child-timeout-s"), "nano": ("--max-async", "--client-timeout-s")}
        for name, item in raw["builders"].items():
            source = (HERE / item["runner"]).read_text()                      # the real runner it names accepts every flag it is given
            for flag in flags[name]:
                self.assertIn(f'"{flag}"', source, (name, flag))
                self.assertIn(flag, item["extra_args"])
            args = item["extra_args"]
            self.assertEqual(args[args.index(flags[name][0]) + 1], "4")      # concurrency 4 for every builder (the plan)
        timeouts = {n: dict(zip(i["extra_args"][::2], i["extra_args"][1::2])) for n, i in raw["builders"].items()}
        self.assertEqual(timeouts["lightrag"]["--llm-timeout"], "1800")
        self.assertEqual(timeouts["nano"]["--client-timeout-s"], "3600")
        self.assertEqual((timeouts["ms"]["--request-timeout-s"], timeouts["ms"]["--child-timeout-s"]), ("3600", "43200"))
        self.assertEqual(timeouts["fast"]["--llm-timeout-s"], "3600")
        self.assertEqual((raw["builders"]["lightrag"]["isolated"], raw["builders"]["ms"]["isolated"]), (True, True))
        for name in raw["builders"].values():                                  # fill the placeholders with real things
            (self.repo / "tools" / "exp" / name["runner"]).write_text("")
        filled = copy.deepcopy(raw)
        filled.update(repo_root=str(self.repo), corpus=str(self.root / "corpus.json"), documents=str(self.root / "documents.tsv"))
        for item in filled["builders"].values():
            item.update(python=sys.executable, tiktoken_cache=str(self.root / "tiktoken"))
            item["env"] = {k: (str(self.root / "home") if k in ("HOME", "TMPDIR") else v) for k, v in item["env"].items()}
        self.cfg_path.write_text(json.dumps(filled))
        config = ps.load_config(self.cfg_path)
        self.assertEqual(set(config.builders), set(ps.BUILDERS))
        self.assertEqual(config.chat_model, "gpt-6-luna")


class RunTests(StageCase):
    def test_two_builders_run_one_after_another_with_the_profile_the_environment_and_the_reports_the_brief_asks_for(self) -> None:
        with mock.patch.dict(os.environ, {"PB_STAGE_PARENT_ONLY": "visible-in-the-parent"}):
            outcome = self.drive(["lightrag", "fast"])
        self.assertEqual(outcome.rc, 0, outcome.err)
        r1, r2 = outcome.spy.runners()
        w1, w2 = outcome.spy.watchdogs()
        # the runner: own session, exactly the configured environment plus PATH, the stage's checkpoints, the config's arguments
        label1, label2 = self.out / "B-r1-lightrag", self.out / "B-r1-fast"
        for call, label, name in ((r1, label1, "lightrag"), (r2, label2, "fast")):
            kw, argv = call["kwargs"], call["argv"]
            self.assertIs(kw["start_new_session"], True)
            self.assertEqual(kw["env"], {"PATH": RUNNER_PATH, **self.config_dict()["builders"][name]["env"]})
            self.assertNotIn("PB_STAGE_PARENT_ONLY", kw["env"])
            self.assertEqual(Path(kw["cwd"]), label)
            self.assertEqual(argv[0], sys.executable)
            self.assertEqual("-I" in argv, self.isolated[name])
            self.assertEqual(opt(argv, "--hosted-profile"), str(label / "profile.json"))
            self.assertEqual(opt(argv, "--workdir"), str(label / "work"))
            self.assertEqual(opt(argv, "--out"), str(label / "result.json"))
            self.assertEqual(opt(argv, "--checkpoints"), "1")
            self.assertEqual(opt(argv, "--tiktoken-cache"), str(self.root / "tiktoken"))
            self.assertEqual(opt(argv, "--upstream-url"), self.local.base_url)
            self.assertEqual((opt(argv, "--model"), opt(argv, "--embed-model")), (CHAT, EMBED))
            self.assertEqual(opt(argv, "--repo-root"), str(self.repo))
            self.assertEqual(argv[-2:], ["--fake-calls", "2"])                 # the config's extra arguments, last
            self.assertEqual(kw["stdin"], subprocess.DEVNULL)
        # the watchdog beside it
        state = self.state()
        self.assertTrue(state["started_utc"].endswith("Z"))
        for call, runner_call in ((w1, r1), (w2, r2)):
            argv = call["argv"]
            self.assertEqual(argv[1], "-I")
            self.assertEqual(Path(argv[2]).name, "passb_watchdog.py")
            self.assertEqual(opt(argv, "--gateway-dir"), str(self.ledger))
            self.assertEqual(opt(argv, "--stop-at-usd"), "0.09")
            self.assertEqual(opt(argv, "--since"), state["started_utc"])
            self.assertEqual(opt(argv, "--kill-pgid"), str(runner_call["proc"].pid))
            self.assertEqual(opt(argv, "--poll-s"), "0.2")
            self.assertEqual(call["kwargs"]["env"], {"PATH": "/usr/bin:/bin"})
            self.assertIs(call["kwargs"]["start_new_session"], True)        # it outlives a group signal aimed at this program
        self.assertEqual(opt(w1["argv"], "--report"), str(label1 / "watchdog.json"))
        # the run profiles: the stage profile with the pre-flight's allowance, key file and ledger unchanged, mode 600
        p1, p2 = self.run_profile("B-r1-lightrag"), self.run_profile("B-r1-fast")
        spent_after_first = CALL_COST * 2
        self.assertEqual(p1["allowance_usd"], "0.2")                          # the stage's limit; the stage profile said 0.05
        self.assertEqual(Decimal(p2["allowance_usd"]), Decimal("0.20") - spent_after_first)
        for p in (p1, p2):
            self.assertEqual((p["key_file"], p["ledger_dir"]), (str(self.key_file), str(self.ledger)))
            self.assertEqual((p["input_per_mtok"], p["output_per_mtok"]), ("0.1", "0.5"))
            self.assertEqual(p["request_defaults"], {"reasoning_effort": "none"})
            self.assertEqual(pb.load_profile(self.out / "B-r1-lightrag" / "profile.json").output_limit_default, 6144)
        for name in ("profile.json", "runner.stdout.log", "runner.stderr.log", "watchdog.stdout.log", "watchdog.stderr.log"):
            self.assertEqual(stat.S_IMODE(os.stat(label1 / name).st_mode), 0o600, name)
        # the runner really ran in its own session, with that environment, and made its calls through the gateway
        for label, name in ((label1, "lightrag"), (label2, "fast")):
            result = json.loads((label / "result.json").read_text())
            self.assertEqual((result["pid"], result["pgid"]), (result["pid"], result["pid"]))      # its group id is its pid
            self.assertNotEqual(result["pgid"], os.getpgrp())
            self.assertEqual(result["isolated"], int(self.isolated[name]))
            self.assertNotIn("PB_STAGE_PARENT_ONLY", result["environ"])
            self.assertEqual(result["environ"]["HOME"], str(self.root / "home"))
            self.assertEqual(result["environ"]["PATH"], RUNNER_PATH)
            self.assertEqual(result["hosted"]["calls_in_this_run"], 2)
        self.assertEqual(len(self.paid.chat_requests()), 4)
        self.assertEqual({r["authorization"] for r in self.paid.chat_requests()}, {"Bearer " + CANARY})   # the gateway sent the key
        for call in outcome.spy.runners() + outcome.spy.watchdogs():       # nothing is left running
            self.assertIsNotNone(call["proc"].poll())
        self.assertEqual(len(outcome.spy.final_reads()), 2)                # one last read per builder
        # the reports and the state file
        first, second = self.report()
        for entry, label, builder in ((first, "B-r1-lightrag", "lightrag"), (second, "B-r1-fast", "fast")):
            self.assertEqual((entry["stage"], entry["run_label"], entry["label"], entry["builder"], entry["outcome"]),
                             ("B", "r1", label, builder, "completed"))
            self.assertEqual((entry["exit_status"], entry["tripped_rules"], entry["left_processes"]), (0, [], False))
            self.assertEqual(entry["spent_usd"], pb.money_text(CALL_COST * 2))
            self.assertEqual(entry["stop_at_usd"], "0.09")
            self.assertEqual(entry["result_file"], f"{label}/result.json")
            self.assertLessEqual(entry["started_utc"], entry["finished_utc"])
        for call, entry in ((w1, first), (w2, second)):                       # the repeat window is THIS run's start, not the stage's
            self.assertEqual(opt(call["argv"], "--repeat-since"), entry["started_utc"])
        self.assertLess(first["started_utc"], second["started_utc"])
        self.assertEqual(first["allowance_usd"], "0.2")
        self.assertEqual(Decimal(second["allowance_usd"]), Decimal("0.20") - spent_after_first)
        self.assertEqual(first["spent_in_stage_usd"], pb.money_text(CALL_COST * 2))
        self.assertEqual(second["spent_in_stage_usd"], pb.money_text(CALL_COST * 4))
        self.assertEqual((state["spent_start"], state["stage"]), ("0", "B"))
        self.assertEqual([r["label"] for r in state["runs"]], ["B-r1-lightrag", "B-r1-fast"])
        self.assertEqual(pf.ledger_spent(self.ledger)[0], CALL_COST * 4)       # the ledger is one file for both runs
        for private_dir in (self.out, label1, label2):                    # they will hold article text and local paths
            self.assertEqual(stat.S_IMODE(os.stat(private_dir).st_mode), 0o700, private_dir.name)
        self.assertEqual(stat.S_IMODE(os.stat(self.out / "stage_report.json").st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(os.stat(self.ledger / "stage_B.json").st_mode), 0o600)
        self.assertIn("completed", outcome.out)

    def test_the_reports_hold_no_path_outside_the_out_dir_and_no_absolute_path_at_all(self) -> None:
        self.paid.reasoning_tokens = 0
        self.assertEqual(self.drive(["lightrag", "fast"]).rc, 0)
        self.extra["ms"] = ["--fake-calls", "40", "--fake-sleep", "0.2", "--fake-child"]
        self.paid.reasoning_tokens = 5
        self.write_all()
        self.assertEqual(self.drive(["ms"], label="r2").rc, 3)                   # a tripped entry too
        text = (self.out / "stage_report.json").read_text()
        self.assertEqual(len(json.loads(text)["entries"]), 3)
        for needle in (str(self.root), str(self.ledger), str(self.key_file), str(HERE), "/tmp", "/var/", "/Users", "provider.key"):
            self.assertNotIn(needle, text)

        def strings(node):
            if isinstance(node, str):
                yield node
            elif isinstance(node, dict):
                for k, v in node.items():
                    yield k
                    yield from strings(v)
            elif isinstance(node, list):
                for v in node:
                    yield from strings(v)

        self.assertEqual([s for s in strings(json.loads(text)) if s.startswith("/") or ":\\" in s], [])
        state = (self.ledger / "stage_B.json").read_text()
        self.assertNotIn(str(self.root), state)

    def test_a_second_run_of_the_stage_shares_the_stage_spend_its_window_and_its_allowance(self) -> None:
        self.paid.completion_tokens = 100_000                                  # 0.05012 USD a call
        self.extra["lightrag"] = ["--fake-calls", "2"]
        self.write_all()
        per_call = Decimal("0.05012")
        first = self.drive(["lightrag"], stage="C", label="r1")
        self.assertEqual(first.rc, 0, first.err)
        second = self.drive(["lightrag"], stage="C", label="r2")
        self.assertEqual(second.rc, 0, second.err)
        w1, w2 = first.spy.watchdogs()[0]["argv"], second.spy.watchdogs()[0]["argv"]
        state = self.state("C")
        self.assertEqual(opt(w1, "--since"), state["started_utc"])
        self.assertEqual(opt(w2, "--since"), state["started_utc"])               # the stage's window, not this run's start
        self.assertEqual((opt(w1, "--stop-at-usd"), opt(w2, "--stop-at-usd")), ("0.6", "0.6"))
        self.assertEqual(opt(first.spy.runners()[0]["argv"], "--checkpoints"), "5")
        p1, p2 = self.run_profile("C-r1-lightrag"), self.run_profile("C-r2-lightrag")
        self.assertEqual(p1["allowance_usd"], "0.6")
        self.assertEqual(Decimal(p2["allowance_usd"]), Decimal("0.60") - 2 * per_call)      # what the first run spent is gone from it
        self.assertEqual(state["spent_start"], "0")
        r1, r2 = self.report()
        self.assertEqual((r1["label"], r2["label"]), ("C-r1-lightrag", "C-r2-lightrag"))
        self.assertEqual(r1["spent_in_stage_usd"], pb.money_text(2 * per_call))
        self.assertEqual(r2["spent_in_stage_usd"], pb.money_text(4 * per_call))
        self.assertEqual([r["label"] for r in state["runs"]], ["C-r1-lightrag", "C-r2-lightrag"])

    def test_the_run_profile_carries_the_max_tokens_translation_flag_so_a_runner_gets_it(self) -> None:
        self.assertEqual(self.drive(["lightrag"]).rc, 0)
        self.assertIs(self.run_profile("B-r1-lightrag")["translate_max_tokens"], False)
        self.profile_over = {"translate_max_tokens": True}
        self.write_all()
        self.assertEqual(self.drive(["lightrag"], label="r2").rc, 0)
        run_profile = self.run_profile("B-r2-lightrag")
        self.assertIs(run_profile["translate_max_tokens"], True)
        self.assertIs(pb.load_profile(self.out / "B-r2-lightrag" / "profile.json").translate_max_tokens, True)

    def test_the_signal_handlers_are_put_back_when_the_driver_returns(self) -> None:
        before = (signal.getsignal(signal.SIGINT), signal.getsignal(signal.SIGTERM))
        self.assertEqual(self.drive(["lightrag"]).rc, 0)
        self.assertEqual((signal.getsignal(signal.SIGINT), signal.getsignal(signal.SIGTERM)), before)

    def test_the_trip_report_keeps_a_watchdog_error_and_drops_a_rule_it_does_not_know(self) -> None:
        path = self.root / "wd.json"
        path.write_text(json.dumps({"trips": [{"rule": "watchdog_error", "counts": {"consecutive_poll_errors": 3}},
                                              {"rule": "a made-up rule", "counts": {"x": 1}}]}))
        self.assertEqual(ps.read_trips(path)[0], [{"rule": "watchdog_error", "counts": {"consecutive_poll_errors": 3}}])

    def test_a_second_run_that_sends_the_first_runs_requests_again_is_not_stopped_as_a_retry_loop(self) -> None:
        """Stage C is run twice on the same documents. The dress rehearsal with the real LightRAG found the second run stopped
        within a second by the repeat rule, because its requests are the first run's, byte for byte."""
        self.extra["lightrag"] = ["--fake-calls", "25", "--fake-body", "same_across_runs"]
        self.write_all()
        first = self.drive(["lightrag"], stage="C", label="r1")
        second = self.drive(["lightrag"], stage="C", label="r2")
        self.assertEqual((first.rc, second.rc), (0, 0), first.err + second.err)
        r1, r2 = self.report()
        self.assertEqual(([r1["outcome"], r2["outcome"]], [r1["tripped_rules"], r2["tripped_rules"]]),
                         (["completed", "completed"], [[], []]))
        hashes = [json.loads(line)["request_sha256"] for line in (self.ledger / "meter.jsonl").read_text().splitlines()]
        self.assertEqual((len(hashes), len(set(hashes))), (50, 25))             # without the window: 25 repeats in 50 records

    def test_a_run_that_repeats_its_own_requests_is_still_stopped(self) -> None:
        self.extra["lightrag"] = ["--fake-calls", "25", "--fake-body", "constant"]
        self.write_all()
        outcome = self.drive(["lightrag"], stage="C", label="r1")
        self.assertEqual(outcome.rc, 3, outcome.err)
        (entry,) = self.report()
        self.assertEqual(entry["outcome"], "tripped")
        self.assertIn("repeated_requests", [t["rule"] for t in entry["tripped_rules"]])

    def test_a_later_stage_starts_its_own_window_at_the_ledgers_spend_and_ignores_the_earlier_stage(self) -> None:
        self.assertEqual(self.drive(["lightrag"], stage="B").rc, 0)
        self.assertEqual(self.drive(["lightrag"], stage="C", label="r1").rc, 0)
        b, c = self.state("B"), self.state("C")
        self.assertEqual(b["spent_start"], "0")
        self.assertEqual((b["stage"], c["stage"]), ("B", "C"))
        self.assertEqual(Decimal(c["spent_start"]), CALL_COST * 2)             # B's spend is not C's
        self.assertEqual(self.report()[1]["spent_in_stage_usd"], pb.money_text(CALL_COST * 2))
        self.assertEqual(self.run_profile("C-r1-lightrag")["allowance_usd"], "0.6")

    def test_earlier_stages_calls_do_not_count_for_the_watchdog_of_a_later_one(self) -> None:
        self.seed_ledger("0.095")                                             # a stage that spent more than this stage's stop at
        outcome = self.drive(["lightrag"])
        self.assertEqual(outcome.rc, 0, outcome.err)
        (entry,) = self.report()
        self.assertEqual((entry["outcome"], entry["tripped_rules"]), ("completed", []))
        self.assertEqual(entry["spent_usd"], pb.money_text(CALL_COST * 2))
        argv = outcome.spy.watchdogs()[0]["argv"]
        self.assertIn("--since", argv)
        self.assertGreater(opt(argv, "--since"), "2026-01-01T00:00:00.000Z")
        self.assertEqual(opt(outcome.spy.final_reads()[0]["argv"], "--since"), opt(argv, "--since"))

    def test_a_runner_failing_by_its_own_fault_is_a_result_and_the_next_builder_runs(self) -> None:
        self.extra["lightrag"] = ["--fake-calls", "2", "--fake-exit", "7", "--fake-marker", str(self.marker("m1"))]
        self.extra["fast"] = ["--fake-calls", "2", "--fake-marker", str(self.marker("m2"))]
        self.write_all()
        outcome = self.drive(["lightrag", "fast"])
        self.assertEqual(outcome.rc, 0, outcome.err)
        first, second = self.report()
        self.assertEqual((first["outcome"], first["exit_status"], first["tripped_rules"]), ("builder_failed", 7, []))
        self.assertEqual((second["outcome"], second["exit_status"]), ("completed", 0))
        self.assertTrue(self.marker("m1").exists() and self.marker("m2").exists())
        self.assertEqual(len(outcome.spy.runners()), 2)
        self.assertEqual(first["result_file"], "B-r1-lightrag/result.json")
        self.assertEqual([r["outcome"] for r in self.state()["runs"]], ["builder_failed", "completed"])
        self.assertNotIn("STOPPED", outcome.err)

    def test_a_runner_that_dies_before_writing_anything_is_its_own_failure_with_no_result_file(self) -> None:
        self.extra["lightrag"] = ["--fake-calls", "0", "--fake-exit", "3", "--fake-nowrite"]
        self.write_all()
        outcome = self.drive(["lightrag"])
        self.assertEqual(outcome.rc, 0)
        (entry,) = self.report()
        self.assertEqual((entry["outcome"], entry["exit_status"], entry["spent_usd"], entry["result_file"]),
                         ("builder_failed", 3, "0", None))
        self.assertFalse((self.out / "B-r1-lightrag" / "result.json").exists())

    def test_a_process_the_runner_leaves_behind_is_terminated_and_recorded(self) -> None:
        self.extra["lightrag"] = ["--fake-calls", "1", "--fake-child"]
        self.write_all()
        outcome = self.drive(["lightrag"])
        self.assertEqual(outcome.rc, 0, outcome.err)
        child = self.pids("B-r1-lightrag")["child"]
        self.assertTrue(wait_for(lambda: not alive(child), 10))
        (entry,) = self.report()
        self.assertTrue(entry["left_processes"])
        self.assertEqual(entry["outcome"], "completed")


class TripTests(StageCase):
    def test_a_trip_stops_the_runner_and_its_child_ends_the_stage_with_3_and_the_next_builder_never_starts(self) -> None:
        self.paid.reasoning_tokens = 7
        self.extra["lightrag"] = ["--fake-calls", "60", "--fake-sleep", "0.3", "--fake-child", "--fake-marker", str(self.marker("m1"))]
        self.extra["fast"] = ["--fake-calls", "2", "--fake-marker", str(self.marker("m2"))]
        self.write_all()
        started = time.monotonic()
        outcome = self.drive(["lightrag", "fast"])
        self.assertEqual(outcome.rc, 3, outcome.err)
        self.assertLess(time.monotonic() - started, 60)                           # it did not wait for 60 slow calls
        info = self.pids("B-r1-lightrag")
        self.assertTrue(wait_for(lambda: not alive(info["pid"]), 10), "the runner is still alive")
        self.assertTrue(wait_for(lambda: not alive(info["child"]), 10), "the runner's child is still alive")
        self.assertFalse(self.marker("m2").exists())                              # the next builder never started
        self.assertFalse((self.out / "B-r1-fast").exists())
        self.assertEqual(len(outcome.spy.runners()), 1)
        (entry,) = self.report()
        self.assertEqual(entry["outcome"], "tripped")
        self.assertLess(entry["exit_status"], 0)                                  # ended by a signal
        (trip,) = entry["tripped_rules"]
        self.assertEqual(set(trip), {"rule", "counts"})                           # names and counts only
        self.assertEqual(trip["rule"], "reasoning_tokens")
        self.assertGreaterEqual(trip["counts"]["responses_with_reasoning_tokens"], 1)
        self.assertTrue((self.out / "B-r1-lightrag" / "watchdog.json").exists())
        self.assertIn("STOPPED", outcome.err)
        self.assertIn("fast", outcome.err)
        self.assertEqual([r["outcome"] for r in self.state()["runs"]], ["tripped"])
        self.assertLess(len(self.paid.chat_requests()), 60)

    def test_repeating_a_stage_after_a_trip_trips_at_once_until_the_state_file_is_moved_aside_and_then_opens_a_new_window(self) -> None:
        self.paid.reasoning_tokens = 3
        self.extra["lightrag"] = ["--fake-calls", "2"]
        self.write_all()
        self.assertEqual(self.drive(["lightrag"]).rc, 3)
        self.paid.reasoning_tokens = 0                                            # the cause is fixed
        again = self.drive(["lightrag"], label="r2")
        self.assertEqual(again.rc, 3, again.err)                                  # the old window still holds the tripped call
        self.assertEqual(self.report()[-1]["tripped_rules"][0]["rule"], "reasoning_tokens")
        (self.ledger / "stage_B.json").rename(self.ledger / "stage_B.json.tripped-1")
        fresh = self.drive(["lightrag"], label="r3")
        self.assertEqual(fresh.rc, 0, fresh.err)
        entry = self.report()[-1]
        self.assertEqual((entry["outcome"], entry["tripped_rules"]), ("completed", []))
        spent_now = pf.ledger_spent(self.ledger)[0]
        self.assertGreater(spent_now, Decimal(entry["spent_usd"]))                # the tripped runs' spend is in the ledger
        self.assertEqual(Decimal(self.state()["spent_start"]), spent_now - Decimal(entry["spent_usd"]))   # the window opened after it
        self.assertTrue((self.ledger / "stage_B.json.tripped-1").exists())         # the old window is kept as the record

    def test_a_call_written_in_the_last_moments_before_the_runner_exits_is_still_caught(self) -> None:
        self.paid.reasoning_tokens = 3
        self.extra["lightrag"] = ["--fake-calls", "2"]                            # the runner exits at once, with status 0
        self.extra["fast"] = ["--fake-calls", "2", "--fake-marker", str(self.marker("m2"))]
        self.write_all()
        outcome = self.drive(["lightrag", "fast"], poll="120")                      # the live watchdog's next look is two minutes away
        self.assertEqual(outcome.rc, 3, outcome.err)
        self.assertEqual(len(outcome.spy.final_reads()), 1)
        (entry,) = self.report()
        self.assertEqual((entry["outcome"], entry["exit_status"]), ("tripped", 0))
        self.assertEqual(entry["tripped_rules"][0]["rule"], "reasoning_tokens")
        self.assertFalse(self.marker("m2").exists())

    def test_the_final_read_uses_the_same_window_rules_and_report_as_the_live_watchdog(self) -> None:
        outcome = self.drive(["lightrag"])
        self.assertEqual(outcome.rc, 0)
        live, final = outcome.spy.watchdogs()[0]["argv"], outcome.spy.final_reads()[0]["argv"]
        for flag in ("--gateway-dir", "--stop-at-usd", "--since", "--repeat-since", "--report"):
            self.assertEqual(opt(live, flag), opt(final, flag))
        self.assertEqual(opt(final, "--max-seconds"), "0")
        self.assertNotIn("--kill-pgid", final)
        self.assertEqual(outcome.spy.final_reads()[0]["kwargs"]["env"], {"PATH": "/usr/bin:/bin"})     # no parent environment

    def test_a_watchdog_that_ends_by_itself_while_the_runner_lives_leaves_no_run_unguarded(self) -> None:
        self.extra["lightrag"] = ["--fake-calls", "1", "--fake-hang", "--fake-child"]
        self.extra["fast"] = ["--fake-marker", str(self.marker("m2"))]
        self.write_all()

        pids_file = self.out / "B-r1-lightrag" / "work" / "pids.json"
        code = ("import os, sys, time\nend = time.time() + 90\n"
                f"while time.time() < end and not os.path.exists({str(pids_file)!r}):\n    time.sleep(0.1)\nsys.exit(2)\n")

        def dead_guard(argv: list[str]) -> list[str]:        # a guard that ends by itself once the runner is up
            return [sys.executable, "-c", code] if "--kill-pgid" in argv else argv

        started = time.monotonic()
        outcome = self.drive(["lightrag", "fast"], override=dead_guard)
        self.assertEqual(outcome.rc, 3, outcome.err)
        self.assertLess(time.monotonic() - started, 45)                       # the runner would hang for 60 s on its own
        info = self.pids("B-r1-lightrag")
        self.assertTrue(wait_for(lambda: not alive(info["pid"]) and not alive(info["child"]), 15))
        (entry,) = self.report()
        self.assertEqual(entry["outcome"], "guard_failed")
        self.assertLess(entry["exit_status"], 0)                              # stopped by the driver, not finished by itself
        self.assertFalse(self.marker("m2").exists())

    def test_a_watchdog_that_reports_a_trip_but_did_not_stop_the_runner_is_backed_up_by_the_driver(self) -> None:
        self.extra["lightrag"] = ["--fake-calls", "1", "--fake-hang", "--fake-child"]
        self.extra["fast"] = ["--fake-marker", str(self.marker("m2"))]
        self.write_all()
        pids_file = self.out / "B-r1-lightrag" / "work" / "pids.json"
        code = ("import os, sys, time\nend = time.time() + 90\n"
                f"while time.time() < end and not os.path.exists({str(pids_file)!r}):\n    time.sleep(0.1)\nsys.exit(3)\n")

        def lying_guard(argv: list[str]) -> list[str]:       # exits 3 like a trip, kills nothing, writes no report
            return [sys.executable, "-c", code] if "--kill-pgid" in argv else argv

        started = time.monotonic()
        with mock.patch.object(ps, "TRIP_WAIT_S", 1.0):
            outcome = self.drive(["lightrag", "fast"], override=lying_guard)
        self.assertEqual(outcome.rc, 3, outcome.err)
        self.assertLess(time.monotonic() - started, 45)                       # the runner would hang for 60 s on its own
        info = self.pids("B-r1-lightrag")
        self.assertTrue(wait_for(lambda: not alive(info["pid"]) and not alive(info["child"]), 15))
        (entry,) = self.report()
        self.assertEqual(entry["outcome"], "tripped")
        self.assertLess(entry["exit_status"], 0)                              # stopped by the driver, not finished by itself
        self.assertEqual(entry["tripped_rules"], [{"rule": "unreadable_report", "counts": {}}])
        self.assertFalse(self.marker("m2").exists())

    def test_a_group_stop_never_signals_this_programs_own_group_or_group_0_or_1(self) -> None:
        with mock.patch.object(ps.wd, "terminate_groups") as terminate:
            for pgid in (os.getpgrp(), 0, 1, -5):
                ps.stop_group(pgid)
            terminate.assert_not_called()
            sleeper = subprocess.Popen(["sleep", "60"], start_new_session=True)
            self.addCleanup(lambda: (sleeper.kill(), sleeper.wait()))
            ps.stop_group(sleeper.pid)
            terminate.assert_called_once()
            self.assertEqual(terminate.call_args[0][0], [sleeper.pid])

    def test_a_runner_the_group_kill_did_not_reach_is_killed_by_itself(self) -> None:
        sleeper = subprocess.Popen(["sleep", "60"])                            # no session of its own: its pid is no group id
        self.addCleanup(lambda: (sleeper.kill(), sleeper.wait()))
        started = time.monotonic()
        with mock.patch.object(ps, "STOP_WAIT_S", 0.5):
            ps.stop_runner(sleeper)
        self.assertLess(time.monotonic() - started, 30)                        # killed by itself, not waited out
        self.assertLess(sleeper.returncode, 0)

    def test_a_runner_that_cannot_be_started_stops_the_stage_with_1(self) -> None:
        real = subprocess.Popen

        def refuse_runner(args, *a, **kw):
            if "--hosted-profile" in args:
                raise FileNotFoundError(2, "No such file")
            return real(args, *a, **kw)

        with mock.patch.object(subprocess, "Popen", refuse_runner), contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            rc = ps.main(self.argv(["lightrag", "fast"]))
        self.assertEqual(rc, 1)
        (entry,) = self.report()
        self.assertEqual((entry["outcome"], entry["exit_status"], entry["error"]), ("start_failed", None, "FileNotFoundError"))
        self.assertFalse((self.out / "B-r1-fast").exists())

    def test_the_trip_report_is_reduced_to_rule_names_and_counts(self) -> None:
        path = self.root / "watchdog.json"
        hostile = "ZEBRA-QUILL-7731-text-of-a-body"
        path.write_text(json.dumps({
            "trips": [{"rule": "reasoning_tokens", "message": hostile, "call_ids": ["call1"],
                       "counts": {"responses_with_reasoning_tokens": 3, "spent_usd": "0.0912", "note": hostile,
                                  "bad name": 1, "nested": {"a": 1}, "flag": True, "text": hostile}},
                      {"rule": hostile, "counts": {"n": 1}}, {"rule": ["unhashable"], "counts": {}}, "not a dict"],
            "kill_groups": {"123": "terminated", "456": hostile, "789": ["unhashable"]}}))
        trips, kills = ps.read_trips(path)
        self.assertEqual(trips, [{"rule": "reasoning_tokens", "counts": {"responses_with_reasoning_tokens": 3, "spent_usd": "0.0912"}}])
        self.assertEqual(kills, ["terminated"])
        self.assertNotIn(hostile, json.dumps([trips, kills]))
        self.assertEqual(ps.read_trips(self.root / "missing.json"), ([], []))
        path.write_text("{broken")
        self.assertEqual(ps.read_trips(path), ([], []))


class SecretTests(StageCase):
    def test_the_key_canary_is_in_the_key_file_and_in_the_providers_request_and_nowhere_else(self) -> None:
        self.paid.echo_authorization = True                  # worst case: the provider puts the key it received into its answer
        with OpenSpy() as spy, mock.patch.dict(os.environ, {"PB_STAGE_PARENT_ONLY": "x"}):
            outcome = self.drive(["lightrag", "fast"])
        self.assertEqual(outcome.rc, 0, outcome.err)
        # not vacuous: the provider received the key through the gateway, and the key file holds it
        self.assertEqual({r["authorization"] for r in self.paid.chat_requests()}, {"Bearer " + CANARY})
        self.assertIn(CANARY, self.key_file.read_text())
        # the driver never opened the key file (the spy did see the other files it reads and writes)
        self.assertNotIn(str(self.key_file), spy.opened)
        self.assertTrue(any(p.endswith("meter.jsonl") for p in spy.opened))
        self.assertTrue(any(p.endswith("stage_report.json.tmp") for p in spy.opened))
        # the driver's own output
        self.assertNotIn(CANARY, outcome.out + outcome.err)
        # every argument list and environment it started a process with
        for call in outcome.spy.calls:
            self.assertNotIn(CANARY, " ".join(map(str, call["argv"])))
            self.assertNotIn(CANARY, json.dumps(call["kwargs"].get("env") or {}))
        self.assertFalse([k for k, v in os.environ.items() if CANARY in k or CANARY in v])
        # every file under the out dir (reports, profiles, stdout and stderr files, results with the runner's environment)
        # and under the ledger (the gateway's log, body log and manifests, the state file, the lock)
        scanned = [p for base in (self.out, self.ledger) for p in base.rglob("*") if p.is_file()]
        names = {p.name for p in scanned}
        self.assertTrue({"stage_report.json", "profile.json", "result.json", "runner.stdout.log", "runner.stderr.log",
                         "watchdog.stdout.log", "watchdog.stderr.log", "meter.jsonl", "meter.jsonl.bodies.jsonl", "stage_B.json",
                         "pids.json"} <= names, names)
        self.assertEqual([str(p) for p in scanned if CANARY.encode() in p.read_bytes()], [])
        # the runner's environment and argument list, as it saw them
        for label in ("B-r1-lightrag", "B-r1-fast"):
            result = self.result(label)
            self.assertNotIn(CANARY, json.dumps(result["environ"]) + json.dumps(result["argv"]))
            self.assertNotIn("PB_STAGE_PARENT_ONLY", result["environ"])
        # the process table: no process this test started carries the key on its command line
        listing = subprocess.run(["ps", "-A", "-o", "command="], capture_output=True, text=True).stdout
        self.assertNotIn(CANARY, listing)


class SignalTests(StageCase):
    def driver(self) -> subprocess.Popen:
        self.extra["lightrag"] = ["--fake-calls", "1", "--fake-hang", "--fake-child"]
        self.write_all()
        return subprocess.Popen([sys.executable, "-B", str(SCRIPT), *self.argv(["lightrag", "fast"])],
                                env={"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"}, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True, start_new_session=True)

    @staticmethod
    def stop_driver(proc: subprocess.Popen) -> None:
        """A test that failed before it sent its signal must not leave the driver's runner and watchdog behind: SIGTERM lets the
        driver clean up (a SIGKILL could not be caught), SIGKILL only if it does not."""
        if proc.poll() is None:
            proc.send_signal(signal.SIGTERM)
            try:
                proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
        for stream in (proc.stdout, proc.stderr):
            if stream:
                stream.close()

    def interrupt_with(self, signum: int) -> None:
        proc = self.driver()
        self.addCleanup(self.stop_driver, proc)
        def child_pid():
            try:
                return self.pids("B-r1-lightrag")["child"]
            except (OSError, ValueError, KeyError):
                return None

        self.assertTrue(wait_for(lambda: bool(child_pid()), 90), "the runner never started")
        info = self.pids("B-r1-lightrag")
        self.assertTrue(alive(info["pid"]) and alive(info["child"]))
        window = self.state()                                              # the stage's window is on disk while its first runner runs
        self.assertEqual(window["spent_start"], "0")
        self.assertTrue(window["started_utc"].endswith("Z"))
        proc.send_signal(signum)
        out, err = proc.communicate(timeout=60)
        self.assertEqual(proc.returncode, 128 + signum, err)
        self.assertTrue(wait_for(lambda: not alive(info["pid"]) and not alive(info["child"]), 10), "the runner's group outlived the driver")
        (entry,) = self.report()
        self.assertEqual((entry["outcome"], entry["signal"]), ("interrupted", signum))
        self.assertFalse((self.out / "B-r1-fast").exists())
        time.sleep(0.5)
        listing = subprocess.run(["ps", "-A", "-o", "command="], capture_output=True, text=True).stdout
        self.assertEqual([line for line in listing.splitlines() if str(self.root) in line and "passb_watchdog" in line], [])
        self.assertNotIn(CANARY, out + err)

    def test_sigterm_stops_the_runners_whole_group_and_the_watchdog_before_the_driver_exits(self) -> None:
        self.interrupt_with(signal.SIGTERM)

    def test_sigint_does_the_same(self) -> None:
        self.interrupt_with(signal.SIGINT)


if __name__ == "__main__":
    unittest.main()
