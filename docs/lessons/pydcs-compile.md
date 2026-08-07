# PyDCS compile & mission layout

Detailed lessons for this topic. Newest first within this file.
Index: [`../LESSONS_LEARNED.md`](../LESSONS_LEARNED.md).

---

## Spec theatre → PyDCS terrain binding (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Never `Mission(terrain=TheChannel())` while ignoring `spec.theatre`. Use
  `theatre_terrain.terrain_for_theatre(spec.theatre)`; unbound ids fail compile and
  validate (`theatre_terrain_unbound`). Registry theatres must stay ⊆ binding keys
  before adding a second theatre.
- **Code:** `theatre_terrain.py`, `pydcs_compiler.py`, `channel_domain.py`.

## R7 PyDCS open-issue triage (2026-08-04)

- **Date:** 2026-08-04
- **Lesson:** Open [pydcs/dcs](https://github.com/pydcs/dcs/issues) triage vs Channel compiler:
  nothing blocks current combat emit beyond workarounds we already keep
  (`_disable_payload_scan`, `_ensure_theatre_member`, explicit waypoint speeds,
  plain `group.frequency`). Payload KeyError fix is on upstream **master**
  (#439/#440, Jun 2026) but **not** in PyPI `0.15.0` — do not remove the disable
  until a released wheel includes `.get(payload_path)`. Trigger vocab gaps (#62)
  and DoScript DictKey quirks (#179) matter for R9 / `#22`. Load→save action
  reordering (#369) matters only if we rewrite foreign `.miz` files.
- **Notes:** `research/pydcs-issues.md` (gitignored). Revisit on R8 bumps.

## Briefing l10n: PyDCS setters + lazy import (no compiler↔agent cycle)

- **Date:** 2026-08-02
- **Lesson:** Populate Sortie / Description / Blue|Red Task via
  `Mission.set_sortie_text` / `set_description_*` (writes `l10n/DEFAULT/dictionary`).
  Dictionary strings use Lua line-continuation `\` for newlines, not `\n` escapes — prefer
  substring asserts over naive regex parsers. Do **not** import `agent.voice` at
  `compiler` module top-level (or via a top-level `briefing`→`agent` import): that pulls
  `agent` → `tools` → `compiler` and raises a circular `ImportError`. Lazy-import
  `build_mission_briefing_texts` inside `_apply_briefing`. Sortie = `spec.name`; Description
  = Spec description + Situation + Watch-outs; player coalition task = Tactics + Procedures
  + closing; opposing task empty in v1. Pin goldens to `voice="raf"`. Free-flight groups still
  show ME main task `CAP` (PyDCS default) — unrelated to briefing Sortie title.
- **Code:** `briefing.py`, `compiler/pydcs_compiler.py` (`_apply_briefing`),
  `tests/fixtures_support.py` (dictionary golden member).

## Escort: package first, then EscortTaskAction + ROE

- **Date:** 2026-08-02
- **Lesson:** Escort compile must place the friendly `package` group **before** attaching
  `EscortTaskAction(group_id=…)` on the player. Destination is airfield-relative
  (`bearing_deg` / `distance_km`) like CAP/strike. Package starts inflight near the
  airfield along the escort bearing (`~8 km`), task `CAS`, waypoint to destination.
  Player task `Escort` + climb / Escort / Cover waypoints; `OptROE` from
  `escort.engagement`. Optional bounce spawns near the destination neighbourhood
  (`+2500`, `-1500` m), not the intercept Hawkinge corridor. Package coalition MUST match
  the player; enemies oppose. Example: Manston → 120° / 55 km, 2× `MosquitoFBMkVI`,
  2× `Bf-109K-4`.
- **Code:** `compiler/pydcs_compiler.py` (`_apply_escort`, `_place_escort_enemies`),
  `examples/manston_escort.yaml`, `models.Escort` / `PackageFlight`.

## Ground-attack: always verify strike position (land vs water, enemy vs practice)

- **Date:** 2026-08-02 (validate enforced 2026-08-05)
- **Lesson:** Before accepting any ground-attack example or compile, **check target
  geography in ME / against PyDCS airport math** — do not trust bearing/distance intuition.
  Shared validation now fails `strike_domain_mismatch` when the compile-equivalent strike
  Point’s Channel land/sea class disagrees with target unit domain (`channel_domain.py`
  UK–FR airport chord heuristic). `randomize` geometry redraws strike until domain matches.
- **Checks (every GA Spec):**
  1. Resolve strike Point from player airfield (`point_from_heading`); compare to known
     Channel airports (e.g. Dunkirk ≈ 120° / 72 km from Manston).
  2. **Land vehicles:** strike must be on land in enemy-held territory for combat (Axis
     French/Belgian coast for Channel WWII blue). Stopping *short* of a coastal airfield
     along a Channel crossing is usually **still water** (e.g. Manston→Dunkirk at 65 km).
     Prefer at/past the coast or an inland offset (example: ≈125° / 76 km inland of Dunkirk).
  3. **Water:** mid-Channel / offshore → `ships.yaml` sea-domain units only, never trucks.
  4. **Practice** (`strike.practice: true`): same-coalition / UK-side land OK; still verify
     the Point is actually on land, not the Strait.
  5. Confirm ME mission planner Target / Bombing waypoint and placed units agree (same
     land/sea domain).
- **Code:** `channel_domain.py`, `validation.py`, `randomize.py`,
  `examples/manston_ground_attack.yaml`, `compiler/pydcs_compiler.py`
  (`_apply_ground_attack`).

## Ground-attack: registry CLSID loadout + Bombing (not install payload scan)

- **Date:** 2026-08-02
- **Symptom / constraint:** Spitfire bomb + slipper loadouts must appear in `.miz` without
  re-enabling PyDCS `UnitPayloads` scanning (KeyError on some install files).
- **Cause:** Centreline pylon is tank **or** 500 lb — not both. Channel-crossing needs
  wing 250s + `SPITFIRE_45GAL_SLIPPER_TANK`. Player jettisons in cockpit; do not set
  `OptRestrictJettison`. A short SE offset (e.g. 140°/40 km) from Manston lands **in the
  sea** — land vehicles must use a bearing/distance that reaches enemy-held French/Belgian
  coast (example: ≈125° / 76 km inland near Dunkirk — **not** 65 km short of the coast,
  which is still water). Mid-Channel water strikes use `ships.yaml`
  ids (`Schnellboot_type_S130`, etc.) via `ship_group`, never trucks. Same-coalition /
  UK-side targets are allowed only when `strike.practice` is true (bombing-practice
  narrative); DCS gladly places friendly units as ME targets.
- **Fix:** Named presets in `payloads.yaml`; compiler `_disable_payload_scan` then
  `group.load_pylon((pylon, {"clsid": ...}))`. Strike uses airfield-relative
  bearing/distance; `get_strike_unit` chooses `vehicle_group` vs `ship_group` by domain;
  enemy coalition only.
- **Code:** `compiler/pydcs_compiler.py` (`_apply_ground_attack`), `data/channel/payloads.yaml`,
  `ground_units.yaml`, `ships.yaml`, `examples/manston_ground_attack.yaml`.

## CAP station is airfield-relative; ROE is Spec-backed

- **Date:** 2026-08-01
- **Lesson:** CAP Spec uses `bearing_deg` + `distance_km` from the player airfield
  (PyDCS `point_from_heading`, metres), not raw map x/y or WGS84. Example Manston CAP:
  135° / 25 km / 4000 m / circle. Engagement maps to PyDCS `OptROE` on the CAP waypoint
  (`weapons_free`→0, `open_fire`→2, `return_fire`→3, `weapons_hold`→4). Optional enemies
  spawn near the station (`+3000`, `-2000` m), not the intercept Hawkinge corridor.
  Optional `duration_min` wraps Orbit in `ControlledTask.stop_after_duration`. Group
  `task` must be `"CAP"`.
- **Code:** `models.Cap`, `compiler/pydcs_compiler.py` (`_apply_cap`, `_place_cap_enemies`);
  example `examples/manston_cap.yaml`.

## Golden fixtures: normalize random `onboard_num`

- **Date:** 2026-07-26
- **Symptom:** Full `mission` member comparison fails across processes even when the Spec is unchanged.
- **Cause:** PyDCS assigns a random `["onboard_num"]` per process; other Manston free-flight fields stay stable.
- **Fix:** Store a normalized golden (`onboard_num` → `"<num>"`) and compare after the same normalization; keep explicit substring contracts (Manston, frequency, etc.).
- **Code:** `tests/fixtures_support.py`, `tests/fixtures/manston_cold_freeflight/`; refresh with `uv run python tests/refresh_manston_golden.py`.

## Mission Scripting API defs ≠ ME trigger predicates

- **Date:** 2026-07-26
- **Lesson:** EmmyLua / `dcs-world-schema` helps author **SSE** Lua (`trigger.action.*`, `world.addEventHandler`). It does **not** validate Mission Editor action names (`a_out_text_delay`, `c_part_of_coalition_in_zone`). Those need PyDCS emit + golden fixtures against stock extracts.
- **Source:** `research/lua-ide-tooling.md`. Vendor LuaLS lab only when M6 `#22` starts; VEAF MCP is a lab microscope, never the product compiler.

## PyDCS: payload loader KeyError when DCS install is present

- **Date:** 2026-07-25 (updated 2026-08-04)
- **Symptom:** `KeyError` on a path under `S:/DCS World/.../UnitPayloads/*.lua` while creating aircraft via `Mission.flight_group_from_airport` / `Plane.__init__` → `FlyingType.load_payloads`.
- **Cause:** With a real DCS install detected, PyDCS scans payload dirs. `scan_payload_dir` skips files with no `["unitType"]` line (never caches them). `load_payloads` then does `_payload_cache[payload_path]` → KeyError. Upstream bug in PyDCS `unittype.py`; free-flight missions do not need payloads.
- **Fix / workaround:** In our compiler only, call `_disable_payload_scan(...)` before creating units: seed `_payload_cache` so the install is not scanned, and set `aircraft_type.payloads = {}` so `load_payloads` returns early. Do **not** edit files under `.venv`.
- **Code:** `src/dcs_miz_planner/compiler/pydcs_compiler.py` (`_disable_payload_scan`).
- **Do not:** Re-enable full install payload scanning without fixing the KeyError path (`.get` / skip missing keys) or pinning a fixed PyDCS.
- **Upstream (R7):** `.get()` fix merged on pydcs `master` (#439/#440, 2026-06); **not** in PyPI `0.15.0`. Keep the monkeypatch until R8 bumps to a release that includes it, then re-test with scan on.

## PyDCS: no standalone `theatre` zip member

- **Date:** 2026-07-25
- **Symptom:** Compiled `.miz` has `mission` / `options` / `warehouses` but no `theatre` file; theatre only appears as `["theatre"]="TheChannel"` inside `mission`.
- **Cause:** PyDCS `Mission.save` does not write a top-level `theatre` member (real ME-exported missions usually do).
- **Fix:** After `mission.save`, append a `theatre` member with the theatre id string if missing (`_ensure_theatre_member`).
- **Code:** `src/dcs_miz_planner/compiler/pydcs_compiler.py`.
- **Note:** DCS often still loads without the file; we keep it for fidelity and our compiler acceptance contract.

## PyDCS weather: `clouds_iprecptns` is an enum

- **Date:** 2026-07-25
- **Symptom:** `AttributeError: 'int' object has no attribute 'value'` in `Weather._make_cloud_dict` during `mission.save`.
- **Cause:** Assigning `clouds_iprecptns = 0` (int). PyDCS expects `Weather.Preceptions` (e.g. `Preceptions.None_`).
- **Fix:** Use `Weather.Preceptions.None_` (and other enum members) for clear / precip settings.
- **Code:** `PyDCSCompiler._apply_weather`.

## Mission Spec vs PyDCS boundary

- **Date:** 2026-07-25
- **Lesson:** Keep `MissionSpec` / loader / CLI free of PyDCS imports. All PyDCS usage stays behind `CompilerInterface` / `pydcs_compiler.py` so a future native compiler can replace the backend.
