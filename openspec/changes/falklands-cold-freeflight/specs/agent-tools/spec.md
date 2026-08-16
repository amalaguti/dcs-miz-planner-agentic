## ADDED Requirements

### Requirement: Spec schema tool accepts Falklands
`get_mission_spec_schema` SHALL accept theatre `Falklands`. When mission type
is `free_flight`, the derived example MUST follow the Mount Pleasant envelope
(not Manston, NeedsOarPoint, Batumi, Incirlik, or Nellis) and notes MUST NOT
concatenate Channel/prior-map template bundles. When mission type is combat
including `cap`, the tool MUST NOT return a prior-map combat skeleton.

#### Scenario: Falklands free_flight schema uses MountPleasant
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Falklands`
- **THEN** the example MUST use `MountPleasant`, `Su-25T`, and `UK`

#### Scenario: Falklands combat schema has no Manston skeleton
- **WHEN** a caller requests a cap or intercept schema with theatre
  `Falklands`
- **THEN** the result MUST NOT present a Manston, NeedsOarPoint, Batumi,
  Incirlik, or Nellis example as the template to copy
