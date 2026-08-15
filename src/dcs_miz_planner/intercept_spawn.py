"""Theatre-keyed intercept enemy spawn recipes.

Only TheChannel has a recipe. Literals are the checked-in Hawkinge map position
plus Dover-approach offset — do not recompute from ``airport_list()`` (golden
``x=30989.935547``, ``y=-35402.577148`` must stay bit-identical).
"""

from __future__ import annotations

from dataclasses import dataclass

CHANNEL_THEATRE = "TheChannel"

# Source: PyDCS TheChannel airport Hawkinge (airdromeId 6) map position, offset
# south-east toward the Strait as a Dover-approach corridor (Channel geography
# relative to Manston id 5). Not invented lat/lon — terrain units from PyDCS.
_HAWKINGE_X = 26989.935547
_HAWKINGE_Y = -29402.577148
_DOVER_APPROACH_OFFSET_X = 4000.0
_DOVER_APPROACH_OFFSET_Y = -6000.0


class InterceptUnsupportedTheatre(ValueError):
    """Raised when intercept spawn is requested for a theatre without a recipe."""

    code = "intercept_unsupported_theatre"


@dataclass(frozen=True)
class InterceptSpawnRecipe:
    hawkinge_x: float
    hawkinge_y: float
    dover_offset_x: float
    dover_offset_y: float

    @property
    def enemy_x(self) -> float:
        return self.hawkinge_x + self.dover_offset_x

    @property
    def enemy_y(self) -> float:
        return self.hawkinge_y + self.dover_offset_y


INTERCEPT_SPAWN_RECIPES: dict[str, InterceptSpawnRecipe] = {
    CHANNEL_THEATRE: InterceptSpawnRecipe(
        hawkinge_x=_HAWKINGE_X,
        hawkinge_y=_HAWKINGE_Y,
        dover_offset_x=_DOVER_APPROACH_OFFSET_X,
        dover_offset_y=_DOVER_APPROACH_OFFSET_Y,
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
