"""Refresh Manston dawn intercept golden fixtures from a fresh compile.

Usage (from repo root):

    uv run python tests/refresh_intercept_golden.py

Does not run during ordinary pytest.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from fixtures_support import INTERCEPT_FIXTURE_DIR, compile_intercept, write_intercept_golden


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        miz = compile_intercept(Path(tmp) / "intercept.miz")
        write_intercept_golden(miz, INTERCEPT_FIXTURE_DIR)
    print(f"Wrote goldens under {INTERCEPT_FIXTURE_DIR}")


if __name__ == "__main__":
    main()
