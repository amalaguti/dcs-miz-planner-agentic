## Context

Continuous altitude/speed → message without cooldown spams. User wants timed re-warn.

## Goals / Non-Goals

**Goals:** Example + behaviour card use warn → cooldown flag → `time_since_flag` re-warn;
clear on recovery; soft-warn fractional thresholds.

**Non-Goals:** Auto-rewriting agent Specs; new condition types.

## Decisions

1. **Per-axis cooldown flags** `alt_gate_cd` / `spd_gate_cd`.
2. **First warn:** high/fast + `flag_is` false → message + `set_flag` true.
3. **Re-warn:** still high/fast + `time_since_flag` ≥ 45s → message + `set_flag` true
   (resets timer).
4. **Clear:** `unit_altitude_lower` / `unit_speed_lower` at same threshold → `set_flag`
   false.
5. **Keep** `time_more` ~30s on warn/rewarn to avoid parking spam.
6. **Soft-warn** `gate_threshold_truncated` when altitude_m or speed_kmh ≠ int(value).

## Risks / Trade-offs

- [Exact threshold gap] → higher/lower are exclusive at the boundary; acceptable.
- [45s hardcoded in example] → documented in recipe; authors can change seconds.
