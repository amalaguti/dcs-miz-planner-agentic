"""R3 historical Spitfire inspiration cards — catalog + registry ids."""

from __future__ import annotations

from dcs_miz_planner.agent.prompts import compose_system_prompt
from dcs_miz_planner.catalog import CatalogService
from dcs_miz_planner.registry import get_channel_registry

HISTORICAL_IDS = (
    "circus_escort",
    "rodeo_sweep",
    "channel_stop_shipping",
    "noball_ski",
)


def test_catalog_lists_historical_inspiration_cards(tmp_path) -> None:
    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).sync()
    rows = CatalogService(db_path=db).list_rows("planning_options", family="mission_inspiration")
    by_id = {r["id"]: r for r in rows}
    for hid in HISTORICAL_IDS:
        assert hid in by_id, hid
        assert by_id[hid]["support"] == "advisory"


def test_historical_card_ids_resolve_in_registry() -> None:
    reg = get_channel_registry()
    assert reg.get_aircraft("MosquitoFBMkVI") is not None
    assert reg.get_aircraft("SpitfireLFMkIX").id == "SpitfireLFMkIX"
    assert reg.get_strike_unit("v1_launcher").domain == "land"
    assert reg.get_strike_unit("Schnellboot_type_S130").domain == "sea"
    assert reg.get_strike_unit("Uboat_VIIC").domain == "sea"


def test_planning_prompt_maps_historical_pattern_names() -> None:
    text = compose_system_prompt("raf")
    assert "circus_escort" in text
    assert "rodeo_sweep" in text
    assert "channel_stop_shipping" in text
    assert "noball_ski" in text
    assert "MosquitoFBMkVI" in text
    assert "v1_launcher" in text
