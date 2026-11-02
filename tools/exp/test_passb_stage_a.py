"""Tests for tools/exp/passb_stage_a.py. Standard library only; loopback only; no model, no provider, no real key.

The "provider" is a fake OpenAI-style server written here: it records every request with its Authorization header, answers
with a `usage` that includes `completion_tokens_details.reasoning_tokens`, and can answer 400 to a request shape, 401 to
everything, or a scripted run of statuses. A second fake plays the local embedding upstream, which must never be called.
The gateway is the real one (`tools/metering_gateway.py`), started as a subprocess by `HostedGateway`. The key is a
made-up string assembled at run time and written to a mode-600 file in a temporary directory. The "pass-A directories"
are small synthetic ones, written here with dummy text and one distinctive sentinel per request.

Run from the repository root:

    uv run python -m unittest tools/exp/test_passb_stage_a.py
"""

from __future__ import annotations

import builtins
import contextlib
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import threading
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

import passa_common as pc  # noqa: E402
import passb_common as pb  # noqa: E402
import passb_stage_a as sa  # noqa: E402

CANARY = "sk-" + "canary" + "-" + "Zr4Kq9" + "Lm2Xv7Tj"      # assembled here: the file holds no key-shaped literal
SENT = "ZQXTEXT"                                             # in every recorded request: stands for article text
RESPONSE_SENT = "ZQXREPLY"                                   # in every answer and error message of the fake provider
CHAT = "gpt-6-luna"
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
SYNTHESISED = {"ping", "fast_summary", "nano_entity_summary", "nano_community_report"}
ORDER = ["ping", "lightrag_extraction", "lightrag_gleaning", "fast_extraction", "fast_summary", "ms_extraction",
         "ms_community_report", "nano_extraction", "nano_entity_summary", "nano_community_report"]
UNIT_COST = Decimal("0.00027")           # 1200 prompt tokens at 0.10 and 300 completion tokens at 0.50 per million


class _Server(ThreadingHTTPServer):
    request_queue_size = 64
    daemon_threads = True


class FakeProvider:
    """A loopback server that plays a provider: records requests, answers chat completions as scripted."""

    def __init__(self) -> None:
        self.prompt_tokens, self.completion_tokens, self.reasoning_tokens = 1200, 300, 0
        self.model = "gpt-6-luna-test-1"
        self.extra_prompt_details: dict = {}
        self.echo_authorization = False
        self.statuses: list[int] = []        # one per chat request, consumed first; 200 answers normally
        self.always: int | None = None       # every chat request gets this status
        self.reject = None                   # callable(body) -> error dict (answered 400) or None
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

            def do_POST(self) -> None:  # noqa: N802
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
                with outer._lock:
                    outer.requests.append({"path": self.path, "body": body, "authorization": self.headers.get("Authorization")})
                    scripted = outer.statuses.pop(0) if outer.statuses else None
                if not self.path.endswith("/chat/completions"):
                    return self._send(404, {"error": {"message": "not found"}})
                status = outer.always or scripted or 200
                error = outer.reject(body) if (status == 200 and outer.reject) else None
                if error:
                    return self._send(400, {"error": error})
                if status != 200:
                    return self._send(status, {"error": {"message": f"{RESPONSE_SENT} refused", "type": "server_error",
                                                         "code": "scripted_failure", "param": None}})
                details = {"cached_tokens": 0, **outer.extra_prompt_details}
                usage = {"prompt_tokens": outer.prompt_tokens, "completion_tokens": outer.completion_tokens,
                         "total_tokens": outer.prompt_tokens + outer.completion_tokens,
                         "prompt_tokens_details": details,
                         "completion_tokens_details": {"reasoning_tokens": outer.reasoning_tokens}}
                text = (self.headers.get("Authorization") or "") if outer.echo_authorization else f"{RESPONSE_SENT} ok"
                self._send(200, {"id": "chatcmpl-test", "object": "chat.completion", "model": outer.model,
                                 "choices": [{"index": 0, "finish_reason": "stop",
                                              "message": {"role": "assistant", "content": text}}], "usage": usage})

        self.server = _Server(("127.0.0.1", 0), H)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base_url = f"http://127.0.0.1:{self.server.server_address[1]}/v1"

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()

    def chat_requests(self) -> list[dict]:
        return [r for r in self.requests if r["path"].endswith("/chat/completions")]


def msg(role: str, label: str, pad: int = 0, extra: str = "") -> dict:
    return {"role": role, "content": f"{SENT}-{label}{extra}" + "." * pad}


CHAT_ROUTE = "/v1/chat/completions"
JSON_OBJECT = {"type": "json_object"}


def strict_schema(strict: bool) -> dict:
    return {"type": "json_schema", "json_schema": {"name": "Report", "strict": strict, "schema": {"type": "object"}}}


def write_passa(directory: Path, calls: list[tuple[str, int, dict]]) -> Path:
    """A pass-A gateway directory: meter.jsonl and its body log, in the shape the gateway writes them."""
    directory.mkdir(parents=True)
    with open(directory / "meter.jsonl", "w") as meter, open(directory / "meter.jsonl.bodies.jsonl", "w") as bodies:
        for i, (route, status, body) in enumerate(calls):
            call_id = f"{i:032x}"
            meter.write(json.dumps({"call_id": call_id, "route": route, "http_status": status, "cost": "0"}) + "\n")
            bodies.write(json.dumps({"call_id": call_id, "request": json.dumps(body),
                                     "response": json.dumps({"choices": [{"message": {"content": "x"}}]})}) + "\n")
    return directory


def passa_dirs(root: Path) -> dict[str, Path]:
    """Four synthetic directories with decoys that a wrong rule would pick. The right pick is the one labelled 1."""
    m = "model-in-the-log"
    return {
        "lightrag": write_passa(root / "lightrag", [
            ("/v1/embeddings", 200, {"model": m, "input": [f"{SENT}-embedding"]}),
            (CHAT_ROUTE, 500, {"model": m, "messages": [msg("system", "LR-FAILED"), msg("user", "LR-FAILED")]}),
            (CHAT_ROUTE, 200, {"model": m, "messages": [msg("system", "LR-EXTRACT-1"), msg("user", "LR-EXTRACT-1")]}),
            (CHAT_ROUTE, 200, {"model": m, "messages": [msg("system", "LR-EXTRACT-2"), msg("user", "LR-EXTRACT-2")]}),
            (CHAT_ROUTE, 200, {"model": m, "messages": [msg("system", "LR-FEWSHOT"), msg("user", "LR-FEWSHOT"), msg("user", "LR-FEWSHOT")]}),
            (CHAT_ROUTE, 200, {"model": m, "messages": [msg("system", "LR-GLEAN-1"), msg("user", "LR-GLEAN-1"),
                                                         msg("assistant", "LR-GLEAN-1"), msg("user", "LR-GLEAN-1")]}),
            (CHAT_ROUTE, 200, {"model": m, "messages": [msg("system", "LR-GLEAN-2"), msg("user", "LR-GLEAN-2"),
                                                         msg("assistant", "LR-GLEAN-2"), msg("user", "LR-GLEAN-2")]}),
        ]),
        "fast": write_passa(root / "fast", [
            (CHAT_ROUTE, 200, {"model": m, "response_format": JSON_OBJECT, "messages": [
                msg("system", "FAST-CONT"), msg("user", "FAST-CONT"), msg("assistant", "FAST-CONT"), msg("user", "FAST-CONT")]}),
            (CHAT_ROUTE, 200, {"model": m, "response_format": JSON_OBJECT,
                               "messages": [msg("system", "FAST-EXTRACT-1", extra=" json"), msg("user", "FAST-EXTRACT-1")]}),
            (CHAT_ROUTE, 200, {"model": m, "response_format": JSON_OBJECT,
                               "messages": [msg("system", "FAST-EXTRACT-2"), msg("user", "FAST-EXTRACT-2")]}),
        ]),
        "ms": write_passa(root / "ms", [
            (CHAT_ROUTE, 200, {"model": m, "messages": [{"role": "user", "content": "Hello, can you hear me?"}]}),
            (CHAT_ROUTE, 200, {"model": m, "messages": [msg("user", "MS-SUMMARY")]}),
            (CHAT_ROUTE, 200, {"model": m, "messages": [msg("user", "MS-EXTRACT-1", extra=" <|> ")]}),
            (CHAT_ROUTE, 200, {"model": m, "messages": [msg("user", "MS-EXTRACT-2", extra=" <|> ")]}),
            (CHAT_ROUTE, 200, {"model": m, "response_format": strict_schema(False), "messages": [msg("user", "MS-REPORT-LOOSE")]}),
            (CHAT_ROUTE, 200, {"model": m, "response_format": strict_schema(True), "messages": [msg("user", "MS-REPORT-1", pad=4000)]}),
            (CHAT_ROUTE, 200, {"model": m, "response_format": strict_schema(True), "messages": [msg("user", "MS-REPORT-2")]}),
        ]),
        "nano": write_passa(root / "nano", [
            (CHAT_ROUTE, 200, {"model": m, "messages": [msg("user", "NANO-EXTRACT-1")]}),
            (CHAT_ROUTE, 200, {"model": m, "messages": [msg("user", "NANO-GLEAN"), msg("assistant", "NANO-GLEAN"),
                                                         msg("user", "NANO-GLEAN")]}),
        ]),
    }


