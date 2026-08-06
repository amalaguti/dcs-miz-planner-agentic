## Context

Play-time variation already works via hand Specs (`set_flag_random`, radio + late
activation). `#30e` catalogued modes. `#30f` adds a **declarative expand pack** so the
mission designer agent can lock `dynamics` without emitting 40 trigger lines.

Precedent: `narrative.enabled` expands when zones/triggers empty.

## Goals / Non-Goals

**Goals:**

- Spec `dynamics` with modes `fixed` | `live` | `choose` | `hybrid`
- Shared `pools` pointing at existing `enemies[]` / `targets[]` indices
- Deterministic expand → typed triggers only (no LLM Lua)
- Example intercept (or CAP) with live + choose or hybrid
- Catalog `dynamics_mode` honesty updated when Spec-backed

**Non-Goals:**

- Implicit pool partitioning; Mist; Layer A randomize inside this block
- Additive expand onto non-empty hand triggers (v1 hard reject)

## Decisions

1. **Expand pack (narrative-like)** — `dynamics` present + empty triggers → expander
   fills triggers; then clear or leave a `dynamics.expanded` marker — prefer clearing
   enabled-style flag analogous to narrative (store mode in comment/meta if needed).
   *Alt:* leave `dynamics` on Spec after expand — lean clear like narrative for one graph.

2. **Modes**
   - `fixed`: no dice/menu emit; referenced late groups may stay late unless product
     says “activate all” — lean: fixed = no auto activate (author activates or groups
     start live). Document clearly.
   - `live`: `set_flag_random` + `flag_equals` → `activate_group` per pool
   - `choose`: F10 `radio_item_add` → flag → activate
   - `hybrid`: F10 includes Auto (dice) + per-pool menu labels

3. **Pools** — `id`, `roll_value` and/or `menu_label`, `enemy_indices` and/or
   `target_indices`, optional `message`. Indices MUST exist; those groups MUST be
   `late_activation: true` (or expander sets it).

4. **`exclusive: true` default** — one pool path; avoid double-spawn footgun.

5. **Conflict** — non-empty `triggers` or `zones` with `dynamics` → error (match
   narrative strictness for v1; zones may be allowed if only used by expand — lean
   reject both non-empty like narrative).

6. **Scope v1 mission types** — intercept, cap, escort first; ground_attack target
   pools if cheap.

7. **Agent** — schema notes + prompt: offer modes from catalog; emit `dynamics` when
   user locks; do not silently force hybrid on one-shot without stating assumption.

## Risks / Trade-offs

- [Risk] Hybrid exclusive ME pattern subtle → Mitigation: follow proven radio + flag
  example; one golden + ME smoke acceptance
- [Risk] Overlap with narrative → Mitigation: cannot enable both expand packs if both
  need empty triggers — validate XOR
- [Risk] Scope creep to GA targets → Mitigation: enemies-first tasks; targets optional

## Migration Plan

- Additive Spec field; old hand recipes remain valid
- Flip `dynamics_mode` cards toward Spec-backed when expand ships
- Rollback: remove expander + field

## Open Questions

- Exact hybrid Auto flag/radio wiring (apply-time against radio example)
- Whether `fixed` activates all late pools or leaves them dormant
