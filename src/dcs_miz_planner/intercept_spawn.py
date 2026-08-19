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

Syria: Incirlik map position plus due-south 40 km (Gulf of Iskenderun corridor;
same station as ``incirlik_iskenderun_cap``). Literals from PyDCS
``point_from_heading(180, 40000)`` — not invented lat/lon.

Nevada: Nellis map position plus heading 350° / 40 km (desert north-range
corridor; same station as ``nellis_north_range_cap``). Literals from live
PyDCS ``point_from_heading(350, 40000)`` — not axis-aligned ±40000,0; do not
recompute Channel Hawkinge from ``airport_list()``.

Falklands: Mount Pleasant map position plus heading 150° / 40 km (South
Atlantic corridor; same station as ``mount_pleasant_south_atlantic_cap``).
Literals from live PyDCS ``point_from_heading(150, 40000)`` — not
axis-aligned ±40000,0; do not recompute Channel Hawkinge from
``airport_list()``.
"""

from __future__ import annotations

from dataclasses import dataclass

CHANNEL_THEATRE = "TheChannel"
NORMANDY_THEATRE = "Normandy"
CAUCASUS_THEATRE = "Caucasus"
SYRIA_THEATRE = "Syria"
NEVADA_THEATRE = "Nevada"
FALKLANDS_THEATRE = "Falklands"

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

# Source: PyDCS Syria Incirlik (airdromeId 16) + heading 180° / 40 km.
_INCIRLIK_X = 221207.773438
_INCIRLIK_Y = -35240.347656
_ISKENDERUN_CORRIDOR_OFFSET_X = -40000.0
_ISKENDERUN_CORRIDOR_OFFSET_Y = 0.0

# Source: live PyDCS Nevada Nellis (airdromeId 4, name "Nellis")
# x=-398195.375 y=-17233.236816 + heading 350° / 40 km.
# point_from_heading(350, 40000) station x=-358803.06487951166
# y=-24179.163922677217; offset is NOT axis-aligned (±40000, 0).
_NELLIS_X = -398195.375
_NELLIS_Y = -17233.236816
_NORTH_RANGE_CORRIDOR_OFFSET_X = 39392.31012048834
_NORTH_RANGE_CORRIDOR_OFFSET_Y = -6945.927106677216

# Source: live PyDCS Falklands Mount Pleasant (airdromeId 2, name "Mount Pleasant")
# x=73318.320313 y=47168.748047 + heading 150° / 40 km (pydcs git e20f328;
# 0.15.0 wheel was x=73318.320312 → dest 38677.30416062245).
# point_from_heading(150, 40000) station x=38677.30416162246
# y=67168.748047; offset is NOT axis-aligned (±40000, 0).
_MOUNT_PLEASANT_X = 73318.320313
_MOUNT_PLEASANT_Y = 47168.748047
_SOUTH_ATLANTIC_CORRIDOR_OFFSET_X = -34641.01615137754
_SOUTH_ATLANTIC_CORRIDOR_OFFSET_Y = 20000.0


class InterceptUnsupportedTheatre(ValueError):
    """Raised when intercept spawn is requested for a theatre without a recipe."""

    code = "intercept_unsupported_theatre"


@dataclass(frozen=True)
class InterceptSpawnRecipe:
    anchor_x: float
    anchor_y: float
    offset_x: float
    offset_y: float
    # When set, enemy spawn uses these map coords (bit-identical dump) instead
    # of anchor+offset, which can ULP-drift after pydcs airport re-exports.
    dest_x: float | None = None
    dest_y: float | None = None

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
        if self.dest_x is not None:
            return self.dest_x
        return self.anchor_x + self.offset_x

    @property
    def enemy_y(self) -> float:
        if self.dest_y is not None:
            return self.dest_y
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
    SYRIA_THEATRE: InterceptSpawnRecipe(
        anchor_x=_INCIRLIK_X,
        anchor_y=_INCIRLIK_Y,
        offset_x=_ISKENDERUN_CORRIDOR_OFFSET_X,
        offset_y=_ISKENDERUN_CORRIDOR_OFFSET_Y,
    ),
    NEVADA_THEATRE: InterceptSpawnRecipe(
        anchor_x=_NELLIS_X,
        anchor_y=_NELLIS_Y,
        offset_x=_NORTH_RANGE_CORRIDOR_OFFSET_X,
        offset_y=_NORTH_RANGE_CORRIDOR_OFFSET_Y,
    ),
    FALKLANDS_THEATRE: InterceptSpawnRecipe(
        anchor_x=_MOUNT_PLEASANT_X,
        anchor_y=_MOUNT_PLEASANT_Y,
        offset_x=_SOUTH_ATLANTIC_CORRIDOR_OFFSET_X,
        offset_y=_SOUTH_ATLANTIC_CORRIDOR_OFFSET_Y,
        dest_x=38677.30416162246,
        dest_y=67168.748047,
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
