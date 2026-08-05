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
