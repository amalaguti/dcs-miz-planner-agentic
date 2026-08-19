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


def _normandy_terrain() -> Any:
    from dcs.terrain import Normandy

    return Normandy()


def _caucasus_terrain() -> Any:
    from dcs.terrain import Caucasus

    return Caucasus()


def _syria_terrain() -> Any:
    from dcs.terrain import Syria

    return Syria()


def _nevada_terrain() -> Any:
    from dcs.terrain import Nevada

    return Nevada()


def _falklands_terrain() -> Any:
    from dcs.terrain import Falklands

    return Falklands()


def _kola_terrain() -> Any:
    from dcs.terrain import Kola

    return Kola()


# Spec theatre id → zero-arg factory returning a PyDCS terrain instance.
_TERRAIN_FACTORIES: dict[str, Callable[[], Any]] = {
    "TheChannel": _the_channel_terrain,
    "Normandy": _normandy_terrain,
    "Caucasus": _caucasus_terrain,
    "Syria": _syria_terrain,
    "Nevada": _nevada_terrain,
    "Falklands": _falklands_terrain,
    "Kola": _kola_terrain,
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
