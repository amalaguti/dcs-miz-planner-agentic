## Why

Adding theatres or strike/recon units by dumping ME trees into YAML has already
caused wrong assumptions (catalog ≠ full ME; era mismatch; domain pitfalls).
After `#8c`/`#8d`/`#8f`/`#8g`, invent can use shelves safely — growth must stay
curated. We need a durable human/agent checklist so every promote batch follows
the same path (research → YAML → class/AI/motion → catalog → invent cues →
accept → docs).

## What Changes

- Add a checked-in promote checklist document covering (A) new theatre/map slice
  and (B) new strike/recon target units.
- Link it from README Docs (and/or ARCHITECTURE) and LESSONS / agent skill
  pointers so agents find it before shelf expand.
- OpenSpec: require the checklist exists (dev-docs / agent-catalog / reference
  registry as appropriate); no auto-scrape behaviour.
- Flip BACKLOG `#8e` idea→done when the checklist is accepted (docs accept;
  ME not required). First unit-batch expand is a **follow-on** OpenSpec change
  that *uses* this checklist.

## Capabilities

### New Capabilities

- *(none)*

### Modified Capabilities

- `dev-docs`: durable promote checklist location and refresh guidance.
- `agent-catalog`: promote path for strike units / theatres points at checklist
  (no discovery auto-promote).
- `golden-fixtures`: hermetic assert that the checklist file exists / key
  sections present.

## Impact

- New `docs/` checklist (path TBD in design), README/ARCHITECTURE links,
  BACKLOG `#8e`, optional `.cursor/skills/dcs-dev-agent-tooling` Hard rule link.
- No runtime invent/compile behaviour change.

## Non-goals

- Scraping full ME unit trees into the catalog.
- Auto-promoting discovered install folders into known YAML.
- Shipping a large armor/troops/sea shelf batch in this change (follow-on).
- Multi-theatre invent allow-list expansion beyond documenting how to do it.

## Acceptance

Checklist checked in with A (theatre) and B (units) sections matching the
BACKLOG draft intent; linked from Docs; specs/tests pin presence; BACKLOG
`#8e` done. Hermetic only (no ME).
