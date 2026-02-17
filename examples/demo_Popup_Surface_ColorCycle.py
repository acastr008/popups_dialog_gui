# examples/demo_Popup_Surface_ColorCycle.py
# Descripción breve: Pinta un rectángulo con un color derivado de time (solo 1er frame en este paso)
# Orden tutorial: 2.2

import pygame
import time
from popups_dialog_gui.Popup_Dialog import PopupDialogWindow, IniPopupDialog, SurfacePPsct
from popups_dialog_gui.interactive_content import InteractiveContent

class ColorCycle(InteractiveContent):
    """
    Esta clase es un stub de contenido 'dinámico'.
    NOTA:
        Un stub es un componente de software simplificado que simula el comportamiento de otro módulo o servicio, 
        usándose para aislar el código devolviendo datos predefinidos sin ejecutar la lógica real, lo cual permite 
        probar diferentes escenarios (éxito, error) de forma controlada y aíslar dependencias. Suele usarse en pruebas,
        pero para nosotros es la forma de conectar un comportamiento dinámico con objetos InteractiveContent.
    - on_mount: prepara fuente
    - draw: pinta un rectángulo con un color derivado de time (solo 1er frame en este paso)
    """
    def __init__(self, label="ColorCycle (Paso 2)"):
        self._font = None
        self.label = label

    def on_mount(self, rect: pygame.Rect) -> None:
        try:
            self._font = pygame.font.SysFont("Arial", max(12, rect.width // 20))
        except Exception:
            self._font = None

    def on_unmount(self) -> None:
        self._font = None

    def draw(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        # Color calculado en base al tiempo actual (verás el frame estático en Paso 2)
        t = int(pygame.time.get_ticks() * 0.002)  # rapidez de cambio
        color = ((t * 7) % 255, (t * 3) % 255, (t * 11) % 255)
        pygame.draw.rect(surface, color, rect)

        if self._font and self.label:
            txt = self._font.render(self.label, True, (0, 0, 0))
            text_rect = txt.get_rect(center=rect.center)
            surface.blit(txt, text_rect)

if __name__ == "__main__":
    pygame.init()
    W, H = 900, 700
    MainDisplay = pygame.display.set_mode((W, H))
    pygame.display.set_caption("2.2) demo_Popup_Surface_ColorCycle.py")
    MainDisplay.fill((40, 40, 40))
    pygame.display.flip()
    time.sleep(0.3)

    IniPopupDialog(MainDisplay, "playful_childlike")

    content = ColorCycle()
    # IMPORTANTE: tamaño fijo para el contenido interactivo (Paso 2)
    kernel_section = SurfacePPsct(
        content,
        W_Margin=20,
        H_Margin=20,
        BorderThikness=2,
        BorderColor=(0, 0, 0),
        interactive_size=(600, 350)
    )

    popup = PopupDialogWindow(
        kernel_section,
        ["Cerrar"],
        Title="<< Demo Paso 2: on_mount + draw (clipping) >>",
        FlagAlert="Blue"
    )
    popup.Run()
    pygame.quit()

