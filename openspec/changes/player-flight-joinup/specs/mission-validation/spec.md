## ADDED Requirements

### Requirement: Join-up validation
Shared validation SHALL accept `player.flight.join_up` as optional boolean. When
`join_up` is true and `role` is not `wingman`, validation MAY warn or ignore without
failing. Invalid types MUST fail structural load.

#### Scenario: join_up on lead does not fail
- **WHEN** a Spec sets `role: lead` and `join_up: true`
- **THEN** validation MUST succeed (join-up is a no-op for lead structure)
