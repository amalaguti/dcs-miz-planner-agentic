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
4. Intercept spawn geometry: Hawkinge anchor + Dover-approach offset (existing helpers).
5. Failure ids: exact stock strings (e.g. `ENG0_MAGNETO0`) from
   `data/channel/aircraft_failures.yaml`.

## Code touchpoints

`data/channel/*.yaml`, `registry.py`, `validation.py`, spawn helpers in compiler.
