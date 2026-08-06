## Context

R10 scanned 60 Spitfire campaign `.miz` files: most use static weather +
`clouds.preset` (`Preset1`…`RainyPreset3`). PyDCS 0.15 supports
`Weather.clouds_preset = CloudPreset.by_name(...)` with per-preset base clamps.
Our compiler still clears `clouds_preset` and only sets density/thickness/fog.

## Goals / Non-Goals

**Goals:** Named Spec weather patterns with gallery recipes; SoT parity; compile
smoke; randomize/agent can pick them; keep trio Specs valid.

**Non-Goals:** Mid-mission cloud/rain changes; fog animation (`#17c`); dynamic
weather; free-form weather JSON from the LLM.

## Decisions

1. **Recipe in YAML** — each preset row gains optional `cloud_preset` (ME id) plus
   numeric defaults (`clouds_base_m`, fog, visibility, temp, qnh, turb, ground wind).
   Registry loads them; compiler maps to PyDCS. Keeps SoT in one file.

2. **Initial new patterns (campaign-seeded)** — at least:
   - `light_scattered_vfr` → Preset1
   - `high_scattered` → Preset3
   - `broken_channel` → Preset14
   - `overcast_low` → Preset22
   - `rain_overcast` → RainyPreset1
   - `scattered_summer` → Preset9
   Keep `sunny_clear` / `dawn_clear` / `marginal_vfr` (legacy density path or light
   gallery migration if tests stay green).

3. **Clamp base** — if `cloud_preset` set, clamp `clouds_base` into
   `CloudPreset.min_base`…`max_base` before save.

4. **Precip** — gallery rain presets usually leave `iprecptns=0` in campaigns; set
   `Preceptions.None_` unless recipe explicitly requests rain/thunderstorm (legacy).

5. **Randomize** — weather axis chooses uniformly among all enum values (existing
   behaviour once enum grows). Optional mild jitter deferred unless cheap.

6. **`#17c`** stays separate (fog animation snippets).

## Risks / Trade-offs

- [Risk] Golden Manston fixtures embed weather → refresh if trio emit changes
- [Risk] PyDCS missing newer Light Rain presets → only ship ids in `cloud_presets`
- [Risk] Wind units m/s in `.miz` vs kt in ME UI → store m/s matching campaign dumps

## Migration Plan

- Additive enum values; old Specs unchanged.
- Catalog sync picks up planning_options rows.
- Rollback: remove new ids + recipe fields; restore density-only apply.
