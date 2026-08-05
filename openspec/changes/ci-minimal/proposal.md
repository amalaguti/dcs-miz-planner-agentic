## Why

Pre-commit runs ruff locally on commit, but pytest is manual and hooks can be skipped.
PRs and GitHub web edits have no remote gate. Adversarial backlog `#36` asks for minimal
GitHub Actions so every PR still gets pytest + ruff.

## What Changes

- Add a GitHub Actions workflow on pull_request (and optionally push to `master`) that
  installs with `uv`, runs `ruff check` / `ruff format --check`, and `pytest`.
- Document the workflow in README Status / stack briefly; mark BACKLOG `#36` done.
- New OpenSpec capability `ci` describing the required remote checks.

## Non-goals

- No `@live_llm` / `@needs_dcs` jobs in v1.
- No pre-commit.ci service; no required status checks configuration in branch protection
  (repo admin may enable later).
- No deploy, release, or coverage upload.
- No DCS Mission Editor acceptance for this change.

## Capabilities

### New Capabilities

- `ci`: Remote continuous integration — hermetic pytest + ruff on PRs via GitHub Actions.

### Modified Capabilities

- (none)

## Impact

- New `.github/workflows/` YAML; docs/BACKLOG/README; new `openspec/specs/ci/`.
- CI runners use Linux + uv; suite must remain hermetic (already true for default pytest).
