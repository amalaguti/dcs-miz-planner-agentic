## Context

Channel, Normandy, and Caucasus are planner-bound. Syria is installed and
PyDCS has `dcs.terrain.Syria` (59 airports). Invent schema special-cases
Caucasus; default is Manston. Making Syria offerable without a schema
envelope would copy Manston or Batumi onto the map.

Live PyDCS: Incirlik airdromeId **16**, 126 parking slots on the airport
object. Country `Turkey` (already on PyDCS Mission blue). Aircraft `Su-25T`
already in era `modern`. Radio 251.0 is the DCS/PyDCS modern UHF default.

## Goals / Non-Goals

**Goals:** Stage A bind + smoke; Turkey in modern era; Syria invent FF only;
dedicated schema notes (no Channel bundle leak).

**Non-Goals:** Extra AFs, places, combat, domain, intercept spawn, paid jets,
USA, ME Instant Action as merge gate.

## Decisions

1. **One AF:** `Incirlik: 16`. Do not dump 59 fields. Alternative (Damascus /
   Ramat David) rejected — Incirlik is the classic Syria starter with parking
   and a blue host country (Turkey), so player coalition can stay blue.

2. **Reuse era `modern`.** Add `Turkey` next to `Georgia` in
   `data/era/modern/countries.yaml`. Reuse `Su-25T` @ 251.0. Do not recreate
   the era. Payloads / ground / ships / failures stay wwii paths this slice.

3. **Era-filter at validate (already shipped F2).** Channel+Turkey →
   `unknown_country`. Syria+UK / Syria+Spitfire fail. Catalog listing MAY
   union for discovery.

4. **Turkey + Su-25T + 251.0.** Turkey is the Incirlik host (not USA/usaaf,
   not Georgia). 251.0 is the packaged modern group default — do not invent
   VHF or copy Incirlik ATC (122.1 / 360.1).

5. **Invent table** (every turn): TheChannel all six; Normandy FF+CAP;
   Caucasus FF only; Syria FF only (CAP refused). Schema Syria+FF →
   Incirlik example; Syria+combat raises with no Manston/NeedsOarPoint/Batumi.
   `infer_theatre`: JSON `Syria` or airfield `Incirlik`. Repair of
   domain/intercept errors must use inferred theatre — do not hardcode
   Caucasus or Normandy. `_notes_for("Syria")` returns `_SYRIA_FF_NOTES` only
   (F2 Bugbot: do not concatenate `_COMMON_NOTES` / `_TYPE_NOTES`).

6. **N1 compile contracts**, not a full golden. Date 2024-06-06 so WWII
   realism does not fire (`era != wwii` already no-ops).

7. **Hermetic inventory:** Syria AVAILABLE + `planner_supported=True`.
   Retarget `test_unsupported_installed_map` onto Nevada.

## Risks / Trade-offs

- [Manston/Batumi leak] offerable without schema → Mitigation: Incirlik
  envelope + combat raise + dedicated notes tuple.
- [Turkey on Channel] → Mitigation: era-filter validate (already in).
- [Syria-on-red] Damascus would force red coalition → Mitigation: pick
  Incirlik / Turkey / blue.
- [Parking] 126 slots — Mitigation: ME Instant Action do-soon.

## Migration Plan

One PR on `syria-cold-freeflight`. After merge, `dcs-miz theatres --refresh`
so cached `planner_supported` flips. Rollback = revert.

## Open Questions

- None blocking. Later: more AFs, modern combat, Nevada Stage A.
