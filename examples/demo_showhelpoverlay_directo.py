#!/usr/bin/python3
"""
Programa asistido por ChatGPT en fecha 15/feb/2026 y hora 11:23
Titulo: Demo ShowHelpOverlay — overlay modal sobre popup visualmente similar
Descripción: Demo Pygame que muestra un PopupDialog con contenido interactivo y, desde él,
             llama DIRECTAMENTE a help_core_pygame.ShowHelpOverlay() para ilustrar el nivel
             de API inferior (framework). El aspecto visual permanece muy parecido al de
             la demo de PopupHELP porque el overlay se dibuja sobre el frame congelado.
"""

import time

import pygame

from popups_dialog_gui.Popup_Dialog import (
    IniPopupDialog,
    PopupDialogWindow,
    SurfacePPsct,
    InteractiveContent,
)

from help_core_pygame.help_core import ShowHelpOverlay


WIDTH = 1200
HEIGHT = 800

KERNEL_MARGIN_W = 80
KERNEL_MARGIN_H = 160

AREA_SIZE = (WIDTH - KERNEL_MARGIN_W, HEIGHT - KERNEL_MARGIN_H)


HELP_MD = f"""
# Ayuda (ShowHelpOverlay directo)

Esta demo ilustra el **nivel inferior** de API:

- `help_core_pygame.help_core.ShowHelpOverlay(display, md_text, ...)`

Comparada con `PopupHELP(md_text, ...)`, aquí:

- Tú aportas el **display** (`pygame.Surface`).
- La ayuda se muestra como **overlay modal** sobre el frame congelado.
- La función es **bloqueante** hasta que se cierra la ayuda (ESC por defecto).

---

## ¿Qué deberías notar?

1) El **aspecto visual** es muy parecido al popup, porque el overlay se dibuja encima del frame congelado
   (donde ya estaba el popup principal).
2) No hay “popup de ayuda” con botones del sistema de popups; el cierre se hace por teclas (`exit_keys`)
   o por QUIT.
3) Tras volver del modal, conviene **descartar dt** para evitar un salto en el loop principal.

---

## Contenido largo para forzar scroll

- Línea 01: Lorem ipsum dolor sit amet.
- Línea 02: Consectetur adipiscing elit.
- Línea 03: Sed do eiusmod tempor incididunt.
- Línea 04: Ut labore et dolore magna aliqua.
- Línea 05: Ut enim ad minim veniam.
- Línea 06: Quis nostrud exercitation ullamco.
- Línea 07: Laboris nisi ut aliquip ex ea commodo consequat.
- Línea 08: Duis aute irure dolor in reprehenderit.
- Línea 09: In voluptate velit esse cillum dolore.
- Línea 10: Eu fugiat nulla pariatur.

---

## Bloque de código

```python
def example():
    print("ShowHelpOverlay() dibuja encima del frame congelado.")
```
"""


class MiniSimulation(InteractiveContent):
    """Contenido interactivo mínimo para el popup principal.

    - Una bola que rebota en el rectángulo (coords relativas al kernel).
    - Click izquierdo: teletransporta la bola.
    - Espacio: pausa/reanuda.
    """

    def __init__(self, area_size: tuple[int, int]) -> None:
        super().__init__()
        self.width, self.height = area_size

        self.ball_pos = pygame.math.Vector2(self.width * 0.25, self.height * 0.30)
        self.ball_vel = pygame.math.Vector2(220.0, 160.0)
        self.ball_radius = 10

        self.paused = False
        self.bg_color = (20, 20, 40)

    def wants_keyboard(self) -> bool:
        return True

    def wants_wheel(self) -> bool:
        return False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Procesa eventos en coordenadas relativas.

        Args:
            event: Evento de pygame.

        Returns:
            True si el evento ha sido consumido por el contenido interactivo.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.paused = not self.paused
                return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # event.pos llega en coords RELATIVAS por SurfacePPsct
                x_rel, y_rel = event.pos
                self.ball_pos.update(x_rel, y_rel)
                return True

        return False

    def update(self, dt_ms: int) -> None:
        """Actualiza la simulación.

        Args:
            dt_ms: Delta time en milisegundos.
        """
        if self.paused:
            return

        dt = dt_ms / 1000.0
        self.ball_pos += self.ball_vel * dt

        left = self.ball_radius
        right = self.width - self.ball_radius
        top = self.ball_radius
        bottom = self.height - self.ball_radius

        if self.ball_pos.x < left:
            self.ball_pos.x = left
            self.ball_vel.x *= -1.0
        elif self.ball_pos.x > right:
            self.ball_pos.x = right
            self.ball_vel.x *= -1.0

        if self.ball_pos.y < top:
            self.ball_pos.y = top
            self.ball_vel.y *= -1.0
        elif self.ball_pos.y > bottom:
            self.ball_pos.y = bottom
            self.ball_vel.y *= -1.0

    def draw(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Dibuja dentro del rectángulo de interacción.

        Args:
            surface: Surface destino (display).
            rect: Rect en coordenadas de pantalla donde debe dibujar.
        """
        surface.fill(self.bg_color, rect)

        # Convertir coords relativas -> coords pantalla
        origin_x, origin_y = rect.x, rect.y
        ball_screen_pos = (int(origin_x + self.ball_pos.x), int(origin_y + self.ball_pos.y))

        pygame.draw.circle(surface, (230, 230, 255), ball_screen_pos, self.ball_radius)
        pygame.draw.circle(surface, (80, 160, 255), ball_screen_pos, self.ball_radius, 2)


def main() -> int:
    """Punto de entrada de la demo.

    Returns:
        Código de salida del proceso.
    """
    pygame.init()

    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Demo ShowHelpOverlay (nivel inferior)")

    display.fill((0, 0, 15))
    pygame.display.flip()
    time.sleep(0.1)

    # Estilo base del sistema de popups
    IniPopupDialog(display, "formal")

    # Contenido interactivo del popup principal
    content = MiniSimulation(area_size=AREA_SIZE)
    kernel_section = SurfacePPsct(content, interactive_size=AREA_SIZE)

    popup = PopupDialogWindow(
        kernel_section,
        ["Cerrar", "Ayuda (Overlay)"],
        Title="Popup principal + ShowHelpOverlay() directo",
        FlagAlert="Blue",
    )

    clock = pygame.time.Clock()

    running = True
    while running:
        dt_ms = clock.tick(60)
        events = pygame.event.get()

        pressed = popup.step(events, dt_ms)

        if pressed == "Ayuda (Overlay)":
            popup.pause()

            ShowHelpOverlay(
                display,
                HELP_MD,
                title="Ayuda — ShowHelpOverlay() directo",
                exit_keys=(pygame.K_ESCAPE,),
                fps=60,
                kernel_bg=(240, 240, 245),
                wheel_step=48,
                scroll_limit_cooldown_ms=300,
                base_dir=None,
            )

            # Descartar el “salto” temporal provocado por el modal
            clock.tick(60)
            popup.resume()
            continue

        if pressed == "Cerrar":
            running = False

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
