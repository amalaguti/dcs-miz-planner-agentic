## ADDED Requirements

### Requirement: Frozen CI install accepts git-sourced pydcs
The GitHub Actions workflow SHALL install project dependencies with `uv sync --frozen` (plus the dev group) even when the lockfile sources `pydcs` from a pinned git revision rather than PyPI. The workflow MUST NOT switch to an unpinned `uv sync` to avoid cloning git. Hermetic pytest and Ruff checks remain the required gate; live LLM and DCS jobs MUST NOT become required.

#### Scenario: Frozen sync with git pydcs
- **WHEN** CI runs on a pull request or push to `master` / `main` and `uv.lock` records pydcs as a git source at a fixed revision
- **THEN** `uv sync --frozen --group dev` MUST succeed and the workflow MUST still run Ruff and hermetic pytest
