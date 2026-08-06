## ADDED Requirements

### Requirement: Compiler emits curated fog animation DoScript
When `fog_dynamics` is set, the compiler MUST emit a native ONCE trigger that
fires after `start_after_s` and runs a curated `DoScript` calling
`world.weather.setFogAnimation` with params derived only from Spec fields.
Unsupported modes MUST fail before writing a `.miz`. The Lua text MUST come from
a human-authored template, not from the LLM.

#### Scenario: Burn-off emits setFogAnimation
- **WHEN** a Spec with `fog_dynamics.mode: burn_off` is compiled
- **THEN** the `.miz` mission/dictionary MUST contain `setFogAnimation` and the
  configured duration
