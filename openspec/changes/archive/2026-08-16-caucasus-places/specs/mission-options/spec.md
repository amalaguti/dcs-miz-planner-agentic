## ADDED Requirements

### Requirement: Caucasus channel_place rows
Packaged `channel_place` options SHALL include `batumi_home` and
`batumi_black_sea_cap` with `meta.theatre: Caucasus`. The CAP place MUST
publish station geometry 270° / 40 km / 4000 m (Batumi west over the Black
Sea). The family name MUST remain `channel_place` (not renamed to
`theatre_place`). Channel rows MUST keep `meta.theatre: TheChannel`.
Normandy rows MUST keep `meta.theatre: Normandy`.

#### Scenario: batumi_black_sea_cap tagged Caucasus
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `batumi_black_sea_cap` MUST include meta theatre `Caucasus` and
  CAP bearing 270° / distance 40 km
