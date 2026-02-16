#!/usr/bin/python3
"""
Titulo: Localizador de assets y cargador de estilos
Descripción: Resuelve rutas de assets de forma independiente del CWD y carga estilos JSON.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import json
import os


@dataclass(frozen=True)
class AssetLayout:
    """Estructura de directorios de assets dentro del proyecto/paquete."""
    assets_dir: Path
    styles_dir: Path
    fonts_dir: Path


def _candidate_assets_dirs() -> list[Path]:
    """Devuelve candidatos a directorio 'assets' en orden de preferencia."""
    candidates: list[Path] = []

    env_root = os.environ.get("POPUP_PROY_ROOT")
    if env_root:
        candidates.append(Path(env_root) / "src" / "popups_dialog_gui" / "assets")

    # Fallback: assets junto al paquete (independiente del CWD)
    package_dir = Path(__file__).resolve().parent
    candidates.append(package_dir / "assets")

    return candidates


def resolve_asset_layout() -> AssetLayout:
    """Resuelve la ubicación real de assets y devuelve rutas normalizadas."""
    for assets_dir in _candidate_assets_dirs():
        styles_dir = assets_dir / "styles"
        fonts_dir = assets_dir / "fonts"
        if styles_dir.is_dir():
            return AssetLayout(
                assets_dir=assets_dir,
                styles_dir=styles_dir,
                fonts_dir=fonts_dir,
            )

    tried = [str(p) for p in _candidate_assets_dirs()]
    raise FileNotFoundError(
        "No se encontró el directorio de estilos. Se probaron estos 'assets':\n- "
        + "\n- ".join(tried)
    )


def load_style_bundle(style_id: str) -> dict[str, Any]:
    """
    Carga y fusiona estilos desde los JSON conocidos.

    Parameters
    ----------
    style_id:
        Identificador del estilo (p.ej. 'playful_childlike', 'formal').

    Returns
    -------
    dict[str, Any]
        Diccionario con la configuración final del estilo (fusionada).

    Raises
    ------
    FileNotFoundError
        Si no se localizan los assets/styles.
    KeyError
        Si el style_id no existe o faltan claves obligatorias del estilo resultante.
    """
    layout = resolve_asset_layout()

    json_files = [
        layout.styles_dir / "popup_gui.json",
        layout.styles_dir / "helpview.json",
        layout.styles_dir / "formulario.json",
    ]

    merged_by_file: dict[str, dict[str, Any]] = {}
    for path in json_files:
        if not path.exists():
            # Aviso no intrusivo: ayuda durante desarrollo
            print(f"**Warning**: No se encontró '{path}'")
            continue

        with path.open(encoding="utf-8") as file_handle:
            data = json.load(file_handle)

        # data se espera como: { "formal": {...}, "playful_childlike": {...}, ... }
        if not isinstance(data, dict):
            raise TypeError(f"El JSON '{path}' no contiene un objeto raíz (dict).")

        merged_by_file[path.name] = data

    if not merged_by_file:
        raise FileNotFoundError(
            "No se pudo cargar ningún JSON de estilos. Revisa la carpeta:\n"
            f"  {layout.styles_dir}"
        )

    # Fusionamos por estilo: se combinan claves de cada fichero para el mismo style_id
    style_result: dict[str, Any] = {}
    available_styles: set[str] = set()
    for _filename, style_map in merged_by_file.items():
        available_styles.update(style_map.keys())
        if style_id in style_map:
            section = style_map[style_id]
            if not isinstance(section, dict):
                raise TypeError(
                    f"El estilo '{style_id}' en '{_filename}' no es un objeto (dict)."
                )
            style_result |= section

    if style_id not in available_styles:
        raise KeyError(
            f"El estilo '{style_id}' no existe. Disponibles: {sorted(available_styles)}"
        )

    # Validación mínima para evitar KeyError tardíos en _load_style()
    required_keys = ["SetFlagAlert"]
    missing = [k for k in required_keys if k not in style_result]
    if missing:
        raise KeyError(
            "El estilo cargado no contiene claves obligatorias "
            f"{missing}. Claves disponibles: {sorted(style_result.keys())}"
        )

    return style_result


def resolve_font_path(font_relative_path: str) -> Path:
    """
    Resuelve una fuente TrueType dentro de assets/fonts.

    Parameters
    ----------
    font_relative_path:
        Ruta relativa dentro de la carpeta fonts, p.ej. 'arialbd.ttf'.

    Returns
    -------
    Path
        Ruta absoluta al fichero de fuente.
    """
    layout = resolve_asset_layout()
    return (layout.fonts_dir / font_relative_path).resolve()

