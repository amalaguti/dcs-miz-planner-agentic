## Context

`narrative.enabled` today only supports CAP. Intercept is the next combat type with
enemies and a clear win condition (`unit_dead`). Escort/ground-attack deferred.

## Goals / Non-Goals

**Goals:**

- Intercept pack: scramble/push message + bandits-down → message + win.
- Multi-pack dispatch in `narrative.py` (CAP behaviour unchanged).
- Example Spec + tests + ME Triggers acceptance.

**Non-Goals:**

- Escort/GA packs; Lua; new trigger types; Spec-level intercept corridor geometry;
  zone-based bogey callouts in v1 (no Spec-relative intercept station yet — avoid
  inventing map coords).

## Decisions

1. **Dispatch by `mission_type`:** `cap` → existing pack; `intercept` → new pack;
   others still error with clear code.
2. **Intercept pack content (v1):**
   - Once `time_more` (~120s) → scramble / vector message (voice templates).
   - Once `unit_dead` `enemy_index: 0` → splash + `mission_end` win.
   - No zone in v1 (intercept enemy placement is compiler Manston corridor constants,
     not Spec-relative).
3. **Same guards as CAP:** refuse non-empty zones/triggers; require non-empty `enemies`.
4. **Example:** `manston_dawn_intercept_narrative.yaml` (leave plain intercept alone).
5. **Refactor:** extract `_apply_cap_pack` / `_apply_intercept_pack` from `apply_narrative`.

## Risks / Trade-offs

- [Risk] Intercept feels thinner than CAP (no on-station) → Mitigation: accept for v1;
  add Spec-relative intercept geometry + zone callout in a later change if wanted.
- [Risk] Multi-flight intercept win on first group only → Mitigation: document; same as CAP.

## Migration Plan

- Additive; CAP Specs unchanged. Rollback: remove intercept branch + example.

## Open Questions

- None blocking. Escort pack after intercept accept.
