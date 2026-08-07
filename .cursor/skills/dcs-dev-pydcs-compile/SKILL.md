---
name: dcs-dev-pydcs-compile
description: >-
  PyDCS Mission compile pitfalls for this repo: terrain binding, payloads,
  theatre zip member, weather enums, briefing l10n, goldens, escort/GA/CAP
  layout. Use when changing the compiler, golden fixtures, or debugging .miz
  structure / KeyErrors.
---

# PyDCS compile

## Read first

[`docs/lessons/pydcs-compile.md`](../../../docs/lessons/pydcs-compile.md)

## Hard rules

1. **Only** `compiler/pydcs_compiler.py` (and emit helpers) import `dcs.*`.
2. Bind terrain via `theatre_terrain.terrain_for_theatre(spec.theatre)` — never
   hard-code `TheChannel()` while ignoring Spec.
3. Keep **`_disable_payload_scan`** until a released pydcs wheel includes the
   payload KeyError fix; use registry CLSID loadouts for GA.
4. Ensure **theatre** zip member (`_ensure_theatre_member`); PyDCS may omit it.
5. Weather: `clouds_iprecptns` is an **enum**, not a raw int.
6. Briefing: PyDCS `set_sortie_text` / `set_description_*`; lazy-import briefing
   to avoid compiler↔agent cycles.
7. Goldens: normalize `onboard_num` (and liveries in CI) — see `normalize_mission`.
8. Escort: package first, then EscortTaskAction + ROE; GA: verify land vs water
   strike placement.

## Code touchpoints

`compiler/pydcs_compiler.py`, `theatre_terrain.py`, `tests/fixtures_support.py`,
`tests/refresh_*_golden.py`.
