## ADDED Requirements

### Requirement: Syria channel_place rows
Packaged `channel_place` options SHALL include `incirlik_home` and
`incirlik_iskenderun_cap` with `meta.theatre: Syria`. The CAP place MUST
publish station geometry 180° / 40 km / 4000 m (Incirlik south over the
Gulf of Iskenderun). The family name MUST remain `channel_place`.

#### Scenario: incirlik_iskenderun_cap tagged Syria
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `incirlik_iskenderun_cap` MUST include meta theatre `Syria` and
  CAP bearing 180° / distance 40 km
