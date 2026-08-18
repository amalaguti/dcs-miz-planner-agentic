## Context

Recon compile already uses airfield-relative AOI. Channel recon observes inland
of Dunkirk (125° / 76 km). Caucasus 43° / 110 km. Syria 121° / 200 km. Nevada GA
already stations inland of Creech at 303° / 85 km (land). CAP/intercept/escort
350/40 is a different land station — wrong for a Creech-range observe. Reuse
`creech_range_strike`; do not copy french_coast, Aleppo 121/200, or north-range
CAP. Domain already classifies 303/85 land and 350/40 land. Dual-offer already
returns Ural-375 on `list_strike_targets(theatre="Nevada")`.

## Goals / Non-Goals

**Goals:**

- Validate + compile a Nellis recon with observe-only Ural-375 contacts inland
  past Creech (radius_m 3000, mark true, weapons hold, no payload).
- Invent/chat may emit Nevada `recon` every turn (all six types allowed).
- Channel, Caucasus, and Syria recon goldens stay bit-identical.

**Non-Goals:**

- Domain rewrite, intercept_spawn, path clamp, sea/harbour recon, new unit ids,
  catalog dual-offer changes, Instant Action as merge gate.

## Decisions

1. **AOI = 303° / 85 km / 2000 m** from Nellis — same land station as GA.
   PyDCS Nellis (4) → Creech (1) is 302.86° / 69.47 km. Integer 303/70 is
   near-field reject (~0.56 km from Creech). 303/85 is ~15.53 km past Creech.
   Station x=-351901.05702 y=-88520.23509. Document in the example YAML comment.
   Do not copy 125/76, 43/110, 121/200, or CAP 350/40.

2. **Reuse `creech_range_strike`.** Add `recon` to `mission_types`. Copy strike
   geometry as AOI. Do not invent a second place. Do not put recon on
   `nellis_north_range_cap`. Extend `nellis_home` with `recon`. Family stays
   `channel_place`.

3. **Observe modern trucks:** `Ural-375` (count 3), country **Russia** red,
   weapons hold, no payload. Date 2024-06-06, 09:00, `sunny_clear`. Player
   Su-25T, USA blue, Nellis. Not USA-on-red. Not country Syria.
   `GroundTarget.country` MUST be set (default is ThirdReich).

4. **Dedicated `_NEVADA_RECON_NOTES`.** Do not concatenate Channel `_TYPE_NOTES`
   / `_COMMON_NOTES`. Schema loads `nellis_creech_recon.yaml`. Stub LLM stays
   Manston. Empty `_NEVADA_UNSUPPORTED_COMBAT`. `_THEATRE_ALLOWED_TYPES["Nevada"]`
   becomes `frozenset(MissionType)`. Lightly edit FF/CAP/intercept/escort/GA
   notes so they no longer say refuse recon. Those example **files** stay
   unchanged.

5. **Repair:** `motion_domain_mismatch` / `strike_domain_mismatch` on Nevada
   MUST nudge `creech_range_strike` 303/85 for land strike **or recon**, not
   CAP 350/40. Fail-closed coverage stays Falklands.

6. **Tests:** validate+compile new example (airdromeId 4, Reconnaissance,
   Ural-375, recon_aoi, USA, Russia; MUST NOT contain CAP station coords).
   Invent: recon allowed. Channel recon unchanged.

## Risks / Trade-offs

- [AOI on north-range CAP] → separate place; compile must not contain CAP coords.
- [Invent copies 125/76, 121/200, or 350/40] → schema/place/prompts name Creech 303/85.
- [Omitted country defaults to ThirdReich] → example MUST set country Russia.
- [Notes concat Manston] → dedicated `_NEVADA_RECON_NOTES` only.
- [Payload left on player] → omit `player.payload`.

## Migration Plan

Implement on `nevada-recon`. Rollback = revert the branch. Channel goldens
must stay green.

## Open Questions

None — Instant Action is do-soon after merge, not a gate.
