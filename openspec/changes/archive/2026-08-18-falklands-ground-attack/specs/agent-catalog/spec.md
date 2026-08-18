## MODIFIED Requirements

### Requirement: Catalog lists extra Falklands airfields and Argentina country
After catalog sync from the packaged registry, known airfields MUST include
`RioGallegos` with `airdromeId` 5 and theatre `Falklands` (and the other
curated keys besides `MountPleasant`), and known countries MUST include
`Argentina` (modern). `list_strike_targets(theatre=Falklands)` MUST dual-offer
Caucasus modern land trucks (same query-time predicate as Syria/Nevada).
Stored `theatre_id` MUST remain `Caucasus`. Channel MUST NOT receive Ural ids.

#### Scenario: Sync populates RioGallegos
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain airfield `RioGallegos` with `airdromeId` 5
  and theatre `Falklands`, and country `Argentina`

#### Scenario: Falklands strike listing dual-offers modern land trucks
- **WHEN** catalog/tools list strike units for theatre `Falklands`
- **THEN** `Ural-375`, `GAZ-66`, and `ZIL-135` MUST be present and Channel
  WWII trucks MUST be absent
