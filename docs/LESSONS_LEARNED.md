# Lessons Learned

Living agent notes. **Read before** PyDCS / compiler / DCS integration work.
**Append** when a non-obvious bug or wrong assumption is fixed so we do not repeat it.

Format per entry: short title, date, symptom → cause → fix/workaround, optional “code touchpoint”.

---

## Install inventory: SQLite cache, never execute DCS Lua

- **Date:** 2026-07-26
- **Lesson:** Local theatre availability lives in `%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite` (override with `DCS_MIZ_INVENTORY_DB` / `--db`). Ordinary `dcs-miz theatres` reads the cache; `--refresh` rescans. Packaged Channel YAML stays the product SoT — do not copy registry facts into SQLite.
- **Parse only:** `autoupdate.cfg` (JSON), terrain `entry.lua` / `pluginsEnabled.lua` via constrained regex for quoted fields. Never `exec` / import DCS Lua.
- **Discovery:** on Windows, prefer `HKCU/HKLM\SOFTWARE\Eagle Dynamics\DCS World` `Path` (covers non-Program-Files installs like `S:\DCS World`), then common Program Files / Steam locations; override with `--dcs-root` / `DCS_MIZ_DCS_ROOT`.
- **Code:** `src/dcs_miz_planner/install/`.

## Stock Channel Spitfire: native triggers, almost no Lua

- **Date:** 2026-07-26
- **Lesson:** ED Channel Spitfire Instant Action missions audited in R5 use **native ME triggers** (zones, flags, radio menus, unit-dead, messages/VO). **No Mist, no MOOSE, no zip-root `.lua`** in that corpus. Prefer native trigger compile (M6 `#20`–`#21`) for Channel combat behaviour.
- **Training exception:** `1-Startup.miz` uses short `a_do_script` payloads stored as **dictionary ActionText** keys (Mission Scripting API / event handlers), not separate zip `.lua` files — template for optional M6 `#22` snippets.
- **Beware! Beware!** Channel campaign missions can ship with **empty** trigger tables; immersion is briefing/kneeboard/VO/AI routes, not triggers.
- **Source:** `research/lua-usage-patterns.md` (gitignored). Revisit after R1–R2 user-file audits.
- **Do not:** assume free flight ⇒ zero triggers (stock Cold/Free Flight still have zone→VO scaffolding).

## Mission Scripting API defs ≠ ME trigger predicates

- **Date:** 2026-07-26
- **Lesson:** EmmyLua / `dcs-world-schema` helps author **SSE** Lua (`trigger.action.*`, `world.addEventHandler`). It does **not** validate Mission Editor action names (`a_out_text_delay`, `c_part_of_coalition_in_zone`). Those need PyDCS emit + golden fixtures against stock extracts.
- **Source:** `research/lua-ide-tooling.md`. Vendor LuaLS lab only when M6 `#22` starts; VEAF MCP is a lab microscope, never the product compiler.

## Spitfire / WWII: group frequency must be in VHF band

- **Date:** 2026-07-26
- **Symptom:** Compiled Manston free-flight `.miz` opens in the Mission Editor, but launching the flight warns the radio frequency is invalid for the Spitfire. PyDCS defaults every group to `["frequency"]=251`.
- **Cause:** 251 MHz is a modern UHF value. WWII radios cannot tune it: Allied VHF is ~**100–156 MHz**, German VHF ~**38.4–42.4 MHz**.
- **Fix:** Set the group frequency from the Channel registry radio table (Spitfire **124**, Bf-109K-4 40, FW-190 38.4) — the values every stock ED Channel mission uses. Assigning `group.frequency` is enough; DCS tunes the aircraft's first radio channel from it, and stock missions leave `radioSet = false`.
- **Code:** `src/dcs_miz_planner/compiler/pydcs_compiler.py`; data in `data/channel/aircraft.yaml` via `registry.py`.
- **Do not:** use the airfield ATC frequency as the flight frequency. It is in-band and works (Channel ATC VHF-high runs 118.05–118.6, Manston = 118.45), but it is the tower channel, not the flight's, and diverges from every stock mission.
- **Note:** PyDCS `set_frequency()` also flips `radio_set` and writes channel presets — more than ME does. Plain attribute assignment matches stock output.

## Spitfire cockpit arguments: triggers only, not compile input

- **Date:** 2026-07-25
- **Lesson:** Community list [DCS User Files 3349460](https://www.digitalcombatsimulator.com/en/files/3349460/) (ModelViewer2 args for Spitfire LF Mk.IX) is for Mission Editor **triggers** that watch cockpit state (e.g. switch/gauge animation args). It does **not** set cold-start / parking state and is **not** needed for free-flight `.miz` compile.
- **Caveats:** Tied to DCS **2.9.25.21402**; some rows marked incomplete (red text in the sheet). Animation argument numbers are not the same as clickable command IDs — re-verify in-game before promoting into a registry.
- **Local copy:** `research/spitfire-cockpit-arguments/` (PDF + Excel; gitignored under `research/`). Do not commit the RAR or dump raw args into the product registry until an interactive/training-mission change needs them.

## PyDCS: payload loader KeyError when DCS install is present

- **Date:** 2026-07-25
- **Symptom:** `KeyError` on a path under `S:/DCS World/.../UnitPayloads/*.lua` while creating aircraft via `Mission.flight_group_from_airport` / `Plane.__init__` → `FlyingType.load_payloads`.
- **Cause:** With a real DCS install detected, PyDCS scans payload dirs. `scan_payload_dir` skips files with no `["unitType"]` line (never caches them). `load_payloads` then does `_payload_cache[payload_path]` → KeyError. Upstream bug in PyDCS `unittype.py`; free-flight missions do not need payloads.
- **Fix / workaround:** In our compiler only, call `_disable_payload_scan(...)` before creating units: seed `_payload_cache` so the install is not scanned, and set `aircraft_type.payloads = {}` so `load_payloads` returns early. Do **not** edit files under `.venv`.
- **Code:** `src/dcs_miz_planner/compiler/pydcs_compiler.py` (`_disable_payload_scan`).
- **Do not:** Re-enable full install payload scanning without fixing the KeyError path (`.get` / skip missing keys) or pinning a fixed PyDCS.

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

## DCS identity strings: never invent

- **Date:** 2026-07-24 (research) / reinforced in M1
- **Symptom:** Mission fails to load or units missing if type / airfield ids are wrong.
- **Cause:** Guessing spellings (`Spitfire IX`, wrong `airdromeId`, etc.).
- **Fix:** Use verified ids only (`SpitfireLFMkIX`, Manston → `airdromeId` 5, theatre `TheChannel`, …). Prefer `registry.py` / `data/channel/*.yaml` over memory. Expand the registry via data PRs, not ad-hoc in prompts.

## Mission Spec vs PyDCS boundary

- **Date:** 2026-07-25
- **Lesson:** Keep `MissionSpec` / loader / CLI free of PyDCS imports. All PyDCS usage stays behind `CompilerInterface` / `pydcs_compiler.py` so a future native compiler can replace the backend.

## OpenSpec / git process

- **Date:** 2026-07-24
- **Lesson:** Never implement or commit OpenSpec work on `master`/`main`. Branch name = change name. Enforced by Cursor hook `protect-master.py` and pre-commit `no-commit-to-branch`.

---

## How to add an entry

1. Put new lessons **at the top** of the list (newest first), under a `##` heading.
2. Prefer one concrete failure over long narrative.
3. Link the code path or OpenSpec change if it exists.
4. If the lesson changes product behavior, also update specs/design as needed — this file is not a substitute for OpenSpec.
