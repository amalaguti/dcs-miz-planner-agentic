## ADDED Requirements

### Requirement: Discipline validation
Shared validation SHALL reject `player.flight.discipline` when flight is absent,
`role` is not `wingman`, or `join_up` is false. Validation SHALL reject unknown
`hard` action ids and out-of-range radius/timing. Validation MUST NOT invent
discipline identifiers.

#### Scenario: Discipline on lead rejected
- **WHEN** a Spec sets `discipline` with `role: lead`
- **THEN** validation MUST fail with a clear role/join_up error

#### Scenario: Unknown hard action rejected
- **WHEN** `discipline.hard` is not a curated id
- **THEN** validation MUST fail with a clear unknown-hard-action error
