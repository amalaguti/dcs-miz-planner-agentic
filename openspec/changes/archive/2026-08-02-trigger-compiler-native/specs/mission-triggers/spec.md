## ADDED Requirements

### Requirement: Validated triggers are compileable
A Spec that passes shared validation for typed zones/triggers MUST be accepted by the
compiler for native emit (subject to registry/install checks). The system MUST NOT leave
validated trigger graphs as validate-only once native compile is implemented.

#### Scenario: Valid sample is not refused
- **WHEN** the checked-in free-flight trigger sample validates successfully
- **THEN** compile MUST proceed to write a `.miz` (not a not-implemented refusal)
