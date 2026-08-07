"""Emit Spec failures into the mission Failures table (ME player failures panel).

Stock Channel/Spitfire missions arm failures via ``mission.failures``
(``enable`` / After ``hh``+``mm`` / Within ``mmint`` / ``prob``), not
``a_set_failure``. ME labels Within as ``(mm)`` = minutes. Within ``0`` is a
zero-width window and effectively never fires — ED defaults ``mmint`` to 1.
"""

from __future__ import annotations

from typing import Any

from ..models import FailureEvent, MissionSpec


def _after_hh_mm(start_after_s: int) -> tuple[int, int]:
    """Map Spec seconds to ME After hh:mm (minute resolution, floored)."""
    total_min = max(0, int(start_after_s)) // 60
    return total_min // 60, total_min % 60


def _within_minutes(random_pause_s: int) -> int:
    """Map Spec random_pause_s to ME Within minutes (minimum 1)."""
    minutes = (max(0, int(random_pause_s)) + 59) // 60
    return max(1, minutes)


def failure_table_entry(event: FailureEvent) -> dict[str, Any]:
    """Build one stock-shaped ``mission.failures`` row."""
    hh, mm = _after_hh_mm(event.start_after_s)
    return {
        "id": str(event.id),
        "enable": True,
        "prob": int(event.probability),
        "hh": hh,
        "mm": mm,
        "mmint": _within_minutes(event.random_pause_s),
    }


def apply_aircraft_failures(mission: Any, spec: MissionSpec) -> None:
    """Write enabled entries into ``mission.failures`` (PyDCS dump → .miz)."""
    if not spec.failures:
        return

    table: dict[str, Any] = dict(getattr(mission, "failures", None) or {})
    for event in spec.failures:
        table[str(event.id)] = failure_table_entry(event)
    mission.failures = table
