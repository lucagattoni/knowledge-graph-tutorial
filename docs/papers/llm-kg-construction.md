---
type: papers
group: llm-kg-construction
order: 3
updated: 20261102 23:22 UTC
---

# Papers: Building knowledge graphs with LLMs

This group holds the papers behind [Building knowledge graphs with LLMs](../trends/llm-kg-construction.md): a [language model](../index/large-language-model.md) turns text into a [knowledge graph](../index/knowledge-graph.md), and the question is who decides the types of entity and relation, a person or the model ([schema induction](../index/schema-induction.md)). Five papers are listed: a 2020 paper that builds a graph from a model's own knowledge, an evaluation and a survey of 2023, EDC, which moves the [schema](../index/schema.md) out of the prompt, and a survey of the shift; each section names the test it passes and says where the evidence for that test is thin. AutoSchemaKG, listed in the first edition, is in the further reading: on the sources read it passes none of the four tests. The sources read name no blog post or gist as the origin of this line, and benchmarks for the step, such as [Text2KGBench](../benchmarks/text2kgbench.md), are in the [benchmarks chapter](../benchmarks/text2kgbench.md). Citation counts are Semantic Scholar, read 20261102 19:47 UTC, carried over from this documentation's candidate research and not queried again; none is compared with a count from another source, and for *widely built on* this page applies one working threshold of 100 citations, which is this page's choice and not a rule of the plan [13].

## Language Models are Open KGs (2020)

*Language Models are Open Knowledge Graphs.* Chenguang Wang, Xiao Liu, Dawn Song (3 authors in total) [1]. Preprint; the arXiv record names no venue [1]. First version 20201022 [1]. <https://arxiv.org/abs/2010.11967>

**Why fundamental:** One test, *origin*, narrowed by a search of earlier work. The abstract (first-party) says a graph is built "from pre-trained language models (e.g., BERT, GPT-2/3), without human supervision", with "a single forward pass" and no fine-tuning [1]. An arXiv search made for this page (titles and abstracts of records before 20201022; source 23) found the nearest earlier records: COMET (20190612), which trains a model on seed tuples to generate commonsense graphs [6][23] (its successor COMET-ATOMIC 2020, of 20201012, was seen by title only), and Language Models as Knowledge Bases? (20190903), which probes what a model recalls through cloze statements [23]. Neither builds a graph from a model's attention weights without training, so the claim stands only in that narrow form, not as "first model-built graph". No independent source read says this work began the line. None of the other papers read for this group, AutoSchemaKG included, names the paper in its full text [4][6][8][10][12]. Its citation count is **unstated**: Semantic Scholar returned an error on the day [13], so the count test cannot be applied. It is listed as the earliest paper of the group.

**Idea:** Match and Map (MaMa). Match runs a beam search over the model's attention weights to find candidate (head, relation, tail) facts in each sentence. Map sends a fact to the fixed schema (Wikidata's, in the paper's example) when it exists there, and otherwise keeps it under an open schema [2]. First-party: the best variant, MaMa-GPT-2 XL, scores 22.39 F1 on Wikidata against 16.77 for Stanford OpenIE, and 29.72 F1 on TAC KBP [2]. It answers [Petroni et al. (2019)](./foundations.md): where that work recalls facts through cloze statements, MaMa "directly generates the whole fact" as a triple [2]. It answers [Bollacker et al. (2008)](./foundations.md) and [Dong et al. (2014)](./foundations.md): hand-written graphs such as Freebase and semi-automatic extractors such as Knowledge Vault are the human cost it removes [2]. It is scored against [Wikidata](../datasets/wikidata.md), the human-made reference graph [1][2].

**Relations:** Answers: [Petroni et al. (2019)](./foundations.md), [Bollacker et al. (2008)](./foundations.md), [Dong et al. (2014)](./foundations.md).

**Read:** the arXiv record in full (20261102 20:58 UTC) [1]; the full text, searched for the passages cited and not read end to end (20261102 20:42 UTC) [2]; the full texts of the other five papers, searched for this paper's title and authors (20261102 20:58 UTC) [4][6][8][10][12].

