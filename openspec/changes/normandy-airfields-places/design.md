## Context

Slice 0b is on master: invent may offer Normandy as free_flight only;
`host_normandy_combat_nudge` refuses every combat type every turn; domain,
intercept spawn, and path clamp fail closed or skip off TheChannel. Packaged
Normandy airfields are `NeedsOarPoint: 28` only. CAP on a valid Normandy
airfield already validates and compiles (airfield-relative `_place_cap_enemies`);
invent still refuses it.

Live PyDCS `Normandy.airport_list()` has 38 airports (ids 37 and 39 absent).
Research computed CAP station **180° / 63 km** from Needs Oar Point toward
Maupertus (mid-Channel, sea). Intercept has no documented spawn offset.

## Goals / Non-Goals

**Goals:**

- Curate eight verified Normandy airfields.
- Add two `channel_place` rows (`meta.theatre: Normandy`) and filter
  `list_mission_options(theatre=)` so Channel invent cannot pick them.
- Ship one CAP example; lift invent/schema refuse for **CAP only**.

**Non-Goals:**

- GA / intercept / escort / recon on Normandy.
- Domain classifier, intercept spawn recipe, path clamp, strike dual-tag.
- `theatre_place` rename; USA country; extra unit YAML; all 38 AFs; fake ICAO.
- Full golden dump of the new CAP `.miz`.

## Decisions

1. **Eight airfields, not 38.** Spec keys from live `airport_list()`:
   `NeedsOarPoint=28`, `Chailey=27`, `Funtington=29`, `Tangmere=30`,
   `FordAF=31` (PyDCS name `Ford_AF`), `Maupertus=4`,
   `SaintPierreduMont=1`, `Carpiquet=19`. Theatre-scoped lookup already
   exists. Alternative (dump every AF) rejected — Channel curated 12 of many.

2. **CAP-only combat this slice.** Station 180° / 63 km / 4000 m from
   NeedsOarPoint (midpoint toward Maupertus). Leave domain fail-closed so
   GA/recon cannot silently use the UK–FR chord. Leave intercept fail-closed
   (no Hawkinge-style offset). Alternative (ship GA at 166°/166 km) deferred
   until a Normandy domain recipe and strike-catalog tag exist.

3. **Keep family `channel_place`.** New rows `needs_oar_point_home` and
   `cherbourg_channel_cap` with `meta.theatre: Normandy`. Do not rename to
   `theatre_place` (cross-cutting, no extra invent power). Filter
   `list_mission_options(*, theatre=)` on `channel_place` via `meta.theatre`.
   Other families pass through. Omitted `theatre=` returns all (backward
   compatible). Alternative (prompt-only filter) rejected — Channel invent
   could copy Cherbourg geometry onto Manston.

4. **Lift nudge for CAP only.** Drop `CAP` from `_NORMANDY_COMBAT_TYPES`.
   Intercept / GA / escort / recon stay every-turn refuse (never capture or
   write). Schema `theatre=Normandy` + `cap` loads
   `examples/needs_oar_point_cap.yaml`. Other Normandy combat still raises
   with no Manston skeleton. Stub LLM stays Manston. Flip 0b tests that used
   CAP JSON as the refused type over to intercept.

5. **N1-style compile contracts, not a full golden.** Zip + mission tokens
   (`airdromeId=28`, CAP Orbit, frequencies 124.0 / 40.0), same pattern as
   `test_normandy_freeflight.py`. Channel CAP goldens stay untouched.

6. **Units reuse era YAML.** `UK` / `ThirdReich`, `SpitfireLFMkIX` 124 MHz,
   `Bf-109K-4` 40 MHz. No USA. Strike `theatre_id` stays `TheChannel`.

## Risks / Trade-offs

- [Invent copies Channel 135/25 onto NOP] → Mitigation: schema example is
  180/63; prompts forbid french-coast / Hawkinge / Manston CAP numbers.
- [Channel invent picks Cherbourg place] → Mitigation: `theatre=` filter on
  `channel_place`.
- [Ford_AF vs FordAF] → Mitigation: Spec key `FordAF`; document PyDCS name.
- [Numeric ids 1–14 look like Channel] → Mitigation: theatre-scoped lookup;
  tests assert `Maupertus` is Normandy 4, not Channel Abbeville.
- [CAP over water with Bf-109] → Mitigation: same as Manston Channel CAP;
  ME Instant Action is do-soon, not a merge gate.

## Migration Plan

One PR on `normandy-airfields-places`. Catalog sync picks up new AFs/places
without a schema bump. Rollback = revert. ME Instant Action do-soon after
merge (`out/needs_oar_point_cap.miz`).

## Open Questions

- None blocking. Later slice: Normandy domain + GA place + strike tag.
