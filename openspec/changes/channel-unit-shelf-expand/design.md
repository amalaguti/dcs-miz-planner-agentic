## Context

Follow [`docs/THEATRE_TARGET_PROMOTE.md`](../../../docs/THEATRE_TARGET_PROMOTE.md)
section B. PyDCS ids verified against `vehicle_map` / `ship_map` before YAML.

## Goals / Non-Goals

**Goals:** Curated soft + AAA + sea harbour/coastal expand; wire class shelves,
motion profiles, AAA AI class membership; example + tests.

**Non-goals:** Armor/troops/radar classes; ME dump; host invent changes beyond
shelf size.

## Decisions

1. **Batch scope** — Soft (Kettenkrad, Horch, Willys), AAA (flak30/37/38,
   searchlight, KDO, Bofors), sea (second dry cargo, HarborTug, Higgins). No
   new strike_target_class rows this change.

2. **AAA AI membership** — Extend `_AAA_UNIT_IDS` in `target_ai.py` to all
   `aaa_guns` shelf ids (including searchlight / KDO / Bofors) so
   `aaa_alert` / interception rules apply.

3. **Motion** — Soft → soft_vehicle profile; HarborTug / Dry-cargo-2 →
   sea_cargo; Higgins_boat → sea_e_boat (fast small craft) or default_sea —
   use sea_e_boat for Higgins (landing craft still relatively fast).

4. **Examples** — One GA inland AAA battery Spec with new flak + searchlight;
   one harbour GA with HarborTug + Dry-cargo ship-2 (static + harbour_static).
   Reuse existing convoy/U-boat examples unchanged.

5. **Accept** — Hermetic validate/compile + catalog list; ME do-soon.

## Risks / Trade-offs

- [Era stretch (Bofors/Willys/Higgins Allied)] → Labels note Allied/practice or
  harbour context; same as Bedford.
- [Searchlight as “AAA”] → Emplaced static with aaa_alert is acceptable; cue
  “searchlight”.

## Migration Plan

- Additive YAML; catalog sync; no schema version bump required.

## Open Questions

- None — armor/halftrack class deferred.
