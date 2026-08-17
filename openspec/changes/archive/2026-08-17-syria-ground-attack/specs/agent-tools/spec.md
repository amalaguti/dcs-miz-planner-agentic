## ADDED Requirements

### Requirement: Spec schema tool accepts Syria ground_attack
`get_mission_spec_schema` SHALL accept theatre `Syria` with mission type
`ground_attack`. The derived example MUST follow the Incirlik Aleppo inland
envelope (not Manston, not Batumi, not Iskenderun CAP 180/40) and notes MUST
NOT concatenate Channel template bundles that cite french-coast 125/76. When
mission type is `recon` on Syria, the tool MUST NOT return a Channel combat
skeleton.

#### Scenario: Syria ground_attack schema uses Incirlik
- **WHEN** a caller requests the ground_attack Spec schema with theatre `Syria`
- **THEN** the example MUST use `Incirlik`, theatre `Syria`, Su-25T, payload
  `su25t_2x_fab250`, Syria-country trucks, and strike geometry 121° / 200 km
  (not CAP 180/40, not Kutaisi 43/110, not Manston 125/76)

#### Scenario: Syria recon schema still has no Manston skeleton
- **WHEN** a caller requests a recon schema with theatre `Syria`
- **THEN** the result MUST NOT present a Manston combat example as the
  template to copy

## MODIFIED Requirements

### Requirement: list_strike_targets theatre filter
`list_strike_targets(theatre="Syria")` SHALL return the packaged modern land
trucks (`Ural-375`, `GAZ-66`, `ZIL-135`). Stored `theatre_id` MAY remain
`Caucasus`. Channel lists MUST still exclude those ids. Nevada and Falklands
lists MUST stay empty.

#### Scenario: Syria strike list includes modern trucks
- **WHEN** a caller lists strike targets with theatre `Syria`
- **THEN** the result MUST include `Ural-375` and MUST NOT include Channel
  WWII `Blitz`
