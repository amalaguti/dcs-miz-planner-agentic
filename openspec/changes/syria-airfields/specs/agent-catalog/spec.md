## ADDED Requirements

### Requirement: Catalog lists extra Syria airfields and Syria country
After `dcs-miz catalog sync`, known airfields MUST include `Palmyra` with
`airdromeId` 28 and theatre `Syria`, and known countries MUST include
`Syria` (modern).

#### Scenario: Sync populates Palmyra
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain airfield `Palmyra` with `airdromeId` 28
  and theatre `Syria`, and country `Syria`
