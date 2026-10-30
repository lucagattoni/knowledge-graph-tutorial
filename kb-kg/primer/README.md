# Before LLMs: the lineage of knowledge bases and knowledge graphs

Where the ideas of "knowledge base" and "knowledge graph" come from, up to the point where large
language models (LLMs) enter. Back to [`kb-kg/`](../README.md). Next: [`llm-era/`](../llm-era/README.md).

How to read this page. Each factual statement carries a bracketed source number; the numbered list
at the end gives the URL and the time it was read (UTC). Event dates are written `YYYYMMDD`, or
`YYYYMM` or `YYYY` when only that is known. Where a source is silent the page says **unstated**.
"As cited in [1]" means the survey names the work and this page did not fetch it.

## 1. Definitions, and the disagreement

**Knowledge base.** In the expert-system tradition, a knowledge-based system has two parts: a
knowledge base and an inference engine. The knowledge base holds rules, facts, axioms, definitions
and statements [2]. Lenat and colleagues use the term in 1985 for "a large knowledge base of
real-world facts and heuristics", with methods for reasoning over it [19]. Ehrlinger and Wöß argue
that an ontology does not differ from a knowledge base, because an ontology can hold instances as
well as classes. They also report that the term is often used as a synonym for ontology, and for
knowledge graph [2]. The date of first use of "knowledge base" is **unstated** in the sources read.

**Knowledge graph.** Hogan et al. adopt an inclusive definition: a graph of data intended to
accumulate and convey knowledge of the real world, whose nodes are entities of interest and whose
edges are relations between them. The data model may be a directed edge-labelled graph or a property
graph. Ontologies and rules are needed only when the graph is meant to hold quantified statements such
as "all capitals are cities" [1].

**There is no single agreed definition.** Hogan et al. call the definition "contentious", with
"sometimes conflicting" proposals ranging from specific technical ones to inclusive ones [1].
Ehrlinger and Wöß list five and find "the lack of a common core" [2]. The table compares them.

| Definition | What it requires | Source |
|---|---|---|
| Paulheim | Real-world entities and relations in a graph; a schema of classes and relations; arbitrary entities may be linked; many topical domains | quoted in [2] |
| Journal of Web Semantics call | "Large networks" of entities, their types, properties and relationships; "large" is not defined | quoted in [2] |
| Färber et al. | An RDF graph (triples of subject, predicate, object). The only formal definition, and it requires RDF | quoted in [2] |
| Pujara et al. | Interrelated facts extracted from the web by extraction systems; stresses automatic extraction | quoted in [2] |
| Ehrlinger and Wöß | A system that "acquires and integrates information into an ontology and applies a reasoner to derive new knowledge". A manually made graph with no integration is, in their terms, a plain knowledge base (or a knowledge-based system if it can reason) | [2] |
| Hogan et al. | Inclusive: any graph of data about real-world entities and relations; schema, reasoning and RDF are optional | [1] |

The same artefact can therefore be a knowledge graph under one row and not under another. A
manually built RDF graph with no integration step and no reasoner is a knowledge graph for Färber
et al. and Hogan et al., and a plain knowledge base for Ehrlinger and Wöß [1][2].

The phrase is older than Google's product. Hogan et al. trace the first relevant use to Schneider
(1973), a directed graph of concepts in a computerised course; the survey's introduction says "at
least 1972", so the two statements in [1] differ by a year. Ehrlinger and Wöß date the term to
researchers at Groningen and Twente in the 1980s [2]; [1] describes 1980s uses by Bakker (1987) and
Stokman and de Vries (1988) for graphs built from medical and sociological texts, and does not say
where they worked. The modern use stems from Google's 2012 announcement [1]. Ehrlinger and Wöß note
that the announcement gave no implementation details, yet is cited as if it explained what a
knowledge graph is [2].

Why this matters when reading projects. A project that calls itself a knowledge graph may be a
property graph in a graph database, an RDF triple store with an ontology, or a set of facts
extracted from text with confidence scores. Under the inclusive reading all three qualify; under
Färber et al. only the RDF one does; under Ehrlinger and Wöß only a system that also integrates
sources and reasons does [1][2]. When two projects are compared, the comparison should say which
of these properties each has, and not rely on the label. This primer uses Hogan et al.'s inclusive
reading unless it says otherwise.

## 2. Timeline

