## ADDED Requirements

### Requirement: Narrative intercept example is covered
The repository MUST include a checked-in intercept Spec with `narrative.enabled` and
tests MUST assert expansion validates and compiles with native trigger structure
(scramble message and/or mission_end).

#### Scenario: Narrative intercept compile structure
- **WHEN** the narrative intercept example is expanded and compiled in tests
- **THEN** the resulting `.miz` MUST include trigger rules consistent with the pack
