# ¿Qué sistema de ayuda debo usar: `PopupHELP()` o `ShowHelpOverlay()`?

En este proyecto hay **dos formas** de mostrar ayuda Markdown, pensadas para **necesidades distintas**:

- **`PopupHELP(md_text, ...)` (popups_dialog_gui)**: ayuda “integrada” en el **sistema de popups** de la GUI.
- **`ShowHelpOverlay(display, md_text, ...)` (help_core_pygame)**: ayuda como **overlay modal** dibujado directamente sobre el **display** de Pygame.

Ambas son válidas. La elección depende de *dónde* estás y *qué control* necesitas.

---

## 1) Cuándo usar `PopupHELP()` (recomendado en interfaces con popups)

### Úsalo cuando…
- Ya estás usando **popups_dialog_gui** (diálogos, confirmaciones, avisos) y quieres que la ayuda **respete el mismo estilo visual** (marcos, tipografías, botones, márgenes).
- Necesitas **un botón de cierre** coherente con tu UI (“Cerrar ayuda”, “Aceptar”, etc.) y un retorno claro (p. ej. devolver el id del botón).
- Quieres configurar la ayuda con parámetros del “mundo GUI”: **márgenes**, **borde**, **variant de estilo**, **fuentes**, etc.

### Ventajas
- **Consistencia visual** con el resto de diálogos/pantallas.
- Integración natural en flujos de usuario: “pulsa Ayuda” → sale un popup de ayuda → vuelve al diálogo original.
- Más fácil de “encajar” en apps con varios diálogos y estados internos del sistema de popups.

### Inconvenientes
- Depende del framework de popups (no es lo ideal si lo que tienes es un juego o un loop Pygame sin ese sistema).
- Suele tener más parámetros y decisiones “de estilo” (por diseño), lo que puede ser excesivo para un prototipo rápido.

### Ejemplos típicos (usuarios finales)
- En un formulario: botón **Ayuda** junto a un campo complejo (“Ruta base”, “Máscara de archivos”…).
- En un popup de error: “¿Qué significa este error?” abre `PopupHELP()` con la explicación.
- En un asistente de configuración: cada paso incluye “Ayuda” contextual.

---

## 2) Cuándo usar `ShowHelpOverlay()` (recomendado en juegos/loops directos de Pygame)

### Úsalo cuando…
- Estás en un **loop principal** (juego, simulación, visor) y quieres una ayuda rápida tipo “pulsa F1”.
- Quieres un overlay que **aparezca encima del frame actual**, sin montar un sistema de popups.
- Necesitas el control “framework-level”: tú decides `exit_keys`, `fps`, `wheel_step`, `base_dir`, etc.

### Ventajas
- Muy directo: le das un **display** y un texto, y aparece la ayuda.
- Encaja perfecto en **apps Pygame puras** (sin framework de GUI).
- La ayuda se ve “encima” del estado congelado: sensación de overlay modal natural.

### Inconvenientes
- No queda automáticamente “igual” que tu estilo de popups, porque **no usa el sistema de popups** (aunque visualmente puede parecerse si congelas el frame donde ya estaba el popup).
- El cierre se basa típicamente en teclas (`ESC`) o QUIT; si quieres botones GUI, ya estás en el terreno de `PopupHELP()` (o de integrar un widget de cierre tú mismo).
- Al volver al loop principal puede aparecer un “salto” de tiempo si tu app usa `dt`; conviene descartar/reajustar el primer `dt` tras cerrar.

### Ejemplos típicos (usuarios finales)
- En un juego: pulsas **F1** y aparece “Controles”, “Objetivo”, “Teclas”.
- En una demo técnica: overlay con instrucciones de manejo y atajos.
- En una herramienta Pygame: “Ayuda rápida” sin dependencias de GUI.

---

## 3) Regla práctica de elección

- Si tu pantalla/flujo está dominado por **popups_dialog_gui** → usa **`PopupHELP()`**.
- Si tu app es un **loop Pygame** y quieres un overlay rápido estilo “F1” → usa **`ShowHelpOverlay()`**.
- Si dudas: **`PopupHELP()`** suele ser la elección “de producto” (más cuidada para usuarios finales) y **`ShowHelpOverlay()`** la elección “de motor” (más directa, más baja).

---

## 4) Comentarios sobre las demos (para entender la diferencia)

En el repositorio pueden coexistir **tres** demos sin redundancia real *si* cada una ilustra un “punto de integración” distinto:

### Demo A — `demo_popuphelp_embebido.py` (PopupHELP)
- Desde un popup principal, botón **Ayuda** → abre **otro popup** con visor Markdown embebido.
- El usuario lo percibe como “parte del mismo sistema de ventanas”.
- Es la referencia cuando quieres ayuda “de producto” (botón, estilo, márgenes, etc.).

### Demo B — `demo_ask_help.py` (ShowHelpOverlay en flujo PopupASK)
- Ilustra un patrón muy habitual: **un diálogo de decisión** (`PopupASK`) que ofrece una opción **Ayuda**.
- La ayuda se muestra con **`ShowHelpOverlay()` directo**, y al salir se **restaura el frame** previo.
- Aporta valor como demo “tutorial” (mínima, conceptual): cómo “colgar” una ayuda de un botón dentro de un flujo de preguntas/respuestas.

### Demo C — `demo_showhelpoverlay_directo.py` (ShowHelpOverlay sobre un popup con contenido interactivo)
- Ilustra el caso “más cercano a una app real”: un popup con **contenido interactivo** (eventos, update/draw) y una ayuda overlay encima.
- Aporta el patrón de robustez: **pausa/reanuda** del popup y **descartar `dt`** al volver del modal para evitar saltos.
- Su valor principal es mostrar la convivencia overlay + contenido interactivo (más allá del caso didáctico de `PopupASK`).

#### ¿Sobra alguna?
- Si quieres **mínimo número de demos**, mantén:
  - `demo_popuphelp_embebido.py` (API alta) y
  - `demo_ask_help.py` (API baja + integración “Ayuda” en PopupASK).
  - En ese caso, `demo_showhelpoverlay_directo.py` puede considerarse opcional.
- Si te interesa conservar un ejemplo “realista” de overlay sobre contenido interactivo (pausa/reanuda + `dt`), entonces **sí tiene sentido** conservar también la Demo C y dejar explícito en la documentación qué aporta frente a `demo_ask_help.py`.

---

## 5) Resumen en una frase

- **`PopupHELP()`**: ayuda *para aplicaciones con GUI basada en popups* (consistencia, botones, estilo).
- **`ShowHelpOverlay()`**: ayuda *para loops Pygame* (overlay modal directo sobre el display, mínimo acoplamiento).
