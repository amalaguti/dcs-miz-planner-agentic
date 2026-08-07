## ADDED Requirements

### Requirement: Structural asserts for section orders
Tests SHALL assert that a Spec with curated `player.flight.orders` compiles to
mission content containing radio-item / section-order wiring and does not invent
Lua for this feature.

#### Scenario: Orders example golden smoke
- **WHEN** the suite compiles the checked-in section-orders example
- **THEN** asserts MUST find radio / order flag wiring for a selected order id
