"""Public inventory API: cache-by-default, refresh on demand."""

from __future__ import annotations

from pathlib import Path

from .models import TheatreInventory
from .probe import probe_installations
from .store import InventoryStore, default_db_path


class InventoryService:
    """SQLite-backed theatre inventory with explicit refresh."""

    def __init__(
        self,
        *,
        db_path: Path | str | None = None,
        dcs_root: Path | str | None = None,
        saved_games: Path | str | None = None,
        env: dict[str, str] | None = None,
    ) -> None:
        self.db_path = Path(db_path) if db_path else default_db_path(env=env)
        self.dcs_root = dcs_root
        self.saved_games = saved_games
        self.env = env
        self._store = InventoryStore(self.db_path)

    def get(self) -> TheatreInventory:
        """Return cached inventory, scanning once if the DB is empty/missing."""
        cached = self._store.load()
        if cached is not None:
            return cached
        return self.refresh()

    def refresh(self) -> TheatreInventory:
        """Rescan disk and replace the SQLite inventory."""
        inventory = probe_installations(
            dcs_root=self.dcs_root,
            saved_games=self.saved_games,
            env=self.env,
        )
        self._store.replace(inventory)
        # Re-load so from_cache reflects storage; callers care about scanned_at.
        loaded = self._store.load()
        if loaded is None:  # pragma: no cover - replace just wrote
            return inventory
        # Preserve from_cache=False semantics for a just-refreshed result.
        return TheatreInventory(
            scanned_at=loaded.scanned_at,
            dcs_roots=loaded.dcs_roots,
            saved_games_roots=loaded.saved_games_roots,
            theatres=loaded.theatres,
            diagnostics=loaded.diagnostics,
            from_cache=False,
        )


def get_inventory(
    *,
    db_path: Path | str | None = None,
    dcs_root: Path | str | None = None,
    saved_games: Path | str | None = None,
    env: dict[str, str] | None = None,
) -> TheatreInventory:
    return InventoryService(
        db_path=db_path, dcs_root=dcs_root, saved_games=saved_games, env=env
    ).get()


def refresh_inventory(
    *,
    db_path: Path | str | None = None,
    dcs_root: Path | str | None = None,
    saved_games: Path | str | None = None,
    env: dict[str, str] | None = None,
) -> TheatreInventory:
    return InventoryService(
        db_path=db_path, dcs_root=dcs_root, saved_games=saved_games, env=env
    ).refresh()
