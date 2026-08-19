## Context

Group `frequency` 124 MHz is already assigned by plain attribute write
(`group.frequency = radio_mhz`). Stock Channel Instant Action
`SPIT-Channel-Cold Start.miz` (2026-08-19) has `radioSet = false` and unit:

```
Radio[1].channels = { 1=124, 2=40, 3=41, 4=42, 5=108.9 }
```

PyDCS `SpitfireLFMkIX.panel_radio` defaults are `{1:105, 2:124, 3:131, 4:139, 5:108.9}`.
`FlyingGroup.set_frequency()` sets `radio_set = True` and clobbers channel 1 —
do not use it.

Current compiles often omit the unit `Radio` table entirely because skill is
assigned without `set_player()` / `set_radio_preset()`.

## Goals / Non-Goals

**Goals:** Channel-accurate A–E on every emitted Spitfire LF Mk IX / CW group
(player and AI); keep group frequency 124 and `radioSet=false`.

**Non-Goals:** other airframes; F10 menus; Lua; Instant Action merge gate.

## Decisions

1. **YAML is SoT after stock copy.** `radio_channels_mhz: [124.0, 40.0, 41.0, 42.0, 108.9]`
   on both Spitfire ids. Channel A MUST equal `radio_mhz`.
2. **Init then overwrite.** If `unit.radio is None`, call `set_radio_preset()`,
   then `set_radio_channel_preset(1, n, mhz)` for n=1..5. Never `set_frequency()`.
3. **All Spitfire groups we emit**, including AI lead/wingmen. Enemies without a
   packaged bank keep frequency-only.
4. **Goldens** pick up the new `Radio` tables; contracts stay `["frequency"]=124.0`
   plus channel numbers.

## Risks / Trade-offs

- [PyDCS dump uses 124.0 vs stock 124] → tests accept either; DCS tunes both.
- [set_radio_preset copies wrong defaults] → overwrite all five channels.
- [radioSet flips true] → never call set_frequency(); assert radioSet false.
