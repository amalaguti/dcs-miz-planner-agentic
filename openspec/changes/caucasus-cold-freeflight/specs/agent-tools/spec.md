## ADDED Requirements

### Requirement: Spec schema tool accepts Caucasus
`get_mission_spec_schema` SHALL accept theatre `Caucasus`. When mission type
is `free_flight`, the derived example MUST follow the Batumi envelope (not
Manston or NeedsOarPoint). When mission type is combat including `cap`, the
tool MUST NOT return a Channel or Normandy combat skeleton.

#### Scenario: Caucasus free_flight schema uses Batumi
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Caucasus`
- **THEN** the example MUST use `Batumi`, `Su-25T`, and `Georgia`

#### Scenario: Caucasus combat schema has no Manston skeleton
- **WHEN** a caller requests a cap or intercept schema with theatre
  `Caucasus`
- **THEN** the result MUST NOT present a Manston or NeedsOarPoint example as
  the template to copy
