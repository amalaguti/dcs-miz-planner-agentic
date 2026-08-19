## Context

Channel, Normandy, Caucasus, Syria, Nevada, and Falklands are planner-bound.
Kola is installed and, after R8, PyDCS has `dcs.terrain.Kola` (37 airports).
Fail-closed tests still use Kola as the unbound stand-in; this slice binds it
and must retarget those tests onto Iraq (no pydcs module) and GermanyCW
(`dcs.terrain.Germany`, terrain name `GermanyCW`).

Live PyDCS (git `e20f328`): Bodo airdromeId **7**, 94 parking slots, class
`Bodo`. Country `Norway` is `dcs.countries.Norway` id 12. Radio 251.0 is the
packaged modern UHF default.

## Goals / Non-Goals

**Goals:** Stage A bind + smoke; Norway in modern era only; Kola invent FF
only; dedicated schema notes; immersion floor stays TheChannel-only.

**Non-Goals:** Extra AFs, places, combat, Finland/Sweden/Russia hosts, paid
jets, dual-offer strike trucks, ME Instant Action as merge gate. Do not bind
Iraq / `MarianaIslandsWWII` / GermanyCW.

## Decisions

1. **One AF:** `Bodo: 7`. Live `airport_list()`; 94 parking slots. Do not dump
   37 fields. Banak (id 1, 26 slots) and Rovaniemi (id 2) are deferred.

2. **Reuse era `modern`.** Add `Norway` next to Georgia, Turkey, USA, UK,
   Russia, Syria, Argentina. Do not put Norway in `era/wwii`. Reuse `Su-25T`
   @ 251.0. Spitfire stays dual-era (Kola+Spitfire validates; Channel+Su-25T
   still unknown).

3. **Era-filter.** Channel+Norway → `unknown_country`. Channel+UK still OK
   (wwii). Kola+Norway+Su-25T OK.

4. **Norway + Su-25T + 251.0.** Host nation at Bodo. Do not copy ATC.

5. **Invent table** (every turn): existing six maps unchanged; **Kola FF
   only**. Schema Kola+FF → Bodo example. Combat types raise
   `combat_unsupported_theatre`. `infer_theatre`: JSON `Kola` or airfield
   `Bodo`. `_notes_for("Kola")` returns `_KOLA_FF_NOTES` only (no
   `_COMMON_NOTES`). Repair must use inferred theatre — do not hardcode
   MountPleasant/Nellis/Incirlik onto Kola.

6. **N1 compile contracts.** Date 2024-06-06 so WWII realism no-ops.
   airdromeId 7, start_time 32400, TakeOffParking, Player, frequency 251.0.

7. **Hermetic inventory:** Kola AVAILABLE + `planner_supported=True`. Add
   Iraq to the install fixture as the unsupported installed map.
   `list_strike_targets(theatre="Kola")` stays empty of dual-offered trucks
   (do not add Kola to the Syria/Nevada/Falklands dual-offer set).

8. **Unbound stand-in:** compile-without-binding and domain/intercept
   `theatre=` copies use **Iraq**. “Exists in pydcs but unbound” uses
   **GermanyCW**.

## Risks / Trade-offs

- [Bodo vs Banak] → Mitigation: Bodo has 94 parking slots vs Banak 26; Spec
  key matches PyDCS name (no underscore).
- [Norway modern-only] → Mitigation: validate by `era_for_theatre`.
- [Prior-map leak] → Mitigation: dedicated notes + Stage A generic refuse.

## Migration Plan

One PR on `kola-cold-freeflight`. After merge, `dcs-miz theatres --refresh`.
Rollback = revert.

## Open Questions

- None blocking. Later: more AFs, Finland/Sweden/Russia, combat. Iraq and
  Marianas WWII stay discovered-only (no pydcs terrain).
