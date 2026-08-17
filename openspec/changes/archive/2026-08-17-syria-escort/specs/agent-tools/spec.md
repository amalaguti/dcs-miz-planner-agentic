## ADDED Requirements

### Requirement: Spec schema tool accepts Syria escort
`get_mission_spec_schema` SHALL accept theatre `Syria` with mission type
`escort`. The derived example MUST follow the Incirlik Iskenderun escort
envelope (not Manston, not Batumi, not Needs Oar Point) and notes MUST NOT
concatenate Channel template bundles that cite Manston 120/55. When mission
type is `ground_attack` or `recon` on Syria, the tool MUST NOT return a
Channel combat skeleton.

#### Scenario: Syria escort schema uses Incirlik
- **WHEN** a caller requests the escort Spec schema with theatre `Syria`
- **THEN** the example MUST use `Incirlik`, theatre `Syria`, Su-25T, Turkey
  package, Syria bounce, and escort geometry 180° / 40 km (not Manston 120° /
  55 km, not Cherbourg 180/63, not Batumi 270/40)

#### Scenario: Syria ground_attack schema still has no Manston skeleton
- **WHEN** a caller requests a ground_attack schema with theatre `Syria`
- **THEN** the result MUST NOT present a Manston combat example as the
  template to copy
