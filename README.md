# Knowledge bases and knowledge graphs

**Documentation site:** <https://lucagattoni.github.io/knowledge-graph-tutorial/>

How the ideas of a knowledge base (KB) and a knowledge graph (KG) evolved, which families of approach are
moving now, and the projects, papers, datasets and benchmarks behind them, with a focus on language models
and agents that build and query them. The documentation was written from scratch on 20261102 (UTC); the
earlier notebook is kept as the archive.

**Status:** work in progress. The state of the experiments is in [`RESUME.md`](RESUME.md); the owner's
decisions are in [`DECISIONS.md`](DECISIONS.md).

## What is where

| Folder or file | What it holds |
|---|---|
| [`docs/`](docs/README.md) | The documentation, and the site's home page: History, Trends, Projects, Papers, Datasets, Benchmarks, Experiments, Applied to Pinakes, and the A to Z Index. Start at [`docs/README.md`](docs/README.md). |
| `kb-kg/`, `pinakes/`, [`DECISIONS.md`](DECISIONS.md) | The archive: the earlier field reference, the notes for [Pinakes](https://github.com/lucagattoni/pinakes), the dated GitHub snapshots and the experiments' working pages. Published unchanged under the Archive tab, at their old addresses. The new documentation uses these pages as sources. |
| [`RESUME.md`](RESUME.md) | Working state of the experiments (not published on the site). |
| `tools/` | Scripts: the GitHub snapshot (`gh_snapshot.py`), the generator for the documentation's generated sections (`build_docs.py`), the archive's projects index, the experiments' instruments, and the public-safety gate. |
| `docs-site/`, `mkdocs.yml` | The site build: staging, the navigation and link hooks, and the theme settings. How it works: [`docs-site/README.md`](docs-site/README.md). |

## Keeping it up to date

The Projects, Papers, Datasets, Benchmarks and Trends chapters are live: each has a dated list of changes
(`changes.tsv` in its folder), and the generated parts of the pages are rebuilt from data.

```bash
uv run tools/gh_snapshot.py        # take a new dated GitHub snapshot (stars, activity, licences)
uv run tools/build_docs.py         # rebuild the generated sections of docs/ (A to Z, watch list, change lists, "appears in")
uv run tools/build_docs.py --check # exit 1 if a generated section is out of date (CI runs this)
```

## Conventions

- **Every timestamp is UTC**, written `YYYYMMDD HH:MM`.
- **Every statement about a project, paper, dataset or benchmark cites a source and the time it was read.**
  Where the source is silent the page says **unstated**.
- **Stars are a signal, not a verdict**, and carry their date. Licences are read from the `LICENSE` file.
- **This repository is public.** Run `tools/check_public_safe.sh` before every commit; it must exit 0.

## Licence

Apache-2.0 for the text and the code. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE): quoted third-party text
and data fetched from other services keep their own terms.
