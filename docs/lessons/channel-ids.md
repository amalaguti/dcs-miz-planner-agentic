# Channel / WWII identity strings

Detailed lessons for this topic. Newest first within this file.
Index: [`../LESSONS_LEARNED.md`](../LESSONS_LEARNED.md).

---

## Falklands MountPleasant key; UK dual-era (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Spec theatre `Falklands` (product name South Atlantic; era
  `modern`) curates **MountPleasant** = airdromeId **2** (PyDCS name
  `Mount Pleasant`; class `Mount_Pleasant`; 37 parking slots; do not dump
  all 27 Falklands fields). Spec key is **`MountPleasant`**, not
  `Mount_Pleasant` — same pitfall as Normandy `FordAF` ≠ `Ford_AF`. Host
  country is **UK** (blue). UK is dual-era: keep it in `era/wwii` and add
  it to `data/era/modern/countries.yaml` next to Georgia, Turkey, and USA
  so Falklands can use UK+Su-25T without putting Frogfoot on Channel.
  Reuse **Su-25T** at **251.0 MHz** (modern UHF default — not Mount
  Pleasant ATC 133.35 / 250.8). Do **not** add Spitfire to modern.
  `usaaf` is voice only, not a country. `Germany` is still not a known id
  in any era. Validate with `era_for_theatre(spec.theatre)`: Channel+UK
  still ok (wwii); Falklands+Spitfire is unknown; Channel+Su-25T is still
  unknown. Because countries are era-keyed, UK is now valid on every
  modern theatre (Caucasus/Syria/Nevada/Falklands).
- **Code:** `data/era/modern/countries.yaml`, `data/theatres/Falklands/`,
  `theatre_terrain.py` (`_falklands_terrain` → `Falklands()`).

## Nevada Nellis smoke; USA not usaaf (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Spec theatre `Nevada` (era `modern`) curates **Nellis** =
  airdromeId **4** (PyDCS name `Nellis`; 247 parking slots; do not dump all
  17 Nevada fields). Host country is **USA** (blue) — not `usaaf` (voice
  only), not Georgia, not Turkey. F2 rejected USA at Batumi because Batumi
  is a Georgia host; Nellis is a US host so USA is correct. Reuse **Su-25T**
  at **251.0 MHz** (modern UHF default — not Nellis ATC 132.55 / 327.0).
  Add USA only to `data/era/modern/countries.yaml` next to Georgia and
  Turkey; do **not** put USA in `era/wwii`. `Germany` is still not a known
  id in any era. Validate with `era_for_theatre(spec.theatre)`:
  Channel+USA or Channel+Su-25T is unknown; Nevada+UK or Nevada+Spitfire is
  unknown; Caucasus+Georgia and Syria+Turkey stay ok.
- **Code:** `data/era/modern/countries.yaml`, `data/theatres/Nevada/`,
  `theatre_terrain.py` (`_nevada_terrain` → `Nevada()`).

## Syria Incirlik smoke; Turkey not USAF (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Spec theatre `Syria` (era `modern`) curates **Incirlik** =
  airdromeId **16** (PyDCS name `Incirlik`; do not dump all 59 Syria fields).
  Host country is **Turkey** (blue) — not USA / `usaaf`, not Georgia, not
  Syria-on-red. Reuse **Su-25T** at **251.0 MHz** (modern UHF default — not
  Incirlik ATC 122.1 / 360.1). Add Turkey only to `data/era/modern/countries.yaml`
  next to Georgia; do **not** put Turkey in `era/wwii`. `Germany` is still not
  a known id in any era. Validate with `era_for_theatre(spec.theatre)`:
  Channel+Turkey or Channel+Su-25T is unknown; Syria+UK or Syria+Spitfire is
  unknown; Caucasus+Georgia stays ok.
- **Code:** `data/era/modern/countries.yaml`, `data/theatres/Syria/`,
  `theatre_terrain.py` (`_syria_terrain` → `Syria()`).

## Modern era + Caucasus Batumi smoke (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Era `modern` is a packaged shelf (`data/era/modern/`) walked by the
  registry for **countries + aircraft only**. WWII payloads / ground / ships /
  failures stay on `era/wwii/` this slice. **Georgia** is the Batumi host
  country (`dcs.countries.Georgia`) — not USAF / `usaaf`. **Su-25T** group radio
  is **251.0 MHz** (PyDCS/DCS modern UHF default) — not Spitfire VHF 124 and not
  Batumi ATC. Airfield **Batumi** = airdromeId **22** (PyDCS name `Batumi`; do
  not dump all 21 Caucasus fields). `Germany` is still not a known id in any era.
  Validate with `era_for_theatre(spec.theatre)`: Channel+Georgia or Channel+Su-25T
  is unknown; Caucasus+UK or Caucasus+Spitfire is unknown. Catalog listing may
  union eras; `list_countries(era="wwii")` stays UK / ThirdReich. Install harvest
  must map `Su-25T` → `CoreMods/aircraft/Su-25T` in `_AIRCRAFT_FOLDERS` or the
  catalog join emits a second discovered-only row with `known=False`.
- **Code:** `data/era/modern/`, `data/theatres/Caucasus/`, `registry.py`,
  `allowlists.py`, `validation.py`, `install/aircraft_modules.py`.

## Curated Normandy airfields; FordAF is not Ford_AF (2026-08-15)

- **Date:** 2026-08-15
- **Lesson:** Packaged Normandy airfields are eight curated keys from
  `Normandy.airport_list()`, not all 38 fields. Spec key **`FordAF`** = 31
  (PyDCS name **`Ford_AF`** — do not use the underscore in Spec YAML).
  `Maupertus` = 4 on Normandy is **not** Channel Abbeville (also id 4 on
  TheChannel). Lookup stays theatre-scoped. Keys: NeedsOarPoint 28, Chailey 27,
  Funtington 29, Tangmere 30, FordAF 31, Maupertus 4, SaintPierreduMont 1
  (PyDCS “Saint Pierre du Mont”), Carpiquet 19.
- **Code:** `data/theatres/Normandy/airfields.yaml`, `registry.airdrome_id`.

## Theatre-keyed intercept and domain (fail closed off TheChannel)

- **Date:** 2026-08-15
- **Lesson:** Land/sea domain classification is the Channel UK–FR airport chord only.
  Non-Channel Specs with strike/recon/path geometry fail
  `domain_unsupported_theatre` — do not run the chord on Normandy (x,y). Intercept
  enemy spawn is a recipe table with **only** TheChannel Hawkinge
  `26989.935547` / `-29402.577148` plus Dover `+4000` / `-6000` (golden
  `30989.935547` / `-35402.577148`). Do **not** recompute from `airport_list()`.
  Other theatres fail `intercept_unsupported_theatre`. Join-up outbound 120° stays
  generic airfield-relative. WWII countries live in `data/era/wwii/countries.yaml`
  (`UK`, `ThirdReich`); Germany is a hint, not a known id. `airfield_relative_map_point`
  must pass `theatre=spec.theatre` into `airdrome_id`.
- **Code:** `channel_domain.py`, `intercept_spawn.py`, `allowlists.py`,
  `data/era/wwii/countries.yaml`, `validation.py`, `compiler/pydcs_compiler.py`.

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
