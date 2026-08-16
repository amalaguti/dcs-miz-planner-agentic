## ADDED Requirements

### Requirement: Spec schema tool accepts Normandy escort
`get_mission_spec_schema` SHALL accept theatre `Normandy` with mission type
`escort`. The derived example MUST follow the Needs Oar Point escort envelope
(not Manston) and notes MUST NOT concatenate Channel template bundles that
cite Manston 120/55. When mission type is `recon` on Normandy, the tool MUST
NOT return a Channel combat skeleton.

#### Scenario: Normandy escort schema uses NeedsOarPoint
- **WHEN** a caller requests the escort Spec schema with theatre `Normandy`
- **THEN** the example MUST use `NeedsOarPoint`, theatre `Normandy`, and
  escort geometry 180° / 63 km (not Manston 120° / 55 km)
