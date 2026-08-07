## Why

Channel briefs still describe weather only in prose from registry descriptions, while
gallery recipes already encode winds, QNH, temp, and cloud layers that could become a
deterministic ICAO-style METAR line. Separately, our rainy gallery only covers
`RainyPreset1`–`3` (overcast rain); light-rain / showery Channel days need
`RainyPreset4`–`6` / `NEWRAINPRESET4` without live METAR.

## What Changes

- Add an offline synthetic METAR line derived from invent `WeatherSnapshot` (+ Spec
  date/time) into squadron-commander / compile briefing text (fixed Channel ICAO
  flavour, e.g. Manston-style — not a live observation).
- Add a named Spec weather pattern for light rain / scattered showers using the
  rainy light gallery ids (`RainyPreset4`, `NEWRAINPRESET4`, `RainyPreset5`,
  `RainyPreset6`) with recipe + invent family + planning_options + SoT parity.
- Document upstream `CloudPresets` / `DecodePreset` taxonomy in gitignored
  `research/weather.md` as R10 audit reference (local research only; not shipped).

## Non-goals

- Live aviationweather / CheckWX / Open-Meteo (or any network meteo) in invent or brief.
- Shipping or shelling out to dcs-real-weather Go binary.
- Dust / thunderstorm precip enums beyond gallery rainy presets.
- Changing ME Dynamic / fog_dynamics behaviour.
- Per-airfield real ICAO codes as Spec fields (fixed synthetic station is enough).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-briefing`: Description/Task include a synthetic METAR from invent snapshot.
- `squadron-voice`: Commander brief includes the same synthetic METAR line.
- `mission-spec`: New `WeatherPreset` id for light-rain / showers pattern.
- `reference-registry`: YAML recipe + gallery_family for the new pattern; packaged
  decode map for gallery → METAR cloud groups.
- `miz-compiler`: Compiles the new pattern via existing weather invent/apply path.
- `mission-options`: Catalog lists the new weather id as supported.
- `mission-validation`: Accepts the new id; weather SoT parity includes it.
- `weather-invent`: Within-family pick among light-rain gallery ids; seed unchanged.
- `golden-fixtures`: Optional example/contract for showers + METAR line hermetic.

## Impact

- `weather_invent` / briefing / voice modules; `weather_presets.yaml`; `WeatherPreset`
  enum; planning_options; examples + optional golden/contract asserts for METAR line
  and showers recipe.
- Acceptance: open an example `.miz` with `showers_*` weather in ME (gallery rainy light)
  and confirm Description/Task shows a METAR-looking line; no network calls.
