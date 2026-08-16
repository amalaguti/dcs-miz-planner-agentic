## ADDED Requirements

### Requirement: Catalog lists Caucasus and Batumi
After catalog sync from the packaged registry, known theatres MUST include
`Caucasus` and known airfields MUST include `Batumi` with `airdromeId` 22
and theatre `Caucasus`.

#### Scenario: Sync populates Batumi
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain theatre `Caucasus` and airfield `Batumi`
  with `airdromeId` 22
