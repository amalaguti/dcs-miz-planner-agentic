## Context

`agent-capability-catalog` added assertive creative recipes. User memory already has
`generation_history.detail_json`, `satisfaction_feedback` (score/tags), and prefs — but
hosts rarely put creative ids in `detail`, and prompts do not bias from past scores.

## Goals / Non-Goals

**Goals:**

- Stable `detail` schema for creative choices at record time.
- Prompt/planning bias from recent scored generations (+ optional prefs).
- Hermetic tests; no Spec/compiler changes.

**Non-Goals:**

- Auto-curating packaged cards; ML; Doc PDF ingestion; multi-user.

## Decisions

1. **Reuse `detail_json`, don’t add a table.** Convention:
   ```json
   {
     "creative": {
       "inspirations": ["low_level_channel_hop"],
       "behaviours": ["altitude_speed_gates"],
       "sources": ["catalog"]
     }
   }
   ```
   `sources` values: `catalog` | `campaign_doc` | `research` | `user_request`.
   Hosts (planner/chat) populate when they know choices; agent MAY pass via
   `record_generation.detail`.

2. **Feedback via existing tags + score.** Prefer tags like `liked:altitude_speed_gates`
   / `avoid:narrative_pack`, or free note; score on the generation is primary signal.
   No mandatory new columns.

3. **Bias helper, not opaque magic.** Small pure function e.g.
   `creative_bias_from_history(generations, feedback, mission_type) -> {prefer[], avoid[]}`
   used to append a short prompt fragment or tool note. Soft weights from scores; empty
   history → empty bias (catalog assertive path unchanged).

4. **Optional prefs (v1 if cheap):** `preferred_behaviours` / `avoid_behaviours` (lists of
   behaviour ids) and/or `creativity_level` (`quiet`|`assertive`|`max`). Prefs override
   or strengthen history bias. If wiring prefs slows apply, ship history-only first.

5. **Prompt rule:** On vague immersion asks, after `list_mission_options`, consult
   `list_generation_history` (and prefs); prefer `prefer[]` behaviours; soft-avoid
   `avoid[]`; still max 1–2 behaviours; never Lua; respect hand triggers.

6. **No Spec infer required in v1.** Explicit detail is the SoT for learning. Optional
   follow-up: infer from Spec triggers for older rows.

## Risks / Trade-offs

- [Risk] Agent forgets to pass detail → Mitigation: host fills from tool-call trace or
  known defaults when recording success; tests cover host path.
- [Risk] Sparse feedback → Mitigation: bias is soft; catalog still works offline.
- [Risk] Overfitting to one liked behaviour → Mitigation: still diversify; prefer not
  force; creativity_level quiet reduces inventing.

## Migration Plan

- Additive detail convention + prompt/helper. Rollback: ignore `creative` key.

## Open Questions

- Whether chat `/feedback` should prompt for behaviour tags (nice-to-have).
- Whether to bump `USER_SCHEMA_VERSION` only if prefs keys need documented defaults
  (likely no bump — prefs are schemaless JSON).
