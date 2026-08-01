## Context

Install inventory and agent catalog already share
`%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite` with distinct table namespaces.
`catalog sync` replaces `catalog_*` only. The NL planner (`agent/planner.py`) uses tools
via `tool_bridge` but has no memory of the user. Backlog M3 `#8b` places prefs, history,
and satisfaction in this same DB family.

## Goals / Non-Goals

**Goals:**

- Durable local prefs (key → JSON value) the agent and CLI can read/write.
- Append-only generation history with outcome (`success` | `validation_failed` |
  `compile_failed` | similar).
- Satisfaction feedback rows optionally linked to a generation.
- Tools + optional CLI; planner consults prefs and records history.
- Schema versioning that never wipes catalog/install on bump.

**Non-Goals:**

- Squadron voice copy (`#11`); only an optional pref key for later.
- Learning models, cloud sync, multi-user auth, UI/MCP.
- Treating prefs as DCS-id SoT (validate/compile stay registry-backed).
- DCS-side post-flight telemetry hooks.

## Decisions

1. **Module layout:** `src/dcs_miz_planner/memory/` with `store.py` + `service.py`
   (mirror `catalog/` / `install/`). Same `default_db_path()`; no second DB file in v1.
2. **Table namespace:** `user_meta`, `user_prefs`, `generation_history`,
   `satisfaction_feedback`. Never named `catalog_*` (those wipe on sync/schema bump).
3. **Schema version:** `user_meta.user_schema_version` (start at `1`). On mismatch,
   migrate or recreate **only** user_* tables — leave install + catalog untouched.
4. **Prefs model:** sparse key/value JSON (`preferred_aircraft`, `preferred_airfield`,
   `preferred_start_type`, `preferred_weather`, `squadron_voice`, …). Unknown keys allowed
   for forward compatibility; documented seed keys in service constants.
5. **Tools (import surface):**
   - `get_user_prefs` → all prefs (or filtered keys)
   - `set_user_prefs` → merge/upsert keys
   - `record_generation` → insert history row (host also auto-calls after plan)
   - `record_feedback` → insert feedback (optional `generation_id`)
   - `list_generation_history` → recent N rows (for agent “like last time”)
6. **Planner hooks:**
   - Prompt nudge: call `get_user_prefs` early; prefer prefs when the user left a knob
     unspecified; never override an explicit user request.
   - On plan success/failure after validate (and compile if requested), host records
     history — do not rely solely on the LLM calling `record_generation`.
7. **CLI:** thin `dcs-miz prefs` (list/set) and `dcs-miz feedback` (score/note); history
   listable via prefs/history subcommand or JSON flag. No `dcs-miz tools` CLI.
8. **Secrets:** never store API keys in SQLite (already env-only for live LLM).

## Risks / Trade-offs

- [Stale prefs point at removed airfields] → Tools return prefs as-is; validate still
  rejects bad Specs; agent should re-check with catalog tools.
- [LLM forgets to read prefs] → Prompt + optional host injection of prefs summary into
  the first user/system context (design preference: tool first, inject if tests show
  stub/live skips the tool).
- [History PII in prompts] → Truncate long prompts in stored rows; no cloud upload.
- [Schema bump wipes user data] → Prefer additive migrations; document wipe only if
  unavoidable and only for user_* tables.

## Migration Plan

1. Implement memory store/service + tests on temp DB.
2. Wire tools + bridge + planner recording + prompt nudge.
3. Optional CLI; update ARCHITECTURE/README/BACKLOG.
4. Existing DBs gain tables on first open (CREATE IF NOT EXISTS).

## Open Questions

- Exact seed pref keys — finalize at apply (keep small: aircraft, airfield, start_type,
  weather, voice).
- Whether host injects prefs into the system message vs tool-only — prefer tool-only
  unless stub tests need injection.
