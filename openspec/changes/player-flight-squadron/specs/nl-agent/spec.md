## ADDED Requirements

### Requirement: Agent schema includes player flight
The derived Mission Spec schema / invent reminders SHALL document optional
`player.flight` (`size`, `role`, `ai_skill`) so the agent can propose multi-ship sections
without inventing free-form skill or aircraft fields.

#### Scenario: Schema tool shows flight fields
- **WHEN** a client requests the Mission Spec shape for invent
- **THEN** the shape MUST include optional `player.flight` with size 2–4 and role
  lead/wingman
