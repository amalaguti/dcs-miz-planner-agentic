## Why

Agent tools need a queryable local catalog of resources. The **known** set stays Channel YAML +
Spec enums (compile SoT — no invented ids). Separately we need **discovery** of what is on
this PC (theatres already probed; more types later) and a clear **ad-hoc** path to promote
discovered or researched items into known YAML when we are ready to compile them.

## What Changes

- Add synced **known catalog** SQLite tables (`catalog_*`) from packaged Channel YAML + Spec enums.
- Expose **discovery** alongside known data: reuse install theatre inventory; record
  discovered theatres as offerable only when known ∩ available ∩ planner_supported; surface
  discovered-but-unsupported for visibility.
- Document **ad-hoc maintenance**: how to expand known YAML (and re-sync catalog) when adding
  a theatre/aircraft after in-game verification — without making SQLite the authoring SoT.
- Python sync/query API + CLI list/dump (`dcs-miz catalog …`).
- **Not BREAKING** to compile path.

## Catalog inventory

### A. Known (synced from YAML / Spec) — compile-capable

| Object | Source | Current scope |
|--------|--------|---------------|
| Theatre | `theatres.yaml` | `TheChannel` |
| Airfield | `airfields.yaml` | 12 Channel fields (incl. Manston) |
| Aircraft | `aircraft.yaml` | SpitfireLFMkIX(+CW), Bf-109K-4, FW-190A8/D9 |
| Weather preset | `weather_presets.yaml` | `sunny_clear` |
| Payload | `payloads.yaml` | empty stub |
| Mission type / start / coalition / objective / country | Spec enums | free_flight, intercept, cold_parking, blue/red, intercept_enemy, UK, ThirdReich |

### B. Discovered (local install — not compile SoT)

| Object | Source today | Role |
|--------|--------------|------|
| Install theatre | existing `dcs-miz theatres` / install SQLite | List installed/enabled maps; join to known |
| Aircraft / modules | *not harvested yet* | Design stub / follow-up: discover without promoting to known |

### C. Out of v1

Prefs/history/satisfaction; landmarks; full ME option matrix; auto-promoting discovery → known.

## Non-goals

- Auto-widening compile support to every installed map/module.
- Harvesting payload CLSIDs from the live DCS install into known YAML.
- Agent NL tools (next change); prefs/history tables.

## Capabilities

### New Capabilities

- `agent-catalog`: Known catalog sync + query; discovery join for theatres; ad-hoc known-growth docs.

### Modified Capabilities

- `installed-theatres`: Catalog may read install inventory for availability joins (no change to
  probe semantics required unless a thin query helper is shared).

## Impact

- `catalog/` module, CLI, tests; docs for sync + “promote to known” workflow.
- Unblocks `agent-tools-surface` with honest known vs discovered flags.
