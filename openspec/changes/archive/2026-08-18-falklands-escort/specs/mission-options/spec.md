## MODIFIED Requirements

### Requirement: Falklands channel_place rows
Packaged `channel_place` options SHALL include `mount_pleasant_home` and
`mount_pleasant_south_atlantic_cap` with `meta.theatre: Falklands`. The CAP
place MUST publish station geometry 150° / 40 km / 4000 m (Mount Pleasant SSE
over the South Atlantic). `mount_pleasant_south_atlantic_cap` SHALL list
mission types including `cap`, `intercept`, and `escort`.
`mount_pleasant_home` MUST include `escort`. The family name MUST remain
`channel_place`.

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
