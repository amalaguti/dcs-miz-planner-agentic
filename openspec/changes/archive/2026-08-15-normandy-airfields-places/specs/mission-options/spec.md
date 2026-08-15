## ADDED Requirements

### Requirement: Normandy channel_place rows
Packaged `channel_place` options SHALL include `needs_oar_point_home` and
`cherbourg_channel_cap` with `meta.theatre: Normandy`. The CAP place MUST
publish station geometry 180° / 63 km / 4000 m (Needs Oar Point toward
Maupertus midpoint). The family name MUST remain `channel_place` (not renamed
to `theatre_place`). Channel rows MUST keep `meta.theatre: TheChannel`.

#### Scenario: cherbourg_channel_cap tagged Normandy
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `cherbourg_channel_cap` MUST include meta theatre `Normandy` and
  CAP bearing 180° / distance 63 km

## MODIFIED Requirements

### Requirement: channel_place rows declare TheChannel
Packaged `channel_place` planning options that describe Channel geography
SHALL declare theatre `TheChannel` in option meta. The family name MUST remain
`channel_place` (not renamed to `theatre_place` in this change). Normandy place
rows MAY exist when they declare `meta.theatre: Normandy`.

#### Scenario: french_coast_strike_belt tagged TheChannel
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `french_coast_strike_belt` MUST include meta theatre `TheChannel`
  (or equivalent) and MUST NOT appear as a Normandy place
