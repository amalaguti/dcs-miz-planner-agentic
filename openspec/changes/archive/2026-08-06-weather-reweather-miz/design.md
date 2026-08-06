## Context

`#17a`/`#17e` produce invent weather snapshots applied at compile. Users accepted
overwrite re-weather + Spec sidecar YAML. PyDCS exposes `Mission.load_file` /
`save`.

## Goals / Non-Goals

**Goals:**

- One API: path(s) + weather pattern (+ optional seed) → overwrite `.miz`
- Spec-first when sibling `.yaml`/`.yml` exists; else patch weather table only
- New seed by default when pattern changes (re-roll invent day)
- CLI + agent tool

**Non-Goals:** Mid-flight; Dynamic weather; non-overwrite outputs

## Decisions

1. **Entry:** `reweather_mission(miz_path, weather, *, seed=None, spec_path=None,
   voice=None) -> dict` returning paths written and mode (`spec_recompile` |
   `miz_patch`).
2. **Sidecar discovery:** same directory, same stem as `.miz` with `.yaml` or
   `.yml`; explicit `spec_path` wins.
3. **Spec path:** load Spec → set `weather` → `ensure_weather_seed(..., draw=True)`
   unless seed provided → `write_spec_yaml` → `PyDCSCompiler.compile` to the
   `.miz` path (overwrite).
4. **Miz-only path:** build a minimal weather context (pattern + seed + default
   Channel date/time from loaded mission start if available, else fixed defaults)
   → `resolve_weather_snapshot` → apply to loaded mission weather → save.
   Theatre must be loadable; fail clearly if load fails.
5. **Apply helper:** extract `apply_weather_snapshot(mission, snapshot)` used by
   compiler and re-weather (single SoT).
6. **Briefing:** Spec recompile refreshes l10n via existing briefing path.
   Miz-only: best-effort skip or light description note — do not invent Lua.

## Risks / Trade-offs

- [Risk] ME has file open → save fails / stale view → document reload
- [Risk] Miz-only lacks full Spec date → weaker season priors → prefer sidecar
- [Risk] Full recompile resets ME hand-edits → accepted for Spec path

## Migration Plan

- Additive CLI/tool; rollback by unused

## Open Questions

- None blocking (overwrite + sidecar + new seed decided)
