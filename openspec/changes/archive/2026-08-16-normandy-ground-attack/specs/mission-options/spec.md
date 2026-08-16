## ADDED Requirements

### Requirement: maupertus_inland_strike place
Packaged `channel_place` options SHALL include `maupertus_inland_strike` with
`meta.theatre: Normandy`, domain `land`, and strike geometry 180° / 133 km /
2000 m (Needs Oar Point inland of Maupertus). The family name MUST remain
`channel_place`. Channel rows MUST keep `meta.theatre: TheChannel`.

#### Scenario: maupertus_inland_strike tagged Normandy
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `maupertus_inland_strike` MUST include meta theatre `Normandy`,
  domain land, and strike bearing 180° / distance 133 km

## MODIFIED Requirements

### Requirement: Normandy channel_place rows
Packaged `channel_place` options SHALL include `needs_oar_point_home`,
`cherbourg_channel_cap`, and `maupertus_inland_strike` with
`meta.theatre: Normandy`. The CAP place MUST publish station geometry 180° /
63 km / 4000 m (Needs Oar Point toward Maupertus midpoint). The GA place MUST
publish strike geometry 180° / 133 km / 2000 m (inland of Maupertus). The
family name MUST remain `channel_place` (not renamed to `theatre_place`).
Channel rows MUST keep `meta.theatre: TheChannel`.

#### Scenario: cherbourg_channel_cap tagged Normandy
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `cherbourg_channel_cap` MUST include meta theatre `Normandy` and
  CAP bearing 180° / distance 63 km
