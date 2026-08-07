## ADDED Requirements

### Requirement: Section order validation
Shared validation SHALL reject unknown order ids and SHALL reject `orders` when
`player.flight` is absent. Validation MUST NOT invent order identifiers.

#### Scenario: Unknown order id rejected
- **WHEN** a Spec sets `player.flight.orders` to include an unknown id
- **THEN** validation MUST fail with a clear unknown-order error

#### Scenario: Orders without flight rejected
- **WHEN** a Spec sets section orders without `player.flight`
- **THEN** validation MUST fail (Pydantic/extra forbid or explicit path error)
