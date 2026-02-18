# HELP_OPTIONS_TUTORIAL
*Documento: opciones para integrar un sistema de ayuda (Markdown) en aplicaciones Pygame con `help_core_pygame` y `popups_dialog_gui`.*

Fecha de generación: **18/Feb/2026 08:30** (Europe/Madrid)

---

## 1. Objetivo del tutorial

Estas demos muestran **tres patrones complementarios** para integrar ayuda en Markdown dentro de una aplicación Pygame:

1) **Ayuda como overlay directo** sobre el `display` (**`ShowHelpOverlay()`**).  
2) **Ayuda como popup embebido** dentro del sistema de diálogos (**`PopupHELP()`**).  
3) Integración con **contenidos dinámicos** (kernels interactivos) y consideraciones prácticas:  
   *pausa/reanudación*, manejo de `dt`, congelación de animación, y preservación del frame.

Las tres demos que se consideran “mínimas y no redundantes” son:

- `demo_ask_help.py`
- `demo_popuphelp_embebido.py`
- `demo_rebota_controles_ok.py`

> Nota: existe una cuarta demo (`demo_showhelpoverlay_directo.py`) que ilustra el overlay directo en un escenario parecido a `demo_popuphelp_embebido.py`. Si buscas reducir ejemplos, puede moverse a *extras* o sustituirse por un snippet breve en la documentación.

---

## 2. Dos enfoques: `ShowHelpOverlay()` vs `PopupHELP()`

### 2.1 `ShowHelpOverlay(display, md_text, ...)` (help_core_pygame)

**Qué es:**  
Un visor de ayuda en formato overlay **dibujado directamente sobre el `display`**. Suele ser **modal** en el sentido práctico (captura eventos hasta salir), pero *no pertenece* al sistema de popups.

**Implicaciones prácticas:**
- Se integra bien en programas sencillos donde no quieres abrir “otra ventana lógica” (otro popup), sino mostrar ayuda encima.
- Al cerrar, tú sigues en tu flujo original, pero debes cuidar:
  - **la restauración del contenido de pantalla** (si el overlay deja “pintado” el último frame),
  - el **salto de tiempo (`dt`)** acumulado mientras la ayuda está abierta,
  - y si tu app tiene animación, si quieres **congelar** o **dejar corriendo** la simulación.

**Cuándo encaja mejor:**
- Aplicaciones con un bucle principal propio donde “interrumpes” temporalmente y luego continúas.
- Flujos tipo “pregunta → ayuda → vuelvo a la pregunta”.
- Programas sin necesidad de que la ayuda sea un “diálogo” formal con estilo o botones del framework de popups.

---

### 2.2 `PopupHELP(md_text, ...)` (popups_dialog_gui)

**Qué es:**  
Un **popup** (ventana de diálogo) que contiene un visor Markdown (internamente usando `help_core_pygame`) como contenido interactivo embebido.

**Implicaciones prácticas:**
- La ayuda se integra **como un elemento más del sistema de diálogos**:
  - mismo estilo, marco, botones, layout, etc.
- Al ser un popup, es natural tratarlo como una operación **modal/bloqueante** respecto al popup llamador.
- El patrón recomendado cuando ya estás usando `PopupDialogWindow` u otros popups.

**Cuándo encaja mejor:**
- Cuando quieres coherencia visual y de interacción con el resto de popups.
- Cuando quieres que la ayuda “forme parte” del sistema de diálogos, no como overlay externo.
- Cuando el programa ya se estructura alrededor de `PopupDialogWindow` y kernels interactivos (`InteractiveContent`).

---

## 3. Consideraciones clave (independientes de la demo)

### 3.1 ¿Tu aplicación tiene bucle general de eventos?

Hay dos casos típicos:

#### Caso A: **Un bucle general propio**

Ejemplo: tu `while running:` principal controla eventos, actualizaciones y dibujado.  
Aquí puedes “entrar” en la ayuda y luego volver.

- Con `ShowHelpOverlay()`: normalmente llamas a la función y esta gestiona su mini-bucle modal hasta salir.
- Con `PopupHELP()`: llamas al popup de ayuda, que ejecuta su propia interacción y vuelve al cerrar.

#### Caso B: **Tu UI corre dentro de un `popup.step(events, dt_ms)`**

Ejemplo: una app organizada como un popup principal con kernel interactivo.  
Aquí normalmente:

1) detectas en tu lógica que se solicita ayuda,  
2) **pausas** el popup principal,  
3) muestras la ayuda,  
4) al cerrar, **reanudación** + control de `dt`.

