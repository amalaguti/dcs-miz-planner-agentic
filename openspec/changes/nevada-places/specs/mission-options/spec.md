## ADDED Requirements

### Requirement: Nevada channel_place rows
Packaged `channel_place` options SHALL include `nellis_home` and
`nellis_north_range_cap` with `meta.theatre: Nevada`. The CAP place MUST
publish station geometry 350° / 40 km / 4000 m (Nellis north over desert
north-range land). The family name MUST remain `channel_place`.

#### Scenario: nellis_north_range_cap tagged Nevada
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `nellis_north_range_cap` MUST include meta theatre `Nevada` and
  CAP bearing 350° / distance 40 km
