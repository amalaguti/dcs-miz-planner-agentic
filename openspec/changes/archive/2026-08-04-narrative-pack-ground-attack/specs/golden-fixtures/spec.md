## ADDED Requirements

### Requirement: Narrative ground-attack example is covered
The repository MUST include a checked-in ground_attack Spec with `narrative.enabled` and
tests MUST assert expansion validates and compiles with native trigger structure
(messages and/or mission_end, and target_dead / group-dead).

#### Scenario: Narrative ground-attack compile structure
- **WHEN** the narrative ground_attack example is expanded and compiled in tests
- **THEN** the resulting `.miz` MUST include trigger rules consistent with the pack
