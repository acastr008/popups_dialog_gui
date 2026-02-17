# examples/demo_rebota_controles.py
# Descripción breve: Partículas rebotando con controles de teclado y de ratón (coord. relativas a rectángulo kernel).
# Orden tutorial: 2.4
#
# - LMB: añade 200 partículas en el punto del clic (valor alto para verificar la precisión).
# - RMB: elimina 20 partículas.
# - Rueda: ajusta velocidad (+/-) 10%.
# - Espacio: pausa/reanuda.
# - 'c': Cambia el tamaño de las particulas,
#
# Nota importante:
#   El contenido trabaja SIEMPRE en coordenadas RELATIVAS (0..w, 0..h) al área útil (inner rect) del kernel.
#   En draw() se suma el offset del rect (ox, oy) para dibujar en pantalla.
#   De esta manera, el clic (que SurfacePPsct remapea ya a relativo) coincide exactamente.

import pygame
import random
import time

from popups_dialog_gui.Popup_Dialog import (
    PopupDialogWindow, IniPopupDialog, SurfacePPsct, PopupHELP, InteractiveContent
)

from popups_dialog_gui.adapters import HelpAsInteractive, run_help_popup_from_md
from help_core_pygame import HelpViewer


WIDTH=1500              # Anchura de la pantalla
HEIGTH=950              # Altura de la pantalla
COUNT=120               # Número inicial de partículas
RADIUS=6                # radio de particula de tamaño normal (grande 2 pixels mayor)
SPEED_LOW=80            # Mínimo de velocidad aleatoria
SPEED_HIGH=220          # Máximo de velocidad aleatoria
BIG=True                # Modo tamaño grande de particulas
BG_COLOR=(0, 0, 40)     # Color de fondo
NUM_SPAWN= 200          # Número de partículas engendradas en cada explosion
NUM_DELETE= 50          # Número de particulas eliminadas en cada borrado


HELP_MD=f"""
# Ayuda para la demo de rebote de partículas con controles de teclado y ratón.

## Controles de ratón.
    **Click izquierdo:** añade {NUM_SPAWN} partículas que se dispersan desde el punto de la superficie donde hemos pinchado con el ratón. 
    **Click derecho:** Elimina las {NUM_DELETE} partículas más antíguas.
    **Rueda:** Ajusta velocidad en (+/-) 10%.

## Controles de teclado.
    **Espacio:** Pausa o reanuda el movimiento de las partículas.
    **Tecla 'c':** Cambia el tamaño de las particulas.

"""


