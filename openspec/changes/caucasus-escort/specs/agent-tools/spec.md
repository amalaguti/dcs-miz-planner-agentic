## ADDED Requirements

### Requirement: Spec schema tool accepts Caucasus escort
`get_mission_spec_schema` SHALL accept theatre `Caucasus` with mission type
`escort`. The derived example MUST follow the Batumi Black Sea escort envelope
(not Manston, not Needs Oar Point) and notes MUST NOT concatenate Channel
template bundles that cite Manston 120/55. When mission type is `recon` on
Caucasus, the tool MUST NOT return a Channel combat skeleton.

#### Scenario: Caucasus escort schema uses Batumi
- **WHEN** a caller requests the escort Spec schema with theatre `Caucasus`
- **THEN** the example MUST use `Batumi`, theatre `Caucasus`, Su-25T, Georgia
  package, and escort geometry 270° / 40 km (not Manston 120° / 55 km)

#### Scenario: Caucasus recon schema still has no Manston skeleton
- **WHEN** a caller requests a recon schema with theatre `Caucasus`
- **THEN** the result MUST NOT present a Manston combat example as the
  template to copy