def run_main(*argv: object) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = sa.main([str(a) for a in argv])
    return code, out.getvalue(), err.getvalue()


def tree(root: Path) -> list[str]:
    return sorted(str(p.relative_to(root)) for p in root.rglob("*"))


class Base(unittest.TestCase):
    """A temporary tree: a key file, a ledger path, a durable requests file made by `extract`, two fake upstreams."""

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.keydir = self.root / "secret"
        self.keydir.mkdir(mode=0o700)
        self.key_file = self.keydir / "provider.key"
        self.key_file.write_text(CANARY + "\n")
        self.key_file.chmod(0o600)
        self.ledger = self.root / "ledger"
        self.out_dir = self.root / "out"
        self.paid, self.local = FakeProvider(), FakeProvider()
        self.addCleanup(self.paid.close)
        self.addCleanup(self.local.close)
        patcher = mock.patch.object(sa, "RETRY_WAIT_S", 0)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.dirs = passa_dirs(self.root / "passa")
        self.requests_file = self.root / "durable" / "requests.json"
        code, _, err = run_main("extract", "--pass-a-dirs", *[f"{k}={v}" for k, v in self.dirs.items()], "--out", self.requests_file)
        self.assertEqual((code, err), (0, ""))
        self.requests = json.loads(self.requests_file.read_text())

    def profile_dict(self, **over: object) -> dict:
        d = {"base_url": self.paid.base_url, "key_file": str(self.key_file), "ledger_dir": str(self.ledger),
             "allowance_usd": "0.10", "upstream_timeout_s": 60, "input_per_mtok": "0.10", "output_per_mtok": "0.50",
             "cached_input_per_mtok": "0.01", "cache_write_per_mtok": "0.125",
             "source_url": "https://pricing.example.invalid/page", "read_at": "20261102 20:20",
             "output_limit_default": 6144, "request_defaults": {"reasoning_effort": "none"}}
        d.update(over)
        return {k: v for k, v in d.items() if v is not ...}

    def profile(self, **over: object) -> pb.Profile:
        path = self.root / "profile.json"
        path.write_text(json.dumps(self.profile_dict(**over)))
        return pb.load_profile(path)

    def run_args(self, *extra: object, requests: Path | None = None, **over: object) -> list:
        path = self.root / "profile.json"
        path.write_text(json.dumps(self.profile_dict(**over)))
        return ["run", "--profile", path, "--requests", requests or self.requests_file, "--out-dir", self.out_dir,
                "--local-upstream-url", self.local.base_url, *extra]

    def send(self, *extra: object, **over: object) -> tuple[int, str, str]:
        return run_main(*self.run_args("--send", *extra, **over))

    def result(self) -> dict:
        return json.loads((self.out_dir / sa.RESULT_NAME).read_text())

    def by_name(self, result: dict | None = None) -> dict[str, dict]:
        return {c["request"]: c for c in (result or self.result())["calls"]}


class ExtractTests(Base):
    def test_it_picks_the_first_request_of_each_kind_and_writes_a_private_file_of_ten_entries_in_order(self) -> None:
        self.assertEqual([r["name"] for r in self.requests], ORDER)
        self.assertEqual(stat.S_IMODE(os.stat(self.requests_file).st_mode), 0o600)
        for r in self.requests:
            self.assertEqual(set(r), {"name", "route", "body"})
            self.assertEqual((r["route"], r["body"]["model"]), ("/chat/completions", sa.MODEL_PLACEHOLDER))
        picked = {r["name"]: json.dumps(r["body"]) for r in self.requests}
        expected = {"lightrag_extraction": "LR-EXTRACT-1", "lightrag_gleaning": "LR-GLEAN-1", "fast_extraction": "FAST-EXTRACT-1",
                    "ms_extraction": "MS-EXTRACT-1", "ms_community_report": "MS-REPORT-1", "nano_extraction": "NANO-EXTRACT-1"}
        for name, label in expected.items():
            with self.subTest(name):
                self.assertIn(f"{SENT}-{label}", picked[name])
                for other in (l for l in ("LR-FAILED", "LR-FEWSHOT", "LR-EXTRACT-2", "LR-GLEAN-2", "FAST-CONT", "FAST-EXTRACT-2", "MS-SUMMARY",
                                          "MS-EXTRACT-2", "MS-REPORT-LOOSE", "MS-REPORT-2", "NANO-GLEAN") if l != label):
                    self.assertNotIn(f"{SENT}-{other}", picked[name])
        self.assertEqual(sa.load_requests(self.requests_file), self.requests)          # the file `run` reads accepts it

    def test_the_synthesised_requests_carry_no_text_from_the_logs_and_the_json_ones_say_json(self) -> None:
        synth = {r["name"]: r for r in self.requests if r["name"] in SYNTHESISED}
        self.assertEqual(set(synth), SYNTHESISED)
        for r in synth.values():
            self.assertNotIn(SENT, json.dumps(r))
        for name in ("nano_community_report", "fast_summary"):
            text = " ".join(m["content"] for m in synth[name]["body"]["messages"]).lower()
            self.assertEqual(synth[name]["body"]["response_format"], JSON_OBJECT)
            self.assertIn("json", text)
        self.assertEqual(synth["nano_entity_summary"]["body"]["max_tokens"], 500)
        self.assertIn("max_tokens", synth["fast_summary"]["body"])
        self.assertIsNone(synth["fast_summary"]["body"]["max_tokens"])
        self.assertEqual(synth["ping"]["body"]["messages"][0]["content"], "Reply with the single word OK.")
        self.assertEqual([m["role"] for m in synth["nano_entity_summary"]["body"]["messages"]], ["user"])
        self.assertEqual([m["role"] for m in synth["fast_summary"]["body"]["messages"]], ["system", "user"])
        # and the recorded ones DO carry their text, so the check above is not vacuous
        self.assertTrue(all(SENT in json.dumps(r) for r in self.requests if r["name"] not in SYNTHESISED))

    def test_the_table_has_names_and_bytes_and_no_request_text_and_the_file_warning_is_printed(self) -> None:
        requests = self.root / "durable" / "again.json"
        code, out, err = run_main("extract", "--pass-a-dirs", *[f"{k}={v}" for k, v in self.dirs.items()], "--out", requests)
        self.assertEqual((code, err), (0, ""))
        for r in self.requests:
            self.assertRegex(out, rf"{r['name']}\s+{sa.request_bytes(r)}\s")
        self.assertNotIn(SENT, out)
        self.assertNotIn("Reply with the single word", out)
        self.assertIn("article text", out)
        self.assertIn("NOT", out)
        self.assertIn("scratch", out)

    def test_without_a_nano_directory_there_are_nine_requests(self) -> None:
        requests = self.root / "durable" / "no-nano.json"
        dirs = [f"{k}={v}" for k, v in self.dirs.items() if k != "nano"]
        self.assertEqual(run_main("extract", "--pass-a-dirs", *dirs, "--out", requests)[0], 0)
        names = [r["name"] for r in json.loads(requests.read_text())]
        self.assertEqual(names, [n for n in ORDER if n != "nano_extraction"])

    def test_an_out_inside_the_repository_is_refused_and_nothing_is_written(self) -> None:
        target = REPO / "stage-a-test-refused.json"
        self.addCleanup(lambda: target.unlink(missing_ok=True))
        code, out, err = run_main("extract", "--pass-a-dirs", *[f"{k}={v}" for k, v in self.dirs.items()], "--out", target)
        self.assertEqual(code, 2)
        self.assertIn("inside the repository", err)
        self.assertFalse(target.exists())
        self.assertNotIn(SENT, out + err)

    def test_a_worktree_also_refuses_the_primary_checkout_that_holds_it(self) -> None:
        primary, worktree = self.root / "primary", self.root / "primary" / ".claude" / "worktrees" / "wt"
        (primary / ".git" / "worktrees" / "wt").mkdir(parents=True)
        worktree.mkdir(parents=True)
        (worktree / ".git").write_text(f"gitdir: {primary}/.git/worktrees/wt\n")
        roots = sa.repository_roots(worktree)
        self.assertEqual(roots, [worktree, primary])
        self.assertTrue(sa.inside_repository(primary / "notes" / "x.json", roots))
        self.assertTrue(sa.inside_repository(worktree / "x.json", roots))
        self.assertFalse(sa.inside_repository(self.root / "elsewhere" / "x.json", roots))
        self.assertEqual(sa.repository_roots(self.root / "passa"), [self.root / "passa"])      # a plain directory: just itself

    def test_write_private_refuses_an_existing_file_even_when_the_caller_did_not_look_first(self) -> None:
        target = self.root / "durable" / "taken.json"
        target.write_text("keep me")
        with self.assertRaisesRegex(sa.StageAError, "already exists"):
            sa.write_private(target, "replacement")
        self.assertEqual(target.read_text(), "keep me")
        fresh = self.root / "new-dir" / "fresh.json"
        sa.write_private(fresh, "text")
        self.assertEqual((fresh.read_text(), stat.S_IMODE(os.stat(fresh).st_mode)), ("text", 0o600))

    def test_it_never_overwrites_a_file_and_never_touches_the_network(self) -> None:
        before = self.requests_file.read_bytes()
        with mock.patch.object(sa, "_http", side_effect=AssertionError("the network was used")), \
                mock.patch.object(subprocess, "Popen", side_effect=AssertionError("a process was started")):
            code, _, err = run_main("extract", "--pass-a-dirs", *[f"{k}={v}" for k, v in self.dirs.items()], "--out", self.requests_file)
        self.assertEqual(code, 2)
        self.assertIn("already exists", err)
        self.assertEqual(self.requests_file.read_bytes(), before)

    def test_a_missing_kind_or_directory_or_a_bad_argument_is_refused_without_writing(self) -> None:
        out = self.root / "durable" / "bad.json"
        no_report = write_passa(self.root / "ms-no-report", [(CHAT_ROUTE, 200, {"model": "m", "messages": [msg("user", "X", extra=" <|> ")]})])
        dirs = {**{k: str(v) for k, v in self.dirs.items()}, "ms": str(no_report)}
        code, _, err = run_main("extract", "--pass-a-dirs", *[f"{k}={v}" for k, v in dirs.items()], "--out", out)
        self.assertEqual(code, 2)
        self.assertIn("ms_community_report", err)
        for argv, needle in (([f"lightrag={self.dirs['lightrag']}"], "missing"),
                             ([f"{k}={v}" for k, v in self.dirs.items()] + ["other=/x"], "unknown"),
                             (["lightrag"], "NAME=DIR"),
                             ([f"{k}={v}" for k, v in self.dirs.items()] + [f"fast={self.dirs['fast']}"], "NAME=DIR"),
                             ([f"lightrag={self.root / 'nowhere'}", f"fast={self.dirs['fast']}", f"ms={self.dirs['ms']}"], "does not exist")):
            code, _, err = run_main("extract", "--pass-a-dirs", *argv, "--out", out)
            self.assertEqual(code, 2, argv)
            self.assertIn(needle, err)
        self.assertFalse(out.exists())

    def test_a_scratch_path_is_recognised(self) -> None:
        self.assertTrue(sa.looks_like_scratch(Path(tempfile.gettempdir()) / "x.json"))
        self.assertTrue(sa.looks_like_scratch(Path("/tmp/anything.json")))
        self.assertTrue(sa.looks_like_scratch(Path("/somewhere/scratchpad/x.json")))
        self.assertFalse(sa.looks_like_scratch(Path("/somewhere/durable/x.json")))


