# Architecture

Developer map of the code. For *why* the project exists, see
[`DCS_AI_Mission_Planner.md`](../DCS_AI_Mission_Planner.md); for sequencing, see
[`BACKLOG.md`](BACKLOG.md).

**One rule shapes every box below:** the planning side decides *what* mission to build,
deterministic code decides *how* it becomes a `.miz`. No LLM writes DCS Lua.

## Compile path

```mermaid
flowchart TD
    yaml["examples/*.yaml<br/>Mission Spec (YAML)"]
    cli["cli.py<br/>dcs-miz validate / compile / theatres"]
    loader["loader.py<br/>YAML parse + SpecLoadError"]
    models["models.py<br/>MissionSpec (Pydantic)<br/>schema_version, extra=forbid"]
    validation["validation.py<br/>validate_mission_spec"]
    base["compiler/base.py<br/>CompilerInterface (ABC)"]
    pydcs["compiler/pydcs_compiler.py<br/>PyDCSCompiler"]
    registry["registry.py<br/>ChannelRegistry API"]
    data["data/channel/*.yaml<br/>airfields, aircraft, theatres,<br/>weather, payloads"]
    install["install/<br/>probe + SQLite inventory"]
    invdb["%LOCALAPPDATA%/dcs-miz-planner/<br/>inventory.sqlite"]
    ref["reference.py<br/>compat façade"]
    lib["PyDCS (dcs.*)<br/>third party"]
    miz["out/*.miz<br/>zip: mission, options,<br/>theatre, warehouses"]

    yaml --> cli --> loader --> models
    cli --> validation
    cli --> base
    cli --> install
    models --> validation
    validation --> registry
    validation --> install
    install --> invdb
    install --> registry
    base -.implemented by.-> pydcs
    models --> pydcs
    pydcs --> validation
    data --> registry
    registry --> pydcs
    registry --> ref
    pydcs --> lib
    pydcs --> miz
```

ASCII fallback:

```text
YAML spec -> cli -> loader -> MissionSpec -> validate_mission_spec
                                                  |     ^
                                                  |     | (same engine)
                                                  v     |
                                          PyDCSCompiler <- registry + install inventory
                                                  |  (PyDCS)
                                                  v
                                               .miz

cli validate  -> validation.py
cli theatres  -> install/ (probe) -> inventory.sqlite  (refresh on demand)
```

## Modules

| Module | Responsibility | Depends on |
|--------|----------------|------------|
| `cli.py` | `validate` / `compile` / legacy spec path; `theatres` list/refresh; clean errors | `loader`, `validation`, `compiler`, `install` |
| `loader.py` | YAML → `MissionSpec`; raises `SpecLoadError` with readable messages | `models`, `pyyaml` |
| `models.py` | The public contract: `MissionSpec` + enums. Rejects unknown fields; reserves `enemies`/`objectives`/`triggers` | `pydantic` |
| `validation.py` | Shared Spec checks (registry DCS-exists + install theatre availability + free-flight semantics); multi-error result | `models`, `registry`, `install` |
| `data/channel/` | Committed Channel YAML tables (airdromeIds, aircraft+radio, theatres, weather presets, payload stub) | — |
| `registry.py` | Loads packaged YAML; lookup API shared by validator/compiler (later agent) | `data/channel`, `pyyaml` |
| `reference.py` | Thin compatibility façade over `registry` (legacy constant names) | `registry` |
| `install/` | Read-only DCS install probe; classify available/disabled/incomplete/unknown; SQLite cache | `registry`, stdlib `sqlite3` |
| `compiler/base.py` | `CompilerInterface` — the seam that keeps PyDCS swappable | `models` |
| `compiler/pydcs_compiler.py` | **Only** module allowed to import PyDCS. Validates via shared engine, then places the flight / writes `.miz` | `models`, `validation`, `registry`, `dcs.*` |

Two stores stay separate on purpose:

- **YAML registry** = product source of truth (what this planner knows how to compile).
- **SQLite inventory** = user-local cache of what is installed/enabled on this PC
  (`%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite`). Ordinary reads hit the DB;
  `dcs-miz theatres --refresh` rescans. Never commit the DB.

Two boundaries worth respecting:

- **`models.py` never imports compiler or PyDCS types.** The Spec is the contract; it must
  stay serializable and backend-agnostic.
- **PyDCS imports live inside `pydcs_compiler.py` function bodies**, so importing the package
  never eagerly loads a DCS install. That module also carries deliberate workarounds
  (payload-scan disable, `theatre` member, VHF frequency) — see
  [`LESSONS_LEARNED.md`](LESSONS_LEARNED.md) before editing it.
- **Install probe never executes DCS Lua**; it only extracts static quoted fields from
  `entry.lua` / `pluginsEnabled.lua`.

## Repo layout

| Path | What lives there |
|------|------------------|
| `src/dcs_miz_planner/` | Product code (the modules above) |
| `examples/` | Checked-in Mission Specs; `manston_cold_freeflight.yaml` is the acceptance fixture |
| `tests/` | pytest: schema, registry, install probe (synthetic fixtures), compile asserts |
| `openspec/` | Spec-driven workflow: `specs/` (current truth), `changes/` (in flight), `changes/archive/` |
| `.cursor/` | Agent tooling: `skills/`, `hooks/`, `rules/`, `commands/` |
| `docs/` | This file, `BACKLOG.md`, `LESSONS_LEARNED.md` |
| `out/` | Generated `.miz` output (gitignored) |
| `research/` | Local DCS samples and findings — **gitignored**, never a source of truth for specs |

Planning and product are deliberately separate: `openspec/specs/` states what the system
must do, `src/` implements it, and no code lands before its change is apply-ready.

## Keeping this current

Update this file when the public package layout changes, a module gains or loses a
responsibility, or the Spec→`.miz` flow shifts — same commit as the change, not later.
A Cursor hook (`.cursor/hooks/architecture-on-push.py`) reminds you on `git push` when
`src/dcs_miz_planner/` is part of what you are pushing. It only reminds; it never blocks,
and it is not a generator — the map is written by hand so it explains intent, not just imports.

Not yet built (arrives with M3 in the backlog): the agent layer that turns natural language
into a Mission Spec, plus registry-backed lookup tools.
