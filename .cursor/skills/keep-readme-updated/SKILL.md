---
name: keep-readme-updated
description: Keep the project README.md brief and current when status, scope, stack, or milestones change. Use when finishing a milestone, before git push, after OpenSpec/init changes, or when the user asks to update docs.
---

# Keep README Updated

## Rules

- Keep `README.md` **brief** (short sections, no essay).
- Update it when any of these change: project status, MVP acceptance criteria, stack, how to run, or repo layout that users need.
- Do **not** dump research notes, OpenSpec change logs, or sample-mission archaeology into the README — link out if needed.
- Prefer editing Status / Stack / Docs sections in place over adding new long sections.

## When pushing

Before `git push`, check whether this session’s work changed status or setup. If yes, update `README.md` in the same commit set (or a follow-up commit) before pushing.

## Related: architecture map

`docs/ARCHITECTURE.md` is the developer module map. Update it (same commit) when package layout,
module responsibilities, or the Mission Spec → `.miz` flow change. A push hook
(`.cursor/hooks/architecture-on-push.py`) reminds you when `src/dcs_miz_planner/` is being pushed
without it. Keep diagrams there, not in README.