class RequestsFileTests(Base):
    def write(self, data: object, mode: int = 0o600, name: str = "x.json") -> Path:
        path = self.root / "durable" / name
        path.write_text(data if isinstance(data, str) else json.dumps(data))
        path.chmod(mode)
        return path

    def refused(self, path: Path, needle: str) -> None:
        with self.assertRaises(sa.StageAError) as ctx:
            sa.load_requests(path)
        self.assertIn(needle, str(ctx.exception))
        self.assertNotIn(SENT, str(ctx.exception))

    def test_a_file_others_can_read_is_refused(self) -> None:
        for mode in (0o644, 0o640, 0o604):
            self.refused(self.write(self.requests, mode), "read by others")

    def test_a_file_inside_the_repository_is_refused(self) -> None:
        with mock.patch.object(sa, "repository_roots", return_value=[self.root / "durable"]):
            self.refused(self.write(self.requests), "inside the repository")

    def test_a_file_that_is_missing_not_json_or_not_a_list_is_refused(self) -> None:
        self.refused(self.root / "nope.json", "cannot read")
        self.refused(self.write("{not json"), "not valid JSON")
        self.refused(self.write({"a": 1}), "JSON list")
        self.refused(self.write([]), "JSON list")
        self.refused(self.write(self.requests + self.requests[:1]), "JSON list")             # eleven entries

    def test_a_malformed_entry_is_refused_and_named_by_number(self) -> None:
        good = self.requests[0]
        for entry, needle in (({**good, "extra": 1}, "exactly name"), ({"name": "x"}, "exactly name"), ("text", "exactly name"),
                              ({**good, "name": "Bad Name"}, "unique, lower case"), ({**good, "name": 5}, "unique, lower case"),
                              ({**good, "route": "/embeddings"}, "route must be"),
                              ({**good, "body": {"model": "m"}}, "model and messages"),
                              ({**good, "body": {"messages": good["body"]["messages"]}}, "model and messages"),
                              ({**good, "body": {**good["body"], "stream": True}}, "streamed")):
            with self.subTest(entry=str(entry)[:40]):
                self.refused(self.write([entry]), "entry 1")
                self.refused(self.write([entry]), needle)
        self.refused(self.write([good, good]), "unique")


