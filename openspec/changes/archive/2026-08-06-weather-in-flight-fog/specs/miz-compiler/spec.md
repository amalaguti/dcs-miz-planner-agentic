## ADDED Requirements

### Requirement: Compiler emits curated fog animation script
When `fog_dynamics` is set, the compiler MUST emit a native ONCE trigger that
fires after `start_after_s` and runs curated Lua calling
`world.weather.setFogAnimation` with params derived only from Spec fields
(prefer `DoScriptFile` + miz resource over DictKey `DoScript`). Unsupported
modes MUST fail before writing a `.miz`. The Lua text MUST come from a
human-authored template, not from the LLM.

#### Scenario: Burn-off emits setFogAnimation
- **WHEN** a Spec with `fog_dynamics.mode: burn_off` is compiled
- **THEN** the `.miz` MUST contain `setFogAnimation` (mission resource and/or
  trigger wiring) and the configured duration
