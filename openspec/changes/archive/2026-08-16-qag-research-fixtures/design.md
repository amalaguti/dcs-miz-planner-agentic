## Context

`research_guidance` offline path is `fixture_notes()` in `tools/research.py`: three
hard-coded Channel/Spitfire lists. Live DuckDuckGo cascade is unchanged.

The user added eight QAG educational HTML pages under gitignored `research/DCS *`
(~15–22 KB each). They document Quick Action Generator era filters and class names.
Those pages are a **local research source** for planning, not product data to ship.
Labels are **not** PyDCS/`vehicle_map` keys. Catalog promote still requires
`docs/THEATRE_TARGET_PROMOTE.md` §B.

## Goals / Non-Goals

**Goals:**

- Index seven real QAG HTML pages via a thin packaged YAML map (skip the Cold War
  anti-ship file that is a copy of the WWII anti-ship page).
- Offline `research_guidance` reads matching snippets from local `research/` when
  the dump exists (`fixture:qag:<id>`) plus existing canned notes.
- Match on query, Spec `mission_type`, optional theatre, and `focus=mission_design`.
- Agent prompts state QAG labels ≠ Spec ids and QAG types ≠ new Spec mission types.

**Non-Goals:**

- Auto-promote into `ground_units.yaml` / `ships.yaml` / `planning_options.yaml`.
- New Spec types (SEAD, Anti-Ship SR, Dogfight) or a `cold_war` era package.
- Copying or committing the HTML into the package.
- Live-web provider changes.

## Decisions

1. **Local dump is the source; package only the index**
   YAML `qag_index.yaml` lists `id`, `html` (path relative to `research/`),
   `qag_era`, `qag_types`, `spec_mission_types`, `theatres`, `keywords`, `enabled`.
   Runtime resolves `research/` from `DCS_MIZ_RESEARCH_DIR` or by walking from cwd.
   Missing dump → no QAG notes (CI-safe).
   **Why:** user provided the HTML as research/planning source, not to ship.
   **Alt:** copy HTML into `data/` — rejected.

2. **Index + extract, do not dump tables**
   Stdlib `HTMLParser`: title/`h1`, lead paragraph, warn notes, up to ~8 `<code>`
   labels. Every QAG snippet MUST say QAG UI names are not Spec/PyDCS ids.
   Cap via existing 600-char sanitize. At most three QAG notes per call.
   **Why:** full tables look like catalog keys and would invite auto-promote.

3. **Match, do not always attach**
   Score: `mission_type` ∈ `spec_mission_types`; query/keyword overlap; theatre
   in `theatres` when provided. `focus=mission_design` raises QAG rank.
   SEAD snippet MUST say the planner has no SEAD Spec type.

4. **Skip duplicate Cold War anti-ship**
   Index row `enabled: false` with `skip_reason`.

5. **Keep canned Channel notes**
   Merge: matching QAG notes (if dump present) + existing canned set.

6. **No new dependencies**
   `html.parser` + PyYAML. Tests use stub HTML under `tmp_path`, not the dump.

## Risks / Trade-offs

- **[Risk] LLM copies QAG `code` names into Spec `unit_id`** → Mitigation:
  disclaimer in every snippet; nl-agent prompt; existing validate unknown-id.
- **[Risk] CI / wheel has no `research/`** → Mitigation: empty QAG notes; canned
  fixtures remain; pytest stubs the dump.
- **[Risk] Folder name drift (em-dash vs hyphen)** → Mitigation: index stores
  exact relative paths; missing file skips that page.
- **[Trade-off] Local-only colour** → Accept; that is the point of gitignored
  research.

## Migration Plan

- Thin index + loader; delete any packaged HTML copies; tests; docs.
- Rollback: revert the change branch; research behaviour returns to canned-only.

## Open Questions

- None for this slice. A later OpenSpec may promote verified PyDCS ids from
  these pages via `#8e` (artillery class still empty).
