## Why

Channel invent has no **armor** class — tank/StuG columns fall back to soft or
halftrack shelves. `#8i` halftracks shipped; next class spine step is curated
AFVs per `#8e`.

## What Changes

- Promote verified PyDCS ids `Pz_IV_H`, `Stug_III`, `Cromwell_IV`, `M4_Sherman`
  into `ground_units.yaml`.
- Add `strike_target_class` `armor` (unit_ids, cues, preferred path +
  `convoy_transit`); wire `target_motion.yaml` armor profiles; french_coast
  `related_classes` + invent prompt cue.
- Example GA Spec + hermetic tests; BACKLOG / checklist spine.

## Capabilities

### New Capabilities

- *(none)*

### Modified Capabilities

- `reference-registry`: new Channel armor land unit ids.
- `mission-options`: new `armor` class shelf + place related_classes.
- `agent-catalog`: sync surfaces new strike units + class tags.
- `golden-fixtures`: example/tests for armor shelf.

## Impact

- Registry YAML, planning_options, target_motion, agent prompts, examples/,
  tests, BACKLOG / THEATRE_TARGET_PROMOTE.

## Non-goals

- Troops / radar / trains (`#8k`–`#8m`); Tiger/Panther/Jagd expand (later).
- New ground AI preset or Opt* keys (reuse `convoy_transit` / soft AI class;
  R12b later if ME options differ).
- ME scrape; invent free-form ids.

## Acceptance

New ids validate + compile in example; `list_strike_targets(class_id=armor)`
returns them after sync; hermetic pytest green. ME Instant Action optional do-soon.
