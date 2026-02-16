# popup_gui/persistence_json.py
#===============================================================================
#:::Paso6
# Utilidades de Persistencia (Save/Load) en JSON (+ JSON.gz) en un módulo independiente.
# - SaveDataJson(data, path, filename=None, gzip=None, ...)  -> guarda en .json o .json.gz (atómico)
# - LoadData(path_or_dir, filename=None, ...)                -> carga desde fichero o, si es directorio, del
#                                                              fichero JSON más reciente (.json / .json.gz)
# Notas:
#   * Si 'path' en LoadData es un directorio, se interpreta como el directorio que contiene los datos JSON.
#   * Extensiones válidas: '.json' y '.json.gz'.
#   * Escritura atómica (tmp + os.replace) para evitar ficheros corruptos.
#   * Codificación UTF-8, ensure_ascii=False, allow_nan=False para JSON estricto.
#===============================================================================

from __future__ import annotations

import json
import gzip
import os
import io
import tempfile
from typing import Any, Iterable, Optional, Tuple

__all__ = [
    "SaveDataJson",
    "LoadData",
    "ListJsonFiles",
    "IsJsonFilename",
    "PickLatestJson",
]


#-----------------------------------------------------------------------------#
# Helpers de rutas y validación de extensión
#-----------------------------------------------------------------------------#

_VALID_EXTS: Tuple[str, ...] = (".json", ".json.gz")


def _expand_path(path: str) -> str:
    """Expande ~ y variables de entorno y devuelve ruta absoluta normalizada."""
    return os.path.abspath(os.path.expandvars(os.path.expanduser(path)))


def IsJsonFilename(name: str) -> bool:
    """Devuelve True si el nombre acaba en '.json' o '.json.gz' (extensiones válidas)."""
    name = name.lower()
    return any(name.endswith(ext) for ext in _VALID_EXTS)


def _infer_gzip_from_name(name: str, gzip_flag: Optional[bool]) -> bool:
    """
    Si gzip_flag es None, infiere por extensión (.json.gz -> True, .json -> False).
    Si gzip_flag es bool, lo respeta (y valida que la extensión sea coherente si existe).
    """
    lower = name.lower()
    if gzip_flag is None:
        return lower.endswith(".json.gz")
    return gzip_flag


def _ensure_dir_exists(dirpath: str) -> None:
    """Crea el directorio si no existe."""
    os.makedirs(dirpath, exist_ok=True)


def _is_dir(path: str) -> bool:
    return os.path.isdir(path)


def _is_file(path: str) -> bool:
    return os.path.isfile(path)


#-----------------------------------------------------------------------------#
# Listado y selección de ficheros JSON dentro de un directorio
#-----------------------------------------------------------------------------#

def ListJsonFiles(directory: str) -> list[str]:
    """
    Lista los ficheros visibles del directorio con extensión válida (.json, .json.gz).
    Devuelve rutas absolutas ordenadas por nombre (no por fecha).
    """
    d = _expand_path(directory)
    if not _is_dir(d):
        raise NotADirectoryError(f"'{directory}' no es un directorio válido.")
    out: list[str] = []
    for name in os.listdir(d):
        if name.startswith("."):
            continue
        path = os.path.join(d, name)
        if _is_file(path) and IsJsonFilename(name):
            out.append(os.path.abspath(path))
    out.sort()
    return out


def PickLatestJson(directory: str) -> Optional[str]:
    """
    Devuelve la ruta absoluta del JSON más reciente (por fecha de modificación) dentro del directorio.
    Si no hay candidatos válidos, devuelve None.
    """
    candidates = ListJsonFiles(directory)
    if not candidates:
        return None
    # Orden por mtime descendente
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]


#-----------------------------------------------------------------------------#
# Escritura atómica en JSON o JSON GZIP
#-----------------------------------------------------------------------------#

