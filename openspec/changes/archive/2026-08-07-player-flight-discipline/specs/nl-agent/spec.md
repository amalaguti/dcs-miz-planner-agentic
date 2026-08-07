## ADDED Requirements

### Requirement: Schema documents discipline
Agent Spec schema notes SHALL document optional `player.flight.discipline`
(radius, soft/hard timing, curated hard actions) and that it applies only to
wingman + join_up.

#### Scenario: Schema mentions discipline
- **WHEN** requesting Spec shape for invent
- **THEN** notes MUST mention optional `player.flight.discipline` and constraints
