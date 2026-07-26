"""Refresh Manston free-flight golden fixtures from a fresh compile.

Usage (from repo root):

    uv run python tests/refresh_manston_golden.py

Does not run during ordinary pytest.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from fixtures_support import FIXTURE_DIR, compile_manston, write_manston_golden


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        miz = compile_manston(Path(tmp) / "manston.miz")
        write_manston_golden(miz, FIXTURE_DIR)
    print(f"Wrote goldens under {FIXTURE_DIR}")


if __name__ == "__main__":
    main()
