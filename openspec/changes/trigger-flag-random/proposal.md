## Why

R1 Channel User Files audits showed community “dynamic BoB” raid dice use ME
**Set Flag Random** (`a_set_flag_random`), not Mist. We already support radio +
late activation; without Spec `set_flag_random`, the agent cannot author that
native pattern.

## What Changes

- Mission Spec trigger action `set_flag_random` (`flag`, `min`, `max`)
- Validate min ≤ max; emit via PyDCS `SetFlagRandom`
- Example Spec + tests; planning_options / schema notes mention the action
- Optional: light behaviour-card note (not required for MVP of this change)

## Capabilities

- `mission-spec`: add `set_flag_random` action
- `compiler`: emit `a_set_flag_random`
- `validation`: range checks

## Out of Scope

- Mist/MOOSE embedding
- Full dynamic-BoB mission authoring / random group spawn Lua
- Agent immersion floor changes
