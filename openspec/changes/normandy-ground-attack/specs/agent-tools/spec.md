## ADDED Requirements

### Requirement: Spec schema tool accepts Normandy ground_attack
`get_mission_spec_schema` SHALL accept theatre `Normandy` with mission type
`ground_attack`. The derived example MUST follow the Needs Oar Point
ground-attack envelope (not Manston) and notes MUST NOT concatenate Channel
template bundles that cite french-coast belts or Manston YAML paths. When
mission type is `intercept`, `escort`, or `recon` on Normandy, the tool MUST
NOT return a Channel combat skeleton.

#### Scenario: Normandy ground_attack schema uses NeedsOarPoint
- **WHEN** a caller requests the ground_attack Spec schema with theatre
  `Normandy`
- **THEN** the example MUST use `NeedsOarPoint`, theatre `Normandy`, and
  strike geometry inland of Maupertus (not Manston 125° / 76 km)

#### Scenario: Normandy intercept schema still has no Manston skeleton
- **WHEN** a caller requests an intercept schema with theatre `Normandy`
- **THEN** the result MUST NOT present a Manston combat example as the
  template to copy

## MODIFIED Requirements

### Requirement: Spec schema tool accepts theatre
`get_mission_spec_schema` SHALL accept an optional theatre id. When theatre is
`Normandy` and mission type is `free_flight`, the derived example MUST follow
the Needs Oar Point envelope (not Manston). When theatre is `Normandy` and
mission type is `cap`, the derived example MUST follow the Needs Oar Point CAP
envelope (not Manston). When theatre is `Normandy` and mission type is
`ground_attack`, the derived example MUST follow the Needs Oar Point
ground-attack envelope (not Manston). When theatre is `Normandy` and mission
type is `intercept`, `escort`, or `recon`, the tool MUST NOT return a Channel
combat skeleton.

#### Scenario: Normandy free_flight schema uses NeedsOarPoint
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Normandy`
- **THEN** the example/notes MUST use `NeedsOarPoint` (not `Manston`)

#### Scenario: Normandy CAP schema uses NeedsOarPoint
- **WHEN** a caller requests the cap Spec schema with theatre `Normandy`
- **THEN** the example MUST use `NeedsOarPoint` and MUST NOT use Manston
  CAP station 135° / 25 km

#### Scenario: Normandy combat schema has no Manston skeleton
- **WHEN** a caller requests an intercept schema with theatre `Normandy`
- **THEN** the result MUST NOT present a Manston combat example as the
  template to copy

### Requirement: list_strike_targets can filter theatre
`list_strike_targets` SHALL accept an optional theatre filter. For theatre
`Normandy`, the result MUST include packaged WWII **land** strike units (not
an empty list). Sea-domain units MUST remain omitted for Normandy. For
Caucasus, Syria, Nevada, and Falklands the result MUST remain empty.

#### Scenario: Normandy strike list includes land units
- **WHEN** `list_strike_targets` is called with theatre `Normandy` after sync
- **THEN** the result MUST include a known land unit (e.g. `Blitz_36-6700A`)
  and MUST NOT include sea_craft
