## ADDED Requirements

### Requirement: Compiler emits multi-unit player flight
When `player.flight` is present with `role: lead` (or default), the compiler SHALL
create one player aircraft group with `group_size` equal to Spec `size`, place all
units at the Spec airfield with the Spec start type and aircraft id, set the first
unit to skill `Player`, and set all other units to Spec `ai_skill` (default
`Average`). When `role: wingman`, the compiler SHALL emit **two** groups: an AI lead
group of size `size - 1` (all `ai_skill`) named distinctly from the player group, and
a size-1 player group with skill `Player` on its first (only) unit — MUST NOT place
`Player` on a non-first unit of a mixed group (DCS single-player will not hand control).
Group radio frequency and mission-type tasking MUST apply to the player group.
When `player.flight` is omitted, the compiler MUST emit a single-unit Player group as
today. Player-bound trigger conditions MUST use the human unit id (player group unit 0).

#### Scenario: Lead four-ship compile
- **WHEN** compiling a free-flight Spec with `player.flight.size: 4` and `role: lead`
- **THEN** the `.miz` MUST contain a player group of four `SpitfireLFMkIX` units with the
  first unit skill `Player` and the other three AI-skilled, cold at the Spec airfield

#### Scenario: Wingman pair compile
- **WHEN** compiling a Spec with `player.flight.size: 2` and `role: wingman`
- **THEN** the `.miz` MUST contain a separate AI lead group (one AI-skilled unit) and a
  size-1 player group with skill `Player` on its only unit

#### Scenario: Solo unchanged
- **WHEN** compiling a Spec that omits `player.flight`
- **THEN** the compiler MUST still emit a one-unit Player group as before
