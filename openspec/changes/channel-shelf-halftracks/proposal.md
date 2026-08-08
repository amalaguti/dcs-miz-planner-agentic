## Why

Channel invent still has no **halftracks_apc** class — pilots asking for
SPW/halftrack columns fall back to soft trucks. `#8h` deferred this shelf; `#8e`
checklist and motion `halftrack` band are ready.

## What Changes

- Promote verified PyDCS ids `Sd_Kfz_251`, `Sd_Kfz_7`, `M2A1_halftrack` into
  `ground_units.yaml`.
- Add `strike_target_class` `halftracks_apc` (unit_ids, cues, preferred path +
  `convoy_transit`); wire `target_motion.yaml` halftrack profiles; french_coast
  `related_classes` + invent prompt cue.
- Example GA Spec + hermetic tests; BACKLOG / checklist spine.

## Capabilities

### New Capabilities

- *(none)*

### Modified Capabilities

- `reference-registry`: new Channel halftrack land unit ids.
- `mission-options`: new `halftracks_apc` class shelf + place related_classes.
- `agent-catalog`: sync surfaces new strike units + class tags.
- `golden-fixtures`: example/tests for halftrack shelf.

## Impact

- Registry YAML, planning_options, target_motion, agent prompts (cue table),
  examples/, tests, BACKLOG / THEATRE_TARGET_PROMOTE.

## Non-goals

- Armor / troops / radar / trains (`#8j`–`#8m`).
- New ground AI preset or Opt* keys (reuse `convoy_transit` / soft AI class).
- ME scrape; invent free-form ids.

## Acceptance

New ids validate + compile in example; `list_strike_targets(class_id=halftracks_apc)`
returns them after sync; hermetic pytest green. ME Instant Action optional do-soon.
