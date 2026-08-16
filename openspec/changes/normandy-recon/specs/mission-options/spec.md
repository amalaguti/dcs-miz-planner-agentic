## MODIFIED Requirements

### Requirement: maupertus_inland_strike place
Packaged `channel_place` options SHALL include `maupertus_inland_strike` with
`meta.theatre: Normandy`, domain `land`, strike/AOI geometry 180° / 133 km /
2000 m, and mission types including `ground_attack` and `recon`. The family
name MUST remain `channel_place`.

#### Scenario: maupertus_inland_strike includes recon
- **WHEN** catalog/registry loads `maupertus_inland_strike`
- **THEN** meta mission_types MUST include `recon` as well as `ground_attack`
