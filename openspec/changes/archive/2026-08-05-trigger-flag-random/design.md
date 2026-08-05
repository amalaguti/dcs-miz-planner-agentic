## Context

PyDCS already exposes `SetFlagRandom(flag, min_value, max_value)` → `a_set_flag_random`.
Named Spec flags map through the existing `flag_id` helper (same as `set_flag_value`).

## Decisions

1. **Action shape:** `{ type: set_flag_random, flag: str, min: int, max: int }`
   using Spec field names `min`/`max` (map to PyDCS `min_value`/`max_value` at emit).
2. **Validation:** `min <= max`; both integers; reuse flag name rules with other flag actions.
3. **Example:** Small free_flight (or extend sound/flags sample) that rolls a flag after
   `time_more` and messages on `flag_equals` — enough for ME/golden coverage without a
   full intercept radio mission.
4. **No Mist:** This change is explicitly the native alternative to Mist RNG.

## Risks

- ME inclusive range semantics — match PyDCS/ME defaults; document in LESSONS if
  off-by-one appears in-game.
