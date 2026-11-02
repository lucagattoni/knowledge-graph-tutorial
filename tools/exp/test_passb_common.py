"""Tests for tools/exp/passb_common.py. Standard library only; loopback only; no model, no provider, no real key.

The "provider" is a fake OpenAI-style server written here (it records every request with its Authorization header and answers
with a `usage` that includes `completion_tokens_details.reasoning_tokens`); the "local" upstream is a second fake that also
answers Ollama's `/api/tags`. The gateway is the real one (`tools/metering_gateway.py`), started as a subprocess. The key is a
made-up string assembled at run time from pieces and written to a mode-600 file in a temporary directory.

Run from the repository root:

    uv run python -m unittest tools/exp/test_passb_common.py
"""

from __future__ import annotations

import builtins
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "tools"))

import metering_gateway as mg  # noqa: E402
import passa_common as pc  # noqa: E402
import passb_common as pb  # noqa: E402

CANARY = "sk-" + "canary" + "-" + "Zr4Kq9" + "Lm2Xv7Tj"      # assembled here: the file holds no key-shaped literal
CHAT, EMBED = "gpt-6-luna", "embed-test"
PRICE = {"input": Decimal("0.13"), "output": Decimal("0.57"), "cached": Decimal("0.011"), "write": Decimal("0.171")}
OUTPUT_LIMIT = 6144
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def expected_cost(prompt: int, completion: int, cached: int = 0) -> Decimal:
    """Tokens times price, worked out from the definition (cached input at the cached price, the rest at the input price)."""
    return (Decimal(prompt - cached) * PRICE["input"] + Decimal(cached) * PRICE["cached"]
            + Decimal(completion) * PRICE["output"]) / Decimal(1_000_000)


class _Server(ThreadingHTTPServer):
    request_queue_size = 64
    daemon_threads = True


class FakeProvider:
    """A loopback server that plays a provider (or the local Ollama): records requests, answers chat and embeddings."""

    def __init__(self) -> None:
        self.prompt_tokens, self.completion_tokens, self.reasoning_tokens, self.cached_tokens = 1200, 300, 0, 0
        self.model = "gpt-6-luna-test-1"
        self.echo_authorization = False
        self.tags = [f"{EMBED}:latest"]
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

            def _record(self, body: dict | None) -> None:
                with outer._lock:
                    outer.requests.append({"method": self.command, "path": self.path, "body": body,
                                           "authorization": self.headers.get("Authorization")})

            def do_GET(self) -> None:  # noqa: N802
                self._record(None)
                if self.path == "/api/tags":
                    self._send(200, {"models": [{"name": n} for n in outer.tags]})
                else:
                    self._send(404, {"error": "not found"})

            def do_POST(self) -> None:  # noqa: N802
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
                self._record(body)
                if self.path.endswith("/chat/completions"):
                    usage = {"prompt_tokens": outer.prompt_tokens, "completion_tokens": outer.completion_tokens,
                             "total_tokens": outer.prompt_tokens + outer.completion_tokens,
                             "completion_tokens_details": {"reasoning_tokens": outer.reasoning_tokens}}
                    if outer.cached_tokens:
                        usage["prompt_tokens_details"] = {"cached_tokens": outer.cached_tokens}
                    text = self.headers.get("Authorization") or "" if outer.echo_authorization else "ok"
                    self._send(200, {"id": "chatcmpl-test", "object": "chat.completion", "model": outer.model,
                                     "choices": [{"index": 0, "finish_reason": "stop",
                                                  "message": {"role": "assistant", "content": text}}], "usage": usage})
                elif self.path.endswith("/embeddings"):
                    inputs = body.get("input") if isinstance(body.get("input"), list) else [body.get("input")]
                    tokens = 3 * len(inputs)
                    self._send(200, {"object": "list", "model": "embed-fake", "usage": {"prompt_tokens": tokens, "total_tokens": tokens},
                                     "data": [{"object": "embedding", "index": i, "embedding": [0.25, 0.5, 0.75]}
                                              for i in range(len(inputs))]})
                else:
                    self._send(404, {"error": "not found"})

        self.server = _Server(("127.0.0.1", 0), H)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.root = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.base_url = self.root + "/v1"

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()

    def chat_requests(self) -> list[dict]:
        return [r for r in self.requests if r["path"].endswith("/chat/completions")]

    def embedding_requests(self) -> list[dict]:
        return [r for r in self.requests if r["path"].endswith("/embeddings")]


