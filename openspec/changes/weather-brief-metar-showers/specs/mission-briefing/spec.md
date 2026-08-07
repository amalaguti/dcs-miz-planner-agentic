## ADDED Requirements

### Requirement: Briefing includes synthetic METAR from weather snapshot
When building mission briefing dictionary text, the shared commander-brief path
SHALL include one synthetic ICAO-style METAR line derived from the invent
`WeatherSnapshot` for the Spec (winds, visibility, cloud groups from packaged
gallery decode, temperature, altimeter) plus Spec date/time. The line MUST use a
fixed Channel station id suitable for Manston-centred sorties (e.g. `EGMH`), MUST
be deterministic for the same Spec + seed, MUST NOT call any network meteo API,
and MUST be marked as simulated (e.g. `NOSIG` and a `RMK SIM` or equivalent remark)
so it is not mistaken for a live observation. Legacy density patterns without a
gallery id MUST still produce a valid METAR-looking line (e.g. `CLR` clouds).

#### Scenario: Gallery pattern brief contains METAR
- **WHEN** a Spec with a gallery weather pattern and pinned `weather_opts.seed` is
  briefed for compile
- **THEN** Description or Task text MUST contain a single-line METAR including the
  fixed station id, a `Z` timestamp group, and `NOSIG`

#### Scenario: Same seed same METAR
- **WHEN** the commander brief / METAR builder runs twice for the same Spec and seed
- **THEN** the synthetic METAR line MUST be identical

#### Scenario: No network for METAR
- **WHEN** synthetic METAR is generated during brief or compile
- **THEN** the implementation MUST NOT fetch aviationweather, CheckWX, Open-Meteo,
  or any other live meteo endpoint
