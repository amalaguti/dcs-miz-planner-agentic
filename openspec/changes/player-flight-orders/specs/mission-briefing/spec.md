## ADDED Requirements

### Requirement: Brief mentions section orders when armed
When `player.flight.orders` is non-empty, generated briefing/voice text SHALL
mention that F10 (or section) orders are available. Specs without orders MUST
keep prior brief behaviour for this topic.

#### Scenario: Orders brief note
- **WHEN** briefing a Spec with at least one section order
- **THEN** Procedures or Watch-outs MUST indicate available section orders
