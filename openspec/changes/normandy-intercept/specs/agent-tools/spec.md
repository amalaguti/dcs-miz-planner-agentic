## ADDED Requirements

### Requirement: Spec schema tool accepts Normandy intercept
`get_mission_spec_schema` SHALL accept theatre `Normandy` with mission type
`intercept`. The derived example MUST follow the Needs Oar Point intercept
envelope (not Manston) and notes MUST NOT concatenate Channel template
bundles that cite Hawkinge. When mission type is `escort` or `recon` on
Normandy, the tool MUST NOT return a Channel combat skeleton.

#### Scenario: Normandy intercept schema uses NeedsOarPoint
- **WHEN** a caller requests the intercept Spec schema with theatre
  `Normandy`
- **THEN** the example MUST use `NeedsOarPoint` and theatre `Normandy` (not
  Manston)
