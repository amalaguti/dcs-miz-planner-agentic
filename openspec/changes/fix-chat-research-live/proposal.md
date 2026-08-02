## Why

Chat `/research` and `research_guidance(live=True)` often return no live snippets and silently
fall back to generic WWII fixtures, so the pilot sees fixture text that looks like a successful
web lookup. Live research must either return query-relevant notes or a clear, actionable
failure — not fake success via fixtures.

## What Changes

- Improve live web retrieval so typical Channel/Spitfire research queries yield usable snippets
  when the network is available (better provider path and/or query enrichment + timeouts).
- When live was requested and returns zero notes or errors, surface the failure reason clearly
  (verbose always; brief pilot-facing message for `/research` and tool warning) instead of
  presenting fixture-only output as if live succeeded.
- Keep fixtures for stub/offline and as optional grounding when live succeeds; never treat
  research as Spec or DCS-id authority.
- Add pytest coverage for live success, empty live, and exception paths (injectable fetch).

## Non-goals

- Paid search APIs, API keys for research, or scraping behind auth.
- Making research authoritative for Mission Spec fields, registry ids, or compile.
- Changing squadron voice packs, briefing → `.miz` `l10n`, or new mission types.
- Defaulting all environments to live network in CI (tests stay mocked/offline).
- Flipping agent verbose default off (`agent-verbose-default-off`).

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `agent-tools`: Strengthen `research_guidance` live-mode contract — useful snippets when
  live succeeds; distinct warning / empty-live handling when it does not; fixtures remain
  offline default.
- `plan-repl`: `/research` MUST distinguish live success vs live-empty/error fallback so
  pilots are not misled by fixture-only output.
- `squadron-voice`: Align optional research requirement with clearer live failure UX
  (fixtures only when offline or after an explicit soft-fail warning).

## Impact

- `tools/research.py`: provider / enrichment / timeout; warning strings; merge policy.
- `tools/surface.py` (`research_guidance`) and `agent/session.py` (`/research` formatting).
- Tests under `tests/test_tools.py` / `tests/test_chat.py` (mocked live paths).
- README / BACKLOG `#10d` status when accepted; LESSONS only if a non-obvious provider pitfall
  is discovered.
- Acceptance: with network, `/research Manston spitfire` returns live-sourced notes (or a
  clear live-failure message); offline/stub still fixture-only; Spec/compile unchanged
  (no DCS Mission Editor acceptance required).
