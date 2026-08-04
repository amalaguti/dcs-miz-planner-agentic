## Why

Radio menus and late activation (#25) unlocked player options, but Channel Specs still
cannot play callout audio or express multi-step flag logic (kill counters, timed chains)
that stock Instant Action uses with native ME only. PyDCS already emits sound and numeric
flag predicates — the Spec vocabulary is the gap.

## What Changes

- Add trigger action `sound` with a curated `asset_id` (no arbitrary paths from the LLM).
- Ship a small checked-in sound asset registry + at least one embeddable sample for compile.
- Extend flags beyond bool: conditions `flag_equals` / `flag_more` / `flag_less` /
  `time_since_flag`; actions `inc_flag` / `set_flag_value` (keep existing `flag_is` /
  `set_flag`).
- Validate unknown `asset_id` and flag numeric ranges; emit via PyDCS (`SoundToAll`,
  `FlagEquals` / `FlagIsMore` / `FlagIsLess`, `TimeSinceFlag`, `IncreaseFlag`,
  `SetFlagValue`) and embed sound files in the `.miz` mapResource.
- Example Spec + tests; agent schema/prompt notes; ME acceptance (sound action + numeric
  flag rules visible).

## Non-goals

- `#22` Lua / Mist / MOOSE; `#24` cockpit args.
- `group_life_less`, altitude/speed gates, smoke/markers (follow-ups).
- Arbitrary Spec file paths; SoundToCoalition/Group in v1 (SoundToAll only).
- Auto-wiring narrative packs to play sounds (authors may combine hand triggers later).
- Changing radio / late-activation behaviour from `#25`.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-triggers`: Sound action + richer flag condition/action vocabulary and validation.
- `mission-spec`: Document that triggers may reference curated sound `asset_id`s.
- `miz-compiler`: Embed sound assets; map new conditions/actions to ME predicates.
- `mission-validation`: Reject unknown `asset_id`; validate numeric flag fields.
- `agent-tools`: Schema/prompt notes for sound + numeric flags.
- `golden-fixtures`: Example coverage for sound + flag structure.

## Impact

- `models.py`, `validation.py`, `triggers_emit.py`, `pydcs_compiler.py`; small sound
  registry + sample file under product assets; example YAML; agent prompts/schema; tests;
  BACKLOG.
- Acceptance: compiled example opens in ME with SOUND TO ALL and numeric flag rules.