def post(gw: pc.LocalGateway, path: str, payload: dict) -> tuple[int, str]:
    req = urllib.request.Request(gw.base_url + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": "Bearer dummy-not-a-key"})
    try:
        with OPENER.open(req, timeout=60) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode()


def chat(gw: pc.LocalGateway, text: str = "hello", **extra: object) -> tuple[int, str]:
    return post(gw, "/chat/completions", {"model": CHAT, "messages": [{"role": "user", "content": text}], **extra})


class Dirs(unittest.TestCase):
    """A temporary tree: a key file in its own directory, a ledger directory, run directories."""

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

    def profile_dict(self, base_url: str = "https://api.example.invalid/v1", **over: object) -> dict:
        d = {"base_url": base_url, "key_file": str(self.key_file), "ledger_dir": str(self.ledger), "allowance_usd": "0.01",
             "upstream_timeout_s": 900, "input_per_mtok": str(PRICE["input"]), "output_per_mtok": str(PRICE["output"]),
             "cached_input_per_mtok": str(PRICE["cached"]), "cache_write_per_mtok": str(PRICE["write"]),
             "source_url": "https://pricing.example.invalid/page", "read_at": "20261102 20:20",
             "output_limit_default": OUTPUT_LIMIT, "request_defaults": {"reasoning_effort": "none"}}
        d.update(over)
        return {k: v for k, v in d.items() if v is not ...}      # `...` removes a key

    def write_profile(self, d: dict | None = None, name: str = "profile.json") -> Path:
        path = self.root / name
        path.write_text(json.dumps(self.profile_dict() if d is None else d))
        return path

    def load(self, **over: object) -> pb.Profile:
        return pb.load_profile(self.write_profile(self.profile_dict(**over)))


class ProfileTests(Dirs):
    def refused(self, d: dict, needle: str = "") -> str:
        with self.assertRaises(pb.ProfileError) as ctx:
            pb.load_profile(self.write_profile(d))
        message = str(ctx.exception)
        self.assertIn(needle, message)
        for secret in (CANARY, str(self.key_file), str(self.ledger)):      # an error names the field, never a value
            self.assertNotIn(secret, message)
        return message

    def test_a_good_profile_loads_with_exact_decimals_and_the_documented_defaults(self) -> None:
        d = self.profile_dict()
        for key in ("base_url", "upstream_timeout_s", "cached_input_per_mtok", "cache_write_per_mtok"):
            del d[key]
        p = pb.load_profile(self.write_profile(d))
        self.assertEqual((p.base_url, p.upstream_timeout_s), ("https://api.openai.com/v1", 900))
        self.assertEqual((p.cached_input_per_mtok, p.cache_write_per_mtok), (None, None))
        self.assertEqual((p.input_per_mtok, p.output_per_mtok, p.allowance_usd), (Decimal("0.13"), Decimal("0.57"), Decimal("0.01")))
        self.assertEqual((p.key_file, p.ledger_dir, p.output_limit_default), (str(self.key_file), str(self.ledger), OUTPUT_LIMIT))
        self.assertEqual(dict(p.request_defaults), {"reasoning_effort": "none"})

    def test_json_numbers_are_read_as_exact_decimals_never_floats(self) -> None:
        text = json.dumps(self.profile_dict()).replace('"0.13"', "0.13").replace('"0.01"', "0.01")
        path = self.root / "numbers.json"
        path.write_text(text)
        p = pb.load_profile(path)
        self.assertIsInstance(p.input_per_mtok, Decimal)
        self.assertEqual((p.input_per_mtok, p.allowance_usd), (Decimal("0.13"), Decimal("0.01")))

    def test_every_required_key_is_required_and_is_named(self) -> None:
        for key in pb.REQUIRED_KEYS:
            with self.subTest(key=key):
                self.refused(self.profile_dict(**{key: ...}), key)
        for key in ("base_url", "upstream_timeout_s", "cached_input_per_mtok", "cache_write_per_mtok"):      # these have defaults
            with self.subTest(optional=key):
                self.load(**{key: ...})

    def test_an_unknown_key_a_duplicate_key_a_non_object_and_bad_json_are_refused(self) -> None:
        self.refused(self.profile_dict(allowence_usd="1"), "allowence_usd")        # a typo is not silently ignored
        path = self.root / "dup.json"
        path.write_text(json.dumps(self.profile_dict()).replace("{", '{"allowance_usd": "5", ', 1))
        with self.assertRaisesRegex(pb.ProfileError, "given twice"):
            pb.load_profile(path)
        for text, needle in (("[1]", "JSON object"), ("{not json", "not valid JSON"), ('{"input_per_mtok": NaN}', "number JSON allows"),
                             ("", "not valid JSON")):
            path.write_text(text)
            with self.assertRaisesRegex(pb.ProfileError, needle):
                pb.load_profile(path)
        with self.assertRaisesRegex(pb.ProfileError, "cannot read"):
            pb.load_profile(self.root / "missing.json")

    def test_values_that_are_odd_are_refused(self) -> None:
        bad = {
            "allowance_usd": [0, "0", -1, "-1", True, "abc", "1e3", "NaN", "0.0000000001", 10 ** 8, "1" * 19, [1]],
            "input_per_mtok": [0, "0", "0.00", -0.1, "x"],           # a hosted model is not free
            "output_per_mtok": [0, "0", "0.0", -2],
            "cached_input_per_mtok": [-1, "-0.1", True, "x"],
            "cache_write_per_mtok": [-1, True],
            "upstream_timeout_s": [0, -5, True, 1.5, "900", 86401, None],
            "output_limit_default": [0, -1, True, "6144", 1.5, None],
            "base_url": ["ftp://x/v1", "http://api.example.com/v1", "https://user:pw@host/v1", "https://host/v1?x=1",
                         "https://host/v1#f", "", 5, "not a url"],
            "source_url": ["pricing page", "", 3, None],
            "read_at": ["2026-11-02", "20261102 2:20", "20261102", 1, None],
            "key_file": ["key.txt", "", "/", CANARY, "sk-" + "x" * 10, "/a\nb", 5, None, "/tmp/\x00x"],
            "ledger_dir": ["ledger", "", "/", "\t", 5, None],
            "request_defaults": [[], "x", None, {"max_tokens": 5}, {"max_completion_tokens": 1}, {"model": "m"}, {"stream": True},
                                 {"bad name": 1}, {"a": None}, {"a": [1]}],
        }
        for key, values in bad.items():
            for value in values:
                with self.subTest(key=key, value=repr(value)[:30]):
                    self.refused(self.profile_dict(**{key: value}), key.split(".")[0])

    def test_plain_http_is_allowed_only_towards_loopback_and_zero_is_allowed_for_the_optional_prices(self) -> None:
        self.assertEqual(self.load(base_url="http://127.0.0.1:8123/v1/").base_url, "http://127.0.0.1:8123/v1")
        self.assertEqual(self.load(base_url="http://localhost:9/v1").base_url, "http://localhost:9/v1")
        p = self.load(cached_input_per_mtok="0", cache_write_per_mtok=0)
        self.assertEqual((p.cached_input_per_mtok, p.cache_write_per_mtok), (Decimal(0), Decimal(0)))

    def test_a_key_pasted_where_a_path_belongs_is_refused_without_showing_it(self) -> None:
        message = self.refused(self.profile_dict(key_file=CANARY), "looks like a key")
        self.assertNotIn(CANARY[:8], message)

    def test_repr_and_redact_hide_the_two_paths(self) -> None:
        p = self.load()
        self.assertNotIn(str(self.key_file), repr(p))
        self.assertNotIn(str(self.ledger), repr(p))
        text = p.redact(f"read {self.key_file} and wrote {self.ledger}/meter.jsonl and {self.keydir}")
        self.assertNotIn(str(self.key_file), text)
        self.assertNotIn(str(self.ledger), text)
        self.assertIn("<key_file>", text)
        self.assertIn("<ledger>/meter.jsonl", text)

    def test_redact_takes_the_longer_path_first_when_one_path_holds_the_other(self) -> None:
        key = self.ledger / "provider.key"                      # the key file lives inside the ledger directory
        p = self.load(ledger_dir=str(self.ledger), key_file=str(key))
        self.assertEqual(p.redact(f"read {key} in {self.ledger}"), "read <key_file> in <ledger>")

    def test_the_example_cannot_run_as_it_stands_and_runs_once_its_two_placeholders_are_filled(self) -> None:
        example = HERE / "passb_profile.example.json"
        raw = json.loads(example.read_text())
        self.assertTrue(set(pb.REQUIRED_KEYS) <= set(raw) <= set(pb.ALLOWED_KEYS))
        with self.assertRaisesRegex(pb.ProfileError, "absolute path"):
            pb.load_profile(example)
        text = example.read_text()
        for forbidden in ("/Users", "/private", "/home/", "sk-"):
            self.assertNotIn(forbidden, text)
        filled = {**raw, "key_file": str(self.key_file), "ledger_dir": str(self.ledger)}
        p = pb.load_profile(self.write_profile(filled))
        self.assertEqual((p.output_limit_default, dict(p.request_defaults)), (6144, {"reasoning_effort": "none"}))
        self.assertEqual((p.upstream_timeout_s, p.base_url), (900, "https://api.openai.com/v1"))


class ConfigTests(Dirs):
    """The config the class writes, read back with the gateway's own parser. No process is started."""

    def gw(self, name: str = "run", request_defaults: dict | None = None, models: tuple = (CHAT, EMBED), **over: object) -> pb.HostedGateway:
        return pb.HostedGateway(self.root / name, "http://127.0.0.1:11434/v1", list(models), REPO, profile=self.load(**over),
                                request_defaults=request_defaults)

    def parsed(self, gw: pb.HostedGateway, cap: str = "1.5") -> mg.Config:
        gw.cap = Decimal(cap)
        return mg.parse_config(gw.write_config().read_text(), {})           # an EMPTY environment: no key variable is needed

    def test_two_upstreams_the_chat_model_on_the_hosted_one_and_the_embedding_model_on_the_local_one(self) -> None:
        cfg = self.parsed(self.gw())
        hosted, local = cfg.upstreams["hosted"], cfg.upstreams["local"]
        self.assertEqual((hosted.protocol, hosted.base_url, hosted.dry_run, hosted.allow_request_defaults),
                         ("openai", "https://api.example.invalid/v1", False, True))
        self.assertEqual(hosted.key_file, str(self.key_file))
        self.assertIsNotNone(hosted.key)                                     # the gateway read the file itself
        self.assertEqual((local.protocol, local.base_url, local.dry_run, local.key, local.key_file),
                         ("openai", "http://127.0.0.1:11434/v1", True, None, None))
        chat_model, embed_model = cfg.models[CHAT], cfg.models[EMBED]
        self.assertEqual((chat_model.upstream, embed_model.upstream), ("hosted", "local"))
        price = chat_model.price
        self.assertEqual((price.input_per_mtok, price.output_per_mtok, price.cached_input_per_mtok, price.cache_write_per_mtok),
                         (PRICE["input"], PRICE["output"], PRICE["cached"], PRICE["write"]))
        self.assertEqual((price.source_url, price.read_at), ("https://pricing.example.invalid/page", "20261102 20:20"))
        self.assertEqual((chat_model.output_limit_default, dict(chat_model.request_defaults)), (OUTPUT_LIMIT, {"reasoning_effort": "none"}))
        self.assertEqual((embed_model.price.input_per_mtok, embed_model.price.output_per_mtok), (0, 0))
        self.assertIsNone(embed_model.output_limit_default)
        self.assertEqual(dict(embed_model.request_defaults), {})
        self.assertEqual(set(cfg.models), {CHAT, EMBED})

    def test_the_gateway_section(self) -> None:
        gw = self.gw()
        cfg = self.parsed(gw, cap="0.0123456789")
        self.assertEqual((cfg.currency, cfg.cap, cfg.upstream_timeout_s, cfg.log_bodies), ("USD", Decimal("0.0123456789"), 900.0, True))
        self.assertEqual(Path(cfg.log_file), self.ledger / "meter.jsonl")          # the shared ledger, not the run directory
        self.assertEqual(Path(cfg.body_log_file), self.ledger / "meter.jsonl.bodies.jsonl")
        self.assertEqual(gw.log_path, self.ledger / "meter.jsonl")
        self.assertEqual(gw.body_path, self.ledger / "meter.jsonl.bodies.jsonl")
        self.assertEqual(self.parsed(self.gw(upstream_timeout_s=77)).upstream_timeout_s, 77.0)

    def test_the_text_holds_the_path_of_the_key_file_and_never_the_key(self) -> None:
        gw = self.gw()
        gw.cap = Decimal(1)
        text = gw.write_config().read_text()
        self.assertIn(str(self.key_file), text)
        self.assertNotIn(CANARY, text)

    def test_an_option_given_to_the_runner_wins_over_the_profile_and_the_rest_is_kept(self) -> None:
        cfg = self.parsed(self.gw(request_defaults={CHAT: {"reasoning_effort": "low", "seed": 7, "thinking": {"type": "off"}}}))
        self.assertEqual(dict(cfg.models[CHAT].request_defaults), {"reasoning_effort": "low", "seed": 7, "thinking": {"type": "off"}})
        cfg = self.parsed(self.gw(request_defaults={CHAT: {"seed": 7}}))
        self.assertEqual(dict(cfg.models[CHAT].request_defaults), {"reasoning_effort": "none", "seed": 7})
        cfg = self.parsed(self.gw(request_defaults={}))
        self.assertEqual(dict(cfg.models[CHAT].request_defaults), {"reasoning_effort": "none"})

    def test_a_profile_with_no_defaults_and_no_option_writes_no_table(self) -> None:
        gw = pb.HostedGateway(self.root / "none", "http://127.0.0.1:1/v1", [CHAT, EMBED], REPO,
                              profile=self.load(request_defaults={}))
        self.assertEqual(dict(self.parsed(gw).models[CHAT].request_defaults), {})

    def test_optional_prices_are_left_out_when_the_profile_has_none(self) -> None:
        cfg = self.parsed(self.gw(cached_input_per_mtok=..., cache_write_per_mtok=...))
        self.assertEqual((cfg.models[CHAT].price.cached_input_per_mtok, cfg.models[CHAT].price.cache_write_per_mtok), (None, None))

    def test_models_and_defaults_that_cannot_be_served_are_refused_before_anything_starts(self) -> None:
        with self.assertRaisesRegex(pc.PassAError, "two different models"):
            self.gw(models=(CHAT, CHAT))
        with self.assertRaisesRegex(pc.PassAError, "two different models"):
            self.gw(models=(CHAT,))
        with self.assertRaisesRegex(pc.PassAError, "letters, digits"):
            self.gw(models=('bad"name', EMBED))
        with self.assertRaisesRegex(pc.PassAError, "do not serve|does not serve"):
            self.gw(request_defaults={"other": {"seed": 1}})
        with self.assertRaisesRegex(pc.PassAError, "may not set"):
            self.gw(request_defaults={CHAT: {"max_tokens": 5}})

    def test_a_ledger_inside_the_repository_is_refused_because_its_body_log_holds_article_text(self) -> None:
        with self.assertRaisesRegex(pc.PassAError, "inside the repository"):
            pb.HostedGateway(self.root / "run", "http://127.0.0.1:1/v1", [CHAT, EMBED], REPO,
                             profile=self.load(ledger_dir=str(REPO / "some-ledger")))

    def test_the_cap_is_not_known_until_the_ledger_has_been_read(self) -> None:
        with self.assertRaisesRegex(pc.PassAError, "cap is computed"):
            self.gw().write_config()

    def test_make_gateway_gives_the_pass_a_class_without_a_profile_and_the_hosted_one_with_one(self) -> None:
        local = pb.make_gateway(None, self.root / "a", "http://127.0.0.1:1/v1", [CHAT, EMBED], REPO, timeout_s=77,
                                request_defaults={CHAT: {"seed": 7}})
        self.assertIs(type(local), pc.LocalGateway)
        self.assertEqual((local.timeout_s, local.request_defaults), (77, {CHAT: {"seed": 7}}))
        self.assertEqual(pb.make_gateway(None, self.root / "a", "http://127.0.0.1:1/v1", [CHAT, EMBED], REPO).timeout_s, 1800)
        hosted = pb.make_gateway(self.load(), self.root / "b", "http://127.0.0.1:1/v1", [CHAT, EMBED], REPO, timeout_s=77)
        self.assertIsInstance(hosted, pb.HostedGateway)
        self.assertEqual(hosted.timeout_s, 900)              # one setting serves both upstreams: the profile's wins

    def test_a_money_amount_is_plain_text_without_exponent_or_trailing_zeros(self) -> None:
        self.assertEqual([pb.money_text(Decimal(x)) for x in ("0.60", "0", "100", "1E+2", "0.000150", "3.00")],
                         ["0.6", "0", "100", "100", "0.00015", "3"])


class LedgerFileTests(unittest.TestCase):
    def test_strict_reading_refuses_a_line_that_is_not_json_and_loose_reading_leaves_an_unfinished_line_for_later(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "meter.jsonl"
            self.assertEqual(pb.read_ledger(path, strict=True), [])
            path.write_bytes(b'{"a":1}\n\n{"a":2}\n{"a":3')           # the last line has no newline yet
            self.assertEqual(pb.read_ledger(path, strict=False), [{"a": 1}, {"a": 2}])
            with self.assertRaisesRegex(pc.PassAError, "line 4"):
                pb.read_ledger(path, strict=True)
            path.write_bytes(b'{"a":1}\nnot json\n')
            with self.assertRaisesRegex(pc.PassAError, "line 2"):
                pb.read_ledger(path, strict=False)
            path.write_bytes(b'[1]\n')
            with self.assertRaisesRegex(pc.PassAError, "not a JSON object"):
                pb.read_ledger(path, strict=True)
            path.write_bytes(b'{"a":1}\nnot json\n[2]\n{"a":4}\n')                  # a run reads from where it began
            self.assertEqual(pb.read_ledger(path, strict=True, start=len(b'{"a":1}\nnot json\n[2]\n')), [{"a": 4}])
            self.assertEqual(pb.read_ledger(path, strict=False, start=len(b'{"a":1}\nnot json\n[2]\n{"a":4}\n')), [])
            self.assertEqual(pb.read_ledger(path, strict=False, start=10**6), [])

    def test_costs_are_summed_exactly_and_a_record_without_one_is_an_error(self) -> None:
        self.assertEqual(pb.sum_costs([{"cost": "0.1"}, {"cost": "0.2"}, {"cost": "0"}]), Decimal("0.3"))
        self.assertEqual(pb.cost_usd([{"cost": "0.000327"}, {"cost": "0.00301"}]), "0.003337")
        self.assertEqual(pb.cost_usd([]), "0")
        with self.assertRaises(pc.PassAError):
            pb.sum_costs([{"cost": "0.1"}, {"tokens": 5}])
        with self.assertRaises(pc.PassAError):
            pb.sum_costs([{"cost": "abc"}])


class GatewayCase(Dirs):
    def setUp(self) -> None:
        super().setUp()
        self.paid, self.local = FakeProvider(), FakeProvider()
        self.addCleanup(self.paid.close)
        self.addCleanup(self.local.close)

    def gateway(self, name: str, *, allowance: str = "0.01", request_defaults: dict | None = None, **over: object) -> pb.HostedGateway:
        profile = self.load(base_url=self.paid.base_url, allowance_usd=allowance, **over)
        return pb.HostedGateway(self.root / name, self.local.base_url, [CHAT, EMBED], REPO, profile=profile,
                                request_defaults=request_defaults)

    def popen_spy(self) -> tuple[list, mock._patch]:
        real, seen = subprocess.Popen, []

        def spy(*args: object, **kwargs: object) -> subprocess.Popen:
            seen.append((args, kwargs))
            return real(*args, **kwargs)

        return seen, mock.patch.object(pb.subprocess, "Popen", spy)


class OneCallTests(GatewayCase):
    def test_a_chat_call_reaches_the_provider_with_the_key_and_both_defaults_and_is_priced_from_its_usage(self) -> None:
        with self.gateway("run1") as gw:
            status, text = chat(gw)
            calls = gw.calls()
        self.assertEqual(status, 200)
        (request,) = self.paid.chat_requests()
        self.assertEqual(request["authorization"], "Bearer " + CANARY)
        self.assertEqual(request["body"]["reasoning_effort"], "none")
        self.assertEqual(request["body"]["max_completion_tokens"], OUTPUT_LIMIT)
        self.assertNotIn("max_tokens", request["body"])
        self.assertEqual(request["path"], "/v1/chat/completions")
        (call,) = calls
        self.assertEqual(Decimal(call["cost"]), expected_cost(1200, 300))
        self.assertEqual(Decimal(call["cost"]), Decimal("0.000327"))
        self.assertEqual((call["upstream"], call["http_status"], call["input_tokens"], call["output_tokens"]), ("hosted", 200, 1200, 300))
        self.assertEqual((call["model_requested"], call["model_reported"], call["currency"]), (CHAT, "gpt-6-luna-test-1", "USD"))
        self.assertEqual(call["request_defaults_applied"], ["reasoning_effort", "max_completion_tokens"])
        self.assertNotIn("reasoning_effort", call["request"])             # the body log keeps what the builder sent
        self.assertEqual(call["response"]["usage"]["completion_tokens_details"], {"reasoning_tokens": 0})

    def test_cached_input_is_priced_at_the_cached_rate_and_reasoning_tokens_are_read_from_the_body_log(self) -> None:
        self.paid.prompt_tokens, self.paid.completion_tokens, self.paid.cached_tokens, self.paid.reasoning_tokens = 5000, 800, 2000, 120
        with self.gateway("run1") as gw:
            chat(gw)
            calls = gw.calls()
        self.assertEqual(Decimal(calls[0]["cost"]), expected_cost(5000, 800, cached=2000))
        self.assertEqual(calls[0]["cached_input_tokens"], 2000)
        self.assertEqual(pc.response_facts(calls)["reasoning_tokens_total"], 120)        # billed inside completion_tokens

    def test_embeddings_go_to_the_local_upstream_only_at_price_zero_and_without_a_key(self) -> None:
        with self.gateway("run1") as gw:
            status, text = post(gw, "/embeddings", {"model": EMBED, "input": ["a", "b"]})
            chat(gw)
            calls = gw.calls()
        self.assertEqual(status, 200)
        self.assertEqual(len(json.loads(text)["data"]), 2)
        self.assertEqual(len(self.local.embedding_requests()), 1)
        self.assertIsNone(self.local.embedding_requests()[0]["authorization"])
        self.assertEqual(self.local.chat_requests(), [])                              # the chat model never reaches the local server
        self.assertEqual(self.paid.embedding_requests(), [])                          # the embedding model never reaches the provider
        emb, ch = calls
        self.assertEqual((emb["upstream"], emb["cost"], emb["input_tokens"]), ("local", "0", 6))
        self.assertEqual(ch["upstream"], "hosted")

    def test_a_runner_option_beats_the_profile_default_and_a_limit_the_client_sent_is_kept(self) -> None:
        with self.gateway("run1", request_defaults={CHAT: {"reasoning_effort": "low", "seed": 7}}) as gw:
            chat(gw)
            chat(gw, max_completion_tokens=50)
            calls = gw.calls()
        first, second = (r["body"] for r in self.paid.chat_requests())
        self.assertEqual((first["reasoning_effort"], first["seed"], first["max_completion_tokens"]), ("low", 7, OUTPUT_LIMIT))
        self.assertEqual(second["max_completion_tokens"], 50)
        self.assertEqual([c["request_defaults_applied"] for c in calls],
                         [["reasoning_effort", "seed", "max_completion_tokens"], ["reasoning_effort", "seed"]])

    def test_calls_before_the_start_is_an_error_and_the_directory_of_the_ledger_is_private(self) -> None:
        gw = self.gateway("run1")
        with self.assertRaisesRegex(pc.PassAError, "not started"):
            gw.calls()
        with self.assertRaises(pc.PassAError):
            _ = gw.base_url
        with gw:
            pass
        self.assertEqual(stat.S_IMODE(os.stat(self.ledger).st_mode), 0o700)           # it will hold article text


class EnvironmentTests(GatewayCase):
    def test_the_gateway_subprocess_gets_the_minimal_environment_and_no_key_on_its_command_line(self) -> None:
        seen, patch = self.popen_spy()
        with patch:
            with self.gateway("run1") as gw:
                chat(gw)
            with self.gateway("run2") as gw:
                chat(gw)
        self.assertEqual(len(seen), 2)
        for args, kwargs in seen:
            self.assertEqual(kwargs["env"], {"PATH": "/usr/bin:/bin"})
            self.assertNotIn(CANARY, " ".join(map(str, args[0])))
            self.assertNotIn("PASSA_UNUSED_KEY", kwargs["env"])
            self.assertEqual(Path(kwargs["cwd"]).name in ("run1", "run2"), True)
        self.assertNotIn("--resume", seen[0][0][0])                       # an empty ledger: a plain start
        self.assertIn("--resume", seen[1][0][0])                           # a ledger with records: the run is continued

    def test_the_runner_side_code_never_opens_the_key_file(self) -> None:
        opened: list[str] = []
        real_open, real_io_open, real_os_open = builtins.open, io.open, os.open

        def note(target: object) -> None:
            try:
                opened.append(os.fspath(target))
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

        with mock.patch.object(builtins, "open", spy_open), mock.patch.object(io, "open", spy_io_open), \
                mock.patch.object(os, "open", spy_os_open):
            with self.gateway("run1") as gw:
                chat(gw)
                gw.calls()
            json.dumps(gw.hosted_block())
        self.assertTrue(any(p.endswith("meter.jsonl") for p in opened))      # the spy sees what the runner side opens
        self.assertNotIn(str(self.key_file), opened)
        self.assertFalse([p for p in opened if p.endswith("provider.key")])

    def test_a_missing_or_unsafe_key_file_stops_the_start_and_the_message_names_no_path(self) -> None:
        for label, damage in (("missing", lambda: self.key_file.unlink()), ("mode", lambda: self.key_file.chmod(0o644))):
            with self.subTest(label):
                damage()
                gw = self.gateway(f"run-{label}")
                with self.assertRaises(pc.PassAError) as ctx:
                    gw.start()
                message = str(ctx.exception)
                self.assertIn("did not start", message)
                self.assertNotIn(str(self.key_file), message)
                self.assertNotIn(str(self.ledger), message)
                self.assertNotIn(CANARY, message)
                self.assertIsNone(gw.proc)
                self.assertEqual(self.paid.requests, [])
                self.key_file.write_text(CANARY + "\n")
                self.key_file.chmod(0o600)

    def test_the_canary_the_key_is_in_the_key_file_and_in_the_providers_request_and_nowhere_else(self) -> None:
        self.paid.echo_authorization = True          # worst case: the provider puts the key it received into its answer
        outputs, blocks, replies = [], [], []
        argv_before = list(sys.argv)
        for name in ("run1", "run2"):
            with self.gateway(name) as gw:
                replies.append(chat(gw)[1])
                post(gw, "/embeddings", {"model": EMBED, "input": ["x"]})
                gw.calls()
            outputs.append(gw.output)
            blocks.append(json.dumps(gw.hosted_block()))
        # not vacuous: the provider received the key, the key file holds it, the echo really happened
        self.assertEqual({r["authorization"] for r in self.paid.chat_requests()}, {"Bearer " + CANARY})
        self.assertIn(CANARY, self.key_file.read_text())
        # the runner side: the process environment, the command line, everything the gateway answered, its stdout and the result block
        self.assertEqual(sys.argv, argv_before)
        self.assertNotIn(CANARY, " ".join(sys.argv))
        self.assertFalse([k for k, v in os.environ.items() if CANARY in k or CANARY in v])
        for reply in replies:
            self.assertNotIn(CANARY, reply)
            self.assertIn("[redacted]", reply)
        for text in outputs + blocks:
            self.assertNotIn(CANARY, text)
        # every file under the run directories and the ledger
        scanned = [p for base in (self.root / "run1", self.root / "run2", self.ledger) for p in base.rglob("*") if p.is_file()]
        names = {p.name for p in scanned}
        self.assertTrue({"gateway.toml", "meter.jsonl", "meter.jsonl.bodies.jsonl"} <= names, names)
        self.assertEqual(len([n for n in names if n.startswith("meter.jsonl.manifest-")]), 2)       # one manifest per start
        self.assertEqual([str(p) for p in scanned if CANARY.encode() in p.read_bytes()], [])
        # the gateway's banner names the key file's path (outside every scanned directory) but never the key
        self.assertTrue(all(str(self.key_file) in o for o in outputs))


class LedgerTests(GatewayCase):
    def test_two_runs_sharing_a_ledger_the_second_sees_only_its_own_calls_and_a_cap_of_spent_plus_allowance(self) -> None:
        self.paid.prompt_tokens, self.paid.completion_tokens = 10000, 3000
        unit = expected_cost(10000, 3000)                                    # 0.00301 per call
        seen, patch = self.popen_spy()
        with patch:
            with self.gateway("run1", allowance="0.01") as gw1:
                self.assertEqual((gw1.records_before, gw1.spent_before, gw1.cap), (0, Decimal(0), Decimal("0.01")))
                self.assertEqual([chat(gw1)[0], chat(gw1)[0]], [200, 200])
                calls1 = gw1.calls()
            with self.gateway("run2", allowance="0.01") as gw2:
                self.assertEqual((gw2.records_before, gw2.spent_before), (2, 2 * unit))
                self.assertEqual(gw2.cap, 2 * unit + Decimal("0.01"))
                cfg2 = mg.parse_config((self.root / "run2" / "gateway.toml").read_text(), {})
                self.assertEqual(cfg2.cap, Decimal("0.01602"))
                self.assertEqual(gw2.calls(), [])                            # nothing of the first run
                statuses = [chat(gw2)[0] for _ in range(4)]
                calls2 = gw2.calls()
        self.assertEqual(len(calls1), 2)
        self.assertEqual(statuses, [200, 200, 200, 429])                      # 3 more fit under 0.01 of allowance, the 4th does not
        self.assertEqual(len(calls2), 4)
        self.assertFalse({c["call_id"] for c in calls1} & {c["call_id"] for c in calls2})
        self.assertEqual(calls2[-1]["refusal"], "gateway_budget_exceeded")
        self.assertEqual(len(self.paid.chat_requests()), 5)                   # the refused call was never forwarded
        self.assertIn("--resume", seen[1][0][0])
        ledger_lines = (self.ledger / "meter.jsonl").read_text().splitlines()
        self.assertEqual(len(ledger_lines), 6)                                # one file for both runs
        self.assertEqual(sum(Decimal(json.loads(x)["cost"]) for x in ledger_lines), 5 * unit)
        with self.gateway("run3", allowance="0.01") as gw3:                   # a third start reads the whole history
            self.assertEqual((gw3.records_before, gw3.spent_before), (6, 5 * unit))

    def test_the_refusal_body_is_the_gateways_budget_error(self) -> None:
        with self.gateway("run1", allowance="0.001") as gw:
            status, text = chat(gw)
        self.assertEqual(status, 429)
        self.assertEqual(json.loads(text)["error"]["code"], "gateway_budget_exceeded")
        self.assertEqual(self.paid.requests, [])

    def test_an_allowance_smaller_than_one_reservation_refuses_the_first_call_even_with_a_history(self) -> None:
        with self.gateway("run1") as gw:
            self.assertEqual(chat(gw)[0], 200)
        with self.gateway("run2", allowance="0.001") as gw:
            self.assertEqual(chat(gw)[0], 429)
            self.assertEqual(chat(gw)[0], 429)
            calls = gw.calls()
        self.assertEqual(len(self.paid.chat_requests()), 1)                   # only the first run's call ever reached the provider
        self.assertEqual([c["refusal"] for c in calls], ["gateway_budget_exceeded"] * 2)

    def test_hosted_block_totals_cover_this_run_only_and_a_checkpoint_cost_is_a_prefix_sum(self) -> None:
        with self.gateway("run1") as gw:
            for _ in range(3):
                chat(gw)
        with self.gateway("run2") as gw:
            for _ in range(2):
                chat(gw)
            calls = gw.calls()
        block = gw.hosted_block()
        unit = expected_cost(1200, 300)
        self.assertEqual(Decimal(block["cost_usd"]), 2 * unit)
        self.assertEqual((block["ledger_records_before"], block["ledger_records_after"], block["calls_in_this_run"]), (3, 5, 2))
        self.assertEqual(Decimal(block["spent_before_usd"]), 3 * unit)
        self.assertEqual(Decimal(block["cap_usd"]), 3 * unit + Decimal("0.01"))
        self.assertEqual([pb.cost_usd(calls[:k]) for k in (0, 1, 2)], ["0", pb.money_text(unit), pb.money_text(2 * unit)])

    def test_the_lines_of_earlier_stages_are_not_parsed_again_even_a_damaged_one_or_a_body_log_cut_by_a_killed_gateway(self) -> None:
        with self.gateway("run1") as gw:
            chat(gw)
        bodies = self.ledger / "meter.jsonl.bodies.jsonl"
        lines = bodies.read_bytes().splitlines(keepends=True)
        bodies.write_bytes(b"this earlier line is not JSON\n" + b"".join(lines[1:]) + b'{"call_id": "cut", "requ')   # killed mid-write
        with self.gateway("run2") as gw:
            chat(gw, "first of run 2")
            chat(gw, "second of run 2")
            calls = gw.calls()                    # would raise if the earlier stage's lines were parsed again
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0]["request"]["messages"][0]["content"], "first of run 2")    # the cut line's start is not in this run
        self.assertEqual(calls[1]["request"]["messages"][0]["content"], "second of run 2")
        self.assertEqual(Decimal(pb.cost_usd(calls)), 2 * expected_cost(1200, 300))

    def test_a_ledger_whose_last_line_is_unfinished_stops_the_start_because_nothing_is_running_to_finish_it(self) -> None:
        self.ledger.mkdir()
        (self.ledger / "meter.jsonl").write_text('{"cost": "0.1"}\n{"cost": "0.2"')
        with self.assertRaisesRegex(pc.PassAError, "ledger's line 2"):
            self.gateway("run1").start()
        self.assertEqual(self.paid.requests, [])

    def test_a_ledger_with_a_line_that_is_not_json_stops_the_start(self) -> None:
        self.ledger.mkdir()
        (self.ledger / "meter.jsonl").write_text('{"cost": "0.1"}\nnot json\n')
        with self.assertRaisesRegex(pc.PassAError, "line 2"):
            self.gateway("run1").start()
        self.assertEqual(self.paid.requests, [])


