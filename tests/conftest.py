"""Shared pytest fixtures.

Hermetic Channel inventory: CI runners (and any machine without a DCS install
cache) would otherwise fail validate/compile with ``install_inventory_unavailable``.
Tests that need a specific inventory still pass ``inventory=`` explicitly
(e.g. empty inventory diagnostic).
"""

from __future__ import annotations

import pytest
from fixtures_support import channel_available_inventory


@pytest.fixture(autouse=True)
def _hermetic_channel_inventory(monkeypatch: pytest.MonkeyPatch) -> None:
    inv = channel_available_inventory()
    monkeypatch.setattr(
        "dcs_miz_planner.validation.get_inventory",
        lambda **_kwargs: inv,
    )
