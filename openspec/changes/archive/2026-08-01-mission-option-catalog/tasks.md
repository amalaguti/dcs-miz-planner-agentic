## 1. Option definitions and sync

- [x] 1.1 Add packaged planning-options YAML (Channel families + support levels)
- [x] 1.2 Extend catalog schema/sync/load for planning option rows
- [x] 1.3 CLI catalog list support for planning options (filter by family/support if cheap)

## 2. Agent surface

- [x] 2.1 Enrich `list_mission_options` with structured options + keep useful legacy keys
- [x] 2.2 Nudge agent system prompt to consult options and respect support levels
- [x] 2.3 Tests: sync, list, tool payload; Ruff clean

## 3. Docs

- [x] 3.1 Update ARCHITECTURE / README / BACKLOG; note Normandy not required for this change
- [x] 3.2 Acceptance: catalog/tool list shows supported + advisory (+ labeled future) options
