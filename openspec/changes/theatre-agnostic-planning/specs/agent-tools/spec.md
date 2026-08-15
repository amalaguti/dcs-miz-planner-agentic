## ADDED Requirements

### Requirement: Spec schema tool accepts theatre
`get_mission_spec_schema` SHALL accept an optional theatre id. When theatre is
`Normandy` and mission type is `free_flight`, the derived example MUST follow
the Needs Oar Point envelope (not Manston). When theatre is `Normandy` and
mission type is combat, the tool MUST NOT return a Channel combat skeleton.

#### Scenario: Normandy free_flight schema uses NeedsOarPoint
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Normandy`
- **THEN** the example/notes MUST use `NeedsOarPoint` (not `Manston`)

#### Scenario: Normandy combat schema has no Manston skeleton
- **WHEN** a caller requests an intercept or ground-attack schema with theatre
  `Normandy`
- **THEN** the result MUST NOT present a Manston combat example as the
  template to copy

### Requirement: list_strike_targets can filter theatre
`list_strike_targets` SHALL accept an optional theatre filter. For theatre
`Normandy` before a Normandy target batch ships, the result MUST be empty (not
Channel trucks).

#### Scenario: Normandy strike list empty
- **WHEN** `list_strike_targets` is called with theatre `Normandy` after sync
- **THEN** the result MUST be an empty list
