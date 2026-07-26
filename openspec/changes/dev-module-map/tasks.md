## 1. Architecture document

- [x] 1.1 Create `docs/ARCHITECTURE.md` with runtime Spec→`.miz` relationship diagram (Mermaid and/or ASCII)
- [x] 1.2 Add short repo-layout section (`src/`, `openspec/`, `.cursor/`, `examples/`, `tests/`, `research/`)
- [x] 1.3 Link from README Docs; keep README brief

## 2. Refresh reminder

- [x] 2.1 Add Cursor hook (or extend an existing push hook) reminding to update `docs/ARCHITECTURE.md` when pushing `src/dcs_miz_planner/` changes
- [x] 2.2 Wire hook in `.cursor/hooks.json`; note refresh policy in ARCHITECTURE and/or `keep-readme-updated` / finish-change skill

## 3. Backlog hygiene

- [x] 3.1 Mark `dev-module-map` `building` while applying, `done` when archived; set next promote back to `reference-registry-channel`
- [x] 3.2 Resolve pending decision “manual vs hook” as: manual doc + push reminder (no CI generator)
