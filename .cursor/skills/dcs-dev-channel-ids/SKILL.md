---
name: dcs-dev-channel-ids
description: >-
  Channel / WWII DCS identity strings that must never be invented. Use when
  adding aircraft, countries, airfields, radio frequencies, spawn geometry, or
  validating Spec ids against the Channel registry.
---

# Channel / WWII identity strings

## Read first

[`docs/lessons/channel-ids.md`](../../../docs/lessons/channel-ids.md)

## Hard rules

1. **Never invent** DCS type ids, country names, airfield names, CLSID, failure ids.
   Source = packaged YAML / registry / stock `.miz` research.
2. **WWII Axis country:** `ThirdReich`, not `Germany`.
3. **Spitfire group frequency** must be in **VHF** band (e.g. 124.0) — not HF defaults.
4. Intercept spawn geometry: packaged TheChannel Hawkinge + Dover-approach
   offset only (`intercept_spawn.py`). Do not recompute from `airport_list()`.
   Other theatres fail `intercept_unsupported_theatre`.
5. Failure ids: exact stock strings (e.g. `ENG0_MAGNETO0`) from
   `data/era/wwii/aircraft_failures.yaml`.
6. **Normandy 2.0** Spec/inventory id is **`Normandy`**. Airfield lookup is
   theatre-scoped (`airdrome_id(name, theatre=)`); folder names under
   `data/theatres/` **are** Spec ids. Curated keys: `NeedsOarPoint` = 28,
   `Chailey` = 27, `Funtington` = 29, `Tangmere` = 30, `FordAF` = 31
   (PyDCS `Ford_AF`), `Maupertus` = 4, `SaintPierreduMont` = 1, `Carpiquet` = 19.
   Do not invent ids or dump all 38 fields.
7. Domain land/sea is TheChannel UK–FR chord only. Non-Channel strike/recon/path
   → `domain_unsupported_theatre`. `airfield_relative_map_point` MUST pass
   `theatre=spec.theatre`.
8. Packaged WWII countries: `UK` and `ThirdReich` only (`data/era/wwii/countries.yaml`).
   Germany is a hint, not a known id in **any** era.
9. **Caucasus** Spec id is **`Caucasus`** (era `modern`). Curated AF: `Batumi` = 22
   (PyDCS name `Batumi`; do not dump 21 fields). Modern smoke: country `Georgia`
   (not USAF), aircraft `Su-25T` at **251.0 MHz** (modern UHF default — not
   Spitfire 124, not Batumi ATC). Validate countries/aircraft with
   `era_for_theatre(spec.theatre)` — Channel+Georgia/Su-25T and
   Caucasus+UK/Spitfire are unknown. Catalog listing may union eras.

## Code touchpoints

`data/era/wwii/*.yaml`, `data/era/modern/*.yaml`, `data/shared/*.yaml`, `data/theatres/<SpecId>/`,
`registry.py`, `validation.py`, `channel_domain.py`, `intercept_spawn.py`,
spawn helpers in compiler.
