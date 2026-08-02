"""Refresh Manston ground-attack golden fixtures from a live compile.

Usage (from repo root)::

    uv run python tests/refresh_ground_attack_golden.py
"""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from fixtures_support import GA_FIXTURE_DIR, compile_ground_attack, write_ground_attack_golden


def main() -> None:
    with TemporaryDirectory() as tmp:
        miz = compile_ground_attack(Path(tmp) / "ga.miz")
        write_ground_attack_golden(miz, GA_FIXTURE_DIR)
    print(f"Wrote golden fixtures under {GA_FIXTURE_DIR}")


if __name__ == "__main__":
    main()