| Date | Event | Why it mattered | Source |
|---|---|---|---|
| 1963 | Quillian's report on a notation for representing conceptual information, for semantics and "mechanical English paraphrasing" (System Development Corporation, SP-1395) | Start of the semantic-network line. Hogan et al. treat semantic networks as "an early version of knowledge graphs" | [1] (as cited) |
| 1973 to 1990s | The phrase "knowledge graph" used in unrelated senses: instructional courses (Schneider 1973), medical expert systems (Rada 1986), causal graphs from texts (Bakker 1987) | The phrase predates Google by decades with other meanings | [1], [2] |
| 19740601 | Minsky, "A Framework for Representing Knowledge" (MIT AI Memo 306): a stored template, a *frame*, is adapted to a new situation by filling slots with specifics | Gave representation a structured unit. Description logics were introduced to formalise frames and semantic networks | [11], [1] |
| 1975 to 1979 | Woods (1975) and Brachman (1977) formalise semantic networks; Sowa proposes conceptual graphs (1979) | Attempts to give graph notations a formal meaning. Sowa (1987), quoting Woods and McDermott: semantic networks "have no well-defined semantics" | [1] (as cited) |
| 1970s to 1980s (decade only; start dates **not verified**) | Expert systems from the Stanford Heuristic Programming Project; MYCIN is the example in [21]. The 1984 MYCIN book has a part called "Building a Knowledge Base" and a chapter "Knowledge Engineering" | The setting in which the sources use "knowledge base" as a technical term: one part of a knowledge-based system, beside an inference engine [2]. First use of the term: **unstated** | [21], [2] |
| 1985 | KL-ONE (Brachman and Schmolze) | Description logics grew from it; they underpin OWL | [1] (as cited) |
| 1985 | Lenat, Prakash and Shepherd, *AI Magazine* 6(4): MCC's CYC project, a multi-year effort to build a large knowledge base of real-world facts and heuristics. They argue common sense can ease both the knowledge-acquisition bottleneck and the brittleness of current expert systems. Project start year: **unstated** in the page fetched (1984 is commonly given; not verified here) | Names the two problems the field kept returning to | [19] |
| 19990222 | W3C Recommendation: RDF Model and Syntax (editors Lassila and Swick), "a foundation for processing metadata" | A building block of the Semantic Web [1]. Its data model is the triple of subject, predicate, object | [4], [2], [1] |
| 200105 | Berners-Lee, Hendler and Lassila, "The Semantic Web", cover story of the May 2001 *Scientific American* (W3C news item dated 20010413) | A general-audience presentation of the Semantic Web. Most open knowledge graphs later emerged from that community or adopted its standards | [13], [1] |
| 20040210 | W3C Recommendation: OWL, with three sublanguages (Lite, DL, Full) | A Web ontology language based on description logics. DL keeps decidability; Full has "no computational guarantees" | [5], [1] |
| 20060727 | Berners-Lee, "Linked Data" design note: four rules (URIs as names; HTTP URIs; useful RDF/SPARQL information on lookup; links to other URIs) | Rules for linking datasets. Ehrlinger and Wöß find Linked Data the lowest common denominator of the open knowledge graphs they list | [7], [2] |
| 2007 | DBpedia project begins; it extracts structured data from Wikimedia projects and publishes it as Linked Data, queryable with SPARQL | An early large open knowledge graph built from Wikipedia | [17], [1] |
| 20080115 | W3C Recommendation: SPARQL query language for RDF (superseded by SPARQL 1.1 in 2013) | The standard query language for RDF graphs | [6] |
| 2008 | Freebase paper (Bollacker et al., SIGMOD): a collaboratively edited graph database with more than 125,000,000 tuples, 4,000 types and 7,000 properties, and an HTTP graph-query API (MQL) | Community-edited knowledge at scale, organised by types and properties | [12] |
| 20100225 | InfoQ reports Neo4j 1.0 (article date; release date not stated there): property graph model of nodes, typed directed relationships and key-value properties on both. "1.0" meant API stability, not a mature codebase. The kernel was AGPLv3, with a commercial licence for closed-source use | A production property-graph database. Cypher came later, with Neo4j 2.0 in 2013 | [15], [14] |
| 20120516 | Google announces its Knowledge Graph ("things, not strings"): more than 500 million objects and more than 3.5 billion facts and relationships at launch, rooted in public sources such as Freebase, Wikipedia and the CIA World Factbook, and not only those | The announcement from which today's use of the term stems. No implementation details were given | [3], [1], [2] |
| 20121029 | Wikidata launches (date per a tertiary source; one search summary showed mirrors giving 30 October, not resolved). Developed mainly by Wikimedia Deutschland | Open, collaboratively edited knowledge graph. Google announced in December 2014 that it would shut down Freebase in favour of Wikidata; the migration is described in Pellissier Tanon et al. 2016 (as cited in [1]) | [16], [1] |
| 2013 | TransE (Bordes et al., NIPS 2013): relations modelled as translations between low-dimensional entity embeddings; trained on 1M entities, 25k relations and more than 17M training samples | A cheap learned model that predicts missing edges at knowledge-graph scale | [8] |
| 2014 | Knowledge Vault (Dong et al., KDD 2014): extracts facts from text, tables, page structure and human annotations, fuses them with prior knowledge, and outputs calibrated probabilities | Automatic construction at web scale with explicit uncertainty | [18] |
| 2016 | Ehrlinger and Wöß, "Towards a Definition of Knowledge Graphs" (SEMANTiCS 2016 posters) | A definitional discussion that [1] builds on, with Bergman (2019) | [2], [1] |
| 201810 and 2019 | Noy et al., *CACM* 62(8) (2019), from a panel at the International Semantic Web Conference, October 2018: knowledge graphs at Microsoft (Bing), Google, Facebook, eBay and IBM | Enterprise knowledge graphs compared. Hogan et al. summarise common trends: data integrated from internal and external sources, often text; millions or billions of nodes and edges; refinement such as consolidating duplicate entities; keeping the graph up to date; a mix of ontological and machine-learning representations | [20], [1] |
| 20200210 | REALM (Guu et al., arXiv): a learned retriever over a document collection such as Wikipedia, trained with masked-word prediction; 4 to 16 points of absolute accuracy better than prior methods on three open-domain question-answering benchmarks | Knowledge kept outside the model weights, in text | [9] |
| 20200522 | RAG (Lewis et al., arXiv v1; NeurIPS 2020): a pretrained seq2seq model (parametric memory) with a dense vector index of Wikipedia (non-parametric memory) read by a neural retriever | Named retrieval-augmented generation. It retrieves text passages, not graph structure | [10] |
| 20200304 | Hogan et al., "Knowledge Graphs" (arXiv v1; v6 on 20210911; *ACM Computing Surveys* 54(4), 2021) | The survey this primer leans on most | [1] |

