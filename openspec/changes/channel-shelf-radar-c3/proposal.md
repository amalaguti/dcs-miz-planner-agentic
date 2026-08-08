## Why

Channel invent has no **radar_c3** class — Freya/Würzburg-style hunts have no
shelf. Other class spines (`#8i`–`#8k`/`#8m`) shipped; promote emplaced WWII
radar ids per `#8e` (static only).

## What Changes

- Promote verified PyDCS ids `FuMG-401`, `FuSe-65` into `ground_units.yaml`.
- Add `strike_target_class` `radar_c3` (static + convoy_transit); french_coast
  `related_classes` + invent cue.
- Example GA Spec + hermetic tests; BACKLOG / checklist spine.

## Capabilities

### New Capabilities

- *(none)*

### Modified Capabilities

- `reference-registry`: new Channel radar land unit ids.
- `mission-options`: new `radar_c3` class shelf + place related_classes.
- `agent-catalog`: sync surfaces new strike units + class tags.
- `golden-fixtures`: example/tests for radar shelf.

## Impact

- Registry YAML, planning_options, agent prompts, examples/, tests, BACKLOG /
  THEATRE_TARGET_PROMOTE.

## Non-goals

- Modern EWR/SAM radars (`1L13 EWR`, Dog Ear, etc.).
- New AI Opt* / `#17b` scenery statics; AAA allowlist membership for radars.
- ME scrape; invent free-form ids.

## Acceptance

New ids validate + compile as static targets; `list_strike_targets(class_id=radar_c3)`
returns them after sync; hermetic pytest green. ME Instant Action optional do-soon.
