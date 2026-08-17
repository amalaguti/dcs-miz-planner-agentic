## Context

Stage A bound Syria with Incirlik=16, Turkey, Su-25T 251.0 MHz, invent
free_flight only. Live PyDCS `Syria.airport_list()` has 59 airports.
Numeric ids collide with other theatres (Palmyra 28 vs Mozdok 28 vs
NeedsOarPoint 28). PyDCS country `Syria` is distinct from Spec theatre
`Syria`; it typically parks on red.

## Goals / Non-Goals

**Goals:**

- Curate eight verified Syria airfields (not all 59).
- Add country `Syria` to era/modern only; keep Su-25T as the only modern player type.
- Compile a Palmyra free-flight smoke (Syria red) without lifting combat invent.
- Infer theatre from the new Spec keys; lookup stays theatre-scoped.

**Non-Goals:**

- Places, CAP/GA, domain, intercept spawn, extra countries (Israel / Jordan /
  Lebanon / Iran), dump of 59 fields.

## Decisions

1. **Eight airfields, not 59.** Live `airport_list()`: `Incirlik=16`,
   `RamatDavid=30` (PyDCS `Ramat David` / `Ramat_David`), `Damascus=7`,
   `BeirutRaficHariri=6` (`Beirut-Rafic Hariri`), `Aleppo=27`,
   `BasselAlAssad=21` (`Bassel Al-Assad` / `Bassel_Al_Assad`), `Palmyra=28`,
   `KingHusseinAirCollege=19` (`King Hussein Air College`). Mix Turkey /
   Israel / Levant / Jordan. Alternative (dump every AF) rejected — Caucasus
   curated 8.

2. **Country Syria modern, not WWII; player still Su-25T.** Era-keyed like
   Turkey/Russia. Adding the country makes it valid on Caucasus/Nevada/
   Falklands too (same leak as Georgia). Channel+country-Syria MUST fail
   unknown-country. Do not add Israel/Jordan/Lebanon this slice.

3. **Palmyra example is Syria red.** PyDCS parks country `Syria` on red;
   compile `_ensure_country` refuses moving it to blue. Invent/schema stay
   Incirlik Turkey blue. Stub LLM stays Manston. Palmyra 28 is not Mozdok 28.

4. **infer_theatre maps the new keys** (and keeps Incirlik). Combat refuse
   unchanged.

5. **N1-style Palmyra contracts**, not a full golden. Assert `airdromeId=28`
   on Syria theatre (not Caucasus Mozdok, not Normandy Needs Oar Point).

## Risks / Trade-offs

- [Palmyra 28 confused with Mozdok/NeedsOarPoint] → theatre-scoped lookup + test.
- [Syria country on blue compile fail] → Palmyra Spec uses `coalition: red`.
- [Invent leaves Incirlik] → intentional; extra AFs are validate/compile +
  find_airfield, not a new invent home.

## Migration Plan

Implement on `syria-airfields`. Rollback = revert the branch. Catalog sync
picks up new AFs/country without a schema bump. ME Instant Action do-soon
(`out/palmyra_cold_freeflight.miz`).

## Open Questions

- None.
