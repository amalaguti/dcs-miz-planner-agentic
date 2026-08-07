## ADDED Requirements

### Requirement: Optional flight join-up flag
The Mission Spec SHALL allow optional `player.flight.join_up` (boolean, default
`true`). When `role` is `wingman` and `join_up` is true, the compiler MUST emit
Follow/shared-route behaviour per miz-compiler. When `join_up` is false, wingman
placement MUST remain separate groups without Follow (as `#15b`). For `role: lead`,
`join_up` MUST NOT change group structure (same-group section).

#### Scenario: Wingman join-up default
- **WHEN** a Spec sets `player.flight.role: wingman` and omits `join_up`
- **THEN** structural load MUST succeed and join-up MUST be treated as enabled

#### Scenario: Wingman join-up opt-out
- **WHEN** a Spec sets `player.flight.role: wingman` and `join_up: false`
- **THEN** structural load MUST succeed
