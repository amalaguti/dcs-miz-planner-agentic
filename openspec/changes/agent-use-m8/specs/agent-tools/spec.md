## ADDED Requirements

### Requirement: Spec schema tool accepts airfield
`get_mission_spec_schema` SHALL accept an optional `airfield` id in addition to
`mission_type` and `theatre`. When airfield is a Channel extra home (Hawkinge,
Detling, BigginHill) or a Normandy extra home (Chailey, Tangmere, FordAF), the
derived example MUST follow that home envelope (place-card `cap_*` / `strike_*`
/ `escort_*`, or packaged Hawkinge YAML when type matches) and MUST NOT return
the default Manston or NeedsOarPoint station numbers. When airfield is omitted
or the theatre default home, behaviour MUST match the existing theatre-only
schema. Unknown airfield MUST be ignored (theatre default) without fabricating
a Spec.

#### Scenario: Hawkinge CAP schema via tool
- **WHEN** `get_mission_spec_schema` is called with mission_type cap, theatre
  TheChannel, and airfield Hawkinge
- **THEN** the result MUST be ok and the example `player.airfield` MUST be
  Hawkinge with CAP geometry from hawkinge_home, not 135/25

#### Scenario: Omitted airfield stays theatre default
- **WHEN** `get_mission_spec_schema` is called with mission_type cap and
  theatre TheChannel without airfield
- **THEN** the example MUST remain the Manston CAP envelope

#### Scenario: Tool definitions include airfield
- **WHEN** the standard agent tool definitions are listed
- **THEN** `get_mission_spec_schema` MUST document optional `airfield`
