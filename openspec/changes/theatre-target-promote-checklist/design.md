## Context

BACKLOG `#8e` already drafts theatre + unit promote steps. Catalog sync
(`#8c`) and invent heuristics (`#8d`–`#8g`) assume curated YAML. Agents still
need a single durable doc — not only a BACKLOG draft — before expanding shelves.

## Goals / Non-Goals

**Goals:**

- One checked-in checklist for theatre slices and target-unit promotes.
- Specs/tests require it; README/ARCHITECTURE/skill link to it.
- Clear hand-off: next OpenSpec change expands Channel units *using* the list.

**Non-Goals:** Implementing a unit batch; ME scrape; auto-promote discovery.

## Decisions

1. **Path:** `docs/THEATRE_TARGET_PROMOTE.md` — peer to ARCHITECTURE/LESSONS;
   BACKLOG keeps a short pointer, not the full checklist text (avoid drift:
   checklist is SoT; BACKLOG summary may slim after ship).

2. **Content:** Sections A (new theatre) and B (new units) from BACKLOG draft,
   plus Explicit non-goals, and a short “first Channel expand candidates”
   pointer table (class spine) without claiming those units are shipped.

3. **Agent discovery:** Link from README Docs; Hard rule in
   `dcs-dev-agent-tooling` (and/or `keep-lessons-learned` index row) to read
   the checklist before registry/shelf edits.

4. **Specs:** `dev-docs` owns “document exists”; `agent-catalog` references it
   for the documented promote path (strike units + theatres); hermetic test
   asserts key headings.

5. **No code path changes** — process only.

## Risks / Trade-offs

- [Checklist drifts from practice] → Keep short; update when a promote batch
  reveals a missing step (LESSONS + checklist same PR).
- [Confusion with shelf-expand change] → Proposal/acceptance state checklist-
  only; next change named for the unit batch.

## Migration Plan

- Additive docs + links; slim BACKLOG `#8e` draft into “see docs/…” after ship.

## Open Questions

- None — first unit batch scope (armor vs sea expand) deferred to follow-on.
