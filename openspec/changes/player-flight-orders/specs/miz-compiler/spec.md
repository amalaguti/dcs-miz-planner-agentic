## ADDED Requirements

### Requirement: Compiler emits section-order F10 packs
When `player.flight.orders` is non-empty, the compiler SHALL emit F10 radio items
and flag→AI-task wiring for each curated order id, targeting AI mates (lead) or
the AI lead group (wingman). Emit MUST use native ME / PyDCS tasks — no LLM Lua.
When `orders` is omitted or empty, the compiler MUST NOT add this feature's F10
order pack.

#### Scenario: Rejoin order wired
- **WHEN** compiling a Spec with `orders` containing `rejoin`
- **THEN** the `.miz` MUST contain a radio item for section rejoin and Follow (or
  equivalent) task wiring for the AI section
