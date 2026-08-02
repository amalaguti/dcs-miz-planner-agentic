"""Command-line entrypoint: compile, validate, theatres, catalog, prefs, plan, and chat."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .agent import (
    AgentConfigError,
    PlanSession,
    StubLLM,
    live_llm_from_env,
    plan_mission,
    run_chat_repl,
    stub_chat_clarify_then_spec,
)
from .catalog import AIRCRAFT_DISCOVERY_DEFERRED, LIST_TYPES, CatalogService
from .compiler import PyDCSCompiler
from .install import InventoryService, default_db_path
from .loader import SpecLoadError, load_mission_spec
from .memory import UserMemoryService
from .randomize import RandomizeError, randomize_mission_spec
from .validation import validate_mission_spec

DEFAULT_OUTPUT_DIR = Path("out")


def _dump_spec_yaml(spec) -> str:
    import yaml

    return yaml.safe_dump(spec.model_dump(mode="json"), sort_keys=False, allow_unicode=True)


def _compile_cmd(args: argparse.Namespace) -> int:
    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"Spec not found: {spec_path}", file=sys.stderr)
        return 2

    try:
        spec = load_mission_spec(spec_path)
    except SpecLoadError as exc:
        print(exc, file=sys.stderr)
        return 2

    voice = None
    if getattr(args, "voice", None):
        from .agent.voice import resolve_voice

        voice = resolve_voice(cli_voice=args.voice)

    output = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR / f"{spec_path.stem}.miz"
    try:
        written = PyDCSCompiler().compile(spec, output, voice=voice)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    print(f"Wrote {written}")
    return 0


def _randomize_cmd(args: argparse.Namespace) -> int:
    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"Spec not found: {spec_path}", file=sys.stderr)
        return 2

    try:
        spec = load_mission_spec(spec_path)
    except SpecLoadError as exc:
        print(exc, file=sys.stderr)
        return 2

    try:
        out_spec = randomize_mission_spec(
            spec,
            args.seed,
            axes=args.axes,
            annotate=args.annotate,
        )
    except RandomizeError as exc:
        print(exc, file=sys.stderr)
        return 2

    if not args.no_validate:
        result = validate_mission_spec(out_spec)
        if not result.ok:
            print("Randomized Spec failed validation:", file=sys.stderr)
            for err in result.errors:
                loc = f"{err.path}: " if err.path else ""
                print(f"  [{err.code}] {loc}{err.message}", file=sys.stderr)
            return 2

    output = (
        Path(args.output)
        if args.output
        else DEFAULT_OUTPUT_DIR / f"{spec_path.stem}_seed{args.seed}.yaml"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(_dump_spec_yaml(out_spec), encoding="utf-8")
    print(f"Wrote {output}")
    return 0


def _validate_cmd(args: argparse.Namespace) -> int:
    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"Spec not found: {spec_path}", file=sys.stderr)
        return 2

    try:
        spec = load_mission_spec(spec_path)
    except SpecLoadError as exc:
        print(exc, file=sys.stderr)
        return 2

    result = validate_mission_spec(spec)
    if args.json:
        payload = {
            "ok": result.ok,
            "errors": [
                {
                    "code": e.code,
                    "path": e.path,
                    "message": e.message,
                    "hint": e.hint,
                }
                for e in result.errors
            ],
        }
        print(json.dumps(payload, indent=2))
    elif result.ok:
        print(f"Valid: {spec_path}")
    else:
        print(f"Invalid: {spec_path}", file=sys.stderr)
        for err in result.errors:
            loc = f"{err.path}: " if err.path else ""
            hint = f" — {err.hint}" if err.hint else ""
            print(f"  [{err.code}] {loc}{err.message}{hint}", file=sys.stderr)
    return 0 if result.ok else 2


def _theatres_cmd(args: argparse.Namespace) -> int:
    service = InventoryService(
        db_path=args.db if args.db else None,
        dcs_root=args.dcs_root,
        saved_games=args.saved_games,
    )
    inventory = service.refresh() if args.refresh else service.get()

    if not inventory.dcs_roots:
        for diag in inventory.diagnostics:
            print(diag.message, file=sys.stderr)
        return 2

    if args.json:
        payload = {
            "scanned_at": inventory.scanned_at.isoformat(),
            "from_cache": inventory.from_cache,
            "dcs_roots": list(inventory.dcs_roots),
            "saved_games_roots": list(inventory.saved_games_roots),
            "db_path": str(service.db_path),
            "theatres": [
                {
                    "theatre_id": t.theatre_id,
                    "update_id": t.update_id,
                    "dcs_root": t.dcs_root,
                    "state": t.state.value,
                    "planner_supported": t.planner_supported,
                    "terrain_path": t.terrain_path,
                    "saved_games_root": t.saved_games_root,
                    "evidence": list(t.evidence),
                }
                for t in inventory.theatres
            ],
            "diagnostics": [
                {"message": d.message, "source": d.source} for d in inventory.diagnostics
            ],
        }
        print(json.dumps(payload, indent=2))
        return 0

    cache_note = "cache" if inventory.from_cache else "refreshed"
    print(
        f"Theatre inventory ({cache_note}) scanned_at={inventory.scanned_at.isoformat()} "
        f"db={service.db_path}"
    )
    for root in inventory.dcs_roots:
        print(f"  DCS root: {root}")
    for root in inventory.saved_games_roots:
        print(f"  Saved Games: {root}")
    print()
    print(f"{'theatre_id':<22} {'update_id':<28} {'state':<12} {'planner':<8} root")
    print("-" * 100)
    for t in inventory.theatres:
        planner = "yes" if t.planner_supported else "no"
        update = t.update_id or "-"
        print(f"{t.theatre_id:<22} {update:<28} {t.state.value:<12} {planner:<8} {t.dcs_root}")
    if inventory.diagnostics:
        print()
        print("Diagnostics:")
        for diag in inventory.diagnostics:
            src = f" ({diag.source})" if diag.source else ""
            print(f"  - {diag.message}{src}")
    return 0


def _catalog_sync_cmd(args: argparse.Namespace) -> int:
    service = CatalogService(db_path=args.db if args.db else None)
    snap = service.sync()
    print(
        f"Catalog synced source={snap.source} synced_at={snap.synced_at.isoformat()} "
        f"db={service.db_path}"
    )
    print(
        f"  theatres={len(snap.theatres)} airfields={len(snap.airfields)} "
        f"aircraft={len(snap.aircraft)} weather={len(snap.weather_presets)} "
        f"payloads={len(snap.payloads)} planning_options={len(snap.planning_options)}"
    )
    return 0


def _catalog_list_cmd(args: argparse.Namespace) -> int:
    service = CatalogService(db_path=args.db if args.db else None)
    resource_type = args.type or "theatres"

    if resource_type == "theatres":
        views = service.list_theatres(include_discovered=not args.known_only)
        if args.json:
            payload = {
                "db_path": str(service.db_path),
                "type": "theatres",
                "rows": [
                    {
                        "theatre_id": v.theatre_id,
                        "known": v.known,
                        "installed": v.installed,
                        "install_state": v.install_state,
                        "planner_supported": v.planner_supported,
                        "offerable": v.offerable,
                        "dcs_root": v.dcs_root,
                    }
                    for v in views
                ],
            }
            print(json.dumps(payload, indent=2))
            return 0
        print(f"Catalog theatres db={service.db_path}")
        print(
            f"{'theatre_id':<22} {'known':<6} {'installed':<10} "
            f"{'state':<12} {'offerable':<10} root"
        )
        print("-" * 90)
        for v in views:
            state = v.install_state or "-"
            root = v.dcs_root or "-"
            print(
                f"{v.theatre_id:<22} {v.known!s:<6} {v.installed!s:<10} "
                f"{state:<12} {v.offerable!s:<10} {root}"
            )
        return 0

    if resource_type == "aircraft":
        note = AIRCRAFT_DISCOVERY_DEFERRED
    else:
        note = None

    family = getattr(args, "family", None)
    support = getattr(args, "support", None)
    if resource_type != "planning_options" and (family or support):
        print(
            "--family/--support apply only with --type planning_options",
            file=sys.stderr,
        )
        return 2

    try:
        rows = service.list_rows(resource_type, family=family, support=support)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2

    if args.json:
        payload: dict[str, object] = {
            "db_path": str(service.db_path),
            "type": resource_type,
            "rows": rows,
        }
        if note:
            payload["note"] = note
        print(json.dumps(payload, indent=2))
        return 0

    print(f"Catalog {resource_type} db={service.db_path} ({len(rows)} rows)")
    if note:
        print(f"Note: {note}")
    for row in rows:
        print("  " + " ".join(f"{k}={v}" for k, v in row.items()))
    return 0


def _catalog_root_cmd(_args: argparse.Namespace) -> int:
    print("Usage: dcs-miz catalog {sync,list} ...", file=sys.stderr)
    return 2


def _plan_cmd(args: argparse.Namespace) -> int:
    output = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR / "planned.yaml"
    if args.stub:
        llm = StubLLM()
    else:
        try:
            llm = live_llm_from_env()
        except AgentConfigError as exc:
            print(exc, file=sys.stderr)
            return 2

    miz = Path(args.miz) if args.miz else None
    result = plan_mission(
        args.prompt,
        output,
        llm=llm,
        compile_output=bool(args.compile),
        miz_path=miz,
        db_path=args.db if getattr(args, "db", None) else None,
        voice=args.voice if getattr(args, "voice", None) else None,
        verbose=bool(args.verbose),
    )
    if not result.ok:
        print(result.error or "Planning failed", file=sys.stderr)
        for err in result.validation_errors:
            print(f"  [{err.get('code')}] {err.get('message')}", file=sys.stderr)
        return 2
    print(f"Wrote Spec {result.spec_path}")
    if result.miz_path:
        print(f"Wrote {result.miz_path}")
    if result.voice:
        print(f"Voice: {result.voice}")
    if result.brief:
        print()
        print(result.brief)
    for warning in result.warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    return 0


def _chat_cmd(args: argparse.Namespace) -> int:
    output = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR / "planned.yaml"
    if args.stub:
        llm = stub_chat_clarify_then_spec()
    else:
        try:
            llm = live_llm_from_env()
        except AgentConfigError as exc:
            print(exc, file=sys.stderr)
            return 2

    session = PlanSession(
        llm=llm,
        output_path=output,
        db_path=args.db if getattr(args, "db", None) else None,
        voice=args.voice if getattr(args, "voice", None) else None,
        compile_on_accept=bool(args.compile),
        miz_path=Path(args.miz) if getattr(args, "miz", None) else None,
        verbose=bool(args.verbose),
    )
    return run_chat_repl(session)


def _prefs_cmd(args: argparse.Namespace) -> int:
    mem = UserMemoryService(db_path=args.db if args.db else None)
    if args.prefs_command == "set":
        if not args.key:
            print("Usage: dcs-miz prefs set <key> <value>", file=sys.stderr)
            return 2
        raw = args.value if args.value is not None else ""
        try:
            value: object = json.loads(raw)
        except json.JSONDecodeError:
            value = raw
        prefs = mem.set_prefs({args.key: value})
        if args.json:
            print(json.dumps({"db_path": str(mem.db_path), "prefs": prefs}, indent=2))
        else:
            print(f"Set {args.key}={value!r} db={mem.db_path}")
        return 0

    if args.prefs_command == "history":
        rows = mem.list_generations(limit=args.limit)
        payload = [
            {
                "id": r.id,
                "created_at": r.created_at,
                "outcome": r.outcome,
                "mission_type": r.mission_type,
                "theatre": r.theatre,
                "spec_path": r.spec_path,
                "prompt": r.prompt,
            }
            for r in rows
        ]
        if args.json:
            print(json.dumps({"db_path": str(mem.db_path), "generations": payload}, indent=2))
        else:
            print(f"Generation history db={mem.db_path} ({len(payload)} rows)")
            for row in payload:
                print(
                    f"  #{row['id']} {row['outcome']} type={row['mission_type']} "
                    f"spec={row['spec_path']}"
                )
        return 0

    # default: list
    prefs = mem.get_prefs()
    if args.json:
        print(json.dumps({"db_path": str(mem.db_path), "prefs": prefs}, indent=2))
    elif not prefs:
        print(f"No prefs set db={mem.db_path}")
    else:
        print(f"Prefs db={mem.db_path}")
        for key, value in sorted(prefs.items()):
            print(f"  {key}={value!r}")
    return 0


def _prefs_root_cmd(_args: argparse.Namespace) -> int:
    print("Usage: dcs-miz prefs {list,set,history} ...", file=sys.stderr)
    return 2


def _feedback_cmd(args: argparse.Namespace) -> int:
    mem = UserMemoryService(db_path=args.db if args.db else None)
    if args.score is None and not (args.note or "").strip():
        print("Provide --score and/or --note", file=sys.stderr)
        return 2
    fid = mem.record_feedback(
        source="cli",
        generation_id=args.generation_id,
        score=args.score,
        note=args.note,
    )
    if args.json:
        print(
            json.dumps(
                {
                    "db_path": str(mem.db_path),
                    "feedback_id": fid,
                    "generation_id": args.generation_id,
                    "score": args.score,
                    "note": args.note,
                },
                indent=2,
            )
        )
    else:
        print(f"Recorded feedback #{fid} db={mem.db_path}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dcs-miz",
        description=(
            "DCS Mission Spec compiler, validator, theatre inventory, catalog, "
            "user prefs, and NL planner."
        ),
    )
    sub = parser.add_subparsers(dest="command")

    compile_p = sub.add_parser("compile", help="Compile a Mission Spec YAML into a .miz")
    compile_p.add_argument("spec", help="Path to a Mission Spec YAML file")
    compile_p.add_argument(
        "-o",
        "--output",
        help="Output .miz path (default: out/<spec-stem>.miz)",
        default=None,
    )
    compile_p.add_argument(
        "--voice",
        help=("Squadron voice for .miz briefing text: raf | usaaf | neutral (default: raf)"),
        default=None,
    )
    compile_p.set_defaults(func=_compile_cmd)

    validate_p = sub.add_parser(
        "validate",
        help="Validate a Mission Spec without compiling",
    )
    validate_p.add_argument("spec", help="Path to a Mission Spec YAML file")
    validate_p.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    validate_p.set_defaults(func=_validate_cmd)

    randomize_p = sub.add_parser(
        "randomize",
        help="Seeded Spec→Spec variation for replayability (writes YAML)",
    )
    randomize_p.add_argument("spec", help="Path to a base Mission Spec YAML file")
    randomize_p.add_argument(
        "--seed",
        type=int,
        required=True,
        help="Non-negative integer seed (same seed → same Spec)",
    )
    randomize_p.add_argument(
        "--axes",
        default=None,
        help="Comma-separated axes: weather,time,geometry,opposition (default: all)",
    )
    randomize_p.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output YAML path (default: out/<stem>_seed<N>.yaml)",
    )
    randomize_p.add_argument(
        "--annotate",
        action="store_true",
        help='Append "(seed N)" to description',
    )
    randomize_p.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip validation before write (debug only)",
    )
    randomize_p.set_defaults(func=_randomize_cmd)

    theatres_p = sub.add_parser(
        "theatres",
        help="List local DCS theatres from SQLite cache (use --refresh to rescan)",
    )
    theatres_p.add_argument("--dcs-root", help="Explicit DCS install root")
    theatres_p.add_argument("--saved-games", help="Explicit Saved Games DCS profile root")
    theatres_p.add_argument(
        "--db",
        help=f"SQLite inventory path (default: {default_db_path()})",
    )
    theatres_p.add_argument(
        "--refresh",
        action="store_true",
        help="Rescan the DCS install and update the SQLite inventory",
    )
    theatres_p.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    theatres_p.set_defaults(func=_theatres_cmd)

    catalog_p = sub.add_parser(
        "catalog",
        help="Sync/list known agent catalog (YAML + Spec enums; joins install for theatres)",
    )
    catalog_p.set_defaults(func=_catalog_root_cmd)
    catalog_sub = catalog_p.add_subparsers(dest="catalog_command")

    sync_p = catalog_sub.add_parser(
        "sync",
        help="Replace known catalog_* tables from packaged Channel YAML + Spec enums",
    )
    sync_p.add_argument(
        "--db",
        help=f"SQLite path shared with install inventory (default: {default_db_path()})",
    )
    sync_p.set_defaults(func=_catalog_sync_cmd)

    list_p = catalog_sub.add_parser(
        "list",
        help="List catalog rows (theatres include install discovery unless --known-only)",
    )
    list_p.add_argument(
        "--type",
        choices=LIST_TYPES,
        default="theatres",
        help="Resource type to list (default: theatres)",
    )
    list_p.add_argument(
        "--known-only",
        action="store_true",
        help="For theatres: omit discovered-only install theatres",
    )
    list_p.add_argument(
        "--family",
        help="For planning_options: filter by family (e.g. weather, time_of_day)",
    )
    list_p.add_argument(
        "--support",
        choices=("supported", "advisory", "future"),
        help="For planning_options: filter by support level",
    )
    list_p.add_argument(
        "--db",
        help=f"SQLite path shared with install inventory (default: {default_db_path()})",
    )
    list_p.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    list_p.set_defaults(func=_catalog_list_cmd)

    plan_p = sub.add_parser(
        "plan",
        help="Natural language → Mission Spec (uses LLM tools; --stub for offline)",
    )
    plan_p.add_argument("prompt", help="Natural-language mission request")
    plan_p.add_argument(
        "-o",
        "--output",
        help="Output Mission Spec YAML (default: out/planned.yaml)",
        default=None,
    )
    plan_p.add_argument(
        "--stub",
        action="store_true",
        help="Offline stub LLM (no API key; canned Manston free-flight Spec)",
    )
    plan_p.add_argument(
        "--compile",
        action="store_true",
        help="Also compile the planned Spec to a .miz",
    )
    plan_p.add_argument(
        "--miz",
        help="Output .miz path when using --compile (default: same stem as Spec)",
        default=None,
    )
    plan_p.add_argument(
        "--db",
        help=f"SQLite path for user memory / catalog (default: {default_db_path()})",
    )
    plan_p.add_argument(
        "--voice",
        help=(
            "Squadron voice for this run: raf | usaaf | neutral "
            "(default: pref squadron_voice, else raf)"
        ),
        default=None,
    )
    plan_p.add_argument(
        "--verbose",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Trace LLM rounds and tool calls on stderr (default: on; --no-verbose to quiet)",
    )
    plan_p.set_defaults(func=_plan_cmd)

    chat_p = sub.add_parser(
        "chat",
        help="Interactive multi-turn plan chat (REPL); /accept writes Spec",
    )
    chat_p.add_argument(
        "-o",
        "--output",
        help="Output Mission Spec YAML on /accept (default: out/planned.yaml)",
        default=None,
    )
    chat_p.add_argument(
        "--stub",
        action="store_true",
        help="Offline stub LLM (scripted clarify → Spec; no API key)",
    )
    chat_p.add_argument(
        "--compile",
        action="store_true",
        help="Also compile to .miz when accepting (/accept or /compile)",
    )
    chat_p.add_argument(
        "--miz",
        help="Output .miz path when compiling (default: same stem as Spec)",
        default=None,
    )
    chat_p.add_argument(
        "--db",
        help=f"SQLite path for user memory / catalog (default: {default_db_path()})",
    )
    chat_p.add_argument(
        "--voice",
        help="Squadron voice: raf | usaaf | neutral",
        default=None,
    )
    chat_p.add_argument(
        "--verbose",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Trace LLM rounds and tool calls on stderr (default: on; --no-verbose to quiet)",
    )
    chat_p.set_defaults(func=_chat_cmd)

    prefs_p = sub.add_parser(
        "prefs",
        help="List/set user preferences or show generation history",
    )
    prefs_p.set_defaults(func=_prefs_root_cmd, prefs_command=None)
    prefs_sub = prefs_p.add_subparsers(dest="prefs_command")

    prefs_list = prefs_sub.add_parser("list", help="List stored preferences")
    prefs_list.add_argument(
        "--db",
        help=f"SQLite path (default: {default_db_path()})",
    )
    prefs_list.add_argument("--json", action="store_true", help="Machine-readable JSON")
    prefs_list.set_defaults(func=_prefs_cmd)

    prefs_set = prefs_sub.add_parser("set", help="Set one preference key")
    prefs_set.add_argument(
        "key",
        help="Preference key (e.g. preferred_airfield, squadron_voice=raf|usaaf|neutral)",
    )
    prefs_set.add_argument(
        "value",
        help="Value (JSON if parseable, otherwise raw string)",
    )
    prefs_set.add_argument(
        "--db",
        help=f"SQLite path (default: {default_db_path()})",
    )
    prefs_set.add_argument("--json", action="store_true", help="Machine-readable JSON")
    prefs_set.set_defaults(func=_prefs_cmd)

    prefs_hist = prefs_sub.add_parser("history", help="List recent generation history")
    prefs_hist.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Max rows (default 20)",
    )
    prefs_hist.add_argument(
        "--db",
        help=f"SQLite path (default: {default_db_path()})",
    )
    prefs_hist.add_argument("--json", action="store_true", help="Machine-readable JSON")
    prefs_hist.set_defaults(func=_prefs_cmd)

    feedback_p = sub.add_parser(
        "feedback",
        help="Record satisfaction feedback for a generation",
    )
    feedback_p.add_argument("--score", type=int, help="Score (e.g. 1–5)")
    feedback_p.add_argument("--note", help="Free-text note")
    feedback_p.add_argument(
        "--generation-id",
        type=int,
        help="Optional generation history id to link",
    )
    feedback_p.add_argument(
        "--db",
        help=f"SQLite path (default: {default_db_path()})",
    )
    feedback_p.add_argument("--json", action="store_true", help="Machine-readable JSON")
    feedback_p.set_defaults(func=_feedback_cmd)

    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = _build_parser()

    # Legacy: `dcs-miz <spec.yaml> [-o ...]` without a subcommand.
    if (
        argv
        and not argv[0].startswith("-")
        and argv[0]
        not in {
            "compile",
            "validate",
            "randomize",
            "theatres",
            "catalog",
            "plan",
            "chat",
            "prefs",
            "feedback",
        }
    ):
        legacy = argparse.ArgumentParser(prog="dcs-miz")
        legacy.add_argument("spec")
        legacy.add_argument("-o", "--output", default=None)
        args = legacy.parse_args(argv)
        return _compile_cmd(args)

    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
