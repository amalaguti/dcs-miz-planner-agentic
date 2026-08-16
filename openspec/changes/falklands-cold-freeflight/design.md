## Context

Channel, Normandy, Caucasus, Syria, and Nevada are planner-bound. Falklands
is installed and PyDCS has `dcs.terrain.Falklands` (27 airports). F4
retargeted the unsupported-map test onto Falklands; this slice binds it and
must retarget that test onto Kola (installed, no PyDCS).

Live PyDCS: Mount Pleasant airdromeId **2**, 37 parking slots. PyDCS class
`Mount_Pleasant`; Spec key **`MountPleasant`** (FordAF lesson). Country `UK`
already exists for WWII; add it to era `modern` so Falklands can use UK+Su-25T
without putting Frogfoot on Channel. Radio 251.0 is the packaged modern UHF
default. ATC 133.35 / 250.8 is not flight radio.

## Goals / Non-Goals

**Goals:** Stage A bind + smoke; UK in modern era (keep wwii UK); Falklands
invent FF only; dedicated schema notes; immersion floor stays TheChannel-only.

**Non-Goals:** Extra AFs, places, combat, Argentina/Chile, paid jets, ME
Instant Action as merge gate.

## Decisions

1. **One AF:** `MountPleasant: 2`. Do not dump 27 fields. Port Stanley
   rejected (civilian, thinner parking).

2. **Reuse era `modern`.** Add `UK` next to Georgia, Turkey, USA. Keep
   `era/wwii` UK + ThirdReich. Reuse `Su-25T` @ 251.0. Spitfire stays wwii.

3. **Era-filter.** Channel+UK still OK (wwii). Falklands+Spitfire →
   `unknown_aircraft`. Falklands+USA → `unknown_country`. Channel+Su-25T
   still unknown.

4. **UK + Su-25T + 251.0.** RAF host at Mount Pleasant. Do not copy ATC.

5. **Invent table** (every turn): TheChannel all six; Normandy FF+CAP;
   Caucasus/Syria/Nevada/Falklands FF only. Schema Falklands+FF → Mount
   Pleasant example. `infer_theatre`: JSON `Falklands` or airfield
   `MountPleasant`. `_notes_for("Falklands")` returns `_FALKLANDS_FF_NOTES`
   only. Repair must use inferred theatre.

6. **N1 compile contracts.** Date 2024-06-06 so WWII realism no-ops.

7. **Hermetic inventory:** Falklands AVAILABLE + `planner_supported=True`.
   Retarget `test_unsupported_installed_map` onto Kola.

## Risks / Trade-offs

- [Mount_Pleasant vs MountPleasant] → Mitigation: Spec key without underscore;
  comment PyDCS name.
- [UK dual-era] → Mitigation: validate by `era_for_theatre`, not a flat union.
- [Prior-map leak] → Mitigation: dedicated notes + Channel-only immersion floor.

## Migration Plan

One PR on `falklands-cold-freeflight`. After merge, `dcs-miz theatres --refresh`.
Rollback = revert.

## Open Questions

- None blocking. Later: more AFs, Argentina/Chile, combat. Unbound maps
  (Kola / Iraq / MarianaIslandsWWII) stay discovered-only until PyDCS exists.
