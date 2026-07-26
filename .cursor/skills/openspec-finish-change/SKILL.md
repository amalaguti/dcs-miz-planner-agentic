---
name: openspec-finish-change
description: Wrap up an accepted OpenSpec change in the correct order - docs, commit, spec sync, archive, commit, then merge. Use when a change passes acceptance testing, when the user says a task is done/accepted, or when asked whether to archive, commit, or merge first.
---

# Finish an OpenSpec Change

Run these steps **in order** on the change branch. Never on `master`/`main`.

## Why this order

Archiving is itself a file change: it moves `openspec/changes/<name>/` into
`openspec/changes/archive/YYYY-MM-DD-<name>/` and syncs delta specs into
`openspec/specs/`. Commits on `master`/`main` are blocked (Cursor hook +
pre-commit), so the archive must be committed from the branch. Merging last
means `master` receives one coherent state: code, synced specs, archived change.

## Steps

```
- [ ] 1. Update docs to match reality
- [ ] 2. Commit the implementation
- [ ] 3. Sync delta specs, then archive the change
- [ ] 4. Commit the archive + spec sync
- [ ] 5. Merge (ask first — the user often merges themselves)
```

**1. Update docs to match reality**

- Tick remaining `tasks.md` boxes, including acceptance tasks; note in-game findings inline.
- Flip the item's status in `docs/BACKLOG.md` (`building` → `done`).
- Refresh `README.md` status if it still claims work is pending (`keep-readme-updated`).
- Add any non-obvious pitfall to `docs/LESSONS_LEARNED.md` (`keep-lessons-learned`).
- Run the test suite before committing: `uv run pytest -q`.

**2. Commit the implementation**

Code, tests, examples, and the doc updates from step 1 — reviewable on its own.
Never stage gitignored scratch files (`research/`, `out/`, `ideas-*.txt`).
Pre-commit runs Ruff on Python; if the hook auto-fixes files, stage those changes and commit (new commit unless amend rules allow).

**3. Sync delta specs, then archive the change**

Delta specs under `openspec/changes/<name>/specs/` become main specs in
`openspec/specs/<capability>/spec.md` (`openspec-sync-specs`), then archive
(`openspec-archive-change`). Verify tasks and artifacts read `done` first.

**4. Commit the archive + spec sync**

Separate commit from step 2, so the archive move stays readable in history.

**5. Merge**

Ask before merging — the user frequently does this themselves. Delete the
branch only once merged.

## Guardrails

- Confirm acceptance actually happened (opened/flew in DCS), not just that it compiled.
- Never `git add -A` blindly; check `git status` for ignored or unrelated files.
- If acceptance revealed a fix, that fix belongs in step 2's commit, not after the archive.
