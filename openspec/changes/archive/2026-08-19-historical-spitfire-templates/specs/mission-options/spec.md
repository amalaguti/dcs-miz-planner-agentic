## ADDED Requirements

### Requirement: Historical Spitfire inspiration cards
The packaged `mission_inspiration` family SHALL include advisory cards
`circus_escort`, `rodeo_sweep`, `channel_stop_shipping`, and `noball_ski`.
Each MUST map to existing Spec mission types and packaged unit/place ids
(Spitfire UK default). Cards MUST NOT authorize Lua or new Spec fields.

#### Scenario: Circus escort card present
- **WHEN** mission_inspiration options are listed after catalog sync
- **THEN** results MUST include `circus_escort` as advisory with escort
  mission type and MosquitoFBMkVI package guidance

#### Scenario: Noball ski card present
- **WHEN** mission_inspiration options are listed after catalog sync
- **THEN** results MUST include `noball_ski` as advisory pointing at
  `v1_launcher` and ground_attack
