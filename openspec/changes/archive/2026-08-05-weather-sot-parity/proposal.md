## Why

Weather presets live in four places: `WeatherPreset` enum, `weather_presets.yaml`,
`planning_options` weather family, and `PyDCSCompiler._apply_weather` branches.
Adding a preset in one place and missing another causes validate OK / compile fail or
silent gaps (adversarial B12). A hermetic parity test locks the chain.

## What Changes

- Add a small helper that collects weather ids from enum, registry YAML, planning
  options, and compiler `_apply_weather` branches (via source inspect of enum members).
- Add pytest asserting enum ⊆ yaml ⊆ planning ⊆ compiler (and equality across the set).
- Spec requirement under `golden-fixtures` or `miz-compiler` for weather SoT parity.

## Non-goals

- New weather presets or physics changes.
- Unifying descriptions across YAML and planning_options (ids only).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `golden-fixtures`: Require weather SoT parity regression in the hermetic suite.
- `miz-compiler`: Optional cross-ref that compile-handled presets stay aligned (can fold
  into golden-fixtures only — prefer golden-fixtures).

## Impact

- New helper + test; docs/BACKLOG `#41`; delta on `golden-fixtures`.