class HostedBlockTests(GatewayCase):
    def test_the_block_records_the_hosted_side_and_holds_no_key_no_key_path_and_no_ledger_path(self) -> None:
        self.paid.reasoning_tokens = 12
        with self.gateway("run1", allowance="0.01") as gw:
            self.assertEqual(gw.hosted_block()["started"], True)
            chat(gw)
            chat(gw)
            post(gw, "/embeddings", {"model": EMBED, "input": ["x"]})
        block = gw.hosted_block()
        text = json.dumps(block)
        for secret in (CANARY, str(self.key_file), str(self.ledger), str(self.root), self.key_file.name):
            self.assertNotIn(secret, text)
        self.assertEqual((block["key_file"], block["ledger"]), ("set", "shared"))
        self.assertEqual(block["model_reported"], {"gpt-6-luna-test-1": 2})
        self.assertEqual(block["currency"], "USD")
        self.assertEqual(Decimal(block["cost_usd"]), 2 * expected_cost(1200, 300))
        self.assertEqual((block["allowance_usd"], block["spent_before_usd"], block["cap_usd"]), ("0.01", "0", "0.01"))
        self.assertEqual(block["prices"], {"unit": "per million tokens", "input_per_mtok": "0.13", "output_per_mtok": "0.57",
                                           "cached_input_per_mtok": "0.011", "cache_write_per_mtok": "0.171",
                                           "source_url": "https://pricing.example.invalid/page", "read_at": "20261102 20:20"})
        self.assertEqual(block["output_limit_default"], OUTPUT_LIMIT)
        self.assertEqual((block["request_defaults_names"], block["request_defaults"]), (["reasoning_effort"], {"reasoning_effort": "none"}))
        self.assertEqual((block["ledger_records_before"], block["ledger_records_after"], block["calls_in_this_run"]), (0, 3, 3))
        self.assertEqual(block["response_facts"]["reasoning_tokens_total"], 24)
        self.assertEqual((block["chat_upstream"], block["embedding_upstream"], block["upstream_timeout_s"]), ("hosted", "local", 900))
        self.assertEqual(len(block["run_records_sha256"]), 64)
        self.assertEqual(block, gw.hosted_block())                       # a finished run gives the same block every time

    def test_a_block_before_the_start_says_so_and_still_holds_the_settings(self) -> None:
        block = self.gateway("run1").hosted_block()
        self.assertEqual(block["started"], False)
        self.assertEqual(block["chat_model"], CHAT)
        self.assertNotIn("cost_usd", block)


