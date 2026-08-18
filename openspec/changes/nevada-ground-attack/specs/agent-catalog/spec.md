## MODIFIED Requirements

### Requirement: Strike units are era- and theatre-tagged
Catalog strike-unit rows SHALL remain tagged `theatre_id=Caucasus` /
`era_id=modern` for packaged modern trucks. Query-time listing for theatre
`Nevada` SHALL dual-offer those modern **land** rows (same pattern as Syria).
Channel MUST NOT receive Ural ids. Syria dual-offer MUST stay. Falklands MUST
stay empty.

#### Scenario: Nevada query dual-offers Caucasus modern land trucks
- **WHEN** catalog lists strike units for theatre `Nevada`
- **THEN** `Ural-375`, `GAZ-66`, and `ZIL-135` MUST be offerable without
  changing stored `theatre_id` away from `Caucasus`
