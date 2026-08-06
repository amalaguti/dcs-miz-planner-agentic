## ADDED Requirements

### Requirement: Weather recipes package cloud presets
Packaged Channel weather YAML SHALL describe each WeatherPreset with a
pilot-facing description and a compile recipe that MAY include a modern ME
`cloud_preset` id (`PresetN` / `RainyPresetN`) plus numeric fields (base,
visibility, fog, temperature, QNH, turbulence, ground wind) used by the compiler.

#### Scenario: Gallery recipe declared
- **WHEN** catalog/registry loads weather presets after this change
- **THEN** at least one expanded pattern MUST declare a non-empty `cloud_preset`
  matching a PyDCS-known gallery id
