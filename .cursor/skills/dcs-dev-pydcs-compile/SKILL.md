---
name: dcs-dev-pydcs-compile
description: >-
  PyDCS Mission compile pitfalls for this repo: terrain binding, payloads,
  theatre zip member, weather enums, briefing l10n, goldens, escort/GA/CAP
  layout. Use when changing the compiler, golden fixtures, or debugging .miz
  structure / KeyErrors.
---

# PyDCS compile

## Read first

[`docs/lessons/pydcs-compile.md`](../../../docs/lessons/pydcs-compile.md)

## Hard rules

1. **Only** `compiler/pydcs_compiler.py` (and emit helpers) import `dcs.*`.
2. Bind terrain via `theatre_terrain.terrain_for_theatre(spec.theatre)` — never
   hard-code `TheChannel()` while ignoring Spec. Intercept enemy spawn uses
   `intercept_spawn.intercept_spawn_for_theatre` (TheChannel Hawkinge/Dover,
   Normandy NeedsOarPoint/Cherbourg 180/63, Caucasus Batumi/Black Sea 270/40,
   Syria Incirlik/Iskenderun 180/40, Nevada Nellis/north-range 350/40
   offset `+39392.31012048834, −6945.927106677216` — not ±40000,0;
   Falklands Mount Pleasant/South Atlantic 150/40 dest
   `38677.30416162246` / `67168.748047` (pydcs git e20f328; not ±40000,0;
   do not recompute from `airport_list()`).
3. Keep **`_disable_payload_scan`** after the git pin unless a recorded compile
   with a real DCS install proves scan-on; use registry CLSID loadouts for GA.
4. Ensure **theatre** zip member (`_ensure_theatre_member`); PyDCS may omit it.
5. Weather: `clouds_iprecptns` is an **enum**, not a raw int.
6. Briefing: PyDCS `set_sortie_text` / `set_description_*`; lazy-import briefing
   to avoid compiler↔agent cycles.
7. Goldens: normalize `onboard_num`, `fuel`, and liveries in CI — see
   `normalize_mission`. Default fuel churns on pydcs DCS aircraft re-exports.
   Do **not** assert an aircraft type is absent via a whole-mission substring:
   PyDCS `requiredModules` lists ED module names (`Su-25T by Eagle Dynamics`)
   even when that type is not a unit. Assert player `["type"]="…"` instead
   (PyDCS dumps no spaces around `=`).
8. Escort: package first, then EscortTaskAction + ROE; GA: verify land vs water
   strike placement. Falklands escort reuses CAP/intercept 150°/40 km (dest
  38677.30416162246 / 67168.748047) — never copy Channel escort 120/55 or
  Nevada 350/40 onto Mount Pleasant. Falklands GA/recon dest is 269°/21 km
  (72951.81977781704 / 26171.946448715786) — never copy CAP 150/40 onto
  East Falkland trucks or recon AOI.
9. Target motion: `target_motion.py` + `target_motion.yaml` speed bands; `add_waypoint`
   speed is km/h; loop with `SwitchWaypoint` (1-based); domain-check path/patrol;
   omit `speed_kmh` for seeded cruise. Moving land: `OptDisparseUnderFire` (default 180s).
10. Target AI (#15h): `target_ai.py` — allowlist by class (soft/AAA/sea); land
    `move_formation` → `PointAction`; do not dump ME Options (Spit ECM lesson).


## Code touchpoints

`compiler/pydcs_compiler.py`, `intercept_spawn.py`, `target_motion.py`, `target_ai.py`,
`theatre_terrain.py`, `tests/fixtures_support.py`, `tests/refresh_*_golden.py`.
