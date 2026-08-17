## MODIFIED Requirements

### Requirement: Nevada channel_place rows
Packaged `channel_place` `nellis_north_range_cap` SHALL list mission types
including `cap`, `intercept`, and `escort`. `nellis_home` MUST include
`escort`.

#### Scenario: nellis_north_range_cap includes escort
- **WHEN** catalog/registry loads `nellis_north_range_cap`
- **THEN** meta mission_types MUST include `escort` as well as `cap` and
  `intercept`
