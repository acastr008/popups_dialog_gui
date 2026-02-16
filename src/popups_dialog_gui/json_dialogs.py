# Archivo sugerido: popup_gui/json_dialogs.py
# -*- coding: utf-8 -*-

"""
Este módulo aún no ha sido utilizado. 
Servira para salvar y guardar diccionarios de datos en ficheros json.
"""

import os
import json
import tempfile
from pathlib import Path
import pygame

from popup_gui.Popup_Dialog import (
    PopupSelectionFiles, PopupASK, PopupINFO, PopupERR,
    PopupDialogWindow
)

# =========
# Guardar (Opción A)
# =========
def SaveDataJson(MainScreen, DictData, PathJsonFile, Title, Comment):
    """
    Guarda DictData como JSON añadiendo metadatos { _meta: {title, comment}, data: ... }.
    - Si PathJsonFile es vacío o None, abre un selector de archivo (modo guardar).
    - Si el archivo existe, solicita confirmación para sobrescribir.
    - Escritura atómica (tmp + rename), UTF-8, indent=2.
    Retorna True si guardó correctamente, False si se canceló o falló.
    """
    try:
        # 1) Verificar serialización
        try:
            json.dumps(DictData)
        except Exception as e:
            PopupERR(f"No se puede serializar el diccionario a JSON:\n{e}")
            return False

        # 2) Resolver ruta destino
        path = Path(PathJsonFile) if PathJsonFile else None
        if not path:
            # Selector en modo guardar; idealmente tu PopupSelectionFiles lo soporta
            sel = PopupSelectionFiles(
                MainScreen,
                Title="Guardar datos como JSON",
                Mode="save",              # depende de tu implementación
                Filter="*.json",          # sugerencia de filtro
                SuggestName="data.json"   # puedes ajustar
            )
            if not sel:
                return False
            path = Path(sel)

        # Asegurar extensión .json
        if path.suffix.lower() != ".json":
            path = path.with_suffix(".json")

        # 3) Confirmar sobrescritura si existe
        if path.exists():
            ans = PopupASK(f"El archivo ya existe:\n{path}\n\n¿Deseas sobrescribirlo?")
            if not (isinstance(ans, str) and ans.lower().startswith("s")):
                return False

        # 4) Preparar estructura
        payload = {
            "_meta": {
                "title": Title or "",
                "comment": Comment or ""
            },
            "data": DictData
        }

        # 5) Escritura atómica
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", delete=False, dir=str(path.parent), encoding="utf-8") as tmp:
            json.dump(payload, tmp, ensure_ascii=False, indent=2)
            tmp.flush()
            os.fsync(tmp.fileno())
            tmp_name = tmp.name

        os.replace(tmp_name, str(path))

        PopupINFO(f"Guardado correcto:\n{path}")
        return True

    except Exception as e:
        try:
            PopupERR(f"Error al guardar:\n{e}")
        finally:
            return False


