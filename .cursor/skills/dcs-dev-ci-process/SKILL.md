---
name: dcs-dev-ci-process
description: >-
  Hermetic CI, install inventory SQLite cache, and OpenSpec/git process notes for
  this repo. Use when changing GitHub Actions, conftest inventory fakes, golden
  normalization for CI, or install discovery.
---

# CI, install inventory & process

## Read first

[`docs/lessons/ci-process.md`](../../../docs/lessons/ci-process.md)

## Hard rules

1. CI is **hermetic** — no DCS install on runners. Tests must not require live inventory
   (`tests/conftest.py` fake / explicit `inventory=`).
2. Strip/normalize **liveries** and `onboard_num` in goldens for cross-machine parity.
3. Install inventory: SQLite cache under LocalAppData; **never execute DCS Lua** to probe.
4. OpenSpec work stays off `master`/`main`; finish = docs → commit → sync → archive →
   commit → ask merge (`openspec-finish-change`).
5. **OpenSpec CLI:** `npx openspec …` (npm `@fission-ai/openspec`). Not `uv openspec`
   / `uv run openspec`. Fallback: `.\node_modules\.bin\openspec.cmd`.
6. After promoting a theatre into registry YAML, run **`dcs-miz theatres --refresh`**
   so cached `planner_supported` flips (stale cache looks “available” but validate fails).

## Code touchpoints

`tests/conftest.py`, `install/`, `.github/workflows/`, OpenSpec skills.
