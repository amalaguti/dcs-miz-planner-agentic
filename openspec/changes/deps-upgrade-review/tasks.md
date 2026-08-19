## 1. Pin pydcs

- [x] 1.1 Replace `pydcs>=0.15.0` in `pyproject.toml` with git SHA `e20f328390aecaac2a7f82444b4f5a96ac6bb2c3`
- [x] 1.2 Run `uv lock` and `uv sync --frozen --group dev`; confirm `from dcs.terrain import Kola` works in the venv and `importlib.metadata.version("pydcs")` is still labeled 0.15.0

## 2. Prove compile and goldens

- [x] 2.1 Add/extend a test that compile of a Kola Spec still raises unbound-theatre (`TheatreTerrainError`); do not add a Kola factory
- [x] 2.2 Run `uv run pytest -q`; refresh Channel goldens only with a recorded reason if contracted `.miz` Lua diverges
- [x] 2.3 Re-test payload scan: keep `_disable_payload_scan` unless a compile with DCS install present stays green with scan on; record the decision in LESSONS

## 3. Docs

- [x] 3.1 Mark BACKLOG R8 done; stop saying Kola waits on missing PyDCS terrain (Kola class exists upstream; this repo still unbound)
- [x] 3.2 Prepend pydcs-compile lesson + index row for the git SHA pin and payload-scan decision; update `dcs-dev-pydcs-compile` hard rule 3
- [x] 3.3 README stack/status: pydcs is git-pinned master SHA, not the 2023 PyPI wheel; Kola still not planner-bound

## 4. Merge gate

- [x] 4.1 `uv run ruff check src tests` and `uv run ruff format --check src tests`
- [x] 4.2 `uv run pytest -q`
- [x] 4.3 Compile `examples/manston_cold_freeflight.yaml` (and one bound-map smoke) still writes a `.miz`
