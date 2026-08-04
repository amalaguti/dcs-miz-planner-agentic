## Context

Narrative dispatch supports CAP, intercept, and escort. Ground-attack Specs include
nested `strike` (airfield-relative) and `targets`, but forbids air `enemies` — so the
existing `unit_dead.enemy_index` win path cannot apply. Target groups are already placed
by the compiler; they need Spec-addressable GroupDead conditions.

## Goals / Non-Goals

**Goals:**

- GA pack: push message; strike-area zone + ingress callout; first-target dead →
  message + win.
- New v1 condition `target_dead` (`target_index` into `targets[]`).
- Compiler returns/collects target group ids and maps `target_dead` → GroupDead.
- Same guards: empty zones/triggers; clear errors for unsupported types / missing fields.
- Example + tests + ME acceptance.

**Non-Goals:**

- Lua; AND-all-targets win; per-unit (not group) dead; free_flight narrative;
  changing practice-strike rules.

## Decisions

1. **Require `strike` and non-empty `targets`** for GA narrative (win needs `target_dead`).
2. **Add `target_dead`** rather than overloading `unit_dead.enemy_index` (GA has no enemies;
   keeps air vs ground refs distinct).
3. **Zone `strike_area`** from `strike.bearing_deg` / `distance_km` (radius ~5000 m).
4. **Beats:** `narrative_push` (time ~120s); `narrative_ingress` (coalition in zone);
   `narrative_targets_down` (`target_dead` 0 → message + win).
5. **Compiler:** `_apply_ground_attack` returns `list[int]` target group ids (order =
   `targets[]`); `apply_zones_and_triggers` accepts them for `target_dead` mapping.
6. **Refactor:** add `_apply_ground_attack_pack`; extend unsupported-type message.

## Risks / Trade-offs

- [Risk] Win on first target *group* dead (count>1 units) — GroupDead waits for whole group
  → Mitigation: document; matches air `unit_dead` semantics.
- [Risk] Practice strikes with same-coalition targets still win on destroy → Mitigation:
  allowed; copy stays combat-neutral where needed.
- [Risk] Broader trigger vocabulary surface → Mitigation: validate range; golden + unit tests.

## Migration Plan

- Additive. Rollback: remove GA branch, `target_dead` model/emit, and example.

## Open Questions

- None blocking.
