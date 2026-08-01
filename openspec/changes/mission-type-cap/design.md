## Context

Intercept v1 is placement-only (player cold + fixed Hawkinge/Dover enemy spawn). No
waypoints, Orbit/CAP tasks, or Spec-backed ROE. Planning options already list `roe_seed` as
`future`. PyDCS exposes `CAP` main task, `OrbitAction` (Circle / Race-Track), and `OptROE`.
Sequencing choice: finish M4 mission types before `briefing-generation`.

## Goals / Non-Goals

**Goals:**

- Represent and compile one checked-in Channel CAP: Spitfire cold at Manston, patrol station
  from Spec (airfield-relative), engagement/ROE applied, optional light opposition.
- Validation + golden + example; free_flight / intercept behaviour unchanged.
- Promote ROE from planning-option `future` to Spec-backed for CAP.
- Light agent/voice awareness of `cap`.

**Non-Goals:**

- Ground-attack, escort, `.miz` l10n briefings, triggers/Lua, wingman packages, multi-theatre.
- Agent-invented WGS84 coords; new weather presets.

## Decisions

1. **`mission_type: cap`**
   - Same short enum style as `free_flight` / `intercept`.
   - Alternative rejected: overload intercept with empty enemies — unclear patrol semantics.

2. **Nested `cap` block on Mission Spec**
   - Required when `mission_type` is `cap`; forbidden otherwise.
   - Fields (v1):
     - `bearing_deg` (0–360) and `distance_km` (>0): station relative to **player airfield**
       position (Channel terrain units via PyDCS airport → offset). No raw map x/y in Spec.
     - `altitude_m` (positive): orbit altitude.
     - `pattern`: `circle` | `race_track` (maps to `OrbitAction.OrbitPattern`).
     - `duration_min` (optional, ≥1): when set, wrap Orbit in `ControlledTask` with stop-after
       duration; when absent, open-ended Orbit.
     - `engagement`: enum mapped to PyDCS `OptROE` —
       `weapons_free` → WeaponFree, `open_fire` → OpenFire, `return_fire` → ReturnFire,
       `weapons_hold` → WeaponHold.
   - Alternative rejected: named registry stations only — less flexible for agent; can add
     named presets later as sugar over the same fields.

3. **Optional enemies for CAP**
   - Empty `enemies` = pure patrol; non-empty = place via existing `_place_enemies` (or a
     station-relative offset toward the CAP point — prefer station-neighbourhood spawn for CAP
     rather than the intercept Dover corridor alone; document constants in LESSONS).
   - `objectives` MUST be non-empty with `type: patrol` for CAP.
   - Free flight still requires empty extensions; intercept still requires enemies +
     `intercept_enemy`.

4. **Compiler CAP path**
   - After player `flight_group_from_airport`: set `group.task = CAP.name`.
   - Add climb/nav waypoint(s) then CAP station waypoint; `wp.add_task(OrbitAction(...))`;
     `wp.add_task(OptROE(...))` from Spec engagement.
   - Race-track: second waypoint offset along a fixed heading (~10 km) to define the track.
   - Reuse radio + payload-scan workarounds.
   - Objectives remain validate-only (no win/lose triggers).

5. **Example Spec**
   - `examples/manston_cap.yaml`: Manston, morning (~09:00), `sunny_clear`, station SE of
     Manston into the Channel (bearing/distance chosen from terrain during apply; document
     source), `circle`, `weapons_free`, optional 1–2× `Bf-109K-4` near station.
   - Golden dir `tests/fixtures/manston_cap/` with contracts: CAP task, Orbit present, ROE
     option value, player/theatre/freq.

6. **Planning options / catalog**
   - Add `mission_type` / `cap` as `supported`.
   - Promote `roe_seed` ids to `supported` with `meta.engagement` mapping into Spec
     `cap.engagement` (advisory→supported for CAP; agent must not emit ROE as a free_flight
     field).

7. **Agent / voice (minimal)**
   - `BASE_PLANNING_RULES` allow `cap` + `cap` block shape; refuse inventing coords (use
     bearing/distance).
   - `build_commander_brief` gains a CAP tactics/procedures/watch-outs branch.

## Risks / Trade-offs

- [Player skill ignores AI Orbit] → Waypoints + Orbit still show in ME and guide the sortie;
  ROE matters more once wingmen exist; still correct Spec→`.miz` contract.
- [Bad station offset off-map] → Resolve bearing/distance during apply against Channel terrain;
  verify in ME; keep example conservative (near Manston / Dover approach).
- [Race-track second point awkward] → Default example uses `circle`; race_track tested in unit
  compile asserts.
- [Scope creep into triggers] → Explicit non-goal; empty `triggers` still required.
- [ROE on free_flight/intercept] → Field lives only under `cap` for v1; other types unchanged.

## Migration Plan

1. Models + validators + unit tests (type matrix).
2. Compiler CAP path + example YAML.
3. Validation engine + planning_options + catalog sync tests.
4. Golden + refresh helper; agent/voice light updates.
5. In-game accept; BACKLOG `building` → `done`; LESSONS for station math / ROE mapping.

## Open Questions

- Exact example bearing/distance_km: finalize during apply from Channel airport geometry
  (document; do not invent WGS84).
- Whether CAP enemy spawn shares intercept Hawkinge corridor or uses station-relative offset —
  prefer station-relative; record in LESSONS.
