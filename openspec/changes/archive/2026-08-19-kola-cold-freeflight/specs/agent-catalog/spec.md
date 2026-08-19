## ADDED Requirements

### Requirement: Catalog lists Kola and Bodo
After catalog sync from the packaged registry, known theatres MUST include
`Kola` and known airfields MUST include `Bodo` with `airdromeId` 7 and
theatre `Kola`.

#### Scenario: Sync populates Bodo
- **WHEN** a catalog sync runs against the packaged registry after this
  change
- **THEN** the catalog MUST contain theatre `Kola` and airfield `Bodo` with
  `airdromeId` 7
