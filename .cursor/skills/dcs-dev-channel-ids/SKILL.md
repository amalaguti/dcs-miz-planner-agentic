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
4. Intercept spawn geometry: packaged recipes in `intercept_spawn.py`.
   TheChannel: Hawkinge + Dover-approach offset. Do not recompute from
   `airport_list()`. Normandy: NeedsOarPoint + Cherbourg corridor
   (`-63000`, `0`) — same station as `cherbourg_channel_cap` (180°/63 km).
   Caucasus: Batumi + Black Sea corridor `(0, -40000)` — same station as
   `batumi_black_sea_cap` (270°/40 km). Other theatres fail
   `intercept_unsupported_theatre`.
5. Failure ids: exact stock strings (e.g. `ENG0_MAGNETO0`) from
   `data/era/wwii/aircraft_failures.yaml`.
6. **Normandy 2.0** Spec/inventory id is **`Normandy`**. Airfield lookup is
   theatre-scoped (`airdrome_id(name, theatre=)`); folder names under
   `data/theatres/` **are** Spec ids. Curated keys: `NeedsOarPoint` = 28,
   `Chailey` = 27, `Funtington` = 29, `Tangmere` = 30, `FordAF` = 31
   (PyDCS `Ford_AF`), `Maupertus` = 4, `SaintPierreduMont` = 1, `Carpiquet` = 19.
   Do not invent ids or dump all 38 fields.
7. Domain land/sea is TheChannel UK–FR chord, Normandy UK–Cotentin chord
   (NeedsOarPoint cluster vs Maupertus / SaintPierreduMont / Carpiquet),
   Caucasus west-of-coast seaward sector (coastal 22/24/18 vs inland
   23/25/29/31/28; heading 270°±45° from nearest coastal → sea), **or**
   Syria per-coastal seaward windows (coastal 16/21/6 vs inland 27/28/7/30/19;
   Incirlik 165–195°; Bassel/Beirut 225–315° those two fields only — never
   apply 270±45 to Incirlik). Other
   theatres fail `domain_unsupported_theatre`. `airfield_relative_map_point`
   MUST pass `theatre=spec.theatre`. Normandy inland strike from NeedsOarPoint
   is **180° / 133 km** (Maupertus is 180.22° / 125.29 km; 120 km is still sea).
   Caucasus inland strike from Batumi is **43° / 110 km** (Kutaisi is 43.14° /
   97.20 km; 100 km is near-field; CAP 270/40 is sea). Syria inland strike/recon from
   Incirlik is **121° / 200 km** (Aleppo is 121.13° / 185.00 km; 121/185 is
   near-field; CAP 180/40 is sea). Do not copy Manston
   125/76 or CAP 180/63 (sea) onto Cotentin land, do not copy CAP 270/40
   onto Caucasus GA, and do not copy CAP 180/40 onto Syria GA or recon.
8. Packaged WWII countries: `UK` and `ThirdReich` only (`data/era/wwii/countries.yaml`).
   Germany is a hint, not a known id in **any** era.
9. **Caucasus** Spec id is **`Caucasus`** (era `modern`). Curated AFs (8 of 21):
   `Batumi` = 22, `Kobuleti` = 24, `SenakiKolkhi` = 23 (PyDCS `Senaki-Kolkhi`),
   `Kutaisi` = 25, `TbilisiLochini` = 29 (`Tbilisi-Lochini`), `Vaziani` = 31,
   `SochiAdler` = 18 (`Sochi-Adler`), `Mozdok` = 28 (not NeedsOarPoint).
   Invent home: `Georgia` + `Su-25T` at **251.0 MHz** at Batumi.    Invent is
   **all six types** (CAP/intercept/escort 270° / 40 km
   west over the Black Sea — not Manston 135/25, not Cherbourg 180/63, not
   Hawkinge, not escort 120/55; GA/recon AOI 43° / 110 km inland past Kutaisi —
   not CAP 270/40).
   Modern trucks: `Ural-375`, `GAZ-66`, `ZIL-135` (not Channel `soft_vehicles`).
   Payload `su25t_2x_fab250` (FAB-250 on pylons 5 and 7). `Russia` is
   modern-only (PyDCS red default — do not place Russia on blue). Channel+Russia
   is unknown. CAP enemies: Russia + Su-25T (set `enemies[].country: Russia`;
   default is ThirdReich). **SpitfireLFMkIX is dual-era** (same 124.0 ref in wwii + modern)
   because DCS flies it on modern maps; Channel still rejects `Su-25T`. UK is
   dual-era. Catalog listing may union eras. Do not dump all 21 fields.
