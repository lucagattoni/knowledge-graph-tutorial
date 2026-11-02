# Candidate fundamental papers: the knowledge-graph era (2012 to 2020)

Researcher file for the papers chapter. Written 20261102 20:08 UTC. Area: Google Knowledge Graph, Wikidata,
Knowledge Vault, definitions, KG embeddings, KG completion and refinement surveys, GNNs on KGs, question
answering over KGs, dense retrieval, language models as knowledge bases, property graphs and Cypher, REALM and RAG.

30 candidates, strongest first. Tests: origin (O), turning point (T), widely built on (W), survey of record (S).

## How the numbers were obtained (read this first)

- **Semantic Scholar was not usable.** Every call to the Graph API returned HTTP 429 (single, batch and search/match
  forms; tries at 20261102 19:45, 19:51 and every retry until 20:03; I stopped to avoid hammering). No Semantic
  Scholar count appears below. [5]
- **Citation counts come from OpenAlex** (field `cited_by_count`, read 20261102 19:50) and, as a second named
  source for papers that have a DOI, **Crossref** (`is-referenced-by-count`, read 20261102 19:53 and 20:00). [3][4]
  The two differ by up to 4x and neither is Google Scholar. OpenAlex then refused further calls (HTTP 429, daily
  budget used up, resets at midnight UTC) so no second OpenAlex pass was possible.
- **Preprint versus published record.** OpenAlex keeps the arXiv record and the published record of one paper as
  separate works. Where the record I read is the arXiv one, the count is a floor, marked "arXiv record". For
  ConvE and LAMA the arXiv-record count (30 and 120) is clearly a partial figure; the Crossref count of the published
  version is used instead. Nothing was summed across records.
- Counts are stale by default: they move daily. Cite them with the read time.
- Dates are `YYYYMMDD`. The first-version date of an arXiv paper is the v1 date from the arXiv record [1][2].
  For other papers it is the date the publisher record states (Crossref [4]) or `YYYY` only.
- Authors: first three and the total, from the arXiv record [1] or Crossref [4].
- "Read" says what I actually read. "Full text, keyword-searched" means I extracted the PDF text and read the
  passages around the terms I searched for, not every page.

---

## 1. RAG (2020)

**Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.** Patrick Lewis, Ethan Perez, Aleksandra Piktus et al. (12).
NeurIPS 2020 (arXiv comment: "Accepted at NeurIPS 2020") [1]. First version 20200522. https://arxiv.org/abs/2005.11401
**Citations:** 3048, OpenAlex, arXiv record, read 20261102 19:50 [3]. Crossref has no record for the arXiv DOI.
**Tests:**
- Origin: the abstract introduces "RAG models" that combine a pre-trained seq2seq model (parametric memory) with a dense vector index of Wikipedia (non-parametric memory) read by a neural retriever, and compares two formulations (same passages for the whole output, or different passages per token) [1].
- Widely built on: 3048 citations on the arXiv record alone [3]; the term is the name of the family of methods in the later era (GraphRAG and others, see relations).
**Idea:** A generator is conditioned on passages that a retriever fetches from an external index, and both are fine-tuned end to end, with the retrieved document as a latent variable. It sets the state of the art on three open-domain QA tasks and generates "more specific, diverse and factual" text than a parametric-only baseline [1].
**Relations:**
- Builds on REALM and ORQA: the introduction says "REALM and ORQA, two recently introduced models that combine masked language models with a differentiable retriever, have shown promising results" [16] (see REALM, ORQA).
- Builds on DPR: "RAG's retriever is initialized using DPR's retriever" [16] (see DPR).
- Evaluates on WebQuestions, Natural Questions and CuratedTrec ("strongly outperform ... on open Natural Questions, WebQuestions and CuratedTrec") [16] (see WebQuestions).
- Answered by GraphRAG (2404.16130): its abstract says "RAG fails on global questions directed at an entire text corpus" [2]. Evaluated against graph RAG by 2502.11371, which compares "RAG and GraphRAG on established text-based tasks" [2]. Those two are in the papers chapter of a later era, not this file.
**Read:** abstract and full text, keyword-searched, 20261102 20:02 [1][16]. Sources: [1][2][3][16].

## 2. DPR (2020)

**Dense Passage Retrieval for Open-Domain Question Answering.** Vladimir Karpukhin, Barlas Oğuz, Sewon Min et al. (8).
EMNLP 2020 (arXiv comment) [1]. First version 20200410. https://arxiv.org/abs/2004.04906
**Citations:** 3593, OpenAlex, EMNLP record, read 20261102 19:50 [3]; 2635, Crossref, read 20261102 19:53 [4].
**Tests:**
- Turning point: the abstract reports that a dense dual-encoder retriever "outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy" [1]. The full text says dense retrieval methods "have thus never be shown to outperform TF-IDF/BM25 for open-domain QA before ORQA" [16]; DPR makes the result practical with a small number of labelled pairs.
- Widely built on: 3593 and 2635 citations [3][4]; RAG initialises its retriever from it [16].
**Idea:** Two BERT encoders embed questions and passages into the same space; retrieval is nearest-neighbour search over dense vectors. Training uses question-answer pairs, with no extra pre-training stage [1].
**Relations:**
- Builds on ORQA: the text describes ORQA's inverse cloze task, says it "successfully demonstrates that dense retrieval can outperform BM25", then names two weaknesses of it [16].
- Answers sparse retrieval and DrQA: the baseline is TF-IDF/BM25 as used in DrQA; the pre-processing code "released in DrQA" is reused [16] (see DrQA).
- Evaluates against REALM: its results table lists "Single REALM Wiki (Guu et al., 2020)" beside ORQA and DPR [16] (see REALM).
- Evaluates on WebQuestions and CuratedTREC besides Natural Questions [16].
- Feeds RAG (see RAG).
**Read:** abstract and full text, keyword-searched, 20261102 20:03 [1][16]. Sources: [1][3][4][16].

## 3. TransE (2013)