## Zhu et al. (2023)

*LLMs for Knowledge Graph Construction and Reasoning: Recent Capabilities and Future Opportunities.* Yuqi Zhu, Xiaohan Wang, Jing Chen (9 authors in total) [3]. *World Wide Web* 27(5), article 58, 2024: the arXiv comment names the journal [3], the volume and article number come from a later paper's reference list [12]. First version 20230522 [3]. <https://arxiv.org/abs/2305.13168>

**Why fundamental:** one test, *widely built on*, by count: 337 citations [13], above this page's threshold of 100. It is also an evaluation study that reports a finding, a kind of paper the chapter keeps. Across eight datasets and four tasks (entity and relation extraction, event extraction, [link prediction](../index/link-prediction.md), question answering), it finds GPT-4 "more suited as inference assistants rather than few-shot information extractors" [3]. The sources read give no evidence that this finding changed what later work did, so *turning point* is not claimed. Pan et al. describe the paper's AutoKG in their construction section, and the 2025 survey cites the paper in its introduction [6][12]. AutoKG is the authors' own approach, so its claims are first-party.

**Idea:** test the models zero-shot and one-shot against fully supervised systems [4]. Add a Virtual Knowledge Extraction task, with a new dataset called VINE, to see whether a model can use knowledge given only in the instructions. Propose AutoKG, a multi-agent approach that uses language models and external sources for construction and reasoning [3]. It is scored on [FB15k-237](../datasets/fb15k-237.md) for link prediction and on [MetaQA](../datasets/metaqa.md), with FreebaseQA, for question answering [4]. Version 4 cites [Pan et al. (2023)](./llm-kg-construction.md) only in a string of references for the general definition of a knowledge graph, as background and not as the base of its method [4]; it builds on no paper of this chapter.

**Relations:** None.

**Read:** the arXiv record in full (20261102 21:01 UTC) [3]; the full text of version 4, searched for the passages cited and not read end to end (20261102 20:58 UTC) [4].

## Pan et al. (2023)

*Unifying Large Language Models and Knowledge Graphs: A Roadmap.* Shirui Pan, Linhao Luo, Yufei Wang (6 authors in total) [5]. *IEEE Transactions on Knowledge and Data Engineering* 36(7), 2024, DOI 10.1109/TKDE.2024.3352100 [5]; volume and pages from a later reference list [12]. First version 20230614 [5]. <https://arxiv.org/abs/2306.08302>

**Why fundamental:** two tests. *Survey of record* for the pairing of the two technologies: it sorts the work into three frameworks, KG-enhanced LLMs, LLM-augmented KGs (embedding, completion, construction, graph-to-text, question answering) and synergized LLMs and KGs [5]. *Widely built on*, by count: 1,927 citations [13], the highest of the counts recorded in this group; the 2025 survey cites it in its introduction [12]. *Reading:* its construction section is organised by entity discovery, coreference resolution, relation extraction, end-to-end construction and distilling graphs from models [6]. Schema induction is not a heading, so it describes the field before the shift this group follows.

**Idea:** language models are fluent but black boxes that fall short on facts; graphs store facts explicitly but are hard to build and keep current. The paper reviews work that joins them, with open problems for each framework [5]. No builds-on, answers or evaluates relation was found in the full text read. Two citations are recorded: it cites [Petroni et al. (2019)](./foundations.md) for the finding that language models implicitly encode much knowledge, as background to its section on distilling graphs from models, and it describes AutoKG, the approach of [Zhu et al. (2023)](./llm-kg-construction.md), in its construction section as one work among several [6].

**Relations:** None.

**Read:** the arXiv record in full (20261102 20:41 UTC) [5]; the full text of version 3, searched for the passages cited and not read end to end (20261102 20:58 UTC) [6].

## EDC (2024)