class EmbeddingPreflightTests(GatewayCase):
    def test_an_installed_embedding_model_passes_and_the_chat_model_is_not_looked_at(self) -> None:
        facts = pb.embedding_preflight(self.local.base_url, EMBED)
        self.assertEqual((facts["ollama"], facts["embedding_model_installed"], facts["chat_model_checked"]), (True, True, False))
        self.assertEqual([r["path"] for r in self.local.requests], ["/api/tags"])
        self.local.tags = [EMBED]                                              # without the :latest suffix
        self.assertTrue(pb.embedding_preflight(self.local.base_url, EMBED)["embedding_model_installed"])

    def test_a_missing_embedding_model_is_refused_and_named(self) -> None:
        self.local.tags = ["something-else:latest"]
        with self.assertRaisesRegex(pc.PassAError, "not installed.*embed-test"):
            pb.embedding_preflight(self.local.base_url, EMBED)

    def test_a_server_that_is_not_ollama_is_a_recorded_skip_unless_the_check_is_required(self) -> None:
        facts = pb.embedding_preflight("http://127.0.0.1:9/v1", EMBED)
        self.assertEqual((facts["ollama"], facts["chat_model_checked"]), (False, False))
        self.assertIn("skipped", facts)
        with self.assertRaisesRegex(pc.PassAError, "does not answer"):
            pb.embedding_preflight("http://127.0.0.1:9/v1", EMBED, "require")
        with self.assertRaises(pc.PassAError):
            pb.embedding_preflight("http://127.0.0.1:9/v1", EMBED, "sometimes")

    def test_skip_asks_nothing(self) -> None:
        self.assertEqual(pb.embedding_preflight(self.local.base_url, "not-there", "skip"), {"mode": "skip"})
        self.assertEqual(self.local.requests, [])


if __name__ == "__main__":
    unittest.main()
