## ADDED Requirements

### Requirement: list_mission_options can filter channel_place by theatre
`list_mission_options` SHALL accept an optional theatre id. When theatre is
set, returned `channel_place` rows MUST have `meta.theatre` equal to that id.
Other option families MUST still be returned. When theatre is omitted, the
tool MAY return all `channel_place` rows (backward compatible).

#### Scenario: Channel filter omits Cherbourg CAP place
- **WHEN** `list_mission_options` is called with theatre `TheChannel`
- **THEN** results MUST NOT include `cherbourg_channel_cap` or
  `needs_oar_point_home`

#### Scenario: Normandy filter omits french coast belt
- **WHEN** `list_mission_options` is called with theatre `Normandy`
- **THEN** results MUST NOT include `manston_home` or
  `french_coast_strike_belt`

## MODIFIED Requirements

### Requirement: Spec schema tool accepts theatre
`get_mission_spec_schema` SHALL accept an optional theatre id. When theatre is
`Normandy` and mission type is `free_flight`, the derived example MUST follow
the Needs Oar Point envelope (not Manston). When theatre is `Normandy` and
mission type is `cap`, the derived example MUST follow the Needs Oar Point CAP
envelope (not Manston). When theatre is `Normandy` and mission type is
`intercept`, `ground_attack`, `escort`, or `recon`, the tool MUST NOT return a
Channel combat skeleton.

#### Scenario: Normandy free_flight schema uses NeedsOarPoint
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Normandy`
- **THEN** the example/notes MUST use `NeedsOarPoint` (not `Manston`)

#### Scenario: Normandy CAP schema uses NeedsOarPoint
- **WHEN** a caller requests the cap Spec schema with theatre `Normandy`
- **THEN** the example MUST use `NeedsOarPoint` and MUST NOT use Manston
  CAP station 135° / 25 km

#### Scenario: Normandy combat schema has no Manston skeleton
- **WHEN** a caller requests an intercept or ground-attack schema with theatre
  `Normandy`
- **THEN** the result MUST NOT present a Manston combat example as the
  template to copy
