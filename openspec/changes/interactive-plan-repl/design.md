## Context

`plan_mission` today is a single user prompt → tool loop → Spec JSON → validate → YAML
(optional compile). Message history is discarded after the run. Users want to start with
no Spec, talk as with a squadron CO, refine, then accept. One-shot `plan` must stay for
scripts/CI.

## Goals / Non-Goals

**Goals:**

- CLI stdin/stdout multi-turn session with persistent in-process message history.
- Same tools, voice resolution, prefs, validation, and compile paths as one-shot plan.
- Explicit Spec accept (slash command and/or confirmed Spec emission) before write.
- Stub/scripted multi-turn tests without live API.

**Non-Goals:**

- GUI/TUI libraries; durable session files across process restarts (optional later).
- New mission types or Spec schema changes.
- Deprecating `dcs-miz plan`.

## Decisions

1. **CLI: `dcs-miz chat`**
   - Dedicated subcommand (not overloading `plan`). Flags: `--voice`, `--db`, `--stub`,
     optional `-o` default Spec path, optional `--compile` as default-on-accept behaviour.
   - Alternative rejected: only `plan --interactive` — harder to discover; keep `plan` pure.

2. **Session object (`PlanSession` / similar)**
   - Holds: `messages[]`, resolved `voice` + system prompt, `db_path`, optional draft
     `MissionSpec | None`, last validation errors, `UserMemoryService` handle.
   - Each user turn: append user message → run tool-capable LLM turn(s) until assistant
     text (no pending tool calls) → print commander reply to stdout.
   - Spec JSON in assistant content does **not** auto-write; host detects candidate Spec
     and offers accept, or user runs `/accept` after the model proposes one.

3. **Slash commands (host-side, not LLM)**
   - Core: `/help`, `/quit` (`/exit`), `/voice <id>`, `/prefs` (show), `/show` (draft Spec
     YAML or “none yet”), `/accept` (validate + write Spec; record generation; print brief),
     `/compile` (accept if needed then compile), `/clear` (reset messages + draft; keep
     voice/prefs).
   - **`/briefing`**: Host prints a commander-style operational brief for the **current draft
     Spec** via `build_commander_brief` (same sections as plan accept). If no draft yet,
     print a short message to propose/accept a Spec first — do not invent a Spec.
   - **`/research [query…]`**: Host runs `research_guidance` (fixtures offline; live when
     `DCS_MIZ_RESEARCH_LIVE` / flag enables it). Query defaults from draft mission type /
     theatre / aircraft when omitted. Print notes to stdout and inject a concise research
     summary into session history so later chat turns can use it. Research is not Spec or
     DCS-id authority.
   - **`/catalog`**: Host prints a readable summary of the local agent catalog (offerable
     theatres, known aircraft, planning options by family/support) via existing catalog /
     `list_mission_options` APIs — no LLM. Optional args later (`/catalog aircraft`); v1
     may print a compact full summary or family sections.
   - Unknown `/…` → short help. Lines without leading `/` go to the LLM.

4. **Conversational system prompt**
   - Extend compose path with a **chat mode** pack: ask clarifying questions, propose
     options, do not dump Spec until the pilot is ready; when proposing a Spec, emit a
     single JSON object (same contract as one-shot) and tell the user to `/accept`.
   - Reuse persona packs + ops-brief rules; brief on `/accept` and on `/briefing` uses
     host-side `build_commander_brief` (not free-form-only LLM prose as the sole brief).

5. **Stub for CI**
   - Scripted stub LLM that returns canned assistant turns / tool calls by turn index
     (or by matching last user content). Pytest drives `PlanSession` with a fake
     `input()` sequence (injectable IO), asserts Spec written after `/accept`.

6. **EOF / interrupt**
   - Ctrl+D / EOF exits cleanly (no write unless already accepted). Ctrl+C cancels
     current turn or exits with message — design pick: exit session with note.

## Risks / Trade-offs

- [Long contexts / cost] → Soft max turns or truncate older tool payloads later; v1
  document practical session length; no hard product limit required.
- [Model dumps Spec early] → Prompt + host gate: no file write without `/accept` (or
  explicit confirm if we add “accept this Spec? [y/N]” when JSON detected).
- [Duplicate logic with `plan_mission`] → Extract shared “run assistant turn with tools”
  helper used by one-shot and REPL; avoid two tool loops.
- [Windows console encoding] → UTF-8 stdout best-effort; ASCII-safe slash help.

## Migration Plan

1. Extract shared turn runner from `planner.py` if needed.
2. Implement `PlanSession` + slash commands + `dcs-miz chat`.
3. Chat-mode prompt composition; stub + pytest.
4. README / BACKLOG; one-shot `plan` unchanged.

## Open Questions

- Confirm prompt vs confirm on detected Spec JSON: prefer `/accept` only for v1 (simpler);
  optional `y/N` can land if apply finds UX too stiff.
- Session transcript save to disk: defer unless apply needs it for debugging.
