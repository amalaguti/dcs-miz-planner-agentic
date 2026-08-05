## Why

Validate can be green for ground-attack Specs whose strike point is mid-Channel while
targets are land trucks (or ships inland). `randomize` geometry jitter makes this worse.
Adversarial B2 / LESSONS Channel land-vs-water checks.

## What Changes

- Resolve strike Point the same way as compile (airfield + bearing/distance via Channel terrain).
- Classify Channel map points as land vs sea (coast-airport heuristic; no DCS runtime DEM).
- Validate: each target’s registry domain (`land`/`sea`) MUST match the strike point domain.
- Randomize: when jittering strike geometry, redraw until domain still matches targets (or keep original).
- Tests: good Manston GA example; deliberate water strike with land unit fails; randomize preserves domain.

## Non-goals

- Full heightmap / DCS `land.getSurfaceType`; non-Channel theatres (`#39`); enemy-held political borders beyond domain.

## Capabilities

### Modified
- `mission-validation`: strike domain vs target unit domain.
- `mission-randomization`: geometry jitter preserves strike domain for GA.

## Impact

New `channel_domain.py` (lazy PyDCS); `validation.py`; `randomize.py`; tests; LESSONS/BACKLOG.
