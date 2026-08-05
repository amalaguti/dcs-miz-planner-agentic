## Context

Shared `validate_mission_spec` (`validation.py`) is index/emptiness-focused for triggers.
Late-act groups can compile dormant; `message.delay_s` is ignored at emit; country/skill and
intercept/CAP enemy coalition fail only at compile or never. Gold path:
`examples/manston_dawn_intercept_radio.yaml`.

## Goals / Non-Goals

**Goals:** Fail-left errors for B1/B3/B4/B5/(B9) so validate and compile agree on these cases.

**Non-Goals:** Real delayed messages; `#34` terrain; `#30c` prompt/memory; soft warnings API.

## Decisions

1. **Errors only** — No new warning channel; binary `ValidationResult.ok` stays.
   *Alt:* soft-warn half-recipes — rejected; dormant bandits must not be green.

2. **Late-act ↔ activate graph** — Bidirectional: each `late_activation: true` enemy/target
   index MUST appear in ≥1 `activate_group`; each activate/deactivate MUST reference a
   late-activated group. Ignore whether activation is radio- vs time-gated (both valid).
   *Alt:* require radio menu too — rejected; time-based scramble is legitimate.

3. **`delay_s > 0` → error** — Reject in validation (and optionally pydantic `le=0` or
   forbid nonzero). Do not implement ME delay in this change.
   *Alt:* strip field silently — rejected; authors must see the lie.

4. **Country/skill allowlists** — Shared constants (or thin helpers) reused by validation and
   compiler: Channel countries at least `UK`, `ThirdReich` (catalog-aligned); skills =
   PyDCS `Skill` member names. Unknown → error with hint (`Germany` → use `ThirdReich` on red).
   *Alt:* call PyDCS from validation — prefer allowlist to keep validate import-light;
   can mirror `_skill_from_name` names without importing dcs if listed explicitly.

5. **Intercept/CAP opposing enemies** — Same `opposing_coalition(player)` rule as escort
   enemies, in `_validate_enemy_aircraft` (or shared helper).

6. **Dead-on-late-act** — If any trigger condition references a late-act enemy/target via
   `unit_dead` / `target_dead` / `group_life_less` (and that group is late-act), require that
   group already satisfies the activate-graph rule (covered by decision 2). Explicit extra
   error only if we need clearer messaging; graph rule is sufficient for B9 win-stall.
   Document in LESSONS that win-on-dead needs activate path.

7. **Stable error codes** — e.g. `late_activation_no_activate`, `activate_not_late`,
   `message_delay_unsupported`, `unknown_country`, `unknown_skill`, `friendly_enemy`.

## Risks / Trade-offs

- [Agent Specs that half-applied radio recipes start failing] → Desired; pairs with `#30c`.
- [Hand Specs using activate without late_act] → Must set `late_activation: true`.
- [Country allowlist too narrow for future theatres] → Channel-only list + LESSONS; expand with `#39`.
- [Pydantic vs validation drift] → Prefer validation as semantic SoT; add pydantic only for
  `delay_s` if load-before-validate paths need it.

## Migration Plan

Branch `validation-false-green`. Fix any example that fails (expect radio example green).
No DB migrate. Rollback = revert.

## Open Questions

- None blocking; exact skill name list can follow compiler’s PyDCS enum at implement time.
