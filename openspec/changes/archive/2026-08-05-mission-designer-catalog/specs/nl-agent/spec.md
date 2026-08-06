## ADDED Requirements

### Requirement: Planner consults mission-designer shelves when co-authoring
Planning and interactive chat system guidance MUST instruct the agent to act as a
mission designer co-author: call `list_mission_options` for families `dynamics_mode`,
`strike_target_class`, and `channel_place` (in addition to existing behaviour/inspiration
consult) when the user discusses play-time variation, ground attack / strike composition,
or where on the Channel to fight. Guidance MUST require recommending only from those
shelves (and other packaged options), explaining tradeoffs before locking Spec fields.
Guidance MUST distinguish CLI/`randomize` (new Spec day) from `dynamics_mode` (play-time
palette deferred to Spec dynamics). The agent MUST NOT treat advisory dynamics rows as
already compile-emitted Spec fields, MUST NOT invent unit/ship ids or airdromeIds, and
MUST NOT emit LLM Lua.

#### Scenario: Prompt guidance mentions designer shelves
- **WHEN** the planning or chat system prompt is built
- **THEN** it MUST include guidance to consult `dynamics_mode`, `strike_target_class`,
  and `channel_place` options when inventing or discussing dynamics, strike targets, or
  Channel places

#### Scenario: Prompt distinguishes randomize from dynamics palette
- **WHEN** guidance describes variation / replayability
- **THEN** it MUST distinguish seeded Spec reroll (`randomize`) from play-time
  `dynamics_mode` shelves
