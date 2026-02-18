# Tutorial popups_dialog_gui

## Requisitos
- Python 3 y `pygame`.

## Cómo ejecutar las demos
- Desde el lanzador del proyecto (recomendado): selecciona la demo en la lista.
- Ejecución directa: `python3 <demo>.py` (desde el entorno del proyecto).

## Estructura del tutorial
- Cada sección corresponde a una demo y describe:
  - qué se aprende,
  - qué API se utiliza,
  - y qué resultado debe observarse.

En este tutorial se presentan demos que ilustran distintos aspectos de `popups_dialog_gui`.

Antes que nada recomendamos echar un vistazo al documento **Visión general (ES)**: [OVERVIEW_es.md](OVERVIEW_es.md)

Empezaremos con una demo extremadamente simple, pensada para validar el funcionamiento más básico del proyecto.

Después seguiremos con una demo que aglutina, en sí misma, demostraciones de las funcionalidades más habituales.

Las demos restantes se dedican a ilustrar el uso de `SurfacePPsct` y la inserción de superficies dinámicas, porque su uso
es menos trivial y menos intuitivo. Solo se utiliza cuando queremos incluir dentro de la popup un contenido dinámico.

Incluso sería posible embutir una aplicación completa dentro de un popup; la conveniencia de hacerlo exige valorar pros y contras.
En general, complicaría el código, aunque puede aportar ventajas.

Muchos de los beneficios de `popups_dialog_gui` se pueden obtener con un uso simple, sin necesidad de contenido dinámico.


