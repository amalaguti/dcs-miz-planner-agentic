## Why

Adversarial review (2026-08-05) found trust-breaking overclaims: README Status still says combat/trigger keys are “reserved for later” while M4–M6 are shipped, and product/prompt copy tells the agent to prefer campaign `Doc/` “briefing themes” when the indexer only returns PDF **filenames**. Cheap honesty now prevents false expectations before `#30c` / `#40` deepen behaviour.

## What Changes

- Rewrite README **Status** lead so it matches shipped Spec, combat types, and native triggers (no “reserved for later” for combat/triggers).
- Downgrade all user- and agent-facing campaign Doc claims to **filenames / titles only** until `#40` (or wontfix): README, prompts, tool descriptions, ARCHITECTURE/LESSONS as needed.
- Align OpenSpec requirements for `list_installed_campaigns` and planner guidance with filename-only reality (no implied PDF text extract).
- Label intentional limits briefly where docs over-promise (Channel MVP, campaign `.miz` not imported, stub/offline research for hermetic tests) without expanding product scope.

## Non-goals

- Fixing `SPEC_SHAPE_REMINDER` “triggers must be []” (owned by `#30c`).
- PDF text extraction from `Doc/` (`#40`).
- Validation false-green / late-activation graph checks (`#32`).
- Assertive creativity policy, schema immersion examples, or memory inference fixes (`#30c`).
- New compiler or Mission Spec fields.
- In-game ME acceptance (docs/prompt honesty only).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `agent-tools`: Campaign index requirement MUST state Doc entries are filenames only; MUST NOT require or imply PDF body extraction.
- `nl-agent`: Assertive planning guidance MUST prefer Doc **filenames/titles** for inspiration, not “themes” or briefing text content.

## Impact

- Docs: `README.md`, possibly `docs/ARCHITECTURE.md` / `docs/LESSONS_LEARNED.md` wording.
- Agent strings: `agent/prompts.py`, `agent/spec_schema.py` (campaign Doc phrasing only — not the empty-triggers reminder), `agent/tool_bridge.py`, `tools/surface.py` docstrings.
- OpenSpec deltas under `agent-tools` / `nl-agent`; backlog `#31` → done after archive.
- Tests: update assertion strings that expect “theme”/“briefing” wording if present; no behaviour change to campaign indexer beyond copy.
