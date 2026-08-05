## Context

Compiler ignores `spec.theatre` for PyDCS terrain construction. Zip `theatre` member is
written from Spec string, so ME can see the label while geometry is always Channel.

## Goals / Non-Goals

**Goals:** Single binding helper; fail-closed; Channel-only entry; parity test.

**Non-Goals:** Second theatre content; changing Manston geometry.

## Decisions

1. **`theatre_terrain.py`** (package-level, imported by compiler): map
   `"TheChannel"` → factory returning `dcs.terrain.TheChannel()` (lazy import inside
   factory to keep PyDCS boundary).
2. **`terrain_for_theatre(theatre_id)`** raises `TheatreTerrainError` with clear message.
3. **Validate:** after registry theatre check succeeds, require binding key present →
   `theatre_terrain_unbound` if missing (defense if YAML grows ahead of map).
4. **channel_domain** uses `terrain_for_theatre("TheChannel")` or `terrain_for_theatre(spec.theatre)`.

## Risks / Trade-offs

- [PyDCS import path churn] → Keep factory next to compiler boundary comments.
