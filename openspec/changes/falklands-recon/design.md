## Context

Recon compile already uses airfield-relative AOI. Channel recon observes inland
of Dunkirk (125° / 76 km). Caucasus 43° / 110 km. Syria 121° / 200 km. Nevada
303° / 85 km. Falklands GA already stations inland short of Goose Green at
269° / 21 km (land). CAP/intercept/escort 150/40 is a different sea station —
wrong for an East Falkland land observe. Reuse `east_falkland_inland_strike`;
do not copy french_coast, Creech 303/85, Aleppo 121/200, or South Atlantic CAP.
Domain already classifies 269/21 land and 150/40 sea. Dual-offer already
returns Ural-375 on `list_strike_targets(theatre="Falklands")`.

## Goals / Non-Goals

**Goals:**

- Validate + compile a Mount Pleasant recon with observe-only Ural-375 contacts
  inland short of Goose Green (radius_m 3000, mark true, weapons hold, no
  payload).
- Invent/chat may emit Falklands `recon` every turn (all six types allowed).
- Channel, Caucasus, Syria, and Nevada recon goldens stay bit-identical.

**Non-Goals:**

- Domain rewrite, intercept_spawn, path clamp, sea/harbour recon, new unit ids,
  catalog dual-offer changes, Instant Action as merge gate, unbound-map binds.

## Decisions

1. **AOI = 269° / 21 km / 2000 m** from Mount Pleasant — same land station as
   GA. Live PyDCS: MountPleasant (2) → Goose Green (24) is 268.80° / 36.01 km.
   Integer 269/36 is near-field reject (~0.13 km from GG). 269/51 is Falkland
   Sound sea. 269/21 is ~15.02 km **SHORT** of Goose Green. Station
   **x=72951.81977681704 y=26171.946448715786**. CAP 150/40
   **x=38677.30416062245 y=67168.748047** MUST NOT equal the recon AOI.
   Document in the example YAML comment. Do not copy 125/76, 43/110, 121/200,
   303/85, or CAP 150/40.

2. **Reuse `east_falkland_inland_strike`.** Add `recon` to `mission_types`.
   Copy strike geometry as AOI. Do not invent a second place. Do not put recon
   on `mount_pleasant_south_atlantic_cap`. Extend `mount_pleasant_home` with
   `recon`. Family stays `channel_place`.

3. **Observe modern trucks:** `Ural-375` (count 3), country **Argentina** red,
   weapons hold, no payload. Date 2024-06-06, 09:00, `sunny_clear`. Player
   Su-25T, UK blue, MountPleasant. Not UK-on-red. Not country Russia.
   `GroundTarget.country` MUST be set (default is ThirdReich). Do not add GA’s
   extra GAZ-66 row.

4. **Dedicated `_FALKLANDS_RECON_NOTES`.** Do not concatenate Channel
   `_TYPE_NOTES` / `_COMMON_NOTES`. Schema loads
   `mount_pleasant_east_falkland_recon.yaml`. Stub LLM stays Manston. Empty
   `_FALKLANDS_UNSUPPORTED_COMBAT`. `_THEATRE_ALLOWED_TYPES["Falklands"]`
   becomes `frozenset(MissionType)`. Lightly edit FF/CAP/intercept/escort/GA
   notes so they no longer say refuse recon. Those example **files** stay
   unchanged.

5. **Repair:** `motion_domain_mismatch` / `strike_domain_mismatch` on Falklands
   MUST nudge `east_falkland_inland_strike` 269/21 for land strike **or recon**,
   not CAP 150/40. Fail-closed coverage stays unbound theatres (`Kola`).

6. **Tests:** validate+compile new example (airdromeId 2, Reconnaissance,
   Ural-375, recon_aoi, UK, Argentina; MUST NOT contain CAP station coords or
   Hawkinge `30989.935547`). Invent: recon allowed. Channel recon unchanged.

## Risks / Trade-offs

- [AOI on South Atlantic CAP] → separate place; compile must not contain CAP
  coords.
- [Invent copies 125/76, 303/85, or 150/40] → schema/place/prompts name East
  Falkland 269/21.
- [Omitted country defaults to ThirdReich] → example MUST set country Argentina.
- [Notes concat Manston] → dedicated `_FALKLANDS_RECON_NOTES` only.
- [Payload left on player] → omit `player.payload`.

## Migration Plan

Implement on `falklands-recon`. Rollback = revert the branch. Channel goldens
must stay green. After merge, bound-map invent is complete; next promote is
not a new theatre (unbound stay discovered-only).

## Open Questions

None — Instant Action is do-soon after merge, not a gate.
