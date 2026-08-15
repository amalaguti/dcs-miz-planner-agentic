## ADDED Requirements

### Requirement: Catalog lists curated Normandy airfields
After catalog sync from the packaged registry, known airfields for theatre
`Normandy` MUST include the curated keys `NeedsOarPoint`, `Chailey`,
`Funtington`, `Tangmere`, `FordAF`, `Maupertus`, `SaintPierreduMont`, and
`Carpiquet` with their packaged `airdromeId` values.

#### Scenario: Sync populates FordAF
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain airfield `FordAF` with theatre `Normandy`
  and `airdromeId` 31
