## Why

Domain-mismatch repair always injects Channel `french_coast_strike_belt` 125°/76 km,
so a Batumi recon that parked the AOI on CAP 270/40 sea (with land trucks) is
steered toward Manston instead of `kutaisi_inland_strike` 43°/110 km.

## What Changes

- `host_spec_repair_nudge` for `motion_domain_mismatch` / `strike_domain_mismatch`
  uses the inferred theatre: Channel 125/76; Caucasus Kutaisi 43/110; Normandy
  Maupertus 180/133. Other theatres MUST NOT receive french-coast geometry.

## Non-goals

- Path clamp stays TheChannel-only. Syria domain classifier. Changing goldens.

## Capabilities

### New Capabilities
- (none)

### Modified Capabilities
- `nl-agent`: domain-mismatch repair is theatre-keyed.

## Impact

`agent/prompts.py` + tests. Channel mismatch nudges stay 125/76 when theatre is
TheChannel or unspecified.
