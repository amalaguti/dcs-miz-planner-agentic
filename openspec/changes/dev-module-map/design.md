## Context

Runtime code lives under `src/dcs_miz_planner/` (`cli`, `loader`, `models`, `reference`, `compiler/`). Repo also has OpenSpec, Cursor skills/hooks, examples, and gitignored research. Ideas backlog asked for a module diagram refreshed on meaningful updates. Backlog pending decision: manual vs hook vs CI — prefer **manual doc + push reminder**, not CI generation.

## Goals / Non-Goals

**Goals:**

- One place a developer opens to see how Spec → `.miz` flows through modules.
- Diagram of relationships (imports / data flow), not a file laundry list.
- Reminder path so the doc does not rot silently.

**Non-Goals:**

- Perfect auto-sync on every commit; full API reference; research corpus docs.

## Decisions

1. **Canonical file: `docs/ARCHITECTURE.md`**
   - Short prose + one Mermaid (or ASCII) diagram of: CLI → loader → MissionSpec → CompilerInterface → PyDCSCompiler → reference → `.miz`.
   - Second small diagram or section for repo layout: `openspec/`, `.cursor/`, `examples/`, `tests/`, `research/` (gitignored).

2. **Refresh policy: manual + Cursor hook reminder**
   - Hook on `git push` (or beforeShellExecution matcher): if diff since upstream includes `src/dcs_miz_planner/**` structural files, remind agent to check `docs/ARCHITECTURE.md` (same style as `readme-on-push.py`).
   - Alternative: CI fail if out of date — rejected (hard to detect drift reliably).
   - Alternative: generate-on-commit — rejected (noise, tooldeps).

3. **README:** one Docs bullet linking ARCHITECTURE; no diagram duplication in README.

4. **OpenSpec capability `dev-docs`:** requirements are about presence and content of the map, not runtime behaviour. No DCS acceptance.

5. **Skill note:** extend `keep-readme-updated` or add a line in finish-change / git-branch that architecture updates go with layout changes.

## Risks / Trade-offs

- [Doc drifts after registry lands] → Reminder hook + finish-change checklist item.
- [Over-long diagram] → Cap at runtime path + one repo-layout section; defer agent boxes until M3 exists (dashed “future” optional).

## Migration Plan

1. Write `docs/ARCHITECTURE.md` from current tree.
2. Link from README; add hook reminder.
3. Update backlog item status on apply/archive.

## Open Questions

- None blocking — Mermaid vs ASCII: prefer Mermaid in GitHub-friendly markdown; ASCII fallback in same file if needed.
