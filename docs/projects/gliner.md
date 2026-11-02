---
type: project
repo: urchade/GLiNER
trends: [llm-kg-construction]
updated: 20261102 23:17 UTC
---

# GLiNER

This page answers what GLiNER is, how it finds entities and relations without a generative model, what its authors published, and whether it is still moving. It sits in the trend on [building knowledge graphs with LLMs](../trends/llm-kg-construction.md) as the small-model way to do the extraction step.

| Field | Value |
|---|---|
| Repository | https://github.com/urchade/GLiNER |
| Licence | Apache-2.0, from the `LICENSE` file: the Apache License 2.0 text, 11,357 bytes, with the appendix placeholder "[yyyy] [name of copyright owner]" left unfilled [2]. GitHub classifies it the same way [2]. Four checkpoints read through the Hugging Face API also carry the tag apache-2.0; all other checkpoints: unstated [10]. |
| Trends | [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md) |

## What it is

GLiNER is a Python framework and a family of small models for [named-entity recognition](../index/named-entity-recognition.md) where the entity types are given at run time. Any label set can be requested without retraining. The README adds streaming NER (named-entity recognition) and joint entity and [relation extraction](../index/relation-extraction.md), and calls the models "optimized to run on CPUs and consumer hardware" [4]. The paper is by Zaratiana, Tomeh, Holat and Charnois: arXiv 20231114, NAACL (North American Chapter of the Association for Computational Linguistics) 2024 [6][8].

A bidirectional transformer encoder scores candidate spans against entity-type embeddings in parallel. An [LLM](../index/large-language-model.md) (large language model) generates tokens one at a time instead [6]. In this original encoder design the extraction step needs no generative model; the GLiNER Decoder variant adds a small decoder that generates entity types [4]. An LLM did appear earlier: the training set, Pile-NER (44,889 passages, 240k entity spans, 13k entity types), was labelled with ChatGPT by other authors [7].

*Reading:* the trend is named for graphs built with LLMs, and the original GLiNER builds none of its output with one. The paper's models have 50M to 0.3B parameters and you run them yourself [7]. The cost is a narrow task: tagging spans and, with the relation model, linking them. The entity and relation label lists come from the user; schema induction is not mentioned in the README or usage page read [4][9]. [OntoGPT](./ontogpt.md) is the contrast: an LLM filling a schema, with grounding to ontologies.

## How it works

Input is a text and a list of type names. `predict_entities` returns spans scored above a threshold (0.5 in the README example) [4]. Models load with `from_pretrained` from Hugging Face. The README lists five architectures [4]:

| Architecture | What it does |
|---|---|
| Uni-encoder | The original; up to about 50 entity types |
| Bi-encoder | Label embeddings computed once; scales past 100 types |
| RelEx | Entities and relations in one model |
| GLiNER Decoder | A small decoder generates the labels |
| StreamingSpan | Incremental NER with reused caches |

For graph building, the usage page loads a RelEx checkpoint and calls `inference` with entity and relation labels; relations point at entity indexes [9]. Fine-tuning is documented [4]. For speed the README documents `torch.compile`, FP16, INT8, ONNX export and a Ray Serve layer; its speed-up figures are the authors' own, with no hardware named [4]. MCP (Model Context Protocol): unstated; no path in the repository tree contains "mcp" [12].

## Evidence

All published results are first-party. Table 1 of the paper is a zero-shot test: seven out-of-domain datasets from CrossNER and MIT, exact-match F1 (a score that balances precision and recall), training only on Pile-NER [7]. The baseline rows are copied from other papers, as the table caption says [7].

| System | Parameters | Average F1 | Who ran it |
|---|---|---|---|
| GLiNER-S | 50M | 52.7 | GLiNER authors, first-party |
| GLiNER-M | 90M | 55.4 | GLiNER authors, first-party |
| GLiNER-L | 0.3B | 60.9 | GLiNER authors, first-party |
| ChatGPT | not given | 47.5 | copied from Zhou et al. 2023 |
| UniNER-7B | 7B | 53.7 | copied from Zhou et al. 2023 |
| UniNER-13B | 13B | 55.6 | copied from Zhou et al. 2023 |
| GoLLIE | 7B | 58.0 | copied from Sainz et al. 2023 |

