## Context

Channel invent can already:

- `list_strike_targets` (`#8c`) — exact unit ids from SQLite
- `list_mission_options` — `strike_target_class`, `ground_ai_preset`,
  `channel_place`, motion-related notes
- Compile `targets[].motion` + `ai_preset` (`#15g` / `#15h`)

Some class rows already have `preferred_motion`; presets have examples. Invent
still lacks a clear **cue → (class, unit, motion, preset)** contract.

## Goals / Non-Goals

**Goals:**

- Document invent decision table in planning_options meta + prompts/schema.
- Prefer tool-returned ids/presets only; no free-form Opt* strings.
- Hermetic tests that pin meta + prompt/schema language (and light Spec-shape
  checks where cheap).
- Capture a BACKLOG promote checklist for future theatres / target shelves.

**Non-Goals:** New compile fields; expanding unit YAML; multi-map registries;
hard-coded unit lists in prompts that bypass `list_strike_targets`.

## Decisions

1. **Meta-first heuristics** — Add/align YAML meta rather than a new Python
   decision engine:
   - `strike_target_class`: `preferred_motion`, `preferred_ai_preset`,
     optional `cues` (short keyword list for human/LLM).
   - `ground_ai_preset`: keep `domain` / `class` / `example`; add
     `preferred_motion` where missing.
   - `channel_place`: optional `related_classes`, `preferred_ai_preset` when
     place strongly implies posture (e.g. mid-Channel → sea + patrol +
     `ship_under_way`).
   Rationale: agent already reads options via tools; enriching cards beats a
   second API for v1.

2. **Call order in prompts** — For GA/recon target invent:
   1. `list_mission_options` (class / place / preset shelves)
   2. `list_strike_targets` (filter by domain/class)
   3. Emit `targets[]` with unit from step 2 + motion/preset from meta
   Schema notes mirror the four canonical cues (convoy, flak, U-boat under way,
   harbour).

3. **No new tool for v1** — A dedicated `suggest_strike_target` tool is deferred;
   meta + prompts + existing tools are enough. Revisit if invent evals fail.

4. **Tests** — Assert planning_options meta after sync for the four rows;
   assert prompts/schema mention the decision table / call order; optional
   stub invent smoke only if already easy (do not require live LLM).

5. **Future promote checklist (BACKLOG only)** — Document steps for new theatre
   and/or new target units so agents/humans do not invent ad-hoc process. Not
   implemented as code in this change.

## Risks / Trade-offs

- [LLM ignores meta] → Strong prompt + schema repetition; later `#8d` follow-on
  tool if needed.
- [Meta drifts from examples] → Tests pin preferred_* keys for shipped presets.
- [Checklist becomes stale] → Keep it short in BACKLOG; link R11 for map audits.

## Migration Plan

- Additive YAML meta + prompt text; re-`catalog sync` picks up planning_options.
- No schema version bump required unless catalog shape changes (it should not).

## Open Questions

- None blocking — optional later: `suggest_strike_target` tool after invent evals.
