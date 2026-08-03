## ADDED Requirements

### Requirement: Narrative CAP example is covered
The repository MUST include a checked-in CAP Spec that enables narrative (or documents
expansion) and tests MUST assert that after expansion the Spec validates and compiles
with non-empty native-trigger structure (zone and/or message / mission_end rules).

#### Scenario: Narrative CAP compile structure
- **WHEN** the narrative CAP example is expanded and compiled in tests
- **THEN** the resulting `.miz` mission tables MUST include trigger rules consistent with
  the expanded Spec (e.g. message and/or mission end actions)
