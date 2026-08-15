## Context

Packaged SoT is a single `data/channel/` tree. `theatres.yaml` lists
`TheChannel` and `Normandy`; `airfields.yaml` is a flat Spec-key → airdromeId
map with `airfield_theatres:` only for `NeedsOarPoint`. `registry.py` loads
`importlib.resources.files("dcs_miz_planner.data.channel")` with no merge.
`airdrome_id(name)` is unscoped. Validate/compile can resolve Channel
`Manston=5` on a Normandy Spec. Archived `normandy-cold-freeflight` deferred
this split.

PyDCS binds stay in `theatre_terrain.py` (`TheChannel`, `Normandy` — not
`Normandy2`). Hatch already force-includes the whole `data/` tree.

## Goals / Non-Goals

**Goals:**

- Split YAML into era + shared + per-theatre packages; delete `data/channel/`.
- Walker loader merges packages. Airfield lookup is theatre-scoped.
- Re-home existing verified ids only. Channel goldens + Needs Oar Point smoke
  stay green.

**Non-Goals:**

- Slice 0b Channel helpers (invent, countries YAML, domain, intercept spawn,
  path clamp, strike-unit tags, reweather/METAR).
- New AFs, places, units, theatres, Stage C combat.
- Bind terrains without PyDCS modules.
- Mass-rename `ChannelRegistry` / `get_channel_registry()`.

## Decisions

1. **Folder names are Spec ids:** `data/theatres/TheChannel/`,
   `data/theatres/Normandy/`.
   *Alt:* slugs `channel` / `normandy` — rejected; needs a folder→id map and
   invites Caucasus/Falklands slug bugs.
   Loader reads `theatre.yaml` `id:` (do not trust `os.listdir` casing) and
   fails if `id` ≠ folder name.

2. **No `countries.yaml` this slice.** `UK` / `ThirdReich` stay in
   `allowlists.KNOWN_COUNTRIES` and catalog sync. *Alt:* new YAML now —
   rejected; two SoTs until validation/invent move (0b).

3. **Entire `weather_presets.yaml` in `data/shared/`.** No Channel climatology
   split. `sunny_clear` (and the rest of the Spec enum) stays one file so
   Normandy smoke needs no Normandy weather YAML. `weather_gallery.yaml` and
   whole `planning_options.yaml` (including `channel_place`) live in `shared/`.
   *Alt:* split Channel-named presets — rejected; goldens and weather SoT
   parity would need a Normandy weather file we will not invent.

4. **Keep `ChannelRegistry` / `get_channel_registry()`.** Add
   `from_packaged_packages()` as the real loader; `from_packaged_yaml()` is an
   alias. Keep the test constructor (`airfields=` + optional
   `airfield_theatres=`; unlisted keys default `TheChannel` if that theatre is
   in the set). *Alt:* mass-rename — rejected; too many call sites for Slice 0.

5. **Layout**

   ```
   data/era/wwii/     aircraft, failures, payloads, ground_units, ships, target_motion
   data/shared/       weather_presets, weather_gallery, planning_options
   data/theatres/TheChannel/{theatre.yaml, airfields.yaml}  # 12 Channel keys
   data/theatres/Normandy/{theatre.yaml, airfields.yaml}    # NeedsOarPoint: 28
   ```

   Delete `theatres.yaml` and `airfield_theatres:`. `theatre.yaml` minimum:
   `id:` (exact Spec/PyDCS id) and `era: wwii`. Do not put PyDCS class paths
   in YAML.

6. **Merge / lookup**

   Load era maps, then shared weather + planning_options, then walk
   `theatres/*/theatre.yaml`. Each theatre’s `airfields.yaml` →
   `_airfields_by_theatre[id][name]`. Fail closed: missing `theatre.yaml`,
   `id` ≠ folder, unknown `era`, duplicate name inside one theatre, empty
   airfields, non-mapping YAML. Same Spec name in two theatres is allowed
   later; unscoped lookup of an ambiguous name MUST fail.

   `airdrome_id(name, theatre: str | None = None)`: theatre set → that map
   only; omitted → unique-name fallback (keeps `_tiny_registry` /
   `test_manston_airdrome_id`). Validate, compile, and `reference.py` MUST
   pass `spec.theatre`. Soften `"Unknown Channel airfield"` →
   `"Unknown airfield"`.

7. **Leave 0b tags.** Catalog `SOURCE_LABEL` and strike-unit
   `theatre_id="TheChannel"` stay. `target_motion.py` loads
   `data/era/wwii/target_motion.yaml`. `weather_gallery.py` loads
   `data/shared/weather_gallery.yaml`. Drop unused flat
   `CHANNEL_AIRDROME_IDS` dump in `reference.py` (restrict to TheChannel or
   remove).

## Risks / Trade-offs

- [Wrong-theatre airdrome] Channel `Manston=5` on Normandy terrain → Mitigation:
  scoped lookup + validate/compile pass `spec.theatre`; tests for Manston on
  Normandy raise.
- [Windows folder casing] `TheChannel` vs `thechannel` → Mitigation: `id:` from
  YAML is SoT; fail if it disagrees with folder name.
- [Duplicate airfield names later] unscoped lookup becomes ambiguous →
  Mitigation: fail and require `theatre=`.
- [Invent still Channel-only] NL will not propose Normandy → Mitigation:
  documented 0b; hand Specs + smoke tests still work.
- [Planning options stay Channel-flavored in shared/] `channel_place` is not
  extracted → Mitigation: no Normandy places this slice; extract in 0b / F1.

## Migration Plan

One PR on branch `theatre-registry-packages`. Move YAML, switch loader, update
call sites, delete `data/channel/`. Rollback = revert the PR. No SQLite schema
migration; `catalog sync` re-reads packaged YAML. ME Instant Action on Manston
and Needs Oar Point is human do-soon after merge.

## Open Questions

- None blocking. Slice 0b unhardcodes invent/domain/countries/strike tags.
