## Why

Channel Specs can place units and fire messages/flags, but cannot enforce ingress
discipline (stay low / stay slow) with native ME altitude and speed gates. PyDCS already
exposes unit altitude (MSL/AGL) and speed predicates — Spec vocabulary is the gap.

## What Changes

- Add player-unit trigger conditions for altitude higher/lower (MSL or AGL) and speed
  higher/lower, compiling to PyDCS `UnitAltitude*` / `UnitSpeed*`.
- Validate positive thresholds; Spec altitude in meters, speed in km/h (compiler converts
  speed to m/s for ME).
- Example Spec (prefer free-flight or ground-attack) showing a continuous altitude or
  speed gate → message; agent schema/prompt notes; ME acceptance of the predicates.

## Non-goals

- `#22` Lua / Mist / MOOSE; `#24` cockpit args; vertical-speed gates.
- Enemy/AI unit altitude or speed conditions (player only in this change).
- Narrative pack rewiring (vocab allows gates; packs do not auto-emit them here).
- Auto-fail mission on gate bust (authors may compose `mission_end` themselves).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-triggers`: Add altitude/speed condition vocabulary and player-unit rules.
- `mission-spec`: Document that triggers may use player altitude/speed gate conditions.
- `miz-compiler`: Map gates to PyDCS UnitAltitude* / UnitSpeed*; pass player unit id.
- `mission-validation`: Reject non-positive thresholds; shared validate path.
- `agent-tools`: Schema/prompt notes for altitude/speed gate conditions.
- `golden-fixtures`: Example coverage for altitude/speed gate emit structure.

## Impact

- `models.py`, `validation.py`, `compiler/triggers_emit.py`, `pydcs_compiler.py` (player
  unit id into emit); example YAML; agent prompts/schema; tests; BACKLOG.
- Acceptance: compiled example opens in ME with Unit Altitude and/or Unit Speed condition
  predicates on the player unit.
