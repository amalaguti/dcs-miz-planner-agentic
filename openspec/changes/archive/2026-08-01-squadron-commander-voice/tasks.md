## 1. Voice packs and resolution

- [x] 1.1 Add `agent/voice.py` with voice ids (`raf`, `usaaf`, `neutral`), alias normalization, `resolve_voice`, and curated persona pack text (commander framing + period jargon/slang + ops-brief guidance; Spec fields stay plain)
- [x] 1.2 Refactor `prompts.py` so `compose_system_prompt(voice)` builds base planning rules + selected pack + tactics/procedures/watch-outs brief instructions; keep exports stable for callers
- [x] 1.3 Unit tests for normalize/resolve/compose (CLI override beats pref; unknown → default; RAF/USAAF markers present; neutral omits commander overlay; prompt mentions operational brief sections)

## 2. Research guidance tool

- [x] 2.1 Add `research_guidance` tool (query + optional mission_type/theatre hints): live web-backed adapter behind a small interface; stub/offline returns canned Channel Spitfire free_flight/intercept notes; soft-fail on errors
- [x] 2.2 Wire tool into `tools` surface + `tool_bridge` definitions/dispatch; export on stable import surface
- [x] 2.3 Tests: stub research returns non-empty notes offline; tool bridge dispatch works; research error does not break callers

## 3. Planner brief and CLI wiring

- [x] 3.1 Wire `plan_mission` to resolve voice before the LLM loop, pass composed system prompt, support post-success commander brief (summary / tactics / procedures / watch-outs) on `PlanResult.brief`; stub path produces assertable brief without network
- [x] 3.2 Add `plan --voice`; print commander brief on successful CLI plan; document `squadron_voice` pref values
- [x] 3.3 Agent/CLI tests: stub plan with `--voice usaaf`/`raf` uses composed prompt; Spec validates; brief contains tactics/procedures/watch-outs; stub can call `research_guidance`

## 4. Docs and acceptance

- [x] 4.1 Update README / ARCHITECTURE for squadron voice + commander brief + research tool; mark backlog `#11` building→done when accepted; note default `raf`
- [x] 4.2 Run targeted pytest + Ruff on touched paths; confirm stub plan still writes a valid Spec under each voice with a structured brief
