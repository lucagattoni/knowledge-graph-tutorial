"""Tests for tools/exp/x2_select_documents.py. Standard library only, fake data, no network.

Run from the repository root:

    uv run python -m unittest tools/exp/test_x2_select_documents.py
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import x2_select_documents as sel  # noqa: E402


def fake(n: int) -> list[dict]:
    return [
        {"url": f"https://example.test/a{i}", "body": "word " * (i + 1), "category": "c", "source": "s", "published_at": "d"}
        for i in range(n)
    ]


class SelectTests(unittest.TestCase):
    def test_keeps_the_n_smallest_digests_in_order(self) -> None:
        arts = fake(50)
        chosen = sel.select(arts, 5)
        digests = [sel.url_digest(a["url"]) for a in chosen]
        self.assertEqual(digests, sorted(digests))
        everyone = sorted(sel.url_digest(a["url"]) for a in arts)
        self.assertEqual(digests, everyone[:5])

    def test_input_order_does_not_change_the_result(self) -> None:
        arts = fake(40)
        forward = [a["url"] for a in sel.select(arts, 8)]
        backward = [a["url"] for a in sel.select(list(reversed(arts)), 8)]
        self.assertEqual(forward, backward)

    def test_digest_is_sha256_of_the_url_in_lowercase_hex(self) -> None:
        url = "https://example.test/x"
        self.assertEqual(sel.url_digest(url), hashlib.sha256(url.encode()).hexdigest())

    def test_repeated_or_missing_urls_are_refused(self) -> None:
        arts = fake(3)
        arts[1]["url"] = arts[0]["url"]
        with self.assertRaises(ValueError):
            sel.select(arts, 2)
        arts = fake(3)
        arts[2]["url"] = ""
        with self.assertRaises(ValueError):
            sel.select(arts, 2)

    def test_n_out_of_range_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            sel.select(fake(3), 0)
        with self.assertRaises(ValueError):
            sel.select(fake(3), 4)

    def test_output_has_identifiers_and_sizes_but_never_the_text(self) -> None:
        arts = fake(3)
        arts[0]["body"] = "SECRET-ARTICLE-TEXT " * 3
        text = sel.render(sel.select(arts, 3), 3, 99)
        self.assertNotIn("SECRET-ARTICLE-TEXT", text)
        self.assertIn("rank\turl_sha256_16\tchars\twords", text)


class MainTests(unittest.TestCase):
    def test_a_file_with_the_wrong_hash_is_refused_and_nothing_is_written(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            corpus = Path(d) / "corpus.json"
            corpus.write_text(json.dumps(fake(5)))
            out = Path(d) / "out" / "documents.tsv"
            self.assertEqual(sel.main([str(corpus), "--out", str(out), "--n", "2"]), 1)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
