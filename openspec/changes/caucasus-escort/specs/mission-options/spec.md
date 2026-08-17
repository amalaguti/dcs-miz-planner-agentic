## MODIFIED Requirements

### Requirement: Caucasus channel_place rows
Packaged `channel_place` options SHALL include `batumi_home`,
`batumi_black_sea_cap`, and `kutaisi_inland_strike` with
`meta.theatre: Caucasus`. The CAP/intercept/escort place MUST publish station
geometry 270° / 40 km / 4000 m (Batumi west over the Black Sea) and MUST list
mission types including `cap`, `intercept`, and `escort`. The GA place MUST
publish strike geometry 43° / 110 km / 2000 m (inland past Kutaisi). The family
name MUST remain `channel_place` (not renamed to `theatre_place`). Channel rows
MUST keep `meta.theatre: TheChannel`.
Normandy rows MUST keep `meta.theatre: Normandy`.

#### Scenario: batumi_black_sea_cap tagged Caucasus
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `batumi_black_sea_cap` MUST include meta theatre `Caucasus` and
  CAP bearing 270° / distance 40 km

#### Scenario: batumi_black_sea_cap includes intercept
- **WHEN** catalog/registry loads `batumi_black_sea_cap`
- **THEN** meta mission_types MUST include `intercept` as well as `cap`

#### Scenario: batumi_black_sea_cap includes escort
- **WHEN** catalog/registry loads `batumi_black_sea_cap`
- **THEN** meta mission_types MUST include `escort` as well as `cap` and
  `intercept`
