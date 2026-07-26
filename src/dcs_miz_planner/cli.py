"""Command-line entrypoint: compile, validate, and list local theatres."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .compiler import PyDCSCompiler
from .install import InventoryService, default_db_path
from .loader import SpecLoadError, load_mission_spec
from .validation import validate_mission_spec

DEFAULT_OUTPUT_DIR = Path("out")


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

    output = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR / f"{spec_path.stem}.miz"
    try:
        written = PyDCSCompiler().compile(spec, output)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    print(f"Wrote {written}")
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


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dcs-miz",
        description="DCS Mission Spec compiler, validator, and local theatre inventory.",
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
    compile_p.set_defaults(func=_compile_cmd)

    validate_p = sub.add_parser(
        "validate",
        help="Validate a Mission Spec without compiling",
    )
    validate_p.add_argument("spec", help="Path to a Mission Spec YAML file")
    validate_p.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    validate_p.set_defaults(func=_validate_cmd)

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
            "theatres",
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