---

### Inciso: qué es `dt` / `dt_ms` y por qué importa al mostrar ayuda

En bucles de juego o simulación es habitual actualizar el estado “en función del tiempo transcurrido desde el último frame”.
A ese tiempo se le suele llamar **`dt`** (*delta time*).

- **`dt`** suele expresarse en **segundos** (float).
- **`dt_ms`** suele expresarse en **milisegundos** (entero).

La idea es que el movimiento y otras evoluciones dependan del tiempo real y no del número de frames. Por ejemplo, si un objeto
se mueve a 200 px/s, en cada frame se avanza:

- `dx = velocidad_px_por_segundo * dt`  (si `dt` está en segundos)
- o equivalentemente `dx = velocidad_px_por_ms * dt_ms` (si trabajas en milisegundos)

**Problema típico al abrir una ayuda modal (overlay o popup):** mientras el usuario lee la ayuda, pasan segundos reales.
Si tu programa calcula `dt` como “ahora - último_frame” y **no lo controlas**, cuando vuelves de la ayuda el primer `dt`
puede ser grande (p. ej., 3000 ms). Eso provoca efectos indeseados: saltos bruscos de animación, físicas inestables,
temporizadores que vencen de golpe o acumulación de pasos de simulación.

**Medidas prácticas para evitarlo:**
1) **Pausar** la simulación (o el popup/kernel) antes de abrir la ayuda (`pause()`), y reanudar después (`resume()`).
2) Al cerrar la ayuda, **resetear/descartar el `dt`** (p. ej. con un `clock.tick(fps)` o re-inicializando el instante
   de referencia), para que el siguiente frame empiece con un `dt` normal.


### 3.2 ¿Hay contenidos dinámicos (animación / simulación)?

- Si NO hay dinámica, el principal riesgo es **visual**: que al cerrar el overlay quede la pantalla “mal”.
- Si SÍ hay dinámica, aparecen además dos riesgos:
  1) **La simulación sigue corriendo** “en tu cabeza” (o acumula `dt`) mientras estás en la ayuda.
  2) Al volver, el primer `dt_ms` puede ser enorme (salto de animación).

**Buenas prácticas típicas:**
- Antes de abrir ayuda, ejecutar `pause()` sobre el contenido/popup principal si existe.
- Al cerrar ayuda:
  - descartar un tick con `clock.tick(fps)` (o reiniciar temporizadores),
  - y luego `resume()`.

---

### 3.3 ¿Congelar o no la ejecución mientras está la ayuda?

Esto depende del patrón:

- `ShowHelpOverlay()` suele ser modal: **tu flujo se interrumpe** y, si no haces nada, la simulación no avanza porque estás dentro del overlay.  
  Aun así, el tiempo real pasa y **`dt` puede acumularse** si lo calculas al volver.
- `PopupHELP()` (modal) también interrumpe el flujo del llamador (lo normal).

La recomendación por defecto cuando hay animación:

- **Congelar** (pausar la simulación) mientras la ayuda está visible.
- Reanudar con un `dt` limpio.

---

### 3.4 ¿Restaurar el frame al cerrar ayuda?

Este punto es crítico en overlays directos:

- Si usas `ShowHelpOverlay()` sobre un `display` que tenía ya un frame “bonito” (o un popup dibujado),
  al cerrar el overlay puede quedar el último dibujo del overlay como fondo si no fuerzas un redibujado inmediato.

Dos estrategias:

1) **Redibujar todo** al volver (loop estándar).  
2) **Congelar/restaurar**: guardar una copia (`screen.copy()`), mostrar overlay, y al salir re-blit + `display.flip()`.

La demo `demo_ask_help.py` pone énfasis en esta segunda.

---

## 4. Qué debe asimilar el usuario con cada demo

### 4.1 `demo_ask_help.py` — “Ayuda como rama de un diálogo”

**Qué enseña (técnico):**
- Uso de `PopupASK()` para decidir un flujo por botones.
- Inserción de ayuda con `ShowHelpOverlay()` **sin** integrar kernels ni crear un popup de ayuda.
- Gestión robusta del retorno visual: patrón de **congelar/restaurar frame**.

**Qué debe asimilar (uso):**
- Un flujo típico de UX:
  - “¿Qué quieres hacer?” → “Ayuda” → vuelvo exactamente al mismo punto.
- La ayuda es una *interrupción breve* y luego el diálogo principal continúa.

