## Context

Combat/free-flight Specs already use `assert_matches_golden` with checked-in normalized
`mission` text. Trigger-rich examples only use `needle in mission` in `test_triggers.py`.
`golden-fixtures` already requires “coverage” for those examples but allows marker-only
asserts.

## Goals / Non-Goals

**Goals:**
- Pin full structural compile output for four checked-in Specs via the existing golden
  harness (same normalize / meta / inventory injection).
- Document refresh paths so intentional emit changes stay explicit.

**Non-Goals:**
- New emit vocabulary; Lua parsers; CI; narrative goldens.

## Decisions

1. **Reuse `fixtures_support.assert_matches_golden`** — same contract as combat goldens
   (required members, theatre, normalized mission, dictionary, `mission_must_contain`).
   Alternatives: only strengthen needles — rejected (still not structural).

2. **Four fixture dirs**, one per example:
   - `manston_dawn_intercept_radio`
   - `manston_freeflight_altitude_speed_gates`
   - `manston_ground_attack_markers`
   - `manston_freeflight_sound_flags`

3. **Contracts include trigger ME markers** (radio/activate/lateActivation, altitude/speed,
   mark/smoke, sound/flags) plus theatre/player basics — so meta catches regressions even
   if someone bypasses full mission equality.

4. **Keep lightweight string-smoke tests** for invalid Spec / schema notes; compile smoke
   for these four Specs MAY remain as thin “compiles” or rely solely on goldens — prefer
   golden as primary structural regression to avoid double maintenance of needles.

5. **Refresh**: one script per fixture or a small multi-target refresh script following
   `tests/refresh_*_golden.py` pattern; never auto-write in pytest.

## Risks / Trade-offs

- [Large fixtures] → Accept; same as combat goldens; refresh when emit changes.
- [Sound asset embedding volatility] → Normalize only known volatile fields (`onboard_num`);
  if sound binary paths churn, pin asset ids in contracts and refresh intentionally.
- [Golden drift vs PyDCS bump] → Same ritual as existing goldens (R8 / refresh).

## Migration Plan

Add fixtures + tests → pytest green → sync `golden-fixtures` on archive → merge.
No runtime migration.
