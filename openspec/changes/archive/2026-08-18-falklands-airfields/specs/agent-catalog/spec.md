## ADDED Requirements

### Requirement: Catalog lists extra Falklands airfields and Argentina country
After catalog sync from the packaged registry, known airfields MUST include
`RioGallegos` with `airdromeId` 5 and theatre `Falklands` (and the other
curated keys besides `MountPleasant`), and known countries MUST include
`Argentina` (modern). Falklands `list_strike_targets` MUST remain empty.

#### Scenario: Sync populates RioGallegos
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain airfield `RioGallegos` with `airdromeId` 5
  and theatre `Falklands`, and country `Argentina`
