## ADDED Requirements

### Requirement: Spec schema tool accepts Normandy recon
`get_mission_spec_schema` SHALL accept theatre `Normandy` with mission type
`recon`. The derived example MUST follow the Needs Oar Point recon envelope
(not Manston) and notes MUST NOT concatenate Channel template bundles that
cite french-coast belts or Manston 125/76.

#### Scenario: Normandy recon schema uses NeedsOarPoint
- **WHEN** a caller requests the recon Spec schema with theatre `Normandy`
- **THEN** the example MUST use `NeedsOarPoint`, theatre `Normandy`, and
  recon AOI 180° / 133 km (not Manston 125° / 76 km)
