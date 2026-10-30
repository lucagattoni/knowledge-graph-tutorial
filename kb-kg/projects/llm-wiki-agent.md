---
slug: llm-wiki-agent
repo: SamurAIGPT/llm-wiki-agent
tier: card
category: markdown-kb
snapshot: 20261030 19:41 UTC
---

# LLM Wiki Agent

| | |
|---|---|
| Repository | https://github.com/SamurAIGPT/llm-wiki-agent [1] |
| Licence | MIT, from the `LICENSE` file (MIT text, copyright line "2023 SamurAIGPT") [2]. The README badge and licence section also say MIT [3]. |
| Language | Python (GitHub primary language) [1] |
| Stars, forks | 3,667, 426 (20261030 19:41 UTC; ratio 11.6 forks per 100 stars) [1] |
| Created, last push | 20230421 08:31 UTC, 20261026 08:57 UTC [1] |
| Latest release | none: the releases list is empty [9] |
| Status | active: pushed 4 days before the read; the snapshot sets no flag [1][12] |
| Paper, docs | no paper stated; the README and one guide [3] |

## What it is

A "coding agent skill": the user drops source documents into a `raw/` folder and tells Claude Code, Codex, OpenCode or Gemini CLI to ingest them, and the agent writes an interlinked Markdown wiki [3]. It is an implementation of the LLM-wiki pattern described in Andrej Karpathy's gist of 20260404, which says an LLM "incrementally builds and maintains a persistent wiki", in three layers (raw sources, wiki, schema) with ingest, query and lint operations [10]. The README and `CLAUDE.md` do not name Karpathy or the gist; the README's RAG comparison table makes a similar argument, and its Related list cites Memex, as the gist does [3][4][10].

The repository was created in 2023 for a different project (first code commit "Camel AGI", 20230428). "Add LLM Wiki Agent" is dated 20260407 01:34 UTC, three days after the gist; a later commit removes "legacy CAMEL dual-agent code" [7]. The stars the older project held are unstated, so the snapshot's 2.85 stars per day, computed from the 2023 creation date, is not a launch rate [12].

## How it works

The gist is an "idea file" with no code [10]. This project turns it into agent instructions (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`), four Claude Code slash commands and Python scripts [1][3][4]. Ingest writes a source page, then updates index, overview, entity and concept pages and an append-only log; query reads the index, then the pages it names [4]. Additions to the gist: a graph (wikilink edges, agent-inferred edges, Louvain clusters, one `graph.html`), a zero-LLM `health` check, and markitdown conversion of PDF and Office files [3][4]. Through a coding agent no API key is needed; the standalone scripts call LiteLLM, model from `LLM_MODEL` [3][5]. The README says "No server, no database"; local-model support is unstated [3].

## Status and direction

Active by push date, but 13 of the 15 commits since 20260801 are the star-history bot; the last human commit is 20260908 [7]. Eight contributors [8]. 6 pull requests open, 35 merged; 7 issues open [11]. The README lists no roadmap [3]. `CLAUDE.md` lists a `/wiki-health` command with no file in the commands folder [1][4]. `requirements.txt` pins LiteLLM after what it calls a March 2026 supply-chain compromise of two versions [6].

## Sources

1. https://github.com/SamurAIGPT/llm-wiki-agent : repository metadata and file tree via the GitHub API (read 20261030 19:41 UTC)
2. https://github.com/SamurAIGPT/llm-wiki-agent/blob/main/LICENSE : MIT text (read 20261030 19:41 UTC)
3. https://github.com/SamurAIGPT/llm-wiki-agent/blob/main/README.md : description, install, usage, graph, RAG comparison, tech stack, licence (read 20261030 19:41 UTC)
4. https://github.com/SamurAIGPT/llm-wiki-agent/blob/main/CLAUDE.md : schema and the ingest, query, lint, health and graph workflows (read 20261030 19:41 UTC)
5. https://github.com/SamurAIGPT/llm-wiki-agent/blob/main/tools/_utils.py : `call_llm` via LiteLLM, `LLM_MODEL` (read 20261030 19:41 UTC)
6. https://github.com/SamurAIGPT/llm-wiki-agent/blob/main/requirements.txt : dependencies and the supply-chain note (read 20261030 19:41 UTC)
7. https://github.com/SamurAIGPT/llm-wiki-agent/commits/main : commit history (2023, April 2026, and since 20260801) (read 20261030 19:41 UTC)
8. https://github.com/SamurAIGPT/llm-wiki-agent/graphs/contributors : eight contributors via the API (read 20261030 19:41 UTC)
9. https://github.com/SamurAIGPT/llm-wiki-agent/releases : empty (read 20261030 19:41 UTC)
10. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f : Karpathy, "LLM Wiki", created 20260404 16:25 (time zone as shown on the page, unstated); the original description of the pattern, traced in [the LLM-era timeline](../llm-era/README.md); raw file read from the gist's raw URL (read 20261030 19:42 UTC)
11. https://github.com/SamurAIGPT/llm-wiki-agent/pulls : pull request and issue counts via the search API (read 20261030 19:41 UTC)
12. [The first GitHub snapshot](../landscape/20261030_1913-github/repos.tsv) : row for this repository, no flag (read 20261030 19:41 UTC)
