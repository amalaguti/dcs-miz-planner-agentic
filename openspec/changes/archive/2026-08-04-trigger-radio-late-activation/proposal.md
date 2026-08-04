## Why

Narrative packs give reactive story (messages / kill→win), but Channel Specs still lack
stock IA–style *player options*: F10 radio menus and late-activated opposition. R9 ranked
that gap as the highest-leverage native enrichment — PyDCS already emits the predicates.

## What Changes

- Extend trigger **actions**: `radio_item_add` / `radio_item_remove`, `activate_group` /
  `deactivate_group` (refs into `enemies[]` / `targets[]` by index).
- Add optional `late_activation: bool` on `enemies` (and `targets`) so groups can start
  dormant and appear when a radio/flag rule fires.
- Keep flags string-named (map to ints as today); v1 radio items set a flag “on”
  (ME value 1) so existing `flag_is` gates activation — no numeric flag model yet.
- Example Spec (CAP or intercept) demonstrating F10 Easy/Med/Hard → activate matching
  late enemy set; tests + ME acceptance.
- Agent schema/prompt notes for the new vocabulary.

## Non-goals

- `#22` Lua / Mist / MOOSE; sound/VO assets; numeric flag compare / `time_since_flag`.
- Cockpit triggers (`#24`); package late-activation (escort) in v1.
- Changing narrative packs (authors may combine narrative + hand triggers once vocab exists).
- Default-on radio menus for all missions.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-triggers`: New actions + late_activation field semantics / validation.
- `mission-spec`: `enemies` / `targets` may declare `late_activation`.
- `miz-compiler`: Emit radio / activate actions; set PyDCS `late_activation` on groups.
- `agent-tools`: Schema notes for radio + late activation.
- `golden-fixtures`: Example coverage for radio + activate structure.

## Impact

- `models.py`, `validation.py`, `triggers_emit.py`, `pydcs_compiler.py` (group placement);
  example YAML; agent prompts/schema; tests; BACKLOG.
- Acceptance: ME shows F10 radio items and late-activated groups on compiled example.
