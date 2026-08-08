## Why

The invent agent only sees strike/recon unit ids indirectly via
`strike_target_class` planning_options meta. That is easy to miss and is not a
queryable unit table. `#8c` syncs Channel registry land+sea units into the agent
catalog SQLite so invent can call `list_strike_targets` and prefer returned ids
only—without scanning YAML mid-turn or inventing DCS ids.

## What Changes

- Extend `dcs-miz catalog sync` to populate `catalog_strike_units` from Channel
  `ground_units.yaml` + `ships.yaml` (via registry APIs), with optional class tags
  derived from `strike_target_class` planning_options meta.
- Read-only agent/CLI query: `list_strike_targets(domain?, class?, q?)` reading
  **SQLite only** after sync.
- Prompts/schema: for GA/recon, call the tool before inventing `targets[]`.
- Tests: sync includes `Uboat_VIIC` as sea; tool filters work hermetically.
- Compile/validate remain registry SoT (unchanged).

## Capabilities

### New Capabilities

- *(none — extends agent-catalog / agent-tools)*

### Modified Capabilities

- `agent-catalog`: sync + list strike/recon unit rows in catalog SQLite.
- `agent-tools`: `list_strike_targets` tool (and invent surface).
- `nl-agent` / `mission-options` (light): discoverability and invent guidance.
- `golden-fixtures` / catalog tests as needed.

## Impact

- `catalog/{models,sync,store,service}.py`, `cli.py`, `tools/surface.py`,
  `agent/tool_bridge.py`, prompts/schema, tests, BACKLOG `#8c`.
- Feeds later `#8d` heuristics; does not expand registry unit shelves.

## Non-goals

- Inventing or scraping new DCS unit ids; WWII Assets Pack dump.
- Replacing registry for validate/compile.
- Building the table inside each LLM turn (sync is offline/CLI).
- Multi-theatre unit SoT (Channel only); R11 stays separate.
- Full `#8d` invent decision table (thin prompt note OK).

## Acceptance

After `catalog sync`, `list_strike_targets(domain=sea)` returns `Uboat_VIIC`;
land soft/AAA ids appear; invent guidance mentions the tool. No ME fly required
(catalog/CLI accept).
