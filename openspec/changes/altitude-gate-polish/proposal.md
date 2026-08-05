## Why

Altitude/speed gate examples use bare continuous (`once: false`) message rules. While the
pilot stays out of limits, DCS can re-fire every evaluate tick → message spam. A one-shot
latch forever risks a missed first warning. Pilots need: warn, quiet gap, re-warn if still
violating, clear when corrected. Emit also silently truncates `altitude_m` via `int()`.

## What Changes

- Rewrite `manston_freeflight_altitude_speed_gates.yaml` to a flag + `time_since_flag`
  re-warn recipe (~45s) for altitude and speed; clear flags when back in limits.
- Update `altitude_speed_gates` planning_option recipe text and LESSONS/docs.
- Soft-warn (non-blocking) when `altitude_m` / `speed_kmh` are non-integers (emit
  truncates).
- Refresh trigger-rich golden for gates; adjust tests.

## Non-goals

- New ME predicates; changing PyDCS continuous semantics globally.
- Hard-fail on fractional altitudes (warn only).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-triggers` or `golden-fixtures`: Document re-warn recipe for altitude/speed
  gates; soft-warn non-integer gate thresholds.
- Prefer `mission-triggers` for recipe/docs + `mission-validation` for soft-warn.

## Impact

- Example YAML, planning_options, validation warnings, golden refresh, tests, LESSONS.
