## Why

Channel invent cannot plan train strikes: no `trains` class and `#15g` forbids
free-form rail geometry. Armor/troops shelves shipped; promote curated loco/wagon
ids plus a named **rail corridor** place so invent copies path recipes only.

## What Changes

- Promote verified PyDCS ids `Locomotive`, `German_covered_wagon_G10`,
  `German_tank_wagon`, `DR_50Ton_Flat_Wagon` into `ground_units.yaml`.
- Add `strike_target_class` `trains` + `train` motion profile; new
  `channel_place` `french_coast_rail_corridor` with strike geometry +
  `path_point_deltas` (not rail-mesh snap).
- Invent prompt cue: trains only via that corridor recipe.
- Example GA Spec + hermetic tests; BACKLOG / checklist spine.

## Capabilities

### New Capabilities

- *(none)*

### Modified Capabilities

- `reference-registry`: new Channel train land unit ids.
- `mission-options`: `trains` class + rail corridor place.
- `agent-catalog`: sync surfaces new strike units + class/place.
- `golden-fixtures`: example/tests for trains shelf.

## Impact

- Registry YAML, planning_options, target_motion, agent prompts, examples/,
  tests, BACKLOG / THEATRE_TARGET_PROMOTE.

## Non-goals

- Auto-snap to DCS rail mesh; LLM free rail routes.
- Modern coaches / electric loco; radar `#8l`.
- New AI Opt* presets (reuse `convoy_transit`).
- R13 campaign scan.

## Acceptance

New ids validate + compile in example using corridor path; catalog lists
`trains` + place; hermetic pytest green. ME Instant Action optional do-soon
(confirm train motion looks acceptable even without mesh snap).
