---
name: openspec-git-branch
description: Keep OpenSpec work off master/main by creating a branch named after the change. Use before /opsx:propose, openspec propose, /opsx:apply, or any OpenSpec change work; also when about to edit files while on master or main.
---

# OpenSpec git branch hygiene

## Hard rule

Do **not** create, edit, or commit project changes on `master` or `main`.

## Before OpenSpec propose or apply

1. Determine the OpenSpec **change name** (kebab-case), e.g. `manston-cold-freeflight`.
2. Check the current branch: `git branch --show-current` (or `git rev-parse --abbrev-ref HEAD`).
3. If the current branch is `master` or `main`:
   - Create and switch: `git checkout -b <change-name>`
   - The branch name **must** be the OpenSpec change name (same string as `openspec new change "<name>"`).
4. If already on a non-protected branch:
   - Prefer working on a branch whose name matches the change name.
   - If the change name is known and the current branch differs, switch with `git checkout -b <change-name>` (or checkout existing `<change-name>` if it already exists).
5. Only then run OpenSpec propose/apply or write proposal/design/spec/task/code files.

## Examples

| Situation | Action |
|-----------|--------|
| On `master`, proposing `manston-cold-freeflight` | `git checkout -b manston-cold-freeflight` then propose |
| On `manston-cold-freeflight` already | Continue; do not switch to master |
| On `master`, user asks for a file edit | Refuse until a feature branch exists; ask for a change/branch name if unknown |

## Do not

- Commit or push directly to `master` / `main`
- Create OpenSpec artifacts on `master` / `main`
- Use vague branch names like `dev` or `wip` for OpenSpec work — use the change name

## Also enforced by pre-commit

`no-commit-to-branch` in `.pre-commit-config.yaml` rejects commits on `master` / `main`.
`ruff-check --fix` and `ruff-format` run on staged Python (see `[tool.ruff]` in `pyproject.toml`).
Cursor hooks block edits earlier; pre-commit is the repo safety net. After clone:
`uv tool install pre-commit` then `pre-commit install`.