**Translating Embeddings for Modeling Multi-relational Data.** Antoine Bordes, Nicolas Usunier, Alberto García-Durán et al. (5).
NIPS 2013 (Advances in Neural Information Processing Systems 26) [8]. Date: `2013` (OpenAlex lists 20131205 [3]). https://papers.nips.cc/paper_files/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html
**Citations:** 5724, OpenAlex, record without a DOI, read 20261102 19:50 [3]. Crossref: none (no DOI).
**Tests:**
- Origin: relations are "interpreted as translations operating on the low-dimensional embeddings of the entities"; the line of translation-based KG embedding (TransH, TransR and others) is named after it [8]. The text also introduces the FB15k subset of Freebase (its table lists "FB15k (in millions)") and the Wordnet data used afterwards [8][16]; Rossi et al. say FB15k's "creators [8]" selected Freebase entities, citing this paper [16].
- Widely built on: 5724 citations [3]; later models list it as the base case in their score-function tables (ComplEx, RotatE, ConvE) [16].
**Idea:** Each relation is a translation vector: for a true triple (h, r, t) the embedding h + r should lie near t. The abstract states it outperforms the state of the art at link prediction on two knowledge bases and trains on a graph with about 1M entities, 25k relations and over 17M training samples [8].
**Relations:**
- Builds on Freebase and WordNet as data; its introduction names "Freebase, Google Knowledge Graph or GeneOntology" as the knowledge bases it targets [16] (Foundations era: Freebase, WordNet).
- Answered by DistMult: a plain bilinear model reaches "a top-10 accuracy of 73.2% vs. 54.7% by TransE on Freebase" [1] (see DistMult).
- Answered by TransH, whose abstract says "TransE does not do well in dealing with" one-to-many, many-to-one and many-to-many relations [4] (TransH is in "Considered").
- Evaluated by Kadlec et al. and Rossi et al. as part of the FB15k/WN18 benchmark set (see Kadlec, Rossi).
**Read:** abstract page 20261102 19:52 and full text keyword-searched 20:03 [8][16]. Sources: [3][8][16][1][4].

## 4. Wikidata (2014)

**Wikidata: a free collaborative knowledgebase.** Denny Vrandečić, Markus Krötzsch (2). *Communications of the ACM* (Crossref title "Wikidata") [4]. Date 20140923 (Crossref issue date). https://doi.org/10.1145/2629489
**Citations:** 3366, OpenAlex, read 20261102 19:50 [3]; 2731, Crossref, read 20261102 19:53 [4].
**Tests:**
- Origin: the paper is the reference description of Wikidata, the open collaboratively edited knowledge base behind Wikipedia. Crossref's abstract field gives only the standfirst: "This collaboratively edited knowledgebase provides a common source of data for Wikipedia, and everyone else." [4]
- Widely built on: 3366 and 2731 citations [3][4]; later work names it among the largest KGs that "remain incomplete" (R-GCN abstract, "Yago, DBPedia or Wikidata") [1] and LAMA probes "relations between entities stored in Wikidata" [16].
**Idea:** A single multilingual, community-edited store of structured statements used by the Wikimedia projects. The project's own introduction calls Wikidata "a free, collaborative, multilingual, secondary knowledge base, collecting structured data" [13]. The detailed design (data model, references, rank) is **unstated** here: the full text was not reachable (ACM and CACM pages returned HTTP 403).
**Relations:**
- Used as a data source by LAMA (cloze probes built from Wikidata relations) [16] (see LAMA).
- Named by R-GCN as one of the incomplete graphs link prediction is meant to repair [1] (see R-GCN).
- Launch date 20121029 and the Freebase-to-Wikidata migration are **leads only** (kb-kg/primer/README.md, a tertiary source); not re-verified here.
**Read:** standfirst only (Crossref) 20261102 19:53; project introduction page 19:56 [13]. Full text not read. Sources: [3][4][13][1][16].

## 5. Knowledge Vault (2014)

**Knowledge Vault: A Web-Scale Approach to Probabilistic Knowledge Fusion.** Xin Luna Dong, Evgeniy Gabrilovich, Geremy Heitz et al. (9).
KDD 2014 (20th ACM SIGKDD), New York, pp. 601-610 [7]. Date 20140824 (Crossref [4]). https://doi.org/10.1145/2623330.2623623
**Citations:** 1533, OpenAlex, read 20261102 19:50 [3]; 1080, Crossref, read 20261102 19:53 [4].
**Tests:**
- Origin: the abstract introduces a "Web-scale probabilistic knowledge base" that combines extractions from text, tables, page structure and human annotations with prior knowledge from existing repositories, fused by supervised learning, with "calibrated probabilities of fact correctness" [3][7].
- Widely built on: 1533 and 1080 citations [3][4].
**Idea:** Instead of curating facts, run many extractors over the web, combine them with priors from existing KBs, and output a probability per triple. The authors say it is "substantially bigger than any previously published structured knowledge repository" (first-party claim) [3].
**Relations:**
- Builds on Wikipedia, Freebase, YAGO, Microsoft's Satori and Google's Knowledge Graph, named in the first sentence of the abstract as the large-scale KBs it wants to outgrow [3].
- Discussed by the Nickel et al. review: "we also discuss Google's knowledge vault project as an example of such combination" of statistical models and text extraction [1] (see Nickel review).
- Criticised by Ehrlinger and Wöß: Knowledge Vault "cannot be classified as a true knowledge base" because it adds reasoning to a store [10] (see Ehrlinger).
**Read:** abstract (OpenAlex and Google Research page) 20261102 19:52 and 19:54; full text not read. Sources: [3][4][7][1][10].

## 6. Introducing the Knowledge Graph (2012)

**Introducing the Knowledge Graph: things, not strings.** Amit Singhal (1). Google blog (Official Google Blog), 20120516. https://blog.google/products/search/introducing-knowledge-graph-things-not/
**Citations:** not a paper; no count from Semantic Scholar or OpenAlex (not queried: S2 blocked, OA budget gone). Second-hand: Ehrlinger and Wöß write that it "has been cited more than 100 times according to Google Scholar" at their August 2016 check [10]. That figure is old and second-hand.
**Tests:**
- Origin: names and launches the industrial KG. Ehrlinger and Wöß: the term's "popularity is clearly influenced by the introduction of Google's Knowledge Graph in 2012" [10]. The post states the graph "understands real-world entities and their relationships to one another: things, not strings" [6].
- Widely built on: second-hand only (above). Weak evidence; the paper is cited as if it defined the term, which they regard as a problem [10].
**Idea:** A search engine answering about entities, not keywords. At launch the graph held "more than 500 million objects" and more than 3.5 billion facts and relationships (first-party figures) and is "rooted in public sources such as Freebase, Wikipedia and the CIA World Factbook" [6]. The post gives no storage, algorithm or architecture details [6].
**Relations:**
- Builds on Freebase and Wikipedia as sources [6] (Foundations era: Freebase).
- Criticised by Ehrlinger and Wöß: two issues, "(a) Google's blog entry ... is cited as if it provides a proper explanation for constituting a knowledge graph" and (b) KG and KB used interchangeably [10] (see Ehrlinger).
- Named by Knowledge Vault's abstract and TransE's introduction as the reference large-scale KB [3][16].
**Read:** the post through a fetch tool answering targeted questions, 20261102 19:52 and 20:04; not read end to end. Sources: [6][10][3][16].

## 7. REALM (2020)

