## ADDED Requirements

### Requirement: Golden fixture for player flight
The repository SHALL include a golden / structural fixture covering a multi-unit player
flight (at least size 2 with `role: lead`) that asserts group size and Player skill on the
lead unit after compile.

#### Scenario: Lead pair golden
- **WHEN** the golden suite compiles the checked-in player-flight example Spec
- **THEN** asserts MUST confirm the player group has the Spec size and the lead unit
  skill is `Player`