*Extract, Define, Canonicalize: An LLM-based Framework for Knowledge Graph Construction.* Bowen Zhang, Harold Soh (2 authors in total) [7]. EMNLP 2024 (arXiv comment) [7]; pages 9820 to 9836 from a later reference list [10]. First version 20240405 [7]. <https://arxiv.org/abs/2404.03868>

**Why fundamental:** One test, *widely built on*, by count: 181 citations [13], above this page's threshold of 100. What the full texts show of its use is smaller. AutoSchemaKG (further reading) cites it once, in its introduction, among earlier work on removing the manual bottleneck of construction, and does not compare against it [10]. The 2025 survey cites it in its introduction, describes it as advancing the pipeline into three stages (open extraction, semantic definition, schema normalization), and uses it as its example of schema-free open extraction [12]. No source read says EDC was the first to do this, so no priority is claimed.

**Idea:** earlier prompted methods put the schema in the prompt, which fails when a schema is larger than the context window or absent [7]. EDC extracts free triples, asks the model to define each type and relation they use, then maps them onto a target schema or onto its own. An optional trained retriever (EDC+R) feeds the relevant schema elements back for a second pass [7][8]. First-party: on REBEL, EDC+R with GPT-4 reaches partial F1 0.601 against 0.385 for GenIE. The authors say the references are incomplete, so scores are pessimistic [8]. It answers the limit of earlier prompt-based extraction, which "are currently limited to small and domain-specific scenarios"; the methods it names (ChatIE, CodeKGC) are not papers of this chapter [8]. The [Bian survey (2025)](./llm-kg-construction.md) describes it and AutoSchemaKG cites it; neither builds on its method [10][12].

**Relations:** None.

**Read:** the arXiv record in full (20261102 20:41 UTC) [7]; the full text, searched for the passages cited and not read end to end (20261102 20:58 UTC) [8].

## Bian survey (2025)

*LLM-empowered knowledge graph construction: A survey.* Haonan Bian (1 author) [11]. No venue stated [11]. First version 20251023 [11]. <https://arxiv.org/abs/2510.20345>

**Why fundamental:** *survey of record*, provisionally. It is dedicated to this step and analyses how language models change the three-layer pipeline of ontology engineering, knowledge extraction and knowledge fusion, in a schema-based and a schema-free paradigm [11]. It is the only survey found that is dedicated to LLM-based construction. A title search of the arXiv listing (20261102 21:00 UTC) also returned surveys of knowledge graph construction of 2021, 2022, 2023 and 2024; the abstracts of the 2023 and 2024 ones do not mention language models, so they are out of scope here, and the 2021 and 2022 ones were seen by title only [20][21][22]. The search was a listing search, not exhaustive. One author and 51 citations [13] make the status provisional.

**Idea:** construction is "shifting from rule-based and statistical pipelines to language-driven and generative frameworks" [11]. Schema-based work stresses structure and consistency; schema-free work stresses flexibility and open discovery [11]. The text calls the schema a component that co-evolves with extraction, not a fixed template [12]. It lists as directions graph-based reasoning for models, dynamic knowledge memory for agents ([agent memory](../index/agent-memory.md)) and multimodal construction [11]. It cites [Pan et al. (2023)](./llm-kg-construction.md) and [Zhu et al. (2023)](./llm-kg-construction.md) in its introduction [12]. It places [EDC (2024)](./llm-kg-construction.md) in its taxonomy as an example of schema-free open extraction, and AutoSchemaKG (further reading) as a system that joins the schema-based and schema-free paradigms [12].

**Relations:** Builds on: [EDC (2024)](./llm-kg-construction.md); also: AutoSchemaKG.

**Read:** the arXiv record in full (20261102 21:01 UTC) [11]; the full text, searched for the passages cited and not read end to end (20261102 20:58 UTC) [12].

## Further reading

Papers left out of the fundamental list, one line each. Counts are Semantic Scholar, read 20261102 19:47 UTC, carried over [13].

