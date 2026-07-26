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
refresh with `dcs-miz theatres --refresh`. Shared validation
(`dcs-miz validate` / compile) checks registry + local theatre inventory.
Module map:
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

**MVP acceptance:** Spitfire LF Mk IX, Channel map, cold start free flight at Manston, 09:00, sunny.

## Stack

- Python 3.12 + uv
- Mission Spec (Pydantic) → shared validation → compiler via PyDCS (behind `CompilerInterface`)
- OpenSpec (`npx openspec`) for SDD
- pre-commit (blocks commits on `master`/`main`; runs Ruff lint + format on Python)

## Validate and compile the Manston example

```bash
uv sync
uv run dcs-miz validate examples/manston_cold_freeflight.yaml
uv run dcs-miz examples/manston_cold_freeflight.yaml
# -> out/manston_cold_freeflight.miz
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
