---
type: index
kind: system
aliases: []
updated: 20261102 21:16 UTC
---

# Freebase

Freebase was a database of structured general knowledge that its users edited together. Google bought its maker in 2010, drew on it for the Knowledge Graph, and let it go read-only in March 2015. This entry gives the definition and the history; for what it contains, how big it is and under which licence it is shared, see the [Freebase dataset page](../datasets/freebase.md).

## Definition

Its authors call Freebase "a practical, scalable tuple database used to structure general human knowledge", whose data is "collaboratively created, structured, and maintained" [1]. Hogan et al. describe it as a general collection of human knowledge that aimed to ease the large-scale integration problems of the decentralised [Semantic Web](./semantic-web.md), and say people added content either through the web interface or through the write function of its API [2].

## How it changed

- **2007 to 2015.** Google's Freebase page says it "was a data-sharing project that ran from 2007 to 2015" [3].
- **2008.** The Freebase team presents the system at SIGMOD (first-party) [1]. The paper is listed in the [foundational papers](../papers/foundations.md).
- **20100716.** Google announces that it has acquired Metaweb, the company behind Freebase, and says Google and Metaweb "plan to maintain Freebase as a free and open database for the world" (first-party) [4]. Era: [The semantic web and linked data](../history/semantic-web.md).
- **20120516.** Google's announcement of the [Google Knowledge Graph](./google-knowledge-graph.md) names Freebase first among its public sources (first-party) [5]. Hogan et al. say its content formed "an important part" of that graph [2]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md).
- **2014.** Pellissier Tanon et al. write that "Google decided in 2014 to offer the content of Freebase to the Wikidata community" [6].
- **March 2015.** Freebase becomes read-only, and "Much of this content was subsequently migrated to Wikidata" [2]. See [Wikidata](./wikidata.md).
- **Today.** The Freebase API "has been shut down". Google hosts the last data dumps, calls them "substantially out of date" and offers no support [3].

## Where sources disagree

No disagreement found in the sources read. The day of the switch to read-only is **unstated**: Hogan et al. give only the month [2], and Google's closure announcement could not be read (the archive host is blocked for this tool).

## Related

Entries: [Wikidata](./wikidata.md), [DBpedia](./dbpedia.md), [YAGO](./yago.md), [Google Knowledge Graph](./google-knowledge-graph.md), [knowledge graph](./knowledge-graph.md), [Semantic Web](./semantic-web.md). Pages: [Freebase dataset](../datasets/freebase.md), [foundational papers](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [The semantic web and linked data](../history/semantic-web.md)

**Trends**

- [Agentic graph retrieval: from one-shot lookup to learned multi-turn traversal](../trends/learned-graph-traversal.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Index**

- [ConceptNet](conceptnet.md)
- [DBpedia](dbpedia.md)
- [Distant supervision](distant-supervision.md)
- [Google Knowledge Graph](google-knowledge-graph.md)
- [Knowledge graph embedding](knowledge-graph-embedding.md)
- [Knowledge-base question answering](knowledge-base-question-answering.md)
- [Linked data](linked-data.md)
- [Relation extraction](relation-extraction.md)
- [Semantic parsing](semantic-parsing.md)
- [Wikidata](wikidata.md)
- [YAGO](yago.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://research.google/pubs/freebase-a-collaboratively-created-graph-database-for-structuring-human-knowledge/ : Bollacker, Evans, Paritosh, Sturge, Taylor, "Freebase: a collaboratively created graph database for structuring human knowledge", SIGMOD 2008; abstract (first-party; read 20261102 20:48 UTC)
2. https://arxiv.org/html/2003.02320v6 : Hogan et al., "Knowledge Graphs", section 10.1.3 (Freebase) and section 1 (read 20261102 20:48 UTC)
3. https://developers.google.com/freebase : Google's Freebase page; "ran from 2007 to 2015", API shut down, last data dumps (first-party; read 20261102 20:51 UTC)
4. https://googleblog.blogspot.com/2010/07/deeper-understanding-with-metaweb.html : "Deeper understanding with Metaweb", Google, 20100716 (first-party; read 20261102 20:48 UTC)
5. https://blog.google/products/search/introducing-knowledge-graph-things-not/ : Singhal, 20120516; sources "such as Freebase, Wikipedia and the CIA World Factbook" (first-party; read 20261102 20:44 UTC)
6. https://research.google/pubs/from-freebase-to-wikidata-the-great-migration/ : Pellissier Tanon, Vrandecic, Schaffert and two others, WWW 2016; abstract (read 20261102 20:48 UTC)
