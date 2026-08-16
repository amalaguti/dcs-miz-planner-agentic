## ADDED Requirements

### Requirement: Catalog lists Syria and Incirlik
After catalog sync from the packaged registry, known theatres MUST include
`Syria` and known airfields MUST include `Incirlik` with `airdromeId` 16
and theatre `Syria`.

#### Scenario: Sync populates Incirlik
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain theatre `Syria` and airfield `Incirlik`
  with `airdromeId` 16
