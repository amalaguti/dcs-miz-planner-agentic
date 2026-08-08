## Context

R13 inventory in gitignored `research/campaign-units.md`. Promote curated
shortlist only — Allied practice labels where needed.

## Goals / Non-Goals

**Goals:** Shelf R13 AAA / armor / train coach / Allied landing ships; wire
classes + motion + AAA AI; examples + tests.

**Non-Goals:** Modern junk; scenery; helos; mesh snap.

## Decisions

1. **AAA** — `flak41` Axis; `M45_Quadmount`, `QF_37_AA`, `Allies_Director`
   Allied practice — all in `_AAA_UNIT_IDS` + aaa_guns.
2. **Armor** — heavies/TD from campaigns; motion `armor` profile.
3. **Trains** — add campaign `Coach cargo` / `Coach cargo open` (not modern
   electric).
4. **Sea** — `LST_Mk2`, `USS_Samuel_Chase` as Allied landing / practice; sea_cargo
   speed band; harbour cues OK.
5. **Examples** — flak41 AAA GA + LST harbour/coast GA.

## Risks / Trade-offs

- [Allied landing ships on Axis coast] → Labels note Allied/practice; useful for
  invent variety.
- [Tiger/Panther era stretch] → Campaigns use them; keep with Axis labels.

## Migration Plan

- Additive; catalog sync; no schema bump.

## Open Questions

- None.
