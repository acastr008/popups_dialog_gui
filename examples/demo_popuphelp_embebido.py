#!/usr/bin/python3
"""
Programa asistido por ChatGPT en fecha 15/feb/2026 y hora 07:36
Titulo: Demo PopupHELP — visor Markdown embebido como contenido interactivo
Descripción: Demo Pygame que abre un PopupDialog con contenido interactivo y, desde él,
             lanza PopupHELP() para mostrar una ayuda Markdown embebida (modal/bloqueante).
"""

import time
import pygame

from popups_dialog_gui.Popup_Dialog import (
    IniPopupDialog,
    PopupDialogWindow,
    SurfacePPsct,
    PopupHELP,
    InteractiveContent,
)


WIDTH = 1200
HEIGHT = 800

KERNEL_MARGIN_W = 80
KERNEL_MARGIN_H = 160

AREA_SIZE = (WIDTH - KERNEL_MARGIN_W, HEIGHT - KERNEL_MARGIN_H)


HELP_MD = f"""
# Ayuda (PopupHELP embebido)

Este popup contiene un **visor Markdown** como **contenido interactivo**.

---

## Controles dentro de la ayuda

- **Rueda del ratón:** scroll vertical (wheel_step configurable).
- **ESC** (o el botón inferior): cerrar la ayuda.

---

## Índice interno

- [1. Qué estás probando](#1-qué-estás-probando)
- [2. Contenido largo para scroll](#2-contenido-largo-para-scroll)
- [3. Bloques de código](#3-bloques-de-código)

---

## 1. Qué estás probando

Estás validando que `PopupHELP(md_text, ...)`:

1) Crea un popup con un área interactiva del tamaño: **{{AREA_SIZE[0]}} x {{AREA_SIZE[1]}}**  
2) Inserta ahí el visor `HelpViewer` (vía `help_core_pygame`)  
3) Es **modal/bloqueante**: detiene el loop del llamador hasta cerrar la ayuda  
4) Devuelve control al llamador sin “romper” el estado del popup principal

---

## 2. Contenido largo para scroll

A continuación hay texto repetido para forzar scroll:

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

(Repítelo mentalmente… lo importante es que haya scroll 🙂)

---

## 3. Bloques de código

```python
def example():
    print("Esto es un bloque de código dentro del visor Markdown")
```

Fin de la ayuda.
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
    pygame.display.set_caption("Demo PopupHELP (visor Markdown embebido)")

    display.fill((0, 0, 15))
    pygame.display.flip()
    time.sleep(0.1)

    # Estilo base del sistema de popups
    IniPopupDialog(display, "formal")  # o "playful_childlike"

    # Contenido interactivo del popup principal
    content = MiniSimulation(area_size=AREA_SIZE)
    kernel_section = SurfacePPsct(content, interactive_size=AREA_SIZE)

    popup = PopupDialogWindow(
        kernel_section,
        ["Cerrar", "Ayuda"],
        Title="Popup principal (contenido interactivo) + PopupHELP embebido",
        FlagAlert="Blue",
    )

    clock = pygame.time.Clock()

    running = True
    while running:
        dt_ms = clock.tick(60)
        events = pygame.event.get()

        pressed = popup.step(events, dt_ms)

        if pressed == "Ayuda":
            popup.pause()

            PopupHELP(
                HELP_MD,
                IdButt="   Cerrar ayuda   ",
                Title="Ayuda — PopupHELP (Markdown embebido)",
                FlagAlert="Blue",
                interactive_size=AREA_SIZE,
                style_variant="formal",
                fonts_dir="fonts",
                kernel_bg=(240, 240, 245),
                wheel_step=48,
                visual_indent_px=24,
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
