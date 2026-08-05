"""Explicit Spec theatre id → PyDCS terrain factory (fail closed).

PyDCS imports stay inside factories so importing this module does not load PyDCS
until a terrain is requested.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class TheatreTerrainError(ValueError):
    """Raised when a Spec theatre has no PyDCS terrain binding."""


def _the_channel_terrain() -> Any:
    from dcs.terrain import TheChannel

    return TheChannel()


# Spec theatre id → zero-arg factory returning a PyDCS terrain instance.
_TERRAIN_FACTORIES: dict[str, Callable[[], Any]] = {
    "TheChannel": _the_channel_terrain,
}


def bound_theatre_ids() -> frozenset[str]:
    return frozenset(_TERRAIN_FACTORIES)


def terrain_for_theatre(theatre_id: str) -> Any:
    """Return a PyDCS terrain instance for ``theatre_id``, or raise."""
    factory = _TERRAIN_FACTORIES.get(theatre_id)
    if factory is None:
        known = ", ".join(sorted(_TERRAIN_FACTORIES)) or "(none)"
        raise TheatreTerrainError(
            f"No PyDCS terrain binding for theatre '{theatre_id}'. "
            f"Bound theatres: {known}. Add a binding before supporting this theatre."
        )
    return factory()
