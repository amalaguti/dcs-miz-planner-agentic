## ADDED Requirements

### Requirement: Re-weather overwrites mission weather
The system SHALL provide an API to change weather on an existing Channel `.miz`
to a named WeatherPreset, applying invent snapshot resolution (`weather-invent`),
and MUST overwrite the target `.miz` path. When a sibling Spec YAML exists (or an
explicit Spec path is given), the system MUST update the Spec weather (and seed)
and recompile onto that `.miz`. When no Spec is available, the system MUST load
the `.miz`, apply the weather snapshot to the mission weather table, and save
in place. Groups and triggers present in the loaded mission MUST remain.

#### Scenario: Spec sidecar recompile
- **WHEN** re-weather is invoked on a `.miz` that has a sibling Spec YAML and a
  valid new weather pattern
- **THEN** the Spec MUST be updated and the `.miz` MUST be overwritten with the
  new weather while remaining a valid compile of that Spec

#### Scenario: Miz-only patch
- **WHEN** re-weather is invoked on a `.miz` without a Spec sidecar
- **THEN** the `.miz` MUST be overwritten with updated static weather and MUST
  still load in PyDCS
