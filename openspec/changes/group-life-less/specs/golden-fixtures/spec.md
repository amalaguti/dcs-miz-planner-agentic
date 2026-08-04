## ADDED Requirements

### Requirement: Group life less example is covered
The repository MUST include a checked-in Spec that uses a `group_life_less` condition
(enemy or target index + percent) with at least one observable action (e.g. `message`).
Tests MUST assert validation and compile emit group-life-less structure for the referenced
placed group.

#### Scenario: Group life less compile structure
- **WHEN** the group-life-less example is compiled in tests
- **THEN** the resulting `.miz` MUST include group-life-less markers consistent with the
  Spec
