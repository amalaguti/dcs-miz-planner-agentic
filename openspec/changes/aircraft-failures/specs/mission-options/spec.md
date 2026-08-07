## ADDED Requirements

### Requirement: Failure planning options
Planning-options SHALL expose supported failure-related knobs or example failure ids
the agent can discover (family for aircraft failures / training), without inventing
ids outside the catalog.

#### Scenario: Options list failures family
- **WHEN** listing mission options after catalog sync
- **THEN** failure-related supported entries MUST appear for Channel Spitfire
