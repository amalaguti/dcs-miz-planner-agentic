## ADDED Requirements

### Requirement: Spec schema tool accepts Nevada recon
`get_mission_spec_schema` SHALL accept theatre `Nevada` with mission type
`recon`. The derived example MUST follow the Nellis Creech inland envelope
(not Manston, not Batumi, not Aleppo 121/200, not north-range CAP 350/40)
and notes MUST NOT concatenate Channel template bundles that cite
french-coast 125/76.

#### Scenario: Nevada recon schema uses Nellis
- **WHEN** a caller requests the recon Spec schema with theatre `Nevada`
- **THEN** the example MUST use `Nellis`, theatre `Nevada`, Su-25T, USA,
  Russia-country trucks, no payload, and recon AOI 303° / 85 km
  (not CAP 350/40, not Aleppo 121/200, not Kutaisi 43/110, not Manston 125/76)
