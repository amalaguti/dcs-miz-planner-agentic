## MODIFIED Requirements

### Requirement: Nevada channel_place rows
Packaged `channel_place` `nellis_north_range_cap` SHALL list mission types
including `cap` and `intercept`. `nellis_home` MUST include `intercept`.

#### Scenario: nellis_north_range_cap includes intercept
- **WHEN** catalog/registry loads `nellis_north_range_cap`
- **THEN** meta mission_types MUST include `intercept` as well as `cap`
