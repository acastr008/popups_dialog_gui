# popup_gui/interactive_content.py
import pygame

class InteractiveContent:
    """
    Interfaz mínima para contenidos interactivos/animados.
    Paso 1: solo definimos las firmas; la integración en SurfacePPsct vendrá en el Paso 2.
    """

    def on_mount(self, rect: pygame.Rect) -> None:
        """Se llama cuando el contenido se coloca dentro de la sección central."""
        pass

    def on_unmount(self) -> None:
        """Limpieza de recursos cuando se retira el contenido."""
        pass

    def update(self, dt_ms: int) -> None:
        """
        Lógica de estado/animación. dt_ms en milisegundos.
        En el Paso 1 no se usa; está por compatibilidad futura.
        """
        pass

    def draw(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """
        Dibuja dentro de 'rect' sobre 'surface'.
        En el Paso 1 lo usaremos para un render de una sola pasada.
        """
        pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Gestiona un evento y devuelve True si lo consume.
        En el Paso 1 no se enrutan eventos aún.
        """
        return False

    def wants_keyboard(self) -> bool:
        """Indica si desea eventos de teclado."""
        return False

    def wants_wheel(self) -> bool:
        """Indica si desea eventos de rueda del ratón."""
        return False

