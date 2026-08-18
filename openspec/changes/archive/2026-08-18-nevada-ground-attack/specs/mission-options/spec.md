## MODIFIED Requirements

### Requirement: Nevada channel_place rows
Packaged `channel_place` options SHALL include `nellis_home`,
`nellis_north_range_cap`, and `creech_range_strike` with
`meta.theatre: Nevada`. The CAP/intercept/escort place MUST publish station
geometry 350° / 40 km / 4000 m (Nellis north over desert north-range land)
and MUST NOT list `ground_attack`. The GA place MUST publish strike geometry
303° / 85 km / 2000 m (inland past Creech) and MUST list `ground_attack`.
`nellis_home` MUST include `ground_attack`. The family name MUST remain
`channel_place`.

#### Scenario: creech_range_strike tagged Nevada
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `creech_range_strike` MUST include meta theatre `Nevada`, domain
  land, and strike bearing 303° / distance 85 km

#### Scenario: nellis_north_range_cap excludes ground_attack
- **WHEN** catalog/registry loads `nellis_north_range_cap`
- **THEN** meta mission_types MUST NOT include `ground_attack`
