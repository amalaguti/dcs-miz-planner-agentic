## ADDED Requirements

### Requirement: Catalog sync includes planning options
Catalog sync from packaged Channel data SHALL also replace planning-option rows from the
packaged planning-options source so agent/UI queries stay aligned with the product package.

#### Scenario: Sync refreshes planning options idempotently
- **WHEN** catalog sync runs twice without package changes
- **THEN** planning-option query results MUST remain equivalent (same ids and support levels)
