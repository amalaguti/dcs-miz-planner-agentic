## ADDED Requirements

### Requirement: Spec schema tool accepts Syria intercept
`get_mission_spec_schema` SHALL accept theatre `Syria` with mission type
`intercept`. The derived example MUST follow the Incirlik dawn intercept
envelope (not Hawkinge/Dover, not Cherbourg, not Batumi).

#### Scenario: Syria intercept schema uses Incirlik
- **WHEN** a caller requests the intercept Spec schema with theatre `Syria`
- **THEN** the example MUST use `Incirlik`, theatre `Syria`, Su-25T, and
  country-Syria opposition
