## Context

Slice 0b fail-closes land/sea domain off TheChannel; F1b added Normandy’s UK–Cotentin
chord. Caucasus Stage C shipped Batumi CAP at **270° / 40 km** (sea). A land strike
needs Colchis inland geometry measured from PyDCS, not copied CAP 270/40, Manston
125/76, or Cherbourg 180/63. WWII trucks must not be the Caucasus default; modern
`vehicle_map` ids were verified in pydcs 0.15.0.

## Goals / Non-Goals

**Goals:**

- Validate + compile a Batumi ground_attack with Russia land trucks inland past Kutaisi.
- Invent/chat may emit Caucasus `ground_attack` every turn; intercept/escort/recon still refuse.
- Domain classifier for Caucasus using curated coastal vs inland airport ids (not Channel/Normandy ids).
- Catalog offers modern **land** units on Caucasus; Channel WWII trucks stay Channel-tagged.

**Non-Goals:**

- Intercept spawn recipe, escort/recon, path clamp on Caucasus, Shilka/`aaa_alert`,
  QAG promote, schema bump unless a filter cannot express modern-land-on-Caucasus.
- Instant Action as merge gate.

## Decisions

1. **Strike geometry 43° / 110 km** (not 270/40, not 43/100).
   PyDCS `heading_between_point` Batumi (22) → Kutaisi (25) is **43.14° / 97.20 km**.
   Integer 43° / 100 km is only ~2.8 km from Kutaisi (near-airport land — reject).
   43° / 110 km is ~12.8 km past Kutaisi. Document the measurement in the example
   YAML comment. Do not invent lat/lon.

2. **Caucasus domain = west-of-coast seaward sector**, not a Batumi–Kutaisi chord
   (that chord is over Colchis land). Curated ids:
   - Coastal: Batumi 22, Kobuleti 24, Sochi-Adler 18.
   - Inland: Senaki-Kolkhi 23, Kutaisi 25, Tbilisi-Lochini 29, Vaziani 31, Mozdok 28.
   Near any curated AF (3 km) → land. Else if nearest curated is inland → land.
   Else nearest is coastal and heading from that AF is 270° ± 45° ([225, 315]) → sea.
   Else land. CAP 270/40 **must** classify sea. GA 43/110 **must** classify land.
   Sochi-due-south water is a known gap (out of scope). Never run Channel or
   Normandy airport ids on Caucasus x,y. Path clamp stays TheChannel-only.

3. **Modern trucks only** (`Ural-375`, `GAZ-66`, `ZIL-135` from `vehicle_map`).
   Country **Russia** red (model default is `ThirdReich`). Do not append these ids
   onto Channel `soft_vehicles` `unit_ids`. New class `modern_soft_vehicles`.
   Skip `ZSU-23-4 Shilka` until `_AAA_UNIT_IDS` is extended. Static smoke — no new
   motion YAML (reuse existing soft band only if a later slice adds path).

4. **Su-25T payload `su25t_2x_fab250`.** FAB-250 CLSID
   `{3C612111-C7AD-476E-8A8E-2485812F4E5C}` exists on pylons 2–5 and 7–10
   (`Su_25T.PylonN.FAB_250___250kg_GP_Bomb_LD`). Inner pair is **5 and 7**
   (symmetric around missing centreline 6). Do not harvest live DCS UnitPayloads.
   Spitfire CLSIDs must not go on Su-25T.

5. **Catalog: tag modern units `theatre_id=Caucasus`, `era_id=modern` at sync.**
   WWII rows stay `TheChannel` / `wwii` (Normandy query-time dual-offer unchanged).
   `list_strike_targets(theatre="Caucasus")` returns the three trucks, not Blitz.
   Channel filter must not return Ural-375. Syria/Nevada/Falklands stay empty.
   No catalog schema bump.

6. **Invent allow-table** adds `GROUND_ATTACK` for Caucasus. Schema loads
   `batumi_kutaisi_ground_attack.yaml`. Dedicated `_CAUCASUS_GA_NOTES` — do not
   concatenate `_TYPE_NOTES` (those cite french_coast / Manston). Intercept/escort/
   recon still raise `combat_unsupported_theatre`. Soft immersion floor stays
   TheChannel-only. Stub LLM stays Manston.

7. **Place `kutaisi_inland_strike`**: family `channel_place`, meta theatre Caucasus,
   domain land, 43/110/2000, related `modern_soft_vehicles`, example path. Update
   `batumi_home` `mission_types` to include `ground_attack`. CAP place stays sea /
   CAP-only.

8. **Tests:** validate+compile new example (airdromeId 22, Su-25T, Ural-375, Russia,
   theatre zip Caucasus, FAB-250 CLSID). Domain: 270/40 sea, 43/110 land; Channel
   and Normandy GA still land. Invent: GA allowed, intercept still refused every
   turn. Channel intercept goldens bit-identical. Schema Caucasus+GA has no
   Manston skeleton. Fail-closed domain moves to Syria (not Caucasus).

## Risks / Trade-offs

- [West-sector misclassifies Sochi-south water as land] → Known gap; smoke uses
  Batumi 270/40 (sea) and 43/110 (land via nearest-inland Kutaisi). Tests lock both.
- [Invent copies 270/40 onto GA] → That point classifies sea; schema/place/prompts
  name Kutaisi 43/110.
- [Ural-375 leaks onto Channel invent] → Separate class; catalog theatre tag;
  do not add to Channel `soft_vehicles` unit_ids.

## Migration Plan

Implement on `caucasus-ground-attack`. No catalog schema version bump. Rollback =
revert the branch. Channel goldens must stay green.

## Open Questions

None — Instant Action is do-soon after merge, not a gate.
