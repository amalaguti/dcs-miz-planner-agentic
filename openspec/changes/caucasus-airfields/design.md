## Context

Stage A bound Caucasus with Batumi=22, Georgia, Su-25T 251.0 MHz, invent
free_flight only. Live PyDCS `Caucasus.airport_list()` has 21 airports
(ids 12–32). Numeric ids collide with other theatres (Mozdok 28 vs
NeedsOarPoint 28). PyDCS `Russia` is country id 0 and defaults to red on a
new Mission.

## Goals / Non-Goals

**Goals:**

- Curate eight verified Caucasus airfields (not all 21).
- Add `Russia` to era/modern only; keep Su-25T as the only modern player type.
- Compile a Mozdok free-flight smoke (Russia red) without lifting combat invent.
- Infer theatre from the new Spec keys; lookup stays theatre-scoped.

**Non-Goals:**

- Places, CAP/GA, domain, intercept spawn, paid FC3 jets, extra countries
  (Abkhazia / SouthOssetia / Ukraine), dump of 21 fields.

## Decisions

1. **Eight airfields, not 21.** Live `airport_list()`: `Batumi=22`,
   `Kobuleti=24`, `SenakiKolkhi=23` (PyDCS `Senaki-Kolkhi` / `Senaki_Kolkhi`),
   `Kutaisi=25`, `TbilisiLochini=29` (`Tbilisi-Lochini`), `Vaziani=31`,
   `SochiAdler=18` (`Sochi-Adler`), `Mozdok=28`. Mix Georgia coast/inland +
   Russian-side coast/inland. Alternative (dump every AF) rejected — Channel
   curated 12; Normandy curated 8.

2. **Russia modern, not WWII; player still Su-25T.** Era-keyed like Georgia.
   Adding Russia makes it valid on Syria/Nevada/Falklands too (same leak as
   Georgia). Channel+Russia MUST fail unknown-country. Do not add paid
   `Su-25` / `Su-27` / `A-10A` / `F-15C`. Alternative (Russia theatre YAML)
   rejected — countries stay era packages.

3. **Mozdok example is Russia red.** PyDCS parks `Russia` on red; compile
   `_ensure_country` refuses moving it to blue. Invent/schema stay Batumi
   Georgia blue. Stub LLM stays Manston.

4. **infer_theatre maps the new keys** (and keeps Batumi). Combat refuse
   unchanged.

5. **N1-style Mozdok contracts**, not a full golden. Assert `airdromeId=28`
   on Caucasus theatre (not Normandy Needs Oar Point). Channel goldens stay
   untouched.

## Risks / Trade-offs

- [Mozdok 28 confused with NeedsOarPoint] → theatre-scoped lookup + test.
- [Russia on blue compile fail] → Mozdok Spec uses `coalition: red`.
- [Invent leaves Batumi] → intentional; extra AFs are validate/compile +
  find_airfield, not a new invent home.

## Migration Plan

Implement on `caucasus-airfields`. Rollback = revert the branch. Catalog sync
picks up new AFs/Russia without a schema bump. ME Instant Action do-soon
(`out/mozdok_cold_freeflight.miz`).

## Open Questions

- None.
