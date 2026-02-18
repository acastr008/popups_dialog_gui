# Archivo: examples/demo_Popup_Surface_Selector.py
# Descripción breve: Selector de superficies con navegación 
# Orden tutorial: 1.5

"""
Demo: selector de superficies con navegación.
- Construye superficies a partir de tamaños y títulos
- Muestra un PopupDialogWindow con botones: Anterior / Posterior / Cancelar / Seleccionar
- Anterior/Posterior se ocultan si estamos al inicio/fin
- Al salir, pinta en pantalla el identificador elegido y termina
"""

import pygame
import time
from popups_dialog_gui.Popup_Dialog import PopupDialogWindow, IniPopupDialog, SurfacePPsct

win_title="1.5) examples/demo_Popup_Surface_Selector.py"

# ----------------------------
# Utilidades de la demo
# ----------------------------
def SampleSurface(w, h, Title):
    """Devuelve una superficie simple con fondo azul, elipse naranja y el texto centrado."""
    AZUL    = (0, 0, 200)
    NARANJA = (255, 140, 0)
    NEGRO   = (0, 0, 0)
    superficie = pygame.Surface((w, h))
    superficie.fill(AZUL)
    marginW = w // 20
    marginH = h // 20
    pygame.draw.ellipse(superficie, NARANJA, (marginW, marginH, w - (marginW * 2), h - (marginH * 2)))
    letra = pygame.font.SysFont("Arial", max(12, w // 15))
    text_surface = letra.render(f"{Title} ({w}x{h})", True, NEGRO, NARANJA)
    text_rect = text_surface.get_rect()
    text_rect.center = (w // 2, h // 2)
    superficie.blit(text_surface, text_rect)
    return superficie

def make_surface_pairs(base_list):
    """
    A partir de una lista [(w,h,titulo), ...] genera [(surface, StrI_dent), ...]
    donde StrI_dent se usa como título del popup.
    """
    pairs = []
    for (w, h, tit) in base_list:
        surf = SampleSurface(w, h, tit)
        ident = f"<<<<< {tit} >>>>>"
        pairs.append((surf, ident))
    return pairs

def resolve_button_label(raw_response, labels):
    """
    Intenta resolver la etiqueta del botón pulsado a partir de lo que devuelva PopupDialogWindow.Run().
    Soporta retorno como string, índice int, o dict {'button': '...'}.
    """
    if isinstance(raw_response, str):
        return raw_response
    if isinstance(raw_response, int):
        if 0 <= raw_response < len(labels):
            return labels[raw_response]
        return None
    if isinstance(raw_response, dict):
        # Algunos diseños devuelven objetos con información adicional
        # Intentamos varias claves habituales
        for k in ("button", "label", "name"):
            if k in raw_response and isinstance(raw_response[k], str):
                return raw_response[k]
    return None

def run_surface_selector(pairs, main_display, style_key="playful_childlike", flag_alert="Blue"):
    """
    Lanza el flujo de selección:
    - pairs: lista [(surface, StrI_dent), ...]
    - style_key: clave de estilo para IniPopupDialog
    - flag_alert: estilo de alerta/tema para el popup
    Retorna el identificador seleccionado (str) o None si se cancela.
    """
    if not pairs:
        return None

    IniPopupDialog(main_display, style_key)

    idx = 0
    selected_ident = None

    while True:
        surface, ident = pairs[idx]

        # Botones según posición
        labels = []
        if idx > 0:
            labels.append("Anterior")
        if idx < len(pairs) - 1:
            labels.append("Posterior")
        labels.extend(["Cancelar", "Seleccionar"])

        # Construir y ejecutar el popup
        popup = PopupDialogWindow(
            surface,
            labels,
            Title=ident,
            FlagAlert=flag_alert
        )
        raw = popup.Run()
        choice = resolve_button_label(raw, labels) or ""

        if choice == "Anterior" and idx > 0:
            idx -= 1
            continue
        if choice == "Posterior" and idx < len(pairs) - 1:
            idx += 1
            continue
        if choice == "Seleccionar":
            selected_ident = ident
            break
        if choice == "Cancelar" or choice == "":
            selected_ident = None
            break

    return selected_ident

def show_final_selection(main_display, selection_text):
    """Muestra en pantalla el resultado final durante un momento y sale."""
    main_display.fill((30, 30, 30))
    w, h = main_display.get_size()
    font = pygame.font.SysFont("Arial", 28)

    if selection_text is None:
        msg = "Selección cancelada."
    else:
        msg = f"Seleccionado: {selection_text}"

    text_surf = font.render(msg, True, (240, 240, 240))
    text_rect = text_surf.get_rect(center=(w // 2, h // 2))
    main_display.blit(text_surf, text_rect)
    pygame.display.flip()
    time.sleep(2.0)

# ----------------------------
# Punto de entrada de la demo
# ----------------------------
if __name__ == "__main__":
    pygame.init()
    ancho, alto = 800, 800
    MainDisplay = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption(win_title)
    MainDisplay.fill((30, 30, 30))
    pygame.display.flip()
    time.sleep(0.5)

    # (1) Lista base
    lista = [
        (700, 200, " Imagen 01 "),
        (200, 600, " Imagen 02 "),
        (600, 600, " Imagen 03 ")
    ]

    # (2) Generar lista de tuplas (superficie, StrI_dent)
    pairs = make_surface_pairs(lista)

    # (3) Ejecutar selector
    selected = run_surface_selector(pairs, MainDisplay, style_key="playful_childlike", flag_alert="Blue")

    # (5) Mostrar resultado en pantalla y terminar
    show_final_selection(MainDisplay, selected)
    pygame.quit()

