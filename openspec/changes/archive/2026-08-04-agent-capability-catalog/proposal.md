## Why

The agent can look up airfields, weather, and mission types, but mission *behaviour*
knobs (altitude/speed gates, marks, narrative, radio/late-act, sound) live mainly in
schema footnotes. For creative-but-assertive planning—e.g. inventing a low-level
ingress challenge without the user spelling every trigger—the agent needs curated
capability cards it is told to consult and apply.

Inspiration should also come from the open web (DCS User Files, public repos) **and the
local DCS install**—especially shipped campaigns under `Mods/campaigns`—not only packaged
YAML. Live research and install discovery already exist in pieces; this change aims them
at *mission-design* discovery and ties results to Spec-backed behaviour cards.

## What Changes

- Extend packaged `planning_options.yaml` with `mission_behaviour` (compile recipes) and
  `mission_inspiration` (advisory pattern cards linked to those recipes).
- Seed v1 behaviour cards for shipped Spec features and v1 inspiration cards from known
  stock/R5-style patterns.
- Extend `research_guidance` live path so creativity queries prefer mission-design sources
  (DCS User Files / community mission pages, public repos, ME references) and return
  short title/snippet/source notes the agent can map onto behaviour cards—soft-fail to
  fixtures as today.
- Add (or extend install tooling with) a **local campaign/mission index** over the discovered
  DCS World root (`Mods/campaigns`): `.cmp` playlist metadata, `.miz` filenames, and each
  campaign’s **`Doc/` briefing PDFs** (sortie briefs, campaign intro—richer for design
  inspiration than `.cmp` alone). List for agent inspiration; optional on-demand Doc text;
  not full `.miz` import.
- Teach prompts/tools: vague user → inspiration + behaviour options + optional live
  research and/or local campaigns (esp. Doc briefs) → emit 1–2 supported behaviours (no LLM Lua).
- Tests for catalog families + research query enrichment / fixture soft-fail + local index
  hermetic fixture; BACKLOG note for R1/R2 deeper download-and-audit promote path.

## Non-goals

- Downloading, unzipping, or fully parsing third-party `.miz` / campaign packs into Specs
  in this change (local index may read `.cmp` / filenames / `Doc/` listing / light metadata
  only; optional single-Doc text extract).
- Auto-compiling community or campaign missions into Specs.
- Shipping copyrighted mission binaries in the repo.
- A second Spec SoT; `#22` Lua; inventing new ME predicates.
- Guaranteeing live DCS site HTML always yields rich results (best-effort + soft-fail).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-options`: `mission_behaviour` + `mission_inspiration` families.
- `agent-catalog`: Sync exposes new planning-option rows.
- `agent-tools`: `list_mission_options` surfaces both families; `research_guidance`
  mission-inspiration bias for live web/repo/DCS-site discovery; local install
  campaign/mission index tool (or extended install API) for `Mods/campaigns`; schema/prompt
  notes.
- `installed-theatres` or install discovery: reuse DCS root discovery for campaign paths
  (delta only if requirements must move; prefer agent-tools + install helper).
- `nl-agent`: Assertive creative loop using cards + research + local campaign index.
- `golden-fixtures`: Coverage for options families, research enrichment, and hermetic
  local-index listing.

## Impact

- `planning_options.yaml`; `tools/research.py`; install helper + agent tool for local
  campaigns; prompts / `spec_schema` / tool_bridge; tests; BACKLOG/README briefly.
- Acceptance: catalog lists behaviour + inspiration; live research enrichment testable;
  local campaign index lists installed campaigns (or hermetic fixture); prompts instruct
  the creative loop.
