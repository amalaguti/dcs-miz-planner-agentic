## ADDED Requirements

### Requirement: Compiler applies shared weather snapshot helper
The compiler weather apply path SHALL use a shared helper that can also apply an
invent `WeatherSnapshot` to an already-loaded PyDCS Mission (for re-weather
miz-patch), including gallery clamp and wind layers.

#### Scenario: Snapshot apply reusable
- **WHEN** a WeatherSnapshot is applied to a loaded Mission
- **THEN** cloud preset / fog / wind fields MUST match invent compile behaviour
  for the same snapshot
