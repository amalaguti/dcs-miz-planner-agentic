## ADDED Requirements

### Requirement: Falklands channel_place rows
Packaged `channel_place` options SHALL include `mount_pleasant_home` and
`mount_pleasant_south_atlantic_cap` with `meta.theatre: Falklands`. The CAP
place MUST publish station geometry 150° / 40 km / 4000 m (Mount Pleasant SSE
over the South Atlantic). The family name MUST remain `channel_place`.

#### Scenario: mount_pleasant_south_atlantic_cap tagged Falklands
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `mount_pleasant_south_atlantic_cap` MUST include meta theatre
  `Falklands` and CAP bearing 150° / distance 40 km
