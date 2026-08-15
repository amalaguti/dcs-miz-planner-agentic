# Channel / WWII identity strings

Detailed lessons for this topic. Newest first within this file.
Index: [`../LESSONS_LEARNED.md`](../LESSONS_LEARNED.md).

---

## Theatre-scoped airfield lookup (replaces `airfield_theatres`)

- **Date:** 2026-08-15
- **Lesson:** Packaged SoT is `data/era/wwii/` + `data/shared/` +
  `data/theatres/<SpecId>/` (folder name **is** the Spec/PyDCS id:
  `TheChannel`, `Normandy`). `theatre.yaml` `id:` MUST match the folder;
  the loader fails closed if not. Airfield → `airdromeId` is
  **per-theatre** (`airdrome_id(name, theatre=)`). Validate/compile/reference
  MUST pass `spec.theatre`. Unscoped unique-name lookup remains for tests.
  Do not keep a combined `data/channel/` tree or a flat `airfield_theatres:`
  map. Channel curated keys are the 12 verified names (no airdromeIds 9 or 11).
  Normandy smoke is `NeedsOarPoint` = 28 only. Shared `weather_presets.yaml`
  covers `sunny_clear` for both maps (no Normandy weather file this slice).
- **Code:** `registry.py` (`from_packaged_packages`, `_airfields_by_theatre`),
  `data/theatres/TheChannel/`, `data/theatres/Normandy/`, `validation.py`,
  `compiler/pydcs_compiler.py`, `reference.py`.

## Normandy 2.0 Spec id is `Normandy`; tag AFs with `airfield_theatres`

- **Date:** 2026-08-09
- **Lesson:** Product name “Normandy 2.0” maps to inventory/Spec/PyDCS theatre id
  **`Normandy`** (not a separate `Normandy2` id). Smoke airfield Spec key
  **`NeedsOarPoint`** → airdromeId **28** (PyDCS name “Needs Oar Point”).
  *(Superseded for packaging: Slice 0 `theatre-registry-packages` replaced the
  combined `data/channel/` + `airfield_theatres:` map with per-theatre packages
  and `airdrome_id(name, theatre=)`. See the 2026-08-15 entry.)*
- **Code:** `data/theatres/Normandy/airfields.yaml`, `registry.airfield_theatre`,
  `catalog/sync.py`; example `examples/needs_oar_point_cold_freeflight.yaml`.

## Channel WWII Axis: use `ThirdReich`, not `Germany`

- **Date:** 2026-07-26 (validate allowlist 2026-08-05)
- **Symptom:** Intercept `.miz` shows “Allies flight: Bf 109 K-4” in the Mission Editor.
- **Cause:** PyDCS Channel defaults put modern **Germany** on **blue** (Allies). Looking up
  `Germany` reuses that blue country even when the Spec says `coalition: red`.
- **Fix:** Spec/compiler use PyDCS country id **`ThirdReich`** (DCS name “Third Reich”) on
  **red**. `_ensure_country` resolves by class attribute name, looks up by DCS display name,
  and refuses a country already parked on the wrong coalition. Shared validate allowlist
  (`allowlists.KNOWN_COUNTRIES` = UK / ThirdReich) rejects unknown countries with a
  Germany→ThirdReich hint before compile.
- **Code:** `allowlists.py`, `validation.py`, `compiler/pydcs_compiler.py`
  (`_ensure_country`); example `examples/manston_dawn_intercept.yaml`.

## Intercept spawn: Hawkinge anchor + Dover-approach offset

- **Date:** 2026-07-26
- **Lesson:** First intercept enemy flight is spawned inflight from PyDCS `TheChannel` **Hawkinge** (airdromeId 6) map x/y, plus a fixed SE offset toward the Strait as a Dover-approach corridor relative to Manston. Do not invent WGS84 lat/lon; stay in Channel terrain units.
- **Radio:** Enemy `Bf-109K-4` group frequency from registry (**40.0** MHz), same VHF rule as Spitfire 124.
- **Code:** `src/dcs_miz_planner/compiler/pydcs_compiler.py` (`_place_enemies`); example `examples/manston_dawn_intercept.yaml`.

## Spitfire / WWII: group frequency must be in VHF band

- **Date:** 2026-07-26
- **Symptom:** Compiled Manston free-flight `.miz` opens in the Mission Editor, but launching the flight warns the radio frequency is invalid for the Spitfire. PyDCS defaults every group to `["frequency"]=251`.
- **Cause:** 251 MHz is a modern UHF value. WWII radios cannot tune it: Allied VHF is ~**100–156 MHz**, German VHF ~**38.4–42.4 MHz**.
- **Fix:** Set the group frequency from the Channel registry radio table (Spitfire **124**, Bf-109K-4 40, FW-190 38.4) — the values every stock ED Channel mission uses. Assigning `group.frequency` is enough; DCS tunes the aircraft's first radio channel from it, and stock missions leave `radioSet = false`.
- **Code:** `src/dcs_miz_planner/compiler/pydcs_compiler.py`; data in `data/era/wwii/aircraft.yaml` via `registry.py`.
- **Do not:** use the airfield ATC frequency as the flight frequency. It is in-band and works (Channel ATC VHF-high runs 118.05–118.6, Manston = 118.45), but it is the tower channel, not the flight's, and diverges from every stock mission.
- **Note:** PyDCS `set_frequency()` also flips `radio_set` and writes channel presets — more than ME does. Plain attribute assignment matches stock output.

## DCS identity strings: never invent

- **Date:** 2026-07-24 (research) / reinforced in M1
- **Symptom:** Mission fails to load or units missing if type / airfield ids are wrong.
- **Cause:** Guessing spellings (`Spitfire IX`, wrong `airdromeId`, etc.).
- **Fix:** Use verified ids only (`SpitfireLFMkIX`, Manston → `airdromeId` 5, theatre `TheChannel`, …). Prefer `registry.py` / packaged `data/era/`, `data/shared/`, `data/theatres/<SpecId>/` over memory. Expand the registry via data PRs, not ad-hoc in prompts.
