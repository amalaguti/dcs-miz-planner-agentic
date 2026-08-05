## Context

Local pre-commit covers ruff + hygiene, not pytest. No `.github/workflows` yet.

## Goals / Non-Goals

**Goals:** PR workflow running uv sync, ruff check/format --check, pytest -q.

**Non-Goals:** Live LLM/DCS markers; coverage badges; Windows matrix (Linux is enough
for hermetic suite).

## Decisions

1. **Trigger:** `pull_request` to `master`/`main`, plus `push` to those branches so
   post-merge master stays green.
2. **Tooling:** Official `astral-sh/setup-uv` + Python 3.12 matching `requires-python`.
3. **Commands:** `uv sync --frozen` if lockfile present else `uv sync`; then
   `uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest -q`.
4. **Capability name `ci`:** documents required remote checks; not a product runtime feature.

## Risks / Trade-offs

- [Lockfile drift] → Prefer `--frozen` when `uv.lock` exists; fail loudly if out of date.
- [Windows-only bugs] → Accept; hermetic suite already runs on developer Windows + CI Linux.

## Migration Plan

Land workflow → archive → merge. Enable required checks in GitHub settings optionally later.
