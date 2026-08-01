"""Refresh Manston CAP golden fixtures from a fresh compile.

Usage (from repo root):

    uv run python tests/refresh_cap_golden.py

Does not run during ordinary pytest.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from fixtures_support import CAP_FIXTURE_DIR, compile_cap, write_cap_golden


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        miz = compile_cap(Path(tmp) / "cap.miz")
        write_cap_golden(miz, CAP_FIXTURE_DIR)
    print(f"Wrote goldens under {CAP_FIXTURE_DIR}")


if __name__ == "__main__":
    main()
