## Context

R9: biggest Channel richness gap after narrative is interactive options (F10 + late spawn).
R5 stock IA (Dawn Raid, Ferry SCRAMBLE, Low Level Hell) uses `a_add_radio_item*` → flags →
`a_activate_group` with late-activated groups. PyDCS 0.15.0 exposes `AddRadioItem`,
`AddRadioItemForCoalition`, `ActivateGroup`, `DeactivateGroup`; `FlyingGroup.late_activation`
exists. Our Spec today only has bool `flag_is` / `set_flag` and always-active groups.

## Goals / Non-Goals

**Goals:**

- Spec actions for radio add/remove and activate/deactivate by enemy/target index.
- `late_activation` on enemy and ground-target groups; compiler sets PyDCS flag and
  keeps group ids for activate actions.
- Example + validate/compile tests + ME accept (F10 items visible; groups late).

**Non-Goals:**

- Numeric flags; sound; package indices; narrative pack changes; Lua.

## Decisions

1. **Bool flags for v1 difficulty:** Each radio item sets one named flag to on (`value=1`).
   Rules use existing `flag_is`. Avoids `flag_equals` scope creep; three items → three flags.
2. **`radio_item_add` fields:** `label` (F10 text), `flag` (string), optional `coalition`
   (default: player coalition → `AddRadioItemForCoalition`; omit coalition → all via
   `AddRadioItem`). Optional `remove_after_use` deferred — authors may `radio_item_remove`.
3. **`activate_group` / `deactivate_group`:** Exactly one of `enemy_index` | `target_index`
   (int ≥ 0). Validate range; compile to group id from placement lists.
4. **`late_activation: bool = false`** on `EnemyFlight` and `GroundTarget`. When true,
   placed group gets `late_activation=True` (dormant until ActivateGroup).
5. **Mission-start radio:** Example uses `time_more` ~1s (or small seconds) to add menu
   items — no new “mission start” condition in v1.
6. **Example:** Intercept or CAP with 2–3 late enemy flights and F10 Easy/Med/Hard that
   activate one flight each (document that only one should be chosen in play).

## Risks / Trade-offs

- [Risk] Player selects multiple difficulties → multiple groups active → Mitigation:
  document; optional later remove-item / mutual exclusion via clearer flags.
- [Risk] `unit_dead` on never-activated group → Mitigation: validate/docs: win rules should
  target the activated flight or use separate narrative; example wires dead to activated index.
- [Risk] Coalition radio vs all → Mitigation: default player coalition for SP Channel.

## Migration Plan

- Additive fields/actions. Rollback: ignore new action types / field.

## Open Questions

- None blocking. Sound and numeric flags stay follow-ups.
