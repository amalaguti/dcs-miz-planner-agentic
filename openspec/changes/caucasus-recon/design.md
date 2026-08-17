## Context

Recon compile already uses airfield-relative AOI. Channel recon observes inland of Dunkirk (125° / 76 km, land). Normandy recon already stations inland of Maupertus at 180° / 133 km (land). Caucasus GA already stations inland of Kutaisi at 43° / 110 km (land). CAP/intercept/escort 270/40 is sea — wrong domain for a Colchis land observe. Reuse `kutaisi_inland_strike`; do not copy french_coast or Batumi Black Sea water.

## Goals / Non-Goals

**Goals:**

- Validate + compile a Batumi recon with observe-only Ural-375 contacts inland of Kutaisi.
- Invent/chat may emit Caucasus `recon` every turn (all six types allowed).
- Channel and Normandy recon goldens stay bit-identical.

**Non-Goals:**

- Path clamp, sea/harbour recon, new unit ids, Instant Action as merge gate.

## Decisions

1. **AOI = 43° / 110 km / 2000 m** from Batumi — same land station as GA. Channel analogue is inland observe, not Black Sea water. Do not copy 125/76 or CAP 270/40.

2. **Reuse `kutaisi_inland_strike`.** Add `recon` to `mission_types`. Copy strike geometry as AOI. Do not invent a second place. Do not put recon on `batumi_black_sea_cap`.

3. **Observe modern trucks:** `Ural-375`, `Russia` red, weapons hold, no payload. Date 2024-06-06, 09:00, `sunny_clear`. Player Su-25T, Georgia blue, Batumi.

4. **Dedicated `_CAUCASUS_RECON_NOTES`.** Do not concatenate Channel `_TYPE_NOTES` (french_coast / U-boat / 125/76). Schema loads `batumi_kutaisi_recon.yaml`. Stub LLM stays Manston.

5. **Invent allow-table** for Caucasus becomes all six types (`frozenset(MissionType)`). Empty unsupported schema set.

6. **Tests:** validate+compile new example (airdromeId 22, Reconnaissance, Ural-375, recon_aoi). Invent: recon allowed. Channel recon unchanged. Fail-closed coverage stays on Syria combat.

## Risks / Trade-offs

- [AOI on water] → 43/110 is already classified land; 270/40 stays sea.
- [Invent copies 125/76 or 270/40] → schema/place/prompts name Kutaisi 43/110.

## Migration Plan

Implement on `caucasus-recon`. Rollback = revert the branch. Channel goldens must stay green.

## Open Questions

- None.
