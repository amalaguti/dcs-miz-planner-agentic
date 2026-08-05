---
name: eval-agent-creativity
description: >-
  Live-evaluates the NL mission planner on vague human-like asks: runs plan/chat
  sessions, checks mission_behaviour/inspiration usage, campaigns/Docs, detail.creative
  memory, and feedback bias; then writes LESSONS and/or OpenSpec proposals from gaps.
  Use when the user asks to eval/test/regression the agent creatively, play the new
  stack, probe assertive immersion, or refresh agent behaviour after shipping features.
---

# Eval agent creativity (live)

Periodic live check that the planner **uses** packaged creativity (behaviours,
inspirations, campaigns, memory) — not that Specs merely validate.

## When to run

- After shipping agent/catalog/prompt/memory changes
- When the user asks to “play the stack”, “eval the agent”, or “see if creativity works”
- Before promoting more Spec predicates (prefer finding prompt/tool gaps first)

Requires: local `.env` with `OPENAI_API_KEY` (see `.env.example`). Prefer `--stub` only
to dry-run the harness, not for creativity judgement.

## Hard rules

- Use an **isolated eval SQLite** under `out/creative_eval/` (gitignored). Do not wipe
  the user’s real inventory DB.
- Never print or commit API keys / `.env`.
- Do **not** invent Lua or new Spec types during eval; record gaps for OpenSpec instead.
- Keep eval artifacts under `out/` (gitignored). Durable outcomes go to LESSONS / OpenSpec /
  BACKLOG only when warranted.

## Workflow

Copy and track:

```
Eval progress:
- [ ] 1. Refresh prompt catalog expectations from current features
- [ ] 2. Preflight catalog + campaigns
- [ ] 3. Run live vague-ask suite
- [ ] 4. Score Specs + history + tool use
- [ ] 5. Outcomes → LESSONS / OpenSpec / BACKLOG
- [ ] 6. Update prompt-catalog.md if new behaviours shipped
```

### 1. Refresh expectations

Read [prompt-catalog.md](prompt-catalog.md). For each scenario, confirm `expect` still
matches shipped cards in `planning_options.yaml` (`mission_behaviour` /
`mission_inspiration`) and tools (`list_installed_campaigns`, research focus, creative
memory). **Update the catalog in the same PR/session** when new behaviours ship.

### 2. Preflight

```bash
uv run python .cursor/skills/eval-agent-creativity/scripts/run_eval.py --preflight
```

Must show non-empty behaviours/inspirations; campaigns optional (warn if missing DCS root).

### 3. Run live suite

Default (all catalog prompts, live LLM, isolated DB):

```bash
uv run python .cursor/skills/eval-agent-creativity/scripts/run_eval.py
```

Useful flags:

- `--only <id>` — one scenario (e.g. `ff-interesting`)
- `--list` — print scenario ids
- `--stub` — harness only (not a creativity pass)
- `--dcs-root <path>` — campaign index root

Allow several minutes (multiple live plans). Verbose tool traces go to stderr.

### 4. Score outcomes

For each run, judge against the scenario’s `expect` in the catalog:

| Signal | Pass hint |
|--------|-----------|
| Spec fields | Triggers/narrative/late-act match expected behaviour recipes |
| Completeness | No half-recipes (e.g. `late_activation` without radio/`activate_group`) |
| Tool use | `list_mission_options` called; campaigns/Docs when scenario says so |
| Memory | `detail.creative` present when immersion applied (infer or explicit) |
| Avoid | Blank free_flight when ask was immersion-shaped; randomize loops instead of authoring |

Write a short table in the chat reply: prompt → mission_type → behaviours used → pass/fail → notes.

Read `out/creative_eval/report.json` for machine summary.

### 5. Turn gaps into durable work

**LESSONS_LEARNED** (`keep-lessons-learned`): append only for non-obvious agent/product
pitfalls (e.g. incomplete radio+late-act combo, free-flight never inventing gates). Skip
one-off model flakiness.

**OpenSpec**: if the gap is product behaviour (prompts, tools, validation of incomplete
recipes, new cards), propose a change (`openspec-propose` / `/opsx:propose`) on a feature
branch — do not implement on `master`.

**BACKLOG**: if research-sized or deferred, add/adjust a row instead of a full change.

Prefer **fix/extend agent assertiveness** over new ME predicates unless play shows a
hard Spec gap.

### 6. Keep the catalog current

When adding a `mission_behaviour` / inspiration card or agent tool:

1. Add or edit a scenario in [prompt-catalog.md](prompt-catalog.md)
2. Mention the new id in this skill’s description only if discovery terms change
3. Re-run at least `--only` for that scenario after implement

## Related

- [prompt-catalog.md](prompt-catalog.md) — vague asks + expectations (maintain this)
- [scripts/run_eval.py](scripts/run_eval.py) — live harness
- `keep-lessons-learned` — when to append `docs/LESSONS_LEARNED.md`
- `openspec-propose` / `openspec-git-branch` — for fix/extend changes
