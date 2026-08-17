## Context

Recon compile already uses airfield-relative AOI. Channel recon observes inland
of Dunkirk (125° / 76 km, land). Caucasus recon already stations inland of
Kutaisi at 43° / 110 km (land). Syria GA already stations inland of Aleppo at
121° / 200 km (land). CAP/intercept/escort 180/40 is sea — wrong domain for a
Levant land observe. Reuse `aleppo_inland_strike`; do not copy french_coast or
Iskenderun water. Domain already classifies 121/200 land and 180/40 sea.

## Goals / Non-Goals

**Goals:**

- Validate + compile an Incirlik recon with observe-only Ural-375 contacts
  inland of Aleppo.
- Invent/chat may emit Syria `recon` every turn (all six types allowed).
- Channel and Caucasus recon goldens stay bit-identical.

**Non-Goals:**

- Domain rewrite, intercept_spawn, path clamp, sea/harbour recon, new unit ids,
  Instant Action as merge gate.

## Decisions

1. **AOI = 121° / 200 km / 2000 m** from Incirlik — same land station as GA.
   PyDCS Incirlik (16) → Aleppo (27) is 121.13° / 185.00 km. Integer 121/185 is
   near-field reject. Do not copy 125/76, 43/110, or CAP 180/40.

2. **Reuse `aleppo_inland_strike`.** Add `recon` to `mission_types`. Copy strike
   geometry as AOI. Do not invent a second place. Do not put recon on
   `incirlik_iskenderun_cap`.

3. **Observe modern trucks:** `Ural-375`, country **Syria** red, weapons hold,
   no payload. Date 2024-06-06, 09:00, `sunny_clear`. Player Su-25T, Turkey
   blue, Incirlik.

4. **Dedicated `_SYRIA_RECON_NOTES`.** Do not concatenate Channel `_TYPE_NOTES`.
   Schema loads `incirlik_aleppo_recon.yaml`. Stub LLM stays Manston.

5. **Invent allow-table** for Syria becomes all six types (`frozenset(MissionType)`).
   Empty unsupported schema set.

6. **Tests:** validate+compile new example (airdromeId 16, Reconnaissance,
   Ural-375, recon_aoi). Invent: recon allowed. Channel recon unchanged.
   Fail-closed coverage stays on Nevada/Falklands.

## Risks / Trade-offs

- [AOI on water] → 121/200 is already classified land; 180/40 stays sea.
- [Invent copies 125/76 or 180/40] → schema/place/prompts name Aleppo 121/200.

## Migration Plan

Implement on `syria-recon`. Rollback = revert the branch. Channel goldens
must stay green.

## Open Questions

None — Instant Action is do-soon after merge, not a gate.
