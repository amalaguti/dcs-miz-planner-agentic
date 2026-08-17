## Context

Caucasus Stage A+B are on master: eight curated airfields, Russia modern, Mozdok
FF, dual-era Spitfire allowed. Invent still free_flight only at Batumi.
`host_theatre_mission_refuse_nudge` refuses every combat type every turn.
Domain, intercept spawn, and path clamp fail closed or skip off
TheChannel/Normandy. CAP on a valid Caucasus airfield already validates and
compiles (airfield-relative `_place_cap_enemies`); invent still refuses it.

Live PyDCS from Batumi (id 22, x=-355810.6875, y=617386.1875): inland AFs lie
22–83° (Kutaisi 43.14°/97.20 km, Tbilisi 81.82°/282.11 km); Sochi along-coast
is 320.96°. Due west 270° / 40 km is Black Sea
(station y=577386.188). Not Manston 135/25, not Cherbourg 180/63.

## Goals / Non-Goals

**Goals:**

- Add two `channel_place` rows (`meta.theatre: Caucasus`).
- Ship one CAP example; lift invent/schema refuse for **CAP only**.
- Enemies: Russia + Su-25T (reuse modern YAML; never ThirdReich/Bf-109).

**Non-Goals:**

- GA / intercept / escort / recon on Caucasus.
- Domain classifier, intercept spawn recipe, path clamp, strike dual-tag.
- Extra AFs, extra unit YAML, Spitfire CAP smoke, paid FC3 jets.
- Full golden dump of the new CAP `.miz`.

## Decisions

1. **CAP-only combat this slice.** Station 270° / 40 km / 4000 m from Batumi
   (west, Black Sea). Leave domain fail-closed so GA/recon cannot silently use
   the UK–FR or Cotentin chord. Leave intercept fail-closed (no Hawkinge-style
   offset). Alternative (ship GA inland of Kutaisi) deferred until a Caucasus
   domain recipe and modern strike shelf exist.

2. **Keep family `channel_place`.** New rows `batumi_home` and
   `batumi_black_sea_cap` with `meta.theatre: Caucasus`. Do not rename to
   `theatre_place`. Existing `list_mission_options(*, theatre=)` filter already
   scopes places. Alternative (prompt-only filter) rejected — Channel invent
   could copy Batumi 270/40 onto Manston.

3. **Smoke identity stays Frogfoot.** Player Georgia + Su-25T blue; enemies
   Russia + Su-25T red at 251.0 MHz both sides. Spec MUST set
   `enemies[].country: Russia` because `EnemyFlight.country` defaults to
   `ThirdReich`. Spitfire is dual-era and may fly Caucasus, but invent home and
   this smoke stay Su-25T. No new identity YAML.

4. **Lift nudge for CAP only.** Add Caucasus to `_THEATRE_ALLOWED_TYPES` as
   `{FREE_FLIGHT, CAP}`. Intercept / GA / escort / recon stay every-turn refuse.
   Schema `theatre=Caucasus` + `cap` loads `examples/batumi_black_sea_cap.yaml`.
   Other Caucasus combat still raises with no Manston skeleton. Stub LLM stays
   Manston. Flip tests that used CAP JSON as the refused type over to intercept.

5. **N1-style compile contracts, not a full golden.** Zip + mission tokens
   (`airdromeId=22`, CAP Orbit, `Su-25T`, frequencies 251.0, `Russia`). Channel
   CAP goldens stay untouched. Do not assert `"Su-25T" not in mission` via
   whole-file substring (`requiredModules` lists ED module names).

6. **Dedicated Caucasus CAP schema notes.** Do not concatenate `_COMMON_NOTES`
   / `_TYPE_NOTES` (those cite Manston YAML and `channel_place` as templates).

## Risks / Trade-offs

- [Invent copies Manston 135/25 or Cherbourg 180/63 onto Batumi] → Mitigation:
  schema example is 270/40; prompts forbid french-coast / Hawkinge / NeedsOarPoint
  numbers.
- [Channel invent picks Batumi place] → Mitigation: `theatre=` filter on
  `channel_place`.
- [Default enemy country ThirdReich] → Mitigation: example YAML sets Russia;
  tests assert country token.
- [Russia-on-blue] → Mitigation: enemies coalition red only.
- [CAP over water with Su-25T] → Mitigation: same pattern as Channel/Normandy
  CAP; ME Instant Action is do-soon, not a merge gate.

## Migration Plan

One PR on `caucasus-places`. Catalog sync picks up new places without a schema
bump. Rollback = revert. ME Instant Action do-soon after merge
(`out/batumi_black_sea_cap.miz`).

## Open Questions

- None blocking. Later slice: Caucasus domain + GA place + modern strike units.
