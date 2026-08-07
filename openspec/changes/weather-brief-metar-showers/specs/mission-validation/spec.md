## ADDED Requirements

### Requirement: Validate showers scattered weather
The shared validation engine SHALL accept Channel Specs with
`weather: showers_scattered` when the id is packaged in the registry, and MUST
continue to reject unknown weather ids.

#### Scenario: Showers validates
- **WHEN** a Spec uses `weather: showers_scattered` on Channel with known player
  assets
- **THEN** validation MUST succeed for weather

### Requirement: Weather SoT parity includes showers scattered
Weather SoT parity checks MUST include `showers_scattered` across enum, YAML
preset keys, planning_options weather ids, and compiler-supported presets.

#### Scenario: Parity includes showers
- **WHEN** `collect_weather_sot` / weather parity tests run after this change
- **THEN** all surfaces MUST list `showers_scattered` in the same weather id set
