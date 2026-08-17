## MODIFIED Requirements

### Requirement: Syria channel_place rows
Packaged `channel_place` options SHALL include `incirlik_home`,
`incirlik_iskenderun_cap`, and `aleppo_inland_strike` with
`meta.theatre: Syria`. The CAP/intercept/escort place MUST publish station
geometry 180° / 40 km / 4000 m (Incirlik south over the Gulf of Iskenderun)
and MUST NOT list `ground_attack`. The GA place MUST publish strike geometry
121° / 200 km / 2000 m (inland past Aleppo) and MUST list `ground_attack`.
The family name MUST remain `channel_place`.

#### Scenario: aleppo_inland_strike tagged Syria
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `aleppo_inland_strike` MUST include meta theatre `Syria`, domain
  land, and strike bearing 121° / distance 200 km

#### Scenario: incirlik_iskenderun_cap excludes ground_attack
- **WHEN** catalog/registry loads `incirlik_iskenderun_cap`
- **THEN** meta mission_types MUST NOT include `ground_attack`
