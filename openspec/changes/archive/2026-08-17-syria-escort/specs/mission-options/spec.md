## MODIFIED Requirements

### Requirement: Syria channel_place rows
Packaged `channel_place` options SHALL include `incirlik_home` and
`incirlik_iskenderun_cap` with `meta.theatre: Syria`. The CAP/intercept/escort
place MUST publish station geometry 180° / 40 km / 4000 m (Incirlik south over
the Gulf of Iskenderun) and MUST list mission types including `cap`,
`intercept`, and `escort`. The family name MUST remain `channel_place` (not
renamed to `theatre_place`). Channel rows MUST keep `meta.theatre: TheChannel`.
Normandy rows MUST keep `meta.theatre: Normandy`. Caucasus rows MUST keep
`meta.theatre: Caucasus`.

#### Scenario: incirlik_iskenderun_cap tagged Syria
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `incirlik_iskenderun_cap` MUST include meta theatre `Syria` and
  CAP bearing 180° / distance 40 km

#### Scenario: incirlik_iskenderun_cap includes intercept
- **WHEN** catalog/registry loads `incirlik_iskenderun_cap`
- **THEN** meta mission_types MUST include `intercept` as well as `cap`

#### Scenario: incirlik_iskenderun_cap includes escort
- **WHEN** catalog/registry loads `incirlik_iskenderun_cap`
- **THEN** meta mission_types MUST include `escort` as well as `cap` and
  `intercept`
