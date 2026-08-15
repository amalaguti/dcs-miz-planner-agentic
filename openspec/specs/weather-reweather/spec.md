# weather-reweather

## Purpose

Overwrite weather on an existing Channel `.miz` using invent snapshots — Spec
sidecar recompile when available, otherwise weather-table patch.

## Requirements

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

### Requirement: Miz-patch reweather is TheChannel-only
The miz-zip weather patch path SHALL run only when the mission theatre is
`TheChannel`. For any other theatre it MUST fail closed (or require the Spec
sidecar recompile path) and MUST NOT build a dummy Manston/TheChannel Spec.

#### Scenario: Channel miz patch still allowed
- **WHEN** reweather patches a TheChannel `.miz` without a sibling Spec
- **THEN** the Channel weather overwrite path MUST still be available

#### Scenario: Normandy miz patch refused
- **WHEN** reweather is asked to miz-patch a Normandy `.miz` without using the
  Spec sidecar path
- **THEN** the operation MUST fail closed and MUST NOT apply Channel/Manston
  dummy Spec geometry