- **SPIRES** (2023), <https://arxiv.org/abs/2304.02711>: zero-shot extraction with GPT-3 and later models that takes "a detailed, user-defined knowledge schema" as input and grounds names to ontology identifiers; the given-schema end of the shift; 12 authors; part of OntoGPT [14].
- **KGGen** (2025), <https://arxiv.org/abs/2502.09956>: a Python package that extracts graphs from plain text and clusters related entities to cut sparsity; releases the MINE benchmark; 9 authors; 92 citations [15][13].
- **Are Large Language Models Effective Knowledge Graph Constructors?** (2025), <https://arxiv.org/abs/2510.11297>: zero-shot, schema-free construction by seven frontier models on a new paediatric-research set; 13 authors; 1 citation, too new to count [16][13].
- **AutoSchemaKG** (2025), <https://arxiv.org/abs/2505.23628>: extracts triples and induces the schema together, with no predefined schema, over more than 50 million documents; it builds ATLAS, graphs of "900+ million nodes and 5.9 billion edges", the largest graph size reported by the papers of this group; 20 authors, 38 citations, all results first-party. The abstract on the arXiv record says 92% semantic alignment with human-made schemas; the abstract block of the version-3 full text says 95% while its introduction says 92% [9][10][13]. Moved from the fundamental list: its citations are under this page's threshold of 100, no source read calls it an origin or a turning point, and the 2025 survey only describes it as joining the schema-based and schema-free paradigms [12].
- **DIAL-KG** (2026), <https://arxiv.org/abs/2603.20059>: closed-loop incremental construction in which new schemas are induced from validated knowledge; accepted to DASFAA 2026 [17].
- **OntoKG** (2026), <https://arxiv.org/abs/2604.02618>: designs the schema first and applies it to a January 2026 Wikidata dump, 34.0 million nodes and 61.2 million edges in a [property graph](../index/property-graph.md) [18].
- **SCOPE and SCION** (2026), <https://arxiv.org/abs/2607.21610>: a benchmark and a reference pipeline for inducing schemas from text, built from 24 public extraction sources; the authors say the results are not claims that induced schemas beat human design [19].

## Sources

