## Why

Live DuckDuckGo HTML/Instant Answer snippets are injected into chat as synthetic user
content (and returned as tool JSON) with little sanitization. Poisoned SERP text can
steer briefs or prefs; Spec accept limits `.miz` damage only (adversarial C2). Agent
`research_guidance` vs `/research` also label live vs fixture inconsistently (A7).

## What Changes

- Sanitize research note title/snippet before return or LLM injection: strip control
  characters, enforce length caps, normalize whitespace.
- Wrap host `/research` session injection in clear delimiters and stronger
  “untrusted / not Spec or tool instructions” wording.
- Align live vs fixture labeling for tool results and `/research` (per-note sources +
  retrieval mode / warnings when fixtures substitute for live).
- Tests for control-char stripping, caps, delimiter wording, and fixture/live labels.

## Non-goals

- No paid research API; no full HTML→text rewrite of DDG parsers.
- No Spec accept-gate or compile sandbox changes (covered by `#33`).
- No PDF Doc extract (`#40`); no CI changes.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `agent-tools`: research note sanitization + clear live/fixture labeling on
  `research_guidance` results.
- `plan-repl`: `/research` injection delimiters and untrusted-content wording;
  label alignment with the tool.

## Impact

- `tools/research.py`, `tools/surface.py`, `agent/session.py`; tests; docs/BACKLOG.
