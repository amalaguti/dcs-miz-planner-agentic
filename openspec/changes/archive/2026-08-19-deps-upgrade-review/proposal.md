## Why

This repo still installs PyPI `pydcs==0.15.0` (2023-04-15). Upstream master (HEAD `e20f328`) has years of terrain, payload, and warehouse fixes — including Kola — but that code is not in the wheel. A loose `pydcs>=0.15.0` (D5) can also silently pull a different 0.15.0. Pin git now so goldens and the payload-scan workaround are proven before any later map bind.

## What Changes

- Replace the PyPI pydcs pin with an exact git SHA: `e20f328390aecaac2a7f82444b4f5a96ac6bb2c3`.
- `uv lock` / `uv sync --frozen`; CI keeps using the lockfile (git clone of pydcs).
- Re-run hermetic pytest; refresh Channel goldens only with a recorded reason if the new backend changes contracted `.miz` structure.
- Re-test `_disable_payload_scan` with a local DCS install if present; keep the monkeypatch unless scan-on stays green.
- Docs: BACKLOG R8 done; LESSONS record the SHA; README/stack honesty; stop claiming Kola waits on missing upstream terrain.

## Non-goals

- No Kola / GermanyCW / Iraq / `MarianaIslandsWWII` factory, examples, or `planner_supported`.
- Do not flip fail-closed tests off Kola (it stays the unbound stand-in).
- Do not drop `_ensure_theatre_member` or other compiler workarounds without evidence.
- No ME Instant Action as an automated gate; human fly stays parallel.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `ci`: Frozen `uv` install MUST succeed when the lockfile sources pydcs from a pinned git revision, not only PyPI.
- `miz-compiler`: Payload-directory scanning MUST stay disabled unless a recorded compile with a real DCS install proves scan-on; git-pin MUST NOT bind new theatres.

## Impact

- [`pyproject.toml`](pyproject.toml), [`uv.lock`](uv.lock), [`.github/workflows/ci.yml`](.github/workflows/ci.yml) if the install step needs git.
- Possible golden refresh under `tests/fixtures/`.
- [`docs/BACKLOG.md`](docs/BACKLOG.md), [`docs/lessons/pydcs-compile.md`](docs/lessons/pydcs-compile.md), [`README.md`](README.md).
- Acceptance: default pytest green; compile still produces ME-openable Channel `.miz`; Kola still fails compile with unbound-theatre.
