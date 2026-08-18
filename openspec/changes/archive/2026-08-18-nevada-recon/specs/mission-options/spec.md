## MODIFIED Requirements

### Requirement: Nevada channel_place rows
Packaged `channel_place` `creech_range_strike` SHALL list mission types
including `ground_attack` and `recon`. `nellis_home` MUST include `recon`.
`nellis_north_range_cap` MUST NOT list `recon` (or `ground_attack`).

#### Scenario: creech_range_strike includes recon
- **WHEN** catalog/registry loads `creech_range_strike`
- **THEN** meta mission_types MUST include `recon` as well as `ground_attack`
