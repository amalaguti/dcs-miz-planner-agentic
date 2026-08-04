## Why

Strike and raid Specs can only detect full group destruction (`unit_dead` /
`target_dead`). Stock Channel IA often treats a target as “done enough” when remaining
group life drops below a threshold. PyDCS already exposes `GroupLifeLess` — Spec
vocabulary is the gap.

## What Changes

- Add trigger condition `group_life_less` that references exactly one of `enemy_index` or
  `target_index` (0-based) plus an integer `percent` life threshold.
- Validate index ranges and percent bounds; emit via PyDCS `GroupLifeLess`
  (`c_group_life_less`).
- Example Spec (prefer ground-attack / soft target) showing damaged-enough → message or
  mission beat; agent schema/prompt notes; ME acceptance of the life-less rule.

## Non-goals

- `#22` Lua / Mist / MOOSE; `#24` cockpit args.
- Altitude/speed gates, smoke/markers, `unit_life_less`, narrative pack rewiring.
- Changing `unit_dead` / `target_dead` semantics (still full GroupDead).
- Player-group life conditions (enemy/target indices only in this change).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-triggers`: Add `group_life_less` condition vocabulary and reference rules.
- `mission-spec`: Document that triggers may use damage-threshold group life conditions.
- `miz-compiler`: Map `group_life_less` to ME `GroupLifeLess` for the placed group.
- `mission-validation`: Reject bad indices / percent; keep shared validate path.
- `agent-tools`: Schema/prompt notes for `group_life_less`.
- `golden-fixtures`: Example coverage for life-less emit structure.

## Impact

- `models.py`, `validation.py`, `compiler/triggers_emit.py`; example YAML; agent
  prompts/schema; tests; BACKLOG.
- Acceptance: compiled example opens in ME with a GROUP LIFE LESS (or equivalent) rule
  tied to the referenced enemy/target group.
