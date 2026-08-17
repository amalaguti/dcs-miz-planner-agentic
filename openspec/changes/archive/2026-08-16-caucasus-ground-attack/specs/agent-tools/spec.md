## ADDED Requirements

### Requirement: Spec schema tool accepts Caucasus ground_attack
`get_mission_spec_schema` SHALL accept theatre `Caucasus` with mission type
`ground_attack`. The derived example MUST follow the Batumi inland
ground-attack envelope (not Manston, not Needs Oar Point) and notes MUST NOT
concatenate Channel template bundles that cite french-coast belts or Manston
YAML paths. When mission type is `intercept`, `escort`, or `recon` on
Caucasus, the tool MUST NOT return a Channel combat skeleton.

#### Scenario: Caucasus ground_attack schema uses Batumi
- **WHEN** a caller requests the ground_attack Spec schema with theatre
  `Caucasus`
- **THEN** the example MUST use `Batumi`, theatre `Caucasus`, Su-25T, and
  strike geometry inland past Kutaisi (not Manston 125° / 76 km, not CAP
  270° / 40 km)

#### Scenario: Caucasus intercept schema still has no Manston skeleton
- **WHEN** a caller requests an intercept schema with theatre `Caucasus`
- **THEN** the result MUST NOT present a Manston combat example as the
  template to copy

## MODIFIED Requirements

### Requirement: list_strike_targets can filter theatre
`list_strike_targets` SHALL accept an optional theatre filter. For theatre
`Normandy`, the result MUST include packaged WWII **land** strike units (not
an empty list). Sea-domain units MUST remain omitted for Normandy. For theatre
`Caucasus`, the result MUST include packaged modern **land** trucks (e.g.
`Ural-375`) and MUST NOT include WWII Channel trucks or sea_craft. For Syria,
Nevada, and Falklands the result MUST remain empty.

#### Scenario: Normandy strike list includes land units
- **WHEN** `list_strike_targets` is called with theatre `Normandy` after sync
- **THEN** the result MUST include a known land unit (e.g. `Blitz_36-6700A`)
  and MUST NOT include sea_craft

#### Scenario: Caucasus strike list includes modern trucks
- **WHEN** `list_strike_targets` is called with theatre `Caucasus` after sync
- **THEN** the result MUST include `Ural-375` and MUST NOT include
  `Blitz_36-6700A` or sea_craft
