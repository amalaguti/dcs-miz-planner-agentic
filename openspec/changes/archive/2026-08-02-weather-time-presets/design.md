## Context

`WeatherPreset` today is only `sunny_clear`. `_apply_weather` clears clouds/fog/dust and
sets 80 km visibility. Planning options already advertise advisory `time_of_day` ids
(`dawn` → `06:00`, etc.) and a single supported weather id. Backlog M5 `#17` asks for
named presets verified in-game: sunny, dawn, marginal VFR.

Constraint: PyDCS `clouds_iprecptns` must be `Weather.Preceptions` enum, not int
(`LESSONS_LEARNED`).

## Goals / Non-Goals

**Goals:**

- Spec + registry + compiler support for `sunny_clear`, a dawn-oriented preset, and
  `marginal_vfr` (ids below).
- Advisory `time_of_day` remains the way to suggest clock time; document pairings
  (dawn weather ↔ ~06:00, sunny ↔ ~09:00, marginal ↔ flexible).
- Examples + tests; in-game visual accept.

**Non-Goals:**

- New Spec field for time-of-day enum; full ME weather authoring surface; multi-theatre.

## Decisions

1. **Preset ids (v1)**
   - `sunny_clear` — unchanged (clear, 80 km, no fog/dust).
   - `dawn_clear` — clear/high visibility with light haze feel (mild fog or slightly
     reduced visibility vs sunny; no precip). Pairs with `time_of_day: dawn` / `06:00`.
   - `marginal_vfr` — broken/overcast density, lower cloud base, visibility in marginal
     VFR band (~5–8 km), no heavy precip. Suitable for harder Channel hops.
   - Alternatives considered: single `dawn` weather id — rejected to avoid colliding with
     `time_of_day: dawn` advisory id; keep weather ids distinct.

2. **Spec stays `weather` + `start_time`**
   - Do not add `atmosphere` or `time_of_day` Spec enums. Agent/planning options continue
     to map time_of_day → `start_time`.

3. **Compiler mapping**
   - Explicit branches in `_apply_weather` per enum member (no free-form YAML→PyDCS
     script). Tune numbers during apply; lock after in-game accept + goldens.
   - Always use `Weather.Preceptions.*` for precip.

4. **Examples**
   - Keep `manston_cold_freeflight.yaml` as sunny `09:00`.
   - Add `examples/manston_dawn_freeflight.yaml` (`dawn_clear`, `06:00`) and
     `examples/manston_marginal_vfr.yaml` (`marginal_vfr`, e.g. `10:00`) as free-flight
     accept slices (minimal placement change).

5. **Planning options / catalog**
   - Mark new weather ids `supported`; leave `time_of_day` advisory unless we later
     compile-bind them (we do not in this change).

6. **Goldens**
   - Extend contracts or add a small golden for dawn and/or marginal (mission weather
     fields differ from sunny). Refresh free-flight golden only if sunny mapping changes.

## Risks / Trade-offs

- [Weather looks wrong in ME] → Iterate numbers after Instant Action; record final values
  in LESSONS.
- [Fog vs haze confusion] → Prefer visibility/cloud density over heavy fog for dawn.
- [Enum + YAML + planning drift] → Same three-place update pattern as other registry ids;
  catalog sync after YAML change.

## Migration Plan

1. YAML + enum + planning options + validation/registry tests.
2. Compiler branches + unit/compile asserts.
3. Examples + golden/contracts; catalog sync note in README if needed.
4. In-game accept three looks; docs/BACKLOG.

## Open Questions

- Exact cloud density / visibility numbers — finalize during apply + DCS accept (start from
  design defaults; adjust once).
