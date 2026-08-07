## ADDED Requirements

### Requirement: Schema documents section orders
Agent Spec schema notes SHALL document optional `player.flight.orders` curated
ids and that free-form order strings are forbidden.

#### Scenario: Schema mentions orders
- **WHEN** requesting Spec shape for invent
- **THEN** notes MUST mention optional `player.flight.orders` and curated ids
