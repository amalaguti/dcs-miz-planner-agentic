## ADDED Requirements

### Requirement: Catalog lists Nevada and Nellis
After catalog sync from the packaged registry, known theatres MUST include
`Nevada` and known airfields MUST include `Nellis` with `airdromeId` 4
and theatre `Nevada`.

#### Scenario: Sync populates Nellis
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain theatre `Nevada` and airfield `Nellis`
  with `airdromeId` 4
