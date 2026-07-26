"""Command-line entrypoint: compile a Mission Spec YAML into a .miz."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .compiler import PyDCSCompiler
from .loader import SpecLoadError, load_mission_spec

DEFAULT_OUTPUT_DIR = Path("out")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="dcs-miz",
        description="Compile a Mission Spec YAML into a DCS .miz file.",
    )
    parser.add_argument("spec", help="Path to a Mission Spec YAML file")
    parser.add_argument(
        "-o",
        "--output",
        help="Output .miz path (default: out/<spec-stem>.miz)",
        default=None,
    )
    args = parser.parse_args(argv)

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

    written = PyDCSCompiler().compile(spec, output)
    print(f"Wrote {written}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