Reading the table in order, three overlapping stretches stand out. Up to the 1980s the work is
about how to write knowledge down: networks, frames, logics, rule bases, and a first multi-year
effort to build a large knowledge base [11][19][1]. From 1999 to 2008 the W3C published RDF, OWL and
SPARQL as Recommendations, and Berners-Lee set out the Linked Data rules [4][5][6][7]. From 2007 to
2014 large graphs appeared: DBpedia, Freebase, Google's Knowledge Graph, Wikidata and Knowledge
Vault, with Neo4j serving the property-graph side [17][12][3][16][18][15]. Learning methods (TransE in 2013)
and retrieval-augmented language models (2020) come last [8][9][10]. Dates marked *not verified*
or *tertiary* in the table rest on weaker evidence than the rest; the list at the end says why.

## 3. Two traditions

The sources do not name two schools. The split below is this page's reading of them, drawn from the
survey's own account of logical and inductive methods [1]. The traditions overlap, and the same
project often uses both.

| | Symbolic and logical | Statistical and graph-data |
|---|---|---|
| Idea | Write meaning down as explicit logic, so a reasoner can derive new facts [1][2] | Treat the graph as data to store, query, integrate and learn from; the schema can wait [1] |
| Artefacts | Semantic networks, frames, description logics, OWL ontologies, expert-system rule bases, Cyc | Property-graph databases, tuple stores such as Freebase, embeddings, extraction-and-fusion systems such as Knowledge Vault, enterprise graphs |
| Did well | Explicit semantics. Deduction: from the graph's edges one can deduce that a festival is located in a city [1]. Shared standards: RDF, OWL, SPARQL, Linked Data [4][5][6][7] | Flexible schema: graphs "allow maintainers to postpone the definition of a schema" and suit incomplete knowledge [1]. Navigational queries over paths of any length [1]. Scale: embeddings trained on more than 17M samples [8]; enterprise graphs with millions or billions of nodes and edges [1]. Predicting missing links [8] |
| Did badly | Semantic networks "have no well-defined semantics" (Sowa, quoted in [1]); the real world is "messy, incompletely explored" (same quote). Brittleness of expert systems and the knowledge-acquisition bottleneck [19]. A trade-off between expressiveness and decidability: OWL DL keeps decidability, OWL Full has "no computational guarantees" [5] | Embeddings give no interpretable reason for a prediction, and cannot answer for nodes or edges unseen in training [1]. TransE is "too simplistic" where one relation has many targets [1]. Extracted facts come with probabilities, not guarantees [18]. Industrial systems are opaque: no official documentation of Google's methods [2] |