## Índice de demos
- [1.1) demo_simple.py](#11-demo_simplepy)
- [1.2) demo_Popup_Dialog.py](#12-demo_popup_dialogpy)
- [1.3) demo_Popup_Surface.py](#13-demo_popup_surfacepy)
- [1.4) demo_Popup_Surface_ColorCycle.py](#14-demo_popup_surface_colorcyclepy)
- [1.5) demo_Popup_Surface_Selector.py](#15-demo_popup_surface_selectorpy)
- [2.1) demo_ask_help.py](#21-demo_ask_helppy)
- [2.2) demo_popuphelp_embebido.py](#22-demo_popuphelp_embebidopy)
- [2.3) demo_rebota_controles_ok.py](#23-demo_rebota_controles_okpy)

---

![1.1 demo_simple](images/1.1_demo_simple.png)

## 1.1) demo_simple.py

### Qué aprenderás en esta demo:

1. Inicialización mínima del sistema de popups sobre una ventana Pygame:
  - Se crea la ventana principal (pygame.display.set_mode) y se pasa a IniPopupDialog().
2. Uso de estilos (Style_ID) como primer parámetro de personalización:
  - El usuario elige entre 'playful_childlike' y 'formal', y ese identificador se aplica al módulo.
3. Uso de una función de alto nivel lista para producción:
  - PopupNOTICE() muestra un diálogo modal con un único botón, sin necesidad de construir clases/secciones.
4. Contexto visual:
  - Se dibuja un fondo (círculos) para comprobar que el popup se superpone correctamente al render principal.

### API utilizada (núcleo):
- IniPopupDialog(Display, Style_ID)
- PopupNOTICE(Message, IdButt=...)

### Resultado observable:
- Tras elegir estilo, verás la escena dibujada y luego un popup NOTICE con el estilo seleccionado y un botón "Finalizar".

---

## 1.2) demo_Popup_Dialog.py

![1.2 demo_Popup_Dialog](images/1.2_demo_Popup_Dialog.png)

Al igual que la demo anterior (1.1) empezamos ofreciendo elegir desde el terminal el tipo de estilo.
En la imagen podemos ver como usa una PopupASK() como menú general para elegir lanzar pequeñas demos muy simples, y también el aspecto de una de esas demos que muestra el contenido de nuestro directorio de fuentes.

### Qué aprenderás en esta demo:
1. Cómo usar PopupASK() para implementar menús y flujos de decisión:
  - Un menú no deja de ser una “pregunta” con opciones; el retorno se usa como selector de comportamiento.
2. Diferencias prácticas entre los popups de alto nivel:
  - PopupERR/PopupWARN/PopupNOTICE/PopupINFO muestran variantes visuales para tipos de mensajes diferentes.
3. Ciclo de interacción basado en un bucle de aplicación:
  - Un while True externo que dispara popups secuencialmente, evitando “apilado” de ventanas (modelo modal).
4. Preparación de datos para una demo realista:
  - Generación de un conjunto de ficheros en /tmp para probar paginación/selección con volumen de elementos.
5. Escaneo y selección de ficheros con UI integrada:
  - PopupScanFiles() recorre un directorio y filtra por extensión (ej. fuentes .ttf).
  - PopupSelectionFiles() permite elegir un fichero y devuelve una ruta/nombre para uso posterior.
6. Manejo de rutas “amigables” para UI sin romper la lógica interna:
  - Se mantiene el path absoluto para operar (PathFonts), y se presenta una versión abreviada para textos del menú.
7. Integración con el localizador de assets del proyecto:
  - resolve_asset_layout() centraliza dónde están recursos como fonts_dir y evita hardcode de rutas.

### API utilizada (núcleo):
- IniPopupDialog(Display, Style_ID)
- PopupASK(Message, Buttons, Title=...)
- PopupERR(Message), PopupWARN(Message), PopupNOTICE(Message), PopupINFO(Message)
- PopupScanFiles(dir=..., extension=...)
- PopupSelectionFiles(dir=..., extension=...)
- resolve_asset_layout()  (fonts_dir)

### Resultado observable:
- Desde el menú principal podemos lanzar distintos tipos de popups. Las dos últimas son demos de ficheros:
  (i) escaneo de .ttf en el directorio de fuentes del proyecto y (ii) selección de .txt en /tmp con muchos elementos.
- En la opción de selección, se observa el caso de cancelación (ret == '') y el caso de retorno con ruta/archivo.

---

## 1.3) demo_Popup_Surface.py

### Qué aprenderás en esta demo:

1. Cómo insertar contenido gráfico (una `pygame.Surface`) como “kernel” central de una `PopupDialogWindow`:
  - En lugar de texto (`MessagePPsct`), el contenido principal es una superficie dibujada por el usuario.
2. Relación conceptual con `SurfacePPsct`:
  - El objetivo es entender que existe una sección central pensada para mostrar superficies (y, en demos posteriores, contenidos interactivos).
3. Construcción de superficies reutilizables:
  - Se genera una surface parametrizable por tamaño y título, combinando fondo, figuras y texto renderizado.
4. Comprobación de auto-dimensionado y presentación con tamaños variados:
  - Se muestran tres popups con superficies de dimensiones muy diferentes para observar el comportamiento de layout.

### API utilizada (núcleo):
- IniPopupDialog(Display, Style_ID)
- PopupDialogWindow(KernelContent, ListIdButt, Title=..., FlagAlert=...)
- PopupDialogWindow.Run()

### Resultado observable:
- Se mostrarán tres popups consecutivos (cada uno con botón “Salir”), donde el área central contiene una imagen generada
  con un rótulo que indica el título y el tamaño (p.ej. “Imagen 01 (700x200)”).

---

## 1.4) demo_Popup_Surface_ColorCycle.py

### Qué aprenderás en esta demo:

1. Cómo incrustar contenido “dinámico” dentro del área central del popup usando `SurfacePPsct`:
   - En lugar de pasar una `pygame.Surface` estática, se pasa un objeto que implementa el ciclo de vida de `InteractiveContent`.
2. Cómo usar un *stub* como “adaptador” de comportamiento para prototipar contenido dinámico:
   - Aquí *stub* no se usa con el sentido clásico de pruebas unitarias, sino como un componente **deliberadamente simple** que encapsula
     un comportamiento visual (ciclo de color) para poder integrarlo rápidamente en el popup.
   - Este patrón es clave porque te permite:
     - validar el **pipeline** de integración (montaje → render por frame → desmontaje) sin añadir complejidad de dominio,
     - aislar la lógica del contenido (qué se dibuja) del contenedor (cómo se presenta y se interactúa con el popup),
     - iterar sobre nuevos “widgets” cambiando solo este componente, manteniendo el resto del popup igual.
   - En la práctica, el stub define tres ganchos de ciclo de vida:
     - `on_mount(rect)`: prepara recursos en función del tamaño asignado,
     - `draw(surface, rect)`: dibuja el estado en cada frame,
     - `on_unmount()`: libera/limpia recursos al cerrar.
3. Tamaño fijo para contenido interactivo y control de clipping:
   - `interactive_size=(600, 350)` fuerza un tamaño consistente para el “kernel” interactivo, útil para validar recortes (clipping) y layout.
4. Separación clara de responsabilidades:
   - La demo define un “widget” (`ColorCycle`) centrado en dibujar, mientras que el popup (`PopupDialogWindow`) gestiona marco, título y botones.

### API utilizada (núcleo):
- `IniPopupDialog(Display, Style_ID)`
- `InteractiveContent` (métodos: `on_mount()`, `draw()`, `on_unmount()`)
- `SurfacePPsct(content, ..., interactive_size=...)`
- `PopupDialogWindow(kernel_section, ListIdButt, Title=..., FlagAlert=...)`
- `PopupDialogWindow.Run()`

### Resultado observable:
- Se abre un popup con estilo `playful_childlike` que contiene, en su zona central, un rectángulo coloreado en función del tiempo
  y un texto centrado con la etiqueta “ColorCycle (Paso 2)”. El popup se cierra con el botón “Cerrar”.

---

## demo_Popup_Surface_Selector.py

### Qué aprenderás en esta demo:

1. Cómo construir un selector navegable sobre una colección de superficies (`pygame.Surface`) usando popups:
   - Se parte de una lista base de tamaños y títulos y se transforma en una lista de pares `(surface, ident)` reutilizable.
2. Cómo implementar navegación “Anterior / Posterior” como flujo modal repetido:
   - Un bucle mantiene el índice actual y vuelve a abrir el popup con el elemento correspondiente, ocultando botones cuando procede
     (inicio/fin de la lista).
3. Cómo parametrizar botones y resolver de forma uniforme el retorno del popup:
   - Se define `labels` dinámicamente y se traduce la respuesta de `PopupDialogWindow.Run()` a una etiqueta de botón mediante
     `resolve_button_label()`, soportando retornos como `str`, `int` o `dict`.
4. Cómo usar el título del popup como “identificador” del elemento mostrado:
   - Cada surface se acompaña de una cadena `ident` que se muestra como `Title` y que, al seleccionar, se devuelve como resultado final.
5. Patrón de salida de una demo con confirmación visual:
   - Tras seleccionar o cancelar, se pinta el resultado en la ventana principal durante un intervalo y se termina.

### API utilizada (núcleo):
- `IniPopupDialog(Display, Style_ID)`
- `PopupDialogWindow(KernelContent, ListIdButt, Title=..., FlagAlert=...)`
- `PopupDialogWindow.Run()`

### Resultado observable:
- Se abre un popup que muestra una “imagen” (surface) y ofrece botones para navegar por varias superficies.
- Si se pulsa “Seleccionar”, la demo cierra el flujo y muestra en la ventana principal el identificador elegido.
- Si se pulsa “Cancelar” (o se cierra sin elección), la demo indica “Selección cancelada.” y termina.

---

## 1.5) demo_Popup_Surface_Selector.py

### Qué aprenderás en esta demo:

1. Cómo construir un selector navegable sobre una colección de superficies (`pygame.Surface`) usando popups:
   - Se parte de una lista base de tamaños y títulos y se transforma en una lista de pares `(surface, ident)` reutilizable.
2. Cómo implementar navegación “Anterior / Posterior” como flujo modal repetido:
   - Un bucle mantiene el índice actual y vuelve a abrir el popup con el elemento correspondiente, ocultando botones cuando procede
     (inicio/fin de la lista).
3. Cómo parametrizar botones y resolver de forma uniforme el retorno del popup:
   - Se define `labels` dinámicamente y se traduce la respuesta de `PopupDialogWindow.Run()` a una etiqueta de botón mediante
     `resolve_button_label()`, soportando retornos como `str`, `int` o `dict`.
4. Cómo usar el título del popup como “identificador” del elemento mostrado:
   - Cada surface se acompaña de una cadena `ident` que se muestra como `Title` y que, al seleccionar, se devuelve como resultado final.
5. Patrón de salida de una demo con confirmación visual:
   - Tras seleccionar o cancelar, se pinta el resultado en la ventana principal durante un intervalo y se termina.

### API utilizada (núcleo):
- `IniPopupDialog(Display, Style_ID)`
- `PopupDialogWindow(KernelContent, ListIdButt, Title=..., FlagAlert=...)`
- `PopupDialogWindow.Run()`

### Resultado observable:
- Se abre un popup que muestra una “imagen” (surface) y ofrece botones para navegar por varias superficies.
- Si se pulsa “Seleccionar”, la demo cierra el flujo y muestra en la ventana principal el identificador elegido.
- Si se pulsa “Cancelar” (o se cierra sin elección), la demo indica “Selección cancelada.” y termina.

---

## Parte 2) Demos con ayuda (Markdown)

En esta segunda parte se muestran **tres patrones complementarios** para integrar un sistema de ayuda en Markdown con `help_core_pygame` y `popups_dialog_gui`.

Fecha de referencia: *(informativa; no afecta a las demos)*

---

### Objetivo de esta parte

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

### Bloque común: Dos enfoques: `ShowHelpOverlay()` vs `PopupHELP()`

#### `ShowHelpOverlay(display, md_text, ...)` (help_core_pygame)

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

#### `PopupHELP(md_text, ...)` (popups_dialog_gui)

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

### Consideraciones prácticas (independientes de la demo)

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

### Qué debe asimilar el usuario con cada demo

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


---

## 2.1) demo_ask_help.py

### Qué aprenderás en esta demo:

1. Cómo integrar ayuda Markdown como **overlay directo** mediante `ShowHelpOverlay()`:
   - La ayuda se dibuja sobre el `display` principal y se cierra con `ESC` (o el mecanismo definido por el visor).
2. Cómo usar un popup de decisión (`PopupASK`) con una opción **“Ayuda”** que vuelve al flujo original:
   - Patrón típico: *pregunta → ayuda → vuelvo a la pregunta*.
3. Cómo evitar que el overlay “deje pintado” su último frame:
   - Se aplica un patrón de **congelar/restaurar** el contenido anterior del `display` (copiar, mostrar ayuda, restaurar y hacer `flip`).
4. Cuándo este patrón es suficiente (y cuándo conviene `PopupHELP()`):
   - Si solo quieres ayuda puntual en un flujo simple, el overlay directo es una solución ligera.

### API utilizada (núcleo):
- `IniPopupDialog(Display, Style_ID)`
- `PopupASK(Message, Buttons, Title=...)`
- `PopupNOTICE(Message, IdButt=...)`
- `help_core_pygame.ShowHelpOverlay(Display, MarkdownText, Title=...)`

### Resultado observable:
- Se muestra un `PopupASK` con varias opciones, incluida “Ayuda”.
- Al pulsar “Ayuda” aparece un visor Markdown en overlay.
- Al salir de la ayuda, se recupera la pantalla anterior y el flujo vuelve al `PopupASK` sin artefactos.

---

## 2.2) demo_popuphelp_embebido.py

### Qué aprenderás en esta demo:

1. Diferencia práctica entre overlay directo y **ayuda como popup**:
   - Aquí la ayuda no se dibuja “por encima” como overlay, sino que se abre un **popup de ayuda** mediante `PopupHELP()`.
2. Cómo pausar un popup con contenido dinámico antes de mostrar ayuda:
   - Patrón recomendado: `popup.pause()` → `PopupHELP(...)` → limpieza de `dt` → `popup.resume()`.
3. Ventajas de `PopupHELP()` dentro del ecosistema `popups_dialog_gui`:
   - Coherencia visual (marco, estilo, botones), y un comportamiento modal alineado con el resto de popups.

### API utilizada (núcleo):
- `IniPopupDialog(Display, Style_ID)`
- `PopupDialogWindow(...).Run()` (popup principal)
- `SurfacePPsct(InteractiveContent, interactive_size=...)`
- `PopupHELP(MarkdownText, Title=..., interactive_size=..., ...)`

### Resultado observable:
- En el popup principal se observa un kernel con animación (p.ej. bola rebotando).
- Al pulsar “Ayuda” se abre un popup de ayuda con scroll.
- Al cerrar la ayuda, vuelve el popup principal y la animación continúa sin “saltos” ni pérdida de estado.

---

## 2.3) demo_rebota_controles_ok.py

### Qué aprenderás en esta demo:

1. Integración robusta de un kernel interactivo “real” (`InteractiveContent`) dentro de un popup:
   - Ratón (LMB/RMB), rueda, teclado, pausa y cambios de tamaño/velocidad.
2. Correcta gestión de coordenadas y offsets del kernel:
   - El contenido trabaja en coordenadas relativas al área útil y `draw()` aplica el offset del rect del kernel.
3. Uso de `PopupHELP()` en un bucle basado en `popup.step(events, dt_ms)`:
   - La demo muestra cómo abrir ayuda sin romper el flujo del bucle principal del popup.
4. Prácticas recomendadas con ayuda modal en contenido dinámico:
   - Pausar, descartar `dt` al volver y reanudar de forma limpia para evitar inestabilidades.

### API utilizada (núcleo):
- `IniPopupDialog(Display, Style_ID)`
- `PopupDialogWindow.step(events, dt_ms)` (loop del popup)
- `SurfacePPsct(InteractiveContent, interactive_size=...)`
- `PopupHELP(MarkdownText, Title=..., ...)`

### Resultado observable:
- Se ve un popup con partículas/objetos rebotando y varios controles de interacción.
- El botón “Ayuda” abre un popup de ayuda.
- Tras cerrar la ayuda, el contenido se reanuda sin saltos de animación ni errores de input.

### Recomendación de aprendizaje (orden sugerido)

1) **`demo_ask_help.py`**  
   Aprende el patrón mínimo: *overlay directo* + retorno correcto.

2) **`demo_popuphelp_embebido.py`**  
   Aprende el patrón recomendado dentro de popups: *PopupHELP* + pausa/reanudación.

3) **`demo_rebota_controles_ok.py`**  
   Aprende la integración avanzada: kernel dinámico, controles, y ayuda sin efectos secundarios.

---

### Checklist de implementación (para tu propia app)

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

### Cierre

Estas tres demos cubren **tres niveles** de integración, de menos a más estructurado:

- Overlay directo para ayuda “rápida” y flujos simples (`ShowHelpOverlay()`).
- Popup de ayuda integrado cuando ya usas un framework de diálogos (`PopupHELP()`).
- Integración robusta en kernels dinámicos (pausa/reanudación + control de `dt`).


