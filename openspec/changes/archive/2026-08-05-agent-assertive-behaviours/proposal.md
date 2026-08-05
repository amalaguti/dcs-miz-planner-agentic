## Why

Live eval and adversarial findings A1–A4 show the agent is told to invent immersion while
`SPEC_SHAPE_REMINDER` forces `triggers: []`, schema examples are bare, and
`infer_creative_from_spec` credits incomplete late-act recipes. `#32` already rejects
dormant late-act Specs; this change aligns prompts, schema views, and memory inference so
assertive creativity is coherent.

## What Changes

- Fix `SPEC_SHAPE_REMINDER`: triggers may be non-empty for immersion; empty only when unused.
- Point `get_mission_spec_schema` notes at immersion example paths (gates, radio, narrative).
- Infer `radio_late_activation` only when late_activation **and** `activate_group` (complete).
- Strengthen prompts: 1–2 behaviours on vague asks; do not use `randomize_mission` as authoring;
  prefer campaign Doc filenames (already honest).
- Soft behaviour floor via prompt (prefer list / assertive creativity_level); no hard reject loop.
- Tests for reminder wording, infer completeness, prompt mentions.

## Non-goals

- Hard post-emit repair loop / force N behaviours in validate (`#32` covers late-act).
- PDF extract (`#40`), tool trust (`#33`), stub multi-tool creativity harness.
- Draft-on-capture full validate (A5 — defer).
- In-game ME acceptance (prompt/memory only).

## Capabilities

### New Capabilities
- (none)

### Modified Capabilities
- `nl-agent`: reminder + assertive emission guidance; schema immersion pointers.
- `user-memory`: creative infer only complete radio+late-act recipes.

## Impact

`agent/spec_schema.py`, `agent/prompts.py`, `memory/creative.py`, tests, BACKLOG `#30c`, LESSONS.
