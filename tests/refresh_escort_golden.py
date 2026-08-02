"""Refresh Manston escort golden fixtures from a live compile.

Usage (from repo root)::

    uv run python tests/refresh_escort_golden.py
"""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from fixtures_support import ESCORT_FIXTURE_DIR, compile_escort, write_escort_golden


def main() -> None:
    with TemporaryDirectory() as tmp:
        miz = compile_escort(Path(tmp) / "escort.miz")
        write_escort_golden(miz, ESCORT_FIXTURE_DIR)
    print(f"Wrote golden fixtures under {ESCORT_FIXTURE_DIR}")


if __name__ == "__main__":
    main()
