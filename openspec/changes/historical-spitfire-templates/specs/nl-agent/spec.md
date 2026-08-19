## ADDED Requirements

### Requirement: Historical pattern names map to inspiration cards
Planning/chat guidance SHALL map vague Fighter Command pattern names to packaged
inspiration cards: Circus/Ramrod → `circus_escort`; Rodeo → `rodeo_sweep`;
Channel Stop / shipping strike → `channel_stop_shipping`; Noball / V-1 / ski →
`noball_ski`. Default player aircraft remains Spitfire unless the user names
Mustang/P-51.

#### Scenario: Prompt mentions Circus and Noball
- **WHEN** the planning or chat system prompt is built
- **THEN** it MUST mention those historical pattern names and the corresponding
  inspiration ids
