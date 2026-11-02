---
type: index
kind: system
aliases: [Wikidata.org]
updated: 20261102 23:12 UTC
---

# Wikidata

Wikidata is the community-edited store of structured data behind Wikipedia and its sister wikis. This entry says what the name means and how the project changed; content, size and licence are on the dataset page.

## Definition

The project calls itself "a free, collaborative, multilingual, secondary knowledge base" that collects structured data to support Wikipedia, Wikimedia Commons, the other Wikimedia wikis and anyone else [1]. Vrandečić and Krötzsch, the authors of its reference paper in the Communications of the ACM, describe it as a collaboratively edited knowledge base that gives Wikipedia and everyone else a common source of data [2]. For the general idea see [knowledge graph](./knowledge-graph.md); its query language is [SPARQL](./sparql.md) [6].

## How it changed

- **20121029.** Wikimedia Deutschland says Wikidata "was launched on October 29, 2012" by a team of twelve people in Berlin (first-party) [3]. The Wikipedia Signpost of the same day reports that Wikidata.org "launched this week" [4]. Era: [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md); the day is also given on the page of [The semantic web and linked data](../history/semantic-web.md).
- **2014.** Pellissier Tanon and four co-authors write that "Google decided in 2014 to offer the content of Freebase to the Wikidata community" [5]. See [Freebase](./freebase.md).
- **20140923.** The reference paper by Vrandečić and Krötzsch appears in CACM 57(10) [2]; it is in the [foundational papers](../papers/foundations.md).
- **2026.** The query service moves off its old engine. The migration hub says Blazegraph "no longer scales efficiently" and is being replaced by QLever; the proposal is dated May 2026, the old endpoints may degrade from February 2027, and the aim is to move all traffic by 20270630, when Blazegraph is decommissioned [6][7]. The data model is not part of this project [7].

## Where sources disagree

The date by which the new query endpoints open to the community. The hub page says "by November 16th" [6]; the project-overview page says "by November 1st" [7]. Neither page gives a year for its November date; the overview timeline places the work in 2026 ("Initial implementation" August to October 2026, "Full implementation" November 2026 to June 2027), so 2026 is an inference. The November 1 date had already passed when the pages were read on 20261102 21:24 UTC. Which date is current is **unstated**. The interview in [3] also disagrees with itself on the team size: it says twelve people started programming, and its list under "These dedicated people launched Wikidata in Berlin in 2012" names 13.

## Related

Entries: [Freebase](./freebase.md), [DBpedia](./dbpedia.md), [YAGO](./yago.md), [WordNet](./wordnet.md), [Google Knowledge Graph](./google-knowledge-graph.md), [knowledge graph](./knowledge-graph.md), [linked data](./linked-data.md), [RDF](./rdf.md), [SPARQL](./sparql.md), [schema.org](./schema-org.md). Dataset: [Wikidata](../datasets/wikidata.md). Papers: [foundations](../papers/foundations.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [History: how knowledge bases and knowledge graphs evolved](../history/README.md)
- [Knowledge graphs at scale](../history/knowledge-graphs-at-scale.md)
- [Language models meet retrieval (2018-2022)](../history/language-models-meet-retrieval.md)
- [The semantic web and linked data](../history/semantic-web.md)

**Papers**

- [Papers: foundations](../papers/foundations.md)

**Index**

- [DBpedia](dbpedia.md)
- [Distant supervision](distant-supervision.md)
- [Entity](entity.md)
- [Entity linking](entity-linking.md)
- [Freebase](freebase.md)
- [Google Knowledge Graph](google-knowledge-graph.md)
- [Linked data](linked-data.md)
- [Semantic Web](semantic-web.md)
- [Triple store](triple-store.md)
- [WordNet](wordnet.md)
- [YAGO](yago.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.wikidata.org/wiki/Wikidata:Introduction : opening definition (first-party; read 20261102 21:03 UTC)
2. https://doi.org/10.1145/2629489 : Crossref record of Vrandečić and Krötzsch, "Wikidata: a free collaborative knowledgebase", CACM 57(10), 78-85, issued 20140923; abstract sentence (read 20261102 21:24 UTC)
3. https://blog.wikimedia.de/en/2022/10/27/wikidata-birthday-interview/ : Wikimedia Deutschland blog, interview with Lydia Pintscher: launch date and team (twelve stated, 13 names listed) (first-party; read 20261102 21:24 UTC; the launch date re-read 20261102 22:53 UTC)
4. https://en.wikipedia.org/wiki/Wikipedia:Wikipedia_Signpost/2012-10-29/Technology_report : Signpost technology report of 20121029, "Wikidata.org goes live": "launched this week" (read 20261102 21:04 UTC; re-read 20261102 22:53 UTC)
5. https://research.google/pubs/from-freebase-to-wikidata-the-great-migration/ : Pellissier Tanon, Vrandečić, Schaffert, Steiner, Pintscher, WWW 2016; abstract (read 20261102 21:04 UTC)
6. https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/WDQS_backend_update : migration hub, wikitext as served; Blazegraph to QLever, February 2027, "by November 16th", no year given (first-party; read 20261102 21:24 UTC)
7. https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/WDQS_backend_update/Learn : project overview and timeline; May 2026 proposal, 20270630, "by November 1st", no year given, data model unchanged (first-party; read 20261102 21:24 UTC)
