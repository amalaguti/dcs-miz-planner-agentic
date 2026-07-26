## Context

Free-flight Manston is production-quality (validate, compile, goldens, in-game). Spec still
refuses non-empty `enemies`/`objectives`/`triggers`. Concept example and judgment memo both
point at a Channel intercept next. Registry already lists `Bf-109K-4` with German VHF radio.

## Goals / Non-Goals

**Goals:**

- Represent and compile one checked-in intercept: player Spitfire at Manston, enemy
  `Bf-109K-4` flight, Channel, early morning, clear weather.
- Shared validation allows that shape; free_flight behaviour unchanged.
- Hermetic golden for intercept structural contracts; in-game accept.

**Non-Goals:**

- Agent/NL; full objectives engine; triggers/Lua; new mission types; dawn weather preset
  unless trivial; inventing DCS ids or map coords without a documented source.

## Decisions

1. **`mission_type: intercept`** (string enum value `intercept`)
   - Concept YAML used `interception`; product enum stays short kebab-style like `free_flight`.
   - Alternative rejected: overload `free_flight` with enemies — unclear validation rules.

2. **Typed enemy entries, minimal fields for v1**
   - e.g. `aircraft` (DCS id), `count` (int ≥ 1), optional `skill` defaulting to Average/High
     as design picks from PyDCS skills already used.
   - No free-form Lua or payload CLSIDs in v1.

3. **Objectives: minimal stub that validates**
   - Either a single structured object `{ "type": "intercept_enemy" }` or a one-item list.
   - Compiler may treat it as documentation / future hook; must not silently drop unknown
     objective types — unknown types fail validation.

4. **Enemy placement: fixed Channel coordinates for the example**
   - Capture coords from a stock/user Channel mission or terrain-relative point near Dover
     approach; record source in LESSONS or example comment. Inject via compiler constants
     or a small registry `intercept_spawns` table if reusable.
   - Alternative rejected: LLM-chosen lat/lon.

5. **Time/weather for “dawn”**
   - Use early `start_time` (e.g. `06:00`) + existing `sunny_clear` to avoid new preset work.
   - `dawn_clear` deferred to M5 weather presets.

6. **Triggers remain empty in v1**
   - Non-empty `triggers` still fail. Stock IA scaffolding not required for accept if mission
     loads and flights are present.

7. **Goldens**
   - New fixture dir `tests/fixtures/manston_intercept/` (name finalized in apply) with
     normalized mission + contracts (enemy type, player, theatre, frequency bands).
   - Free-flight golden untouched.

## Risks / Trade-offs

- [Wrong / off-map enemy coords] → Source from stock Channel mission extract; verify in ME.
- [Bf-109 radio 40 MHz omitted] → Set group frequency from registry like Spitfire.
- [Payload KeyError on enemy spawn] → Reuse `_disable_payload_scan` for all unit types used.
- [Scope creep into triggers] → Explicit non-goal; fail if triggers non-empty.

## Migration Plan

1. Spec/models + validation first (tests for free_flight still refuse enemies).
2. Compiler intercept path + example YAML.
3. Golden + refresh helper sibling.
4. In-game accept; docs/BACKLOG building → done.

## Open Questions

- Exact Dover-approach map x/y: resolve during apply from local research/stock extract (must
  be documented; do not invent).
