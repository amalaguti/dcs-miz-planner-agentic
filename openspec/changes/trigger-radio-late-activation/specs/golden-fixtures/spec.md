## ADDED Requirements

### Requirement: Radio late-activation example is covered
The repository MUST include a checked-in Spec that uses F10 radio items and late-activated
enemy (or target) groups, and tests MUST assert validation and compile emit radio-item and
activate-group structure (and late activation on the group where applicable).

#### Scenario: Radio late-activation compile structure
- **WHEN** the radio / late-activation example is compiled in tests
- **THEN** the resulting `.miz` MUST include radio-item and activate-group markers
  consistent with the Spec
