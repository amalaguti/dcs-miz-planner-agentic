## Context

[`pyproject.toml`](pyproject.toml) declares `pydcs>=0.15.0`; [`uv.lock`](uv.lock) resolves the 2023-04-15 PyPI wheel. Upstream [pydcs master](https://github.com/pydcs/dcs) still labels itself `0.15.0` but includes Kola, GermanyCW, DCS 2.28 export, payload `.get()` skip, and warehouse load/save. Spec theatre binding in [`theatre_terrain.py`](src/dcs_miz_planner/theatre_terrain.py) is Channel/Normandy/Caucasus/Syria/Nevada/Falklands only. Compiler keeps `_disable_payload_scan` for the old KeyError.

## Goals / Non-Goals

**Goals:**

- Exact pydcs pin at git SHA `e20f328390aecaac2a7f82444b4f5a96ac6bb2c3`.
- Hermetic pytest green (refresh goldens only with a recorded reason).
- Payload-scan decision recorded in LESSONS; default keep monkeypatch.
- Docs stop saying Kola waits on missing upstream terrain.

**Non-Goals:**

- Kola (or any new) terrain factory, examples, catalog, invent home.
- Iraq / `MarianaIslandsWWII` dumps.
- Floating `master` branch pin.

## Decisions

1. **Git SHA, not PyPI 0.16.** Upstream has not published a newer wheel; waiting is unbounded. Pin the commit, not `git+…@master`.
2. **uv git dependency in pyproject.** Use PEP 508 `pydcs @ git+https://github.com/pydcs/dcs.git@e20f328…` so the lock records the revision. Alternative (`>=0.15.0` + hope) is D5.
3. **Keep `_disable_payload_scan` unless proven.** Master has the `.get()` skip (2026-06-16) but also loads weapon settings from payload lua (2026-06-29). Scan-on can change pylons and still KeyError on odd files. Re-test with DCS present; do not drop as a drive-by.
4. **Kola stays fail-closed.** Presence of `dcs.terrain.Kola` in the venv MUST NOT add a factory. Tests that use `Kola` as the unbound stand-in stay.
5. **Golden refresh is explicit.** If warehouses/weapon-settings/`utc_offset` change contracted Lua, refresh via existing `refresh_*_golden.py` helpers and note why. Do not weaken normalize rules.
6. **CI unchanged command.** `uv sync --frozen --group dev` already clones git deps; GitHub-hosted runners have git. No extra workflow step unless freeze fails.

## Risks / Trade-offs

- [Goldens explode from 2.28 export / warehouses / pylons] → Refresh on this branch with a LESSONS note; do not abandon the pin.
- [CI cannot reach github.com/pydcs/dcs] → Fail the job; pin is useless if lock cannot install.
- [Version string still 0.15.0] → Document SHA in LESSONS; do not treat `importlib.metadata.version("pydcs")` as the pin.
- [Kola class imported accidentally] → Factory map is the contract; tests assert `TheatreTerrainError` for `Kola`.

## Migration Plan

1. Change pyproject + `uv lock` + `uv sync`.
2. Pytest; refresh goldens if needed.
3. Payload-scan re-test (DCS present → optional scan-on experiment; keep disable if anything fails).
4. Docs. Rollback = revert pyproject/lock to the PyPI wheel.

## Open Questions

- None for this slice. Scan-on drop is evidence-gated during apply, not a product question.
