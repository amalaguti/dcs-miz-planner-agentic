## 1. Spec model

- [x] 1.1 Add `MarkAction` (`zone`, `text`, optional `readonly`) and `SmokeAction` (`zone`, curated `color`, optional `altitude_m`) and extend `TriggerAction` union

## 2. Validate and emit

- [x] 2.1 Validate `mark`/`smoke` zone refs and smoke color in `validation.py`
- [x] 2.2 Map `mark` → PyDCS `MarkToAll` (zone id + compiler mark ids) and `smoke` → `ExplodeWPMarker` in `triggers_emit.py`

## 3. Example, agent, docs

- [x] 3.1 Add example Spec (prefer ground-attack) with zone + `mark`/`smoke` → message
- [x] 3.2 Agent schema/prompt notes; BACKLOG status `building`

## 4. Tests and acceptance

- [x] 4.1 Unit/integration: validate failures + compile structure (`a_mark_to_all` / `a_explosion_marker`); regression on prior triggers
- [x] 4.2 In-game: ME shows Mark To All and/or Smoke Marker on the compiled example
  - Accepted 2026-08-04: ME shows `mark_targets` with Smoke Marker (red) + Mark To All (value/mark id 1) on `strike_mark`.