def _atomic_write_text(target_path: str, data_str: str) -> None:
    """
    Escritura atómica de texto UTF-8 en target_path:
      1) Escribe en fichero temporal en el mismo directorio.
      2) fsync + os.replace al destino.
    """
    dirpath = os.path.dirname(target_path)
    _ensure_dir_exists(dirpath)

    # Crear fichero temporal en el mismo directorio para que os.replace sea atómico
    fd, tmp_path = tempfile.mkstemp(dir=dirpath, prefix=".tmp_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as tmp_fp:
            tmp_fp.write(data_str)
            tmp_fp.flush()
            os.fsync(tmp_fp.fileno())
        os.replace(tmp_path, target_path)
    finally:
        # Limpieza defensiva
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass


def _atomic_write_gzip_json(target_path: str, data_obj: Any, *, indent: int, sort_keys: bool) -> None:
    """
    Escritura atómica JSON comprimida (.json.gz). Se serializa directamente al gzip temporal
    para evitar dobles buffers y reducir memoria intermedia.
    """
    dirpath = os.path.dirname(target_path)
    _ensure_dir_exists(dirpath)

    fd, tmp_path = tempfile.mkstemp(dir=dirpath, prefix=".tmp_", suffix=".json.gz")
    try:
        # Escribimos en modo texto UTF-8 dentro del gzip temporal
        with os.fdopen(fd, "wb") as raw_fp:
            with gzip.GzipFile(fileobj=raw_fp, mode="wb") as gz_bin:
                with io.TextIOWrapper(gz_bin, encoding="utf-8", newline="\n") as gz_txt:
                    json.dump(
                        data_obj,
                        gz_txt,
                        ensure_ascii=False,
                        indent=indent,
                        sort_keys=sort_keys,
                        allow_nan=False,  # JSON estricto
                    )
                    gz_txt.flush()
                    # fsync del fd original (gz_bin/gz_txt envuelven el mismo descriptor)
                    raw_fp.flush()
                    os.fsync(raw_fp.fileno())
        os.replace(tmp_path, target_path)
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass


#-----------------------------------------------------------------------------#
# API pública: Guardar y Cargar
#-----------------------------------------------------------------------------#

def SaveDataJson(
    data: Any,
    path: str,
    *,
    filename: Optional[str] = None,
    gzip: Optional[bool] = None,
    indent: int = 2,
    sort_keys: bool = False,
    overwrite: bool = True,
) -> str:
    """
    Guarda 'data' en JSON (UTF-8). Admite gzip si la extensión es '.json.gz' o si 'gzip=True'.
    Escritura atómica. Devuelve la ruta absoluta del fichero guardado.

    Parámetros:
        data        : objeto serializable a JSON (dict, list, etc.)
        path        : puede ser un fichero destino ('.json' o '.json.gz') o un directorio.
        filename    : (opcional) si 'path' es directorio, nombre de fichero ('*.json' o '*.json.gz').
        gzip        : (opcional) si None, se infiere por extensión; si bool, fuerza compresión.
        indent      : indentación del JSON (por defecto 2).
        sort_keys   : ordenar claves del dict al serializar.
        overwrite   : si False y el destino existe, lanza FileExistsError.

    Comportamiento:
        - Si 'path' termina en '.json' o '.json.gz', se usa como destino directo.
        - Si 'path' es un directorio, 'filename' es obligatorio y debe tener extensión válida.
    """
    target = _expand_path(path)

    # Determinar destino final y compresión
    if IsJsonFilename(target):
        # 'path' es un fichero destino válido
        out_path = target
        gz = _infer_gzip_from_name(out_path, gzip)
    else:
        # Asumimos 'path' directorio
        if not filename:
            raise ValueError(
                "SaveDataJson: si 'path' es un directorio, debe proporcionar 'filename' "
                "con extensión '.json' o '.json.gz'."
            )
        if not IsJsonFilename(filename):
            raise ValueError("SaveDataJson: 'filename' debe terminar en '.json' o '.json.gz'.")
        _ensure_dir_exists(target)
        out_path = os.path.join(target, filename)
        out_path = _expand_path(out_path)
        gz = _infer_gzip_from_name(out_path, gzip)

    if not overwrite and os.path.exists(out_path):
        raise FileExistsError(f"El fichero de destino ya existe: {out_path}")

    # Serialización / escritura atómica
    if gz:
        _atomic_write_gzip_json(out_path, data, indent=indent, sort_keys=sort_keys)
    else:
        # Volcamos primero a cadena para validar JSON estricto antes de escribir
        data_str = json.dumps(
            data,
            ensure_ascii=False,
            indent=indent,
            sort_keys=sort_keys,
            allow_nan=False,
        )
        _atomic_write_text(out_path, data_str)

    return out_path


def LoadData(
    path: str,
    *,
    filename: Optional[str] = None,
    object_hook=None,
    strict: bool = True,
) -> Any:
    """
    Carga datos JSON desde 'path'. Soporta '.json' y '.json.gz'.
    Si 'path' es directorio, se interpreta como el directorio que contiene los datos y:
        - Si 'filename' se proporciona, carga ese fichero dentro del directorio.
        - Si 'filename' es None, carga el JSON más reciente (por mtime) dentro del directorio.
    Devuelve el objeto Python (dict/list/etc.).

    Parámetros:
        path        : ruta a fichero '.json' / '.json.gz' O a un directorio con ficheros JSON válidos.
        filename    : nombre del fichero dentro del directorio (opcional).
        object_hook : hook de decodificación de JSON (opcional).
        strict      : si True, forzamos JSON estricto (no NaN/Infinity). (Se respeta a través del decode por defecto)

    Errores:
        - FileNotFoundError si no se localiza un fichero válido.
        - ValueError si las extensiones no son válidas o el JSON es inválido.
    """
    in_path = _expand_path(path)

    # Caso: 'path' es un fichero
    if _is_file(in_path):
        if not IsJsonFilename(in_path):
            raise ValueError(f"Extensión no válida para JSON: '{in_path}'. Use .json o .json.gz")
        return _load_from_file(in_path, object_hook=object_hook)

    # Caso: 'path' es un directorio -> decidir qué fichero cargar
    if _is_dir(in_path):
        if filename:
            candidate = os.path.join(in_path, filename)
            candidate = _expand_path(candidate)
            if not _is_file(candidate):
                raise FileNotFoundError(f"No existe el fichero especificado: {candidate}")
            if not IsJsonFilename(candidate):
                raise ValueError(f"Extensión no válida para JSON: '{candidate}'. Use .json o .json.gz")
            return _load_from_file(candidate, object_hook=object_hook)
        else:
            # Elegir el más reciente por mtime
            latest = PickLatestJson(in_path)
            if not latest:
                raise FileNotFoundError(
                    f"No se encontraron ficheros .json / .json.gz en el directorio: {in_path}"
                )
            return _load_from_file(latest, object_hook=object_hook)

    # Ni fichero ni directorio válido
    raise FileNotFoundError(f"Ruta inexistente o inválida: {path}")


#-----------------------------------------------------------------------------#
# Procedimientos internos de lectura en formato (JSON / JSON.GZ)
#-----------------------------------------------------------------------------#

def _load_from_file(filepath: str, *, object_hook=None) -> Any:
    """Despacha a lectura normal o gzip según extensión."""
    lower = filepath.lower()
    if lower.endswith(".json.gz"):
        return _load_json_gz(filepath, object_hook=object_hook)
    elif lower.endswith(".json"):
        return _load_json(filepath, object_hook=object_hook)
    else:
        raise ValueError(f"Extensión no válida: {filepath}")


def _load_json(filepath: str, *, object_hook=None) -> Any:
    """Lee JSON de texto UTF-8."""
    try:
        with open(filepath, "r", encoding="utf-8") as fp:
            return json.load(fp, object_hook=object_hook)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON inválido en '{filepath}': {e}") from e


def _load_json_gz(filepath: str, *, object_hook=None) -> Any:
    """Lee JSON comprimido GZIP en UTF-8."""
    try:
        with gzip.open(filepath, "rt", encoding="utf-8") as fp:
            return json.load(fp, object_hook=object_hook)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON.gz inválido en '{filepath}': {e}") from e

