## Context

Intercept, CAP, and ground-attack compile Channel sorties (scramble, Orbit/ROE, strike
loadouts). No friendly AI package, no Escort main task, no Spec link from player → escorted
group. PyDCS exposes `Escort` main task and `EscortTaskAction(group_id=…)` (default offset
behind/below; engage air planes within a max distance). CAP already maps `Engagement` →
`OptROE`. Sequencing: finish M4 escort before M5 `briefing-generation`.

## Goals / Non-Goals

**Goals:**

- Represent and compile one checked-in Channel escort: Spitfire cold at Manston, escort a
  friendly AI package along an airfield-relative route, apply escort engagement/ROE, optional
  light bounce near the route.
- Validation + golden + example; other mission types unchanged.
- Light agent/voice/schema awareness of `escort`.

**Non-Goals:**

- Briefings→`l10n`, triggers/Lua, multi-theatre, ground/ship escort, package bomb Specs.
- Agent-invented coords/ids; player multi-ship wingmen UI; new weather.

## Decisions

1. **`mission_type: escort`**
   - Same short enum style as other types.
   - Alternative rejected: overload CAP with a “protect group” flag — unclear package
     semantics and wrong main task.

2. **Nested `escort` block (required for escort; forbidden otherwise)**
   - Fields (v1):
     - `bearing_deg` (0–360) and `distance_km` (>0): **package destination** relative to
       the player departure airfield (same Point math as CAP/strike).
     - `altitude_m` (positive): package / escort cruise altitude.
     - `engagement`: reuse CAP `Engagement` enum → `OptROE` on the player Escort waypoint.
   - Alternative rejected: full multi-waypoint route list — overkill for v1; one destination
     plus fixed climb/IP waypoints in the compiler is enough for ME acceptance.

3. **Top-level `package` list (required non-empty) — friendly only**
   - Shape mirrors `enemies` / `EnemyFlight`: `aircraft`, `count` (1–16), `skill` (default
     Average), `country` (default `UK`), `coalition` (default `blue`).
   - Every package entry's `coalition` MUST equal `player.coalition` (no escorting the
     enemy). Opposing-coalition package entries MUST be rejected.
   - Aircraft MUST be known Channel registry ids. v1 example uses `MosquitoFBMkVI` (exact
     PyDCS id) as a classic Channel strike package; register it with Allied VHF radio
     (~124.0). Fallback note: a Spitfire package remains valid if Mosquito is undesirable
     for a given install — still same Spec shape.
   - Do **not** reuse `targets` / `strike` / `player.payload` on escort Specs.

4. **Optional `enemies` (bounce)**
   - Empty = clean escort; non-empty = place opposing aircraft near the package route
     (station-neighbourhood style offset from destination or mid-route — prefer mid-route /
     destination-neighbourhood, not the intercept Hawkinge corridor alone; document
     constants in LESSONS).
   - Enemy coalitions MUST oppose the player (same rule as intercept/CAP).

5. **Objective `escort_package`**
   - Required non-empty `objectives` including `escort_package`. Validate-only (no win/lose
     triggers). Reject on non-escort types unless a later change allows it.

6. **Compiler path**
   - Place **package first** (`flight_group_inflight` near the departure airfield at cruise
     altitude, same-coalition country), waypoints: climb/nav → destination Point; set a
     sensible main task (e.g. `CAS` or `GroundAttack` — pick during apply; package is the
     escorted flight, not the player Escort task).
   - Player cold start; `group.task = Escort.name`; add climb + escort waypoints toward the
     package route; attach `EscortTaskAction(group_id=package.id)` and `OptROE` from Spec
     engagement. Default PyDCS escort offset is fine for v1.
   - Optional enemies via existing inflight helpers with escort-route offset.
   - Keep radio + theatre-member workarounds. No payload scan changes.
   - Objectives remain validate-only.

7. **Example Spec**
   - `examples/manston_escort.yaml`: Manston morning, `sunny_clear`, destination SE toward
     the French coast / Channel approach (finalize bearing/distance during apply against
     airport math — keep package over a sensible Channel route, not random mid-map),
     `weapons_free`, 2× `MosquitoFBMkVI` package, optional 2× `Bf-109K-4` bounce.
   - Golden `tests/fixtures/manston_escort/`: Escort task, EscortTaskAction/`groupId`,
     Mosquito + optional Bf-109, player/theatre/freq.

8. **Planning options / catalog / agent**
   - Add `mission_type` / `escort` as `supported`.
   - `get_mission_spec_schema` / planning rules / commander brief gain an escort branch
     (stay with the package, engagement posture, bounce watch-outs).

## Risks / Trade-offs

- [Mosquito module missing on some installs] → Spec/registry still valid; ME may warn;
  document; Spitfire package remains a valid alternate Spec without schema change.
- [Player skill ignores AI Escort task] → Task + EscortTaskAction still correct in ME and
  for future wingmen; route waypoints guide the sortie.
- [Package starts too far / too close] → Inflight near airfield + destination from Spec;
  tune offsets during apply; verify in ME.
- [Scope creep into package bombs / triggers] → Explicit non-goals; empty
  `targets`/`triggers`; no `strike`/`payload` on escort.

## Migration Plan

1. Models + validators + registry Mosquito (if used) + unit tests.
2. Compiler escort path + example YAML.
3. Validation + planning_options + catalog/agent/voice light updates.
4. Golden + refresh; pytest/Ruff green.
5. In-game accept; BACKLOG → done; LESSONS for EscortTaskAction / package placement.

## Open Questions

- Exact example bearing/distance_km: finalize during apply from Channel airport geometry.
- Package main task string (`CAS` vs `Ground Attack`): decide during compiler apply after
  a quick ME check.
- Whether bounce spawns at mid-route or destination neighbourhood — prefer destination
  neighbourhood ± documented offset; record in LESSONS.
