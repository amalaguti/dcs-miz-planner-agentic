## 1. Memory store

- [x] 1.1 Add `memory/` package: `UserMemoryStore` on `default_db_path()` with `user_meta`, `user_prefs`, `generation_history`, `satisfaction_feedback`
- [x] 1.2 Implement prefs get/upsert, history append/list, feedback insert; schema version that never wipes catalog/install
- [x] 1.3 Tests: round-trip prefs, history, feedback; catalog sync does not clear prefs

## 2. Tools and planner

- [x] 2.1 Expose `get_user_prefs`, `set_user_prefs`, `record_generation`, `record_feedback`, `list_generation_history` on tools surface + tool_bridge
- [x] 2.2 Host-record generation history from `plan_mission` on success/failure; nudge system prompt to consult prefs
- [x] 2.3 Tests: tool dicts, stub planner prefs tool + history row after success; Ruff clean

## 3. CLI and docs

- [x] 3.1 Optional CLI: `dcs-miz prefs` (list/set) and `dcs-miz feedback` (score/note)
- [x] 3.2 Update ARCHITECTURE / README / BACKLOG for user-memory layer
- [x] 3.3 Acceptance: prefs round-trip via tool/CLI; stub plan writes history
