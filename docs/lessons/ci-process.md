# CI, install inventory & process

Detailed lessons for this topic. Newest first within this file.
Index: [`../LESSONS_LEARNED.md`](../LESSONS_LEARNED.md).

---

## Promote theatre → refresh inventory for `planner_supported`

- **Date:** 2026-08-09
- **Lesson:** Probe caches `planner_supported` from the packaged registry at
  `--refresh` time. After adding a theatre to `theatres.yaml` / terrain bind,
  stale SQLite rows can still show the map as `available` with
  `planner_supported=false`, and validate fails with a confusing
  “planner-supported but not locally available (state=['available'])” message
  (registry says supported; inventory row does not). Fix: run
  `dcs-miz theatres --refresh` (and `catalog sync`) before live compile.
- **Code:** `install/probe.py`, `validation.py` theatre availability join.

## OpenSpec CLI invoke: use `npx`, not `uv` (2026-08-07)

- **Date:** 2026-08-07
- **Lesson:** OpenSpec in this repo is the **npm** package `@fission-ai/openspec`
  (see `package.json` / `node_modules/.bin/openspec`). It is **not** a `uv`
  subcommand or Python tool. `uv openspec` → unrecognized subcommand;
  `uv run openspec` / `uvx openspec` → not found. Prefer **`npx openspec …`**
  (or `npx --yes openspec …`). After `npm install`,
  `.\node_modules\.bin\openspec.cmd …` also works. Do not hunt PATH for a global
  `openspec` binary first.
- **Code / notes:** README Stack; hook `protect-master.py` already allows
  `npx openspec …` read-only on master; skills `openspec-*` / `dcs-dev-ci-process`.

## Install inventory: SQLite cache, never execute DCS Lua

- **Date:** 2026-07-26
- **Lesson:** Local theatre availability lives in `%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite` (override with `DCS_MIZ_INVENTORY_DB` / `--db`). Ordinary `dcs-miz theatres` reads the cache; `--refresh` rescans. Packaged Channel YAML stays the product SoT — do not treat install inventory rows as known catalog. Known agent rows are separate `catalog_*` tables in the same file, filled only by `dcs-miz catalog sync`.
- **Parse only:** `autoupdate.cfg` (JSON), terrain `entry.lua` / `pluginsEnabled.lua` via constrained regex for quoted fields. Never `exec` / import DCS Lua.
- **Discovery:** on Windows, prefer `HKCU/HKLM\SOFTWARE\Eagle Dynamics\DCS World` `Path` (covers non-Program-Files installs like `S:\DCS World`), then common Program Files / Steam locations; override with `--dcs-root` / `DCS_MIZ_DCS_ROOT`.
- **Code:** `src/dcs_miz_planner/install/`.

## CI needs hermetic inventory; strip install-local liveries (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** GitHub runners have no DCS install cache. Any test that calls
  `validate_mission_spec` / `PyDCSCompiler` / CLI `validate` without an explicit
  `inventory=` hits `get_inventory()` → `install_inventory_unavailable`. Autouse
  `tests/conftest.py` patches `validation.get_inventory` to
  `channel_available_inventory()`; tests that need empty/disabled inventory still
  pass `inventory=` explicitly. Golden mission dumps also embed
  `livery_id` from PyDCS’s local livery scan — normalize those lines away (like
  `onboard_num`) or CI diverges even when compile is correct. Registry discovery
  must still call `_registry_dcs_paths()` on all platforms so unit tests can
  monkeypatch it (real impl returns `[]` off Windows).
- **Code:** `tests/conftest.py`, `tests/fixtures_support.normalize_mission`,
  `install/discover.py`.

## GitHub CLI + hermetic CI (no Windows/DCS on runners) (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Product CI does **not** need a Windows runner or DCS installed.
  Hermetic pytest (fake Channel inventory + golden normalizers) runs on
  `ubuntu-latest`. Install `gh` via winget (`GitHub.cli`); auth with
  `gh auth login` (HTTPS device flow) as the GitHub user that owns the remote.
  On PowerShell, do **not** use bash heredoc for `git commit` — use multiple
  `-m` flags. Prefer `gh pr create` / `gh pr merge` / `gh run watch` for remote
  CI; first green suite needed: (1) `tests/conftest.py` patches
  `validation.get_inventory`, (2) strip `livery_id` from both sides of golden
  compare, (3) always call `_registry_dcs_paths()` so Linux can monkeypatch it.
  Keep PR/push CI for the hermetic suite; in-game / live LLM stay local.
- **Code:** `.github/workflows/ci.yml`, `tests/conftest.py`,
  `fixtures_support.normalize_mission`.

## OpenSpec / git process

- **Date:** 2026-07-24
- **Lesson:** Never implement or commit OpenSpec work on `master`/`main`. Branch name = change name. Enforced by Cursor hook `protect-master.py` and pre-commit `no-commit-to-branch`.

---