# =========
# Cargar (Opción B con vista previa tipo “Surface Selector”)
# =========
def LoadData(MainScreen, PathDirJsonFiles):
    """
    Muestra una vista previa navegable de los JSON en PathDirJsonFiles:
    - Escanea *.json, extrae metadatos (title/comment) para previsualización.
    - Permite navegar con Anterior/Posterior y Seleccionar/Cancelar (PopupDialogWindow).
    - Al seleccionar, abre y retorna (DictData, Title, Comment).
    - Si se cancela o hay error, retorna (None, None, None).
    """
    try:
        base_dir = Path(PathDirJsonFiles) if PathDirJsonFiles else Path(".")
        files = sorted([p for p in base_dir.glob("*.json") if p.is_file()])
        if not files:
            PopupERR(f"No se encontraron archivos JSON en:\n{base_dir}")
            return (None, None, None)

        # Pre-cargar metadatos mínimos para preview
        previews = []
        for p in files:
            title, comment = _peek_meta(p)
            surf = _make_preview_surface(p.name, title, comment, size=(700, 300))
            # (surface, ident, filepath) — usaremos el ident como título del popup
            ident = f"<<<<< {title or p.stem} >>>>>"
            previews.append((surf, ident, p))

        # Navegación tipo Surface Selector (Anterior/Posterior/Cancelar/Seleccionar)
        idx = 0
        while True:
            surface, ident, filepath = previews[idx]

            labels = []
            if idx > 0:
                labels.append("Anterior")
            if idx < len(previews) - 1:
                labels.append("Posterior")
            labels.extend(["Cancelar", "Seleccionar"])

            popup = PopupDialogWindow(
                surface,
                labels,
                Title=ident,
                FlagAlert="Blue"
            )
            raw = popup.Run()
            choice = _resolve_button_label(raw, labels) or ""

            if choice == "Anterior" and idx > 0:
                idx -= 1
                continue
            if choice == "Posterior" and idx < len(previews) - 1:
                idx += 1
                continue
            if choice == "Seleccionar":
                # Abrir completo y devolver
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    meta = data.get("_meta", {}) if isinstance(data, dict) else {}
                    title = meta.get("title", "")
                    comment = meta.get("comment", "")
                    dict_data = data.get("data", data if isinstance(data, dict) else None)
                    if dict_data is None or not isinstance(dict_data, (dict, list)):
                        # Aceptamos list/dict como raíz de "data"; si no, intento fallback
                        dict_data = data
                    return (dict_data, title, comment)
                except Exception as e:
                    PopupERR(f"No se pudo abrir el archivo:\n{filepath}\n\n{e}")
                    return (None, None, None)

            if choice == "Cancelar" or choice == "":
                return (None, None, None)

    except Exception as e:
        try:
            PopupERR(f"Error al cargar:\n{e}")
        finally:
            return (None, None, None)


# =========
# Helpers internos
# =========
def _peek_meta(path: Path):
    """Lee solo metadatos _meta.title/comment si existen. Fallback a nombre de archivo."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "_meta" in data and isinstance(data["_meta"], dict):
            title = data["_meta"].get("title", "") or path.stem
            comment = data["_meta"].get("comment", "")
        else:
            title, comment = path.stem, ""
        return title, comment
    except Exception:
        return path.stem, "(No legible / JSON inválido)"

def _make_preview_surface(filename, title, comment, size=(700, 300)):
    """Genera una Surface con preview de metadatos."""
    w, h = size
    surf = pygame.Surface((w, h))
    bg = (18, 22, 28)
    fg = (240, 240, 240)
    accent = (70, 130, 180)
    surf.fill(bg)

    # Marcos simples
    pygame.draw.rect(surf, accent, (0, 0, w, h), width=2, border_radius=10)

    # Fuentes (robustas para distintos tamaños)
    title_font = pygame.font.SysFont("Arial", max(16, w // 28), bold=True)
    small_font = pygame.font.SysFont("Arial", max(12, w // 40))

    # Líneas de texto
    title_text = f"{title}".strip() or "(Sin título)"
    file_line = f"Archivo: {filename}"
    comment = (comment or "").strip()

    # Render
    y = 18
    _blit_text_line(surf, title_font, title_text, (16, y), fg); y += title_font.get_height() + 8
    _blit_text_line(surf, small_font, file_line, (16, y), fg); y += small_font.get_height() + 10

    # Comentario con wrap sencillo
    wrap_w = w - 32
    for line in _wrap_text(comment or "(Sin comentario)", small_font, wrap_w):
        _blit_text_line(surf, small_font, line, (16, y), fg)
        y += small_font.get_height() + 4
        if y > h - 16:
            break

    return surf

def _wrap_text(text, font, max_w):
    """Quebra texto simple por palabras para no exceder max_w."""
    words = text.split()
    lines, current = [], ""
    for w in words:
        test = f"{current} {w}".strip()
        if font.size(test)[0] <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines

def _blit_text_line(surface, font, text, pos, color):
    img = font.render(text, True, color)
    surface.blit(img, pos)

def _resolve_button_label(raw_response, labels):
    """Intenta resolver la etiqueta del botón pulsado desde distintos formatos."""
    if isinstance(raw_response, str):
        return raw_response
    if isinstance(raw_response, int):
        return labels[raw_response] if 0 <= raw_response < len(labels) else None
    if isinstance(raw_response, dict):
        for k in ("button", "label", "name"):
            v = raw_response.get(k)
            if isinstance(v, str):
                return v
    return None

