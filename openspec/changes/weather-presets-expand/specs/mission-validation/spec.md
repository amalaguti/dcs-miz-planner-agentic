## ADDED Requirements

### Requirement: Weather SoT parity includes expanded patterns
Weather SoT parity checks MUST require enum, YAML preset keys, planning_options
weather ids, and compiler-supported presets to stay aligned when patterns are
added.

#### Scenario: Parity green after expand
- **WHEN** `collect_weather_sot` / weather parity tests run after this change
- **THEN** all surfaces MUST list the same expanded weather id set
