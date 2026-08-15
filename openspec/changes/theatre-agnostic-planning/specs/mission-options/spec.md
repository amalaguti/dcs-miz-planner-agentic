## ADDED Requirements

### Requirement: channel_place rows declare TheChannel
Packaged `channel_place` planning options SHALL declare theatre `TheChannel`
in option meta. The family name MUST remain `channel_place` (not renamed to
`theatre_place` in this change). No Normandy place rows SHALL be added.

#### Scenario: french_coast_strike_belt tagged TheChannel
- **WHEN** catalog/registry loads `channel_place` options
- **THEN** `french_coast_strike_belt` MUST include meta theatre `TheChannel`
  (or equivalent) and MUST NOT appear as a Normandy place
