## Context

After `#26`, Specs can play curated sounds and use numeric/timed flags. Strike and raid
objectives still only detect **full** group death via `unit_dead` / `target_dead`
(`GroupDead`). Stock Channel IA often fires when remaining group life drops below a
percent. PyDCS 0.15.0 already exposes `GroupLifeLess(group, percent)` →
`c_group_life_less`. Spec vocabulary and validation are the gap.

## Goals / Non-Goals

**Goals:**

- Spec condition `group_life_less` referencing one enemy or target group + percent threshold.
- Validate indices and percent; emit `GroupLifeLess` for the placed group id.
- Example (prefer ground-attack) + tests; ME shows the life-less rule.

**Non-Goals:**

- Altitude/speed gates, smoke/markers, `unit_life_less`, player-group life.
- Narrative pack rewiring; Lua / Mist / MOOSE; changing `unit_dead` / `target_dead`.

## Decisions

1. **Index pattern matches activate_group:** Condition fields are exactly one of
   `enemy_index` or `target_index` (0-based) plus `percent` (integer). Same XOR validator
   as activate/deactivate. Alternative rejected: free DCS group ids in Spec (LLM unsafe /
   non-portable).

2. **Percent bounds:** Require `1 <= percent <= 100` (ME percentage of remaining life).
   Default is not required in Spec — authors must set an explicit threshold. PyDCS default
   of 10 is irrelevant when Spec always supplies the value.

3. **Semantics vs GroupDead:** `group_life_less` is additive beside `unit_dead` /
   `target_dead`. Authors choose partial-damage beats vs full destruction. Do not redefine
   dead conditions.

4. **Emit:** `condition_mod.GroupLifeLess(group_id, percent)` using the same
   `enemy_group_ids` / `target_group_ids` maps as other group-referencing conditions.

5. **Example:** Ground-attack (or soft-target) Spec with `group_life_less` on
   `target_index: 0` → `message` (and optionally `set_flag` / `mission_end`) so ME
   acceptance is obvious without needing to destroy every unit.

6. **Narrative packs unchanged:** Vocabulary allows the new type; packs do not auto-emit
   life-less rules in this change.

## Risks / Trade-offs

- [Risk] Authors confuse life-% with unit count → Mitigation: docs/notes say remaining
  group life percent (ME Group Life Less), not “N units left.”
- [Risk] Very high percent (e.g. 99) fires on light damage → Mitigation: example uses a
  clear mid threshold (e.g. 50); validation does not second-guess author intent.
- [Risk] Late-activated groups not yet spawned → Mitigation: same as activate/dead —
  condition only meaningful after the group exists / is active; document in notes.

## Migration Plan

- Additive Spec type. Rollback: ignore `group_life_less` conditions.

## Open Questions

- None blocking. Follow-ups: altitude/speed gates, smoke/markers, optional narrative
  “damaged enough” beats.
