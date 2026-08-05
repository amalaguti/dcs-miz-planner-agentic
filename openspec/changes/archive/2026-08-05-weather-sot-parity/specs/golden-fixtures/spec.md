## ADDED Requirements

### Requirement: Weather preset SoT parity
The test suite SHALL assert that Mission Spec weather preset ids are aligned across the
`WeatherPreset` enum, Channel `weather_presets.yaml` (registry), `planning_options`
weather family ids, and the presets explicitly handled by the compiler weather apply
path. The sets MUST be equal (no enum-only, YAML-only, planning-only, or
compiler-orphan ids). Ordinary pytest MUST run this check hermetically without a DCS
install.

#### Scenario: Weather id sets match
- **WHEN** the weather SoT parity test runs
- **THEN** enum, registry YAML, planning weather options, and compiler-handled preset
  ids MUST be the same non-empty set
