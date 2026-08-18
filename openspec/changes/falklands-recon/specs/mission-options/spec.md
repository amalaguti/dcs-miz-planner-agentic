## MODIFIED Requirements

### Requirement: Falklands channel_place rows
Packaged `channel_place` `east_falkland_inland_strike` SHALL list mission
types including `ground_attack` and `recon`. `mount_pleasant_home` MUST
include `recon`. `mount_pleasant_south_atlantic_cap` MUST NOT list `recon`
(or `ground_attack`).

#### Scenario: east_falkland_inland_strike includes recon
- **WHEN** catalog/registry loads `east_falkland_inland_strike`
- **THEN** meta mission_types MUST include `recon` as well as `ground_attack`
