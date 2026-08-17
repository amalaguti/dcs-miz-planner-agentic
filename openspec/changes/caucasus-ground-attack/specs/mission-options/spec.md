## ADDED Requirements

### Requirement: kutaisi_inland_strike place
Packaged `channel_place` options SHALL include `kutaisi_inland_strike` with
`meta.theatre: Caucasus`, domain `land`, and strike geometry 43° / 110 km /
2000 m (Batumi inland past Kutaisi). The family name MUST remain
`channel_place`. Channel rows MUST keep `meta.theatre: TheChannel`.

#### Scenario: kutaisi_inland_strike tagged Caucasus
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `kutaisi_inland_strike` MUST include meta theatre `Caucasus`,
  domain land, and strike bearing 43° / distance 110 km

## MODIFIED Requirements

### Requirement: Caucasus channel_place rows
Packaged `channel_place` options SHALL include `batumi_home`,
`batumi_black_sea_cap`, and `kutaisi_inland_strike` with
`meta.theatre: Caucasus`. The CAP place MUST publish station geometry 270° /
40 km / 4000 m (Batumi west over the Black Sea). The GA place MUST publish
strike geometry 43° / 110 km / 2000 m (inland past Kutaisi). The family name
MUST remain `channel_place` (not renamed to `theatre_place`). Channel rows
MUST keep `meta.theatre: TheChannel`.

#### Scenario: batumi_black_sea_cap tagged Caucasus
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `batumi_black_sea_cap` MUST include meta theatre `Caucasus` and
  CAP bearing 270° / distance 40 km