1. <https://arxiv.org/abs/2010.11967> : Language Models are Open KGs: title, three authors, first version 20201022, no venue, abstract with "without human supervision" and the single forward pass (read 20261102 20:58 UTC)
2. <https://ar5iv.labs.arxiv.org/html/2010.11967> : full text: Match and Map, F1 scores of Tables 2 and 3, the comparison with cloze-style recall, the introduction's account of Freebase and Knowledge Vault (read 20261102 20:42 UTC)
3. <https://arxiv.org/abs/2305.13168> : Zhu et al.: title, nine authors, first version 20230522, journal named in the comment, abstract with the eight datasets, four tasks and the GPT-4 finding (read 20261102 21:01 UTC)
4. <https://arxiv.org/html/2305.13168> : full text of version 4: datasets (FB15K-237, MetaQA, FreebaseQA and others), zero-shot and one-shot setting, the one citation of the roadmap, in the string of references on the definition of a knowledge graph (read 20261102 20:58 UTC)
5. <https://arxiv.org/abs/2306.08302> : Pan et al.: title, six authors, first version 20230614, journal reference and DOI, abstract (read 20261102 20:41 UTC)
6. <https://arxiv.org/html/2306.08302> : full text of version 3: section headings of the construction part, the AutoKG sentences, COMET with its 2019 reference and seed set of tuples, citation of Petroni et al. (read 20261102 20:58 UTC)
7. <https://arxiv.org/abs/2404.03868> : EDC: title, two authors, first version 20240405, EMNLP 2024 in the comment, abstract (read 20261102 20:41 UTC)
8. <https://arxiv.org/html/2404.03868> : full text: the quoted limit of earlier methods, three phases, REBEL scores 0.601 and 0.385, incomplete references (read 20261102 20:58 UTC)
9. <https://arxiv.org/abs/2505.23628> : AutoSchemaKG: title, twenty authors, first version 20250529, "preprint" in the comment, abstract with 50 million documents, 900+ million nodes, 5.9 billion edges and 92% (read 20261102 20:58 UTC)
10. <https://arxiv.org/html/2505.23628> : full text of version 3: the single citation of EDC in the introduction, the introduction's "12-18%" against "state-of-the-art baselines", section 5.2 (12-18% over BM25 and Contriever with HippoRAG2 integration), the baselines, Tables 5 and 7 with Think-on-Graph, the MuSiQue, 2Wiki and HotpotQA rows for HippoRAG2 and for Full-KG with HippoRAG2, 78,400 GPU hours, 95% in the abstract block against 92% in the introduction (read 20261102 20:58 UTC)
11. <https://arxiv.org/abs/2510.20345> : Bian survey: title, one author, first version 20251023, abstract with the quoted shift (read 20261102 21:01 UTC)
12. <https://arxiv.org/html/2510.20345> : full text: the introduction's citations of Pan et al., Zhu et al. and Zhang and Soh with their venues, the descriptions of EDC (three stages, open extraction, canonicalization) and AutoSchemaKG, the schema-co-evolution passage (read 20261102 20:58 UTC)
13. Semantic Scholar Graph API, batch call on arXiv ids : citation counts 1927 (2306.08302), 337 (2305.13168), 181 (2404.03868), 51 (2510.20345), 38 (2505.23628), 92 (2502.09956), 1 (2510.11297), and the venue field of 2505.23628 (read 20261102 19:47 UTC, carried over from this documentation's candidate research; not queried again because the interface was rate-limited that day; no count for 2010.11967 was obtained). The 100-citation threshold is this page's own choice.
14. <https://arxiv.org/abs/2304.02711> : SPIRES: twelve authors, quoted input, OntoGPT (read 20261102 20:47 UTC)
15. <https://arxiv.org/abs/2502.09956> : KGGen: nine authors, clustering, MINE (read 20261102 20:47 UTC)
16. <https://arxiv.org/abs/2510.11297> : seven models, 13 authors, first version 20251013 (read 20261102 20:47 UTC)
17. <https://arxiv.org/abs/2603.20059> : DIAL-KG: closed loop, schema induction, DASFAA 2026 (read 20261102 20:47 UTC)
18. <https://arxiv.org/abs/2604.02618> : OntoKG: schema first, Wikidata dump, node and edge counts (read 20261102 20:47 UTC)
19. <https://arxiv.org/abs/2607.21610> : SCOPE and SCION: benchmark, 24 sources, the authors' caveat (read 20261102 20:47 UTC)
20. arXiv API listings, two title-and-abstract queries for surveys of knowledge graph construction (`export.arxiv.org/api/query`, queries on the words survey, knowledge graph, construction, and on large language models): titles, dates and author counts of the surveys of 2021, 2022, 2023, 2024 and 2025 that it returned (read 20261102 21:00 UTC)
21. <https://arxiv.org/abs/2302.05019> : A Comprehensive Survey on Automatic Knowledge Graph Construction (2023): abstract, more than 300 methods, no mention of language models (read 20261102 21:00 UTC)
22. <https://arxiv.org/abs/2405.16929> : Uncertainty Management in the Construction of Knowledge Graphs: a Survey (2024): abstract, no mention of language models (read 20261102 21:00 UTC)
23. https://export.arxiv.org/api/query : arXiv searches for earlier work before the first version of Language Models are Open KGs (submission date up to 20201021; fields searched: title, abstract, comment): `commonsense` with `knowledge graph`, `language model` and `generate` (8 records, among them COMET 1906.05317 of 20190612, whose abstract says it learns "to generate rich and diverse commonsense descriptions", and COMET-ATOMIC 2020, 2010.05953 of 20201012); `BERT` with `relational knowledge` and `knowledge base` (2 records: Language Models as Knowledge Bases? 1909.01066 of 20190903, and BERTnesia 2010.09313 of 20201019); `pre-trained language models` with `knowledge graph` and `construction` (2 records, COMET and one off-topic); two narrower queries returned 0 or off-topic records (searches read 20261102 22:56 to 23:03 UTC; the abstract of COMET read 23:04 UTC). A search of titles and abstracts, not of full texts, and not exhaustive
