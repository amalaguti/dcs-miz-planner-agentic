"""Theatre-keyed intercept enemy spawn recipes.

TheChannel: Hawkinge map position plus Dover-approach offset — do not recompute
from ``airport_list()`` (golden ``x=30989.935547``, ``y=-35402.577148`` must
stay bit-identical).

Normandy: Needs Oar Point map position plus due-south 63 km (Cherbourg corridor;
same station as ``cherbourg_channel_cap``). Literals from PyDCS
``point_from_heading(180, 63000)`` — not invented lat/lon.

Caucasus: Batumi map position plus due-west 40 km (Black Sea corridor; same
station as ``batumi_black_sea_cap``). Literals from PyDCS
``point_from_heading(270, 40000)`` — not invented lat/lon.
"""

from __future__ import annotations

from dataclasses import dataclass

CHANNEL_THEATRE = "TheChannel"
NORMANDY_THEATRE = "Normandy"
CAUCASUS_THEATRE = "Caucasus"

# Source: PyDCS TheChannel airport Hawkinge (airdromeId 6) map position, offset
# south-east toward the Strait as a Dover-approach corridor (Channel geography
# relative to Manston id 5). Not invented lat/lon — terrain units from PyDCS.
_HAWKINGE_X = 26989.935547
_HAWKINGE_Y = -29402.577148
_DOVER_APPROACH_OFFSET_X = 4000.0
_DOVER_APPROACH_OFFSET_Y = -6000.0

# Source: PyDCS Normandy Needs Oar Point (airdromeId 28) + heading 180° / 63 km.
_NEEDS_OAR_POINT_X = 141296.390625
_NEEDS_OAR_POINT_Y = -84372.234375
_CHERBOURG_CORRIDOR_OFFSET_X = -63000.0
_CHERBOURG_CORRIDOR_OFFSET_Y = 0.0

# Source: PyDCS Caucasus Batumi (airdromeId 22) + heading 270° / 40 km.
_BATUMI_X = -355810.6875
_BATUMI_Y = 617386.1875
_BLACK_SEA_CORRIDOR_OFFSET_X = 0.0
_BLACK_SEA_CORRIDOR_OFFSET_Y = -40000.0


class InterceptUnsupportedTheatre(ValueError):
    """Raised when intercept spawn is requested for a theatre without a recipe."""

    code = "intercept_unsupported_theatre"


@dataclass(frozen=True)
class InterceptSpawnRecipe:
    anchor_x: float
    anchor_y: float
    offset_x: float
    offset_y: float

    @property
    def hawkinge_x(self) -> float:
        """Channel-test alias for :attr:`anchor_x`."""
        return self.anchor_x

    @property
    def hawkinge_y(self) -> float:
        """Channel-test alias for :attr:`anchor_y`."""
        return self.anchor_y

    @property
    def dover_offset_x(self) -> float:
        """Channel-test alias for :attr:`offset_x`."""
        return self.offset_x

    @property
    def dover_offset_y(self) -> float:
        """Channel-test alias for :attr:`offset_y`."""
        return self.offset_y

    @property
    def enemy_x(self) -> float:
        return self.anchor_x + self.offset_x

    @property
    def enemy_y(self) -> float:
        return self.anchor_y + self.offset_y


INTERCEPT_SPAWN_RECIPES: dict[str, InterceptSpawnRecipe] = {
    CHANNEL_THEATRE: InterceptSpawnRecipe(
        anchor_x=_HAWKINGE_X,
        anchor_y=_HAWKINGE_Y,
        offset_x=_DOVER_APPROACH_OFFSET_X,
        offset_y=_DOVER_APPROACH_OFFSET_Y,
    ),
    NORMANDY_THEATRE: InterceptSpawnRecipe(
        anchor_x=_NEEDS_OAR_POINT_X,
        anchor_y=_NEEDS_OAR_POINT_Y,
        offset_x=_CHERBOURG_CORRIDOR_OFFSET_X,
        offset_y=_CHERBOURG_CORRIDOR_OFFSET_Y,
    ),
    CAUCASUS_THEATRE: InterceptSpawnRecipe(
        anchor_x=_BATUMI_X,
        anchor_y=_BATUMI_Y,
        offset_x=_BLACK_SEA_CORRIDOR_OFFSET_X,
        offset_y=_BLACK_SEA_CORRIDOR_OFFSET_Y,
    ),
}


def intercept_supported(theatre: str) -> bool:
    return theatre in INTERCEPT_SPAWN_RECIPES


def intercept_spawn_for_theatre(theatre: str) -> InterceptSpawnRecipe:
    recipe = INTERCEPT_SPAWN_RECIPES.get(theatre)
    if recipe is None:
        raise InterceptUnsupportedTheatre(
            f"Intercept spawn is not supported for theatre {theatre!r}"
        )
    return recipe