**REALM: Retrieval-Augmented Language Model Pre-Training.** Kelvin Guu, Kenton Lee, Zora Tung et al. (5). Venue: none stated in the arXiv record [1]. First version 20200210. https://arxiv.org/abs/2002.08909
**Citations:** 540, OpenAlex, arXiv record (floor), read 20261102 19:50 [3].
**Tests:**
- Origin: the abstract claims that "for the first time" a knowledge retriever is pre-trained "in an unsupervised manner", with masked language modelling as the learning signal and backpropagation through a retrieval step over millions of documents [1].
- Widely built on: RAG and DPR both cite it and compare against it in results tables [16]; count 540 is a floor.
**Idea:** A language model retrieves and attends over Wikipedia documents during pre-training, fine-tuning and inference, instead of storing knowledge only in its weights. It beats prior methods on three open-domain QA benchmarks by 4 to 16 points of absolute accuracy (first-party result) [1].
**Relations:**
- Builds on LAMA's observation: the introduction begins from the finding that models capture world knowledge, citing "Petroni et al., 2019" [16] (see LAMA).
- Builds on ORQA: "ORQA formulates Open-QA using a similar latent variable model" and the retrievers of both are initialised with the Inverse Cloze Task [16] (see ORQA).
- Answered by RAG: "Unlike REALM and T5+SSM, RAG enjoys strong results without expensive, specialized 'salient span masking' pre-training" [16] (see RAG).
- Evaluated by DPR in a head-to-head table [16].
- Evaluates on Natural Questions-Open, WebQuestions and CuratedTrec [16] (see WebQuestions).
**Read:** abstract and full text keyword-searched, 20261102 20:02 [1][16]. Sources: [1][3][16].

## 8. ORQA (2019)

**Latent Retrieval for Weakly Supervised Open Domain Question Answering.** Kenton Lee, Ming-Wei Chang, Kristina Toutanova (3). ACL 2019 (arXiv comment) [1]. First version 20190601. https://arxiv.org/abs/1906.00300
**Citations:** 771, OpenAlex, ACL record, read 20261102 19:50 [3].
**Tests:**
- Origin: the abstract shows "for the first time" that one can "jointly learn the retriever and reader from question-answer string pairs and without any IR system", with evidence retrieval from all of Wikipedia as a latent variable and an Inverse Cloze Task for pre-training [1].
- Turning point: DPR's text says dense retrieval had never been shown to beat BM25 for open-domain QA "before ORQA" [16]; the abstract reports learned retrieval "outperforming BM25 by up to 19 points in exact match" on user-seeking datasets, while BM25 suffices where the questioner already knows the answer [1].
**Idea:** Retriever and reader are trained together from answer strings only; the retriever is warmed up with the Inverse Cloze Task [1].
**Relations:**
- Answers DrQA-style pipelines that use a black-box IR system (the abstract calls strong supervision and a black-box IR system "suboptimal") [1] (see DrQA).
- Built on by REALM (similar latent-variable model, same ICT initialisation), DPR (names two weaknesses) and RAG (cites it with REALM) [16].
**Read:** abstract; the later papers' discussion of it from full text, 20261102 20:02 [1][16]. ORQA's own full text not read. Sources: [1][3][16].

## 9. LAMA, "Language Models as Knowledge Bases?" (2019)

**Language Models as Knowledge Bases?** Fabio Petroni, Tim Rocktäschel, Patrick Lewis et al. (7). EMNLP 2019 (arXiv comment: "accepted at EMNLP 2019") [1]. First version 20190903. https://arxiv.org/abs/1909.01066
**Citations:** 953, Crossref, EMNLP-IJCNLP record, read 20261102 20:00 [4]. OpenAlex arXiv record: 120 (floor), read 19:50 [3].
**Tests:**
- Origin: it defines the LAMA probe: a pretrained LM "knows" a fact (subject, relation, object) if it predicts the masked object in a cloze sentence, over facts from Wikidata, ConceptNet and SQuAD [16].
- Turning point: it opened the dispute between parametric and explicit knowledge. Findings: BERT without fine-tuning holds relational knowledge "competitive with traditional NLP methods that have some access to oracle knowledge", and BERT-large reaches 57.1% precision@10 on open-domain QA against 63.5% for a knowledge base built by a supervised relation extraction system [1][16].
**Idea:** Probe pretrained language models for facts with fill-in-the-blank queries. The abstract lists LM advantages over structured KBs: "no schema engineering", an open class of relations, easy extension, no supervision [1].
**Relations:**
- Probes Wikidata and ConceptNet relations [16] (see Wikidata).
- Motivates REALM, which cites it in its first paragraph [16], and RAG, whose abstract begins from LMs storing "factual knowledge in their parameters" [1]; whether RAG cites LAMA at that point is unstated (its reference list contains Petroni et al. entries) [16].
- Followed by Roberts et al. 2020, "How Much Knowledge Can You Pack Into the Parameters of a Language Model?", whose abstract opens "It has recently been observed that neural language models ... can implicitly store and retrieve knowledge using natural language queries" [1] (in "Considered").
**Read:** abstract and full text keyword-searched, 20261102 20:02 [1][16]. Sources: [1][3][4][16].

## 10. Hogan et al., "Knowledge Graphs" (2020)

**Knowledge Graphs.** Aidan Hogan, Eva Blomqvist, Michael Cochez et al. (18). *ACM Computing Surveys* 54(4), 2021 (arXiv journal reference) [1]. First version 20200304 (arXiv v1; v6 later). https://arxiv.org/abs/2003.02320
**Citations:** 2144, OpenAlex, CSUR record, read 20261102 19:50 [3]; 1950, Crossref, read 20:00 [4].
**Tests:**
- Survey of record: the abstract covers graph data models and query languages, "the roles of schema, identity, and context", deductive and inductive knowledge, creation, enrichment, quality assessment, refinement and publication, and prominent open and enterprise KGs [1].
**Idea:** A single introduction to KGs spanning data models (including property graphs), query languages, schema, reasoning, learning and publication [1].
**Relations:**
- Covers the same ground as the refinement survey (Paulheim), the embedding surveys (Wang, Nickel, Ji) and the industry comparison (Noy) at textbook length; the exact citations are **unstated** (survey body not read).
- Leads (kb-kg/primer/README.md, not re-verified): Hogan et al. summarise the Noy et al. trends and build on Ehrlinger and Wöß.
**Read:** abstract only, 20261102 19:52 [1]. Sources: [1][3][4].

## 11. Wang et al., KG embedding survey (2017)

