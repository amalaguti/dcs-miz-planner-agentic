## Why

`dcs-miz validate` can return green for Specs that compile into empty skies, silent no-ops, or compile-time `ValueError`s. Adversarial findings B1/B3/B4/B5/B9 and live “dormant bandits” eval show the shared engine checks indexes but not late-act↔activate graphs, `message.delay_s`, country/skill, or intercept/CAP enemy coalition. Fail-left in validation restores “validate ≈ compile-ready” for these known holes.

## What Changes

- **BREAKING (validate):** every `late_activation: true` enemy/target MUST be targeted by at least one `activate_group`; every `activate_group`/`deactivate_group` MUST target a late-activated group.
- **BREAKING (validate/load):** reject `message.delay_s > 0` until real delayed emit exists (prefer Spec field stay at 0 / omit).
- Move country + skill allowlist checks into shared validation (Channel: curated countries e.g. `UK`/`ThirdReich`; skill = known PyDCS skill names). Align with compiler `_ensure_country` / `_skill_from_name` fail-left.
- Require intercept and CAP enemies to use opposing coalition vs player (same bar as escort enemies).
- When a late-activated group is referenced by `unit_dead` / `target_dead` / `group_life_less` that can gate success, require an activate path (error).
- Tests: negative cases for each rule; keep `manston_dawn_intercept_radio.yaml` as the positive gold path.
- Docs/LESSONS: note Germany≠ThirdReich and dormant-bandit graph rule.

## Non-goals

- Implementing real `message.delay_s` ME delay (reject only).
- Strike land/water domain (`#34`), theatre→terrain binding (`#39`), aircraft module warn (`#38`).
- Agent prompt / `infer_creative` half-recipe fixes (`#30c`) beyond what validation errors give the agent.
- Warning channel / soft-fail severity (errors only so CLI exit codes stay binary).
- Dual-SoT full merge of pydantic vs validation (B11) — add rules in validation; light pydantic only if needed for load consistency.
- In-game ME acceptance for new negative fixtures (pytest + existing radio example validate/compile suffice).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-validation`: late-act↔activate graph; country/skill; intercept/CAP opposing enemies; dead-on-late-act activate path; `delay_s` rejection.
- `mission-triggers`: document that `activate_group`/`deactivate_group` require late_activation on the referenced group; `message.delay_s` MUST be 0 / omitted until implemented.

## Impact

- `validation.py` (+ possibly shared constants with compiler for country/skill).
- Optional `models.py` constraint on `MessageAction.delay_s` or validate-only reject.
- `openspec` deltas; `tests/test_validation.py` / `test_triggers.py`; BACKLOG `#32`; LESSONS.
- Example Specs already correct should remain green; half-recipe agent Specs start failing validate (desired).
