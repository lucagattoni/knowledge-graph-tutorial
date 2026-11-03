#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Local metering gateway: one place where every hosted model call of an experiment is counted and capped.

    uv run tools/metering_gateway.py --config CONFIG.toml [--port N] [--resume]
    uv run tools/metering_gateway.py --summary LOGFILE

A code under test is pointed at this gateway (`OPENAI_BASE_URL=http://127.0.0.1:PORT/v1`, or the Anthropic
equivalent) with a dummy key. The gateway holds the real key (read from its own environment, never from the config),
refuses a call that would take spend past the cap before forwarding anything, forwards the rest, and writes one JSONL
record per call from the provider's own usage fields.

Standard library only (threaded http.server and http.client). Binds 127.0.0.1 only. See tools/metering_gateway.md
for the config, the log record and what it does not do. It has been tested against fake upstreams only.
"""

from __future__ import annotations

import argparse
import decimal
import hashlib
import ipaddress
import json
import os
import re
import signal
import ssl
import stat
import sys
import threading
import time
import tomllib
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from http.client import HTTPConnection, HTTPException, HTTPSConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable, Mapping
from urllib.parse import urlsplit

__version__ = "1.2.0"

BIND_HOST = "127.0.0.1"
KEY_FILE_MAX_BYTES = 4096
# The field a per-model `output_limit_default` is written to, by the protocol of the model's upstream.
OUTPUT_LIMIT_FIELD = {"openai": "max_completion_tokens", "anthropic": "max_tokens"}
SUMMARY_PATH = "/_meter/summary"
MAX_BODY_BYTES = 32 * 1024 * 1024
MTOK = 1_000_000
ZERO = Decimal(0)
REDACTED = b"[redacted]"
DATE_RE = re.compile(r"^\d{8} \d{2}:\d{2}$")
ENV_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,63}$")
NAME_RE = re.compile(r"^[A-Za-z0-9._:/-]{1,100}$")
# Fields a request_defaults table may not set: they decide what is asked for, how much output is reserved, or how the
# reply comes back, and the reservation is computed from the client's own request.
PROTECTED_REQUEST_FIELDS = frozenset({"model", "messages", "input", "stream", "stream_options", "n",
                                      "max_tokens", "max_completion_tokens"})

# --------------------------------------------------------------------------- money
# Every sum and product runs in a context that raises instead of rounding, so a figure is exact or the call fails.
_EXACT = decimal.Context(
    prec=60,
    traps=[decimal.InvalidOperation, decimal.DivisionByZero, decimal.Overflow, decimal.Inexact, decimal.Rounded],
)


def exact():
    return decimal.localcontext(_EXACT)


def money_text(value: Decimal) -> str:
    """Plain decimal text without exponent or trailing zeros: Decimal('0.60') -> '0.6', 0 -> '0'."""
    with exact():
        return format(value.normalize(), "f")


def tokens_cost(tokens: int, per_mtok: Decimal) -> Decimal:
    with exact():
        return (Decimal(tokens) * per_mtok).scaleb(-6)


class ConfigError(Exception):
    """The gateway must not start (fail closed)."""


class HttpError(Exception):
    def __init__(self, status: int, code: str, message: str):
        super().__init__(message)
        self.status, self.code, self.message = status, code, message


# --------------------------------------------------------------------------- config


class Secret:
    """Holds the real key. Printing or logging one shows nothing; only `reveal()` returns the value."""

    __slots__ = ("_v",)

    def __init__(self, value: str):
        self._v = value

    def reveal(self) -> str:
        return self._v

    def __repr__(self) -> str:
        return "Secret(<redacted>)"

    __str__ = __repr__


@dataclass(frozen=True)
class Upstream:
    name: str
    protocol: str  # "openai" | "anthropic"
    base_url: str  # includes the version prefix, e.g. https://host/v1
    key_env: str  # the NAME of the environment variable
    dry_run: bool
    key: Secret | None
    allow_request_defaults: bool = False  # a model on this upstream may carry request_defaults although the upstream is paid
    key_file: str | None = None  # the path the key was read from, when it came from a file (never the key itself)


@dataclass(frozen=True)
class Price:
    input_per_mtok: Decimal
    output_per_mtok: Decimal
    cached_input_per_mtok: Decimal | None
    cache_write_per_mtok: Decimal | None
    source_url: str
    read_at: str


@dataclass(frozen=True)
class Model:
    name: str
    upstream: str
    price: Price
    request_defaults: Mapping[str, Any] = field(default_factory=dict)  # fields added to a request that lacks them
    output_limit_default: int | None = None  # written as the provider's own output-limit field when the client sent none
    translate_max_tokens: bool = False  # chat requests only: drop a null max_tokens, rename a set one to max_completion_tokens


@dataclass(frozen=True)
class Config:
    currency: str
    cap: Decimal
    default_max_output_tokens: int
    input_bytes_per_token: int
    upstream_timeout_s: float
    port: int
    log_file: str
    log_bodies: bool
    body_log_file: str | None
    upstreams: Mapping[str, Upstream]
    models: Mapping[str, Model]
    config_sha256: str


def _section(data: Mapping[str, Any], key: str, where: str) -> Mapping[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ConfigError(f"{where}: missing table [{key}]")
    return value


def _only(table: Mapping[str, Any], allowed: set[str], where: str) -> None:
    extra = sorted(set(table) - allowed)
    if extra:
        raise ConfigError(f"{where}: unknown key(s) {', '.join(extra)} (a typo would otherwise be ignored silently)")


def _decimal(value: Any, where: str, *, positive: bool = False) -> Decimal:
    if isinstance(value, bool):
        raise ConfigError(f"{where}: must be a number")
    try:
        number = Decimal(value) if isinstance(value, (int, str)) else value
        if not isinstance(number, Decimal):
            raise ValueError
        if not number.is_finite():
            raise ValueError
    except (ValueError, decimal.InvalidOperation):
        raise ConfigError(f"{where}: must be a finite decimal number") from None
    if number < 0 or (positive and number == 0):
        raise ConfigError(f"{where}: must be {'greater than' if positive else 'at least'} zero")
    if len(number.as_tuple().digits) > 18:
        raise ConfigError(f"{where}: more than 18 digits")
    return number


def _positive_int(value: Any, where: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ConfigError(f"{where}: must be a whole number of at least 1")
    return value


def _string(table: Mapping[str, Any], key: str, where: str) -> str:
    value = table.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{where}: {key} is required and must be a non-empty string")
    return value


def check_key_shape(upstream: str, value: str) -> None:
    """Reject a key that is empty, holds whitespace/control characters, or is one key pasted twice. Never prints it."""
    if not value:
        raise ConfigError(f"upstream {upstream}: the key variable is set but empty")
    if any(ord(c) < 33 or ord(c) > 126 for c in value):
        raise ConfigError(
            f"upstream {upstream}: the key holds whitespace, control or non-ASCII characters "
            "(two keys pasted together? a trailing newline?)"
        )
    half = len(value) // 2
    if len(value) % 2 == 0 and value[:half] == value[half:]:
        raise ConfigError(f"upstream {upstream}: the key looks like one key pasted twice")


TOKEN_LIKE_RE = re.compile(r"^[A-Za-z0-9_-]{20,}$")


def read_key_file(upstream: str, path: str) -> str:
    """The key held in `path`, for an upstream that names a key_file. Fails closed; no message holds key text.

    The file must be a regular file that group and others can neither read nor write (mode 0o600 or stricter), at most
    4 KiB, and hold one non-empty line. The newline after the key is not part of it; blank lines are ignored.
    """
    where = f"[upstreams.{upstream}]: key_file \"{path}\""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_CLOEXEC", 0))  # O_NONBLOCK: a FIFO cannot hang the start
    except FileNotFoundError:
        raise ConfigError(f"{where} does not exist") from None
    except IsADirectoryError:
        raise ConfigError(f"{where} is not a regular file") from None
    except (OSError, ValueError) as exc:
        raise ConfigError(f"{where} cannot be opened ({type(exc).__name__})") from None
    try:  # the checks run on the open file, so the file cannot change between the check and the read
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise ConfigError(f"{where} is not a regular file")
        if info.st_mode & 0o077:
            raise ConfigError(f"{where} can be read or written by group or others (mode {info.st_mode & 0o777:04o}); "
                              "make it 600 (chmod 600) and check that no copy of the key exists elsewhere")
        chunks, room = [], KEY_FILE_MAX_BYTES + 1
        while room > 0:
            chunk = os.read(fd, room)
            if not chunk:
                break
            chunks.append(chunk)
            room -= len(chunk)
        data = b"".join(chunks)
    except OSError as exc:
        raise ConfigError(f"{where} cannot be read ({type(exc).__name__})") from None
    finally:
        os.close(fd)
    if len(data) > KEY_FILE_MAX_BYTES:
        raise ConfigError(f"{where} is larger than {KEY_FILE_MAX_BYTES} bytes; it should hold one key")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise ConfigError(f"{where} is not text") from None
    lines = [line for line in text.split("\n") if line]  # empty pieces: the newline after the key, and any blank line
    if not lines:
        raise ConfigError(f"{where} is empty")
    if len(lines) > 1:
        raise ConfigError(f"{where} holds more than one non-empty line (two keys pasted together?)")
    return lines[0]


def _is_loopback_host(host: str | None) -> bool:
    if host is None:
        return False
    return host == "localhost" or is_loopback(host)


def parse_config(text: str, environ: Mapping[str, str]) -> Config:
    """Parse and validate a config; raise ConfigError on anything missing. Reads keys from `environ` only."""
    try:
        data = tomllib.loads(text, parse_float=Decimal)
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"config is not valid TOML: {exc}") from None
    _only(data, {"gateway", "upstreams", "models"}, "config")

    gw = _section(data, "gateway", "config")
    _only(gw, {"currency", "cap", "default_max_output_tokens", "input_bytes_per_token", "upstream_timeout_s",
               "port", "log_file", "log_bodies", "body_log_file"}, "[gateway]")
    if "cap" not in gw:
        raise ConfigError("[gateway]: cap is required (no cap, no start)")
    cap = _decimal(gw["cap"], "[gateway] cap", positive=True)
    currency = _string(gw, "currency", "[gateway]")
    default_max = _positive_int(gw.get("default_max_output_tokens", 1024), "[gateway] default_max_output_tokens")
    bytes_per_token = _positive_int(gw.get("input_bytes_per_token", 2), "[gateway] input_bytes_per_token")
    timeout = float(_decimal(gw.get("upstream_timeout_s", 120), "[gateway] upstream_timeout_s", positive=True))
    port = gw.get("port", 8089)
    if isinstance(port, bool) or not isinstance(port, int) or not 0 <= port <= 65535:
        raise ConfigError("[gateway] port: must be 0..65535")
    log_file = _string(gw, "log_file", "[gateway]")
    log_bodies = gw.get("log_bodies", False)
    if not isinstance(log_bodies, bool):
        raise ConfigError("[gateway] log_bodies: must be true or false")
    body_log = None
    if log_bodies:
        body_log = gw.get("body_log_file", log_file + ".bodies.jsonl")
        if not isinstance(body_log, str) or not body_log or body_log == log_file:
            raise ConfigError("[gateway] body_log_file: must be a path different from log_file")

    upstreams: dict[str, Upstream] = {}
    for name, table in _section(data, "upstreams", "config").items():
        where = f"[upstreams.{name}]"
        if not NAME_RE.match(name) or not isinstance(table, dict):
            raise ConfigError(f"{where}: bad name or not a table")
        _only(table, {"protocol", "base_url", "key_env", "key_file", "dry_run", "allow_request_defaults"}, where)
        protocol = _string(table, "protocol", where)
        if protocol not in ("openai", "anthropic"):
            raise ConfigError(f"{where}: protocol must be \"openai\" or \"anthropic\"")
        base_url = _string(table, "base_url", where).rstrip("/")
        parts = urlsplit(base_url)
        if parts.scheme not in ("http", "https") or not parts.hostname or parts.query or parts.fragment:
            raise ConfigError(f"{where}: base_url must be an http(s) URL without query or fragment")
        if parts.scheme == "http" and not _is_loopback_host(parts.hostname):
            raise ConfigError(f"{where}: plain http is allowed only to a loopback host (the real key would travel in clear)")
        dry_run = table.get("dry_run", False)
        if not isinstance(dry_run, bool):
            raise ConfigError(f"{where}: dry_run must be true or false")
        allow_defaults = table.get("allow_request_defaults", False)
        if not isinstance(allow_defaults, bool):
            raise ConfigError(f"{where}: allow_request_defaults must be true or false")
        key_env = table.get("key_env", "")
        key_file = table.get("key_file")
        key: Secret | None = None
        if key_file is not None:
            if dry_run:
                raise ConfigError(f"{where}: key_file is allowed only when dry_run is false (a dry_run upstream sends no key)")
            if "key_env" in table:
                raise ConfigError(f"{where}: give key_env or key_file, not both")
            if not isinstance(key_file, str) or not key_file.strip():
                raise ConfigError(f"{where}: key_file must be the path of a file that holds the key")
            if TOKEN_LIKE_RE.match(key_file) or any(value == key_file for value in environ.values()):
                raise ConfigError(f"{where}: key_file looks like a key, not a path (not shown); give the path of a file, "
                                  "for example ./name")
            key = Secret(read_key_file(name, key_file))
            check_key_shape(name, key.reveal())
        else:
            if not dry_run or key_env:
                if not isinstance(key_env, str) or not ENV_NAME_RE.match(key_env):
                    raise ConfigError(f"{where}: key_env must be the NAME of an environment variable "
                                      "(a paid upstream needs key_env or key_file)")
                if any(value == key_env for value in environ.values()):
                    raise ConfigError(f"{where}: key_env holds a secret value, not a variable name; put the key in the environment")
            if not dry_run:
                value = environ.get(key_env)
                if value is None:
                    raise ConfigError(f"{where}: the environment variable named by key_env is not set (and dry_run is not true)")
                check_key_shape(name, value)
                key = Secret(value)
        upstreams[name] = Upstream(name, protocol, base_url, key_env if isinstance(key_env, str) else "", dry_run, key,
                                   allow_defaults, key_file if isinstance(key_file, str) else None)
    if not upstreams:
        raise ConfigError("config: no upstream configured")

    models: dict[str, Model] = {}
    for name, table in _section(data, "models", "config").items():
        where = f"[models.{name}]"
        if not NAME_RE.match(name) or not isinstance(table, dict):
            raise ConfigError(f"{where}: bad name or not a table")
        _only(table, {"upstream", "input_per_mtok", "output_per_mtok", "cached_input_per_mtok",
                      "cache_write_per_mtok", "source_url", "read_at", "request_defaults", "output_limit_default",
                      "translate_max_tokens"}, where)
        upstream = _string(table, "upstream", where)
        if upstream not in upstreams:
            raise ConfigError(f"{where}: upstream {upstream!r} is not configured")
        defaults = table.get("request_defaults", {})
        if not isinstance(defaults, dict):
            raise ConfigError(f"{where}: request_defaults must be a table")
        if defaults and not upstreams[upstream].dry_run and not upstreams[upstream].allow_request_defaults:
            raise ConfigError(f"{where}: request_defaults is allowed only on a dry_run upstream, or on an upstream whose "
                              f"[upstreams.{upstream}] table sets allow_request_defaults = true (a field added to a paid "
                              "call can change what it costs)")
        protected = sorted(set(defaults) & PROTECTED_REQUEST_FIELDS)
        if protected:
            raise ConfigError(f"{where}: request_defaults may not set {protected}")
        try:
            json.dumps(defaults)
        except (TypeError, ValueError):
            raise ConfigError(f"{where}: request_defaults must hold only JSON values") from None
        for required in ("input_per_mtok", "output_per_mtok"):
            if required not in table:
                raise ConfigError(f"{where}: {required} is required (a model with no price is refused)")
        source_url = _string(table, "source_url", where)
        if not re.match(r"^https?://\S+$", source_url):
            raise ConfigError(f"{where}: source_url must be an http(s) URL")
        read_at = _string(table, "read_at", where)
        if not DATE_RE.match(read_at):
            raise ConfigError(f"{where}: read_at must be UTC like \"20261102 10:00\"")
        output_limit = _positive_int(table["output_limit_default"], f"{where} output_limit_default") \
            if "output_limit_default" in table else None
        translate = table.get("translate_max_tokens", False)
        if not isinstance(translate, bool):
            raise ConfigError(f"{where}: translate_max_tokens must be true or false")
        if translate and upstreams[upstream].protocol != "openai":
            raise ConfigError(f"{where}: translate_max_tokens applies to an upstream that speaks the openai protocol "
                              "(an anthropic upstream takes max_tokens as it is)")
        if translate and not upstreams[upstream].dry_run and not upstreams[upstream].allow_request_defaults:
            raise ConfigError(f"{where}: translate_max_tokens is allowed only on a dry_run upstream, or on an upstream whose "
                              f"[upstreams.{upstream}] table sets allow_request_defaults = true (it changes a paid request)")
        optional = {k: (_decimal(table[k], f"{where} {k}") if k in table else None)
                    for k in ("cached_input_per_mtok", "cache_write_per_mtok")}
        price = Price(
            _decimal(table["input_per_mtok"], f"{where} input_per_mtok"),
            _decimal(table["output_per_mtok"], f"{where} output_per_mtok"),
            optional["cached_input_per_mtok"], optional["cache_write_per_mtok"], source_url, read_at,
        )
        models[name] = Model(name, upstream, price, defaults, output_limit, translate)
    if not models:
        raise ConfigError("config: no model priced (no prices, no start)")

    return Config(currency, cap, default_max, bytes_per_token, timeout, port, log_file, log_bodies, body_log,
                  upstreams, models, hashlib.sha256(text.encode("utf-8")).hexdigest())


def load_config(path: str | Path, environ: Mapping[str, str]) -> Config:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigError(f"cannot read config: {type(exc).__name__}") from None
    return parse_config(text, environ)


# --------------------------------------------------------------------------- peers


def is_loopback(host: str) -> bool:
    """True only for a loopback address; anything unparsable is refused."""
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return ip.is_loopback


def host_allowed(value: str | None) -> bool:
    """The Host header must name this machine, so a web page cannot reach the gateway through a rebound name."""
    if not value:
        return False
    host = value.strip().lower()
    host = host[1:].split("]", 1)[0] if host.startswith("[") else host.split(":", 1)[0]
    return _is_loopback_host(host)


# --------------------------------------------------------------------------- usage


@dataclass(frozen=True)
class Usage:
    input_tokens: int  # all prompt tokens, cached and cache-written included
    output_tokens: int
    cached_input_tokens: int | None  # None: the provider gave no figure
    cache_creation_input_tokens: int | None


def _int(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def openai_usage(usage: Any, kind: str) -> Usage | None:
    """Usage from an OpenAI-style `usage` object; None when it is absent or unusable."""
    if not isinstance(usage, dict):
        return None
    prompt = _int(usage.get("prompt_tokens"))
    if prompt is None:
        return None
    completion = 0 if kind == "embeddings" else _int(usage.get("completion_tokens"))
    if completion is None:
        return None
    cached = None
    details = usage.get("prompt_tokens_details")
    if isinstance(details, dict):
        cached = _int(details.get("cached_tokens"))
    if cached is not None and cached > prompt:
        return None
    return Usage(prompt, completion, cached, None)


def anthropic_usage(usage: Any) -> Usage | None:
    """Usage from an Anthropic-style `usage` object. Total input = input + cache read + cache creation."""
    if not isinstance(usage, dict):
        return None
    plain, out = _int(usage.get("input_tokens")), _int(usage.get("output_tokens"))
    if plain is None or out is None:
        return None
    read, write = _int(usage.get("cache_read_input_tokens")), _int(usage.get("cache_creation_input_tokens"))
    return Usage(plain + (read or 0) + (write or 0), out, read, write)


def cost_of(usage: Usage, price: Price) -> Decimal:
    cached = usage.cached_input_tokens or 0
    written = usage.cache_creation_input_tokens or 0
    plain = usage.input_tokens - cached - written
    cached_price = price.cached_input_per_mtok if price.cached_input_per_mtok is not None else price.input_per_mtok
    write_price = price.cache_write_per_mtok if price.cache_write_per_mtok is not None else price.input_per_mtok
    with exact():
        return (tokens_cost(plain, price.input_per_mtok) + tokens_cost(cached, cached_price)
                + tokens_cost(written, write_price) + tokens_cost(usage.output_tokens, price.output_per_mtok))


def usage_from_body(protocol: str, kind: str, obj: Any) -> tuple[Usage | None, str | None]:
    """(usage, model as reported) from a non-streamed JSON response."""
    if not isinstance(obj, dict):
        return None, None
    model = obj.get("model") if isinstance(obj.get("model"), str) else None
    if protocol == "anthropic":
        return anthropic_usage(obj.get("usage")), model
    return openai_usage(obj.get("usage"), kind), model


class SseUsage:
    """Incremental reader of an SSE stream that keeps only the usage and the model name."""

    def __init__(self, protocol: str, kind: str):
        self.protocol, self.kind = protocol, kind
        self._tail = b""
        self.model: str | None = None
        self._openai_usage: Any = None
        self._anthropic: dict[str, int] = {}
        self._saw_delta = False

    def feed(self, chunk: bytes) -> None:
        lines = (self._tail + chunk).split(b"\n")
        self._tail = lines.pop()
        if len(self._tail) > MAX_BODY_BYTES:
            self._tail = b""
        for line in lines:
            self._line(line.rstrip(b"\r"))

    def _line(self, line: bytes) -> None:
        if not line.startswith(b"data:"):
            return
        payload = line[5:].strip()
        if not payload or payload == b"[DONE]":
            return
        try:
            obj = json.loads(payload)
        except ValueError:
            return
        if not isinstance(obj, dict):
            return
        if self.protocol == "openai":
            if isinstance(obj.get("model"), str):
                self.model = obj["model"]
            if isinstance(obj.get("usage"), dict):
                self._openai_usage = obj["usage"]
            return
        kind = obj.get("type")
        if kind == "message_start" and isinstance(obj.get("message"), dict):
            message = obj["message"]
            if isinstance(message.get("model"), str):
                self.model = message["model"]
            self._merge(message.get("usage"))
        elif kind == "message_delta":
            self._saw_delta = True
            self._merge(obj.get("usage"))

    def _merge(self, usage: Any) -> None:
        # The token counts in message_delta are cumulative, so the latest value for a key wins.
        if isinstance(usage, dict):
            for key, value in usage.items():
                if _int(value) is not None:
                    self._anthropic[key] = value

    def result(self) -> Usage | None:
        if self.protocol == "openai":
            return openai_usage(self._openai_usage, self.kind)
        return anthropic_usage(self._anthropic) if self._saw_delta else None


# --------------------------------------------------------------------------- ledger and totals


class Ledger:
    """Spend plus open reservations against a cap, under one lock."""

    def __init__(self, cap: Decimal, spent: Decimal = ZERO):
        self.cap = cap
        self.lock = threading.RLock()
        self.spent = spent
        self.open = ZERO
        self.peak = spent  # highest spent + open ever held; a test checks it never passed the cap

    def _committed(self) -> Decimal:
        return self.spent + self.open

    def try_reserve(self, amount: Decimal) -> bool:
        with self.lock, exact():
            if self._committed() + amount > self.cap:
                return False
            self.open += amount
            self.peak = max(self.peak, self.spent + self.open)
            return True

    def settle(self, reserved: Decimal, cost: Decimal) -> None:
        with self.lock, exact():
            self.open -= reserved
            self.spent += cost

    def remaining(self) -> Decimal:
        with self.lock, exact():
            return self.cap - self._committed()


class Totals:
    """Running totals over call records; used live and by `--summary`, so the two cannot disagree."""

    def __init__(self):
        self.requests = self.calls = self.voided = self.refused = self.usage_missing = 0
        self.input_tokens = self.output_tokens = self.cached_input_tokens = 0
        self.spent = ZERO
        self.by_model: dict[str, dict[str, Any]] = {}

    def add(self, rec: Mapping[str, Any]) -> None:
        self.requests += 1
        if rec.get("refusal") is not None:
            self.refused += 1
            return
        self.calls += 1
        self.voided += bool(rec["voided"])
        self.usage_missing += bool(rec["usage_missing"])
        for key, attr in (("input_tokens", "input_tokens"), ("output_tokens", "output_tokens"),
                          ("cached_input_tokens", "cached_input_tokens")):
            if rec.get(key) is not None:
                setattr(self, attr, getattr(self, attr) + rec[key])
        with exact():
            cost = Decimal(rec["cost"])
            self.spent += cost
            entry = self.by_model.setdefault(str(rec.get("model_requested")), {
                "calls": 0, "voided": 0, "usage_missing": 0, "input_tokens": 0, "output_tokens": 0, "spent": ZERO})
            entry["calls"] += 1
            entry["voided"] += bool(rec["voided"])
            entry["usage_missing"] += bool(rec["usage_missing"])
            entry["input_tokens"] += rec.get("input_tokens") or 0
            entry["output_tokens"] += rec.get("output_tokens") or 0
            entry["spent"] += cost

    def as_dict(self, cap: Decimal | None, currency: str | None, open_reservations: Decimal = ZERO) -> dict[str, Any]:
        with exact():
            remaining = None if cap is None else cap - self.spent - open_reservations
        return {
            "currency": currency,
            "cap": None if cap is None else money_text(cap),
            "spent": money_text(self.spent),
            "open_reservations": money_text(open_reservations),
            "remaining": None if remaining is None else money_text(remaining),
            "requests": self.requests,
            "calls": self.calls,
            "ok": self.calls - self.voided - self.usage_missing,
            "voided": self.voided,
            "usage_missing": self.usage_missing,
            "refused": self.refused,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cached_input_tokens": self.cached_input_tokens,
            "by_model": {m: dict(e, spent=money_text(e["spent"])) for m, e in sorted(self.by_model.items())},
        }


def read_log(path: str | Path) -> list[dict[str, Any]]:
    records = []
    with open(path, encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except ValueError:
                raise ConfigError(f"{path}: line {number} is not valid JSON") from None
    return records


# --------------------------------------------------------------------------- the gateway


class JsonlWriter:
    def __init__(self, path: str):
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        self._file = os.fdopen(fd, "a", encoding="utf-8")

    def write(self, obj: Mapping[str, Any]) -> None:
        self._file.write(json.dumps(obj, separators=(",", ":")) + "\n")
        self._file.flush()

    def close(self) -> None:
        self._file.close()


@dataclass(frozen=True)
class Route:
    kind: str  # "chat" | "embeddings" | "messages"
    protocol: str
    suffix: str  # appended to the upstream base_url


ROUTES = {
    "/v1/chat/completions": Route("chat", "openai", "/chat/completions"),
    "/v1/embeddings": Route("embeddings", "openai", "/embeddings"),
    "/v1/messages": Route("messages", "anthropic", "/messages"),
}

DROP_REQUEST_HEADERS = {
    "authorization", "x-api-key", "proxy-authorization", "cookie", "host", "content-length", "connection",
    "keep-alive", "transfer-encoding", "te", "upgrade", "accept-encoding", "expect", "trailer",
}
DROP_RESPONSE_HEADERS = {
    "connection", "keep-alive", "transfer-encoding", "content-length", "set-cookie", "trailer", "upgrade",
    "proxy-authenticate", "te", "server", "date",
}
JSON_TYPE = [("Content-Type", "application/json")]


def utc_stamp(now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"


def error_body(protocol: str, code: str, message: str) -> bytes:
    if protocol == "anthropic":
        obj = {"type": "error", "error": {"type": code, "message": message}}
    else:
        obj = {"error": {"message": message, "type": code, "code": code}}
    return json.dumps(obj).encode("utf-8")


def max_output_tokens(route: Route, request: Mapping[str, Any], default: int) -> int:
    """The most output tokens the request can ask for (n choices multiply it)."""
    if route.kind == "embeddings":
        return 0
    names = ("max_completion_tokens", "max_tokens") if route.kind == "chat" else ("max_tokens",)
    found = []
    for name in names:
        value = request.get(name)
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise HttpError(400, "gateway_bad_request", f"{name} must be a positive integer")
        found.append(value)
    limit = max(found) if found else default
    if route.kind == "chat":
        n = request.get("n", 1)
        if n is None:
            n = 1
        if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= 128:
            raise HttpError(400, "gateway_bad_request", "n must be a whole number from 1 to 128")
        limit *= n
    return limit


def translate_max_tokens(request: dict[str, Any]) -> list[str]:
    """For a model with `translate_max_tokens`, on a chat request: a null `max_tokens` is dropped (a null limit counts as not
    sent, and the provider rejects the null itself), and a set one is renamed `max_completion_tokens` (the field a reasoning
    model takes). Returns the names for the log. Both limits set at once is refused: the gateway will not choose between them."""
    if "max_tokens" not in request:
        return []
    if request["max_tokens"] is None:
        del request["max_tokens"]
        return ["max_tokens(null)-dropped"]
    if request.get("max_completion_tokens") is not None:
        raise HttpError(400, "gateway_bad_request",
                        "both max_tokens and max_completion_tokens are set, and this model translates max_tokens; send one")
    request["max_completion_tokens"] = request.pop("max_tokens")
    return ["max_tokens->max_completion_tokens"]


def output_limit_field(route: Route, upstream: Upstream, model: Model, request: Mapping[str, Any]) -> str | None:
    """The field a model's `output_limit_default` goes into for this request, or None when nothing is to be injected.

    Only a chat-style route takes it (embeddings have no output). A client's own limit on either field wins, whatever
    its value; a `null` counts as not sent.
    """
    if route.kind == "embeddings" or model.output_limit_default is None:
        return None
    if request.get("max_tokens") is not None or request.get("max_completion_tokens") is not None:
        return None
    return OUTPUT_LIMIT_FIELD[upstream.protocol]


def reserve_amount(price: Price, body_bytes: int, bytes_per_token: int, max_output: int) -> Decimal:
    """Upper bound on what a call can cost: every input byte pessimistically costs 1/bytes_per_token of a token."""
    input_tokens = -(-body_bytes // bytes_per_token)
    prices = [price.input_per_mtok]
    if price.cache_write_per_mtok is not None:
        prices.append(price.cache_write_per_mtok)
    with exact():
        return tokens_cost(input_tokens, max(prices)) + tokens_cost(max_output, price.output_per_mtok)


class Redactor:
    """Removes the real key (raw and JSON-escaped) from anything that leaves the gateway."""

    def __init__(self, secrets: list[str]):
        needles = set()
        for secret in secrets:
            needles.add(secret.encode("utf-8"))
            needles.add(json.dumps(secret)[1:-1].encode("utf-8"))
        self._needles = sorted(needles, key=len, reverse=True)

    def __call__(self, data: bytes) -> bytes:
        for needle in self._needles:
            if needle in data:
                data = data.replace(needle, REDACTED)
        return data

    def text(self, value: str) -> str:
        return self(value.encode("utf-8")).decode("utf-8")


@dataclass
class Call:
    call_id: str
    started: float
    ts: str
    route: str
    upstream: str | None = None
    model_requested: str | None = None
    model_reported: str | None = None
    http_status: int | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    cached_input_tokens: int | None = None
    cache_creation_input_tokens: int | None = None
    cost: Decimal = ZERO
    reserve: Decimal | None = None
    voided: bool = False
    usage_missing: bool = False
    streamed: bool = False
    reserve_exceeded: bool = False
    refusal: str | None = None
    error: str | None = None
    latency_ms: int = 0
    request_sha256: str | None = None
    bytes_in: int = 0
    bytes_out: int = 0
    held: bool = False
    forwarded: bool = False
    done: bool = False
    request_body: bytes = b""
    response_body: bytes = b""
    defaults_applied: list = field(default_factory=list)

    def record(self, currency: str) -> dict[str, Any]:
        return {
            "ts": self.ts, "call_id": self.call_id, "route": self.route, "upstream": self.upstream,
            "model_requested": (self.model_requested or "")[:200] or None, "model_reported": self.model_reported,
            "http_status": self.http_status, "input_tokens": self.input_tokens, "output_tokens": self.output_tokens,
            "cached_input_tokens": self.cached_input_tokens, "cost": money_text(self.cost), "currency": currency,
            "reserve": None if self.reserve is None else money_text(self.reserve), "voided": self.voided,
            "usage_missing": self.usage_missing, "streamed": self.streamed, "latency_ms": self.latency_ms,
            "request_sha256": self.request_sha256, "bytes_in": self.bytes_in, "bytes_out": self.bytes_out,
            "refusal": self.refusal, "error": self.error, "reserve_exceeded": self.reserve_exceeded,
            "cache_creation_input_tokens": self.cache_creation_input_tokens,
            "request_defaults_applied": list(self.defaults_applied),
        }


class Gateway:
    def __init__(self, config: Config, *, resume: bool = False):
        self.cfg = config
        self.broken = False
        secrets = [u.key.reveal() for u in config.upstreams.values() if u.key is not None]
        self.redact = Redactor(secrets)
        self._ssl = ssl.create_default_context()
        self.totals = Totals()
        spent = ZERO
        log_path = Path(config.log_file)
        if log_path.exists() and log_path.stat().st_size > 0:
            if not resume:
                raise ConfigError("the log file already holds records; use --resume to continue its run or choose a new log_file")
            for rec in read_log(log_path):
                self.totals.add(rec)
            spent = self.totals.spent
        elif resume:
            raise ConfigError("--resume given but the log file is missing or empty")
        self.ledger = Ledger(config.cap, spent)
        self.log = JsonlWriter(config.log_file)
        self.body_log = JsonlWriter(config.body_log_file) if config.body_log_file else None
        try:
            self.manifest_path = self._write_manifest()
        except BaseException:
            self.close()
            raise

    # -- startup record of where the numbers came from

    def _write_manifest(self) -> str:
        cfg = self.cfg
        manifest = {
            "version": __version__,
            "started_at": utc_stamp(),
            "config_sha256": cfg.config_sha256,
            "currency": cfg.currency,
            "cap": money_text(cfg.cap),
            "spent_at_start": money_text(self.ledger.spent),
            "default_max_output_tokens": cfg.default_max_output_tokens,
            "input_bytes_per_token": cfg.input_bytes_per_token,
            "upstreams": {n: {"protocol": u.protocol, "base_url": u.base_url, "key_env": u.key_env, "dry_run": u.dry_run,
                              "allow_request_defaults": u.allow_request_defaults,
                              **({"key_file": u.key_file} if u.key_file is not None else {})}  # the path, never the key
                          for n, u in cfg.upstreams.items()},
            "models": {n: {"upstream": m.upstream, "source_url": m.price.source_url, "read_at": m.price.read_at,
                           "request_defaults": dict(m.request_defaults),
                           "output_limit_default": m.output_limit_default,
                           "translate_max_tokens": m.translate_max_tokens,
                           "input_per_mtok": money_text(m.price.input_per_mtok),
                           "output_per_mtok": money_text(m.price.output_per_mtok),
                           "cached_input_per_mtok": None if m.price.cached_input_per_mtok is None
                           else money_text(m.price.cached_input_per_mtok),
                           "cache_write_per_mtok": None if m.price.cache_write_per_mtok is None
                           else money_text(m.price.cache_write_per_mtok)}
                       for n, m in cfg.models.items()},
        }
        path = f"{cfg.log_file}.manifest-{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')}.json"
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            raise ConfigError("a manifest with this timestamp already exists; start again") from None
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=2)
            handle.write("\n")
        return path

    def close(self) -> None:
        self.log.close()
        if self.body_log:
            self.body_log.close()

    def summary(self) -> dict[str, Any]:
        with self.ledger.lock:
            return self.totals.as_dict(self.cfg.cap, self.cfg.currency, self.ledger.open)

    # -- one request

    def process(self, peer: str, method: str, target: str, headers: Mapping[str, str],
                read_body: Callable[[], bytes], out: Any) -> None:
        if not is_loopback(peer):
            out.send_reply(403, JSON_TYPE, error_body("openai", "gateway_forbidden_peer", "loopback clients only"))
            return
        lowered = {k.lower(): v for k, v in headers.items()}
        if not host_allowed(lowered.get("host")):
            out.send_reply(403, JSON_TYPE, error_body("openai", "gateway_forbidden_host", "the Host header must be loopback"))
            return
        path, _, query = target.partition("?")
        if method == "GET" and path == SUMMARY_PATH:
            out.send_reply(200, JSON_TYPE, json.dumps(self.summary(), indent=2).encode("utf-8"))
            return
        route = ROUTES.get(path)
        if method != "POST" or route is None:
            out.send_reply(404, JSON_TYPE, error_body("openai", "gateway_not_found", "unknown route"))
            return
        call = Call(uuid.uuid4().hex, time.monotonic(), utc_stamp(), path)
        try:
            self._api_call(call, route, query, headers, read_body, out)
        except Exception as exc:  # noqa: BLE001 - every failure must settle the ledger
            self._internal_error(call, route, exc, out)

    def _api_call(self, call: Call, route: Route, query: str, headers: Mapping[str, str],
                  read_body: Callable[[], bytes], out: Any) -> None:
        refuse = lambda status, code, message: self._refuse(call, route, status, code, message, out)  # noqa: E731
        if self.broken:
            return refuse(503, "gateway_log_failure", "the log cannot be written; the gateway stopped accepting calls")
        media = next((v for k, v in headers.items() if k.lower() == "content-type"), "").split(";")[0].strip().lower()
        if media != "application/json":  # a web page can send text/plain across origins without a preflight
            return refuse(415, "gateway_unsupported_media_type", "send Content-Type: application/json")
        try:
            body = read_body()
        except HttpError as exc:
            return refuse(exc.status, exc.code, exc.message)
        call.request_body, call.bytes_in = body, len(body)
        call.request_sha256 = hashlib.sha256(body).hexdigest()
        try:
            request = json.loads(body)
        except (ValueError, RecursionError):
            return refuse(400, "gateway_bad_request", "the body is not valid JSON")
        if not isinstance(request, dict):
            return refuse(400, "gateway_bad_request", "the body must be a JSON object")
        name = request.get("model")
        call.model_requested = name if isinstance(name, str) else None
        model = self.cfg.models.get(name) if isinstance(name, str) else None
        if model is None:
            return refuse(400, "gateway_model_not_priced", "this model has no price in the gateway config")
        upstream = self.cfg.upstreams[model.upstream]
        call.upstream = upstream.name
        if upstream.protocol != route.protocol:
            return refuse(400, "gateway_route_mismatch", "this model's upstream speaks a different protocol than this route")
        forward_body = body
        # What the gateway adds is decided from the client's request, then written in one go: first the model's output
        # limit (so the reservation below is made from it), then its request_defaults. A field the client sent wins.
        translated: list[str] = []
        if route.kind == "chat" and model.translate_max_tokens:
            try:
                translated = translate_max_tokens(request)  # first, so the client's own limit still wins and is what is reserved
            except HttpError as exc:
                return refuse(exc.status, exc.code, exc.message)
        limit_field = output_limit_field(route, upstream, model, request)
        if limit_field is not None:
            request[limit_field] = model.output_limit_default
        added = [k for k in model.request_defaults if k not in request]
        request.update({k: model.request_defaults[k] for k in added})
        if limit_field is not None or added or translated:
            forward_body = json.dumps(request).encode("utf-8")  # one re-serialisation for all of it
        try:
            max_out = max_output_tokens(route, request, self.cfg.default_max_output_tokens)
        except HttpError as exc:
            return refuse(exc.status, exc.code, exc.message)
        call.defaults_applied = translated + added + ([limit_field] if limit_field is not None else [])
        stream = request.get("stream") is True
        if stream and route.kind == "chat":
            options = request.get("stream_options")
            if options is None or (isinstance(options, dict) and "include_usage" not in options):
                request["stream_options"] = {**(options or {}), "include_usage": True}
                forward_body = json.dumps(request).encode("utf-8")

        call.reserve = reserve_amount(model.price, len(forward_body), self.cfg.input_bytes_per_token, max_out)
        if not self.ledger.try_reserve(call.reserve):
            return refuse(429, "gateway_budget_exceeded",
                          f"this call could cost up to {money_text(call.reserve)} {self.cfg.currency}; "
                          f"{money_text(self.ledger.remaining())} remain under the cap. Nothing was forwarded.")
        call.held = True
        self._forward(call, route, model, upstream, query, headers, forward_body, stream, out)

    # -- refusals and errors

    def _refuse(self, call: Call, route: Route, status: int, code: str, message: str, out: Any) -> None:
        call.refusal, call.http_status = code, status
        body = error_body(route.protocol, code, message)
        call.bytes_out = len(body)
        self._complete(call)
        out.send_reply(status, JSON_TYPE, body)

    def _internal_error(self, call: Call, route: Route, exc: Exception, out: Any) -> None:
        if call.done:
            return
        call.error = f"internal_error:{type(exc).__name__}"
        if call.forwarded:  # the provider may have billed this call: count the whole reservation
            call.usage_missing, call.cost = True, call.reserve or ZERO
        else:
            call.refusal = "gateway_internal_error"
        call.http_status = 500
        body = error_body(route.protocol, "gateway_internal_error", "internal error")
        call.bytes_out = len(body)
        self._complete(call)
        if not getattr(out, "head_sent", False):
            try:
                out.send_reply(500, JSON_TYPE, body)
            except OSError:
                pass

    def _complete(self, call: Call) -> None:
        """Settle the ledger and write the record. Runs once per call, before the final reply bytes are sent."""
        if call.done:
            return
        call.done = True
        call.latency_ms = int((time.monotonic() - call.started) * 1000)
        record = call.record(self.cfg.currency)
        with self.ledger.lock:
            if call.held:
                self.ledger.settle(call.reserve or ZERO, call.cost)
            self.totals.add(record)
            try:
                self.log.write(record)
                if self.body_log is not None:
                    self.body_log.write({
                        "call_id": call.call_id,
                        "request": self.redact.text(call.request_body.decode("utf-8", "replace")),
                        "response": self.redact.text(call.response_body.decode("utf-8", "replace")),
                    })
            except OSError:
                self.broken = True

    # -- forwarding

    def _forward(self, call: Call, route: Route, model: Model, upstream: Upstream, query: str,
                 headers: Mapping[str, str], body: bytes, stream: bool, out: Any) -> None:
        sent = {k: v for k, v in headers.items() if k.lower() not in DROP_REQUEST_HEADERS}
        if not any(k.lower() == "content-type" for k in sent):
            sent["Content-Type"] = "application/json"
        sent["Connection"] = "close"
        if upstream.key is not None:
            if upstream.protocol == "anthropic":
                sent["x-api-key"] = upstream.key.reveal()
            else:
                sent["Authorization"] = "Bearer " + upstream.key.reveal()
        parts = urlsplit(upstream.base_url)
        path = parts.path.rstrip("/") + route.suffix + (("?" + query) if query else "")
        timeout = self.cfg.upstream_timeout_s
        call.forwarded = True
        try:
            if parts.scheme == "https":
                conn: HTTPConnection = HTTPSConnection(parts.hostname, parts.port or 443, timeout=timeout, context=self._ssl)
            else:
                conn = HTTPConnection(parts.hostname, parts.port or 80, timeout=timeout)
            try:
                conn.request("POST", path, body=body, headers=sent)
                response = conn.getresponse()
            except BaseException:
                conn.close()
                raise
        except (OSError, HTTPException) as exc:
            return self._void(call, route, out, exc, "connection failed or timed out before any response")
        try:
            self._handle_response(call, route, model, upstream, response, out)
        finally:
            conn.close()

    def _void(self, call: Call, route: Route, out: Any, exc: BaseException, why: str) -> None:
        timed_out = isinstance(exc, TimeoutError)
        call.voided = True
        call.error = "upstream_timeout" if timed_out else "upstream_connection_failed"
        status = 504 if timed_out else 502
        code = "gateway_upstream_timeout" if timed_out else "gateway_upstream_unreachable"
        self._reply_buffered(call, route, out, status, JSON_TYPE, error_body(route.protocol, code, why))

    def _reply_buffered(self, call: Call, route: Route, out: Any, status: int, headers: list[tuple[str, str]],
                        body: bytes) -> None:
        call.http_status, call.bytes_out, call.response_body = status, len(body), body
        self._complete(call)
        out.send_reply(status, headers, body)

    def _pass_headers(self, response: Any) -> list[tuple[str, str]]:
        kept = []
        for name, value in response.getheaders():
            if name.lower() not in DROP_RESPONSE_HEADERS:
                kept.append((name, self.redact.text(value)))
        return kept

    def _apply_usage(self, call: Call, model: Model, usage: Usage | None) -> None:
        if usage is None:
            call.usage_missing, call.cost = True, call.reserve or ZERO
            return
        call.input_tokens, call.output_tokens = usage.input_tokens, usage.output_tokens
        call.cached_input_tokens = usage.cached_input_tokens
        call.cache_creation_input_tokens = usage.cache_creation_input_tokens
        call.cost = cost_of(usage, model.price)
        call.reserve_exceeded = call.cost > (call.reserve or ZERO)

    def _handle_response(self, call: Call, route: Route, model: Model, upstream: Upstream,
                         response: Any, out: Any) -> None:
        status = response.status
        ok = 200 <= status < 300
        headers = self._pass_headers(response)
        if ok and "text/event-stream" in (response.getheader("Content-Type") or "").lower():
            return self._relay_stream(call, route, model, upstream, response, status, headers, out)
        try:
            data = response.read()
        except (OSError, HTTPException) as exc:
            if ok:  # the provider answered 2xx and may have billed; no usage reached us
                call.usage_missing, call.cost, call.error = True, call.reserve or ZERO, "upstream_body_incomplete"
                return self._reply_buffered(call, route, out, 502, JSON_TYPE, error_body(
                    route.protocol, "gateway_upstream_incomplete", "the upstream response was cut short"))
            return self._void(call, route, out, exc, "the upstream response was cut short")
        if not ok:
            call.voided, call.error = True, "upstream_status"
        else:
            try:
                obj = json.loads(data)
            except (ValueError, RecursionError):
                obj = None
            usage, reported = usage_from_body(upstream.protocol, route.kind, obj)
            call.model_reported = reported
            self._apply_usage(call, model, usage)
        self._reply_buffered(call, route, out, status, headers, self.redact(data))

    def _relay_stream(self, call: Call, route: Route, model: Model, upstream: Upstream, response: Any,
                      status: int, headers: list[tuple[str, str]], out: Any) -> None:
        call.streamed, call.http_status = True, status
        parser = SseUsage(upstream.protocol, route.kind)
        keep = bytearray() if self.body_log is not None else None
        client_alive = True
        try:
            out.send_stream_head(status, headers)
        except OSError:
            client_alive = False
        try:
            while True:
                chunk = response.read1(65536)
                if not chunk:
                    break
                parser.feed(chunk)
                if keep is not None:
                    keep += chunk
                if client_alive:
                    try:
                        out.send_chunk(chunk)
                        call.bytes_out += len(chunk)
                    except OSError:
                        client_alive = False  # keep reading: the provider still bills and still reports usage
        except (OSError, HTTPException):
            call.error = "stream_interrupted"
        call.model_reported = parser.model
        self._apply_usage(call, model, parser.result())
        if keep is not None:
            call.response_body = bytes(keep)
        self._complete(call)


# --------------------------------------------------------------------------- HTTP front end


def read_chunked(rfile: Any, limit: int) -> bytes:
    body = bytearray()
    while True:
        line = rfile.readline(65537)
        if not line:
            raise HttpError(400, "gateway_bad_request", "chunked body ended early")
        try:
            size = int(line.split(b";", 1)[0].strip(), 16)
        except ValueError:
            raise HttpError(400, "gateway_bad_request", "bad chunk size") from None
        if size == 0:
            while rfile.readline(65537) not in (b"\r\n", b"\n", b""):
                pass
            return bytes(body)
        if len(body) + size > limit:
            raise HttpError(413, "gateway_body_too_large", "request body too large")
        chunk = rfile.read(size)
        if len(chunk) != size or rfile.read(2) != b"\r\n":
            raise HttpError(400, "gateway_bad_request", "chunked body ended early")
        body += chunk


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "metering-gateway"
    sys_version = ""
    timeout = 600  # an idle or stuck client cannot hold a thread forever
    head_sent = False

    def peer(self) -> str:
        return self.client_address[0]

    def log_message(self, *args: Any) -> None:  # no access log on stderr: the JSONL log is the record
        pass

    def _read_body(self) -> bytes:
        if "chunked" in (self.headers.get("Transfer-Encoding") or "").lower():
            return read_chunked(self.rfile, MAX_BODY_BYTES)
        length = self.headers.get("Content-Length")
        if length is None:
            raise HttpError(411, "gateway_length_required", "send a Content-Length or a chunked body")
        try:
            size = int(length)
        except ValueError:
            raise HttpError(400, "gateway_bad_request", "bad Content-Length") from None
        if size < 0 or size > MAX_BODY_BYTES:
            raise HttpError(413, "gateway_body_too_large", "request body too large")
        data = self.rfile.read(size)
        if len(data) != size:
            raise HttpError(400, "gateway_bad_request", "body shorter than Content-Length")
        return data

    def _serve(self) -> None:
        self.close_connection = True
        self.server.gateway.process(self.peer(), self.command, self.path, dict(self.headers.items()),  # type: ignore[attr-defined]
                                    self._read_body, self)

    do_GET = do_POST = do_PUT = do_DELETE = do_PATCH = do_HEAD = do_OPTIONS = _serve

    # -- reply helpers used by Gateway.process

    def send_reply(self, status: int, headers: list[tuple[str, str]], body: bytes) -> None:
        self.send_response(status)
        for name, value in headers:
            self.send_header(name, value)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.head_sent = True
        if self.command != "HEAD":
            self.wfile.write(body)

    def send_stream_head(self, status: int, headers: list[tuple[str, str]]) -> None:
        self.send_response(status)
        for name, value in headers:
            self.send_header(name, value)
        self.send_header("Connection", "close")
        self.end_headers()
        self.head_sent = True
        self.wfile.flush()

    def send_chunk(self, chunk: bytes) -> None:
        self.wfile.write(chunk)
        self.wfile.flush()


class GatewayServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 256

    def __init__(self, gateway: Gateway, port: int = 0, handler: type[BaseHTTPRequestHandler] = Handler):
        super().__init__((BIND_HOST, port), handler)  # the bind address is not a parameter on purpose
        self.gateway = gateway


# --------------------------------------------------------------------------- command line


def summary_from_log(path: str) -> dict[str, Any]:
    totals = Totals()
    for record in read_log(path):
        totals.add(record)
    cap = currency = None
    manifests = sorted(Path(path).parent.glob(Path(path).name + ".manifest-*.json"))
    if manifests:
        manifest = json.loads(manifests[-1].read_text(encoding="utf-8"))
        cap, currency = Decimal(manifest["cap"]), manifest["currency"]
    return totals.as_dict(cap, currency)


def main(argv: list[str] | None = None, environ: Mapping[str, str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Local metering gateway (loopback only).")
    parser.add_argument("--config", help="TOML config (see tools/metering_gateway.md)")
    parser.add_argument("--port", type=int, help="override the config's port; 0 picks a free one")
    parser.add_argument("--resume", action="store_true", help="continue a run: rebuild spend from the existing log")
    parser.add_argument("--summary", metavar="LOGFILE", help="print the totals of a finished log and exit")
    args = parser.parse_args(argv)
    environ = os.environ if environ is None else environ
    try:
        if args.summary:
            print(json.dumps(summary_from_log(args.summary), indent=2))
            return 0
        if not args.config:
            parser.error("--config is required (or --summary LOGFILE)")
        config = load_config(args.config, environ)
        gateway = Gateway(config, resume=args.resume)
    except (ConfigError, OSError) as exc:
        print(f"metering_gateway: {exc}", file=sys.stderr)
        return 2
    port = config.port if args.port is None else args.port
    try:
        server = GatewayServer(gateway, port)
    except OSError as exc:
        print(f"metering_gateway: cannot bind {BIND_HOST}:{port}: {type(exc).__name__}", file=sys.stderr)
        return 2
    actual = server.server_address[1]
    print(f"metering_gateway: listening on http://{BIND_HOST}:{actual}  cap {money_text(config.cap)} {config.currency}  "
          f"spent so far {money_text(gateway.ledger.spent)}  log {config.log_file}  manifest {gateway.manifest_path}")
    for upstream in config.upstreams.values():
        if upstream.dry_run:
            shown = "dry_run, no key"
        elif upstream.key_file is not None:
            shown = f"key read from the file {upstream.key_file}"
        else:
            shown = f"key from ${upstream.key_env}"
        print(f"  upstream {upstream.name}: {upstream.protocol} {upstream.base_url} ({shown})")
    sys.stdout.flush()

    def stop(*_: Any) -> None:
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        gateway.close()
    print(json.dumps(gateway.summary()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