class BouncingParticles(InteractiveContent):
    """
    Partículas rebotando dentro del área útil del kernel.
    Coord. internas RELATIVAS: (0,0) esquina superior izquierda; (w,h) la opuesta.
    """
    def __init__(self, area_size, count=100, radius=4, speed_range=(80, 220),
                 bg_color=(0, 0, 40), big=False):
        super().__init__()
        self.base_count = count
        self.radius = radius
        self.speed_range = list(speed_range)
        self.bg_color = tuple(bg_color)  # color de fondo del área dinámica
        self.big = big

        # Tamaño lógico conocido en construcción (rect fijo)
        self._w, self._h = area_size
        # Estado interno
        self.particles = []  # cada elemento: [x_rel, y_rel, vx, vy, color]
        self.paused = False
        self.speed_scale = 1.0

        # Siembra inicial (depende de _w,_h, ya conocidos)
        self._spawn_random(self.base_count)

    # --- Integración con el router del Popup ---
    def wants_keyboard(self) -> bool: return True
    def wants_wheel(self) -> bool:    return True

    def Radius(self):
        return self.radius + 5 if self.big else self.radius

    # --- Generación de partículas ---
    def _spawn_random(self, n):
        if self._w <= 0 or self._h <= 0:
            return
        r = self.Radius()
        left, right = r, self._w - r
        top, bottom = r, self._h - r

        for _ in range(n):
            x = random.uniform(left, right)
            y = random.uniform(top, bottom)
            spd = random.uniform(self.speed_range[0], self.speed_range[1]) * self.speed_scale
            ang = random.uniform(0, 360)
            v = pygame.math.Vector2(1, 0).rotate(ang) * spd
            color = (random.randint(120, 255), random.randint(120, 255), random.randint(120, 255))
            self.particles.append([x, y, v.x, v.y, color])

    def _spawn_at(self, n, pos_rel):
        if self._w <= 0 or self._h <= 0:
            return
        x0, y0 = pos_rel  # POS RELATIVA recibida desde SurfacePPsct.handle_event
        r = self.Radius()
        x0 = max(r, min(self._w - r, x0))  # clamp
        y0 = max(r, min(self._h - r, y0))

        for _ in range(n):
            spd = random.uniform(self.speed_range[0], self.speed_range[1]) * self.speed_scale
            ang = random.uniform(0, 360)
            v = pygame.math.Vector2(1, 0).rotate(ang) * spd
            color = (random.randint(120, 255), random.randint(120, 255), random.randint(120, 255))
            self.particles.append([x0, y0, v.x, v.y, color])

    # --- Eventos ---
    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:      # LMB: explosión grande
                self._spawn_at(NUM_SPAWN, event.pos)
                return True
            elif event.button == 3:    # RMB: borrar algunas
                if self.particles and len(self.particles) > NUM_DELETE:
                    del self.particles[:min(NUM_DELETE, len(self.particles))]
                return True

        elif event.type == pygame.MOUSEWHEEL:
            # Ajuste de velocidad global (escala) y de las ya existentes
            if event.y > 0:
                self.speed_scale *= 1.1
                factor = 1.1
            elif event.y < 0:
                self.speed_scale /= 1.1
                factor = 1.0 / 1.1
            else:
                factor = 1.0
            if factor != 1.0:
                for p in self.particles:
                    p[2] *= factor
                    p[3] *= factor
            return True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.paused = not self.paused
                return True
            elif event.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                self._spawn_random(10)
                return True
            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                if self.particles:
                    del self.particles[:min(10, len(self.particles))]
                return True
            elif event.key == pygame.K_c:
                self.big = not self.big
                return True

        return False

    # --- Actualización y dibujo ---
    def update(self, dt_ms: int) -> None:
        if self._w <= 0 or self._h <= 0 or self.paused:
            return
        dt = dt_ms / 1000.0
        r = self.Radius()
        left, right = r, self._w - r
        top, bottom = r, self._h - r

        for p in self.particles:
            x, y, vx, vy, color = p
            x += vx * dt
            y += vy * dt

            if x < left:      x = left;  vx = -vx
            elif x > right:   x = right; vx = -vx
            if y < top:       y = top;   vy = -vy
            elif y > bottom:  y = bottom;vy = -vy

            p[0], p[1], p[2], p[3] = x, y, vx, vy

    def draw(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        # Pintar el fondo solo dentro del rect (clipping activo desde SurfacePPsct)
        surface.fill(self.bg_color, rect)
        # Offset absoluto para convertir coords relativas -> pantalla
        ox, oy = rect.x, rect.y
        for x, y, vx, vy, color in self.particles:
            pygame.draw.circle(surface, color, (int(ox + x), int(oy + y)), self.Radius())


################################################################################################################
############################################ M  A  I  N  #######################################################
################################################################################################################
if __name__ == "__main__":
    pygame.init()
    W, H = WIDTH, HEIGTH
    MainDisplay = pygame.display.set_mode((W, H))
    pygame.display.set_caption("2.4) demo_rebota_controles.py")
    # Color de fondo de la ventana principal (fuera del popup)
    MainDisplay.fill((0, 0, 20))  # azul muy oscuro exterior
    pygame.display.flip()
    time.sleep(0.2)

    # Estilo del popup
    IniPopupDialog(MainDisplay, "playful_childlike")

    # Tamaño lógico fijo del área de juego (debe coincidir con interactive_size de la sección)
    AREA_SIZE = (WIDTH - 100, HEIGTH - 200)

    # Contenido interactivo (siembra inicial en __init__, conociendo (w,h))
    content = BouncingParticles(
        area_size=AREA_SIZE,
        count=COUNT,
        radius=RADIUS,
        speed_range=(SPEED_LOW, SPEED_HIGH),
        big=BIG,
        bg_color=BG_COLOR
    )

    # Sección del kernel (rect fijo)
    kernel_section = SurfacePPsct(
        content,
        interactive_size=AREA_SIZE
    )

    # Popup única (no se reinstancia)
    popup = PopupDialogWindow(
        kernel_section,
        ["Cerrar", "Ayuda"],
        Title="Partículas rebotando (controles con el ratón y con el teclado)",
        FlagAlert="Blue"
    )

    clock = pygame.time.Clock()

    while True:
        dt_ms = clock.tick(30)  # ~30 FPS
        events = pygame.event.get()

        pressed = popup.step(events, dt_ms)  # NO bloqueante: procesa eventos, update y dibuja

        if pressed == "Ayuda":
            popup.pause() # Congelar la demo mientras se muestra la ayuda (suele venir bien hacerlo)
            PopupHELP(
                HELP_MD,
                Title="Ayuda — Partículas",
                FlagAlert="Blue",
                interactive_size=AREA_SIZE,
                style_variant="formal",  # o "playful_childlike"
                fonts_dir="fonts",
                kernel_bg=(240, 240, 245)
            )
            #.........................................................................................................
            # NOTA:
            # Hacemos un tick de descarte al volver de la ayuda, así evitamos que el siguiente frame acumule todo el 
            # tiempo de la pausa provocanto un dt_ms enorme. (dt_ms normal son los milisegundos trancurridos entre un
            # frame y el siguiente, así que un dt_ms enorme provocaría un salto de tiempo muy fuerte en la simulación).
            # pygame.time.Clock.tick(fps) devuelve los ms transcurridos desde la última llamada a tick y, además, 
            # reinicia la referencia interna del reloj.
            #.........................................................................................................
            clock.tick(30) # Descartar el tiempo acumulado durante la ayuda y reanudar
            popup.resume() # Reanuda las actualizaciones para continuar generando nuevos frames
            continue  # Volvemos al mismo popup

        if pressed == "Cerrar":
            break  # Termina la demo

