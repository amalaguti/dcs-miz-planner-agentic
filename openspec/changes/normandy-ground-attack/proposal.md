## Why

Normandy invent can fly CAP but cannot place WWII ground targets. Channel already has a land/sea domain recipe, strike shelf, and GA examples; Normandy still fail-closes domain and returns an empty strike list. Stage 0b is on master, so this is the Stage C combat slice: Needs Oar Point ground_attack onto Axis Cotentin land, using existing WWII unit ids.

## What Changes

- Allow invent/chat **ground_attack** on Normandy (NeedsOarPoint, Spitfire, `sunny_clear`, UK blue). Intercept / escort / recon stay every-turn refuse.
- Add a Normandy land/sea domain recipe (UK vs Cotentin airport chord). Do not run the Channel UK–FR chord on Normandy x,y.
- Ship `examples/needs_oar_point_ground_attack.yaml`: strike inland of Maupertus (measured PyDCS 180° / 133 km from NeedsOarPoint). Soft trucks plus Flak 18 from the existing WWII shelf (`Blitz_36-6700A`, `flak18`). Payload `spitfire_2x250_slipper`.
- Add `channel_place` row `maupertus_inland_strike` (`meta.theatre: Normandy`). Family name stays `channel_place`.
- Offer WWII **land** strike units on `list_strike_targets(theatre="Normandy")`. Sea craft stay Channel-only.
- Schema `theatre=Normandy` + `ground_attack` loads the new example with dedicated notes (no Channel french-coast concatenation).

## Non-goals

- Normandy intercept spawn, escort, recon, path clamp, harbour/sea GA, extra unit YAML, artillery class, QAG scrape, `theatre_place` rename, all 38 airfields, Caucasus/Syria/Nevada/Falklands combat.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Normandy invent is free_flight, CAP, **or ground_attack**; intercept/escort/recon still refuse; do not copy Channel geometry onto Normandy.
- `agent-tools`: schema Normandy+GA example; `list_strike_targets(theatre=Normandy)` returns land WWII units.
- `mission-options`: `maupertus_inland_strike` place recipe.
- `agent-catalog`: WWII land strike units offered for Normandy after sync.
- `mission-validation`: Normandy land/sea domain; well-formed Normandy GA validates.
- `miz-compiler`: Normandy GA compiles (N1-style contracts).

## Impact

`channel_domain.py`, invent allow-table / schema / prompts, catalog strike filter, `planning_options.yaml`, new GA example + tests. Channel Hawkinge intercept goldens and Manston GA stay bit-identical. Acceptance: ruff + pytest + compile the new example. ME Instant Action at Needs Oar Point is do-soon after merge.
