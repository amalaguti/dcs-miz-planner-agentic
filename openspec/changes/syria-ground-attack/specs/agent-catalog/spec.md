## MODIFIED Requirements

### Requirement: Strike units are era- and theatre-tagged
Catalog strike-unit rows SHALL remain tagged `theatre_id=Caucasus` /
`era_id=modern` for packaged modern trucks. Query-time listing for theatre
`Syria` SHALL dual-offer those modern **land** rows (same pattern as Normandy
WWII land dual-offer). Channel MUST NOT receive Ural ids. Nevada and
Falklands MUST stay empty.

#### Scenario: Syria query dual-offers Caucasus modern land trucks
- **WHEN** catalog lists strike units for theatre `Syria`
- **THEN** `Ural-375`, `GAZ-66`, and `ZIL-135` MUST be offerable without
  changing stored `theatre_id` away from `Caucasus`
