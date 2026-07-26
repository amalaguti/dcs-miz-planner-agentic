"""Minimal reference data for the Manston free-flight slice.

Full Channel registry is backlog item `reference-registry-channel` (M2).
Values verified from the local DCS install / sample missions.
"""

from __future__ import annotations

# The Channel airfield display name -> DCS airdromeId.
CHANNEL_AIRDROME_IDS: dict[str, int] = {
    "Abbeville": 1,
    "MervilleCalonne": 2,
    "SaintOmer": 3,
    "Dunkirk": 4,
    "Manston": 5,
    "Hawkinge": 6,
    "Lympne": 7,
    "Detling": 8,
    "Eastchurch": 10,
    "HighHalden": 12,
    "Headcorn": 13,
    "BigginHill": 14,
}

# Verified exact DCS type ids (do not invent alternate spellings).
KNOWN_AIRCRAFT: frozenset[str] = frozenset(
    {"SpitfireLFMkIX", "SpitfireLFMkIXCW", "Bf-109K-4", "FW-190A8", "FW-190D9"}
)

# Intra-flight radio channel (MHz) per aircraft, taken from the stock DCS
# Channel missions. PyDCS defaults every group to 251 MHz, which WWII radios
# cannot tune: Allied VHF is ~100-156 MHz, German VHF ~38.4-42.4 MHz.
AIRCRAFT_RADIO_MHZ: dict[str, float] = {
    "SpitfireLFMkIX": 124.0,
    "SpitfireLFMkIXCW": 124.0,
    "Bf-109K-4": 40.0,
    "FW-190A8": 38.4,
    "FW-190D9": 38.4,
}

SUPPORTED_THEATRES: frozenset[str] = frozenset({"TheChannel"})


def radio_frequency_mhz(aircraft: str) -> float:
    try:
        return AIRCRAFT_RADIO_MHZ[aircraft]
    except KeyError as exc:
        raise KeyError(
            f"No radio frequency known for aircraft '{aircraft}'. "
            f"Known: {sorted(AIRCRAFT_RADIO_MHZ)}"
        ) from exc


def airdrome_id(theatre: str, airfield_name: str) -> int:
    if theatre != "TheChannel":
        raise KeyError(f"Unsupported theatre for airfield lookup: {theatre}")
    try:
        return CHANNEL_AIRDROME_IDS[airfield_name]
    except KeyError as exc:
        raise KeyError(
            f"Unknown Channel airfield '{airfield_name}'. Known: {sorted(CHANNEL_AIRDROME_IDS)}"
        ) from exc
