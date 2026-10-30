---
slug: gliner
repo: urchade/GLiNER
tier: card
category: core
snapshot: 20261030 19:39 UTC
---

# GLiNER

| | |
|---|---|
| Repository | https://github.com/urchade/GLiNER [1] |
| Licence | Apache-2.0, from the `LICENSE` file (Apache License, Version 2.0 text; head and tail read) [2]. GitHub's licence field agrees [1]. The licence of the pretrained weights on Hugging Face is unstated here (model cards not read). |
| Language | Python [1] |
| Stars, forks | 4,184, 322 (20261030 19:39 UTC; the repository is not in the landscape snapshot) [1] |
| Created, last push | 20231114 18:11 UTC, 20261024 17:44 UTC [1] |
| Latest release | v0.2.29, 20260908 12:40 UTC [3]. PyPI lists 0.2.29, uploaded 20260908 12:50 UTC [4]. |
| Status | active: 6 days since the last push; not archived [1] |
| Paper, docs | arXiv 2311.08526 [6]; the README cites it as NAACL 2024 [5]; docs at https://urchade.github.io/GLiNER [5][7] |

## What it is

GLiNER is a Python framework for training and running small named-entity-recognition (NER) models to which the entity types are given at run time, so any label set can be requested without retraining [5][6]. The README says the models are fine-tunable, "optimized to run on CPUs and consumer hardware", and have performance "competitive with LLMs several times its size, like ChatGPT and UniNER" [5]. The paper's abstract says a bidirectional transformer encoder extracts entities in parallel, rather than generating tokens one at a time as LLMs do [6]. On that description extraction needs no generative LLM, and the usage page I read mentions no LLM component [6][7]. The README lists knowledge graph construction as a use case: entities and relations extracted together to feed Graph RAG [5][7]. In the paper's Table 1 (zero-shot, seven out-of-domain datasets from CrossNER and MIT) the average F1 is 52.7, 55.4 and 60.9 for models of 50M, 90M and 0.3B parameters, against 47.5 for ChatGPT, 53.7 for UniNER-7B and 55.6 for UniNER-13B; training data was Pile-NER (44,889 passages, 13k entity types) [8]. These are the authors' numbers; no independent evaluation was read.

## How it works

Input is a text and a list of entity-type names; `predict_entities` returns the spans scored above a threshold (0.5 in the README example) [5]. The README lists five architectures: uni-encoder (up to about 50 types), bi-encoder (label embeddings precomputed, 100+ types), RelEx (entities and relations in one model), a decoder variant that generates labels, and a streaming span model [5]. Models load with `from_pretrained` from Hugging Face; a medium checkpoint is about 745 MB in fp32 [5][7]. CPU use, INT8, `torch.compile`, ONNX and a Ray Serve HTTP layer are documented [5][7]. MCP: unstated.

## Status and direction

Active. Main has 76 commits since 20260701 (29 in July, 5 in August, 38 in September, 4 in October), the newest dated 20261005; open pull request #402 ("Implement new quantization and serving options") was updated 20261024 [1][9][10]. The newest 12 releases run from v0.2.17 (20250324) to v0.2.29 (20260908) [3]. 54 open issues and pull requests; 45 contributors by the API count [1]. Open issue #401 reports a call hanging for over five minutes on some short inputs [10]. Roadmap: unstated.

## Sources

1. https://github.com/urchade/GLiNER : repository metadata via the GitHub API (stars, forks, licence field, dates, open issue count) and the contributors count (read 20261030 19:39 UTC)
2. https://github.com/urchade/GLiNER/blob/main/LICENSE : Apache License 2.0 text (read 20261030 19:39 UTC)
3. https://github.com/urchade/GLiNER/releases : newest 12 releases, v0.2.17 to v0.2.29 (read 20261030 19:40 UTC)
4. https://pypi.org/project/gliner/ : version 0.2.29 and upload time, read through the PyPI JSON API (read 20261030 19:40 UTC)
5. https://github.com/urchade/GLiNER/blob/main/README.md : description, architectures, optimisation and serving notes, paper citation (read 20261030 19:39 UTC)
6. https://arxiv.org/abs/2311.08526 : abstract of the paper; the page states no venue (read 20261030 19:41 UTC)
7. https://urchade.github.io/GLiNER/usage.html : knowledge-graph and CPU usage notes, model size (read 20261030 19:41 UTC)
8. https://ar5iv.labs.arxiv.org/html/2311.08526 : Table 1 results and Pile-NER size, read through a summarising fetch of the ar5iv rendering (read 20261030 19:43 UTC)
9. https://github.com/urchade/GLiNER/commits/main : commit subjects and counts per month since 20260701 (read 20261030 19:40 UTC)
10. https://github.com/urchade/GLiNER/issues : most recently updated issues and pull requests (read 20261030 19:40 UTC)