class DryRunTests(Base):
    def test_the_dry_run_starts_nothing_and_writes_nothing(self) -> None:
        args = self.run_args()                                                 # writes the profile, which is the owner's input
        before = tree(self.root)
        with mock.patch.object(subprocess, "Popen", side_effect=AssertionError("a process was started")), \
                mock.patch.object(sa, "_http", side_effect=AssertionError("the network was used")):
            code, out, err = run_main(*args)
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(tree(self.root), before)                            # no out-dir, no ledger, no gateway directory
        self.assertFalse(self.out_dir.exists())
        self.assertFalse(self.ledger.exists())
        self.assertEqual((self.paid.requests, self.local.requests), ([], []))
        self.assertIn("DRY RUN", out)
        for name in ORDER:
            self.assertRegex(out, rf"\n{name}\s+\d+\s")
        for needle in ("worst case", "0.1", "0.0001", "gpt-6-luna", "11 of at most 12"):
            self.assertIn(needle, out)
        self.assertRegex(out, r"the largest request \(ms_community_report\) against an allowance of USD 0\.0001")
        for secret in (CANARY, SENT, RESPONSE_SENT, str(self.root), self.key_file.name):
            self.assertNotIn(secret, out)

    def test_the_worst_case_follows_the_gateways_reservation_formula(self) -> None:
        profile = self.profile()
        by_name = {r["name"]: r for r in self.requests}
        ping = by_name["ping"]["body"]
        forward = {**ping, "model": CHAT, "max_completion_tokens": 6144, "reasoning_effort": "none"}
        tokens = -(-len(json.dumps(forward).encode()) // 2)
        expected = (Decimal(tokens) * Decimal("0.125") + Decimal(6144) * Decimal("0.5")) / 1_000_000    # dearer of input and cache write
        self.assertEqual(sa.worst_case_usd(profile, ping, CHAT), expected)
        nano = by_name["nano_entity_summary"]["body"]                          # a client limit wins: 500, not 6144
        self.assertEqual(sa.forwarded_body(profile, nano, CHAT).get("max_completion_tokens"), None)
        self.assertLess(sa.worst_case_usd(profile, nano, CHAT), sa.worst_case_usd(profile, ping, CHAT))
        null = by_name["fast_summary"]["body"]                                  # a null counts as no limit
        self.assertEqual(sa.forwarded_body(profile, null, CHAT)["max_completion_tokens"], 6144)

    def test_a_profile_that_would_load_more_than_the_stage_cap_is_refused_in_the_dry_run_and_with_send(self) -> None:
        for args in (self.run_args(allowance_usd="0.50"), self.run_args("--send", allowance_usd="0.1000001")):
            code, out, err = run_main(*args)
            self.assertEqual(code, 2)
            self.assertIn("REFUSED", err)
            self.assertIn("stage cap", err)
            self.assertFalse(self.out_dir.exists())
            self.assertFalse(self.ledger.exists())
            self.assertEqual(self.paid.requests, [])

    def test_the_pilot_cap_less_what_the_ledger_holds_limits_the_allowance(self) -> None:
        self.ledger.mkdir()
        (self.ledger / "meter.jsonl").write_text("".join(json.dumps({"cost": "0.99"}) + "\n" for _ in range(3)))     # 2.97 spent: 0.03 left
        code, _, err = run_main(*self.run_args("--send"))
        self.assertEqual(code, 2)
        self.assertIn("pilot cap", err)
        self.assertEqual(self.paid.requests, [])
        self.assertFalse(self.out_dir.exists())
        (self.ledger / "meter.jsonl").write_text(json.dumps({"cost": "0.95"}) + "\n")                              # 0.95: room for 0.10
        code, out, _ = run_main(*self.run_args())
        self.assertEqual(code, 0)
        self.assertIn("ledger holds 1 record(s), USD 0.95", out)
        self.assertIn("cap of USD 1.05", out)

    def test_a_worst_case_above_the_allowance_and_a_refusal_test_that_could_prove_nothing_are_refused(self) -> None:
        code, _, err = run_main(*self.run_args(allowance_usd="0.02"))
        self.assertEqual(code, 2)
        self.assertIn("worst-case", err)
        code, _, err = run_main(*self.run_args(output_per_mtok="0.00001", input_per_mtok="0.00001", cache_write_per_mtok=...))
        self.assertEqual(code, 2)
        self.assertIn("prove nothing", err)

    def test_it_is_refused_when_the_out_dir_is_inside_the_repository_or_not_empty_or_the_model_is_odd(self) -> None:
        inside = REPO / "stage-a-out-test"
        self.addCleanup(lambda: inside.exists() and inside.rmdir())
        args = self.run_args("--send")
        args[args.index("--out-dir") + 1] = inside
        code, _, err = run_main(*args)
        self.assertEqual((code, "inside the repository" in err), (2, True))
        self.assertFalse(inside.exists())
        self.out_dir.mkdir()
        (self.out_dir / "old").write_text("x")
        for args in (self.run_args("--send"), self.run_args()):                  # the dry run finds it too
            code, _, err = run_main(*args)
            self.assertEqual((code, "new or empty" in err), (2, True))
        self.assertEqual(self.paid.requests, [])
        code, _, err = run_main(*self.run_args("--model", "bad model!"))
        self.assertEqual((code, "--model" in err), (2, True))

    def test_the_entry_point_works_as_a_script_and_a_dry_run_there_starts_nothing(self) -> None:
        env = {"PATH": "/usr/bin:/bin"}
        done = subprocess.run([sys.executable, "-B", str(HERE / "passb_stage_a.py"), *map(str, self.run_args())],
                              capture_output=True, text=True, env=env, timeout=60)
        self.assertEqual((done.returncode, done.stderr), (0, ""))
        self.assertIn("DRY RUN", done.stdout)
        self.assertEqual(self.paid.requests, [])
        self.assertFalse(self.out_dir.exists())


class SendTests(Base):
    def test_the_whole_sequence_runs_against_the_fake_and_the_result_holds_the_gates(self) -> None:
        code, out, err = self.send()
        self.assertEqual((code, err), (0, ""))
        # what reached the provider: ten calls, each with the key the gateway added and the fields it injected
        sent = self.paid.chat_requests()
        self.assertEqual(len(sent), 10)
        self.assertEqual({r["authorization"] for r in sent}, {"Bearer " + CANARY})
        for request in sent:
            self.assertEqual(request["body"]["model"], CHAT)
            self.assertEqual(request["body"]["reasoning_effort"], "none")
        bodies = {r["name"]: b["body"] for r, b in zip(self.requests, sent)}
        self.assertEqual(bodies["nano_entity_summary"]["max_tokens"], 500)
        self.assertNotIn("max_completion_tokens", bodies["nano_entity_summary"])
        self.assertIsNone(bodies["fast_summary"]["max_tokens"])
        self.assertEqual(bodies["fast_summary"]["max_completion_tokens"], 6144)
        self.assertEqual(bodies["ping"]["max_completion_tokens"], 6144)
        self.assertEqual(self.local.requests, [])                                       # the embedding upstream is never called
        # the result
        self.assertEqual(stat.S_IMODE(os.stat(self.out_dir / sa.RESULT_NAME).st_mode), 0o600)
        r = self.result()
        self.assertEqual([c["request"] for c in r["calls"]], ORDER)
        self.assertEqual((r["stopped"], r["not_sent"]), (None, []))
        self.assertEqual(r["models_reported"], ["gpt-6-luna-test-1"])
        g = r["gates"]
        for gate in ("every_call_200_or_recorded_incompatible", "no_request_left_unsent", "reasoning_effort_accepted",
                     "reasoning_tokens_reported_on_every_answer", "reasoning_tokens_zero_on_every_answer", "reasoning_off_ok",
                     "output_limit_injected_wherever_the_client_set_none", "usage_present_on_every_answer",
                     "refusal_test_passed", "total_cost_within_stage_cap"):
            self.assertIs(g[gate], True, gate)
        self.assertIs(g["usage_has_a_cache_write_field"], False)
        self.assertEqual(g["null_max_tokens_with_injected_limit"], {"calls": 1, "all_accepted": True, "all_carried_the_injected_field": True})
        self.assertEqual(g["shapes"]["json_object"], {"accepted": ["fast_extraction", "fast_summary", "nano_community_report"], "rejected": []})
        self.assertEqual(g["shapes"]["json_schema"], {"accepted": ["ms_community_report"], "rejected": []})
        self.assertEqual(g["shapes"]["max_tokens"], {"accepted": ["nano_entity_summary"], "rejected": []})
        self.assertEqual(g["shapes"]["max_tokens_null"], {"accepted": ["fast_summary"], "rejected": []})
        self.assertEqual(g["usage_field_names"], ["completion_tokens", "completion_tokens_details", "completion_tokens_details.reasoning_tokens",
                                                  "prompt_tokens", "prompt_tokens_details", "prompt_tokens_details.cached_tokens", "total_tokens"])
        self.assertEqual(g["rejected_requests"], [])
        calls = self.by_name(r)
        self.assertEqual(calls["ping"]["request_defaults_applied"], ["reasoning_effort", "max_completion_tokens"])
        self.assertEqual(calls["nano_entity_summary"]["request_defaults_applied"], ["reasoning_effort"])
        self.assertIs(calls["fast_summary"]["null_max_tokens_with_injected_limit"], True)
        self.assertEqual((calls["ping"]["http_status"], calls["ping"]["finish_reason"], calls["ping"]["model_reported"],
                          calls["ping"]["prompt_tokens"], calls["ping"]["completion_tokens"], calls["ping"]["reasoning_tokens"]),
                         (200, "stop", "gpt-6-luna-test-1", 1200, 300, 0))
        self.assertEqual(Decimal(calls["ping"]["cost_usd"]), UNIT_COST)
        self.assertEqual(r["totals"], {"forwarded_attempts": 10, "gateway_cost_usd": "0.0027", "gateway_records": 10})
        self.assertIn("10 requests", r["console_check"])
        self.assertIn("0.0027", r["console_check"])
        self.assertEqual(r["caps_usd"], {"stage_cap": "0.1", "allowance": "0.1", "gateway_cap": "0.1", "ledger_spent_before": "0"})
        self.assertEqual(r["hosted"]["calls_in_this_run"], 10)
        # the shared ledger holds the ten calls; the throwaway one holds the refusal and no body log
        self.assertEqual(len((self.ledger / "meter.jsonl").read_text().splitlines()), 10)
        refusal_ledger = self.out_dir / "refusal-ledger"
        self.assertEqual(len((refusal_ledger / "meter.jsonl").read_text().splitlines()), 1)
        self.assertFalse((refusal_ledger / "meter.jsonl.bodies.jsonl").exists())
        self.assertIn("PASSED", out)

    def test_the_refusal_test_sends_the_largest_request_and_the_provider_is_not_called(self) -> None:
        code, _, _ = self.send()
        self.assertEqual(code, 0)
        r = self.result()
        largest = max(self.requests, key=sa.request_bytes)
        self.assertEqual(largest["name"], "ms_community_report")
        t = r["refusal_test"]
        self.assertEqual((t["request"], t["request_bytes"]), (largest["name"], sa.request_bytes(largest)))
        self.assertEqual((t["client_http_status"], t["client_error_code"], t["ledger_records"]), (429, "gateway_budget_exceeded", 1))
        self.assertEqual((t["nothing_forwarded"], t["passed"], t["throwaway_body_log_removed"]), (True, True, True))
        self.assertEqual(t["allowance_usd"], "0.0001")
        self.assertEqual(len(self.paid.chat_requests()), 10)                            # the refused call reached no provider
        record = json.loads((self.out_dir / "refusal-ledger" / "meter.jsonl").read_text())
        self.assertEqual((record["refusal"], record["http_status"], record["cost"], record["voided"]), ("gateway_budget_exceeded", 429, "0", False))
        self.assertEqual(record["model_requested"], CHAT)

    def test_even_when_aimed_at_the_provider_the_refusal_forwards_nothing_and_a_cap_that_lets_it_through_is_caught(self) -> None:
        profile = self.profile()
        entries = sa.load_requests(self.requests_file)
        result, code = sa.run_stage(profile, entries, self.out_dir, model=CHAT, embed_model="stage-a-unused-embedding",
                                    local_url=self.local.base_url, out=io.StringIO(), refusal_upstream_url=self.paid.base_url)
        self.assertEqual(code, 0)
        self.assertEqual(len(self.paid.chat_requests()), 10)                            # the fake upstream's count: unchanged
        self.assertEqual(result["refusal_test"]["upstream"], "a URL given by the caller")
        self.assertTrue(result["refusal_test"]["passed"])
        # a refusal test whose allowance is big enough lets the call through: the program must say so, and the fake sees it
        out2 = self.root / "out2"
        ledger2 = self.root / "ledger2"
        profile2 = self.profile(ledger_dir=str(ledger2))
        result2, code2 = sa.run_stage(profile2, entries, out2, model=CHAT, embed_model="stage-a-unused-embedding", local_url=self.local.base_url,
                                      out=io.StringIO(), refusal_upstream_url=self.paid.base_url, refusal_allowance=Decimal("0.5"))
        self.assertEqual(code2, 3)
        self.assertEqual(len(self.paid.chat_requests()), 21)                            # 10 + 10 + the one that got through
        t = result2["refusal_test"]
        self.assertEqual((t["client_http_status"], t["nothing_forwarded"], t["passed"]), (200, False, False))
        self.assertFalse(result2["gates"]["refusal_test_passed"])

    def test_a_refusal_that_is_forwarded_to_the_dead_port_shows_as_a_failure_not_a_pass(self) -> None:
        profile = self.profile()
        entries = sa.load_requests(self.requests_file)
        result, code = sa.run_stage(profile, entries, self.out_dir, model=CHAT, embed_model="stage-a-unused-embedding",
                                    local_url=self.local.base_url, out=io.StringIO(), refusal_allowance=Decimal("0.5"))
        self.assertEqual(code, 3)
        t = result["refusal_test"]
        self.assertEqual((t["client_http_status"], t["nothing_forwarded"], t["passed"]), (502, False, False))
        self.assertEqual(len(self.paid.chat_requests()), 10)                            # the dead port took it: the provider saw nothing

    def test_a_400_on_a_shape_is_recorded_as_incompatibility_and_the_run_continues(self) -> None:
        error = {"message": f"{RESPONSE_SENT} unsupported", "type": "invalid_request_error", "param": "response_format",
                 "code": "invalid_value"}
        self.paid.reject = lambda body: error if (body.get("response_format") or {}).get("type") == "json_object" else None
        code, out, _ = self.send()
        self.assertEqual(code, 0)
        self.assertEqual(len(self.paid.chat_requests()), 10)                            # each request once: nothing retried
        r = self.result()
        calls = self.by_name(r)
        rejected = ["fast_extraction", "fast_summary", "nano_community_report"]
        for name in rejected:
            self.assertEqual((calls[name]["http_status"], calls[name]["outcome"]), (400, "rejected_incompatible"))
            self.assertEqual(calls[name]["error"], {"type": "invalid_request_error", "code": "invalid_value",
                                                    "param": "response_format", "message_length": len(error["message"])})
            self.assertEqual(calls[name]["attempt"], 1)
        self.assertEqual(r["gates"]["rejected_requests"], rejected)
        self.assertEqual(r["gates"]["shapes"]["json_object"], {"accepted": [], "rejected": rejected})
        self.assertEqual(r["gates"]["shapes"]["json_schema"]["accepted"], ["ms_community_report"])
        self.assertIs(r["gates"]["every_call_200_or_recorded_incompatible"], True)
        self.assertIs(r["gates"]["reasoning_off_ok"], True)
        self.assertEqual(r["gates"]["null_max_tokens_with_injected_limit"]["all_accepted"], False)
        self.assertEqual(r["stopped"], None)
        self.assertTrue(r["refusal_test"]["passed"])
        self.assertIn("rejected_incompatible", out)
        self.assertNotIn(RESPONSE_SENT, json.dumps(r) + out)                            # the message was measured, never kept

    def test_a_rejected_max_tokens_names_the_parameter_and_a_rejected_reasoning_effort_fails_that_gate(self) -> None:
        self.paid.reject = lambda b: ({"message": "no", "type": "invalid_request_error", "param": "max_tokens", "code": "unsupported_parameter"}
                                      if isinstance(b.get("max_tokens"), int) else None)
        self.assertEqual(self.send()[0], 0)
        r = self.result()
        self.assertEqual(r["gates"]["shapes"]["max_tokens"], {"accepted": [], "rejected": ["nano_entity_summary"]})
        self.assertEqual(self.by_name(r)["nano_entity_summary"]["error"]["param"], "max_tokens")
        self.assertIs(r["gates"]["reasoning_effort_accepted"], True)
        self.paid.reject = lambda b: ({"message": "no", "type": "invalid_request_error", "param": "reasoning_effort", "code": "unsupported_value"}
                                      if "response_format" in b and b["response_format"].get("type") == "json_schema" else None)
        self.paid.requests.clear()
        self.out_dir = self.root / "out-b"
        self.ledger = self.root / "ledger-b"
        self.assertEqual(self.send()[0], 0)
        r = self.result()
        self.assertIs(r["gates"]["reasoning_effort_accepted"], False)
        self.assertIs(r["gates"]["reasoning_off_ok"], False)

    def test_reasoning_tokens_above_zero_fail_the_reasoning_gates(self) -> None:
        self.paid.reasoning_tokens = 12
        self.assertEqual(self.send()[0], 0)
        g = self.result()["gates"]
        self.assertIs(g["reasoning_effort_accepted"], True)
        self.assertIs(g["reasoning_tokens_zero_on_every_answer"], False)
        self.assertIs(g["reasoning_off_ok"], False)
        self.assertEqual(self.by_name()["ping"]["reasoning_tokens"], 12)

    def test_a_cache_write_field_in_the_usage_is_seen_by_name(self) -> None:
        self.paid.extra_prompt_details = {"cache_write_tokens": 0}
        self.assertEqual(self.send()[0], 0)
        g = self.result()["gates"]
        self.assertIs(g["usage_has_a_cache_write_field"], True)
        self.assertIn("prompt_tokens_details.cache_write_tokens", g["usage_field_names"])

    def test_a_401_stops_at_once_and_nothing_else_is_sent_and_no_refusal_test_runs(self) -> None:
        self.paid.always = 401
        code, out, _ = self.send()
        self.assertEqual(code, 3)
        self.assertEqual(len(self.paid.chat_requests()), 1)                             # the ping, once: not retried, nothing after it
        r = self.result()
        self.assertEqual(r["stopped"], {"reason": "auth", "at_request": "ping", "http_status": 401})
        self.assertEqual(r["not_sent"], ORDER[1:])
        self.assertEqual(r["refusal_test"], {"skipped": "stopped earlier (auth)", "passed": False})
        self.assertFalse((self.out_dir / "refusal-ledger").exists())
        self.assertIs(r["gates"]["no_request_left_unsent"], False)
        self.assertIs(r["gates"]["refusal_test_passed"], False)
        self.assertIs(r["gates"]["reasoning_off_ok"], False)
        self.assertEqual(r["totals"]["gateway_cost_usd"], "0")
        self.assertIn("STOPPED: auth", out)
        for status in (403,):
            self.paid.requests.clear()
            self.paid.always = status
            self.out_dir, self.ledger = self.root / "out403", self.root / "ledger403"
            self.assertEqual(self.send()[0], 3)
            self.assertEqual(len(self.paid.chat_requests()), 1)
            self.assertEqual(self.result()["stopped"]["reason"], "auth")

    def test_a_401_after_the_ping_also_stops_the_run_there(self) -> None:
        self.paid.statuses = [200, 200, 401]
        self.assertEqual(self.send()[0], 3)
        r = self.result()
        self.assertEqual(len(self.paid.chat_requests()), 3)
        self.assertEqual(r["stopped"]["at_request"], "lightrag_gleaning")
        self.assertEqual(r["not_sent"], ORDER[3:])

    def test_a_429_or_5xx_is_retried_once_and_a_second_failure_stops(self) -> None:
        self.paid.statuses = [429]
        self.assertEqual(self.send()[0], 0)
        self.assertEqual(len(self.paid.chat_requests()), 11)
        r = self.result()
        self.assertEqual([(c["request"], c["attempt"], c["outcome"]) for c in r["calls"][:2]],
                         [("ping", 1, "retryable_error"), ("ping", 2, "ok")])
        self.assertEqual(r["totals"]["forwarded_attempts"], 11)
        self.assertEqual(r["totals"]["gateway_cost_usd"], "0.0027")                      # the 429 was free
        self.assertIs(r["gates"]["every_call_200_or_recorded_incompatible"], True)
        for statuses in ([500, 500], [429, 503]):
            with self.subTest(statuses):
                self.paid.requests.clear()
                self.paid.statuses = list(statuses)
                self.out_dir, self.ledger = self.root / f"out{statuses[1]}", self.root / f"ledger{statuses[1]}"
                self.assertEqual(self.send()[0], 3)
                self.assertEqual(len(self.paid.chat_requests()), 2)
                r = self.result()
                self.assertEqual(r["stopped"]["reason"], "provider_unavailable_after_retry")
                self.assertEqual(r["calls"][1]["outcome"], "provider_unavailable_after_retry")
                self.assertEqual(r["not_sent"], ORDER[1:])

    def test_a_rejected_ping_stops_the_run_and_an_unexpected_status_stops_it_too(self) -> None:
        self.paid.reject = lambda b: {"message": "no", "type": "invalid_request_error", "param": "reasoning_effort", "code": "unsupported_value"}
        self.assertEqual(self.send()[0], 3)
        self.assertEqual(len(self.paid.chat_requests()), 1)
        self.assertEqual(self.result()["stopped"]["reason"], "ping_rejected")
        self.paid.reject = None
        self.paid.requests.clear()
        self.paid.always = 404
        self.out_dir, self.ledger = self.root / "out404", self.root / "ledger404"
        self.assertEqual(self.send()[0], 3)
        self.assertEqual(self.result()["stopped"]["reason"], "unexpected_status")
        self.assertEqual(len(self.paid.chat_requests()), 1)

    def test_the_attempt_limit_keeps_the_stage_within_twelve_calls(self) -> None:
        self.assertEqual((sa.MAX_CALLS, sa.MAX_ATTEMPTS, sa.MAX_REQUESTS), (12, 11, 10))
        with mock.patch.object(sa, "MAX_ATTEMPTS", 3):
            self.assertEqual(self.send()[0], 3)
        r = self.result()
        self.assertEqual(len(self.paid.chat_requests()), 3)
        self.assertEqual(r["stopped"]["reason"], "attempt_limit")
        self.assertEqual(r["not_sent"], ORDER[3:])

    def test_a_spend_above_the_stage_cap_stops_the_run(self) -> None:
        self.paid.prompt_tokens, self.paid.completion_tokens = 600_000, 100_000          # 0.06 + 0.05 = 0.11 per call
        with mock.patch.object(sa, "STAGE_CAP", Decimal("0.10")):
            code, _, _ = self.send(allowance_usd="0.10")
        self.assertEqual(code, 3)
        r = self.result()
        self.assertEqual(r["stopped"]["reason"], "spend_above_stage_cap")
        self.assertEqual(r["stopped"]["at_request"], "ping")
        self.assertEqual(len(self.paid.chat_requests()), 1)
        self.assertIs(r["gates"]["total_cost_within_stage_cap"], False)

    def test_a_call_that_does_not_add_exactly_one_record_stops_the_run(self) -> None:
        real = pb.HostedGateway.run_records
        reads = []

        def stale(gw):
            reads.append(1)
            records = real(gw)
            return records[:-1] if len(reads) == 2 else records           # the read right after the first send misses its record

        with mock.patch.object(pb.HostedGateway, "run_records", stale):
            code, _, _ = self.send()
        self.assertEqual(code, 3)
        r = self.result()
        self.assertEqual(r["stopped"], {"reason": "ledger_mismatch", "at_request": "ping", "http_status": 200})
        self.assertEqual(r["not_sent"], ORDER[1:])
        self.assertEqual(len(self.paid.chat_requests()), 1)

    def test_an_interrupt_is_recorded_and_the_rest_is_listed_as_not_sent(self) -> None:
        real = sa._send_with_retry
        seen = []

        def interrupt(gw, entry, *args):
            seen.append(entry["name"])
            if len(seen) == 3:
                raise KeyboardInterrupt
            return real(gw, entry, *args)

        with mock.patch.object(sa, "_send_with_retry", interrupt):
            code, _, _ = self.send()
        self.assertEqual(code, 3)
        r = self.result()
        self.assertEqual(r["stopped"], {"reason": "interrupted", "at_request": "lightrag_gleaning", "http_status": None})
        self.assertEqual(r["not_sent"], ORDER[2:])
        self.assertEqual(len(self.paid.chat_requests()), 2)

    def test_a_defect_in_the_harness_is_recorded_by_its_class_name_and_the_run_still_writes_its_result(self) -> None:
        real = sa._send_with_retry
        seen = []

        def broken(gw, entry, *args):
            seen.append(entry["name"])
            if len(seen) == 2:
                raise RuntimeError(f"{SENT} a message that must not be kept")
            return real(gw, entry, *args)

        with mock.patch.object(sa, "_send_with_retry", broken):
            code, out, err = self.send()
        self.assertEqual(code, 3)
        r = self.result()
        self.assertEqual(r["stopped"], {"reason": "harness_error_RuntimeError", "at_request": "lightrag_extraction", "http_status": None})
        self.assertEqual(r["not_sent"], ORDER[1:])
        self.assertEqual(r["refusal_test"]["skipped"], "stopped earlier (harness_error_RuntimeError)")
        self.assertNotIn(SENT, json.dumps(r) + out + err)

    def test_a_refusal_test_that_cannot_run_is_a_failed_test_not_a_lost_result(self) -> None:
        with mock.patch.object(sa, "run_refusal_test", side_effect=pc.PassAError("the gateway did not start")):
            code, out, _ = self.send()
        self.assertEqual(code, 3)
        r = self.result()
        self.assertEqual(r["refusal_test"], {"skipped": "failed to run (PassAError)", "passed": False})
        self.assertIs(r["gates"]["refusal_test_passed"], False)
        self.assertEqual(len(r["calls"]), 10)

    def test_the_second_run_on_the_same_ledger_continues_it_and_the_cap_is_spent_plus_allowance(self) -> None:
        self.assertEqual(self.send()[0], 0)
        self.out_dir = self.root / "out-second"
        self.assertEqual(self.send(allowance_usd="0.05")[0], 0)
        r = self.result()
        self.assertEqual((r["caps_usd"]["gateway_cap"], r["caps_usd"]["ledger_spent_before"]), ("0.0527", "0.0027"))
        self.assertEqual(r["hosted"]["resumed_an_existing_ledger"], True)
        self.assertEqual(r["totals"]["gateway_cost_usd"], "0.0027")
        self.assertEqual(len((self.ledger / "meter.jsonl").read_text().splitlines()), 20)

    def test_a_cap_the_gateway_did_not_load_stops_everything_before_a_call(self) -> None:
        class Stub:
            port, cap = 1, Decimal("0.10")
        for reply, ok in (((200, b'{"cap": "0.1"}'), True), ((200, b'{"cap": "0.5"}'), False), ((200, b'{"cap": null}'), False),
                          ((200, b"not json"), False), ((500, b'{"cap": "0.1"}'), False), ((None, b""), False)):
            with self.subTest(reply), mock.patch.object(sa, "_http", return_value=reply):
                if ok:
                    sa.verify_cap_loaded(Stub())
                else:
                    with self.assertRaisesRegex(sa.StageAError, "did not report the cap"):
                        sa.verify_cap_loaded(Stub())
        with mock.patch.object(sa, "verify_cap_loaded", side_effect=sa.StageAError("the gateway did not report the cap")):
            code, _, err = self.send()
        self.assertEqual((code, self.paid.requests), (2, []))
        self.assertIn("did not report the cap", err)
        self.assertFalse((self.out_dir / sa.RESULT_NAME).exists())


class LeakTests(Base):
    def test_the_result_and_the_output_hold_neither_the_key_nor_any_request_text_nor_a_path(self) -> None:
        self.paid.echo_authorization = True            # worst case: the provider puts the key it received into its answer
        code, out, err = self.send()
        self.assertEqual(code, 0)
        self.assertEqual({r["authorization"] for r in self.paid.chat_requests()}, {"Bearer " + CANARY})   # not vacuous
        result_text = (self.out_dir / sa.RESULT_NAME).read_text()
        self.assertGreater(len(result_text), 2000)
        for label, text in (("result", result_text), ("stdout", out), ("stderr", err)):
            for secret in (CANARY, CANARY[:10], SENT, RESPONSE_SENT, "Reply with the single word", "Alpha Widget", str(self.root),
                           str(self.key_file), self.key_file.name, str(self.ledger)):
                self.assertNotIn(secret, text, f"{label} holds {secret!r}")
        # nothing under the out-dir holds the key or any request text (the throwaway body log was deleted)
        files = [p for p in self.out_dir.rglob("*") if p.is_file()]
        self.assertTrue({"gateway.toml", "meter.jsonl", sa.RESULT_NAME} <= {p.name for p in files})
        for path in files:
            data = path.read_bytes()
            self.assertNotIn(CANARY.encode(), data, path.name)
            self.assertNotIn(SENT.encode(), data, path.name)

    def test_a_failed_run_leaks_nothing_either(self) -> None:
        self.paid.always = 401
        code, out, err = self.send()
        self.assertEqual(code, 3)
        text = (self.out_dir / sa.RESULT_NAME).read_text() + out + err
        for secret in (CANARY, SENT, RESPONSE_SENT, str(self.root), str(self.key_file)):
            self.assertNotIn(secret, text)

    def test_the_program_never_opens_the_key_file(self) -> None:
        opened: list[str] = []
        real_open, real_io_open, real_os_open = builtins.open, io.open, os.open

        def note(target: object) -> None:
            try:
                opened.append(os.fspath(target))
            except TypeError:
                pass

        def spy(real):
            def inner(file, *a, **k):
                note(file)
                return real(file, *a, **k)
            return inner

        with mock.patch.object(builtins, "open", spy(real_open)), mock.patch.object(io, "open", spy(real_io_open)), \
                mock.patch.object(os, "open", spy(real_os_open)):
            self.assertEqual(self.send()[0], 0)
            run_main(*self.run_args())
        self.assertTrue(any(p.endswith(sa.RESULT_NAME) for p in opened))               # the spy sees what this process opens
        self.assertNotIn(str(self.key_file), opened)
        self.assertFalse([p for p in opened if p.endswith("provider.key")])

    def test_the_gateway_gets_the_key_through_its_file_only_and_the_program_sends_a_dummy_authorization(self) -> None:
        sent = []
        real = sa._http

        def spy(url, payload, timeout):
            sent.append((url, payload is not None))
            return real(url, payload, timeout)

        with mock.patch.object(sa, "_http", spy):
            self.assertEqual(self.send()[0], 0)
        self.assertEqual(sa.DUMMY_AUTHORIZATION, "Bearer dummy-not-a-key")
        self.assertNotIn(CANARY, sa.DUMMY_AUTHORIZATION)
        self.assertTrue(all(url.startswith("http://127.0.0.1:") for url, _ in sent))      # only loopback, only the gateways


class ProxyTests(Base):
    def test_a_system_proxy_never_sees_the_loopback_traffic(self) -> None:
        code = ("import sys; sys.path.insert(0, sys.argv[1]); import passb_stage_a as sa; "
                "print(sa._http(sys.argv[2] + '/chat/completions', {'model': 'm', 'messages': [{'role': 'user', 'content': 'q'}]}, 20)[0])")
        env = {"PATH": "/usr/bin:/bin", "http_proxy": "http://127.0.0.1:9", "HTTP_PROXY": "http://127.0.0.1:9"}
        done = subprocess.run([sys.executable, "-I", "-B", "-c", code, str(HERE), self.paid.base_url], capture_output=True,
                              text=True, env=env, timeout=60)
        self.assertEqual((done.stdout.strip(), done.stderr), ("200", ""))
        self.assertEqual(len(self.paid.chat_requests()), 1)
        # the same call through an opener that honours the environment would have gone to the proxy
        through = subprocess.run([sys.executable, "-I", "-B", "-c",
                                  "import urllib.request as u; print(u.build_opener().handlers and "
                                  "[h.proxies for h in u.build_opener().handlers if isinstance(h, u.ProxyHandler)])"],
                                 capture_output=True, text=True, env=env, timeout=60)
        self.assertIn("127.0.0.1:9", through.stdout)                                  # not vacuous: the environment is honoured by default


class PureTests(unittest.TestCase):
    """The decisions, without a gateway: what a status means, what a refusal proves, what the gates say."""

    def call(self, name: str = "x", status: int | None = 200, **over: object) -> dict:
        record = {"cost": "0.0001", "request_defaults_applied": ["reasoning_effort", "max_completion_tokens"], "refusal": None,
                  "voided": False, "usage_missing": False}
        record.update(over.pop("record", {}))
        raw = over.pop("raw", None)
        if raw is None:
            raw = json.dumps({"model": "m-1", "choices": [{"finish_reason": "stop"}],
                              "usage": {"prompt_tokens": 10, "completion_tokens": 5, "completion_tokens_details": {"reasoning_tokens": 0}}}).encode()
        entry = over.pop("entry", {"name": name, "body": {"model": "m", "messages": [{"role": "user", "content": "q"}]}})
        call = sa.describe_call(entry, 1, status, raw, record)
        call["outcome"] = over.pop("outcome", "ok" if status == 200 else "rejected_incompatible")
        call.update(over)
        return call

    def test_judge_maps_each_status_to_one_action(self) -> None:
        table = [(200, {}, False, "ok"), (200, {"usage_missing": True}, False, "stop:usage_missing"), (400, {}, False, "incompatible"),
                 (422, {}, False, "incompatible"), (400, {}, True, "stop:ping_rejected"), (401, {}, False, "stop:auth"),
                 (403, {}, False, "stop:auth"), (429, {}, False, "retry"), (500, {}, False, "retry"), (503, {}, True, "retry"),
                 (404, {}, False, "stop:unexpected_status"), (413, {}, False, "stop:unexpected_status"),
                 (429, {"gateway_refusal": "gateway_budget_exceeded"}, False, "stop:gateway_refusal"),
                 (None, {}, False, "stop:gateway_unreachable")]
        for status, over, ping, expected in table:
            with self.subTest(status=status, over=over, ping=ping):
                call = {"http_status": status, "gateway_refusal": None, "usage_missing": False, **over}
                self.assertEqual(sa.judge(call, is_ping=ping), expected)

    def test_describe_call_keeps_numbers_names_and_short_codes_and_never_the_words(self) -> None:
        prose = "a sentence that is not a field name, with spaces and a verdict about " + SENT
        raw = json.dumps({"error": {"message": prose, "type": prose, "code": "bad_value", "param": prose}}).encode()
        call = self.call(status=400, raw=raw)
        self.assertEqual(call["error"], {"type": None, "code": "bad_value", "param": None, "message_length": len(prose)})
        self.assertNotIn(SENT, json.dumps(call))
        raw = json.dumps({"model": prose, "choices": [{"finish_reason": prose}], "usage": {"prompt_tokens": "7", "x y": 1}}).encode()
        call = self.call(raw=raw)
        self.assertEqual((call["model_reported"], call["finish_reason"], call["prompt_tokens"], call["usage_fields"]), (None, None, None, ["prompt_tokens"]))
        self.assertNotIn(SENT, json.dumps(call))
        self.assertEqual(self.call(status=502, raw=b"<html>gateway</html>")["error"]["message_length"], len(b"<html>gateway</html>"))
        self.assertEqual(self.call(status=None, raw=b"")["error"], None)

    def test_usage_names_are_nested_with_dots_and_ignore_odd_keys(self) -> None:
        usage = {"prompt_tokens": 1, "prompt_tokens_details": {"cached_tokens": 0, "deep": {"deeper": {"deepest": {"x": 1}}}}, "bad key": 1}
        self.assertEqual(sa.usage_names(usage), ["prompt_tokens", "prompt_tokens_details", "prompt_tokens_details.cached_tokens",
                                                 "prompt_tokens_details.deep", "prompt_tokens_details.deep.deeper",
                                                 "prompt_tokens_details.deep.deeper.deepest"])
        self.assertEqual(sa.usage_names("text"), [])

    def test_refusal_proof_accepts_only_a_refusal_with_nothing_forwarded(self) -> None:
        good = {"refusal": "gateway_budget_exceeded", "http_status": 429, "input_tokens": None, "output_tokens": None, "cost": "0",
                "voided": False, "usage_missing": False, "model_reported": None}
        raw = json.dumps({"error": {"code": "gateway_budget_exceeded"}}).encode()
        self.assertEqual(sa.refusal_proof([good], 429, raw)["passed"], True)
        bad_records = [[], [good, good], [{**good, "refusal": None}], [{**good, "input_tokens": 5}], [{**good, "output_tokens": 0}],
                       [{**good, "cost": "0.0001"}], [{**good, "cost": None}], [{**good, "voided": True}],
                       [{**good, "usage_missing": True}], [{**good, "model_reported": "gpt"}], [{**good, "http_status": 200}],
                       [{**good, "refusal": "gateway_bad_request"}]]
        for records in bad_records:
            with self.subTest(records=str(records)[:60]):
                proof = sa.refusal_proof(records, 429, raw)
                self.assertEqual((proof["nothing_forwarded"], proof["passed"]), (False, False))
        for status, body in ((200, raw), (429, b'{"error": {"code": "rate_limit"}}'), (429, b"nope"), (None, b""), (502, raw)):
            with self.subTest(status=status):
                proof = sa.refusal_proof([good], status, body)
                self.assertEqual((proof["nothing_forwarded"], proof["passed"]), (True, False))

    def test_free_loopback_url_is_a_port_nothing_listens_on(self) -> None:
        import socket
        url = sa.free_loopback_url()
        port = int(url.split(":")[2].split("/")[0])
        with socket.socket() as probe:
            self.assertNotEqual(probe.connect_ex(("127.0.0.1", port)), 0)
        self.assertTrue(url.startswith("http://127.0.0.1:") and url.endswith("/v1"))

    def gates(self, calls: list[dict], not_sent: list[str] | None = None, refusal_passed: bool = True, cost: str = "0.001",
              names: list[str] | None = None) -> dict:
        entries = [{"name": n, "body": {"model": "m", "messages": [{"role": "user", "content": "q"}]}} for n in (names or [c["request"] for c in calls])]
        return sa.compute_gates(entries, calls, not_sent or [], {"passed": refusal_passed}, Decimal(cost))

    def test_the_reasoning_gate_needs_acceptance_and_zero_tokens_and_the_field_present_on_every_answer(self) -> None:
        zero = self.call("a")
        some = self.call("b", raw=json.dumps({"model": "m", "usage": {"prompt_tokens": 1, "completion_tokens": 1,
                                                                    "completion_tokens_details": {"reasoning_tokens": 3}}}).encode())
        absent = self.call("c", raw=json.dumps({"model": "m", "usage": {"prompt_tokens": 1, "completion_tokens": 1}}).encode())
        self.assertIs(self.gates([zero])["reasoning_off_ok"], True)
        g = self.gates([zero, some])
        self.assertEqual((g["reasoning_effort_accepted"], g["reasoning_tokens_zero_on_every_answer"], g["reasoning_off_ok"]), (True, False, False))
        g = self.gates([zero, absent])
        self.assertEqual((g["reasoning_tokens_reported_on_every_answer"], g["reasoning_tokens_zero_on_every_answer"], g["reasoning_off_ok"]),
                         (False, False, False))
        no_field = self.call("d", record={"request_defaults_applied": ["max_completion_tokens"]})
        self.assertIs(self.gates([zero, no_field])["reasoning_effort_accepted"], False)
        rejected = self.call("e", status=400, raw=json.dumps({"error": {"param": "reasoning_effort", "code": "unsupported_value"}}).encode())
        self.assertIs(self.gates([zero, rejected])["reasoning_effort_accepted"], False)
        self.assertIs(self.gates([rejected])["reasoning_off_ok"], False)
        self.assertIs(self.gates([])["reasoning_off_ok"], False)                      # no answer proves nothing

    def test_a_retried_request_counts_by_its_last_attempt_and_the_unsent_are_not_a_pass(self) -> None:
        first = self.call("a", status=429, outcome="retryable_error")
        second = self.call("a")
        self.assertIs(self.gates([first, second])["every_call_200_or_recorded_incompatible"], True)
        self.assertIs(self.gates([first])["every_call_200_or_recorded_incompatible"], False)
        self.assertIs(self.gates([second], not_sent=["b"], names=["a", "b"])["no_request_left_unsent"], False)
        self.assertIs(self.gates([second], refusal_passed=False)["refusal_test_passed"], False)
        self.assertIs(self.gates([second], cost="0.100001")["total_cost_within_stage_cap"], False)
        self.assertIs(self.gates([second], cost="0.1")["total_cost_within_stage_cap"], True)

    def test_a_null_max_tokens_is_judged_by_whether_the_gateway_added_the_limit_field_and_whether_the_provider_took_it(self) -> None:
        null_entry = {"name": "n", "body": {"model": "m", "max_tokens": None, "messages": [{"role": "user", "content": "q"}]}}
        added = self.call("n", entry=null_entry)
        not_added = self.call("n", entry=null_entry, record={"request_defaults_applied": ["reasoning_effort"]})
        refused = self.call("n", status=400, entry=null_entry)
        self.assertEqual((added["null_max_tokens_with_injected_limit"], not_added["null_max_tokens_with_injected_limit"]), (True, False))
        self.assertEqual(self.gates([added])["null_max_tokens_with_injected_limit"],
                         {"calls": 1, "all_accepted": True, "all_carried_the_injected_field": True})
        self.assertEqual(self.gates([not_added])["null_max_tokens_with_injected_limit"]["all_carried_the_injected_field"], False)
        self.assertEqual(self.gates([refused])["null_max_tokens_with_injected_limit"]["all_accepted"], False)
        self.assertIsNone(self.gates([self.call("a")])["null_max_tokens_with_injected_limit"])          # no such call: nothing to say

    def test_a_missing_usage_or_a_missing_injected_limit_fails_its_gate(self) -> None:
        none_usage = self.call("a", raw=json.dumps({"model": "m", "choices": [{"finish_reason": "stop"}]}).encode())
        self.assertIs(self.gates([none_usage])["usage_present_on_every_answer"], False)
        self.assertIs(self.gates([self.call("a")])["usage_present_on_every_answer"], True)
        missing = self.call("a", record={"request_defaults_applied": ["reasoning_effort"]})
        self.assertIs(self.gates([missing])["output_limit_injected_wherever_the_client_set_none"], False)
        own = self.call("a", record={"request_defaults_applied": ["reasoning_effort"]},
                        entry={"name": "a", "body": {"model": "m", "max_tokens": 500, "messages": [{"role": "user", "content": "q"}]}})
        self.assertEqual(own["client_limit"], "max_tokens=500")
        self.assertIs(self.gates([own])["output_limit_injected_wherever_the_client_set_none"], False)       # no call without a limit: nothing shown


if __name__ == "__main__":
    unittest.main()