Two end-points make the contrast concrete. Cyc, described in 1985, bets that a large knowledge
base of facts and heuristics, with reasoning built in, will remove brittleness and ease knowledge
acquisition [19]. Knowledge Vault, in 2014, bets the other way: let extractors read the web, fuse
what they find with prior knowledge, and attach a calibrated probability to each fact [18]. The
first puts its effort into the content of one large knowledge base; the second into automated
extraction and an uncertainty estimate for each fact. Both descriptions come from the papers'
abstracts [19][18]; this page has not read the full texts or their evaluations.

What the two share. Hogan et al. list "combinations of formal (logical) and statistical forms of
reasoning" among the notions established in the early work [1]. The enterprise trends in [20], as
summarised in [1], include mixing ontological and machine-learning representations. Ehrlinger and
Wöß's definition asks for both data integration and a reasoner [2].

## 4. What was still hard

By 2020 the data models, query languages, ontology languages and learning methods were in place
(the previous section). This primer's reading is that the cost left over was building and keeping
the graph. In the survey, creation and enrichment (its section 6) comes after the sections on data
models, schema, deduction and induction [1].

| Problem | What it means | Evidence it was hard |
|---|---|---|
| Extraction | Turning text into nodes and edges: pre-processing, named-entity recognition, entity linking and relation extraction [1] | Extracting from text "with high precision and recall" is "a non-trivial challenge" [1]. Hand-written rules are still used where predictable behaviour matters [1]. Knowledge Vault fuses several sources to reduce the noise of text-only extraction and reports a probability per fact [18] |
| Entity resolution and linking | Deciding which mentions, and which nodes, denote the same real-world thing | The survey says identity, with schema and context, "often play a key role" [1]. Linking must disambiguate: "Santiago" most often means the Chilean capital but not always [1]. Predicting identity links is analogous to entity matching, record linkage and deduplication [1]. Consolidating duplicate entities is on the enterprise list [1] |
| Schema design | Choosing the classes and relations | Early ontology-engineering methods were waterfall-like, fixing requirements first; large or fast-changing ontologies led to agile ones [1]. Humans are still used to define high-level schema [1]. Graphs let a team postpone this choice [1]; it still has to be made |
| Upkeep | Keeping content correct and current | Human editing is costly and brings error, disagreement, bias and vandalism, plus licensing, tooling and culture problems [1]. Enterprise graphs need refinement and up-to-date content [1] |

Two older points. The knowledge-acquisition bottleneck was already named in the expert-system era,
and a 1985 paper presents Cyc as one answer to it [19]. And the best-known industrial graph does not
document its methods: the announcement names some sources but gives no implementation details [3][2].

In sum, the four rows above are the work that someone has to do before any graph is queried. Systems
that automate parts of it, such as Knowledge Vault, produce probabilities rather than certainties [18].

## 5. Bridge to the LLM era

In February and May 2020, REALM and RAG showed neural text models reading from an external document
index through a learned retriever, so that knowledge sits in documents and not only in weights. Both
retrieved text passages from Wikipedia, not graph structure [9][10]. On the other side stood
knowledge graphs with explicit semantics and costly construction: extraction, entity resolution,
schema design and upkeep, as section 4 sets out [1]. This primer's framing of the questions that
follow is: can a language model lower that construction cost, and does graph structure help
retrieval? What changed from 2022 on, and in what order, is in
[`llm-era/`](../llm-era/README.md).

## Sources

Read times are UTC to the minute, set from the order of the fetches; accuracy about one minute.

