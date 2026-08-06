## Why

v0.3 left the agent able to invent Specs, but without an explicit **mission-designer
working memory**: dynamics modes, strike target classes ↔ payload/domain, and curated
Channel places. Without those shelves the agent improvises recommendations instead of
co-authoring from declared options.

## What Changes

- Add packaged planning-option families for mission-designer co-authoring:
  - `dynamics_mode` — `fixed` / `live` / `choose` / `hybrid` (advisory until `#30f`)
  - `strike_target_class` — trucks / AAA / soft / hard / sea craft ↔ domain, unit ids, payload guidance
  - `channel_place` — curated Channel places for talk/recommend (airfields + coastal/mid-Channel cues)
- Sync those families into the agent catalog; surface via `list_mission_options` / CLI.
- Update invent/chat prompts so the agent **queries shelves then recommends** (co-design),
  not silent Spec fill.
- Tests that the new families appear after catalog sync with expected meta shape.

## Non-goals

- Spec `dynamics` expand pack / compiler emit (`#30f`)
- New ME predicates, Mist/MOOSE, or LLM Lua
- Full Channel landmark GIS or importing campaign `.miz` as Spec
- Guaranteeing live in-game acceptance for designer chat (catalog + hermetic tests)

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-options`: New designer shelf families in packaged Channel planning options
- `agent-catalog`: Sync/list includes the new families
- `agent-tools`: `list_mission_options` exposes designer shelves for tools/CLI
- `nl-agent`: Prompts require catalog shelf consult before recommending dynamics / strike / place

## Impact

- `data/channel/planning_options.yaml` (new families + meta)
- `catalog/` sync path (already loads planning options — verify/tests)
- Agent prompts (`prompts.py` / invent instructions)
- Tests under `tests/`; BACKLOG `#30e` stays `building` until apply accepted
- Follow-on `#30f` consumes `dynamics_mode` meta when emitting Spec
