---
name: /full-catalog-orchestrate
id: full-catalog-orchestrate
category: Workflow
description: Orchestrate one full-catalog OpenSpec slice (planner → implementer → verifier → Agent Review)
---

Run **one** full-catalog theatre/catalog slice using the orchestrator pattern.
You are the parent coordinator. Do not implement the slice yourself unless a
subagent is unavailable; prefer specialists.

**Read first:** `.cursor/skills/full-catalog-orchestrator/SKILL.md`

**Input:** Optional slice name after the command (kebab-case), e.g.
`/full-catalog-orchestrate theatre-registry-packages`. If omitted, default to
the next `idea` campaign item in `docs/BACKLOG.md` (usually Slice 0
`theatre-registry-packages`, then `theatre-agnostic-planning`). If ambiguous,
ask.

## Steps

1. **Git** — If on `master`/`main`, create/switch to a branch named **exactly**
   the OpenSpec change name (`.cursor/skills/openspec-git-branch/SKILL.md`).
   One change per branch. Do not start a second map writer.

2. **Explore** — Use the built-in Explore subagent for current code/tests that
   will move (keep noisy search out of this context).

3. **Research** — `/theatre-researcher` for map geography / PyDCS bind. For
   unit shelves also `/catalog-units`. For invent/prompts `/mission-catalog`.

4. **Plan** — `/planner`. Then `/opsx-propose` (or `openspec-propose` skill)
   so `proposal.md` / `design.md` / `tasks.md` exist.

5. **Implement** — `/implementer` only after artifacts exist. Implementer is
   the only writer. Specialists stay readonly.

6. **Verify** — `/verifier` (ruff + `uv run pytest -q` + compile new examples).
   If it fails, resume implementer; do not merge.

7. **Agent Review** — `/agent-review` (or Source Control → Agent Review).
   **Deep** if registry/compiler/validation moved; **Quick** if docs-only.

8. **Finish** — `.cursor/skills/openspec-finish-change/SKILL.md`: docs, impl
   commit, archive+spec sync commit, **ask before merge**. ME Instant Action
   is a human do-soon after merge, not a merge gate.

9. **Stop** — Do not start the next map until this branch is merged to master.
   Readonly research of map N+1 may write only gitignored `research/theatres/`.

## Gates

- Never invent DCS ids; never auto-promote install discovery.
- No Stage C combat on a new map until Slice **0b** `theatre-agnostic-planning`
  has landed on master.
- Do not `/in-cloud` two theatres at once. Optional `/babysit` only on the
  current PR.
- Campaign target: existing six mission types on PyDCS-bound installed maps —
  not AAR/SEAD/helo types, not terrains without PyDCS modules.