| # | Source | URL | Read |
|---|---|---|---|
| 1 | Hogan et al., "Knowledge Graphs", arXiv:2003.02320 v6, *ACM Computing Surveys* 54(4), 2021 (abstract page and full text) | https://arxiv.org/abs/2003.02320 | 20261030 18:59 UTC |
| 2 | Ehrlinger and Wöß, "Towards a Definition of Knowledge Graphs", SEMANTiCS 2016 posters | https://ceur-ws.org/Vol-1695/paper4.pdf | 20261030 18:59 UTC |
| 3 | Singhal, "Introducing the Knowledge Graph: things, not strings", Google, 20120516 | https://blog.google/products/search/introducing-knowledge-graph-things-not/ | 20261030 18:59 UTC |
| 4 | W3C, RDF Model and Syntax Specification, 19990222 | https://www.w3.org/TR/1999/REC-rdf-syntax-19990222/ | 20261030 18:59 UTC |
| 5 | W3C, OWL Web Ontology Language Overview, 20040210 | https://www.w3.org/TR/2004/REC-owl-features-20040210/ | 20261030 18:59 UTC |
| 6 | W3C, SPARQL Query Language for RDF, 20080115 | https://www.w3.org/TR/rdf-sparql-query/ | 20261030 18:59 UTC |
| 7 | Berners-Lee, Linked Data (Design Issues), dated 20060727 | https://www.w3.org/DesignIssues/LinkedData.html | 20261030 18:59 UTC |
| 8 | Bordes et al., "Translating Embeddings for Modeling Multi-relational Data", NIPS 2013 | https://papers.nips.cc/paper_files/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html | 20261030 18:59 UTC |
| 9 | Guu et al., "REALM: Retrieval-Augmented Language Model Pre-Training", arXiv:2002.08909 | https://arxiv.org/abs/2002.08909 | 20261030 19:00 UTC |
| 10 | Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", arXiv:2005.11401 | https://arxiv.org/abs/2005.11401 | 20261030 19:00 UTC |
| 11 | Minsky, "A Framework for Representing Knowledge", MIT AI Memo 306, 19740601 | https://dspace.mit.edu/handle/1721.1/6089 | 20261030 19:00 UTC |
| 12 | Bollacker et al., "Freebase: a collaboratively created graph database for structuring human knowledge", SIGMOD 2008 (Google Research record) | https://research.google/pubs/freebase-a-collaboratively-created-graph-database-for-structuring-human-knowledge/ | 20261030 19:00 UTC |
| 13 | W3C news, "Semantic Web Featured in Scientific American", 20010413 | https://www.w3.org/news/2001/semantic-web-featured-in-scientific-american | 20261030 19:00 UTC |
| 14 | Neo4j, "A decade of graphs: Neo4j's top 10 biggest moments of the 2010s" | https://neo4j.com/blog/news/neo4j-top-10-biggest-moments-of-2010s/ | 20261030 19:01 UTC |
| 15 | InfoQ, Neo4j 1.0 news item, 20100225 | https://www.infoq.com/news/2010/02/neo4j-10 | 20261030 19:01 UTC |
| 16 | Wikipedia, "Wikidata" (tertiary source; first 100,000 characters read) | https://en.wikipedia.org/wiki/Wikidata | 20261030 19:01 UTC |
| 17 | DBpedia, About | https://www.dbpedia.org/about/ | 20261030 19:01 UTC |
| 18 | Dong et al., "Knowledge Vault", KDD 2014 (Google Research record) | https://research.google/pubs/knowledge-vault-a-web-scale-approach-to-probabilistic-knowledge-fusion/ | 20261030 19:01 UTC |
| 19 | Lenat, Prakash and Shepherd, "CYC: Using Common Sense Knowledge to Overcome Brittleness and Knowledge Acquisition Bottlenecks", *AI Magazine* 6(4), 1985 (bibliographic record with abstract) | https://interlisp.org/history/bibliography/qxtftccf/ | 20261030 19:02 UTC |
| 20 | Noy et al., "Industry-scale Knowledge Graphs: Lessons and Challenges", *CACM* 62(8), 2019 (Google Research record with abstract) | https://research.google/pubs/industry-scale-knowledge-graphs-lessons-and-challenges/ | 20261030 19:02 UTC |
| 21 | Buchanan and Shortliffe (eds.), *Rule-Based Expert Systems: The MYCIN Experiments of the Stanford Heuristic Programming Project*, 1984 (contents page only) | https://people.dbmi.columbia.edu/~ehs7001/Buchanan-Shortliffe-1984/MYCIN%20Book.htm | 20261030 19:02 UTC |

Not verified in this run, and left out or marked above:

- The date of first use of "knowledge base", and the start dates of DENDRAL and MYCIN. The Britannica page returned an access error; the MYCIN book page gave only a contents list.
- The start year of Cyc (1984 is common). The AAAI page for the 1985 paper was under maintenance; only a bibliographic record with the abstract was read [19].
- The full text of Noy et al. (ACM and CACM pages returned access errors); the abstract [20] and the survey's summary of it [1] were used.
- The DBpedia ISWC 2007 paper and the Wikidata CACM paper: not reachable. Wikidata's launch date rests on a tertiary source [16].
- Quillian, Woods, Brachman, Sowa, KL-ONE and Schneider: known here only through the survey's references and text [1].
