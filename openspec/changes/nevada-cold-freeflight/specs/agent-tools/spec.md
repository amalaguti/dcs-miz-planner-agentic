## ADDED Requirements

### Requirement: Spec schema tool accepts Nevada
`get_mission_spec_schema` SHALL accept theatre `Nevada`. When mission type
is `free_flight`, the derived example MUST follow the Nellis envelope (not
Manston, NeedsOarPoint, Batumi, or Incirlik) and notes MUST NOT concatenate
Channel/Normandy/Caucasus/Syria template bundles. When mission type is combat
including `cap`, the tool MUST NOT return a prior-map combat skeleton.

#### Scenario: Nevada free_flight schema uses Nellis
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Nevada`
- **THEN** the example MUST use `Nellis`, `Su-25T`, and `USA`

#### Scenario: Nevada combat schema has no Manston skeleton
- **WHEN** a caller requests a cap or intercept schema with theatre
  `Nevada`
- **THEN** the result MUST NOT present a Manston, NeedsOarPoint, Batumi, or
  Incirlik example as the template to copy
