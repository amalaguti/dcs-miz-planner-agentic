## ADDED Requirements

### Requirement: Structural asserts for Failures table
Tests SHALL assert that a Spec with a curated failure compiles to mission content
containing the failure id and an enabled Failures panel table row (not
`a_set_failure`).

#### Scenario: Failure example golden smoke
- **WHEN** the suite compiles the checked-in failures example
- **THEN** asserts MUST find the failure id and enabled Failures table wiring
