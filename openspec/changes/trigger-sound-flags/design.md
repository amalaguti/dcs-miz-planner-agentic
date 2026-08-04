## Context

After `#25`, Specs can drive F10 menus and late-activated groups with bool flags.
Stock Channel IA still uses **SoundToAll** callouts and **numeric / timed flags** for
multi-step logic. PyDCS 0.15.0 already exposes `SoundToAll` (via `map_resource` embed),
`FlagEquals` / `FlagIsMore` / `FlagIsLess`, `TimeSinceFlag`, `IncreaseFlag`, and
`SetFlagValue`. Spec vocabulary and validation are the gap — not DCS capability.

## Goals / Non-Goals

**Goals:**

- Curated `sound` action (`asset_id` → checked-in file) embedded into `.miz` mapResource.
- Numeric flag conditions/actions + `time_since_flag` alongside existing bool flags.
- Example + validate/compile tests; ME shows SOUND TO ALL and numeric flag rules.

**Non-Goals:**

- `group_life_less`, altitude/speed, markers, coalition-targeted sound, narrative auto-VO.
- Arbitrary paths in Spec; Lua / Mist / MOOSE; changing `#25` radio/late-activation.

## Decisions

1. **`asset_id` only (no paths in Spec):** Spec action `sound: { asset_id: "beep" }`.
   A small YAML registry under `src/dcs_miz_planner/data/sounds/` maps id → relative
   `.ogg`/`.wav` path. Unknown ids fail validation. Alternative rejected: free paths
   (LLM unsafe / non-portable).

2. **Ship one sample asset:** At least `beep` (short tone) checked in so compile is
   hermetic without DCS install sounds. More VO ids can be added later without Spec
   schema changes.

3. **Emit `SoundToAll` only:** Coalition/group sound deferred. Compiler:
   `map_resource.add_resource_file(path)` → `SoundToAll(file_res_key=...)`.

4. **String flag names unchanged:** Continue mapping names → int ids as today. Bool
   `flag_is` / `set_flag` stay; numeric types are additive:
   - conditions: `flag_equals`, `flag_more`, `flag_less` (`flag` + `value: int`),
     `time_since_flag` (`flag` + `seconds`)
   - actions: `inc_flag` (`flag` + optional `by` default 1), `set_flag_value`
     (`flag` + `value`)

5. **Do not overload `flag_is`:** Keep bool semantics (`FlagIsTrue`/`False`). Avoids
   breaking existing Specs and radio menus.

6. **Example:** Free-flight or intercept sample with (a) `time_more` → `sound` +
   `message`, and (b) a small numeric-flag chain (e.g. `inc_flag` on event then
   `flag_more` → message/end) so ME acceptance covers both.

7. **Narrative packs unchanged:** New types are allowed in the supported vocabulary;
   packs do not auto-add sounds in this change.

## Risks / Trade-offs

- [Risk] Sample tone feels crude vs stock VO → Mitigation: registry designed for more
  assets; document that `beep` is a compile/ME fixture, not final immersion.
- [Risk] Authors mix bool `set_flag` and `set_flag_value` on same flag → Mitigation:
  docs note bool on/off vs numeric; validation does not forbid (DCS allows both).
- [Risk] Large binary assets in git → Mitigation: keep v1 sample tiny (short ogg/wav).

## Migration Plan

- Additive Spec types and registry. Rollback: ignore new action/condition types.

## Open Questions

- None blocking. Optional later: SoundToCoalition; wiring narrative beats to `asset_id`s.
