## Why

`trigger-model-spec` lets Specs declare typed zones/triggers, but the compiler still
refuses to emit them. Without native ME trigger tables in the `.miz`, declared behaviour
never appears in DCS. M6 needs the compile half so validate-only samples become flyable
(messages, flags, win/fail, zone entry).

## What Changes

- Remove the compile refusal for non-empty `zones`/`triggers`.
- Emit Spec zones as PyDCS circular trigger zones (airfield-relative → map points).
- Emit each `TriggerRule` as `TriggerOnce` / continuous with mapped conditions and actions:
  `time_more`→`TimeAfter`, `flag_is`→`FlagIsTrue`/`False`, `unit_dead`→`GroupDead`,
  `coalition_in_zone`→`PartOfCoalitionInZone`; `message`→`MessageToAll`,
  `set_flag`→`SetFlag`/`ClearFlag`, `mission_end`→`EndMission` (player coalition win/lose).
- Map Spec string flag ids to integer ME flags deterministically.
- Compile the checked-in trigger sample to `.miz`; assert trig predicates in tests;
  in-game accept message at T+120 on the sample.
- Update LESSONS / BACKLOG / README; goldens for empty-trigger examples unchanged.

## Non-goals

- New Spec condition/action types beyond the `#20` vocabulary.
- Mist/MOOSE, `DoScript`, radio menus, cockpit args.
- Full ME trigger surface or OR predicate trees.
- Refreshing all combat goldens unless trig members appear unexpectedly.

## Capabilities

### New Capabilities
- (none — extends compiler behaviour for existing mission-triggers)

### Modified Capabilities
- `miz-compiler`: Emit native zones/triggers; stop refusing non-empty graphs.
- `mission-triggers`: Clarify that validated graphs MUST compile to native ME tables.
- `golden-fixtures`: Cover or contract-assert at least one Spec with a simple trigger
  (sample free-flight message).

## Impact

- `compiler/pydcs_compiler.py` (+ small helper module if needed)
- Example sample becomes compileable; tests; docs
