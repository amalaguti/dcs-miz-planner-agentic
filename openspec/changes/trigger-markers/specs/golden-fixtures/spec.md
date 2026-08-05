## ADDED Requirements

### Requirement: Mark and smoke example is covered
The repository MUST include a checked-in Spec that uses `mark` and/or `smoke` actions
referencing a Spec zone, with at least one observable companion action (e.g. `message`).
Tests MUST assert validation and compile emit mark-to-all and/or smoke-marker structure
for the referenced zone.

#### Scenario: Mark/smoke compile structure
- **WHEN** the mark/smoke example is compiled in tests
- **THEN** the resulting `.miz` MUST include mark-to-all and/or smoke-marker predicates
  consistent with the Spec
