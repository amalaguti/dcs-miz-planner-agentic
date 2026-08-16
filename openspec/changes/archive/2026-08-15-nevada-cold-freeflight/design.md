## Context

Channel, Normandy, Caucasus, and Syria are planner-bound. Nevada is installed
and PyDCS has `dcs.terrain.Nevada` (17 airports). F3 retargeted the
unsupported-map test onto Nevada; this slice binds Nevada and must retarget
that test onto Falklands.

Live PyDCS: Nellis airdromeId **4**, 247 parking slots. Country `USA` (already
on PyDCS Mission blue). Aircraft `Su-25T` already in era `modern`. Radio 251.0
is the packaged modern UHF default. F2 rejected USA at Batumi because Batumi’s
host is Georgia; Nellis is a US host.

## Goals / Non-Goals

**Goals:** Stage A bind + smoke; USA in modern era; Nevada invent FF only;
dedicated schema notes; immersion floor stays TheChannel-only.

**Non-Goals:** Extra AFs, places, combat, domain, intercept spawn, paid jets,
extra countries, ME Instant Action as merge gate.

## Decisions

1. **One AF:** `Nellis: 4`. Do not dump 17 fields. Creech / Groom Lake
   rejected — Nellis is the classic starter with parking.

2. **Reuse era `modern`.** Add `USA` next to Georgia and Turkey. Reuse
   `Su-25T` @ 251.0. `usaaf` is not a country. Payloads / ground / ships /
   failures stay wwii paths.

3. **Era-filter at validate.** Channel+USA → `unknown_country`. Nevada+UK /
   Nevada+Spitfire fail. Catalog listing MAY union.

4. **USA + Su-25T + 251.0.** USA is the Nellis host (not usaaf). Do not copy
   Nellis ATC (132.55 / 327.0) as flight radio.

5. **Invent table** (every turn): TheChannel all six; Normandy FF+CAP;
   Caucasus FF only; Syria FF only; Nevada FF only (CAP refused). Schema
   Nevada+FF → Nellis example; Nevada+combat raises with no prior-map
   skeleton. `infer_theatre`: JSON `Nevada` or airfield `Nellis`. Repair
   must use inferred theatre. `_notes_for("Nevada")` returns
   `_NEVADA_FF_NOTES` only. Soft immersion floor stays TheChannel-only.

6. **N1 compile contracts.** Date 2024-06-06 so WWII realism no-ops.

7. **Hermetic inventory:** Nevada AVAILABLE + `planner_supported=True`.
   Retarget `test_unsupported_installed_map` onto Falklands.

## Risks / Trade-offs

- [Prior-map leak] → Mitigation: Nellis envelope + combat raise + dedicated
  notes + Channel-only immersion floor.
- [USA on Channel] → Mitigation: era-filter validate.
- [usaaf vs USA] → Mitigation: country is `USA`; voice id stays `usaaf`.

## Migration Plan

One PR on `nevada-cold-freeflight`. After merge, `dcs-miz theatres --refresh`.
Rollback = revert.

## Open Questions

- None blocking. Later: more AFs, modern combat, Falklands Stage A.
