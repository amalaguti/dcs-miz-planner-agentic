"""Refresh Manston recon golden fixtures.

Usage (from repo root):

    uv run python tests/refresh_recon_golden.py
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures_support import RECON_FIXTURE_DIR, compile_recon, write_recon_golden


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        miz = compile_recon(Path(tmp) / "recon.miz")
        write_recon_golden(miz, RECON_FIXTURE_DIR)
    print(f"Wrote golden fixtures under {RECON_FIXTURE_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
