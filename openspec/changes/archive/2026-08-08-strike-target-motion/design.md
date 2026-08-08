## Context

Today `_apply_ground_attack` / `_apply_recon` place each `targets[]` entry once via
`mission.ship_group` / `vehicle_group` with a small lateral spread — no route.
PyDCS `ShipGroup` / `VehicleGroup` already expose `add_waypoint`. Domain validation
(`channel_domain`) already classifies strike/AOI points as land|sea.

Channel registry v1 units that can demonstrate motion: sea (`Uboat_VIIC`, E-boat,
dry cargo) and land soft vehicles (`Blitz_36-6700A`, …). AAA stays static by policy.

## Goals / Non-Goals

**Goals:**

- Optional per-target motion that is backward compatible (omit = static).
- Native ME waypoints only (no Lua) for land and sea groups.
- Agent/examples prefer motion where it fits (open sea, convoys); static for docks/AAA.
- Update U-boat mid-Channel examples to patrol; one truck path example.

**Non-Goals:**

- Crash-dive / ASW / submerge AI.
- Auto-snap to DCS rail mesh; curated train corridors (later).
- Free-form LLM routes; Mist/MOOSE.
- Expanding registry with tanks/troops/trains (motion Spec works when those land).
- Changing strike/AOI geometry model (bearing/distance of the target *area* stays).

## Decisions

### 1. Spec shape on `GroundTarget`

```yaml
# omit or:
motion: static

motion: patrol
patrol_radius_m: 2000   # required when motion=patrol; clamp e.g. 500–15000

motion: path
path:                     # 2–6 points, airfield-relative like strike/recon
  - bearing_deg: 140
    distance_km: 40
  - bearing_deg: 145
    distance_km: 42
# loop implied (return to first / ME route loop)
```

- **Why nested on each target:** one Spec can mix static AAA and a moving truck.
- **Why airfield-relative path points:** same contract as strike/recon geometry;
  no raw map x/y in Spec.
- **Alternatives:** mission-level motion only (rejected — mixed targets); absolute
  lat/lon (rejected — Channel Spec style is airfield-relative).

### 2. Compiler emit

- **static / omit:** unchanged single placement at AOI/strike offset.
- **patrol:** place group at first corner; add remaining circle waypoints; loop via
  `SwitchWaypoint`.
- **path:** spawn at first path point; add remaining; loop.
- **Speed:** curated bands in `data/channel/target_motion.yaml` (PyDCS has no
  MaxSpeed). Omit `speed_kmh` → seeded cruise in [min, max] (`weather_opts.seed`
  or Spec name hash); waypoints jitter around cruise (within-mission pacing).
  Optional Spec `speed_kmh` clamped to the unit profile.
- **Disperse Under Fire:** moving land groups get `OptDisparseUnderFire` (default
  180s) on WP0 — built-in AI scatter when attacked from the air. Spec
  `disperse_under_fire_s` (0=off, or custom seconds). Sea skips.


### 3. Validation

- Unknown `motion` → reject.
- `patrol` requires `patrol_radius_m` in range; forbids `path`.
- `path` requires 2–6 points with valid bearing/distance; forbids `patrol_radius_m`.
- Each path point (and patrol center = strike/AOI) SHOULD match unit domain
  (reuse `classify_channel_domain` / strike+recon map points). Soft-fail or hard
  reject on domain mismatch — prefer **hard** like existing strike domain rules.
- `static` / omit: ignore motion-only fields if present → reject extras for
  clarity (strict).

### 4. Agent / options

- `mid_channel_shipping` / sea_craft inspiration: prefer `patrol` for U-boat examples.
- `soft_vehicles`: prefer short `path` or `patrol`.
- `aaa_guns` / harbour notes: prefer omit/`static`.
- Voice: if any target has non-static motion, brief may say contacts are under way /
  on the move (surfaced U-boat language from `#15f` still applies).

### 5. Examples

- Update `manston_uboat_recon.yaml` + `manston_uboat_hunt.yaml` with
  `motion: patrol` + modest radius (stay mid-Channel sea).
- Add `examples/manston_ground_attack_convoy.yaml` (or extend existing GA) with
  Blitz `motion: path` of 2–3 inland points near Dunkirk belt — domain land.

## Risks / Trade-offs

- **[Risk] Patrol circle clips onto land/coast** → Mitigation: keep mid-Channel
  radii modest; validate sample points on circle if cheap, else document accept
  geometry; ME smoke on known sea Specs.
- **[Risk] PyDCS waypoint loop semantics differ ship vs vehicle** → Mitigation:
  spike one ship + one vehicle compile early; pin asserts on waypoint count /
  route flags in `.miz`.
- **[Risk] Bombing task still aims at fixed strike point while target moves** →
  Mitigation: acceptable for v1 (player aims visually; AI Bombing may lag). Note
  in design; do not retarget Bombing dynamically without Lua.
- **[Risk] Agent invents long paths** → Mitigation: max 6 points; prompts prefer
  short curated legs.

## Migration Plan

- Omit motion = identical compile to today (no BREAKING).
- Update U-boat examples in same change; refresh goldens/asserts.
- Rollback: remove motion fields; compiler ignores unknown only if we never
  shipped — we validate unknown keys via pydantic, so old Specs stay valid.

## Open Questions

- Exact patrol waypoint count (4 vs 8) — default **4** unless ME looks coarse.
- Whether GA `Bombing` waypoint should stay at strike point (yes for v1).
