"""Packaged ME gallery metadata (METAR decode + base clamps beyond PyDCS enum)."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_DATA = Path(__file__).resolve().parent / "data" / "channel" / "weather_gallery.yaml"


@dataclass(frozen=True)
class MetarLayer:
    code: str
    base_100ft: str


@dataclass(frozen=True)
class GalleryPresetMeta:
    name: str
    min_base: int
    max_base: int
    metar_layers: tuple[MetarLayer, ...]
    precip: str | None = None


@lru_cache(maxsize=1)
def load_gallery_presets() -> dict[str, GalleryPresetMeta]:
    raw = yaml.safe_load(_DATA.read_text(encoding="utf-8")) or {}
    presets_raw = raw.get("presets") or {}
    if not isinstance(presets_raw, dict):
        raise TypeError("weather_gallery.yaml: 'presets' must be a mapping")
    out: dict[str, GalleryPresetMeta] = {}
    for name, meta in presets_raw.items():
        if not isinstance(meta, dict):
            raise TypeError(f"weather_gallery.yaml: {name!r} must be a mapping")
        layers_raw = meta.get("metar_layers") or []
        if not isinstance(layers_raw, list):
            raise TypeError(f"weather_gallery.yaml: {name!r} metar_layers must be a list")
        layers: list[MetarLayer] = []
        for row in layers_raw:
            if not isinstance(row, dict):
                raise TypeError(f"weather_gallery.yaml: {name!r} layer must be a mapping")
            layers.append(MetarLayer(code=str(row["code"]), base_100ft=str(row["base_100ft"])))
        precip = meta.get("precip")
        out[str(name)] = GalleryPresetMeta(
            name=str(name),
            min_base=int(meta["min_base"]),
            max_base=int(meta["max_base"]),
            metar_layers=tuple(layers),
            precip=str(precip) if precip else None,
        )
    return out


def gallery_preset_meta(name: str) -> GalleryPresetMeta | None:
    return load_gallery_presets().get(name)


def resolve_cloud_preset(name: str) -> Any:
    """Return a PyDCS ``CloudPreset`` for ``name``, including ME-only rainy light ids.

    Prefer ``CloudPreset.by_name`` when PyDCS knows the id; otherwise construct from
    packaged ``weather_gallery.yaml`` min/max so ``_make_cloud_dict`` can still emit
    the gallery string DCS expects.
    """
    from dcs.weather import CloudPreset

    try:
        return CloudPreset.by_name(name)
    except KeyError:
        meta = gallery_preset_meta(name)
        if meta is None:
            raise ValueError(f"Unknown weather cloud_preset {name!r}") from None
        return CloudPreset(
            name=meta.name,
            ui_name=meta.name,
            description=meta.name,
            min_base=meta.min_base,
            max_base=meta.max_base,
        )


__all__ = [
    "GalleryPresetMeta",
    "MetarLayer",
    "gallery_preset_meta",
    "load_gallery_presets",
    "resolve_cloud_preset",
]
