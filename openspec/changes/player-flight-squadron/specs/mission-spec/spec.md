## ADDED Requirements

### Requirement: Optional player flight section
The Mission Spec SHALL allow an optional nested `player.flight` object on `player`.
When present it MUST declare `size` (integer 2–4 inclusive) and MAY declare `role`
(`lead` or `wingman`, default `lead`) and `ai_skill` (an AI skill name from the Channel
skill allowlist excluding `Player` and `Client`, default `Average`). When `player.flight`
is omitted, the Spec MUST continue to mean a solo player aircraft (effective size 1).
`role: wingman` MUST require `size` ≥ 2.

#### Scenario: Four-ship lead accepted
- **WHEN** a Mission Spec sets `player.flight.size` to `4` and `role` to `lead` (or omits
  role) with otherwise valid Channel player fields
- **THEN** structural load MUST succeed

#### Scenario: Pair wingman accepted
- **WHEN** a Mission Spec sets `player.flight.size` to `2` and `role` to `wingman`
- **THEN** structural load MUST succeed

#### Scenario: Solo by omission
- **WHEN** a Mission Spec omits `player.flight`
- **THEN** the Spec MUST remain valid as a solo player placement (unchanged from prior
  behaviour)

#### Scenario: Invalid size rejected
- **WHEN** a Mission Spec sets `player.flight.size` to `1` or `5`
- **THEN** loading or validation MUST fail with a clear error that size MUST be 2–4