**Lecciones prácticas:**
- `ShowHelpOverlay()` es ideal para ayuda “rápida” en flujos sencillos.
- Si tras cerrar ayuda ves artefactos, aplica congelación/restauración o fuerza un redibujado completo.

**Resumen didáctico:**
> “Cómo añadir ayuda a un diálogo con mínima infraestructura: overlay directo + retorno limpio.”

---

### 4.2 `demo_popuphelp_embebido.py` — “Ayuda como popup formal (recomendado en ecosistema popups)”

**Qué enseña (técnico):**
- Un popup principal con kernel interactivo (`SurfacePPsct` + `InteractiveContent`).
- Apertura de ayuda con `PopupHELP()` (la ayuda es otro popup).
- Patrón `pause()` → abrir ayuda → `clock.tick()` para descartar `dt` → `resume()`.

**Qué debe asimilar (uso):**
- Si tu app está basada en popups, la ayuda debe integrarse con el mismo sistema:
  - coherencia visual,
  - interacción estándar,
  - y “modalidad” natural dentro del framework.

**Lecciones prácticas:**
- `PopupHELP()` reduce problemas de integración porque la ayuda ya “encaja” como diálogo.
- Aun así, en presencia de animación debes:
  - pausar el popup principal,
  - limpiar el `dt` al volver.

**Resumen didáctico:**
> “El patrón de ayuda recomendado cuando ya usas popups: la ayuda es un popup, no un overlay externo.”

---

### 4.3 `demo_rebota_controles_ok.py` — “Caso real: kernel dinámico + controles + ayuda”

**Qué enseña (técnico):**
- Un `InteractiveContent` más exigente:
  - ratón (LMB/RMB),
  - rueda,
  - teclado,
  - cambio de tamaño, pausa, y variables de estado.
- Correcta separación entre:
  - coordenadas relativas del kernel y
  - `draw()` aplicando offset del rect.
- Apertura de `PopupHELP()` desde un loop basado en `popup.step(...)` sin romper el flujo.
- Gestión sólida de pausa/reanudación para evitar:
  - salto de animación,
  - acumulación de `dt`,
  - inconsistencia visual.

**Qué debe asimilar (uso):**
- Esta demo valida el escenario “de verdad”:
  - contenido dinámico continuo,
  - mucha interacción,
  - y ayuda modal sin destruir el estado del kernel.

**Lecciones prácticas:**
- En kernels dinámicos, la ayuda debe tratarse como un “modal”:
  - pausa controlada,
  - reanudación con `dt` limpio.
- `PopupHELP()` es especialmente conveniente aquí porque ya está alineado con el framework.

**Resumen didáctico:**
> “La plantilla para integrar ayuda en un sistema interactivo real: input, animación y modalidad bien resueltas.”

---

## 5. Recomendación de aprendizaje (orden sugerido)

1) **`demo_ask_help.py`**  
   Aprende el patrón mínimo: *overlay directo* + retorno correcto.

2) **`demo_popuphelp_embebido.py`**  
   Aprende el patrón recomendado dentro de popups: *PopupHELP* + pausa/reanudación.

3) **`demo_rebota_controles_ok.py`**  
   Aprende la integración avanzada: kernel dinámico, controles, y ayuda sin efectos secundarios.

---

## 6. Checklist de implementación (para tu propia app)

### Si usas `ShowHelpOverlay()`
- [ ] ¿Al volver se redibuja correctamente la pantalla?
- [ ] Si no: ¿congelas/restauras el frame o fuerzas redibujado completo?
- [ ] ¿Hay animación? Si sí:
  - [ ] ¿pausas la simulación antes?
  - [ ] ¿limpias/descartas `dt` al volver?

### Si usas `PopupHELP()`
- [ ] ¿El popup llamador se pausa (`pause()`) antes de abrir la ayuda?
- [ ] ¿Descartas el tick / reinicias temporizadores al salir?
- [ ] ¿Reanudas (`resume()`) correctamente?
- [ ] ¿La ayuda debe ser coherente con el estilo del resto de popups? (normalmente sí)

---

## 7. Cierre

Estas tres demos cubren **tres niveles** de integración, de menos a más estructurado:

- Overlay directo para ayuda “rápida” y flujos simples (`ShowHelpOverlay()`).
- Popup de ayuda integrado cuando ya usas un framework de diálogos (`PopupHELP()`).
- Integración robusta en kernels dinámicos (pausa/reanudación + control de `dt`).

Si reduces demos, este trío mantiene **cobertura didáctica completa** sin redundancia funcional.
