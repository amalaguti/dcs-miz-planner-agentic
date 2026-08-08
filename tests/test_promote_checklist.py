"""Hermetic checks for durable process docs (#8e)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "docs" / "THEATRE_TARGET_PROMOTE.md"


def test_theatre_target_promote_checklist_present() -> None:
    assert CHECKLIST.is_file(), f"missing {CHECKLIST}"
    text = CHECKLIST.read_text(encoding="utf-8")
    assert "## A. New theatre" in text or "New theatre" in text
    assert "## B. New strike" in text or "New strike" in text
    assert "non-goals" in text.lower() or "Non-goals" in text
    assert "ME" in text or "Mission Editor" in text
    assert "auto-promot" in text.lower() or "Auto-promot" in text
    assert "list_strike_targets" in text or "catalog sync" in text
