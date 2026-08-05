## 1. Spec model

- [x] 1.1 Add `UnitAltitudeHigherCondition` / `UnitAltitudeLowerCondition` (`altitude_m`, optional `agl` default true) and `UnitSpeedHigherCondition` / `UnitSpeedLowerCondition` (`speed_kmh`); extend `TriggerCondition` union

## 2. Validate and emit

- [x] 2.1 Validate positive `altitude_m` / `speed_kmh` in `validation.py` (Pydantic bounds may already reject ≤ 0)
- [x] 2.2 Pass player unit id from `pydcs_compiler` into `apply_zones_and_triggers`; map altitude/speed conditions to PyDCS `UnitAltitude*` / `UnitSpeed*` (km/h → m/s) in `triggers_emit.py`

## 3. Example, agent, docs

- [x] 3.1 Add free-flight example Spec with continuous altitude and/or speed gate → message (after short `time_more` to avoid parking spam)
- [x] 3.2 Agent schema/prompt notes; BACKLOG status `building`

## 4. Tests and acceptance

- [x] 4.1 Unit/integration: validate failures + compile structure (`c_unit_altitude_*` / `c_unit_speed_*`); regression on prior triggers
- [x] 4.2 In-game: ME shows Unit Altitude and/or Unit Speed condition on the player unit for the compiled example
  - Accepted 2026-08-04: continuous altitude (AGL) + speed gates after T+30s look correct in ME; useful for mission challenges.
