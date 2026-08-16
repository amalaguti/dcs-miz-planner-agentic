## Context

Channel and Normandy are planner-bound (WWII era). Caucasus is installed and
PyDCS has `dcs.terrain.Caucasus` (21 airports). Registry `_KNOWN_ERAS` is
`wwii` only; the loader reads only `era/wwii`. Invent schema special-cases
Normandy; default is Manston. Making Caucasus offerable without a schema
envelope would copy Manston onto the map.

Live PyDCS: Batumi airdromeId **22**, 10 airplane parking slots. Country
`Georgia`. Aircraft `Su-25T` in `plane_map`. Radio 251.0 is the DCS/PyDCS
modern UHF default (not Spitfire VHF 124).

## Goals / Non-Goals

**Goals:** Stage A bind + smoke; era-filter validate; Caucasus invent FF only.

**Non-Goals:** Extra AFs, places, combat, domain, intercept spawn, paid jets,
USA/Russia, ME Instant Action as merge gate.

## Decisions

1. **One AF:** `Batumi: 22`. Do not dump 21 fields. Alternative (Sukhumi /
   Senaki) rejected — Batumi is the classic Caucasus starter with parking.

2. **Era `modern`**, not `wwii`. New `data/era/modern/{countries,aircraft}.yaml`.
   Loader walks `data/era/<id>/` for countries + aircraft only. Payloads /
   ground / ships / failures stay wwii paths this slice.

3. **Era-filter at validate.** `known_countries(era=)` and known aircraft via
   `era_for_theatre(spec.theatre)`. Flat union would leak Georgia/Su-25T onto
   Channel and break WWII-only tests. Catalog listing MAY union for discovery.

4. **Georgia + Su-25T + 251.0.** Georgia is the Batumi host country (not
   USAF/usaaf). Su-25T is the free ED module. 251.0 is sourced as the PyDCS
   modern group default — do not invent VHF.

5. **Invent table** (every turn): TheChannel all six; Normandy FF+CAP;
   Caucasus and other Stage A FF only (CAP refused). Schema Caucasus+FF →
   Batumi example; Caucasus+combat raises with no Manston/NeedsOarPoint.
   `infer_theatre`: JSON `Caucasus` or airfield `Batumi`. Repair of
   domain/intercept errors must use inferred theatre — do not hardcode
   Normandy.

6. **N1 compile contracts**, not a full golden. Date 2024-06-06 so WWII
   realism does not fire (`era != wwii` already no-ops).

## Risks / Trade-offs

- [Manston leak] offerable without schema → Mitigation: Batumi envelope +
  combat raise before planner_supported.
- [Georgia on Channel] → Mitigation: era-filter validate.
- [251 vs ATC] Batumi ATC is not flight radio → Mitigation: group frequency
  251.0 only.
- [Parking] 10 airplane slots — Mitigation: ME Instant Action do-soon.

## Migration Plan

One PR on `caucasus-cold-freeflight`. After merge, `dcs-miz theatres --refresh`
so cached `planner_supported` flips. Rollback = revert.

## Open Questions

- None blocking. Later: more AFs, modern combat, era-filter catalog tools.
