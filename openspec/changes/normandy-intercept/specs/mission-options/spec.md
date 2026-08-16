## MODIFIED Requirements

### Requirement: Normandy channel_place rows
Packaged `channel_place` options SHALL include `needs_oar_point_home`,
`cherbourg_channel_cap`, and `maupertus_inland_strike` with
`meta.theatre: Normandy`. The CAP/intercept place MUST publish station
geometry 180° / 63 km / 4000 m and MUST list mission types including `cap`
and `intercept`. The family name MUST remain `channel_place`.

#### Scenario: cherbourg_channel_cap includes intercept
- **WHEN** catalog/registry loads `cherbourg_channel_cap`
- **THEN** meta mission_types MUST include `intercept` as well as `cap`
