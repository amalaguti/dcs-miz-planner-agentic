## ADDED Requirements

### Requirement: Compiler emits gallery weather recipes
When compiling a Spec weather pattern whose recipe includes `cloud_preset`, the
compiler MUST set PyDCS `Weather.clouds_preset` via `CloudPreset.by_name`, clamp
cloud base to that preset’s allowed range, and apply recipe fog/visibility/temp/
QNH/turbulence/ground wind. Patterns without `cloud_preset` MAY keep the legacy
density/thickness path. Unsupported recipe preset ids MUST fail clearly before
writing a `.miz`.

#### Scenario: Rain overcast compiles with RainyPreset
- **WHEN** a Spec with a rain-overcast pattern is compiled
- **THEN** the mission weather table MUST include the corresponding rainy gallery
  preset string (e.g. `RainyPreset1`)

#### Scenario: Legacy sunny still compiles
- **WHEN** `examples/manston_cold_freeflight.yaml` (sunny_clear) is compiled
- **THEN** compile MUST succeed and prior clear-weather visibility behaviour MUST
  remain acceptable (high visibility, no fog unless recipe says otherwise)
