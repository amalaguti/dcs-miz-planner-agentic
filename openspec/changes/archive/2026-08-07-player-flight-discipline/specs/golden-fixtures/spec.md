## ADDED Requirements

### Requirement: Structural asserts for discipline
Tests SHALL assert that a Spec with `player.flight.discipline` armed compiles to
mission content containing moving-zone / outside-zone (or equivalent) wiring and
does not invent Lua for this feature.

#### Scenario: Discipline example golden smoke
- **WHEN** the suite compiles the checked-in discipline example
- **THEN** asserts MUST find outside-moving-zone (or documented equivalent) wiring
  and a soft-warn message path
