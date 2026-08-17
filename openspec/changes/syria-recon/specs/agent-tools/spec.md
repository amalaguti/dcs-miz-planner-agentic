## ADDED Requirements

### Requirement: Spec schema tool accepts Syria recon
`get_mission_spec_schema` SHALL accept theatre `Syria` with mission type
`recon`. The derived example MUST follow the Incirlik Aleppo inland envelope
(not Manston, not Batumi, not Iskenderun CAP 180/40) and notes MUST NOT
concatenate Channel template bundles that cite french-coast 125/76.

#### Scenario: Syria recon schema uses Incirlik
- **WHEN** a caller requests the recon Spec schema with theatre `Syria`
- **THEN** the example MUST use `Incirlik`, theatre `Syria`, Su-25T, Syria-country
  trucks, and recon AOI 121° / 200 km (not CAP 180/40, not Kutaisi 43/110,
  not Manston 125/76)
