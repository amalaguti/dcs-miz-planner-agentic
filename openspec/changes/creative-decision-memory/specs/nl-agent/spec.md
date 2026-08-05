## ADDED Requirements

### Requirement: Planner biases creative choices from memory
Planning and chat system guidance MUST instruct the agent, when inventing immersion on
vague asks, to consult generation history (and prefs when present) after listing
mission options, and to prefer behaviours that past feedback scored well while
soft-avoiding poorly scored ones — still emitting at most one or two supported
behaviours, never Lua, and never forcing narrative when hand triggers exist.

#### Scenario: Prompt mentions history bias for creativity
- **WHEN** the planning or chat system prompt is built
- **THEN** it MUST mention consulting generation history / feedback (or derived bias)
  when choosing mission_behaviour recipes on vague asks
