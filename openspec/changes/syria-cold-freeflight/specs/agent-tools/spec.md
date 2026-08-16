## ADDED Requirements

### Requirement: Spec schema tool accepts Syria
`get_mission_spec_schema` SHALL accept theatre `Syria`. When mission type
is `free_flight`, the derived example MUST follow the Incirlik envelope (not
Manston, NeedsOarPoint, or Batumi) and notes MUST NOT concatenate
Channel/Normandy/Caucasus template bundles. When mission type is combat
including `cap`, the tool MUST NOT return a Channel, Normandy, or Caucasus
combat skeleton.

#### Scenario: Syria free_flight schema uses Incirlik
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Syria`
- **THEN** the example MUST use `Incirlik`, `Su-25T`, and `Turkey`

#### Scenario: Syria combat schema has no Manston skeleton
- **WHEN** a caller requests a cap or intercept schema with theatre
  `Syria`
- **THEN** the result MUST NOT present a Manston, NeedsOarPoint, or Batumi
  example as the template to copy
