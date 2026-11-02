---
type: index
kind: standard
aliases: [CODASYL network model, DBTG, Data Base Task Group]
updated: 20261102 21:28 UTC
---

# CODASYL

This entry answers what CODASYL's database work was, how it grew out of Bachman's Integrated Data Store (IDS), and why graph databases are compared to it. It does not cover the relational model or the later SQL standards. The acronym's expansion is unstated in the sources read.

## Definition

CODASYL here means the committee work, and the report it produced, for a network data model: records of different types are tied into "data structure sets" that a program follows as retrieval paths [1]. Bachman, the designer of IDS, says the COBOL Data Base Task Group (DBTG) implementations are of this class [1]. His 1973 Turing Award presentation called the specifications "the only proposal of stature" for a common architecture [1]. Whether the output was a formal standard is disputed (below); the kind "standard" is the index's label, not a finding.

## How it changed

- **1961 to 1964.** Bachman develops IDS at General Electric [1][2]. See [The advent](../history/advent.md).
- **196510, renamed 1967.** The interviewer cites an article dating the List Processing Task Group to October 1965 and its renaming to 1967; Bachman answers "Two years" [2].
- **1970s.** Stonebraker and Pavlo list the network model (CODASYL) as a 1970s movement beside the relational one [3]. See [Formal foundations](../history/formal-foundations.md).
- **197311.** Bachman's Turing lecture, "The Programmer as Navigator", appears in *Communications of the ACM* 16(11), pages 653 to 658 [1][4].
- **2024.** Stonebraker and Pavlo write that Neo4j "supports edges using pointers (as in CODASYL)" [3]. This is their characterisation. See [Neo4j](../projects/neo4j.md).

## Where sources disagree

**Was it a standard?** Gutierrez and Sequeda say IDS "became the basis for the CODASYL standard" [5]. The oral-history abstract speaks of "database standards" [2]. Bachman himself says the Task Group "didn't standardize it. It made recommendations" (p. 95), and "The CODASYL report from DBTG was not a standard; it was a report", unlike an ANSI standard (p. 128) [2]. The interviewer, Haigh, describes a later CODASYL committee whose report was printed in 1974 and, in a footnote he marks as not fully verified, a series of standards in its Journal of Development. Bachman calls that group "totally different" and says of a 1974 standard "I have no knowledge of it" (pp. 95, 128) [2].

**When was IDS made?** The award presentation says 1961 to 1964 [1]; Gutierrez and Sequeda say Bachman designed it "in 1963" [5]. Neither says whether 1963 is a design date inside the span.

**How long did Bachman serve?** 1966 to 1968 per the presentation [1]; he thinks he stayed throughout, without knowing when the group ended [2].

## Related

[data independence](./data-independence.md) · [relational model](./relational-model.md) · [property graph](./property-graph.md) · [Neo4j](../projects/neo4j.md) · [foundation papers](../papers/foundations.md)

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**History**

- [The advent: machines that hold knowledge](../history/advent.md)

**Index**

- [Data independence](data-independence.md)
- [Entity-relationship model](entity-relationship-model.md)
- [INGRES](ingres.md)
- [Object-oriented database](object-oriented-database.md)
- [Relational model](relational-model.md)
- [SQL](sql.md)
- [System R](system-r.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://www.arabou.edu.kw/faculties/computer/Documents/ReadingList/ITC/a1973-bachman.pdf (a university reading-list copy; the published version is at https://doi.org/10.1145/355611.362534) : Bachman, "The Programmer as Navigator", Turing Award lecture, CACM 16(11), November 1973, with the award presentation: IDS 1961-1964, Task Group 1966-1968, data structure sets, "only proposal of stature" (read 20261102 20:49 UTC)
2. https://tomandmaria.com/Tom2/Writing/Bachman%20Haigh%20Oral%20History.pdf (a personal-site copy; its title page says transcript and tapes were donated to the Charles Babbage Institute, whose own record was not reachable) : Bachman, oral history with Thomas Haigh, 25-26 September 2004, for ACM SIGMOD: abstract; pages 91-95 and 128 on the Data Base Task Group and on "report" versus "standard" (read 20261102 20:50 UTC; pages 95, 128 and the abstract re-read 20261102 21:24 UTC)
3. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, "What Goes Around Comes Around... And Around...", SIGMOD Record 53(2), June 2024: introduction and section 2.8 (read 20261102 20:45 UTC)
4. https://api.crossref.org/works/10.1145/355611.362534 : Crossref record of Bachman 1973: volume 16, issue 11, pages 653-658 (read 20261102 20:49 UTC)
5. https://users.dcc.uchile.cl/~cgutierr/papers/kg-gutierrez-sequeda.pdf : Gutierrez and Sequeda, "Knowledge Graphs", CACM 64(3), 2021: "Languages and systems to manage data" (read 20261102 20:47 UTC; the IDS passage re-read 20261102 21:24 UTC)
