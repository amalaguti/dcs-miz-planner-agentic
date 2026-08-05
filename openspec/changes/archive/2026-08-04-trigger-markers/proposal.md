## Why

Strike and FAC-style Channel Specs can place targets and fire messages, but cannot drop
an F10 map mark or colored zone smoke. Stock IA uses those visual aids constantly; PyDCS
already exposes `MarkToAll` and smoke-marker actions — Spec vocabulary is the gap.

## What Changes

- Add trigger action `mark` that references a Spec zone by name, carries mark text, and
  compiles to ME Mark To All (`a_mark_to_all`) with a compiler-assigned unique mark id.
- Add trigger action `smoke` that references a Spec zone by name plus a curated smoke
  color, compiling to ME Smoke Marker (`a_explosion_marker`).
- Validate zone references and color enums; example Spec (prefer ground-attack) showing
  mark/smoke → message; agent schema/prompt notes; ME acceptance of the actions.

## Non-goals

- Altitude/speed gates; `#22` Lua / Mist / MOOSE; `#24` cockpit args.
- Signal flares, `MarkToCoalition` / `MarkToGroup`, remove-mark, big fire/smoke
  (`a_effect_smoke`), unit-attached markers.
- Narrative pack rewiring (vocab allows mark/smoke; packs do not auto-emit them here).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-triggers`: Add `mark` and `smoke` action vocabulary and zone-reference rules.
- `mission-spec`: Document that triggers may use map-mark and zone-smoke actions.
- `miz-compiler`: Map `mark`/`smoke` to PyDCS MarkToAll / ExplodeWPMarker.
- `mission-validation`: Reject unknown zones / invalid smoke colors; shared validate path.
- `agent-tools`: Schema/prompt notes for `mark` and `smoke`.
- `golden-fixtures`: Example coverage for mark/smoke emit structure.

## Impact

- `models.py`, `validation.py`, `compiler/triggers_emit.py`; example YAML; agent
  prompts/schema; tests; BACKLOG.
- Acceptance: compiled example opens in ME with Mark To All and/or Smoke Marker actions
  tied to the referenced trigger zone.
