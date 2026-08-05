## Context

Four SoTs for weather ids; descriptions may differ — parity is **ids only**.

## Goals / Non-Goals

**Goals:** Hermetic test: enum == yaml == planning weather ids == compiler-handled ids.

**Non-Goals:** Auto-generating compiler branches; description string equality.

## Decisions

1. **`weather_sot.py`** helper returns named frozensets for tests/docs.
2. **Compiler set** from `inspect.getsource(_apply_weather)` matching `WeatherPreset.NAME`
   mapped to `.value` — fails if a branch is missing for an enum member referenced only
   in the else (else has no WeatherPreset.X).
3. **Planning** = registry planning options with `family == "weather"`.

## Risks / Trade-offs

- [Inspect brittle] → Prefer over duplicate frozenset; if rename method, test fails loudly.
