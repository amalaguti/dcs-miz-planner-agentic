## Why

Trigger-rich examples (radio+late-act, altitude/speed gates, mark/smoke, sound+numeric
flags) are covered only by substring smoke in `test_triggers.py`. That catches missing
predicate names but not silent reshaping of trig rules, zones, or group late-activation.
Adversarial backlog `#35` asks for the same structural golden harness already used for
combat/free-flight Specs.

## What Changes

- Add checked-in structural goldens (normalized `mission` + theatre + dictionary +
  `meta.json` contracts) for the four trigger-rich Manston example Specs.
- Add hermetic pytest that compiles each Spec with injected Channel inventory and
  `assert_matches_golden`.
- Add explicit refresh helpers; ordinary pytest MUST NOT rewrite fixtures.
- Raise `golden-fixtures` requirements from string-marker-only to full structural
  goldens for those four paths (keep existing string-smoke tests or thin them to
  avoid duplicate weak asserts).

## Non-goals

- No new Spec trigger vocabulary or compiler emit behaviour (unless a refresh reveals a
  bug).
- No Lua AST / trig-table parser — still zip-member + normalized mission text.
- No narrative-pack goldens, `group_life_less`, or empty-trigger combat golden rewrites.
- No CI workflow (that is `#36` `ci-minimal`).
- No in-game DCS acceptance beyond compile/golden regression (ME open optional).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `golden-fixtures`: Require structural goldens (not string-smoke only) for radio+late-act,
  altitude/speed gates, mark/smoke, and sound+numeric flag example Specs.

## Impact

- New dirs under `tests/fixtures/`; helpers in `fixtures_support.py`; refresh scripts;
  golden tests; delta + main `golden-fixtures` spec sync on archive.
- Fixture size grows (full mission text for four Specs).
