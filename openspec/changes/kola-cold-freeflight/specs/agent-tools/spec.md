## ADDED Requirements

### Requirement: Spec schema tool accepts Kola
`get_mission_spec_schema` SHALL accept theatre `Kola`. When mission type is
`free_flight`, the derived example MUST follow the Bodo envelope (not
Manston, NeedsOarPoint, Batumi, Incirlik, Nellis, or MountPleasant) and
notes MUST NOT concatenate Channel/prior-map template bundles. When mission
type is combat including `cap`, the tool MUST NOT return a prior-map combat
skeleton.

#### Scenario: Kola free_flight schema uses Bodo
- **WHEN** a caller requests the free_flight Spec schema with theatre `Kola`
- **THEN** the example MUST use `Bodo`, `Su-25T`, and `Norway`

#### Scenario: Kola combat schema has no Manston skeleton
- **WHEN** a caller requests a cap or intercept schema with theatre `Kola`
- **THEN** the result MUST NOT present a Manston, NeedsOarPoint, Batumi,
  Incirlik, Nellis, or MountPleasant example as the template to copy
