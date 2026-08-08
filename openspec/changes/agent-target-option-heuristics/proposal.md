## Why

`#8c` lets invent query exact Channel strike unit ids; `#15h` ships curated
`ai_preset` / motion. Invent still depends on sparse prompt memory for
“truck column” → Blitz + path + `convoy_transit`. Pilots need reliable
place×class×ask → unit + motion + AI posture without free-form ME Opt*.

## What Changes

- Enrich `strike_target_class` / `ground_ai_preset` / `channel_place` planning
  meta with invent heuristics (`preferred_motion`, `preferred_ai_preset`,
  example paths, cue keywords where cheap).
- Invent prompts + Spec schema: call `list_strike_targets` +
  `list_mission_options` before emitting GA/recon `targets[]`; emit only
  allowlisted units/presets/fields from those tools.
- Optional decision table in prompts or a thin helper note (not a new compile
  engine). Hermetic tests: 3–4 cue → expected Spec shape (unit class / motion /
  preset presence).
- BACKLOG: durable **promote checklist** for future theatres + target shelves
  (docs only this change — not multi-map code).

## Capabilities

### New Capabilities

- *(none)*

### Modified Capabilities

- `mission-options`: planning_options meta carries invent heuristics for
  classes / presets / places.
- `nl-agent`: invent guidance for place×class×ask → unit + motion + ai_preset.
- `agent-tools`: tool descriptions / schema notes reinforce the call order
  (list_strike_targets + list_mission_options before targets[]).
- `golden-fixtures`: hermetic invent/heuristic coverage as needed.

## Impact

- `data/channel/planning_options.yaml`, `agent/prompts.py`, `agent/spec_schema.py`,
  optional `tool_bridge` descriptions, tests, `docs/BACKLOG.md`.
- No compiler/validate SoT change; no new DCS unit ids required for v1.

## Non-goals

- Dumping ME Options; inventing DCS ids; RL from flight logs.
- Expanding registry shelves (armor/troops/more ships) — separate promotes.
- Multi-theatre registries or auto-scraping installs for units/maps.
- Implementing the full future-map promote pipeline in code (checklist in
  BACKLOG only).

## Acceptance

Stub/hermetic: invent guidance + options meta make “truck inland / flak /
U-boat under way / harbour” map to soft+path+`convoy_transit`,
aaa+static+`aaa_alert`, sea+patrol+`ship_under_way`, sea+static+`harbour_static`
(ids from `list_strike_targets`). No ME fly required for `#8d` accept; `#15h`
ME smoke stays do-soon.
