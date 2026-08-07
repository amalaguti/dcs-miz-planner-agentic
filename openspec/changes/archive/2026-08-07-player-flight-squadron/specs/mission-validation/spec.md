## ADDED Requirements

### Requirement: Player flight validation
Shared validation SHALL enforce `player.flight` rules when the object is present: `size`
in 2–4; `role` in `lead`|`wingman`; `ai_skill` in the AI allowlist (not `Player` /
`Client`); `player.skill` MUST be `Player` when flight is present; `role: wingman`
requires `size` ≥ 2. Validation MUST NOT invent aircraft ids or allow free-form skill
strings outside the allowlist.

#### Scenario: Client skill rejected with flight
- **WHEN** a Spec sets `player.flight` and `player.skill` to `Client`
- **THEN** validation MUST fail with a clear error that the human slot MUST be `Player`

#### Scenario: AI skill Player rejected
- **WHEN** a Spec sets `player.flight.ai_skill` to `Player`
- **THEN** validation MUST fail with a clear error that mates MUST use an AI skill
