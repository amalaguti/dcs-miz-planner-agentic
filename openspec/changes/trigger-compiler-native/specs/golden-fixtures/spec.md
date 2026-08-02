## ADDED Requirements

### Requirement: Trigger sample structural coverage
The test suite SHALL assert that compiling the checked-in trigger sample produces a `.miz`
whose mission member includes expected native trigger predicates for the sample rule
(time-after and out-text). Full golden refresh of all combat fixtures is NOT required solely
for empty-trigger missions.

#### Scenario: Sample trig predicates present
- **WHEN** the free-flight trigger sample is compiled in tests
- **THEN** assertions MUST find time-after and out-text (or equivalent) markers in the
  mission member
