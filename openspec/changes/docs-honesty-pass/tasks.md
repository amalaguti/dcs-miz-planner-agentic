## 1. Docs honesty

- [x] 1.1 Rewrite README Status lead: remove combat/trigger “reserved for later”; reflect shipped Spec combat types + native triggers; keep accepted-in-game detail; add a short intentional-limits note (Channel MVP; campaign `.miz` not imported; stub/offline hermetic research)
- [x] 1.2 Align README / ARCHITECTURE / LESSONS campaign Doc wording to **filenames/titles only** (no “themes” / extracted briefings); cross-link `#40` if mentioning future extract
- [x] 1.3 Mark `docs/BACKLOG.md` `#31` as `building` while applying (then `done` at finish)

## 2. Agent-facing copy

- [x] 2.1 Update `agent/prompts.py` campaign / Doc guidance to filenames/titles only
- [x] 2.2 Update `agent/tool_bridge.py` `list_installed_campaigns` description (no “prefer Doc briefing themes”)
- [x] 2.3 Update `tools/surface.py` / `install/campaigns.py` docstrings to match filename-only Doc listing
- [x] 2.4 Fix campaign Doc phrasing in `agent/spec_schema.py` common notes only — **do not** change `SPEC_SHAPE_REMINDER` empty-triggers line (owned by `#30c`)

## 3. Tests & verify

- [x] 3.1 Update any prompt/tool tests that assert old “theme” / “briefing themes” wording; keep campaign fixture filename assertions
- [x] 3.2 Run targeted pytest (`test_tools`, `test_campaigns`, prompt-related) and full suite if quick
- [x] 3.3 Grep repo (src/docs/README, exclude archive) for “Doc briefing theme” / overclaim phrases; clean stragglers