**Knowledge Graph Embedding: A Survey of Approaches and Applications.** Quan Wang, Zhendong Mao, Bin Wang et al. (4). *IEEE Transactions on Knowledge and Data Engineering* [4]. Date 20171201 (Crossref issue; OpenAlex online date 20170920 [3]). https://doi.org/10.1109/TKDE.2017.2754499
**Citations:** 2642, OpenAlex, read 20261102 19:50 [3]; 2192, Crossref, read 19:53 [4].
**Tests:** survey of record for KG embeddings. The abstract reviews techniques that use "only facts observed in the KG" and techniques that add entity types, relation paths, textual descriptions and logical rules, then applications in completion, relation extraction and QA [3].
**Idea:** A taxonomy of embedding models by the information they use, with training procedures and pros and cons [3].
**Relations:** surveys the line begun by TransE and continued by TransH/TransR, DistMult and ComplEx; the abstract names no papers, so which ones it covers is **unstated** (body not read). Preceded by the Nickel et al. review, followed by the Ji et al. survey (dates).
**Read:** abstract only (OpenAlex) 20261102 19:54 [3]. Sources: [3][4].

## 12. Nickel et al., relational machine learning review (2016)

**A Review of Relational Machine Learning for Knowledge Graphs.** Maximilian Nickel, Kevin Murphy, Volker Tresp et al. (4). *Proceedings of the IEEE*, January 2016 (arXiv comment: "To appear in Proceedings of the IEEE") [1][4]. First version 20150302. https://arxiv.org/abs/1503.00759
**Citations:** 1672, OpenAlex, read 20261102 19:50 [3]; 1143, Crossref, read 19:53 [4].
**Tests:** survey of record for statistical models on KGs: "latent feature models such as tensor factorization and multiway neural networks" versus "mining observable patterns in the graph", plus a combination [1].
**Idea:** Frames link prediction on KGs as relational learning, contrasts latent-feature with observable-pattern models, and shows how both connect to text extraction [1].
**Relations:** discusses Knowledge Vault as the example of combining statistical models with extraction ("we also discuss Google's knowledge vault project") [1] (see Knowledge Vault). Covers the RESCAL tensor-factorisation line (abstract: tensor factorization; RESCAL not named there). Its author co-wrote HolE and RESCAL.
**Read:** abstract 20261102 19:52 [1]. Sources: [1][3][4].

## 13. Ji et al., KG survey (2021)

**A Survey on Knowledge Graphs: Representation, Acquisition and Applications.** Shaoxiong Ji, Shirui Pan, Erik Cambria et al. (5). *IEEE Transactions on Neural Networks and Learning Systems* 2021 (arXiv journal reference) [1]. First version 20200202. https://arxiv.org/abs/2002.00388
**Citations:** 2956, OpenAlex, read 20261102 19:50 [3]; 2410, Crossref, read 20:00 [4].
**Tests:** survey of record. Four topics: representation learning, "knowledge acquisition and completion", temporal KGs, knowledge-aware applications; embeddings organised "from four aspects of representation space, scoring function, encoding models, and auxiliary information"; plus datasets and open-source libraries [1].
**Idea:** A full-view taxonomy of KG research as of early 2020 [1].
**Relations:** extends the embedding survey of Wang et al. with temporal KGs and meta-relational learning (the abstract lists "meta relational learning, commonsense reasoning, and temporal knowledge graphs" as emerging topics) [1]. Overlaps with Hogan et al. (same year, different emphasis: Hogan covers data models and publication).
**Read:** abstract 20261102 19:52 [1]. Sources: [1][3][4].

## 14. Paulheim, KG refinement survey (2017)

**Knowledge graph refinement: A survey of approaches and evaluation methods.** Heiko Paulheim (1). *Semantic Web* journal [4]. Date 20161206 (Crossref online). https://doi.org/10.3233/SW-160218
**Citations:** 1210, OpenAlex, read 20261102 19:50 [3]; 845, Crossref, read 19:53 [4].
**Tests:**
- Survey of record for refinement: completion (adding missing knowledge) and error detection (flagging wrong facts), with the evaluation methods used [11].
- Widely built on, as a definition: Ehrlinger and Wöß's Table 1 starts with Paulheim's four-point definition (real-world entities and their interrelations in a graph; classes and relations in a schema; arbitrary interrelations; various topical domains) [10]. On the journal's open review page reviewer Natasha Noy called the definition "still a bit vague" [11].
**Idea:** Classifies refinement methods and how they are evaluated, over open and commercial KGs. The abstract says Google "coined the term 'Knowledge Graph' in 2012" [3][11].
**Relations:** the definition is criticised by Ehrlinger and Wöß (restricts the term to "any graph-based knowledge representation") [10]. Names DBpedia, YAGO and Freebase among open KGs [3].
**Read:** abstract and review page 20261102 19:54 and 19:55; full text not read. Sources: [3][4][10][11].

## 15. DistMult (2014)

**Embedding Entities and Relations for Learning and Inference in Knowledge Bases.** Bishan Yang, Wen-tau Yih, Xiaodong He et al. (5). Venue: none stated in the arXiv record (comment: "12 pages, 4 figures") [1]. First version 20141220. https://arxiv.org/abs/1412.6575
**Citations:** 2250, OpenAlex, arXiv record (floor), read 20261102 19:50 [3].
**Tests:**
- Turning point: shows that most models, "including NTN and TransE", fit one framework and that "a simple bilinear formulation achieves new state-of-the-art results", with "a top-10 accuracy of 73.2% vs. 54.7% by TransE on Freebase" [1]. Kadlec et al. later show a tuned DistMult beats almost all later models (see Kadlec).
- Widely built on: it is the base case in ConvE, ComplEx, RotatE and R-GCN [16].
**Idea:** Entities are vectors, relations are diagonal bilinear maps; the same relation embeddings can be used to mine Horn rules such as BornInCity(a,b) and CityInCountry(b,c) imply Nationality(a,c) [1].
**Relations:**
- Answers TransE and NTN (abstract) (see TransE).
- Extended by ComplEx (symmetry problem) and by R-GCN (encoder added: "factorization models ... such as DistMult can be significantly improved") [1][16].
- Re-evaluated by Kadlec et al. [1] and Rossi et al. [16].
**Read:** abstract and full text keyword-searched, 20261102 20:03 [1][16]. Sources: [1][3][16].

## 16. ComplEx (2016)

