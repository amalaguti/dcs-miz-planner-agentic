## MODIFIED Requirements

### Requirement: Syria channel_place rows
Packaged `channel_place` `aleppo_inland_strike` SHALL list mission types
including `ground_attack` and `recon`. `incirlik_home` MUST include `recon`.
`incirlik_iskenderun_cap` MUST NOT list `recon`.

#### Scenario: aleppo_inland_strike includes recon
- **WHEN** catalog/registry loads `aleppo_inland_strike`
- **THEN** meta mission_types MUST include `recon` as well as `ground_attack`
