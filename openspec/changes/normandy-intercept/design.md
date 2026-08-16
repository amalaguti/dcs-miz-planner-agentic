## Context

Intercept spawn is a theatre-keyed recipe table. Only TheChannel is populated (Hawkinge map x/y + Dover-approach offset). Normandy CAP already stations at 180° / 63 km from NeedsOarPoint (`cherbourg_channel_cap`, domain sea). Ground-attack inland of Maupertus is 180/133 (land). Enemy intercept inflight belongs on the sea station, not on Maupertus or Hawkinge.

## Goals / Non-Goals

**Goals:**

- Validate + compile a Needs Oar Point dawn intercept with Bf-109K-4 on the Cherbourg corridor.
- Invent/chat may emit Normandy `intercept` every turn; escort/recon still refuse.
- Channel Hawkinge goldens stay bit-identical.

**Non-Goals:**

- Escort/recon, path clamp, new unit ids, Instant Action as merge gate.

## Decisions

1. **Spawn = NeedsOarPoint + 180° / 63 km**, measured with PyDCS `point_from_heading`.
   NeedsOarPoint (id 28) = `141296.390625, -84372.234375`. Offset `(-63000, 0)`.
   Enemy = `78296.390625, -84372.234375`. Store these literals (same pattern as Hawkinge). Do not call `airport_list()` at compile time for Channel or Normandy.

2. **Keep Channel field aliases.** Generalize recipe storage to `anchor_*` / `offset_*` with `hawkinge_*` / `dover_offset_*` properties so existing Channel tests stay green.

3. **Reuse `cherbourg_channel_cap`** for intercept cues (add `intercept` to `mission_types`). Do not invent a second place with the same numbers.

4. **Dawn 06:00** like Manston intercept (Channel colour), not 09:00 CAP. Same date/weather/aircraft as other Normandy smokes.

5. **Dedicated `_NORMANDY_INTERCEPT_NOTES`.** Do not concatenate Channel `_TYPE_NOTES` (Hawkinge / Manston radio example). Schema loads `needs_oar_point_dawn_intercept.yaml`. Stub LLM stays Manston.

6. **Tests:** validate+compile new example (airdromeId 28, Bf-109K-4, theatre Normandy). Channel intercept recipe literals unchanged. Invent: intercept allowed; escort/recon still refused.

## Risks / Trade-offs

- [Enemy on water vs over land] → 180/63 is already classified sea on the UK–Cotentin chord.
- [Invent copies Hawkinge] → schema/place/prompts name Cherbourg 180/63.

## Migration Plan

Implement on `normandy-intercept`. Rollback = revert the branch. Channel goldens must stay green.

## Open Questions

None — Instant Action is do-soon after merge.
