---
slug: deepke
repo: zjunlp/DeepKE
tier: card
category: core
snapshot: 20261030 19:39 UTC
---

# DeepKE

| | |
|---|---|
| Repository | https://github.com/zjunlp/DeepKE [1] |
| Licence | MIT, from the `LICENSE` file ("MIT License", copyright 2021 ZJUNLP; head and tail read) [2]. GitHub's licence field agrees [1]. |
| Language | Python [1] |
| Stars, forks | 4,487, 748 (20261030 19:39 UTC; the repository is not in the landscape snapshot) [1] |
| Created, last push | 20180801 01:54 UTC, 20260713 16:40 UTC [1] |
| Latest release | 2.2.7, 20230921 03:43 UTC [3]. PyPI lists 2.2.7 as the newest version, uploaded 20230921 04:12 UTC [6]. |
| Status | quiet: 109 days since the last push (the template's 90-day rule); not archived [1] |
| Paper, docs | arXiv 2201.03335, EMNLP 2022 System Demonstrations [5]; docs https://zjunlp.github.io/DeepKE/ and an online demo, both linked from the README (not fetched) [4] |

## What it is

DeepKE describes itself as "a knowledge extraction toolkit for knowledge graph construction" that supports cnSchema, low-resource, document-level and multimodal settings for entity, relation and attribute extraction [4]. The README's Quick Start also covers event extraction, and its example data tables are in Chinese [4]. The paper presents it as an open-source, extensible toolkit for knowledge base population; the abstract gives no performance figures [5]. The README points to two LLM routes, DeepKE-LLM and OneKE, and describes OneKE as a bilingual schema-based extraction model based on Chinese-Alpaca-2-13B [4]. Benchmark results in the task READMEs were not read. Independent evaluation: none read.

## How it works

Per the README, every task and scenario is built from Data (tokenizer, preprocessor, loader), Model (module, encoder, forwarder) and Core (training, evaluation, prediction) parts [4]. Typical use: download a dataset, set parameters in a `conf` folder, train with `run.py`, predict with `predict.py` [4]. Models named include LightNER, W2NER, KnowPrompt, PRGC, PURE and ASP [4]. Data are plain `.txt`, `.csv` or `.tsv` files [4]. LLMs enter only through `example/llm` [4]. For agents, `mcp-tools` exposes supervised NER, relation, attribute and event prediction as MCP tools; its README calls the service early stage [7]. The README pins Python 3.8, torch up to 1.11 and transformers 4.26.0 [4]. Graph store or graph loading: unstated [4].

## Status and direction

Quiet, not archived. The default branch had 191 commits in 2024 (86 in April), 14 in 2025 and 1 in 2026, on 20260713, titled "Update README.md" [8]. The latest release and the PyPI version are both 2.2.7, from September 2023 [3][6]. GitHub shows 0 open issues; the 15 most recently updated are closed, the newest on 20260414 [1][9]. The README promises long-term maintenance and a "stronger LLM for KE" in the next version; date: unstated [4].

## Sources

1. https://github.com/zjunlp/DeepKE : repository metadata via the GitHub API (stars, forks, licence field, dates, open issue count) (read 20261030 19:39 UTC)
2. https://github.com/zjunlp/DeepKE/blob/main/LICENSE : MIT License text (read 20261030 19:39 UTC)
3. https://github.com/zjunlp/DeepKE/releases : latest release 2.2.7 (read 20261030 19:39 UTC)
4. https://github.com/zjunlp/DeepKE/blob/main/README.md : description, news list, architecture, tasks, requirements, to-do, citation (read 20261030 19:39 UTC)
5. https://arxiv.org/abs/2201.03335 : abstract and venue of the paper (read 20261030 19:41 UTC)
6. https://pypi.org/project/deepke/ : version list and upload times, read through the PyPI JSON API (read 20261030 19:40 UTC)
7. https://github.com/zjunlp/DeepKE/blob/main/mcp-tools/README.md : MCP tool interfaces and early-stage note (read 20261030 19:41 UTC)
8. https://github.com/zjunlp/DeepKE/commits/main : commits per month since 20240101 and subjects since 20250601 (read 20261030 19:44 UTC)
9. https://github.com/zjunlp/DeepKE/issues : the 15 most recently updated issues (read 20261030 19:40 UTC)
