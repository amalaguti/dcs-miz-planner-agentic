## Why

Channel invent has no **troops** class — infantry columns/patrols have nowhere
to land. Armor `#8j` shipped; next class spine step is curated WWII infantry
per `#8e`. Motion `troops` band already exists.

## What Changes

- Promote verified PyDCS ids `soldier_mauser98`, `soldier_wwii_br_01`,
  `soldier_wwii_us` into `ground_units.yaml`.
- Add `strike_target_class` `troops` (unit_ids, cues, preferred path +
  `convoy_transit`); wire `target_motion.yaml` troops profiles; french_coast
  `related_classes` + invent prompt cue.
- Example GA Spec + hermetic tests; BACKLOG / checklist spine.

## Capabilities

### New Capabilities

- *(none)*

### Modified Capabilities

- `reference-registry`: new Channel infantry land unit ids.
- `mission-options`: new `troops` class shelf + place related_classes.
- `agent-catalog`: sync surfaces new strike units + class tags.
- `golden-fixtures`: example/tests for troops shelf.

## Impact

- Registry YAML, planning_options, target_motion, agent prompts, examples/,
  tests, BACKLOG / THEATRE_TARGET_PROMOTE.

## Non-goals

- Radar / trains (`#8l`–`#8m`); modern infantry (`Soldier RPG`, AK, etc.).
- New ground AI preset (reuse `convoy_transit` / soft AI class).
- ME scrape; invent free-form ids; R13 campaign scan (separate research).

## Acceptance

New ids validate + compile in example; `list_strike_targets(class_id=troops)`
returns them after sync; hermetic pytest green. ME Instant Action optional do-soon.
