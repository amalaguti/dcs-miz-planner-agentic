## ADDED Requirements

### Requirement: Expanded shelf covered by examples and tests
Hermetic tests SHALL assert new registry ids, class shelf membership, AAA AI
class for new flak ids, and at least one example Spec using a new AAA unit and
one using a new sea unit compile/validate.

#### Scenario: Shelf expand tests green
- **WHEN** registry / catalog / target AI / example tests run in CI
- **THEN** they MUST pass and fail if promoted ids or class lists regress
