## Why

Only `sunny_clear` is a compile-backed weather preset; dawn and marginal-VFR Channel
sorties still cannot be expressed without inventing weather. Time-of-day planning options
are advisory only. M5 immersion needs named weather + verified clock times that look right
in DCS ME / Instant Action.

## What Changes

- Add compile-backed weather presets beyond `sunny_clear`: at least **dawn-oriented** and
  **marginal VFR** (exact ids in design), with Channel registry YAML + Spec enum +
  compiler mappings (PyDCS weather fields; respect `Preceptions` enum lesson).
- Keep Spec fields separate: `weather` + `start_time` (no combined Spec block). Promote
  matching `time_of_day` / weather planning options to `supported` where compile-backed.
- Checked-in example Specs (or free-flight variants) for sunny morning, dawn, and marginal
  VFR; golden/contract coverage for new weather output.
- In-game accept: open each example in DCS and confirm sky/visibility/time look correct.

## Non-goals

- Full dynamic weather / seasons / cyclones / custom cloud presets from ME authoring UI.
- Changing mission types, briefing `l10n`, or triggers.
- Making `time_of_day` a Mission Spec enum (stays advisory → `start_time` guidance).
- Multi-theatre weather tables beyond Channel.

## Capabilities

### New Capabilities
- (none — extends existing weather/time behaviour)

### Modified Capabilities
- `mission-spec`: Expand allowed `weather` preset values for schema_version `"1"`.
- `reference-registry`: Channel `weather_presets.yaml` lists the new presets.
- `miz-compiler`: Compile maps each new preset to concrete PyDCS weather settings.
- `mission-options`: Weather (and related time_of_day) support levels reflect compile
  backing.
- `mission-validation`: Unknown weather still fails; new ids validate when registered.
- `golden-fixtures`: Cover at least one non-sunny compile path (or contracts).

## Impact

- `models.WeatherPreset`, `data/channel/weather_presets.yaml`, `planning_options.yaml`
- `compiler/pydcs_compiler.py` (`_apply_weather`)
- Examples + tests/goldens; catalog sync picks up registry YAML
- README / BACKLOG / LESSONS after in-game verify
