"""Local DCS installation probe — theatres available on this machine."""

from __future__ import annotations

from .campaigns import (
    CampaignDocRef,
    CampaignIndex,
    CampaignMissionRef,
    CampaignSummary,
    index_installed_campaigns,
    scan_campaigns_root,
)
from .models import (
    AircraftModuleRecord,
    AvailabilityState,
    Diagnostic,
    TheatreInventory,
    TheatreRecord,
)
from .service import InventoryService, default_db_path, get_inventory, refresh_inventory

__all__ = [
    "AircraftModuleRecord",
    "AvailabilityState",
    "CampaignDocRef",
    "CampaignIndex",
    "CampaignMissionRef",
    "CampaignSummary",
    "Diagnostic",
    "InventoryService",
    "TheatreInventory",
    "TheatreRecord",
    "default_db_path",
    "get_inventory",
    "index_installed_campaigns",
    "refresh_inventory",
    "scan_campaigns_root",
]
