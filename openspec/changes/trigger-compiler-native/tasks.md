## 1. Emit path

- [x] 1.1 Remove `_refuse_uncompiled_triggers`; call `_apply_zones_and_triggers` after groups exist
- [x] 1.2 Map zones → `add_triggerzone` from player airport heading/distance
- [x] 1.3 Map TriggerRule → TriggerOnce/Continious with condition/action helpers + flag id table
- [x] 1.4 Wire `unit_dead` to enemy group ids collected during enemy spawn

## 2. Tests and example

- [x] 2.1 Update `test_triggers.py`: compile sample succeeds; assert trig predicates; empty still compiles
- [x] 2.2 Update sample YAML comment (compileable); agent schema note that compile works
- [x] 2.3 Compile `out/manston_freeflight_trigger_sample.miz` for in-game accept

## 3. Docs

- [x] 3.1 BACKLOG `#21` done/building; README; LESSONS (refuse removed; mapping notes)
- [x] 3.2 Note in-game accept: message ~T+120 on sample Instant Action
  - Accepted 2026-08-02: `out/manston_freeflight_trigger_sample.miz` — on-screen
    message after ~2 minutes (“Manston Tower — you are clear to taxi when ready.”).
    ME: mission Triggers panel (not group Triggered Actions).
