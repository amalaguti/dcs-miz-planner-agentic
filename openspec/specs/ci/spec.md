# CI

## Purpose

Remote continuous integration gate for hermetic tests and lint on GitHub.

## Requirements

### Requirement: Pull request CI runs pytest and ruff
The repository SHALL include a GitHub Actions workflow that runs on pull requests targeting
`master` or `main`. The workflow MUST install project dependencies with `uv`, MUST run
Ruff lint and format check (equivalent to `ruff check` and `ruff format --check`), and
MUST run the default hermetic pytest suite. Jobs that require a live LLM or DCS install
MUST NOT be required for this minimal CI gate.

#### Scenario: PR workflow present
- **WHEN** a developer opens or updates a pull request against `master` or `main`
- **THEN** GitHub Actions MUST run a workflow that executes Ruff checks and pytest

#### Scenario: Hermetic suite only
- **WHEN** the minimal CI workflow runs
- **THEN** it MUST NOT require `@live_llm` or `@needs_dcs` (or equivalent) markers as a
  required step

### Requirement: Frozen CI install accepts git-sourced pydcs
The GitHub Actions workflow SHALL install project dependencies with `uv sync --frozen` (plus the dev group) even when the lockfile sources `pydcs` from a pinned git revision rather than PyPI. The workflow MUST NOT switch to an unpinned `uv sync` to avoid cloning git. Hermetic pytest and Ruff checks remain the required gate; live LLM and DCS jobs MUST NOT become required.

#### Scenario: Frozen sync with git pydcs
- **WHEN** CI runs on a pull request or push to `master` / `main` and `uv.lock` records pydcs as a git source at a fixed revision
- **THEN** `uv sync --frozen --group dev` MUST succeed and the workflow MUST still run Ruff and hermetic pytest
