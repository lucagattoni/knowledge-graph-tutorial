#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Freeze the 20 documents of the X2 pilot by a rule that involves no choice.

    uv run tools/exp/x2_select_documents.py CORPUS_JSON [--out documents.tsv] [--n 20]

The rule, fixed before the result was looked at: rank every article by the SHA-256 of its URL, as lowercase hex,
and keep the n smallest. It needs no random generator and no judgement, and anyone with the corpus gets the same list.

CORPUS_JSON is the MultiHop-RAG `corpus.json` at the revision pinned in the benchmark repository's manifest. The tool
refuses a file whose SHA-256 differs from the pinned one. The output lists identifiers and sizes only; the article text
is never written, because the dataset's news text comes from publishers whose own terms were not checked.

Standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

PINNED_SHA256 = "20b61b5ab84de84a927420c5d265b7ec8d859ae49980699958a787ade9e4d28f"
PINNED_REVISION = "71ac0d0bd1f951d2d6b70311f7d2ae404e1ffa82"
RULE = "the n articles whose SHA-256 of the URL, as lowercase hex, is smallest"


def url_digest(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def select(articles: list[dict], n: int) -> list[dict]:
    """The n articles with the smallest URL digest, smallest first. Raises on a missing or repeated URL."""
    urls = [a.get("url") for a in articles]
    if not all(isinstance(u, str) and u for u in urls):
        raise ValueError("every article needs a non-empty url")
    if len(set(urls)) != len(urls):
        raise ValueError("urls are not distinct, so the rule would be ambiguous")
    if not 1 <= n <= len(articles):
        raise ValueError(f"n must be between 1 and {len(articles)}")
    ranked = sorted(articles, key=lambda a: url_digest(a["url"]))
    return ranked[:n]


def render(chosen: list[dict], total_articles: int, total_chars: int) -> str:
    lines = [
        f"# X2 pilot documents: {RULE}.",
        f"# corpus: MultiHop-RAG corpus.json, revision {PINNED_REVISION}, sha256 {PINNED_SHA256}",
        f"# corpus size: {total_articles} articles, {total_chars} characters of body text",
        "rank\turl_sha256_16\tchars\twords\tcategory\tsource\tpublished_at\turl",
    ]
    for rank, a in enumerate(chosen, 1):
        body = a.get("body", "")
        fields = [
            str(rank),
            url_digest(a["url"])[:16],
            str(len(body)),
            str(len(body.split())),
            str(a.get("category", "")),
            str(a.get("source", "")),
            str(a.get("published_at", "")),
            a["url"],
        ]
        lines.append("\t".join(f.replace("\t", " ").replace("\n", " ") for f in fields))
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("corpus", help="path to MultiHop-RAG corpus.json at the pinned revision")
    parser.add_argument("--out", default="kb-kg/experiments/x2-index-cost/documents.tsv")
    parser.add_argument("--n", type=int, default=20)
    args = parser.parse_args(argv)

    raw = Path(args.corpus).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != PINNED_SHA256:
        print(f"refusing: corpus sha256 {digest} is not the pinned {PINNED_SHA256}", file=sys.stderr)
        return 1
    articles = json.loads(raw)
    chosen = select(articles, args.n)
    total_chars = sum(len(a.get("body", "")) for a in articles)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(chosen, len(articles), total_chars))
    print(f"wrote {len(chosen)} rows to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
