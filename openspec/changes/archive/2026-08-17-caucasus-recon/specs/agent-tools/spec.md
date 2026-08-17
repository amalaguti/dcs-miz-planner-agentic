## ADDED Requirements

### Requirement: Spec schema tool accepts Caucasus recon
`get_mission_spec_schema` SHALL accept theatre `Caucasus` with mission type
`recon`. The derived example MUST follow the Batumi Kutaisi recon envelope
(not Manston) and notes MUST NOT concatenate Channel template bundles that
cite french-coast belts or Manston 125/76.

#### Scenario: Caucasus recon schema uses Batumi
- **WHEN** a caller requests the recon Spec schema with theatre `Caucasus`
- **THEN** the example MUST use `Batumi`, theatre `Caucasus`, Su-25T, and
  recon AOI 43° / 110 km (not Manston 125° / 76 km, not CAP 270° / 40 km)
