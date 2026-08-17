## ADDED Requirements

### Requirement: Spec schema tool accepts Caucasus intercept
`get_mission_spec_schema` SHALL accept theatre `Caucasus` with mission type
`intercept`. The derived example MUST follow the Batumi dawn-intercept
envelope (not Manston, not Needs Oar Point, not Hawkinge) and notes MUST NOT
concatenate Channel template bundles that cite Hawkinge. When mission type is
`escort` or `recon` on Caucasus, the tool MUST NOT return a Channel combat
skeleton.

#### Scenario: Caucasus intercept schema uses Batumi
- **WHEN** a caller requests the intercept Spec schema with theatre
  `Caucasus`
- **THEN** the example MUST use `Batumi`, theatre `Caucasus`, Su-25T, and
  Russia opposition (not Hawkinge / Manston)

#### Scenario: Caucasus escort schema still has no Manston skeleton
- **WHEN** a caller requests an escort schema with theatre `Caucasus`
- **THEN** the result MUST NOT present a Manston combat example as the
  template to copy
