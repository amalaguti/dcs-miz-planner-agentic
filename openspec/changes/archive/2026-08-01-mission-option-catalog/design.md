## Context

`list_mission_options` returns flat enum arrays. The user wants the agent to help build
mission content creatively but realistically — that needs labeled knobs with meaning and
honest support levels. Normandy/other maps are out of scope for compile here.

## Goals / Non-Goals

**Goals:**

- Curated option catalog (packaged YAML → SQLite on sync).
- Families useful for Channel free_flight + intercept planning.
- Clear `supported` / `advisory` / `future` so the agent does not lie.
- Tool + CLI visibility; tests with temp DB.

**Non-Goals:**

- Making Normandy offerable/compile-supported.
- Implementing new Spec fields for every future knob in this change.
- Prefs, voice, MCP.

## Decisions

1. **Source of truth for option *definitions***: packaged YAML (e.g.
   `data/channel/planning_options.yaml`), synced like other catalog rows — not hand-edited SQL.
2. **Support levels**
   - `supported`: value is a current Spec enum/id the compiler accepts.
   - `advisory`: helps choose an existing Spec field (e.g. time band → `start_time`).
   - `future`: listed for discovery/roadmap; agent must not emit as if compile-backed.
3. **v1 families (seed)**
   - mission_type, start_type, weather (supported from Spec/registry)
   - time_of_day bands (advisory → HH:MM suggestions)
   - opposition_density for intercept (advisory/future — count/skill hints only if Spec already has enemies.count)
   - payload_family (future/stub until payloads.yaml grows)
   - roe_seed (future)
4. **Normandy / extra DCS content**: **not required**. Install discovery may already show
   Normandy as known=false; this change does not promote it.
5. **API**: extend `list_mission_options` payload with `options: [{family, id, label,
   description, support, meta}]` while keeping legacy enum keys for compatibility (or
   deprecate gently in docs).

## Risks / Trade-offs

- [Agent uses future options in Spec] → Prompt + support field; validate still rejects unknown fields.
- [Catalog bloat] → Keep Channel-scoped seed small; grow deliberately.

## Migration Plan

1. YAML + schema sync + list enrichment + tests.
2. Accept via catalog list / tool JSON (no new DCS map required).
3. Later Spec/compiler changes promote `future` → `supported`.

## Open Questions

- Exact YAML shape — finalize at apply (keep flat rows: family, id, …).