10. **Syria** Spec id is **`Syria`** (era `modern`). Curated AFs (8 of 59):
    `Incirlik` = 16, `RamatDavid` = 30 (`Ramat David`), `Damascus` = 7,
    `BeirutRaficHariri` = 6 (`Beirut-Rafic Hariri`), `Aleppo` = 27,
    `BasselAlAssad` = 21 (`Bassel Al-Assad`), `Palmyra` = 28 (not Mozdok,
    not NeedsOarPoint), `KingHusseinAirCollege` = 19. Do not dump 59 fields.
    Invent home: `Turkey` + `Su-25T` at **251.0 MHz** at Incirlik (all six types;
    CAP/intercept/escort 180° / 40 km south Iskenderun — not Cherbourg 180/63, not Batumi 270/40,
    not escort 120/55; GA/recon AOI 121° / 200 km inland past Aleppo — not CAP 180/40).
    Country **`Syria`** is modern-only (PyDCS red default — Palmyra smoke
    uses coalition red; GA trucks must set `targets[].country: Syria`). Theatre id `Syria` ≠ country `Syria`. Channel+country-Syria
    is unknown. Add Syria-the-country only to `era/modern` — never `era/wwii`.
    Spitfire is dual-era.
11. **Nevada** Spec id is **`Nevada`** (era `modern`). Curated AFs (8 of 17):
    `Nellis` = 4 (PyDCS name `Nellis`), `GroomLake` = 2 (`Groom Lake` / class
    `Groom_Lake` — Spec key MUST be `GroomLake`, not `Groom_Lake`; id 2 is
    not Falklands `MountPleasant` and not Channel `MervilleCalonne`),
    `Creech` = 1, `TonopahTestRange` = 18 (`Tonopah Test Range`),
    `NorthLasVegas` = 15 (`North Las Vegas`), `HendersonExecutive` = 8
    (`Henderson Executive`), `BoulderCity` = 6 (`Boulder City`),
    `Mesquite` = 13. Do not invent id 12 or dump all 17 fields. Nellis 4 is
    not Maupertus and not Dunkirk. Modern smoke: country `USA` (not `usaaf`,
    not Georgia, not Turkey), aircraft `Su-25T` at **251.0 MHz**. Invent home
    stays Nellis (free_flight only). Add USA only to `era/modern` next to
    Georgia and Turkey — never `era/wwii`. `usaaf` is voice only, not a
    country. Channel+USA/Su-25T is unknown. Spitfire is dual-era. UK is
    dual-era (wwii + modern).
12. **Falklands** Spec id is **`Falklands`** (product name South Atlantic;
    era `modern`). Curated AF: `MountPleasant` = 2 (PyDCS name
    `Mount Pleasant`; class `Mount_Pleasant`; do not dump 27 fields). Spec
    key MUST be `MountPleasant`, not `Mount_Pleasant` (same pitfall as
    Normandy `FordAF` ≠ `Ford_AF`). Modern smoke: country `UK` (keep UK in
    `era/wwii` as well), aircraft `Su-25T` at **251.0 MHz**. Spitfire is
    dual-era (same 124.0 in wwii + modern). Channel+UK still ok (wwii);
    Channel+Su-25T is unknown.

## Code touchpoints

`data/era/wwii/*.yaml`, `data/era/modern/*.yaml`, `data/shared/*.yaml`, `data/theatres/<SpecId>/`,
`registry.py`, `validation.py`, `channel_domain.py`, `intercept_spawn.py`,
spawn helpers in compiler.
