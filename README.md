# DCS AI Mission Planner

Natural-language → validated Mission Spec → deterministic `.miz` compiler for DCS World.

**Principle:** the AI plans; software compiles. No LLM-authored DCS Lua.

## Status

First vertical slice done: Manston cold free flight compiles and flies in DCS
(accepted in-game). Mission Spec is formalized (`schema_version: "1"`, unknown
fields rejected, combat/trigger keys reserved for later). Channel DCS facts
(airfields, aircraft, radio, weather presets) live in packaged YAML under
`src/dcs_miz_planner/data/channel/`, queried via `registry.py`. Local map
availability is cached in SQLite (`%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite`);
refresh with `dcs-miz theatres --refresh`. Known agent catalog (`catalog_*` tables in the
same DB) syncs from Channel YAML + Spec enums via `dcs-miz catalog sync`. Shared validation
(`dcs-miz validate` / compile) checks registry + local theatre inventory.
Manston compile structure is pinned by golden fixtures under `tests/fixtures/`
(refresh: `uv run python tests/refresh_manston_golden.py`). Intercept Spec
(`examples/manston_dawn_intercept.yaml`) places Bf-109K-4s on a Hawkinge/Dover
approach corridor — open the compiled `.miz` in DCS to accept. Module map:
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

**MVP acceptance:** Spitfire LF Mk IX, Channel map, cold start free flight at Manston, 09:00, sunny.
**Next:** squadron-commander voice (prefs/history already in local SQLite).

## Stack

- Python 3.12 + uv
- Mission Spec (Pydantic) → shared validation → compiler via PyDCS (behind `CompilerInterface`)
- OpenSpec (`npx openspec`) for SDD
- pre-commit (blocks commits on `master`/`main`; runs Ruff lint + format on Python)

## Validate and compile examples

```bash
uv sync
uv run dcs-miz validate examples/manston_cold_freeflight.yaml
uv run dcs-miz examples/manston_cold_freeflight.yaml
# -> out/manston_cold_freeflight.miz

uv run dcs-miz validate examples/manston_dawn_intercept.yaml
uv run dcs-miz examples/manston_dawn_intercept.yaml
# -> out/manston_dawn_intercept.miz
```

Open the result in the DCS Mission Editor, or copy it into
`Saved Games\DCS\Missions\` to fly it from Instant Action / Load Mission.

## List local theatres

```bash
uv run dcs-miz theatres                 # SQLite cache (scans once if empty)
uv run dcs-miz theatres --refresh       # rescan DCS install + update cache
uv run dcs-miz theatres --json          # machine-readable
uv run dcs-miz theatres --dcs-root "S:/DCS World"
```

Product theatre ids stay in YAML; the SQLite file is only a user-local install inventory.

## Agent catalog (known + discovery)

```bash
uv run dcs-miz catalog sync              # replace catalog_* from packaged YAML + Spec enums
uv run dcs-miz catalog list              # theatres: known vs installed vs offerable
uv run dcs-miz catalog list --known-only
uv run dcs-miz catalog list --type aircraft --json
uv run dcs-miz catalog list --type planning_options --json
uv run dcs-miz catalog list --type planning_options --family weather --support supported
```

To grow **known** entries: edit `src/dcs_miz_planner/data/channel/*.yaml` (and Spec enums
when needed), accept in DCS when compile-supported, then `catalog sync`. Planning knobs live
in `planning_options.yaml` with support levels (`supported` / `advisory` / `future`).
Discovered install theatres are listed with `known=false` and are not auto-promoted.
Normandy (or other maps) is not required for the planning-option catalog.

## Agent tools (Python API)

Import from `dcs_miz_planner.tools` (no dedicated tools CLI — pytest is the acceptance path):

- `find_airfield(query)` / `get_aircraft_details(aircraft_id)` — known catalog
- `list_mission_options()` — Spec enums + enriched planning options + offerable theatres
- `get_user_prefs` / `set_user_prefs` / `list_generation_history` / `record_generation` /
  `record_feedback` — local user memory
- `validate_mission_spec(path)` / `compile_mission(path, output)` — wrap existing engines

Results are JSON-friendly dicts with an `ok` flag for later LLM tool calling.

## User prefs and history

Same SQLite file as install/catalog (`%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite`):

```bash
uv run dcs-miz prefs set preferred_airfield Manston
uv run dcs-miz prefs list --json
uv run dcs-miz prefs history --json
uv run dcs-miz feedback --score 5 --note "good sortie"
```

The NL planner records generation history on success/failure; prefs are never wiped by
`catalog sync`.

## Plan a mission (natural language)

Offline stub (no API key — canned Manston free flight):

```bash
uv run dcs-miz plan "cold Spitfire free flight at Manston" --stub -o out/planned.yaml
uv run dcs-miz plan "..." --stub --compile -o out/planned.yaml
```

Live (OpenAI-compatible):

```bash
# PowerShell
$env:OPENAI_API_KEY = "sk-..."
# optional: $env:DCS_MIZ_LLM_MODEL = "gpt-4o-mini"
uv run dcs-miz plan "dawn intercept from Manston vs Bf-109s" -o out/planned.yaml --compile
```

The agent may call catalog tools, then writes Mission Spec YAML; `--compile` uses PyDCS.
Never put API keys in the repo or SQLite — environment only.
Dates should fit the history you want (WWII Channel content usually 1939–1945; modern
or other eras are allowed). A mismatched Channel date still succeeds but prints a
**Warning** on stderr.

## Setup notes

```bash
uv tool install pre-commit
pre-commit install
```

Agent work stays off `master`/`main` (Cursor hook + skill). Commits are also blocked there by pre-commit. Every commit runs Ruff (`ruff-check --fix` + `ruff-format`) via pre-commit.

## Docs

- Concept: [`DCS_AI_Mission_Planner.md`](DCS_AI_Mission_Planner.md)
- Architecture / module map: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- Roadmap / backlog: [`docs/BACKLOG.md`](docs/BACKLOG.md)
- Agent lessons (PyDCS/DCS pitfalls): [`docs/LESSONS_LEARNED.md`](docs/LESSONS_LEARNED.md)
- OpenSpec config: [`openspec/config.yaml`](openspec/config.yaml)
- Local research samples are gitignored (`research/`)
