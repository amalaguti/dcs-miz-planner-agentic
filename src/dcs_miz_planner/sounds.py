"""Curated sound-asset registry for Spec ``sound`` actions (no arbitrary paths)."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any

import yaml

from .registry import RegistryError

_MATERIALIZED: dict[str, Path] = {}


@dataclass(frozen=True)
class SoundAssetRef:
    """Known sound asset embeddable into a ``.miz``."""

    id: str
    file: str
    description: str = ""


def _load_yaml() -> dict[str, Any]:
    root = resources.files("dcs_miz_planner.data.sounds")
    text = (root / "sounds.yaml").read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise RegistryError("sounds.yaml must be a mapping")
    return data


@lru_cache(maxsize=1)
def _assets() -> dict[str, SoundAssetRef]:
    data = _load_yaml()
    raw = data.get("assets") or {}
    if not isinstance(raw, dict):
        raise RegistryError("sounds.yaml 'assets' must be a mapping")
    out: dict[str, SoundAssetRef] = {}
    for asset_id, meta in raw.items():
        if not isinstance(meta, dict) or "file" not in meta:
            raise RegistryError(f"Sound asset {asset_id!r} must have a 'file' field")
        out[str(asset_id)] = SoundAssetRef(
            id=str(asset_id),
            file=str(meta["file"]),
            description=str(meta.get("description") or ""),
        )
    return out


def list_sound_assets() -> list[str]:
    """Sorted known ``asset_id`` values."""
    return sorted(_assets())


def get_sound_asset(asset_id: str) -> SoundAssetRef:
    """Resolve a curated sound asset by id."""
    assets = _assets()
    if asset_id not in assets:
        raise RegistryError(
            f"Unknown sound asset_id {asset_id!r}; known: {sorted(assets) or '(none)'}"
        )
    return assets[asset_id]


def resolve_sound_path(asset_id: str) -> Path:
    """Path to audio bytes for ``asset_id`` (materialized; safe until process exit).

    PyDCS ``MapResource`` needs a filesystem path that still exists at ``mission.save``.
    Packaged wheel members are copied into a stable temp file once per asset id.
    """
    cached = _MATERIALIZED.get(asset_id)
    if cached is not None and cached.is_file():
        return cached

    ref = get_sound_asset(asset_id)
    blob = (resources.files("dcs_miz_planner.data.sounds") / ref.file).read_bytes()
    suffix = Path(ref.file).suffix or ".wav"
    dest = Path(tempfile.gettempdir()) / f"dcs_miz_planner_sound_{asset_id}{suffix}"
    dest.write_bytes(blob)
    _MATERIALIZED[asset_id] = dest
    return dest
