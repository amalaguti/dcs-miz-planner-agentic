## MODIFIED Requirements

### Requirement: Caucasus channel_place rows
Packaged `channel_place` options SHALL include `batumi_home`,
`batumi_black_sea_cap`, and `kutaisi_inland_strike` with
`meta.theatre: Caucasus`. The CAP/intercept place MUST publish station
geometry 270° / 40 km / 4000 m (Batumi west over the Black Sea) and MUST list
`intercept` in `mission_types`. The GA place MUST publish strike geometry
43° / 110 km / 2000 m (inland past Kutaisi). The family name MUST remain
`channel_place`. Channel rows MUST keep `meta.theatre: TheChannel`.

#### Scenario: batumi_black_sea_cap includes intercept
- **WHEN** catalog/registry loads `batumi_black_sea_cap`
- **THEN** meta mission_types MUST include `intercept` as well as `cap`
