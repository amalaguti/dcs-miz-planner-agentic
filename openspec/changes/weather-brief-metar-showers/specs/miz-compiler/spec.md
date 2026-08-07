## ADDED Requirements

### Requirement: Compiler emits showers scattered gallery weather
When compiling a Spec with `weather: showers_scattered`, the compiler MUST apply
the invent-resolved weather snapshot and set a rainy light gallery
`cloud_preset` from that pattern’s allowed family (via existing
`CloudPreset.by_name` / base clamp path).

#### Scenario: Showers compiles with light-rain gallery
- **WHEN** a Spec with `weather: showers_scattered` and a pinned
  `weather_opts.seed` is compiled
- **THEN** the mission weather table MUST include a gallery preset string from
  the showers family (e.g. `RainyPreset4` or `NEWRAINPRESET4`)
