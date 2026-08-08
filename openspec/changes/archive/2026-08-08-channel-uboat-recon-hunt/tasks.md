## 1. Examples and geometry

- [x] 1.1 Choose mid-Channel Manston-relative bearing/distance that validates as **sea**
      domain; confirm `Uboat_VIIC` via registry + PyDCS `ship_map`
      (140° / 40 km; same corridor as GA ship tests)
- [x] 1.2 Add `examples/manston_uboat_recon.yaml` (recon AOI + `Uboat_VIIC` contacts; no
      payload; `recon_area`)
- [x] 1.3 Add `examples/manston_uboat_hunt.yaml` (GA strike + `Uboat_VIIC` + bomb payload +
      `attack_ground`)
- [x] 1.4 Unit/compile tests: both examples validate; `.miz` contains `Uboat_VIIC`; recon
      has no bomb CLSIDs; hunt has bomb CLSIDs

## 2. Catalog, agent, voice

- [x] 2.1 Add `mission_inspiration` for surfaced U-boat locate/hunt; extend
      `mid_channel_shipping` to include `recon`
- [x] 2.2 Schema / prompts: surfaced-only U-boat guidance; forbid ASW invention
- [x] 2.3 Commander brief branch (or target-type hint) for `Uboat_VIIC` Specs

## 3. Goldens, docs, acceptance

- [x] 3.1 Golden fixtures (or shared compile asserts) for both examples
      (`tests/test_uboat_recon_hunt.py` compile asserts)
- [x] 3.2 Update README / ARCHITECTURE / BACKLOG `#15f` building→done when accepted;
      LESSONS only if geometry/domain pitfall is non-obvious
- [x] 3.3 Ruff + full pytest green
- [x] 3.4 In-game accept: ME / Instant Action both `.miz` — surfaced U-boat in water AOI /
      strike; recon find beat; GA loadout (accepted 2026-08-08)
