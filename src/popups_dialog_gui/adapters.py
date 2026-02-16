# helpview/adapters.py
# Adaptadores para integrar HelpViewer dentro de popups (SurfacePPsct) u otros contenedores.

from __future__ import annotations
from typing import Any, Tuple, Optional

# NOTA: no importamos popup_gui a nivel de módulo para evitar dependencias duras.
# Los imports de popup_gui se hacen DENTRO de las funciones de conveniencia.


class HelpAsInteractive:
    """
    Envuelve un HelpViewer para usarlo como contenido interactivo en SurfacePPsct.
    Implementa la interfaz mínima esperada por SurfacePPsct (on_mount, update, draw, handle_event,
    wants_keyboard, wants_wheel).
    """
    def __init__(self, help_viewer: Any):
        self.viewer = help_viewer
        self._rect = None  # type: Optional[Any]

    # Llamado por el contenedor cuando se monta el contenido (rect = área útil del kernel)
    def on_mount(self, rect: Any) -> None:
        self._rect = rect
        # Si el visor soporta resize(ancho, alto) o resize((w,h)), intentamos ajustarlo
        if hasattr(self.viewer, "resize"):
            try:
                # Preferir firma (w,h), si no, (w,h) dentro de tupla
                self.viewer.resize((rect.width, rect.height))
            except TypeError:
                try:
                    self.viewer.resize(rect.width, rect.height)
                except Exception:
                    pass

    def on_unmount(self) -> None:
        # No hay recursos que limpiar por defecto
        pass

    # dt en milisegundos (la popup actualiza a ~30 FPS). El visor no necesita animación → noop.
    def update(self, dt: int) -> None:
        pass

    # El contenedor recorta con set_clip; delegamos el render en el visor: draw(surface, rect)
    def draw(self, surface: Any, rect: Any) -> None:
        self.viewer.draw(surface, rect)

    # Devolver True si el visor consume el evento (rueda/teclas/navegación)
    def handle_event(self, event: Any) -> bool:
        if hasattr(self.viewer, "handle_event"):
            try:
                return bool(self.viewer.handle_event(event))
            except Exception:
                return False
        return False

    # Flags para enrutado de entrada en la popup
    def wants_keyboard(self) -> bool:
        return True

    def wants_wheel(self) -> bool:
        return True

def run_help_popup_from_md(
        md_text: str,
        *,
        title: str = "Ayuda",
        interactive_size: tuple[int, int],
        popup_title: str | None = None,
        popup_buttons: tuple[str, ...] = ("Cerrar ayuda",),
        popup_flag_alert: str = "Blue",
        style_variant: str = "formal",
        style_json_path: str | None = None,
        fonts_dir: str | None = None,
        help_font_file: str | None = None,
        help_code_font_file: str | None = None,
        kernel_bg: tuple[int, int, int] | None = None,
        margins: tuple[int, int] = (20, 20),
        border_th: int = 2,
        border_color: tuple[int, int, int] = (0, 0, 0),) -> str:
    """
    Conveniencia: construye un HelpViewer con md_text, lo adapta y lo muestra en una PopupDialogWindow.
    Requiere que el llamante ya haya hecho IniPopupDialog(...).
    Devuelve la etiqueta del botón pulsado.
    """

    from help_core_pygame import HelpViewer
    from popups_dialog_gui.Popup_Dialog import SurfacePPsct, PopupDialogWindow
    # HelpAsInteractive ya está en este mismo módulo; no hace falta reimportarlo

    '''ççç OBSOLETO
    from helpview.help_core import HelpViewer
    from popup_gui.Popup_Dialog import SurfacePPsct, PopupDialogWindow
    from .adapters import HelpAsInteractive  # nos referenciamos a nosotros mismos, ok
    '''

    hv = HelpViewer(
        md_text,                      # ← 1er argumento posicional = el texto
        size=interactive_size,        # ← tamaño por keyword
        style_variant=style_variant,
        style_json_path=style_json_path,
        fonts_dir=fonts_dir,
        help_font_file=help_font_file,
        help_code_font_file=help_code_font_file,
        kernel_bg=kernel_bg)

    interactive_content = HelpAsInteractive(hv)

    W_Margin, H_Margin = margins
    kernel = SurfacePPsct(
        interactive_content,
        W_Margin=W_Margin,
        H_Margin=H_Margin,
        BorderThikness=border_th,
        BorderColor=border_color,
        interactive_size=interactive_size,
    )

    popup = PopupDialogWindow(
        kernel,
        list(popup_buttons),
        Title=(popup_title or f"Ayuda — {title}"),
        FlagAlert=popup_flag_alert,
    )
    return popup.Run()


