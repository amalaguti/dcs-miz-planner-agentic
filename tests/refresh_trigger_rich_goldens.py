"""Refresh trigger-rich Manston golden fixtures from fresh compiles.

Usage (from repo root):

    uv run python tests/refresh_trigger_rich_goldens.py

Does not run during ordinary pytest.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from fixtures_support import (
    GATES_FIXTURE_DIR,
    MARKERS_FIXTURE_DIR,
    RADIO_FIXTURE_DIR,
    SOUND_FLAGS_FIXTURE_DIR,
    compile_gates,
    compile_markers,
    compile_radio,
    compile_sound_flags,
    write_gates_golden,
    write_markers_golden,
    write_radio_golden,
    write_sound_flags_golden,
)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_radio_golden(compile_radio(root / "radio.miz"), RADIO_FIXTURE_DIR)
        write_gates_golden(compile_gates(root / "gates.miz"), GATES_FIXTURE_DIR)
        write_markers_golden(compile_markers(root / "markers.miz"), MARKERS_FIXTURE_DIR)
        write_sound_flags_golden(
            compile_sound_flags(root / "sound_flags.miz"), SOUND_FLAGS_FIXTURE_DIR
        )
    print("Wrote trigger-rich goldens under tests/fixtures/")


if __name__ == "__main__":
    main()
