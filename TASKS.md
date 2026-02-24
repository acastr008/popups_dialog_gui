# Tareas pendientes

- Repaso general antes de subir a GitHub tal cual o Incluir Formularios

- No incluiremos formularios. (Es posible que ChessOC no necesite que los formularios estén integrados en Popups Windows)

- Añadir juegos y simulaciones a GitHub (Aterrizaje Lunar, Péndulos, etc.)

- Desatascar ChessOC.

# Mejoras pendientes a más largo plazo

- ???

# Tareas ya realizadas por orden cronológico

- (24-feg-2026) Texto añadido en OVERVIEW_e(s/n).md mejoras en tools/diagnose_up2_pypi.py

- (20-feb-2026) Más correcciones de documentos (incluidos los README): se hacen más traducciones y corrigen enlaces entre ellos. 

- (19-feb-2026) Se han añadido traduciones de /docs/*_es.md a la version inglesa. EL /README_es.md no enlaza bien con el /docs/INDEX_es.md

- (17-feb-2026) Revisadas todas las demos, y retocadas las cabeceras y titulos de ventana pygame.

- (16-feb-2026) Conseguimos subirlo a GitHup. Hubp que modificar pyproject.toml, .gitignore, y crear entorno virtual pyenv_popup_gui.

- (15-feb-2026) Retomamos el desarrollo: demo_showhelpoverlay_directo.py, demo_popuphelp_embebido.py, HELP_API_LEVELS_es.md

- (24-ene-2026) Se consiguió dotar al proyecto de una lista plana de ficheros ttf con fuentes libres de derechos. Si incluyó documentacion al respecto, y algunas herranientas.

- (21-ene-2026) Primera versión de TUTORIAL.md (faltan las imagenes)

- (19-ene-2026 10:24) Se actualizan las APIS (PENDIENTES DE BACKUPS)

- (19-ene-2026 8:30) Tras muchos cambios en varios módulos se logró hacer funcionar todas las demos.
  
  - Tras mover adapters.py al paquete popups_dialog_gui y extraer el visor de ayuda a help_core_pygame (renombrando/retirando el antiguo helpview), varias demos dejaron de funcionar por rutas de import obsoletas y por cambios de API entre el visor antiguo y el nuevo.
  
  - Cambios clave realizados
    
    - Actualización de imports en Popup_Dialog.py: se eliminó la dependencia rígida de helpview.* y se adaptó la carga del visor para trabajar con el paquete nuevo (help_core_pygame) manteniendo compatibilidad razonable.
    
    - Reconstrucción correcta de HelpPPsct: se restauró el “contrato” que exige PopupDialogWindow (métodos como GetWidthHeigthMessage, Draw, manejo de eventos) y se corrigieron errores estructurales que impedían que esos métodos existieran realmente en la clase.
    
    - Adaptación al API real de help_core_pygame: se corrigió la creación del visor para usar el patrón HelpConfig → HelpViewer(cfg) (en vez de pasar markdown/kwargs como antes), evitando la cascada de TypeError por argumentos no soportados y el error de cfg mal tipado.
    
    - Ajuste de SurfacePPsct para no romper demos previas: se relajó la validación del tamaño interno en el caso de surface estática (permitiendo inner_rect mayor y centrado), manteniendo la prohibición de redimensionado para contenido interactivo donde sí es crítico.
  
  - Resultado conseguido: Se pasó de un estado donde varias demos fallaban por incompatibilidades de empaquetado/importación y por divergencia de API, a un estado donde el sistema vuelve a ser coherente: el “core” de popups funciona con help_core_pygame, los adaptadores están en su paquete correcto, y las demos vuelven a ejecutarse todas correctamente, incluyendo las que dependen de ayuda embebida y las que usan superficies con tamaños variables.

- (18-ene-2026) Corregir fallos que afectaban a la demo 'demo_Popup_Dialog.py'
  
  - El problema surgió tras migrar a asset_locator.py, en demo_Popup_Dialog.py dejó de existir la variable PathFonts, y al construir el texto del menú (donde se mostraba {PathFonts}) se produjo un NameError.
  
  - La solución fue obtener PathFonts desde resolve_asset_layout().fonts_dir (path absoluto) para usarlo en PopupScanFiles(dir=PathFonts, ...), y crear aparte una versión abreviada del path solo para mostrar en pantalla (elipsis descentrada, conservando más parte derecha) para que no desborde el tamaño de la tantalla de la demo.

- (17-ene-2026) Corregir Lanzador main.py. Realizar una demo muy simple.  Corregir los assets y el programa popuos_dialogs_gui.py. 
  Se probaron los cambios hasta hacerlos funcionar. Se han ralizado un montón de pequeños cambios.
  
  - [ ] **Definir convención canónica de rutas de assets**
    
    - Fuentes: `src/popups_dialog_gui/assets/fonts/*.ttf`
    - Estilos: `src/popups_dialog_gui/assets/styles/*.json`
    - Regla: en JSON, las fuentes se referencian únicamente por **nombre de fichero** (p.ej. `Yrsa-Medium.ttf`), sin prefijos ni rutas.
  
  - [ ] **Eliminar `Path_Fonts` del JSON**
    
    - Borrar `"Path_Fonts": "Fonts/"` en todos los estilos (p.ej. `playful_childlike`, `formal`). :contentReference[oaicite:1]{index=1}
    - Añadir una nota en el JSON (o en documentación) indicando que ya no existe prefijo global.
  
  - [ ] **Normalizar todas las claves de fuente del JSON**
    
    - Sustituir valores con prefijo `Fonts/` por solo el nombre:
      - `hlp_Font: "Fonts/Yrsa-Medium.ttf"` → `hlp_Font: "Yrsa-Medium.ttf"` :contentReference[oaicite:2]{index=2}
      - `hlp_FontBold: "Fonts/Verdana_Bold_Italic.ttf"` → `Verdana_Bold_Italic.ttf` :contentReference[oaicite:3]{index=3}
      - `hlp_CodeFont: "Fonts/Consolas.ttf"` → `Consolas.ttf` :contentReference[oaicite:4]{index=4}
    - Revisar también `Tit_FontType`, `Krn_FontType`, `Lbt_FontType` para asegurar que no contienen rutas (en `playful_childlike` y `formal`). :contentReference[oaicite:5]{index=5}
  
  - [ ] **Alinear el set de fuentes reales con lo que piden los estilos**
    
    - Inventariar `assets/fonts/` y verificar que existen las fuentes referenciadas:
      - `Impact.ttf`, `ariali.ttf`, `Verdana.ttf`, `Verdana_Bold_Italic.ttf`, `Consolas.ttf`, `Yrsa-Medium.ttf`, `arialbd.ttf`, etc. :contentReference[oaicite:6]{index=6}
    - Decidir estrategia:
      - (A) Incorporar esos `.ttf` al repositorio en `assets/fonts/`, o
      - (B) Modificar el JSON para usar únicamente fuentes existentes (p.ej. sustituir Impact/Verdana/Consolas por las disponibles).
  
  - [ ] **Actualizar `GetFont()` (ruptura total de compatibilidad)**
    
    - Resolver siempre la ruta como: `<paquete>/assets/fonts/<FontType>`
    - Prohibir rutas en `FontType` (si contiene `/` o `\`, error explícito).
    - Eliminar cualquier uso de `Path_Fonts` y cualquier concatenación basada en prefijos.
  
  - [ ] **Actualizar `IniPopupDialog()` para cargar estilos sin depender del CWD**
    
    - Resolver `assets/styles/` con `Path(__file__).resolve().parent / "assets" / "styles"`.
    - Cargar/mezclar JSON de estilos (p.ej. `popup_gui.json`, `helpview.json`).
    - Mantener validación temprana de claves mínimas necesarias (p.ej. `SetFlagAlert`) para fallar con mensaje claro.
  
  - [ ] **Eliminar restos de compatibilidad previa**
    
    - Buscar y eliminar:
      - Lecturas/uso de `Path_Fonts` en cualquier módulo.
      - Hardcodes tipo `"styles/..."`, `"../../../styles/..."`, o `Fonts/...` en el código.
    - Revisar impresiones/warnings heredados que sugieren rutas antiguas.
  
  - [ ] **Pruebas de regresión**
    
    - Ejecutar `./main.py` en modo “sin cambiar cwd” y verificar:
      - Carga correcta de JSON desde `assets/styles`.
      - Carga correcta de fuentes desde `assets/fonts`.
      - Ausencia de rutas duplicadas (`Fonts/Fonts/...`) y de `FileNotFoundError` por fuentes inexistentes.
      - Funcionamiento correcto de los estilos `playful_childlike` y `formal`.

- (16-ene-2026) Lograda versiones bastante completas de API_REFERENCE_es.md y API_REFERENCE_en.md

- (14-ene-2026) Revision API_REFERENCE_es.md

- (12-ene-2026) 

- (11-ene-2026) Se ha creado una plantilla y vamos a ir trasladando los contenidos en ella para ir reorganizando todo el proyecto
