## ADDED Requirements

### Requirement: Catalog lists Falklands and MountPleasant
After catalog sync from the packaged registry, known theatres MUST include
`Falklands` and known airfields MUST include `MountPleasant` with
`airdromeId` 2 and theatre `Falklands`.

#### Scenario: Sync populates MountPleasant
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain theatre `Falklands` and airfield
  `MountPleasant` with `airdromeId` 2
