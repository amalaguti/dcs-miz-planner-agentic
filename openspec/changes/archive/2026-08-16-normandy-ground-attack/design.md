## Context

Slice 0b fail-closes land/sea domain off TheChannel. F1 lifted Normandy invent to free_flight + CAP. WWII ground units already live in `data/era/wwii/ground_units.yaml`; catalog sync tags every strike row `theatre_id=TheChannel`, so `list_strike_targets(theatre="Normandy")` is empty. CAP station `cherbourg_channel_cap` (180° / 63 km) is **sea**. A land strike needs Cotentin geometry measured from PyDCS, not copied Channel 125/76.

## Goals / Non-Goals

**Goals:**

- Validate + compile a Needs Oar Point ground_attack with Axis land targets inland of Maupertus.
- Invent/chat may emit Normandy `ground_attack` every turn; intercept/escort/recon still refuse.
- Domain classifier for Normandy using curated UK vs French airport ids (not Channel ids).
- Catalog offers existing WWII **land** units on Normandy; sea stays Channel-only.

**Non-Goals:**

- Intercept spawn recipe, escort/recon, path clamp on Normandy, new unit ids, QAG promote, schema bump unless a filter cannot express dual-theatre land units.
- Instant Action as merge gate.

## Decisions

1. **Strike geometry 180° / 133 km** (not 180/63).
   PyDCS `heading_between_point` NeedsOarPoint (28) → Maupertus (4) is **180.22° / 125.29 km**. Integer 180° / 125 km is on the field (near-airport land). 180° / 120 km is still sea on a UK–Cotentin chord. 180° / 133 km is ~8 km inland of Maupertus — same “past the coast” pattern as Channel 125° / 76 km inland of Dunkirk. Document the measurement in the example YAML comment. Do not invent lat/lon.

2. **Normandy domain = UK–Cotentin chord**, same algorithm as Channel with different airport sets.
   - UK: NeedsOarPoint 28, Chailey 27, Funtington 29, Tangmere 30, FordAF 31.
   - FR: Maupertus 4, SaintPierreduMont 1, Carpiquet 19.
   Near-airport (3 km) → land; else if d_uk + d_fr ≤ chord + 8 km slack → sea; else land.
   `classify_domain_for_theatre` dispatches TheChannel vs Normandy; other theatres still raise `DomainUnsupportedTheatre`. Never run Channel ids on Normandy x,y.

3. **Targets reuse shipped WWII ids** (`Blitz_36-6700A` + `flak18` / `aaa_alert`). No YAML unit adds. Artillery class stays empty.

4. **Catalog: query-time dual offer, no schema bump.** Keep one row per unit (`theatre_id=TheChannel`). `list_strike_targets(theatre="Normandy")` includes land + `era_id=wwii` Channel-tagged units; sea_craft stay excluded. Unfiltered / TheChannel lists stay unique. Caucasus/Syria/Nevada/Falklands stay empty.

5. **Invent allow-table** adds `GROUND_ATTACK` for Normandy. Schema loads `needs_oar_point_ground_attack.yaml`. Dedicated `_NORMANDY_GA_NOTES` — do not concatenate `_TYPE_NOTES` (those cite french_coast / Manston). Intercept/escort/recon still raise `combat_unsupported_theatre`. Soft immersion floor stays TheChannel-only. Stub LLM stays Manston. `infer_theatre` may map `Maupertus` → Normandy.

6. **Place `maupertus_inland_strike`**: family `channel_place`, meta theatre Normandy, domain land, 180/133/2000, related soft + AAA, example path. Update `needs_oar_point_home` `mission_types` to include `ground_attack`. Path clamp remains TheChannel-only (static smoke; french_coast deltas must not rewrite onto Normandy).

7. **Tests:** validate+compile new example (airdromeId 28, Spitfire, Blitz, flak18, theatre zip Normandy). Domain: 180/63 sea, 180/133 land; Channel GA still land. Invent: GA allowed, intercept still refused every turn. Channel intercept goldens bit-identical. Schema Normandy+GA has no Manston skeleton.

## Risks / Trade-offs

- [Chord misclassifies some inland points] → Smoke uses 180/133 which is land via both near-field and inland rules; tests lock 63 vs 133.
- [Invent copies 125/76 onto NeedsOarPoint] → That point can classify land (FordAF) but is the wrong fight; schema/place/prompts name Maupertus 180/133.
- [Catalog theatre field still says TheChannel on Normandy hits] → Acceptable; filter is the contract. Schema bump deferred.

## Migration Plan

Implement on `normandy-ground-attack`. No catalog schema version bump. Rollback = revert the branch. Channel goldens must stay green.

## Open Questions

None — Instant Action is do-soon after merge, not a gate.
