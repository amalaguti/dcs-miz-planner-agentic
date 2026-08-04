## ADDED Requirements

### Requirement: Narrative escort example is covered
The repository MUST include a checked-in escort Spec with `narrative.enabled` and tests
MUST assert expansion validates and compiles with native trigger structure (messages
and/or mission_end).

#### Scenario: Narrative escort compile structure
- **WHEN** the narrative escort example is expanded and compiled in tests
- **THEN** the resulting `.miz` MUST include trigger rules consistent with the pack
