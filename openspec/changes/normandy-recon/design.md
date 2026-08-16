## Context

Recon compile already uses airfield-relative AOI. Channel recon observes inland of Dunkirk (125° / 76 km, land). Normandy GA already stations inland of Maupertus at 180° / 133 km (land). CAP/intercept/escort 180/63 is sea — wrong domain for a Cotentin land observe. Reuse `maupertus_inland_strike`; do not copy french_coast.

## Goals / Non-Goals

**Goals:**

- Validate + compile a Needs Oar Point recon with observe-only Blitz contacts inland of Maupertus.
- Invent/chat may emit Normandy `recon` every turn (all six types allowed).
- Channel recon goldens stay bit-identical.

**Non-Goals:**

- Path clamp, sea/harbour recon, new unit ids, Instant Action as merge gate.

## Decisions

1. **AOI = 180° / 133 km / 2000 m** from NeedsOarPoint — same land station as GA. Channel analogue is inland observe, not Cherbourg-channel water. Do not copy 125/76.

2. **Reuse `maupertus_inland_strike`.** Add `recon` to `mission_types`. Copy strike geometry as AOI. Do not invent a second place.

3. **Same observe ids as Channel recon:** `Blitz_36-6700A`, `ThirdReich` red, weapons hold, no payload. Date 1944-06-06, 09:00, `sunny_clear`.

4. **Dedicated `_NORMANDY_RECON_NOTES`.** Do not concatenate Channel `_TYPE_NOTES` (french_coast / U-boat / 125/76). Schema loads `needs_oar_point_recon.yaml`. Stub LLM stays Manston.

5. **Invent allow-table** for Normandy becomes all six types (`frozenset(MissionType)`). Empty unsupported schema set.

6. **Tests:** validate+compile new example (airdromeId 28, Reconnaissance, Blitz, recon_aoi). Invent: recon allowed. Channel recon unchanged.

## Risks / Trade-offs

- [AOI on water] → 180/133 is already classified land; 180/63 stays sea.
- [Invent copies 125/76] → schema/place/prompts name Maupertus 180/133.

## Migration Plan

Implement on `normandy-recon`. Rollback = revert the branch. Channel goldens must stay green.

## Open Questions

- None.
