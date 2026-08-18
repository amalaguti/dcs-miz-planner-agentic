## ADDED Requirements

### Requirement: Spec schema tool accepts Falklands recon
`get_mission_spec_schema` SHALL accept theatre `Falklands` with mission type
`recon`. The derived example MUST follow the East Falkland inland envelope
(not Manston, not Batumi, not Aleppo 121/200, not Creech 303/85, not South
Atlantic CAP 150/40) and notes MUST NOT concatenate Channel template bundles
that cite french-coast 125/76.

#### Scenario: Falklands recon schema uses MountPleasant
- **WHEN** a caller requests the recon Spec schema with theatre `Falklands`
- **THEN** the example MUST use `MountPleasant`, theatre `Falklands`, Su-25T,
  UK, Argentina-country trucks, no payload, and recon AOI 269° / 21 km
  (not CAP 150/40, not Nevada 303/85, not Aleppo 121/200, not Kutaisi 43/110,
  not Manston 125/76)
