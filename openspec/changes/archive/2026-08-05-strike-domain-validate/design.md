## Context

B2 — no terrain probe at validate; randomize can put trucks in water.

## Decisions

1. Lazy PyDCS `TheChannel` for airport positions (same as compile).
2. Domain heuristic: nearest UK vs FR Channel airport; near either ≤3 km → land;
   if roughly on the UK–FR chord (dU+dF ≤ dUF+8 km) → sea; else land.
3. Validate error `strike_domain_mismatch` with bearing/distance hint.
4. Randomize retries strike jitter up to 24 draws; fallback to pre-jitter strike.

## Risks

- [Heuristic edge cases near coast] → Calibrated to LESSONS examples; document limits.
- [PyDCS import in validate] → Lazy, Channel-only for now.
