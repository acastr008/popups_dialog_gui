# popups_dialog_gui: (API_REFERENCE_es.md)  19/ene/2026

## Listado estructurado de la API

### **Módulo Popup_Dialog.py**

- **Funciones del módulo** 
  
  - [DrawRect()](#popup_dialog_py_drawrect)
  - [GetFont()](#popup_dialog_py_getfont)
  - [GetStyleDict()](#popup_dialog_py_getstyledict)
  - [get_style()](#popup_dialog_py_get_style)
  - [set_style_overrides()](#popup_dialog_py_set_style_overrides)
  - [IniPopupDialog()](#popup_dialog_py_inipopupdialog)
  - [TestIni()](#popup_dialog_py_testini)
  - [GetWidthHeigthText()](#popup_dialog_py_getwidthheigthtext)
  - [PopupERR()](#popup_dialog_py_popuperr)
  - [PopupWARN()](#popup_dialog_py_popupwarn)
  - [PopupNOTICE()](#popup_dialog_py_popupnotice)
  - [PopupINFO()](#popup_dialog_py_popupinfo)
  - [PopupASK()](#popup_dialog_py_popupask)
  - [MenuScanFiles()](#popup_dialog_py_menuscanfiles)
  - [MenuSelectFiles()](#popup_dialog_py_menuselectfiles)
  - [GetList_Num_Filenames()](#popup_dialog_py_getlist_num_filenames)
  - [PopupSelectionFiles()](#popup_dialog_py_popupselectionfiles)
  - [PopupScanFiles()](#popup_dialog_py_popupscanfiles)
  - [PopupMens_ERR_WARN_NOTICE_INFO()](#popup_dialog_py_popupmens_err_warn_notice_info)
  - [PopupHELP()](#popup_dialog_py_popuphelp)

### **Modulo adapters.py**

- **Funciones del modulo**
  
  - [run_help_popup_from_md()](#adapters_py_run_help_popup_from_md)

- **Clases**
  
  - `HelpAsInteractive`
    - [on_mount()](#adapters_py_helpasinteractive_on_mount)
    - [on_unmount()](#adapters_py_helpasinteractive_on_unmount)
    - [update()](#adapters_py_helpasinteractive_update)
    - [draw()](#adapters_py_helpasinteractive_draw)
    - [handle_event()](#adapters_py_helpasinteractive_handle_event)
    - [wants_keyboard()](#adapters_py_helpasinteractive_wants_keyboard)
    - [wants_wheel()](#adapters_py_helpasinteractive_wants_wheel)

- **Clase - PopupDialogWindow**
  *La idea de crear una clase PopupDialogWindow es la de diseñar un objeto para simplificar al máximo la creación de ventanas emergentes simuladas con Pygame.*
  
  ***PopupDialogWindow(KernelContent: Any, ListIdButt: Any, Title: str = 'Aviso', FlagAlert: str = 'Green', PosCenter: Any = None)***
  
  - **Métodos**
    - [Draw()](#popup_dialog_py_popupdialogwindow_draw)
    - [Run()](#popup_dialog_py_popupdialogwindow_run)
    - [step()](#popup_dialog_py_popupdialogwindow_step)
    - [pause()](#popup_dialog_py_popupdialogwindow_pause)
    - [resume()](#popup_dialog_py_popupdialogwindow_resume)

- **Clase - PopupSection**
  *Clase base de las diferentes secciones que componen una PopupDialogWindow.*
  
  ***PopupSection(W_Margin: Any, H_Margin: Any, FontType: Any, FontSize: Any, ColorFg: Any, ColorBg: Any, BorderThikness: Any, BorderColor: Any)***
  
  - **Métodos**
    - [Draw()](#popup_dialog_py_popupsection_draw)

- **Clase - TitlePPsct**
  *Sección superior correspondiente al título.*
  
  ***- TitlePPsct(W_Margin: Any, H_Margin: Any, FontType: Any, FontSize: Any, ColorFg: Any, ColorBg: Any, BorderThikness: Any, BorderColor: Any, TxtTitle: Any)***
  
  - **Métodos**
    - [GetWidthHeigthTitle()](#popup_dialog_py_titleppsct_getwidthheigthtitle)
    - [Draw()](#popup_dialog_py_titleppsct_draw)

- **Clase - MessagePPsct**
  *Sección central para texto.*
  
  ***MessagePPsct(W_Margin: Any, H_Margin: Any, FontType: Any, FontSize: Any, ColorFg: Any, ColorBg: Any, BorderThikness: Any, BorderColor: Any, Message: Any, PorcSepLines: Any)***
  
  - **Métodos**
    - [GetWidthHeigthMessage()](#popup_dialog_py_messageppsct_getwidthheigthmessage)
    - [Draw()](#popup_dialog_py_messageppsct_draw)

- **Clase - ListButtonsPPsct**
  *Sección inferior con uno o más botones.*
  
  ***ListButtonsPPsct(W_Margin: Any, H_Margin: Any, FontType: Any, FontSize: Any, ColorFg: Any, ColorBg: Any, BorderThikness: Any, BorderColor: Any, ListIdButt: Any, ButtPadding: Any, ColorBgBut: Any)***
  
  - **Métodos**
    - [GetWidthHeigthContent()](#popup_dialog_py_listbuttonsppsct_getwidthheigthcontent)
    - [Draw()](#popup_dialog_py_listbuttonsppsct_draw)

- **Clase - SurfacePPsct**
  *Sección central para contenidos de una PopupDialogWindow. Este contenido puede ser una pygame.Surface estática o un contenido interactivo.*
  
  ***SurfacePPsct(content_or_surface: Any, W_Margin: Any = None, H_Margin: Any = None, BorderThikness: Any = None, BorderColor: Any = None, *, interactive_size: Any = None)***
  
  - **Métodos**
    - [Draw()](#popup_dialog_py_surfaceppsct_draw)
    - [GetWidthHeigthSurface()](#popup_dialog_py_surfaceppsct_getwidthheigthsurface)
    - [GetWidthHeigthMessage()](#popup_dialog_py_surfaceppsct_getwidthheigthmessage)
    - [update()](#popup_dialog_py_surfaceppsct_update)
    - [handle_event()](#popup_dialog_py_surfaceppsct_handle_event)
    - [wants_keyboard()](#popup_dialog_py_surfaceppsct_wants_keyboard)
    - [wants_wheel()](#popup_dialog_py_surfaceppsct_wants_wheel)

- **Clase - HelpPPsct**
  *Sección central que integra un visor de ayuda Markdown (HelpViewer) via `help_core_pygame` y `HelpConfig`.*
  
  ***HelpPPsct(md_text: Any, interactive_size: Any, W_Margin: Any, H_Margin: Any, BorderThikness: Any, BorderColor: Any, *, title: str = 'Ayuda', style_variant: str = 'formal', style_json_path: Any = None, fonts_dir: Any = None, help_font_file: Any = None, help_code_font_file: Any = None, kernel_bg: Any = None, wheel_step: int = 48, visual_indent_px: int = 24, indent_spaces_per_level: int = 2)***
  
  - **Métodos**
    - [GetWidthHeigthMessage()](#popup_dialog_py_helpppsct_getwidthheigthmessage)
    - [Draw()](#popup_dialog_py_helpppsct_draw)
    - [on_mount()](#popup_dialog_py_helpppsct_on_mount)
    - [on_unmount()](#popup_dialog_py_helpppsct_on_unmount)
    - [update()](#popup_dialog_py_helpppsct_update)
    - [handle_event()](#popup_dialog_py_helpppsct_handle_event)
    - [wants_keyboard()](#popup_dialog_py_helpppsct_wants_keyboard)
    - [wants_wheel()](#popup_dialog_py_helpppsct_wants_wheel)

### **Módulo interactive_content.py**

- **Clase - InteractiveContent**
  *Base opcional para contenidos interactivos/animados que irán embebidos en SurfacePPsct.*
  
  ***InteractiveContent(*args: Any, **kwargs: Any)***
  
  - **Métodos**
    - [on_mount()](#interactive_content_py_interactivecontent_on_mount)
    - [on_unmount()](#interactive_content_py_interactivecontent_on_unmount)
    - [update()](#interactive_content_py_interactivecontent_update)
    - [draw()](#interactive_content_py_interactivecontent_draw)
    - [handle_event()](#interactive_content_py_interactivecontent_handle_event)
    - [wants_keyboard()](#interactive_content_py_interactivecontent_wants_keyboard)
    - [wants_wheel()](#interactive_content_py_interactivecontent_wants_wheel)

## Resumen de contabilidad de la API

### Totales

- **Módulos:** 3  
- **Funciones a nivel de módulo:** 22  
- **Clases:** 10  
- **Métodos (sumatorio de métodos listados por clase, sin contar constructores):** 43  

### Desglose por módulo

#### Popup_Dialog.py

- **Funciones de módulo:** 21  
- **Clases:** 8  
- **Métodos (en clases):** 29  

#### adapters.py

- **Funciones de módulo:** 1  
- **Clases:** 1  
- **Métodos (en clases):** 7  

#### interactive_content.py

- **Funciones de módulo:** 0  
- **Clases:** 1  
- **Métodos (en clases):** 7  

---

## Descripción del módulo principal Popup_Dialog.py

Popup_Dialog_Py.py es un módulo de ventanas emergentes (pop-up) usando pygame para generar avisos, diálogos, etc. 
y está basada en Pygame. 

### Inicialización

Antes de usar el módulo, es necesario inicializarlo comunicando 
la pantalla Pygame y el estilo que vamos a usar.
Sobre el estilo elegido podemos hacer variaciones pero han de hacerse inmediatamente después de IniPopupDialog() y antes de construir SurfacePPsct/PopupDialogWindow, para que las nuevas
métricas (padding, bordes, márgenes, etc.) se tengan en cuenta al medir
y maquetar las secciones.

Ejemplo:

```
IniPopupDialog(screen, "playful_childlike")
set_style_overrides({
    "Kernel": {"Padding": 0, "Border": 0},
    "Section_Margins": {"Top": 0, "Right": 0, "Bottom": 0, "Left": 0},
})
popup = PopupDialogWindow(...)
```

### Caraterísticas generales de las ventanas

Estas ventanas pop-up tienen tres secciones dispuestas verticalmente y hacen uso de la clase PopupDialogWindow()
La sección superior para el título o para indicar el tipo de mensaje, la siguiente es una sección que dará cabida
al texto del mensaje y finalmente una inferior con uno o más botones.

El método Draw aparece en varias clases con diferentes cometidos para cada una de es tres secciones mencionadas. 
Una vez se obtiene el dibujo de una sección se dispondran convenientemente para dibujar todas ellas en la clase de nivel superior.

```
class PopupDialogWindow:
    class PopupSection: ((agregación))
        Draw(self):  # definicion del método abstracto Draw() para PopupSection

    class TitlePPsct(PopupSection):
        Draw(self, x, y, Wide, Heigth, BorderRadius): # Dibuja la sección del título en la parte alta

    class MessagePPsct(PopupSection):
        -.Draw(self, x, y, Wide, Heigth, BorderRadius, PorcSepLines=130): # Dibuja la sección central

    class ListButtonsPPsct(PopupSection):
        -.Draw(self, x, y, Wide, Heigth, BorderRadius): # Dibuja la sección inferior con los botones de acción.  
```

### Consideraciones de uso

La ventana principal de pygame tendrá que venir ya inicializada y será guardada en una variable global 'gameDisplay'.
Esta decisión de diseño se hizo para evitar tener que pasarla continuamente como parámetro a un montón de funciones. 

### Generalidades sobre las funciones públicas principales:

- **PopupERR(), PopupWARN(), PopupNOTICE(), PopupINFO():**
  Estas cuatro funciones son PopupDialogWindow y son similares. Se usan para distinto tipo de nivel de alerta. 
  Tras mostrar la información permiten salir cerrando la ventana pulsando un botón.

- **PopupASK():**
  También es una PopupDialogWindow, similar a las anteriores y requiere una lista de identificadores para poder ofrecer varios botones con una total libertad de usos. 
  Esto se presta a hacer uso de este tipo de ventanas no solo para las preguntas típicas de 'Confirmar', 'Cancelar', 'Reintentar', sino para cualquier otro tipo de preguntas, lo que da pie a usarla para funcionalidades muy diversas. 
  Un ejemplo inmediato es la posibilidad de usarlas para obtener una funcionalidad de menú tal y como puede verse en la Demo.

- **PopupSelectionFiles():**
  Basándonos en la PopupASK() que acabamos de describir, se ha implementado un procedimiento que permite seleccionar ficheros de un directorio. 
  Se puede obligar a que solo considere los ficheros que tengan una determinada extensión.  El diseño es muy sencillo, pero pese a ello admite que los nombre de los ficheros puedan ser muy largos y que el número de los ficheros contenidos en el directorio sean muy numerosos ya que para seleccionar alguno de ellos nos permitirá ir mostrando los nombres de ficheros paginando la información. 

--- 

# Documentación de código para las funciones de alto nivel.

## Popup_Dialog.py — Funciones de módulo

<a id="popup_dialog_py_drawrect"></a>

### Popup_Dialog.py — DrawRect(BgColor, BorderColor, Rect, BorderThikness, BorderRadius)

"""Dibuja un rectángulo con fondo y borde (opcional) sobre gameDisplay, admitiendo esquinas redondeadas.

**Parámetros:**

- BgColor: Color de relleno (RGB/RGBA o pygame.Color).
- BorderColor: Color del borde.
- Rect: Geometría destino (pygame.Rect o tupla x,y,w,h).
- BorderThikness (int): Grosor del borde (0 para sin borde).
- BorderRadius (int): Radio de redondeo (0 para esquina recta).

**Notas:**

- Requiere que gameDisplay esté inicializado (IniPopupDialog/TestIni).
- Pinta primero el fondo y luego el borde."""

<a id="popup_dialog_py_getfont"></a>

### Popup_Dialog.py — GetFont(FontType, FontSize)

"""Carga y devuelve una fuente TrueType usando pygame.font.Font.

**Parámetros:**

- FontType (str): Ruta (relativa o absoluta) al fichero de fuente (p.ej. *.ttf).
- FontSize (int): Tamaño de la fuente en píxeles.

**Retorno:**

- pygame.font.Font: Objeto fuente listo para renderizar texto.

**Notas:**

- Si existe la variable de entorno POPUP_PROY_ROOT, se antepone como raíz del proyecto.
- Lanza excepción si no puede cargar la fuente.""" 

<a id="popup_dialog_py_inipopupdialog"></a>

### Popup_Dialog.py — IniPopupDialog(Display=None, Style_ID=None)

"""Inicializa el módulo: fija la superficie principal (gameDisplay) y carga el estilo ST desde JSON.

**Parámetros:**

- Display: pygame.Surface principal ya creada (p.ej. pygame.display.get_surface()).
- Style_ID (str): Identificador de estilo (p.ej. "playful_childlike" o "formal").

**Efectos:**

- Define globals: gameDisplay, Style_id y ST.
- Carga estilo base y variantes desde JSON (si aplica) y valida que el Style_ID exista.

**Errores:**

- KeyError si el estilo no existe en los JSON cargados.
- Propaga errores de lectura/parseo JSON o de ruta.

**Notas:**

- Al final llama a TestIni() para verificar coherencia mínima.
- Si vas a llamar a set_style_overrides(), hazlo justo después de IniPopupDialog() y antes de crear PopupDialogWindow/SurfacePPsct.""" 

<a id="popup_dialog_py_get_style"></a>

### Popup_Dialog.py — get_style()

"""Devuelve el diccionario de estilo activo (ST).

**Retorno:**

- dict: Estilo activo (mismo objeto global).

**Notas:**

- Se expone para lectura; si se modifica directamente afectará al render.
- Para cambios controlados se recomienda set_style_overrides().""" 

<a id="popup_dialog_py_set_style_overrides"></a>

### Popup_Dialog.py — set_style_overrides(overrides)

"""Aplica overrides (parciales) al estilo activo ST mediante actualización profunda.

**Parámetros:**

- overrides (dict): Diccionario parcial con claves/valores a fusionar sobre ST.

**Retorno:**

- None

**Notas:**

- Debe invocarse después de IniPopupDialog() y antes de instanciar popups, para que las métricas
  (padding, bordes, márgenes) se usen correctamente en el cálculo de tamaños.""" 

<a id="popup_dialog_py_getstyledict"></a>

### Popup_Dialog.py — GetStyleDict()

"""Devuelve el diccionario de estilo activo (ST) tal y como fue cargado en IniPopupDialog().

**Retorno:**

- dict | None: El estilo activo, o None si todavía no se inicializó.

**Notas:**

- Se mantiene por compatibilidad; para validar inicialización usa TestIni().
- El dict retornado es el mismo objeto global (modificarlo afecta al render).""" 

<a id="popup_dialog_py_testini"></a>

### Popup_Dialog.py — TestIni()

"""Verifica que el módulo está inicializado y que el estilo/configuración mínima es válida.

**Validaciones típicas:**

- Style_id debe pertenecer al conjunto soportado.
- gameDisplay debe ser una superficie pygame válida (se comprueba con get_size()).

**Errores:**

- ValueError si el estilo no es válido.
- Propaga excepciones si la superficie no está inicializada.""" 

<a id="popup_dialog_py_getwidthheigthtext"></a>

### Popup_Dialog.py — GetWidthHeigthText(Text, Font, PorcSepLines=130)

"""Calcula el tamaño (ancho, alto) de un texto multilínea renderizado con una fuente dada.

**Parámetros:**

- Text (str): Texto con posibles saltos de línea.
- Font (pygame.font.Font): Fuente ya cargada.
- PorcSepLines (int): Factor porcentual de separación vertical entre líneas (p.ej. 130).

**Retorno:**

- tuple[int, int]: (ancho, alto) estimados para el bloque de texto.

**Notas:**

- Se usa para dimensionar secciones de mensaje y el layout global de la popup.""" 

<a id="popup_dialog_py_popupmens_err_warn_notice_info"></a>

### Popup_Dialog.py — PopupMens_ERR_WARN_NOTICE_INFO(Message, Title, FlagAlert)

"""Popup interno (no recomendado como API estable) para mensajes con un único botón de continuación.

**Parámetros:**

- Message (str): Texto del mensaje a mostrar.
- Title (str): Título de la ventana emergente.
- FlagAlert (str): Nivel/color de alerta ("Green", "Yellow", "Orange", "Red", "Blue").

**Efectos:**

- Crea una PopupDialogWindow modal y bloquea hasta que el usuario pulse continuar.
- No retorna valor (flujo “acknowledge”).""" 

<a id="popup_dialog_py_popuperr"></a>

### Popup_Dialog.py — PopupERR(Message, IdButt='   Continuar   ', Title='Mensaje de error', FlagAlert='Red')

"""Muestra un popup de error con un único botón.

**Retorno:**

- None""" 

<a id="popup_dialog_py_popupwarn"></a>

### Popup_Dialog.py — PopupWARN(Message, IdButt='   Continuar   ', Title='Advertencia importante', FlagAlert='Orange')

"""Muestra un popup de advertencia (warning) con un único botón.

**Retorno:**

- None""" 

<a id="popup_dialog_py_popupnotice"></a>

### Popup_Dialog.py — PopupNOTICE(Message, IdButt='   Continuar   ', Title='Aviso', FlagAlert='Yellow')

"""Muestra un popup de aviso (notice) con un único botón.

**Retorno:**

- None""" 

<a id="popup_dialog_py_popupinfo"></a>

### Popup_Dialog.py — PopupINFO(Message, IdButt='   Continuar   ', Title='Mensaje informativo', FlagAlert='Green')

"""Muestra un popup de información con un único botón.

**Retorno:**

- None""" 

<a id="popup_dialog_py_popupask"></a>

### Popup_Dialog.py — PopupASK(Message, ListIdButt, Title='Pregunta', FlagAlert='Blue')

"""Muestra un popup con uno o más botones y devuelve la etiqueta pulsada.

**Retorno:**

- str: Etiqueta/identificador del botón pulsado.""" 

<a id="popup_dialog_py_menuscanfiles"></a>

### Popup_Dialog.py — MenuScanFiles(Page, PageNum, TotNumPages)

"""Construye un menú paginado (solo lectura) para listar ficheros y navegar por páginas.

**Parámetros:**

- Page: Lista de tuplas (num, filename) correspondientes a la página actual.
- PageNum (int): Índice de página actual (0-based).
- TotNumPages (int): Número total de páginas.

**Retorno:**

- str: Identificador del botón pulsado (p.ej. " Re.Pag ", " Av.Pag " o " Finalizar visualización ").""" 

<a id="popup_dialog_py_menuselectfiles"></a>

### Popup_Dialog.py — MenuSelectFiles(Page, PageNum, TotNumPages)

"""Construye un menú paginado para seleccionar un fichero por número o navegar entre páginas.

**Parámetros:**

- Page: Lista de tuplas (num, filename) de la página actual.
- PageNum (int): Índice de página actual (0-based).
- TotNumPages (int): Número total de páginas.

**Retorno:**

- str: Etiqueta del botón pulsado:
  - " Cancelar " para abortar,
  - " Re.Pag " / " Av.Pag " para navegación,
  - o un número ("1", "2", ...) para seleccionar el fichero.""" 

<a id="popup_dialog_py_getlist_num_filenames"></a>

### Popup_Dialog.py — GetList_Num_Filenames(dir, extension, readable, sort)

"""Obtiene la lista (numerada) de ficheros de un directorio y genera su paginación.

**Parámetros:**

- dir (str): Directorio a escanear.
- extension (str | None): Extensión a filtrar (sin punto) o None para no filtrar.
- readable (bool): Si True, filtra por ficheros legibles.
- sort (str): Política de ordenación (según implementación; p.ej. 'nd').

**Retorno:**

- tuple[list[tuple[int,str]], list[list[tuple[int,str]]]]:
  - List_Num_Filenames: lista completa numerada (num, filename)
  - listPagesFilenames: lista de páginas, cada una con su subconjunto (num, filename)""" 

<a id="popup_dialog_py_popupselectionfiles"></a>

### Popup_Dialog.py — PopupSelectionFiles(dir='.', extension=None, readable=True, sort='nd', Title='Seleccionar Fichero', FlagAlert='Blue')

"""Permite seleccionar un fichero del directorio usando popups paginados.

**Retorno:**

- str: Nombre del fichero seleccionado (incluye directorio) o "" si el usuario cancela.""" 

<a id="popup_dialog_py_popupscanfiles"></a>

### Popup_Dialog.py — PopupScanFiles(dir='.', extension=None, readable=True, sort='nd', Title='Seleccionar Fichero', FlagAlert='Blue')

"""Permite explorar (solo lectura) un directorio en modo paginado.

**Retorno:**

- None""" 

<a id="popup_dialog_py_popuphelp"></a>

### Popup_Dialog.py — PopupHELP(md_text, IdButt='   Cerrar ayuda   ', Title='Ayuda', FlagAlert='Blue', *, interactive_size=(800, 480), W_Margin=None, H_Margin=None, BorderThikness=None, BorderColor=None, title=None, style_variant='formal', style_json_path=None, fonts_dir=None, help_font_file=None, help_code_font_file=None, kernel_bg=None, wheel_step=48, visual_indent_px=24)

"""Muestra un popup con un visor de ayuda Markdown embebido como contenido interactivo.

**Dependencias:**

- Requiere `help_core_pygame` (HelpViewer + HelpConfig).

**Parámetros clave:**

- md_text (str): Texto Markdown a visualizar.
- interactive_size (tuple[int,int]): Tamaño lógico del área interactiva (w,h).
- (resto): Parámetros de márgenes/borde del kernel, y configuración del HelpViewer.

**Retorno:**

- str: Etiqueta/identificador del botón pulsado (normalmente el de cierre).""" 

### Popup_Dialog.py — (_privada) _deep_update(dst, src) -> None

"""Actualiza recursivamente un dict destino con las claves del dict origen.

**Notas:**

- Utilidad interna para fusionar overrides de estilo.
- No se considera API estable."""

## Popup_Dialog.py — Clases (constructores y métodos)

<a id="popup_dialog_py_popupdialogwindow_init"></a>

### Popup_Dialog.py — PopupDialogWindow.__init__(self, KernelContent, ListIdButt, Title='Aviso', FlagAlert='Green', PosCenter=None)

"""Construye una ventana emergente compuesta por: título, kernel central y botones.""" 

<a id="popup_dialog_py_popupdialogwindow_draw"></a>

### Popup_Dialog.py — PopupDialogWindow.Draw(self)

"""Dibuja la ventana emergente completa (marco + secciones) sobre la superficie principal.""" 

<a id="popup_dialog_py_popupdialogwindow_step"></a>

### Popup_Dialog.py — PopupDialogWindow.step(self, events, dt_ms)

"""Procesa un “tick” no bloqueante: enruta eventos y actualiza el contenido.

**Retorno:**

- str | None: Etiqueta del botón pulsado si se resuelve el diálogo; None si continúa abierto.""" 

<a id="popup_dialog_py_popupdialogwindow_run"></a>

### Popup_Dialog.py — PopupDialogWindow.Run(self)

"""Ejecuta el bucle modal hasta que el usuario pulse un botón de salida.

**Retorno:**

- str: Etiqueta/identificador del botón pulsado.""" 

<a id="popup_dialog_py_popupdialogwindow_pause"></a>

### Popup_Dialog.py — PopupDialogWindow.pause(self)

"""Pausa la actualización del contenido (si el bucle externo decide respetarlo).""" 

<a id="popup_dialog_py_popupdialogwindow_resume"></a>

### Popup_Dialog.py — PopupDialogWindow.resume(self)

"""Reanuda la actualización del contenido (si el bucle externo decide respetarlo).""" 

<a id="popup_dialog_py_popupsection_init"></a>

### Popup_Dialog.py — PopupSection.__init__(self, W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, BorderThikness, BorderColor)

"""Constructor base de una sección de popup: guarda estilo, márgenes, tipografía, colores y borde.""" 

<a id="popup_dialog_py_popupsection_draw"></a>

### Popup_Dialog.py — PopupSection.Draw(self)

"""Método abstracto de renderizado para una sección de popup."""

<a id="popup_dialog_py_titleppsct_init"></a>

### Popup_Dialog.py — TitlePPsct.__init__(self, W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, BorderThikness, BorderColor, TxtTitle)

"""Crea la sección superior de título y prepara su fuente.""" 

<a id="popup_dialog_py_titleppsct_getwidthheigthtitle"></a>

### Popup_Dialog.py — TitlePPsct.GetWidthHeigthTitle(self)

"""Devuelve el tamaño necesario (W,H) para renderizar el título con el estilo actual.""" 

<a id="popup_dialog_py_titleppsct_draw"></a>

### Popup_Dialog.py — TitlePPsct.Draw(self, x, y, Wide, Heigth, BorderRadius)

"""Dibuja la sección del título en la parte superior del popup.""" 

<a id="popup_dialog_py_messageppsct_init"></a>

### Popup_Dialog.py — MessagePPsct.__init__(self, W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, BorderThikness, BorderColor, Message, PorcSepLines)

"""Crea la sección central de mensaje, almacenando texto y política de separación de líneas.""" 

<a id="popup_dialog_py_messageppsct_getwidthheigthmessage"></a>

### Popup_Dialog.py — MessagePPsct.GetWidthHeigthMessage(self)

"""Devuelve el tamaño total (W,H) requerido por el mensaje (incluye márgenes y borde).""" 

<a id="popup_dialog_py_messageppsct_draw"></a>

### Popup_Dialog.py — MessagePPsct.Draw(self, x, y, Wide, Heigth, BorderRadius, PorcSepLines=130)

"""Dibuja la sección de mensaje (texto multilínea) dentro del área asignada.""" 

<a id="popup_dialog_py_listbuttonsppsct_init"></a>

### Popup_Dialog.py — ListButtonsPPsct.__init__(self, W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, BorderThikness, BorderColor, ListIdButt, ButtPadding, ColorBgBut)

"""Crea la sección inferior de botones y prepara su layout.""" 

<a id="popup_dialog_py_listbuttonsppsct_getwidthheigthcontent"></a>

### Popup_Dialog.py — ListButtonsPPsct.GetWidthHeigthContent(self)

"""Devuelve el tamaño total (W,H) requerido por la zona de botones.""" 

<a id="popup_dialog_py_listbuttonsppsct_draw"></a>

### Popup_Dialog.py — ListButtonsPPsct.Draw(self, x, y, Wide, Heigth, BorderRadius)

"""Dibuja la sección inferior con los botones de acción.""" 

<a id="popup_dialog_py_surfaceppsct_init"></a>

### Popup_Dialog.py — SurfacePPsct.__init__(self, content_or_surface, W_Margin=None, H_Margin=None, BorderThikness=None, BorderColor=None, *, interactive_size=None)

"""Construye el kernel central para mostrar una Surface estática o un contenido interactivo.""" 

<a id="popup_dialog_py_surfaceppsct_draw"></a>

### Popup_Dialog.py — SurfacePPsct.Draw(self, x, y, Wide, Heigth, BorderRadius=0)

"""Dibuja la sección de kernel basada en Surface o contenido interactivo dentro del área asignada.""" 

<a id="popup_dialog_py_surfaceppsct_getwidthheigthmessage"></a>

### Popup_Dialog.py — SurfacePPsct.GetWidthHeigthMessage(self)

"""Alias de compatibilidad para obtener el tamaño total de la sección de kernel.""" 

<a id="popup_dialog_py_surfaceppsct_getwidthheigthsurface"></a>

### Popup_Dialog.py — SurfacePPsct.GetWidthHeigthSurface(self)

"""Calcula el tamaño total requerido por la sección SurfacePPsct.""" 

<a id="popup_dialog_py_surfaceppsct_update"></a>

### Popup_Dialog.py — SurfacePPsct.update(self, dt_ms)

"""Actualiza el estado del contenido interactivo del kernel, si existe.""" 

<a id="popup_dialog_py_surfaceppsct_handle_event"></a>

### Popup_Dialog.py — SurfacePPsct.handle_event(self, event)

"""Enruta eventos al contenido interactivo (si existe) y devuelve True si el contenido los consume.""" 

<a id="popup_dialog_py_surfaceppsct_wants_keyboard"></a>

### Popup_Dialog.py — SurfacePPsct.wants_keyboard(self)

"""Indica si el kernel desea recibir eventos de teclado.""" 

<a id="popup_dialog_py_surfaceppsct_wants_wheel"></a>

### Popup_Dialog.py — SurfacePPsct.wants_wheel(self)

"""Indica si el kernel desea recibir eventos de rueda del ratón.""" 

<a id="popup_dialog_py_helpppsct_init"></a>

### Popup_Dialog.py — HelpPPsct.__init__(self, md_text, interactive_size, W_Margin, H_Margin, BorderThikness, BorderColor, *, title='Ayuda', style_variant='formal', style_json_path=None, fonts_dir=None, help_font_file=None, help_code_font_file=None, kernel_bg=None, wheel_step=48, visual_indent_px=24, indent_spaces_per_level=2)

"""Construye la sección de ayuda que integra un HelpViewer (Markdown) dentro del popup.""" 

<a id="popup_dialog_py_helpppsct_draw"></a>

### Popup_Dialog.py — HelpPPsct.Draw(self, x, y, Wide, Heigth, BorderRadius)

"""Dibuja el área de ayuda (viewport del HelpViewer) dentro del rectángulo asignado.""" 

<a id="popup_dialog_py_helpppsct_on_mount"></a>

### Popup_Dialog.py — HelpPPsct.on_mount(self, rect)

"""Hook de montaje: informa al visor del rectángulo absoluto útil para render y eventos.""" 

<a id="popup_dialog_py_helpppsct_on_unmount"></a>

### Popup_Dialog.py — HelpPPsct.on_unmount(self)

"""Hook de desmontaje para la sección de ayuda (HelpViewer).""" 

<a id="popup_dialog_py_helpppsct_update"></a>

### Popup_Dialog.py — HelpPPsct.update(self, dt)

"""Actualización periódica del visor de ayuda (mantenido por homogeneidad del ciclo).""" 

<a id="popup_dialog_py_helpppsct_handle_event"></a>

### Popup_Dialog.py — HelpPPsct.handle_event(self, event)

"""Gestiona eventos Pygame delegando en el HelpViewer embebido.""" 

<a id="popup_dialog_py_helpppsct_wants_keyboard"></a>

### Popup_Dialog.py — HelpPPsct.wants_keyboard(self)

"""Indica si la sección de ayuda desea recibir eventos de teclado.""" 

<a id="popup_dialog_py_helpppsct_wants_wheel"></a>

### Popup_Dialog.py — HelpPPsct.wants_wheel(self)

"""Indica si la sección de ayuda desea recibir eventos de rueda del ratón.""" 

<a id="popup_dialog_py_interactivecontent_init"></a>

### Popup_Dialog.py — InteractiveContent.__init__(self, *args, **kwargs)

"""Base opcional para contenidos embebidos en SurfacePPsct.""" 

<a id="popup_dialog_py_interactivecontent_on_mount"></a>

### Popup_Dialog.py — InteractiveContent.on_mount(self, rect)

"""Guarda rect absoluto y marca el contenido como montado.""" 

<a id="popup_dialog_py_interactivecontent_on_unmount"></a>

### Popup_Dialog.py — InteractiveContent.on_unmount(self)

"""Desmontaje: limpia flags y rect.""" 

## interactive_content.py — Clases

<a id="interactive_content_py_interactivecontent"></a>

### interactive_content.py — InteractiveContent

"""Interfaz mínima para contenidos interactivos/animados (definición de firmas).""" 

<a id="interactive_content_py_interactivecontent_on_mount"></a>

### interactive_content.py — InteractiveContent.on_mount(self, rect)

"""Se llama cuando el contenido se coloca dentro de la sección central.""" 

<a id="interactive_content_py_interactivecontent_on_unmount"></a>

### interactive_content.py — InteractiveContent.on_unmount(self)

"""Limpieza de recursos cuando se retira el contenido.""" 

<a id="interactive_content_py_interactivecontent_update"></a>

### interactive_content.py — InteractiveContent.update(self, dt_ms)

"""Actualización periódica (dt en milisegundos).""" 

<a id="interactive_content_py_interactivecontent_draw"></a>

### interactive_content.py — InteractiveContent.draw(self, surface, rect)

"""Dibuja dentro de 'rect' sobre 'surface'.""" 

<a id="interactive_content_py_interactivecontent_handle_event"></a>

### interactive_content.py — InteractiveContent.handle_event(self, event)

"""Gestiona un evento y devuelve True si lo consume.""" 

<a id="interactive_content_py_interactivecontent_wants_keyboard"></a>

### interactive_content.py — InteractiveContent.wants_keyboard(self)

"""Indica si desea eventos de teclado.""" 

<a id="interactive_content_py_interactivecontent_wants_wheel"></a>

### interactive_content.py — InteractiveContent.wants_wheel(self)

"""Indica si desea eventos de rueda del ratón.""" 

# Comentarios finales

- Depende de Pygame; la ejecución requiere un display inicializado (pygame.display).
- Usa estado global (sentencias 'global'); conviene inicializar el módulo con un método dedicado.
- Incluye salidas forzadas (sys.exit), lo que puede ser indeseable si se integra como librería.
- Carga estilos desde ficheros JSON con rutas relativas; la resolución de paths depende del cwd.
- El código contiene comentarios 'BUG' que indican comportamientos conocidos a revisar.
- Importaciones detectadas: pygame, sys, time, os, os.path, pygame_widgets, json, pygame_widgets.textbox.TextBox, help_core_pygame.help_core.HelpViewer, help_core_pygame.help_core.HelpConfig, pathlib.Path
- Variables declaradas como global: gameDisplay, Style_id, ST
- Contiene TODOs; hay funcionalidad prevista no implementada.

---

## adapters.py - Funciones y clases

<a id="adapters_py_helpasinteractive"></a>

### adapters.py - HelpAsInteractive

"""Envuelve un `HelpViewer` para usarlo como contenido interactivo embebible en `SurfacePPsct`.

Implementa la interfaz minima esperada por el router del popup:

- on_mount / on_unmount
- update
- draw
- handle_event
- wants_keyboard / wants_wheel
  """

<a id="adapters_py_helpasinteractive_on_mount"></a>

### adapters.py - HelpAsInteractive.on_mount(self, rect)

"""Recibe el rectangulo util del kernel (pygame.Rect) y lo comunica al visor si este soporta redimensionado."""

<a id="adapters_py_helpasinteractive_on_unmount"></a>

### adapters.py - HelpAsInteractive.on_unmount(self)

"""Hook de desmontaje (por defecto no libera recursos; se mantiene por contrato)."""

<a id="adapters_py_helpasinteractive_update"></a>

### adapters.py - HelpAsInteractive.update(self, dt)

"""Actualizacion periodica (dt en ms). Por defecto no hace nada; el visor es estatico."""

<a id="adapters_py_helpasinteractive_draw"></a>

### adapters.py - HelpAsInteractive.draw(self, surface, rect)

"""Dibuja el visor en el rectangulo indicado delegando en `HelpViewer.draw(surface, rect)`."""

<a id="adapters_py_helpasinteractive_handle_event"></a>

### adapters.py - HelpAsInteractive.handle_event(self, event)

"""Pasa eventos al visor (rueda/teclado/navegacion) y devuelve True si el visor los consume."""

<a id="adapters_py_helpasinteractive_wants_keyboard"></a>

### adapters.py - HelpAsInteractive.wants_keyboard(self)

"""Indica al router que este contenido desea eventos de teclado."""

<a id="adapters_py_helpasinteractive_wants_wheel"></a>

### adapters.py - HelpAsInteractive.wants_wheel(self)

"""Indica al router que este contenido desea eventos de rueda del raton."""

<a id="adapters_py_run_help_popup_from_md"></a>

### adapters.py - run_help_popup_from_md(md_text, *, title="Ayuda", interactive_size, ...)

"""Funcion de conveniencia: construye un `HelpViewer` a partir de Markdown, lo adapta como contenido interactivo
y lo muestra dentro de una `PopupDialogWindow`.

**Notas:**

- Debe llamarse tras `IniPopupDialog(...)`.
- Normaliza el flujo tipico: `HelpViewer` -> `HelpAsInteractive` -> `SurfacePPsct` -> `PopupDialogWindow.Run()`.
  """
