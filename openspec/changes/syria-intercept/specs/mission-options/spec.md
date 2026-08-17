## MODIFIED Requirements

### Requirement: Syria channel_place rows
Packaged `channel_place` `incirlik_iskenderun_cap` SHALL list mission types
including `cap` and `intercept`. `incirlik_home` MUST include `intercept`.

#### Scenario: incirlik_iskenderun_cap includes intercept
- **WHEN** catalog/registry loads `incirlik_iskenderun_cap`
- **THEN** meta mission_types MUST include `intercept` as well as `cap`
