## Context

`#20`–`#21` give typed `zones`/`triggers` and native ME emit. Combat examples
(`manston_cap.yaml`, etc.) still leave `triggers: []`. The free-flight trigger sample
proves time→message in Instant Action. `#23` layers **opt-in narrative packs** that
expand into that same vocabulary for CAP immersion, in squadron-commander voice.

## Goals / Non-Goals

**Goals:**

- Opt-in CAP narrative pack → typed zones/triggers (on-station / bandit-down / win).
- Message copy follows RAF / USAAF / neutral voice packs (same voices as briefing).
- Example Spec + validate/compile + in-game ME Triggers / Instant Action acceptance.
- Agent schema notes know narrative is opt-in and expands to existing trigger types.

**Non-Goals:**

- `#22` Lua snippets; new trigger types; default-on for all combat Specs; other mission
  types' packs; VO audio; changing PyDCS emit mapping.

## Decisions

1. **Opt-in Spec field `narrative.enabled` (bool, default false).**
   When true and `mission_type` is `cap`, apply pack `cap_v1`. Other mission types with
   `enabled: true` fail validation in v1 (clear error).
   *Alt considered:* always-on for CAP — rejected (surprises authors / fixtures).
   *Alt:* free-form event list — deferred; packs keep content curated.

2. **Expand before validate/compile, not inside PyDCS emit.**
   Pure function `apply_narrative(spec, voice=...) -> MissionSpec` fills `zones`/`triggers`
   (and leaves other fields alone). Compiler keeps emitting whatever Spec triggers exist.
   *Alt:* expand only in compiler — rejected (validate would miss the graph).

3. **Refuse expand when `zones` or `triggers` already non-empty.**
   Avoid merge conflicts / duplicate rules. Authors who hand-write triggers leave
   `narrative.enabled: false`.
   *Alt:* merge by name — more complex; skip for v1.

4. **CAP pack content (v1):**
   - Zone `cap_station` from Spec `cap` bearing/distance (radius ~5000 m).
   - Once: `time_more` (~120s) → push / climb message.
   - Once: `coalition_in_zone` (player coalition, `cap_station`) → on-station / weapons-free.
   - Once: `unit_dead` `enemy_index: 0` → splash message + `mission_end` win
     (requires ≥1 enemy; validate pack preconditions).
   Copy from voice-keyed templates (human-authored strings).

5. **Example:** new `examples/manston_cap_narrative.yaml` (leave `manston_cap.yaml`
   unchanged for existing fixtures). CLI/agent may expand on compile when field set.

6. **No `#22`:** if a desired beat needs Lua, park it; CAP v1 fits native vocab.

## Risks / Trade-offs

- [Risk] `unit_dead` = whole enemy *group* dead → Mitigation: CAP example keeps one enemy
  flight; document that multi-flight “all clear” needs flags/follow-on.
- [Risk] On-station fires only if player enters zone → Mitigation: keep time-based push so
  something always shows even if player never reaches station.
- [Risk] Voice strings diverge from briefing tone → Mitigation: reuse `resolve_voice` +
  shared persona wording guidelines; keep templates short.
- [Risk] Agents set `narrative.enabled` with hand triggers → Mitigation: validation error.

## Migration Plan

- Additive Spec field (default off). Existing Specs unchanged.
- Rollback: disable field / delete example; expander unused.

## Open Questions

- None blocking: intercept/escort packs after CAP acceptance.
