# DCS AI Mission Planner

Natural-language → validated Mission Spec → deterministic `.miz` compiler for DCS World.

**Principle:** the AI plans; software compiles. No LLM-authored DCS Lua.

## Status

First vertical slice done: Manston cold free flight compiles and flies in DCS
(accepted in-game). Mission Spec is formalized (`schema_version: "1"`, unknown
fields rejected, combat/trigger keys reserved for later).

**MVP acceptance:** Spitfire LF Mk IX, Channel map, cold start free flight at Manston, 09:00, sunny.

## Stack

- Python 3.12 + uv
- Mission Spec (Pydantic) → compiler via PyDCS (behind `CompilerInterface`)
- OpenSpec (`npx openspec`) for SDD
- pre-commit (blocks commits on `master`/`main`)

## Compile the Manston example

```bash
uv sync
uv run dcs-miz examples/manston_cold_freeflight.yaml
# -> out/manston_cold_freeflight.miz
```

Open the result in the DCS Mission Editor, or copy it into
`Saved Games\DCS\Missions\` to fly it from Instant Action / Load Mission.

## Setup notes

```bash
uv tool install pre-commit
pre-commit install
```

Agent work stays off `master`/`main` (Cursor hook + skill). Commits are also blocked there by pre-commit.

## Docs

- Concept: [`DCS_AI_Mission_Planner.md`](DCS_AI_Mission_Planner.md)
- Roadmap / backlog: [`docs/BACKLOG.md`](docs/BACKLOG.md)
- Agent lessons (PyDCS/DCS pitfalls): [`docs/LESSONS_LEARNED.md`](docs/LESSONS_LEARNED.md)
- OpenSpec config: [`openspec/config.yaml`](openspec/config.yaml)
- Local research samples are gitignored (`research/`)
