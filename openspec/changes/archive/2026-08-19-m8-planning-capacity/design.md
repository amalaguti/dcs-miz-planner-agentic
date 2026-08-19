## Context

Six mission types compile. `player.flight` already exists (`#15b`–`#15e`).
The gap is catalog density and agent assertiveness on Channel/Normandy.

Verified PyDCS (do not invent): `P-51D` radio 124, `{AN-M64}` pylons 4+7;
no Typhoon; artillery `LeFH_18-40-105` / `Wespe124` / `M2A1-105`; statics
`Hangar A` / `Revetment_x4` / `Tent01` / `Belgian gate` / `Shelter`. Extra-home
geometry was measured from the same map points as Manston CAP 135/25 and
strike 125/76.

## Goals / Non-Goals

**Goals:** denser WWII catalog; extra invent homes with honest parking;
agent chooses solo vs section; recon narrative; scenery smoke; inspiration
cards. GermanyCW documented as gated idea only.

**Non-Goals:** new mission families; modern-map depth; compiler rebuild of
`player.flight`; auto-promote install discovery.

## Decisions

1. **USA is dual-era.** Needed for P-51 on Channel/Normandy. Do not copy
   modern USA radio (251) onto WWII. `usaaf` stays voice.

2. **P-51D first, not Typhoon.** `plane_map` has no Typhoon type id.

3. **Per-home recipes.** Extra homes must not copy Manston/NOP stations.
   Tangmere 15 parking → max_flight_size 3.

4. **Recon narrative defers.** `apply_narrative` returns recon unchanged;
   `expand_recon_find_pack` prepends `narrative_push` then the AOI find beat
   so one zone graph remains.

5. **Scenery via `fortification_map`.** `Mission.static_group`; exact keys
   including spaces (`Hangar A`).

6. **Sortie size is prompt/schema.** Do not rebuild the compiler. Escort
   `package[]` stays friendly strikers, not the player section.

## Risks / Trade-offs

- Live invent from Hawkinge can still clone Manston CAP 135/25 when the
  schema example is Manston; notes must keep repeating per-home `cap_*`.
- ME Instant Action is do-soon, not a merge gate.
