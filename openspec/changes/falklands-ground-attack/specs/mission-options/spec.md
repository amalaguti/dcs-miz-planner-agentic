## MODIFIED Requirements

### Requirement: Falklands channel_place rows
Packaged `channel_place` options SHALL include `mount_pleasant_home`,
`mount_pleasant_south_atlantic_cap`, and `east_falkland_inland_strike` with
`meta.theatre: Falklands`. The CAP place MUST publish station geometry 150° /
40 km / 4000 m (South Atlantic sea) and MUST NOT list `ground_attack`. The GA
place MUST publish strike geometry 269° / 21 km / 2000 m (inland short of
Goose Green) and MUST list `ground_attack`. `mount_pleasant_home` MUST include
`ground_attack`. The family name MUST remain `channel_place`.

#### Scenario: mount_pleasant_south_atlantic_cap tagged Falklands
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `mount_pleasant_south_atlantic_cap` MUST include meta theatre
  `Falklands` and CAP bearing 150° / distance 40 km

#### Scenario: mount_pleasant_south_atlantic_cap includes intercept
- **WHEN** catalog/registry loads `mount_pleasant_south_atlantic_cap`
- **THEN** meta mission_types MUST include `intercept` as well as `cap`

#### Scenario: mount_pleasant_south_atlantic_cap includes escort
- **WHEN** catalog/registry loads `mount_pleasant_south_atlantic_cap`
- **THEN** meta mission_types MUST include `escort` as well as `cap` and
  `intercept`

#### Scenario: east_falkland_inland_strike tagged Falklands
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `east_falkland_inland_strike` MUST include meta theatre
  `Falklands`, domain land, and strike bearing 269° / distance 21 km

#### Scenario: mount_pleasant_south_atlantic_cap excludes ground_attack
- **WHEN** catalog/registry loads `mount_pleasant_south_atlantic_cap`
- **THEN** meta mission_types MUST NOT include `ground_attack`
