➡ Consolidated at: ../dev/guides/rag-systems.md#adr-0002-multi-storage-pattern
## Status

Accepted
➡ Consolidated at: ../dev/guides/rag-systems.md#

## Decision

Use OpenSearch for full-text search, Neo4j for graph relations and PostgreSQL for transactional data.

## Consequences

Best-of-breed storage for each workload but increases operational overhead and data consistency challenges.

## Alternatives

- Single relational database
- Vendor-specific multi-model database

## References

- [opensearch.org](https://opensearch.org/)
- [neo4j.com](https://neo4j.com/)
