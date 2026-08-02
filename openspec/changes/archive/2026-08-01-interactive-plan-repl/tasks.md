## 1. Session core and shared turn runner

- [x] 1.1 Extract shared “assistant turn + tool dispatch” helper from `plan_mission` for reuse by one-shot and chat
- [x] 1.2 Implement `PlanSession` (messages, voice/system prompt, draft Spec, db_path, IO hooks)
- [x] 1.3 Add chat-mode system prompt composition (clarify → propose → wait for `/accept`)

## 2. Slash commands and CLI

- [x] 2.1 Implement host slash commands: `/help`, `/quit`/`/exit`, `/show`, `/accept`, `/compile`, `/voice`, `/prefs`, `/clear`
- [x] 2.2 Gate Spec file write on `/accept` (validate, write YAML, record history, print brief); no auto-write on JSON alone
- [x] 2.3 Implement `/briefing` (commander brief from draft Spec via `build_commander_brief`; graceful if no draft)
- [x] 2.4 Implement `/research [query]` (host `research_guidance`, print notes, inject into session context; default query from draft when omitted)
- [x] 2.5 Implement `/catalog` (host catalog / `list_mission_options` summary; no LLM)
- [x] 2.6 Add `dcs-miz chat` CLI (`--stub`, `--voice`, `--db`, `-o`, optional compile-on-accept); leave `plan` unchanged

## 3. Stub, tests, docs

- [x] 3.1 Scripted multi-turn stub LLM for offline chat tests
- [x] 3.2 Pytest: clarifying exchange and/or tool use, then `/accept` writes valid Spec without API key; cover `/briefing`, `/research`, `/catalog`; one-shot `plan` still green
- [x] 3.3 Update README (how to chat + slash commands), ARCHITECTURE, BACKLOG; Ruff + pytest green

## 4. Acceptance

- [x] 4.1 Live chat CAP from Manston: Spec JSON captured after prompt shape fix; `/accept` wrote YAML (2026-08-01). Verbose default on; Luna rejected (reasoning_effort + tools on Chat Completions) — stay on `gpt-4o-mini` for now.
