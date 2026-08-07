## Context

Player aircraft failures live in the mission-root `failures` table (ME Failures
panel: enable, After hh:mm, Within mm, probability). Stock Spitfire `.miz` files
use that table; they do not use trigger `a_set_failure`. Spitfire failure id
strings (e.g. `ENG0_MAGNETO0/1`, radiator leaks, control rods, fuel/hydraulic
pumps) come from stock Channel missions.

Acceptance (2026-08-07): `a_set_failure` with Within=0 never fired; Failures panel
with Within≥1 works. ME Within `(mm)` is **minutes**.

## Goals / Non-Goals

**Goals:** Opt-in Spec list; curated Spitfire ids; compile into Failures panel
table; validate; brief honesty; ME/Instant Action smoke.

**Non-Goals:** Free-form ids; AI-mate failures; full ME catalog dump; Lua; pool
dice beyond native probability / Within window.

## Decisions

1. **Spec shape** — optional `failures: list[FailureEvent]`:
   - `id: str` — must be in Channel catalog for `player.aircraft`
   - `start_after_s: int` ≥ 0 — After time (floored to minutes → `hh`/`mm`)
   - `probability: int` 0–100 (default 100)
   - `random_pause_s: int` ≥ 0 (default 0) — maps to Within minutes
     (`max(1, ceil(s/60))`; Within 0 never fires)
   Omit / `[]` = none.

2. **Catalog** — `data/channel/aircraft_failures.yaml` keyed by aircraft type id
   (`SpitfireLFMkIX` only in v1). Each entry: `id`, short `label`, optional `family`
   (engine|controls|fuel|…). Registry API: `list_failures(aircraft)` /
   `is_known_failure(aircraft, id)`.

3. **v1 curated set** (not exhaustive) — include at least:
   - `ENG0_MAGNETO0`, `ENG0_MAGNETO1`
   - `ENG0_WATER_RADIATOR_0_MAJOR_LEAK` (or minor)
   - `CTRL_AILERON_ROD_MAJOR_DAMAGE`, `CTRL_ELEVATOR_ROD_MAJOR_DAMAGE`,
     `CTRL_RUDDER_ROD_MAJOR_DAMAGE`
   - `FUEL_ENGINE0_FUEL_PUMP_FAILURE`
   - `HYDR_PUMP_FAILURE`
   Expand YAML later without Spec schema bump.

4. **Emit** — write `mission.failures[id]` rows (`enable`, `hh`, `mm`, `mmint`,
   `prob`, `id`) via PyDCS `mission.failures`. Do **not** emit `a_set_failure`
   triggers (stock path + Within=0 pitfall). Example messages may still use Spec
   `triggers`.

5. **Brief** — when `failures` non-empty, voice/brief mentions possible system
   failures / keep a cool head (no dumping raw ids unless useful).

6. **Randomness** — per-entry `probability` + Within minutes only in v1. Options →
   Misc → Random System Failures is separate MTBF noise, not required for scripted
   Failures panel entries.

## Risks / Trade-offs

- [Risk] Wrong/obsolete failure id → Mitigation: catalog from stock Spitfire `.miz`;
  ME smoke magneto first.
- [Risk] Minute resolution only on After/Within → Mitigation: document floor/ceil;
  example uses T+120 → After 0:02 / Within 1.
- [Risk] Catalog drift on DCS updates → Mitigation: LESSONS + re-scan stock miz.

## Migration Plan

- Additive optional field; existing Specs unchanged.

## Open Questions

- None blocking. Full catalog expansion and AI-mate failures later.