Only the large model beats every row. The medium model ties UniNER-13B at 55 F1, as the authors write [7]. Table 3 compares two variants, En and Multi, on ten non-English languages [7]. The Multi variant (mdeBERTa-v3-base) beats ChatGPT in 8 of the 10, losing on Korean and Turkish. The En variant (deBERTa-v3-Large) scores 0.89 F1 on Bengali, and the paper calls its non-Latin performance "markedly less competitive" [7]. Figures were read from arXiv v1, marked "Work in progress" [6]; the NAACL version was not read. No independent evaluation appears in the sources read. The paper in context is in the [papers group](../papers/llm-kg-construction.md).

## Status and direction

Active. The latest release is v0.2.30, 20261102 08:55 UTC [3]. It adds FP8 inference, confidence calibration and a unified `/gliner/v1/process` serving API for entity and relation tasks [3]. Before it came v0.2.29 (20260908) and v0.2.28 (20260724); 43 releases in all [3][12].

In the 90 days since 20260804, `main` took 61 commits: 5 in August, 38 in September, 18 in October; 18 are pull-request merges. There are 45 contributors and 54 open issues and pull requests, 2 of them pull requests [1][12]. Open issue #401 reports `predict_entities` hanging for over five minutes on some short inputs; pull request #404 proposes a fix [11].

The README names two maintainers, at Fastino and Knowledgator, and lists a separate GLiNER2 project [4]. It shows no maintenance-mode notice. Roadmap: unstated.

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Building knowledge graphs with LLMs: from fixed schemas to induced ones](../trends/llm-kg-construction.md)
- [Graph features removed and added](../trends/features-in-and-out.md)
- [Trends: what the field is doing now](../trends/README.md)

**Projects**

- [Cognee](cognee.md)
- [GraphRAG SDK](graphrag-sdk.md)
- [Memgraph](memgraph.md)
- [OntoGPT](ontogpt.md)
- [Projects](README.md)

**Applied to Pinakes**

- [What Pinakes should measure next](../applied-to-pinakes/next.md)

**Index**

- [Named-entity recognition](../index/named-entity-recognition.md)
- [Relation extraction](../index/relation-extraction.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://github.com/urchade/GLiNER : repository metadata by `gh api` (archived flag, open issues and pull requests) (read 20261102 20:09 UTC)
2. https://github.com/urchade/GLiNER/blob/main/LICENSE : licence file by `gh api .../license`: Apache License 2.0, size, GitHub classification (read 20261102 20:09 UTC)
3. https://github.com/urchade/GLiNER/releases : latest release v0.2.30 with its notes, the eight newest releases (read 20261102 20:10 UTC)
4. https://github.com/urchade/GLiNER/blob/main/README.md : description, architectures including the Decoder row, optimisation and serving notes, maintainers, ecosystem (read 20261102 20:31 UTC)
5. https://github.com/urchade/GLiNER/commits/main : 61 commits since 20260804 by month (read 20261102 20:09 UTC)
6. https://arxiv.org/abs/2311.08526 : title, authors, submission history (v1 only), comment "Work in progress" (read 20261102 20:31 UTC)
7. https://ar5iv.labs.arxiv.org/html/2311.08526 : abstract, Pile-NER size, Table 1, protocol, Table 3 (two variants, ten languages) and its caption, script results; renders arXiv v1 (read 20261102 20:31 UTC)
8. https://aclanthology.org/2024.naacl-long.300/ : venue NAACL 2024, pages 5364 to 5376 (read 20261102 20:11 UTC)
9. https://urchade.github.io/GLiNER/usage.html : knowledge-graph construction example with a RelEx model (read 20261102 20:11 UTC)
10. https://huggingface.co/api/models/gliner-community/gliner_small-v2.5 : licence tag apache-2.0; the same for knowledgator/gliner-relex-large-v1.0, urchade/gliner_multi_pii-v1 and urchade/gliner_medium-v2.1 (read 20261102 20:11 UTC)
11. https://github.com/urchade/GLiNER/issues/401 : open issue; pull request 404 (read 20261102 20:12 UTC)
12. https://github.com/urchade/GLiNER : repository tree (no path containing "mcp"), contributor and release counts by `gh api` (read 20261102 20:11 UTC)
