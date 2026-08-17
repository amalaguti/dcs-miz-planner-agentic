## MODIFIED Requirements

### Requirement: kutaisi_inland_strike place
Packaged `channel_place` options SHALL include `kutaisi_inland_strike` with
`meta.theatre: Caucasus`, domain `land`, strike/AOI geometry 43° / 110 km /
2000 m, and mission types including `ground_attack` and `recon`. The family
name MUST remain `channel_place`.

#### Scenario: kutaisi_inland_strike includes recon
- **WHEN** catalog/registry loads `kutaisi_inland_strike`
- **THEN** meta mission_types MUST include `recon` as well as `ground_attack`
