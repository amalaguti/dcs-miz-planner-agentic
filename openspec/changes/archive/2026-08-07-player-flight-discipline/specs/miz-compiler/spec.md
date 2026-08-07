## ADDED Requirements

### Requirement: Compiler emits fail-to-follow discipline
When `player.flight.discipline` is armed, the compiler SHALL emit native
moving-zone + flag/message wiring that soft-warns the player after sustained
time outside the AI-lead bubble, then applies the curated hard action after
further time outside. Emit MUST NOT use LLM-authored Lua. When discipline is
omitted, the compiler MUST NOT add this feature's discipline pack. Soft warn
SHOULD set the `#15d` rejoin flag when `orders` includes `rejoin`.

#### Scenario: Soft warn wired
- **WHEN** compiling a wingman+join_up Spec with discipline armed
- **THEN** the `.miz` MUST contain moving-zone / outside-zone (or equivalent)
  conditions and a rejoin/soft-warn message path
