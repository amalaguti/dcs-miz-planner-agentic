## ADDED Requirements

### Requirement: Spec schema tool accepts Nevada intercept
`get_mission_spec_schema` SHALL accept theatre `Nevada` with mission type
`intercept`. The derived example MUST follow the Nellis dawn intercept
envelope (not Hawkinge/Dover, not Incirlik, not Batumi, not Cherbourg).

#### Scenario: Nevada intercept schema uses Nellis
- **WHEN** a caller requests the intercept Spec schema with theatre `Nevada`
- **THEN** the example MUST use `Nellis`, theatre `Nevada`, Su-25T, USA, and
  country-Russia opposition
