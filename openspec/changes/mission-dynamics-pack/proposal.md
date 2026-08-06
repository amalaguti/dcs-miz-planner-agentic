## Why

`#30e` put dynamics modes on the catalog shelf; pilots still cannot *declare* play-time
variation cleanly. Hand-wiring `set_flag_random` + late pools + F10 works but is noisy
for the agent and easy to get wrong (double-spawn). A narrative-style expand pack makes
`live` / `choose` / `hybrid` / `fixed` first-class Spec so co-authoring locks a real
decision the compiler expands deterministically.

## What Changes

- Mission Spec optional `dynamics` block: `mode`, `pools` (enemy/target indices into
  existing late groups), optional `roll` / `menu`, `exclusive` default true
- Expand before validate/compile (like `narrative.enabled`): emit native
  `set_flag_random` / radio / `activate_group` / messages; clear expand flag after
- Conflict: non-empty hand `triggers` + `dynamics` → hard error (v1)
- Example Spec(s) + goldens/smoke; mark `dynamics_mode` planning options `supported`
  (or keep advisory with meta pointing at Spec field) once emit exists
- Light prompt notes: prefer emitting `dynamics` over long hand graphs when the pattern
  matches; still co-author / ask before assuming hybrid

## Non-goals

- Mist/MOOSE / magic spawn-from-void
- Mid-sortie second roll / route jitter (Layer A `randomize` stays separate)
- Full GA target-pool polish beyond enemy indices if timeboxed — may ship enemies-first
  with `target_indices` stubbed or thin
- Hard invent default to hybrid without user lock (soft recommend only)

## Capabilities

### New Capabilities

- (none — extend existing)

### Modified Capabilities

- `mission-spec`: optional `dynamics` model
- `mission-validation`: expand + conflict / late-activation / index checks
- `miz-compiler`: expand before emit (or share expander with validation)
- `mission-triggers`: expanded graph uses existing actions only
- `mission-options`: dynamics_mode support honesty after emit
- `nl-agent` / `agent-tools`: schema notes + invent guidance for dynamics Spec

## Impact

- `models.py`, new `dynamics.py` (or beside `narrative.py`), validation, compiler
- Examples under `examples/`; tests; planning_options meta; BACKLOG `#30f`
- Builds on `#22a` / `#25` primitives and `#30e` shelves
