---
type: index
kind: concept
aliases: [embeddable database, in-process database]
updated: 20261102 22:26 UTC
---

# Embedded database

This entry says what makes a database embedded, dates its best-known examples, and shows why the word no longer settles whether a server is involved.

## Definition

An embedded database is an engine linked into the application as a library, so the application's own process runs it and no server process stands between them. SQLite calls itself "an embedded SQL database engine" with no separate server process; it reads and writes ordinary disk files directly [1]. The Berkeley DB authors say the software "is distributed as a library that can be linked directly into an application", and add that it is neither a network server nor an SQL engine [2]. Stonebraker and Pavlo describe embedded storage managers as "designed to run in the same address space as a higher-level application" [3]. The form fits several data models: Berkeley DB stores key/value pairs [2], SQLite and DuckDB run SQL [1][7], Kuzu runs Cypher [6].

## How it changed

- **1991.** Berkeley DB has its first general release [2]. Stonebraker and Pavlo place one of the first standalone embedded key-value systems in the early 1990s [3]. Era: [Knowledge systems](../history/knowledge-systems.md).
- **20000509.** The SQLite project starts [1]. Era: [The Web changes data and search](../history/the-web.md).
- **20180402.** SQLite adds a section that separates "classic serverless" (the engine runs in the application's process) from "neo-serverless" (a cloud service that hides its servers) [4].
- **2019.** DuckDB, an in-process engine for analytical queries, is first released (first-party) [5][7].
- **20251010.** Kuzu, an embedded property-graph database with Cypher, has its last release (v0.11.3) and last push on this day; its repository is now flagged archived, date unstated [6]. Graphiti's README now warns that its Kuzu driver "is deprecated" [8]. See [Infrastructure and MCP](../trends/infrastructure-and-mcp.md) and [Features in and out](../trends/features-in-and-out.md).
- **20260512.** DuckDB announces Quack, a protocol that lets DuckDB instances run client-server with several concurrent writers. The team says in-process mode works "less well" when several processes change one database file (first-party) [5].

## Where sources disagree

**Does embedded mean no server?** SQLite pairs "embedded" with "serverless" and claims the classic sense [1][4]. DuckDB's documentation says it adopted in-process operation but "later stepped out of the realm of in-process operations through the Quack protocol", while by default it "does not run as a separate process" [7]. *Reading:* since 2026 the label can describe a default mode, not a guarantee.

## Related

[SQL](./sql.md), [graph database](./graph-database.md), [property graph](./property-graph.md), [Cypher](./cypher.md), [vector search](./vector-search.md), [HNSW](./hnsw.md), [ACID](./acid.md), [NoSQL](./nosql.md). Project: [Graphiti](../projects/graphiti.md). Trends: [Infrastructure and MCP](../trends/infrastructure-and-mcp.md) and [Features in and out](../trends/features-in-and-out.md).

## Appears in

<!-- BEGIN GENERATED: appears-in -->

**Trends**

- [Infrastructure and MCP: what knowledge systems run on, and how agents reach them](../trends/infrastructure-and-mcp.md)

**Index**

- [Graph database](graph-database.md)

<!-- END GENERATED: appears-in -->

## Sources

1. https://sqlite.org/about.html : "About SQLite": "embedded SQL database engine", no separate server process, project started 2000-05-09 (page last updated 2025-11-13) (read 20261102 22:07 UTC)
2. https://www.usenix.org/legacy/publications/library/proceedings/usenix99/full_papers/olson/olson.pdf : Olson, Bostic, Seltzer, "Berkeley DB", FREENIX Track, USENIX Annual Technical Conference, Monterey, 6-11 June 1999: abstract, sections 1 and 1.1 (library, first general release 1991), section 1.3 (not a server, not SQL) (read 20261102 22:10 UTC)
3. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf : Stonebraker and Pavlo, SIGMOD Record 53(2), 2024: section 2.2, key/value stores (embedded storage managers; BerkeleyDB "from the early 1990s") (read 20261102 22:12 UTC)
4. https://www.sqlite.org/serverless.html : "SQLite Is Serverless", section 2, "Classic Serverless Vs. Neo-Serverless", added 2018-04-02 (read 20261102 22:10 UTC)
5. https://duckdb.org/2026/05/12/quack-remote-protocol : DuckDB team, "Quack: The DuckDB Client-Server Protocol", 20260512: DuckDB first released in 2019, in-process mode and its limit, the protocol (first-party; read 20261102 22:12 UTC)
6. https://github.com/kuzudb/kuzu : repository metadata and README by `gh api`: archived flag, last push 2025-10-10, latest release v0.11.3 published 2025-10-10, "embedded graph database", Cypher (read 20261102 22:12 UTC)
7. https://duckdb.org/why_duckdb : DuckDB documentation, "Why DuckDB": in-process operation, "completely embedded within a host process" by default, the Quack protocol (first-party; read 20261102 22:10 UTC)
8. https://github.com/getzep/graphiti : README by `gh api`, section "Installing with Kuzu Support": "Kuzu is deprecated and will be removed in a future release" (read 20261102 22:22 UTC)