**Complex Embeddings for Simple Link Prediction.** Théo Trouillon, Johannes Welbl, Sebastian Riedel et al. (5). ICML 2016 (arXiv comment) [1]. First version 20160620. https://arxiv.org/abs/1606.06357
**Citations:** 2098, OpenAlex, arXiv record (floor), read 20261102 19:50 [3].
**Tests:** widely built on. It is a standard baseline (RotatE's table lists "ComplEx (Trouillon et al., 2016)" beside TransE, DistMult and HolE; ConvE and Rossi et al. also cover it) [16].
**Idea:** Use complex-valued embeddings and the Hermitian dot product so one linear-time model handles symmetric and antisymmetric relations; "arguably simpler" than the Neural Tensor Network and HolE and outperforming them on standard benchmarks (first-party) [1].
**Relations:**
- Builds on DistMult: its text explains that the real-valued bilinear score "is not symmetric any more" once complex numbers are used; its table lists RESCAL, TransE, DistMult and HolE as the compared scoring functions [16].
- Answered by RotatE, which also models symmetry and antisymmetry (rotation in complex space) [1].
**Read:** abstract and full text keyword-searched, 20261102 20:03 [1][16]. Sources: [1][3][16].

## 17. R-GCN (2017)

**Modeling Relational Data with Graph Convolutional Networks.** Michael Schlichtkrull, Thomas N. Kipf, Peter Bloem et al. (6). Published in *Lecture Notes in Computer Science* (*The Semantic Web*) 2018 [4]. First version 20170317. https://arxiv.org/abs/1703.06103
**Citations:** 5677, OpenAlex, publisher record, read 20261102 19:50 [3]; 3740, Crossref, read 20:00 [4].
**Tests:**
- Origin: "We introduce Relational Graph Convolutional Networks (R-GCNs) and apply them to two standard knowledge base completion tasks: Link prediction ... and entity classification" [1]. It is the first widely used GNN built for multi-relational KGs.
- Widely built on: 5677 and 3740 citations [3][4]; GRAFT-Net and ConvE compare with or build on it [16].
**Idea:** Message passing with relation-specific weights over a KG, used as an encoder in front of a factorisation decoder. Result: DistMult plus an R-GCN encoder gains 29.8% on FB15k-237 over the decoder-only model (first-party) [1].
**Relations:**
- Builds on Kipf and Welling's GCN: the text applies "similar to Kipf and Welling" local-neighbourhood operators to large-scale relational data [16]. The GCN paper is in "Considered".
- Builds on DistMult and evaluates on FB15k-237 (Toutanova and Chen 2015) [1][16].
- Evaluated by ConvE, which reports equal performance with "17x fewer parameters" than R-GCN [1].
- Built on by GRAFT-Net, which cites "Schlichtkrull et al., 2017" for graph representation learning over KB subgraphs [16].
**Read:** abstract and full text keyword-searched, 20261102 20:03 [1][16]. Sources: [1][3][4][16].

## 18. ConvE (2018)

**Convolutional 2D Knowledge Graph Embeddings.** Tim Dettmers, Pasquale Minervini, Pontus Stenetorp et al. (4). AAAI 2018 (arXiv comment: "Extended AAAI2018 paper") [1]. First version 20170705. https://arxiv.org/abs/1707.01476
**Citations:** 1959, Crossref, AAAI record, read 20261102 20:00 [4]. OpenAlex arXiv record: 30 (partial, not used), read 19:50 [3].
**Tests:**
- Turning point: it quantifies test-set leakage through inverse relations in WN18 and FB15k: "a simple rule-based model can achieve state-of-the-art results on both WN18 and FB15k", and derives robust dataset variants [1].
- Widely built on: 1959 citations [4]; a standard baseline in later tables [16].
**Idea:** A multi-layer 2D convolution over reshaped, stacked entity and relation embeddings; it matches DistMult and R-GCN with 8x and 17x fewer parameters (first-party) [1].
**Relations:**
- Builds on Toutanova and Chen: "It was first noted by Toutanova and Chen (2015) that WN18 and FB15k suffer from test leakage ... they did not explicitly investigate the severity of this problem" [16] (see FB15k-237).
- Evaluates TransE, DistMult, ComplEx, R-GCN and HolE as baselines [16] (see those entries).
- Companion to Kadlec et al.: both argue reported gains were partly an artefact of evaluation [1].
**Read:** abstract and full text keyword-searched, 20261102 20:03 [1][16]. Sources: [1][4][16][3].

## 19. Kadlec et al., "Baselines Strike Back" (2017)

**Knowledge Base Completion: Baselines Strike Back.** Rudolf Kadlec, Ondrej Bajgar, Jan Kleindienst (3). 2nd Workshop on Representation Learning for NLP (RepL4NLP) 2017 [4]. First version 20170530. https://arxiv.org/abs/1705.10744
**Citations:** 173, OpenAlex, read 20261102 19:50 [3]; 61, Crossref, read 20:00 [4]. Low; the argument matters more than the count.
**Tests:**
- Turning point, independent evaluation: the accuracy of almost all models published on FB15k "can be outperformed by an appropriately tuned baseline" (a reimplementation of DistMult), casting "doubt on the claim that the performance improvements of recent models are due to architectural changes as opposed to hyper-parameter tuning or different training objectives" [1]. The text counts 27 of 29 published models beaten on Hits@10 [16].
**Idea:** Retune DistMult (softmax likelihood instead of an L1 max-margin loss, and hyper-parameters) and report it against published results [16].
**Relations:**
- Evaluates DistMult against the field's later models (see DistMult).
- Cited by Rossi et al.: "it has been demonstrated by Kadlec et al. that, when carefully tuned, DistMult can still reach state-of-the-art performance" [16].
**Read:** abstract and full text keyword-searched, 20261102 20:03 [1][16]. Sources: [1][3][4][16].

## 20. RotatE (2019)

**RotatE: Knowledge Graph Embedding by Relational Rotation in Complex Space.** Zhiqing Sun, Zhi-Hong Deng, Jian-Yun Nie et al. (4). ICLR 2019 (arXiv comment) [1]. First version 20190226. https://arxiv.org/abs/1902.10197
**Citations:** 1414, OpenAlex, arXiv record (floor), read 20261102 19:50 [3].
**Tests:** widely built on. It is one of the 16 methods in the Rossi et al. comparison and a standard baseline after 2019 [16].
**Idea:** Each relation is a rotation from head to target entity in complex space, so symmetry, antisymmetry, inversion and composition are all modelled; adds self-adversarial negative sampling [1].
**Relations:**
- Answers TransE, DistMult, ComplEx, HolE: its score-function table lists these four as the prior models [16].
- Evaluated by Rossi et al. (list of 16 methods includes "RotatE") [16].
**Read:** abstract and full text keyword-searched, 20261102 20:03 [1][16]. Sources: [1][3][16].

## 21. FB15k-237, "Observed versus latent features" (2015)

**Observed versus latent features for knowledge base and text inference.** Kristina Toutanova, Danqi Chen (2). 3rd Workshop on Continuous Vector Space Models and their Compositionality, 2015 [4]. Date: `2015` (month unstated). https://doi.org/10.18653/v1/w15-4007
**Citations:** 1071, OpenAlex, read 20261102 19:50 [3]; 719, Crossref, read 19:53 [4].
**Tests:**
- Origin: ConvE's text says "Toutanova and Chen (2015) introduced FB15k-237 - a subset of FB15k where inverse relations are removed" [16].
- Turning point: the abstract shows "the surprising effectiveness of a simple observed features model in comparison to latent feature models" on FB15K and WN18 [3].
- Widely built on: FB15k-237 is the dataset R-GCN's headline gain is reported on [1].
**Idea:** Compare observed-feature and latent-feature models for KB completion, and build a harder dataset coupled with textual mentions [3].
**Relations:**
- Evaluates FB15k and WN18, the datasets of TransE [3][16].
- Built on by ConvE (quantifies the leakage) and R-GCN (evaluation on FB15k-237) [1][16].
**Read:** abstract (OpenAlex) 20261102 19:54; full text not read. Sources: [3][4][1][16].

## 22. WebQuestions (2013)

**Semantic Parsing on Freebase from Question-Answer Pairs.** Jonathan Berant, Andrew Chou, Roy Frostig et al. (4). EMNLP 2013, Seattle, pp. 1533-1544 [9]. Date: October 2013 [9]. https://aclanthology.org/D13-1160/
**Citations:** 1582, OpenAlex, read 20261102 19:50 [3]; 373, Crossref, read 19:53 [4].
**Tests:**
- Origin: trains a semantic parser that scales to Freebase from question-answer pairs, with no annotated logical forms, and "collected a more realistic and challenging dataset of question-answer pairs" (WebQuestions) [3].
- Widely built on: REALM, DPR and RAG all evaluate on WebQuestions [16]; STAGG reports its headline score on it [15].
**Idea:** Learn a mapping from phrases to Freebase predicates from a KB and a large text corpus, and add a bridging operation to generate extra predicates [3].
**Relations:**
- Answered by STAGG (F1 52.5% on WebQuestions "outperforms previous methods substantially") [15] and WebQSP (parse labels add 5 points) [3] (see both).
- Evaluated by REALM, DPR and RAG, which carry it from KG question answering into open-domain text retrieval [16].
**Read:** ACL Anthology metadata page 20261102 19:53 (no abstract there) and abstract via OpenAlex 19:54. Full text not read. Sources: [3][4][9][15][16].

## 23. DrQA (2017)

**Reading Wikipedia to Answer Open-Domain Questions.** Danqi Chen, Adam Fisch, Jason Weston et al. (4). ACL 2017 (arXiv comment) [1]. First version 20170331. https://arxiv.org/abs/1704.00051
**Citations:** 1545, OpenAlex, read 20261102 19:50 [3]; 726, Crossref, read 19:53 [4].
**Tests:**
- Origin: proposes "open-domain question answering using Wikipedia as the unique knowledge source" and names it "machine reading at scale": document retrieval (bigram hashing and TF-IDF) plus a recurrent reader [1].
- Widely built on: DPR reuses its Wikipedia pre-processing code and its answer-matching normalisation; REALM and DPR cite it for the retrieve-and-read setup [16].
**Idea:** Retrieve with TF-IDF, read with a multi-layer RNN, train on several QA datasets with distant supervision [1].
**Relations:**
- Answered by ORQA and DPR, which replace its sparse retriever [16] (see ORQA, DPR).
- Evaluates on WebQuestions among others (text lists SQuAD, TREC, WebQuestions, WikiMovies) [16] (see WebQuestions).
**Read:** abstract and full text keyword-searched, 20261102 20:03 [1][16]. Sources: [1][3][4][16].

## 24. STAGG (2015)

**Semantic Parsing via Staged Query Graph Generation: Question Answering with Knowledge Base.** Wen-tau Yih, Ming-Wei Chang, Xiaodong He et al. (4). ACL 2015, Beijing, 26-31 July, pp. 1321-1331 [15]. https://doi.org/10.3115/v1/p15-1128 (also https://aclanthology.org/P15-1128/)
**Citations:** 768, OpenAlex, read 20261102 19:50 [3]; 363, Crossref, read 19:53 [4].
**Tests:**
- Turning point: "our system outperforms previous methods substantially, and achieves an F1 measure of 52.5% on the WEBQUESTIONS dataset" [15] (first-party result).
- Widely built on: 768 and 363 citations [3][4]. Later KBQA work that builds on it was not read.
**Idea:** Define a query graph that "resembles subgraphs of the knowledge base" and maps directly to a logical form; semantic parsing becomes staged query-graph generation that uses the KB early to prune the search space, with entity linking and a CNN matching questions to predicate sequences [15].
**Relations:**
- Builds on Berant et al.: evaluates on WebQuestions "(Berant et al., 2013)" [15] (see WebQuestions).
- Followed by WebQSP, from the same group [4] (see WebQSP).
**Read:** abstract and introduction from the PDF, 20261102 20:01 [15]. Sources: [3][4][15].

## 25. WebQSP (2016)

**The Value of Semantic Parse Labeling for Knowledge Base Question Answering.** Wen-tau Yih, Matthew Richardson, Chris Meek et al. (5). ACL 2016 (short papers) [4]. Date: `2016`. https://doi.org/10.18653/v1/p16-2033
**Citations:** 492, OpenAlex, read 20261102 19:50 [3]; 285, Crossref, read 19:53 [4].
**Tests:**
- Origin: it released "the largest semantic-parse labeled dataset to date" (WebQuestionsSP) [3].
- Widely built on: GRAFT-Net evaluates on "WebQuestionsSP (Yih ...)" [16].
- Turning point (modest): learning from labelled semantic parses gives "an absolute 5 point gain compared to learning from answers", at comparable annotation cost [3].
**Idea:** Collect parse labels for WebQuestions through a suitable interface rather than answers only [3].
**Relations:**
- Related to WebQuestions and STAGG: the dataset is named WebQuestionsSP by GRAFT-Net [16], and STAGG has the same first author [15]; that it re-annotates WebQuestions is not stated in the abstract read (**unstated**).
- Used by GRAFT-Net (text plus KB QA) [16].
**Read:** abstract (OpenAlex) 20261102 19:54. Full text not read. Sources: [3][4][15][16].

## 26. Ehrlinger and Wöß, "Towards a Definition of Knowledge Graphs" (2016)

**Towards a Definition of Knowledge Graphs.** Lisa Ehrlinger, Wolfram Wöß (2). SEMANTiCS 2016 Posters and Demos, Leipzig, 13-14 September 2016 (CEUR-WS Vol-1695) [10]. https://ceur-ws.org/Vol-1695/paper4.pdf
**Citations:** 497, OpenAlex (record without DOI), read 20261102 19:50 [3]. Crossref: none.
**Tests:** widely built on, as the definition others reply to; the only test passed, and a weaker one than the entries above. It is a four-page poster. Evidence of use beyond the count: the kb-kg primer lead says Hogan et al. build on it (not re-verified).
**Idea:** Table 1 lists five definitions (Paulheim; the Journal of Web Semantics; the Semantic Web Company; Färber et al.: a KG "as an RDF graph"; Pujara et al.) and shows "the lack of a common core". It proposes: "A knowledge graph acquires and integrates information into an ontology and applies a reasoner to derive new knowledge." [10] It also records that the term "knowledge graph" was used in the 1980s by researchers at Groningen and Twente for a natural-language system [10].
**Relations:**
- Answers Paulheim's definition (as too broad: "any graph-based knowledge representation") and the Google blog (cited as if it defined the term) [10] (see both).
- Applies its definition to Knowledge Vault: not a true KB [10] (see Knowledge Vault).
- Connects to the Foundations era via the 1980s use of the term [10].
**Read:** full text (4 pages) via PDF extraction 20261102 19:54 [10]. Sources: [3][10].

## 27. Rossi et al., KG embedding comparative analysis (2020)

**Knowledge Graph Embedding for Link Prediction: A Comparative Analysis.** Andrea Rossi, Donatella Firmani, Antonio Matinata et al. (5). *ACM Transactions on Knowledge Discovery from Data* 2021 (arXiv comment) [1]. First version 20200203. https://arxiv.org/abs/2002.00819
**Citations:** 608, OpenAlex, TKDD record, read 20261102 19:50 [3]; 485, Crossref, read 20:00 [4].
**Tests:**
- Turning point, independent evaluation: it compares "effectiveness and efficiency of 16 state-of-the-art methods", adds "a rule-based baseline", and objects that the usual practice of aggregating accuracy over test facts lets methods succeed by "attending to structural properties" of over-represented entities [1].
**Idea:** A standardised comparison of embedding models and design choices on the common benchmarks, with per-relation and per-entity analysis [1].
**Relations:**
- Evaluates TransE, HolE, RotatE, ConvE and others (its list of methods) [16].
- Builds on Kadlec et al. and ConvE's leakage finding (cites both; FB15k-237 "was built" after the leakage observation) [16].
**Read:** abstract and full text keyword-searched, 20261102 20:03 [1][16]. Sources: [1][3][4][16].

## 28. Cypher (2018)

**Cypher: An Evolving Query Language for Property Graphs.** Nadime Francis, Alastair Green, Paolo Guagliardo et al. (10). SIGMOD 2018 (Crossref title "Cypher") [4]. Date 20180527. https://doi.org/10.1145/3183713.3190657
**Citations:** 549, OpenAlex, read 20261102 19:50 [3]; 514, Crossref, read 19:53 [4].
**Tests:**
- Origin: a formal semantic definition of Cypher 9, "the first version of the language governed by the openCypher Implementers Group", covering "its variant of the property graph data model" and ASCII-art pattern matching [3].
- Widely built on: 549 and 514 citations; the Angles et al. survey treats Cypher as one of three representative languages [4][3].
**Idea:** Cypher began in the Neo4j database and is "currently used by several commercial database products"; the paper gives its formal read-query semantics and previews Cypher 10 (compositional, graph projections, multiple named graphs) [3].
**Relations:**
- Compared with other property graph query languages in the paper itself [3].
- Surveyed by Angles et al. next to SPARQL and Gremlin [4] (see Angles).
- Standardisation by GQL after 2018 is **unstated** here (no source read).
**Read:** abstract (OpenAlex) 20261102 19:54. Full text not read. Sources: [3][4].

## 29. Angles et al., query languages for graph databases (2017)

**Foundations of Modern Query Languages for Graph Databases.** Renzo Angles, Marcelo Arenas, Pablo Barceló et al. (6). *ACM Computing Surveys* [4]. Date 20170926. https://doi.org/10.1145/3104031
**Citations:** 395, OpenAlex, read 20261102 19:50 [3]; 294, Crossref, read 19:53 [4].
**Tests:** survey of record for graph query languages. It discusses two graph data models, "edge-labelled graphs" and "property graphs", the two fundamental functionalities (graph patterns and navigational expressions), semantics and complexity, with examples from "SPARQL, Cypher, and Gremlin" [4].
**Idea:** A formal map of what graph query languages share and where they differ [4].
**Relations:** covers the RDF side (SPARQL) and the property-graph side (Cypher, Gremlin); Cypher's formalisation (Francis et al., SIGMOD 2018) appeared after it. Which papers it cites for Cypher is **unstated**.
**Read:** abstract (Crossref) 20261102 19:53. Sources: [3][4].

## 30. Noy et al., industry-scale knowledge graphs (2019)

**Industry-scale Knowledge Graphs: Lessons and Challenges.** Natasha Noy, Yuqing Gao, Anshu Jain et al. (6). *Communications of the ACM* 62(8), pp. 36-43 [12]. Date 20190724 (Crossref). https://doi.org/10.1145/3331166
**Citations:** 363, OpenAlex, read 20261102 19:50 [3]; 271, Crossref, read 19:53 [4].
**Tests:** survey of record for deployed KGs. It compares knowledge graphs at five companies: Microsoft (Bing), Google, Facebook, eBay and IBM (Knowledge Graph Framework for Watson Discovery), and identifies challenges that knowledge-driven enterprises commonly face (paraphrase of the record); it expands a panel at ISWC, Asilomar, October 2018 [12]. Weakest of the survey candidates: the count is the lowest on this list.
**Idea:** Lessons from running KGs at scale, with similarities and differences across the five [12].
**Relations:** the Google KG it describes is the one announced in 2012 (see Google blog). The kb-kg primer lead says Hogan et al. summarise its common trends (not re-verified).
**Read:** Google Research record with abstract 20261102 19:55; full text not read. Sources: [3][4][12].

---

## Considered and not proposed

| Paper | Why not |
|---|---|
| TransH, Wang et al. AAAI 2014 (OpenAlex 3914, Crossref 2432, read 19:50 and 19:53) | A widely cited increment on TransE; its abstract is the evidence that TransE fails on 1-to-N relations. Cite in TransE's text; one group page does not need both. |
| TransR, Lin et al. AAAI 2015 (OpenAlex 3749, Crossref 2260) | Same: incremental on TransE and TransH. Candidate for further reading. |
| RESCAL, Nickel et al. ICML 2011 (OpenAlex 1783) | Origin of the tensor-factorisation line, but dated 2011, before the era; full abstract read [14], no citation from a source of record besides the count. Better placed in the Foundations group if the owner wants it. |
| Neural Tensor Network, Socher et al. NIPS 2013 (OpenAlex 1656) | Contemporary of TransE; DistMult shows it can be generalised and beaten. Abstract not read. Further reading. |
| HolE, Nickel et al. AAAI 2016 (OpenAlex 559, Crossref 623) | Abstract read: compositional circular-correlation embeddings; superseded by ComplEx, which shows equivalence-level simplicity. Further reading. |
| GCN, Kipf and Welling 2017 (OpenAlex 23981) | Hugely cited but a general graph-learning paper, not a KG paper (its abstract mentions "a knowledge graph dataset"); belongs to a graph-ML area, and R-GCN carries the KG relation. |
| GRAFT-Net, Sun et al. EMNLP 2018 (OpenAlex 492) | Text plus KB QA on a question subgraph; useful relation, below the bar for a fundamental paper. |
| SimpleQuestions, Bordes et al. 2015 (OpenAlex 528) | Introduces a 100k-question dataset; fits the datasets chapter, not papers. |
| ComplexWebQuestions, Talmor and Berant NAACL 2018 (OpenAlex 520, Crossref 275) | Successor of WebQuestions with question decomposition; a dataset page candidate. |
| FiD, Izacard and Grave 2021 (OpenAlex 1092) | Important RAG-era reader; abstract read, but it builds on DPR/RAG rather than starting a line. Further reading. |
| kNN-LM, Khandelwal et al. 2020 (OpenAlex 285) | Retrieval-augmented language modelling by interpolation; adjacent, not on the main line. |
| Roberts et al., "How Much Knowledge Can You Pack..." 2020 (OpenAlex 639) | Closed-book QA with T5; a follow-up to LAMA. Further reading. |
| KG-BERT, Yao et al. 2019 (OpenAlex 412) | Pretrained LM for KG completion; early but not field-changing on the evidence read. |
| DeepPath (OpenAlex 862), MINERVA (431), Neural LP (410) | Path-based reasoning and rule learning in KGs; abstracts read, each a good further-reading line, none passes a test on the evidence gathered. |
| Never-Ending Learning (NELL), Mitchell et al. CACM 2018 (OpenAlex 508, Crossref 426) | Abstract read (120M beliefs, learning since January 2010). Strong, but the system dates from 2010; belongs to the pre-2012 group or to extraction. |
| Core techniques of QA over KBs, Diefenbach et al. 2018 (OpenAlex 349, Crossref 250) | A QA-over-KB survey; abstract not read, so no case made. |
| The Property Graph Database Model, Angles AMW 2018 (OpenAlex 101) | Formal property-graph model; lower count; the Cypher and Angles 2017 entries cover the area. |
| The Gremlin Graph Traversal Machine and Language, Rodriguez 2015 (OpenAlex 271) | Third property-graph language; abstract read; kept to a further-reading line. |
| Mintz et al. 2009 (distant supervision), Freebase (Bollacker 2008), DBpedia, YAGO | Outside my years or my area; covered by other researchers' files. |
| Hogan survey follow-ups, Pan et al. LLM and KG roadmap (2306.08302) | Belong to the LLM era file; the roadmap's abstract was read [2] only for cross-era relations. |

---

## Sources

1. https://export.arxiv.org/api/query?id_list=... : arXiv records (v1 dates, authors, journal reference or comments, abstracts) for 2005.11401, 2002.08909, 2004.04906, 1909.01066, 1703.06103, 1707.01476, 1606.06357, 1412.6575, 1902.10197, 1510.04935, 1503.00759, 2003.02320, 2002.00388, 1704.00051, 1803.06643, 1506.02075, 1809.00782, 1705.10744, 2002.00819, 1707.06690, 1702.08367, 1711.05851, 1609.02907, 1906.00300, 2007.01282, 1911.00172, 1909.03193, 2002.08910, 1508.03843 (read 20261102 19:52)
2. https://export.arxiv.org/api/query?id_list=... : arXiv records 2404.16130 (GraphRAG), 2405.14831, 2307.07697, 2502.11371, 2306.08302, used for cross-era relations (read 20261102 20:04)
3. https://api.openalex.org/works/... : OpenAlex `cited_by_count`, publication date, authorships, record type (read 20261102 19:50); abstracts via `abstract_inverted_index` (read 20261102 19:54)
4. https://api.crossref.org/works/<doi> : Crossref metadata, dates, author counts and `is-referenced-by-count` (read 20261102 19:53 and 20:00)
5. https://api.semanticscholar.org/graph/v1/ : HTTP 429 on all attempts, 20261102 19:45 to 20:03; no data obtained
6. https://blog.google/products/search/introducing-knowledge-graph-things-not/ : Singhal, 20120516; size and sources statements (read 20261102 19:52 and 20:04)
7. https://research.google/pubs/knowledge-vault-a-web-scale-approach-to-probabilistic-knowledge-fusion/ : authors, venue, pages (read 20261102 19:52)
8. https://papers.nips.cc/paper_files/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html : TransE authors, venue, abstract (read 20261102 19:52); PDF text from https://papers.nips.cc/paper_files/paper/2013/file/1cecc7a77928ca8133fa24680a88d2f9-Paper.pdf (read 20261102 20:03)
9. https://aclanthology.org/D13-1160/ : WebQuestions paper metadata (read 20261102 19:53)
10. https://ceur-ws.org/Vol-1695/paper4.pdf : Ehrlinger and Wöß, full text (read 20261102 19:54)
11. https://www.semantic-web-journal.net/content/knowledge-graph-refinement-survey-approaches-and-evaluation-methods : Paulheim survey page with open reviews (read 20261102 19:55)
12. https://research.google/pubs/industry-scale-knowledge-graphs-lessons-and-challenges/ : Noy et al. record with abstract (read 20261102 19:55)
13. https://www.wikidata.org/wiki/Wikidata:Introduction : the project's description of itself (read 20261102 19:56)
14. https://icml.cc/2011/papers/438_icmlpaper.pdf : RESCAL paper, abstract and introduction (read 20261102 20:01)
15. https://aclanthology.org/P15-1128.pdf : STAGG, abstract and introduction (read 20261102 20:01)
16. Full-text PDF extractions from https://arxiv.org/pdf/<id> for 2005.11401, 2002.08909, 2004.04906, 1909.01066, 1707.01476, 1705.10744, 1703.06103, 1606.06357, 1412.6575, 1902.10197, 2002.00819, 1809.00782, 1704.00051, read by keyword search (read 20261102 20:02 to 20:03)

Leads consulted but not used as sources: kb-kg/primer/README.md (for the event list), kb-kg/papers-benchmarks/README.md and kb-kg/llm-era/README.md (post-2020 material, other eras).
