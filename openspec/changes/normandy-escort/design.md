## Context

Escort compile already uses the player airfield (`airport.position.point_from_heading`). No intercept-spawn recipe table is required. Channel escort is a mid-Channel package transit (120° / 55 km from Manston), not an inland strike. Normandy CAP/intercept already station at 180° / 63 km sea (`cherbourg_channel_cap`). Reusing that station keeps geometry measured and avoids copying Manston 120/55.

## Goals / Non-Goals

**Goals:**

- Validate + compile a Needs Oar Point escort with Mosquito package + Bf-109 bounce on the Cherbourg corridor.
- Invent/chat may emit Normandy `escort` every turn; recon still refuses.
- Channel escort goldens stay bit-identical.

**Non-Goals:**

- Recon, path clamp, new unit ids, Instant Action as merge gate.

## Decisions

1. **Package destination = 180° / 63 km / 4000 m** from NeedsOarPoint — same sea station as CAP/intercept. Channel analogue is over-water transit, not Maupertus inland 180/133. Do not copy 120/55.

2. **Reuse `cherbourg_channel_cap`.** Add `escort` to `mission_types`. Do not invent a second place with the same numbers.

3. **Same aircraft ids as Channel escort:** `SpitfireLFMkIX`, `MosquitoFBMkVI` (124.0), `Bf-109K-4` (40.0), countries `UK` / `ThirdReich`. Date 1944-06-06, 09:00, `sunny_clear`.

4. **Dedicated `_NORMANDY_ESCORT_NOTES`.** Do not concatenate Channel `_TYPE_NOTES` (Manston 120/55). Schema loads `needs_oar_point_escort.yaml`. Stub LLM stays Manston.

5. **Tests:** validate+compile new example (airdromeId 28, MosquitoFBMkVI, Escort task, theatre Normandy). Invent: escort allowed; recon still refused. Channel escort example unchanged.

## Risks / Trade-offs

- [Package over land vs sea] → 180/63 is already classified sea on the UK–Cotentin chord.
- [Invent copies 120/55] → schema/place/prompts name Cherbourg 180/63.

## Migration Plan

Implement on `normandy-escort`. Rollback = revert the branch. Channel goldens must stay green.

## Open Questions

- None.
