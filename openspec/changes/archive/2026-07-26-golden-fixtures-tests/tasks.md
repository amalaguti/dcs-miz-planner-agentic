## 1. Fixture layout and generation

- [x] 1.1 Add `tests/fixtures/manston_cold_freeflight/` layout (`theatre`, mission contract artifacts, required zip members metadata)
- [x] 1.2 Add an explicit refresh helper that compiles Manston with injected Channel inventory and writes/updates those fixtures (normal pytest must not rewrite them)
- [x] 1.3 Generate initial goldens from current accepted compiler output and commit them

## 2. Golden regression tests

- [x] 2.1 Add pytest that compiles Manston with injected inventory and asserts against the golden fixtures (members + theatre/mission contracts including airdromeId 5, start_time 32400, frequency 124.0)
- [x] 2.2 Thin or migrate overlapping asserts in `tests/test_compile_manston.py` so goldens are the primary structural surface (keep round-trip smoke if still useful)
- [x] 2.3 Confirm suite stays hermetic without live SQLite inventory; Ruff clean; full `uv run pytest -q` green

## 3. Docs and acceptance

- [x] 3.1 Document fixture location + refresh steps (`tests/fixtures/README.md` and brief README/ARCHITECTURE pointer); set BACKLOG item `building` → `done` on accept
- [x] 3.2 If compiler code changed: recompile Manston and open in DCS ME / Instant Action; if tests-only: green suite is acceptance (accepted 2026-07-26: tests-only, 40 passed)
