#!/home/antonio/pyenv_goliat/bin/python
# -*- coding: utf-8 -*-

"""
Versión (18-ene-2026) 

Popup_Dialog_Py.py es un módulo de ventanas emergentes (pop-up) usando pygame para generar avisos, diálogos, etc. 
y está basada en Pygame. Si se invoca directamen se ejecutará la demo del módulo.
Funciones: IniPopupDialog(), PopupERR(), PopupWARN(), PopupNOTICE(), PopupINFO(), PopupASK(), PopupSelectionFiles(), etc.

La versión anterior Popup_Dialog.py en estaba en en lo proyecto TortuLogan de 26-Dic-2023 Incluye el uso de la
variable global VG_gameDisplay que ya no se usa ahora se pasa gameDisplay por parámetro a las clases.

No se trata de emular un TkInter, o un GTK, ni nada parecido. Sí que se intenta ofrecer funcionalidades muy básicas
tipo graphical user interface (GUI) usando PyGame, porque no siempre los GUI avanzados combinan bien con otros
entornos gráficos con sus propios gestores de eventos.

Funciones públicas disponibles:
    PopupERR(), PopupWARN(), PopupNOTICE(), PopupINFO():
        Son PopupDialogWindow y son similares para. Se usan para distinto tipo de nivel de alerta.
        Tras mostrar la información permiten salir cerrando la ventana pulsando un botón.

    PopupASK():
        También es una PopupDialogWindow, similar a las anteriores y requiere una lista de identificadores para 
        poder ofrecer varios botones con una total libertad de usos. Esto se presta a hacer uso de este tipo de 
        ventanas no solo para las preguntas típicas de 'Confirmar', 'Cancelar', 'Reintentar', sino para cualquier 
        otro tipo de preguntas, lo que da pie a usarla para funcionalidades muy diversas. Un ejemplo inmediato es 
        la funcionalidad de menú tal y como puede verse en la Demo.

    PopupSelectionFiles():
        Basándonos en la PopupASK() que acabamos de describir, se ha implementado un procedimiento que permite 
        seleccionar ficheros de un directorio. Se puede obligar a que solo considere los ficheros que tengan una 
        determinada extensión. El diseño es muy sencillo, pero pese a ello admite que los nombre de los ficheros 
        puedan ser muy largos y que el número de los ficheros contenidos en el directorio sean muy numerosos ya que
        para seleccionar alguno de ellos nos permitirá ir mostrando los nombres de ficheros paginando la información. 

Caraterísticas generales de las ventanas:
    Estas ventanas emergente tienen tres secciones dispuestas verticalmente y hacen uso de la clase PopupDialogWindow()
    La sección superior para el título o para indicar el tipo de mensaje, la siguiente es una sección que dará cabida
    al texto del mensaje y finalmente una inferior con uno o más botones.
 
    Esta ventana emergente se dimensionará para dar cabida a los textos con las fuentes indicadas en cada sección.
    Usamos ventanas emergentes Modales. Es decir, bloquearán la interacción con el resto de la aplicación hasta que 
    se cierre la ventana emergente.

    La estética por defecto con fuentes grandecitas y colores llamativos está orientada a juegos infantiles pygame. 
    Al usar una estructura de objetos se podría modificar sin excesivo esfuerzo a varios niveles.
"""



"""
ESTRUCTURA DEL MODULO 
=====================
El método Draw común en varias clases tiene diferentes cometidos. Una vez se obtiene el dibujo de una parte se
dispondran convenientemente para dibujar todas ellas en la clase de nivel superior.

class PopupDialogWindow:
    class PopupSection: ((agregación))
        -.Draw(self):  # definicion del método abstracto Draw() para PopupSection
        class TitlePPsct(PopupSection):
            -.Draw(self, x, y, Wide, Heigth, BorderRadius): # Implementacion particular de Draw() para Title
                Dibuja el rectángulo de la sección y encima el texto
                Debe venir precedida de los cálculos de las dimensiones de las tres secciones
        class MessagePPsct(PopupSection):
            -.Draw(self, x, y, Wide, Heigth, BorderRadius, PorcSepLines=130): ## Implementacion particular para MessagePPsct
                GetWidthHeigthText() hizo el trabajo previo para calcular el espacio necesario para representar 
                todo el texto con la fuente y el tamaño de fuente indicado.
        class ListButtonsPPsct(PopupSection):
            -.Draw(self, x, y, Wide, Heigth, BorderRadius): ## Implementacion particular de Draw() para ListButtonsPPsct
                Primero averigua anchura y altura de la secció con self.GetWidthHeigthContent() 
                Luego dibuja el rectángulo de la sección en la pantalla y luuego hace lo propio con cada botón             

Para evitarnos tener que pasar continuamente como parámetro a un montón de funciones la ventana principal de pygame
que tiene qu venir ya inicializada. Usaremos una variable global 'gameDisplay' que debe ser inicilizada antes de usar 
este módulo.

"""

import pygame
import sys, time
#import Tracer
import os, os.path
from pathlib import Path
import pygame_widgets
import json
from pygame_widgets.textbox import TextBox # Dependencia externa indeseable.
from popups_dialog_gui.asset_locator import load_style_bundle, resolve_font_path
from help_core_pygame import HelpViewer

# ST={}
ST: dict | None = None


#########################################################################
def GetFont(FontType, FontSize):
    """
    Carga una fuente TrueType desde assets/fonts.

    Reglas (sin compatibilidad hacia atrás):
      - FontType debe ser un nombre de fichero, p.ej. 'Arimo-Bold.ttf'
      - La fuente debe existir en: <paquete>/assets/fonts/

    Parameters
    ----------
    FontType:
        Nombre del fichero de fuente (sin rutas).
    FontSize:
        Tamaño de fuente.

    Returns
    -------
    pygame.font.Font
        Objeto de fuente listo para usar.
    """
    from pathlib import Path
    import pygame

    # Nota: estas globals se establecen en IniPopupDialog()
    fonts_dir = globals().get("POPUP_FONTS_DIR")

    if fonts_dir is None:
        # Si alguien llama GetFont antes de IniPopupDialog, fallamos con claridad.
        raise RuntimeError(
            "GetFont() fue llamado antes de IniPopupDialog(). "
            "Inicializa primero IniPopupDialog(Display, Style_ID)."
        )

    if "/" in str(FontType) or "\\" in str(FontType):
        raise ValueError(
            f"FontType ({str(FontType)}) debe ser un nombre de fichero, no una ruta. "
            "Ejemplo valido: 'Arimo-Bold.ttf'"
        )

    font_path = Path(fonts_dir) / FontType
    if not font_path.exists():
        raise FileNotFoundError(
            "No existe el fichero de fuente esperado:\n"
            f"  {font_path}\n"
            "Solución: copia la fuente a assets/fonts o ajusta el JSON para usar una fuente existente."
        )

    return pygame.font.Font(str(font_path), FontSize)


#########################################################################
def IniPopupDialog(Display=None, Style_ID=None):
    """
    Inicializa el sistema de popups y carga el estilo solicitado.

    Decisiones de diseño (sin compatibilidad hacia atrás):
      - Los assets viven *siempre* dentro del paquete:
            <paquete>/assets/styles/*.json
            <paquete>/assets/fonts/*.ttf
      - Los JSON de estilo deben referenciar fuentes por *nombre de fichero*,
        por ejemplo: "Arimo-Bold.ttf" (no "fonts/Arimo-Bold.ttf", no rutas relativas).
      - No se usan rutas relativas al CWD ni variables de entorno.

    Parameters
    ----------
    Display:
        Surface o display principal donde se renderizarán los popups.
    Style_ID:
        Identificador del estilo (p.ej. 'playful_childlike', 'formal').

    Raises
    ------
    ValueError:
        Si Style_ID es None o vacío.
    FileNotFoundError:
        Si no existe la carpeta assets/styles o no hay JSON cargables.
    KeyError:
        Si el estilo no existe o faltan claves obligatorias.
    TypeError:
        Si los JSON no tienen el formato esperado.
    """
    global gameDisplay, Style_id, ST
    global POPUP_ASSETS_DIR, POPUP_STYLES_DIR, POPUP_FONTS_DIR

    import json
    from pathlib import Path

    gameDisplay = Display
    Style_id = Style_ID

    if not Style_ID:
        raise ValueError("Style_ID no puede ser None o vacío.")

    # Layout canónico: assets junto al módulo (paquete)
    package_dir = Path(__file__).resolve().parent
    POPUP_ASSETS_DIR = package_dir / "assets"
    POPUP_STYLES_DIR = POPUP_ASSETS_DIR / "styles"
    POPUP_FONTS_DIR = POPUP_ASSETS_DIR / "fonts"

    if not POPUP_STYLES_DIR.is_dir():
        raise FileNotFoundError(
            "No existe la carpeta de estilos esperada:\n"
            f"  {POPUP_STYLES_DIR}\n"
            "Crea 'assets/styles' dentro del paquete o ajusta la estructura del proyecto."
        )

    # Si 'formulario.json' ya no forma parte del proyecto, no lo listamos.
    # Añádelo solo si realmente existe y lo necesitas.
    json_files = [
        POPUP_STYLES_DIR / "popup_gui.json",
        POPUP_STYLES_DIR / "helpview.json",
        # POPUP_STYLES_DIR / "formulario.json",
    ]

    loaded_any = False
    available_styles: set[str] = set()
    style_data: dict = {}

    for path in json_files:
        if not path.exists():
            print(f"**Warning**: No se encontró '{path}'")
            continue

        loaded_any = True
        with path.open(encoding="utf-8") as file_handle:
            styles_map = json.load(file_handle)

        if not isinstance(styles_map, dict):
            raise TypeError(f"El JSON '{path}' no contiene un objeto raíz (dict).")

        available_styles.update(styles_map.keys())

        if Style_ID in styles_map:
            section = styles_map[Style_ID]
            if not isinstance(section, dict):
                raise TypeError(
                    f"El estilo '{Style_ID}' en '{path.name}' no es un objeto (dict)."
                )
            style_data |= section

    if not loaded_any:
        raise FileNotFoundError(
            "No se pudo cargar ningún JSON de estilos. Revisa:\n"
            f"  {POPUP_STYLES_DIR}"
        )

    if Style_ID not in available_styles:
        raise KeyError(
            f"El estilo '{Style_ID}' no existe. Disponibles: {sorted(available_styles)}"
        )

    # Valida lo mínimo que sabes que vas a usar después, para fallar pronto y bien.
    required_keys = ["SetFlagAlert"]
    missing = [k for k in required_keys if k not in style_data]
    if missing:
        raise KeyError(
            "El estilo cargado no contiene claves obligatorias "
            f"{missing}. Claves disponibles: {sorted(style_data.keys())}"
        )

    ST = style_data


############################################################(15-sept-2025)
def get_style() -> dict:
    """
    Devuelve una **referencia** al diccionario de estilo activo (ST).

    - ST se inicializa dentro de IniPopupDialog(Display, Style_ID).
    - Lo que se obtiene aquí es el propio dict vivo que usa el sistema de popups:
      leerlo permite inspeccionar tamaños, colores, márgenes, etc.
      Modificarlo directamente **no es recomendable**; usa set_style_overrides().
    - Si se llama antes de IniPopupDialog, se lanza un error.
    """
    if ST is None:
        raise RuntimeError("IniPopupDialog() no ha inicializado ST todavía.")
    return ST


############################################################(15-sept-2025)
def _deep_update(dst: dict, src: dict) -> None:
    """Fusión recursiva dict→dict: actualiza claves y, si ambos valores son dict, baja un nivel."""
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            _deep_update(dst[k], v)
        else:
            dst[k] = v


############################################################(15-sept-2025)
def set_style_overrides(overrides: dict) -> None:
    """
    Aplica **overrides** (merge profundo) sobre el estilo activo (ST).

    Uso recomendado: llamar **inmediatamente después** de IniPopupDialog() y
    **antes** de construir SurfacePPsct/PopupDialogWindow, para que las nuevas
    métricas (padding, bordes, márgenes, etc.) se tengan en cuenta al medir
    y maquetar las secciones.

    Ejemplo:
        IniPopupDialog(screen, "playful_childlike")
        set_style_overrides({
            "Kernel": {"Padding": 0, "Border": 0},
            "Section_Margins": {"Top": 0, "Right": 0, "Bottom": 0, "Left": 0},
        })
        popup = PopupDialogWindow(...)

    Si se llama antes de IniPopupDialog(), se lanza un error.
    """
    if ST is None:
        raise RuntimeError("IniPopupDialog() no ha inicializado ST todavía.")
    _deep_update(ST, overrides)



#####################################
def GetStyleDict():
    global ST

    return ST 


#####################################
def TestIni():
    global gameDisplay,Style_id

    if  not Style_id in ["playful_childlike", "formal"]:
        raise ValueError (f"ERROR: Unavailable value of Style_id={Style_id}") 
    try:
        gameDisplay.get_size()
    except Exception as e:
        print(f"""
ERROR: {e}
Módulo 'Popup_Dialog_Pygame' no nicializado.
Antes de usarlo debe inicializarlo usando:
IniPopupDialog(display_surface)""")
        raise # Provoca la excepción del tipo Exception para facilitar la localizacion del fallo
        

#############################################
# Base mínima para contenidos interactivos  #
#############################################
class InteractiveContent:
    """
    Base opcional para contenidos embebidos en SurfacePPsct.
    Responsabilidad ÚNICA del montaje:
      - Guardar el rect absoluto (posición y tamaño definitivos)
      - Marcar estado de montaje.
    No realiza siembras ni inicializaciones lógicas; eso va en __init__ del contenido.
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.mounted = False
        self.rect_abs = None  # pygame.Rect del área útil ABSOLUTA

    def on_mount(self, rect):
        """Guardar rect absoluto y marcar como montado."""
        try:
            self.rect_abs = rect.copy() if hasattr(rect, "copy") else rect
        except Exception:
            self.rect_abs = rect
        self.mounted = True
        # Hook opcional para descendientes: did_mount()
        hook = getattr(self, "did_mount", None)
        if callable(hook):
            hook()

    def on_unmount(self):
        """Desmontaje opcional. Limpia flags y rect. Hook: did_unmount()."""
        self.mounted = False
        self.rect_abs = None
        hook = getattr(self, "did_unmount", None)
        if callable(hook):
            hook()

####################################################################################################################
# Esta es la superclase principal de este módulo. PopupDialogWindow muestra una ventana emergente de diálogo con 
# tres partes (llamadas secciones): Titulo, Nucleo (Kernel) y Lista de botones.
# Lo primero que hacemos justo antes de dibujar la ventana emergente es sacar una copia de la pantalla de Pygame. 
# Tras pulsar un botón de la ventana de diálogo, lo último que hacemos es borrar la ventana
# emergente y recuperar el contenido de la ventana de Pygame para tapar el hueco y en su caso retornar información
# del botón pulsado.
####################################################################################################################
class PopupDialogWindow:
    """
    La idea de PopupDialogWindow es diseñar un objeto para simplificar al máximo la creacion de procedimientos 
    de Notificación de Errores, notificación de avisos varios, abrir dialogos de diverso tipo: para Confirmar, 
    Denegar, Cancelar, Reintentar, etc.

    Un Objeto tipo PopupDialogWindow constará de tres partes (secciones) que son: Título, Mensaje, y la parte de 
    Botones.

    Para ello usarmos unos niveles de alerta que se traducirán en un color para el título de la ventana.
    El resto de colores se conformarán de forma preestablecida y las fuentes de los textos también.

    El tamaño de la ventana PopupDialog (por llamarlo de alguna forma), no se podrá conocer hasta que tengamos el
    tamaño de las tres secciones que acabamos de referir y que deberían visualizarse con el mismo ancho, ajustado a 
    la anchura de la seccion más ancha de las tres, y hasta que no tengamos las alturas de las tres secciones no 
    podremos obtener la altura total de la ventana PopupDialog, que será la suma de las alturas de sus tres secciones.

    Por lo tanto, las secciones vendrán cada una con su anchura y altura, pero antes de ser visualizadas deberemos
    ajustar su tamaño para que todas las secciones se visualicen con la misma anchura y respetando los márgenes 
    establecidos. Para ello habrá que:
        1) Consultar las dimensiones de cada sección con sus respectivos márgenes.
        2) Ajustar las anchuras de las dos secciones más estrechas, al valor de la mayor anchura de las tres.
        3) Dibujar las tres secciones una debajo de otra y centradas dentro de la PopupDialogWindow que será
            una zona rectangular ligeramente más grande que la suma de las tres secciones porque le damos un pequeño 
            margen.
        4) Establecer un bucle de eventos donde detectamos con el método Run() cualquier click de ratón en 
            alguno de los botones de la PopupDialogWindow que finalizará cerándose y en su caso retornará el Id
            del botón pulsado cuando se ofrezca más de un botón.
    """
    ############################################### (Constructor ) ###########################################
    def __init__(self, KernelContent, ListIdButt, Title="Aviso", FlagAlert="Green", PosCenter=None): 
        """
        Title (str): 
            Cadena caracteres sin retorno de linea para el título
        KernelContent:
            Message: Cadena de caracteres con una o más lineas para el mensaje.
            FormContent: Contenido de un formulario. Será una lista de FormElement.
                Un FormElemente Puede ser varias cosas:
                    Una Label, un InputField, un TextArea, una lista [ Label, InputField ]. 
        ListIdButt: Lista con cadenas de caracteres para los botones.
        FlagAlert: Nivel de alerta ("Green"/"Yellow"/"Orange"/"Red"/"Blue")
        PosCenter: Posición (x,y) donde situaremos el centro de la PopupDialogWindow
        """
        # Verificar que hemos recibido una copia de la ventana principal en la inicializacion.
        TestIni()
        # Verificamos que venga una lista de identificadores de botones del tipo adecuado
        # Ojo el orden evaluación condicional es importante para evitar errores de ejecución

        # Para que los textos no salgan pegados al márgen superior, lo más práctico es que empiecen con un retorno de
        # carro. Si ya viene con un retorno de carro inicial se asume que se puso así por legibilidad en el código
        # python cuando se usa triples comillas, y no es necesario añadir nada.
        self.KernelContent=KernelContent
        if isinstance(self.KernelContent, str): # Si el tipo de contenido del núcleo es una cadena (string)
            if self.KernelContent[0] != "\n":
                self.KernelContent = "\n" + self.KernelContent

        self.Title=Title
        self.ListIdButt=ListIdButt
        self.FlagAlert=FlagAlert
        if ListIdButt==None or not isinstance(ListIdButt, list) or len(ListIdButt)==0:
            print("ERROR: Falta una lista de identificadores de botones para la PopupDialogWindow", file=sys.stderr)
            sys.exit()
        for idBut in ListIdButt:
            if not isinstance(idBut, str):
                print("ERROR: La lista de identificadores de botones contiene un elemento extraño", idBut, \
                    file=sys.stderr)        
        
        self.DisplayCopy=pygame.display.get_surface().copy() # Sacar una copia del contenido de toda la gameDisplay
        if PosCenter==None:
            self.PosCenter=gameDisplay.get_rect().center 
        self.X_Center, self.Y_Center= self.PosCenter

        self._load_style()

        # ===(Cálculo de dimensiones de la PopupDialogWindow en funcion de las dimensiones de las tres secciones) ===
        # --- Cabecera (Titulo) --- # 
        W_Tit, self.H_Tit= self.TitleSect.GetWidthHeigthTitle()
        # --- (Zona media) ---
        W_Kernel_Sect, self.H_Kernel_Sect= self.KernelSect.GetWidthHeigthMessage()
        # --- Pie (Zona de botones) --- #
        # W_But, self.H_But = (150, 60)
        W_But, self.H_But= self.ListButSect.GetWidthHeigthContent()

        # === Obtener maximos y mínimos de altura y anchura de las tres secciones === #
        self.MaxW= max(W_Tit,W_Kernel_Sect,W_But) # Ancho máximo de las secciones
        self.MinW= min(W_Tit,W_Kernel_Sect,W_But) # Ancho mínimo de las secciones
        self.TotH= self.H_Tit + self.H_Kernel_Sect +self.H_But # Altura total de las secciones
        self.MinH= min(self.H_Tit,self.H_Kernel_Sect,self.H_But) # Altura mínima de las secciones
        self.BorderSectRadius= self.MinH//4 # Radio del redondeo de esquinas de las secciones
        self.BorderRadius=self.BorderSectRadius+self.WinMargin # Radio del redondeo de esquinas de la PopupDialogWindow
        self.W= self.MaxW + 2*self.WinMargin                           # Ancho de la PopupDialogWindow
        self.H= self.H_Tit+self.H_Kernel_Sect+self.H_But+(2*self.WinMargin)    # Altura de la PopupDialogWindow
        self.X= self.X_Center-(self.MaxW//2)                        # Posición X de la PopupDialogWindow
        self.Y= self.Y_Center-(self.TotH//2)                        # Posicion Y de la PopupDialogWindow
        self.Rect=pygame.Rect(self.X, self.Y, self.W, self.H)       # Rectángulo de la PopupDialogWindow

        # Guardar rects absolutos de secciones (para re-dibujo eficiente del kernel a 30 FPS)
        self._origY = self.Y
        self._title_rect = pygame.Rect(
            self.X + self.WinMargin,
            self.Y + self.WinMargin,
            self.MaxW,
            self.H_Tit
        )
        self._kernel_rect = pygame.Rect(
            self.X + self.WinMargin,
            self.Y + self.WinMargin + self.H_Tit,
            self.MaxW,
            self.H_Kernel_Sect
        )
        self._buttons_rect = pygame.Rect(
            self.X + self.WinMargin,
            self.Y + self.WinMargin + self.H_Tit + self.H_Kernel_Sect,
            self.MaxW,
            self.H_But
        )

        # ===(Terminamos dibujando toda la PopupDialogWindow y dejamos todo listo) === #
        self.Draw()
        self._paused = False     # Estado de pausa desactivado (sin congelación del kernel en contenidos interactivos)
        pygame.display.update()  # display.update() (sin argumentos) actualiza el contenido de toda la pantalla
        
    ##############################################################################################################
    def _load_style(self):
        """
        Carga una larga lista de atributos para definir el estilo visual del funcionamiento de este módulo 
        Style_id debe proporcionarse al inicializar el módulo con IniPopupDialog().
        Los colores del tipo de ventana en funcion del nivel de alerta son: 
            "Green"     Informacion 
            "Yellow"    Aviso
            "Orange"    Advertencia
            "Red"       Error crítico
            "Blue"      Pregunta
            """
        global ST

        self.SetFlagAlert = {k: tuple(v) for k, v in ST["SetFlagAlert"].items()}
        self.ColorAlert = self.SetFlagAlert[self.FlagAlert]
        
        # - - - - - - -(Atributos generales comunes de las tres secciones) - - - - - - - - - - - - - - - - - - - - - - -
        self.WinMargin=ST["SF_WinMargin"]                   # Espacio libre entre las secciones y el borde de la 
                                                            # PopupDialogWindow
        self.WinBorderThikness=ST["SF_WinBorderThikness"]   # Grosor del borde de la PopupDialogWindow
        self.WinBgColor=ST["SF_WinBgColor"]                 # Color para el fondo de la PopupDialogWindow
        self.WinBorderColor=ST["SF_WinBorderColor"]         # Color del borde de la PopupDialogWindow negro
        self.SectFgColor=ST["SF_SectFgColor"]               # El color de los textos en las secciones será el mismo 
        self.SectBgColor=ST["SF_SectBgColor"]                  # Color de fondo para los textos
        self.SectBgButColor=ST["SF_SectBgButColor"]            # Color para el fondo de los botones
        self.SectBorderColor=ST["SF_SectBorderColor"]          # Color de los bordes de las tres secciones
        self.SectBorderThikness=ST["SF_SectBorderThikness"]    # Grosor de los bordes de las tres secciones en pixels
        self.SectW_Margin=ST["SF_SectW_Margin"]                # Margen a lo ancho
        self.SectH_Margin=ST["SF_SectH_Margin"]                # Margen a lo alto

        # - - - - - (Parametros específicos para la sección Title) - - - - - - - - - - - - - - - - - - - - - - - - - - -
        Tit_FontType=ST["Tit_FontType"]                 # Fuente para el título        
        Tit_FontSize=ST["Tit_FontSize"]                 # Tamaño de la fuente para el título
        Tit_ColorFg=ST["Tit_ColorFg"]                   # color de fondo para el título                         
        Tit_BorderThikness=ST["Tit_BorderThikness"]     # Grosor del borde para el título
        Tit_BorderColor=ST["Tit_BorderColor"]           # Color del borde para el título
        Tit_ColorBg=self.ColorAlert                     # Color de fondo  para el título, igual al color de alerta

        # - - (Parametros específicos para la sección contenido del núcleo ) - - - - - - - - - - - - - - - - - - - - - - 
        Krn_FontType=ST["Krn_FontType"]                 # Fuente para el contenido del núcleo
        Krn_FontSize=ST["Krn_FontSize"]                 # Tamaño de la fuente para el contenido del núcleo 
        Krn_ColorFg=ST["Krn_ColorFg"]                   # Color del contenido para el contenido del núcleo   
        Krn_ColorBg=ST["Krn_ColorBg"]                   # Color del fondo para el contenido del núcleo
        Krn_BorderThikness=ST["Krn_BorderThikness"]     # Grosor del borde para el contenido del núcleo
        Krn_BorderColor=ST["Krn_BorderColor"]           # Color del borde para el contenido del núcleo
        Krn_TypeContent=type(self.KernelContent)        # Tipo de contenido del nucleo 

        # - - (Parametros específicos para la sección ListBut )  - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        Lbt_FontType=ST["Lbt_FontType"]                 # Fuente para ListBut      
        Lbt_FontSize=ST["Lbt_FontSize"]                 # Tamaño de la fuente para ListBut 
        Lbt_ColorFg=ST["Lbt_ColorFg"]                   # Color de fondo para ListBut
        Lbt_BorderThikness=ST["Lbt_BorderThikness"]     # Grosor del borde para ListBut
        Lbt_BorderColor=ST["Lbt_BorderColor"]           # Color del borde para ListBut
        Lbt_ColorBgBut=ST["Lbt_ColorBgBut"]             # Color del fondo de los botones para ListBut
        Lbt_ColorBg=self.ColorAlert             # Color de fondo  para la sección ListBut, igual al color de alerta
        Lbt_ButtPadding=Lbt_FontSize            # Separacion entre botones igual al tamaño (en altura altura) de la 
                                                # fuente en pixels 

        #----------------(Instanciar secciones: (Título, KernelContent y Botones) -------------------------------
        self.TitleSect=TitlePPsct(self.SectW_Margin, self.SectH_Margin, Tit_FontType, Tit_FontSize, \
            Tit_ColorFg, Tit_ColorBg, Tit_BorderThikness, Tit_BorderColor, TxtTitle=self.Title)

        # Selección de la sección del kernel:
        # - Si ya nos pasan una sección preparada (SurfacePPsct o HelpPPsct), la usamos tal cual.
        # - Si nos pasan una pygame.Surface, la envolvemos en SurfacePPsct (modo estático).
        # - En cualquier otro caso, asumimos texto (MessagePPsct).
        if isinstance(self.KernelContent, (SurfacePPsct, HelpPPsct)):
            # Ya viene una sección preparada (respetamos sus márgenes y borde)
            self.KernelSect = self.KernelContent
        elif isinstance(self.KernelContent, pygame.Surface):
            # Envolver automáticamente un pygame.Surface con márgenes y borde del estilo
            self.KernelSect = SurfacePPsct(
                self.KernelContent,
                self.SectW_Margin,
                self.SectH_Margin,
                Krn_BorderThikness,
                Krn_BorderColor)
        else:
            # Caso texto (comportamiento existente)
            self.KernelSect = MessagePPsct(
                self.SectW_Margin, self.SectH_Margin, Krn_FontType, Krn_FontSize,
                Krn_ColorFg, Krn_ColorBg, Krn_BorderThikness, Krn_BorderColor,
                Message=self.KernelContent, PorcSepLines=130)

        self.ListButSect=ListButtonsPPsct(self.SectW_Margin, self.SectH_Margin, Lbt_FontType, Lbt_FontSize, \
            Lbt_ColorFg, Lbt_ColorBg, Lbt_BorderThikness, Lbt_BorderColor, ListIdButt=self.ListIdButt, \
            ButtPadding=Lbt_ButtPadding, ColorBgBut=Lbt_ColorBgBut)


    ##############################################################################################################
    def Draw(self): ## Dibujar toda la PopupDialogWindow con su contenido
        # - - - - - - - - - (Dibujar un marco general para toda la PopupDialogWindow) - - - - - - - - - -
        DrawRect(self.WinBgColor, self.WinBorderColor, self.Rect, self.WinBorderThikness, self.BorderRadius)
        BorderColor, BorderThikness, BorderRadius = self.WinBorderColor, self.WinBorderThikness, self.BorderRadius
        # - - - - - - - - (Dibujamos las tres secciones) - - - - - - - - - - - - - -  
        # 1) Title
        self.TitleSect.Draw(self.X+self.WinMargin, self.Y+self.WinMargin, self.MaxW, self.H_Tit, self.BorderSectRadius)
        # 2) Message
        self.Y += self.H_Tit 
        self.KernelSect.Draw(self.X+self.WinMargin, self.Y+self.WinMargin, self.MaxW, self.H_Kernel_Sect, self.BorderSectRadius)
        # 3) ListBut
        self.Y += self.H_Kernel_Sect 
        self.ListButSect.Draw(self.X+self.WinMargin, self.Y+self.WinMargin, self.MaxW, self.H_But, self.BorderSectRadius)
        self.Y += self.H_But

    ##################################################################
    # Paso único no bloqueante: enrutar eventos → actualizar → dibujar.
    # Devuelve None si no hay botón pulsado; o la etiqueta del botón.
    ##################################################################
    def step(self, events, dt_ms):
        """
        Iteración no bloqueante del popup:
          - enruta eventos a contenido/botones,
          - actualiza kernel,
          - redibuja SOLO el kernel,
          - hace pygame.display.update() del rect del kernel, y devuelve None o el id del botón pulsado.
        """
        Ret = None

        # Cálculo del rect interno del kernel (inner: descontando márgenes de la sección) para hit-testing
        km = getattr(self.KernelSect, "W_Margin", 0)
        hm = getattr(self.KernelSect, "H_Margin", 0)
        kernel_inner = self._kernel_rect.inflate(-2 * km, -2 * hm)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # -------------------------
            # RATÓN: captura DOWN -> UP
            # -------------------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                if kernel_inner.collidepoint(event.pos):
                    # Captura para el contenido
                    self._mouse_capture = "content"
                    if hasattr(self.KernelSect, "handle_event"):
                        try:
                            self.KernelSect.handle_event(event)
                        except Exception as e:
                            print(f"[PopupDialogWindow] handle_event(DOWN->content) error: {e}")
                else:
                    # ¿Cae en algún botón?
                    pressed = None
                    for idButt, rect in self.ListButSect.DictButts.items():
                        if pygame.Rect(rect).collidepoint(event.pos):
                            pressed = idButt
                            break
                    if pressed:
                        self._mouse_capture = "buttons"
                        self._pressed_button_id = pressed
                    else:
                        self._mouse_capture = None
                        self._pressed_button_id = None

            elif event.type == pygame.MOUSEMOTION:
                if getattr(self, "_mouse_capture", None) == "content":
                    if hasattr(self.KernelSect, "handle_event"):
                        try:
                            self.KernelSect.handle_event(event)
                        except Exception as e:
                            print(f"[PopupDialogWindow] handle_event(MOTION->content) error: {e}")

            elif event.type == pygame.MOUSEBUTTONUP:
                if getattr(self, "_mouse_capture", None) == "content":
                    if hasattr(self.KernelSect, "handle_event"):
                        try:
                            self.KernelSect.handle_event(event)
                        except Exception as e:
                            print(f"[PopupDialogWindow] handle_event(UP->content) error: {e}")
                    self._mouse_capture = None

                elif getattr(self, "_mouse_capture", None) == "buttons":
                    # Validar click sobre el mismo botón
                    butt_ok = None
                    for idButt, rect in self.ListButSect.DictButts.items():
                        if pygame.Rect(rect).collidepoint(event.pos):
                            butt_ok = idButt
                            break
                    if butt_ok and butt_ok == getattr(self, "_pressed_button_id", None):
                        Ret = butt_ok
                    self._mouse_capture = None
                    self._pressed_button_id = None

            # -------------------------
            # TECLADO y RUEDA -> SOLO contenido (si lo pide)
            # -------------------------
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                if hasattr(self.KernelSect, "wants_keyboard") and self.KernelSect.wants_keyboard():
                    if hasattr(self.KernelSect, "handle_event"):
                        try:
                            self.KernelSect.handle_event(event)
                        except Exception as e:
                            print(f"[PopupDialogWindow] handle_event(KEY->content) error: {e}")

            elif event.type == pygame.MOUSEWHEEL:
                if hasattr(self.KernelSect, "wants_wheel") and self.KernelSect.wants_wheel():
                    if hasattr(self.KernelSect, "handle_event"):
                        try:
                            self.KernelSect.handle_event(event)
                        except Exception as e:
                            print(f"[PopupDialogWindow] handle_event(WHEEL->content) error: {e}")

        # Actualizar contenido interactivo (si lo hay). Si está en pausa, dt_ms=0.
        used_dt = 0 if getattr(self, "_paused", False) else dt_ms
        if hasattr(self.KernelSect, "update"):
            try:
                self.KernelSect.update(used_dt)
            except Exception as e:
                print(f"[PopupDialogWindow] KernelSect.update() error: {e}")

        # Redibujar SOLO la sección central (bordes + contenido) con clipping interno
        try:
            self.KernelSect.Draw(
                self._kernel_rect.x,
                self._kernel_rect.y,
                self._kernel_rect.width,
                self._kernel_rect.height,
                self.BorderSectRadius
            )
        except Exception as e:
            print(f"[PopupDialogWindow] KernelSect.Draw() error (redraw): {e}")

        pygame_widgets.update(events)  # Actualizar widgets como TextBox
        pygame.display.update(self._kernel_rect)  # Refrescar solo el área del kernel

        return Ret


    ################################
    # Control de pausa (congelar)
    ################################
    def pause(self):
        """Congela las actualizaciones (update recibe dt=0). Dispara hook on_pause() si existe."""
        if not getattr(self, "_paused", False):
            self._paused = True
            # Intentar notificar al contenido (si existe hook)
            try:
                # Puede estar en la sección (proxy) o en el contenido interno
                target = getattr(self.KernelSect, "_content", self.KernelSect)
                hook = getattr(target, "on_pause", None)
                if callable(hook):
                    hook()
            except Exception as e:
                print(f"[PopupDialogWindow] on_pause() error: {e}")


    ################################
    # Control de pausa (reanudar)
    ################################
    def resume(self):
        """Reanuda las actualizaciones. Dispara hook on_resume() si existe."""
        if getattr(self, "_paused", False):
            self._paused = False
            try:
                target = getattr(self.KernelSect, "_content", self.KernelSect)
                hook = getattr(target, "on_resume", None)
                if callable(hook):
                    hook()
            except Exception as e:
                print(f"[PopupDialogWindow] on_resume() error: {e}")

    ##################################################################
    # Esperar a recoger el evento de pulsar un botón para finalizar
    ##################################################################
    def Run(self):
        """
        Bucle modal del popup hasta que se pulse un botón.
        (Sigue existiendo para compatibilidad; internamente usa step()).
        """
        Ret = None
        # Reloj para FPS unificado (30 FPS) y dt en ms
        clock = pygame.time.Clock()
        # Estado de captura de ratón (DOWN -> UP) y botón presionado
        self._mouse_capture = None       # None | "content" | "buttons"
        self._pressed_button_id = None   # id del botón presionado (si captura de botones)

        while not Ret:
            dt_ms = clock.tick(30)              # milisegundos desde el frame anterior
            events = pygame.event.get()
            Ret = self.step(events, dt_ms)      # usar paso no bloqueante


        # on_unmount() del contenido interactivo (limpieza de recursos)
        if hasattr(self.KernelSect, "on_unmount"):
            try:
                self.KernelSect.on_unmount()
            except Exception as e:
                print(f"[PopupDialogWindow] KernelSect.on_unmount() error: {e}")

        gameDisplay.blit(self.DisplayCopy, (0, 0))  # Restaurar pantalla original
        pygame.display.flip()                      # Redibujar todo
        return Ret


# ----- END  class PopupDialogWindow: -----

#################################################################################################################
# Secciónes rectangulares de una Popup de Diálogo. Estas secciones serán Título, Mensaje y botones. Cada parte 
# tendrá una serie de atributos comunes que se incluyen aquí. Entendemos por seccion una de las tres partes de una 
# ventana PopUp de diálogo que serán (TitlePPsct, MessagePPsct, ListButtonsPPsct) para una PopupDialogWindow y serán
# (TitlePPsct, FormPPsct, ListButtonsPPsct) para una PopupDialogForm
#   
# PopupSection: Usamos el postfijo PPsct para estas secciones que heredan de PopupSection y que pueden usarse 
# para construir una PopupFormWindow, una PopupDialogWindow o para cualquiera de las dos indistintamente.
# Lo que sigue es una tabla con los tipos de PopupSections:
#
#   TitlePPsct          : Sección superior correspondiente al título. (Tendrá una sola línea).
#   MessagePPsct        : Sección correspondiente al mensaje de PopupDialogWindow . (Tendrá una o más líneas)
#   FormPPsct           : Sección correspondiente a la parte central del formulario con los campos de entrada.
#   ListButtonsPPsct    : Sección de la lista de botones. (Tendrá uno o más botones en una fila horizontal)
#################################################################################################################
class PopupSection:
    ###########################################################################################################
    """
    W_Margin:
    H_Margin:
    FontType:
    FontSize:
    ColorFg:
    ColorBg:
    BorderThikness:
    BorderColor:
    """
    def __init__(self, W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, \
                BorderThikness, BorderColor):
        TestIni()
        self.W_Margin=W_Margin
        self.H_Margin=H_Margin
        self.FontType=FontType
        self.FontSize=FontSize
        self.ColorFg=ColorFg
        if FontType and FontSize:
            try:
                self.Font=GetFont(FontType, FontSize) # Carga un fichero de fuente TrueType  (*.ttf) 
            except Exception as e:
                    print(f"""
    ERROR: {e} en PopupSection.__init__()
    FontType={FontType}, FontSize={FontSize}""")
        else:
            self.Font = None  # Sección sin texto (p.ej., SurfacePPsct)

        self.ColorBg=ColorBg
        self.WinBorderThikness=BorderThikness
        self.WinBorderColor=BorderColor

    ##################################################################
    # Dibujar la sección. Método abstracto.
    ##################################################################
    # @abstractmethod 
    def Draw(self):  # definicion del método abstracto Draw para PopupSection
        pass # 

# ----- END  class PopupSection: -----


################################################################################################################
class TitlePPsct(PopupSection):
    """
    Es la sección del popup correspondiente al título. (Hereda de PopupSection)
    """
    ############################## (Constructor de la clase TitlePPsct ) #########################################
    def __init__(self, W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, \
                    BorderThikness, BorderColor, TxtTitle):
        super().__init__(W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, \
        BorderThikness, BorderColor)
        self.TxtTitle=TxtTitle
        #self.FontMess=pygame.font.SysFont(FontType, FontSize) # Fuente del texto del mensaje
        self.Font=GetFont(FontType, FontSize) # Carga un fichero de fuente TrueType  (*.ttf) 

    ###########################################################################################################
    def GetWidthHeigthTitle(self):
        """
        Obtiene las dimensiones del contenido de esta sección TitlePPsct. (se incluyen los márgenes de la sección).
        """
        self.WideTitle, self.HeigthTitle=  GetWidthHeigthText(self.TxtTitle, self.Font)
        self.WideTitle += (2*self.W_Margin) # Incrementamos con los márgenes derecho e izquierdo
        self.HeigthTitle += (2*self.H_Margin) # Incrementamos con los márgenes superior e inferior
        return self.WideTitle, self.HeigthTitle

    ##########################################################################################################
    def Draw(self, x, y, Wide, Heigth, BorderRadius): # Implementacion particular de Draw() para Title
        """
        Implementación específica del método abstracto para dibujar el Title.
        Debe venir precedida de los cálculos de las dimensiones de las tres secciones, gracias a
        esos cálculos que parten de las informaciones GetWidthHeigthTitle() de cada sección 
        podremos recibir los parámetros (x, y, Wide, Heigth, BorderRadius) con los valores correctos 
        ya que las dimensiones finales están en función de los contenidos de todas las secciones para
        generar una composición optimizada de la PopupDialogWindow.
        """

        # Dibujar el rectángulo de la sección Title en la pantalla
        Rect=(x, y, Wide, Heigth) # Damos la posicion y el tamaño al rectángulo
        DrawRect(self.ColorBg, self.WinBorderColor, Rect, 5, BorderRadius)
        # Creamos una fuente utilizando GetFont, y luego utilizamos font.render para renderizar el texto 
        # en una superficie llamada text_surface. A continuación, obtenemos el rectángulo del texto utilizando
        # text_surface.get_rect(), y lo centramos dentro del rectángulo principal (PopupDialogWindow) utilizando
        # text_rect.center.
        text_surface = self.Font.render(self.TxtTitle, True, self.ColorFg)  # Renderizar el texto  obteniedo text_surface
        text_rect = text_surface.get_rect()                                 # Obtener el pygame.Rect del texto
        text_rect.center = ((x + Wide//2), (y + Heigth//2))     # Centrar el texto en el rectángulo de la PopupDialogWindow
        gameDisplay.blit(text_surface, text_rect)          # Dibujar el texto en el centro del rectángulo
        #pygame.display.update()     # display.update() (sin argumentos) actualiza el contenido de toda la pantalla

# ----- END  class TitlePPsct(PopupSection): -----

################################################################################################################
class MessagePPsct(PopupSection):
    """
    Es la sección del popup correspondiente al mensaje, tendrá una o más líneas. (Hereda de PopupSection)
    """
    ################################ (Constructor de la clase MessagePPsct ) ####################################
    def __init__(self, W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, \
        BorderThikness, BorderColor, Message, PorcSepLines):
        super().__init__(W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, \
        BorderThikness, BorderColor)
        self.Message=Message
        self.PorcSepLines=PorcSepLines
        #self.FontMess=pygame.font.SysFont(FontType, FontSize) # Fuente del texto del mensaje
        self.Font=GetFont(FontType, FontSize) # Carga un fichero de fuente TrueType  (*.ttf) 

    ##############################################################################################################
    def GetWidthHeigthMessage(self):
        """
        Obtiene las dimensiones del contenido de esta sección Message. (se incluyen los márgenes de la seccion).
        """
        self.WideMessage, self.HeigthMessage=  GetWidthHeigthText(self.Message, self.Font, self.PorcSepLines)
        self.WideMessage += (2*self.W_Margin) # Incrementamos con los márgenes derecho e izquierdo
        self.HeigthMessage += (2*self.H_Margin) # Incrementamos con los márgenes superior e inferior
        return self.WideMessage, self.HeigthMessage

    ##############################################################################################################
    def Draw(self, x, y, Wide, Heigth, BorderRadius, PorcSepLines=130): ## Implementacion particular para MessagePPsct
        """
        Implementación específica del método abstracto  para dibujar el Message.
        Véase: GetWidthHeigthText() que hizo el trabajo previo para calcular el espacio necesario para representar 
        todo el texto con la fuente y el tamaño de fuente indicado.
        """
        # Dibujar el rectángulo de la seccion Message en la pantalla
        self.GetWidthHeigthMessage()
        Rect=(x, y, Wide, Heigth) # Damos la posicion y el tamaño al rectángulo
        DrawRect(self.ColorBg, self.WinBorderColor, Rect, 5, BorderRadius)
        x=x+self.W_Margin
        Sep=PorcSepLines//100
        Y2=y
        for line in self.Message.splitlines():
            text_surface = self.Font.render(line, True, self.ColorFg) # Renderizar el texto en una superficie
            text_rect = text_surface.get_rect()             # Obtener el pygame.Rect del texto
            gameDisplay.blit(text_surface, (x, Y2))    # Lo dibujamos en su posición definitiva
            Y2 +=  text_surface.get_height() + Sep          # Obtenemos la posición vertical de la siguiente linea
        #pygame.display.update()  # display.update() (sin argumentos) actualiza el contenido de toda la pantalla

# ----- END  class MessagePPsct(PopupSection): -----


# ------------------------------------------------------------------------------------
# SurfacePPsct (VERSIÓN SIMPLIFICADA — rect fijo, interfaz clásica para PopupDialogWindow)
# - Mantiene: GetWidthHeigthSurface(), Draw(...), update(dt_ms), handle_event(e),
#             wants_keyboard(), wants_wheel()
# - Quita: negociación de tamaño dinámica y cualquier soporte de resize.
# - Márgenes y borde: si no se pasan, se toman del estilo activo (GetStyleDict()).
# - Rueda del ratón: SOLO si el cursor está sobre inner_rect (política pedida).
# ------------------------------------------------------------------------------------
import pygame

class SurfacePPsct:
    """
    Sección de kernel para contenido interactivo o una pygame.Surface estática.
    Tamaño del área útil (inner) FIJO durante la vida de la popup.

    Params
    ------
    content_or_surface : objeto interactivo o pygame.Surface
        - Interactivo: debe exponer draw(surface, rect) y opcionalmente:
          on_mount(rect), update(dt_ms), handle_event(event), wants_keyboard(), wants_wheel()
        - Estático: pygame.Surface
    interactive_size : (w, h) | None
        - Obligatorio si el contenido es interactivo (tamaño lógico del área útil).
        - Ignorado si es pygame.Surface (se usa surface.get_size()).
    W_Margin, H_Margin : int | None
        Márgenes internos. Si None, se toman del estilo.
    BorderThikness : int | None
        Grosor del borde. Si None, del estilo.
    BorderColor : (r,g,b) | None
        Color del borde. Si None, del estilo.

    Interfaz expuesta para PopupDialogWindow:
        GetWidthHeigthSurface() -> (W, H)  (tamaño TOTAL de la sección, borde+márgenes+inner)
        Draw(x, y, Wide, Heigth, BorderRadius)
        update(dt_ms)
        handle_event(event) -> bool (True si consumido)
        wants_keyboard() -> bool
        wants_wheel() -> bool
    """
    def __init__(self,
                 content_or_surface,
                 W_Margin=None, H_Margin=None,
                 BorderThikness=None, BorderColor=None,
                 *,
                 interactive_size=None):

        # 1) Determinar si es contenido interactivo o una Surface estática
        self._is_surface = isinstance(content_or_surface, pygame.Surface)
        self._content = content_or_surface if not self._is_surface else None
        self._surface = content_or_surface if self._is_surface else None

        if self._is_surface:
            self._inner_size = self._surface.get_size()
        else:
            if not isinstance(interactive_size, (tuple, list)) or len(interactive_size) != 2:
                raise ValueError("interactive_size=(w,h) es obligatorio para contenido interactivo.")
            self._inner_size = (int(interactive_size[0]), int(interactive_size[1]))

        # 2) Estilo por defecto si no se pasan parámetros (no rompemos API)
        try:
            from popup_gui.Popup_Dialog import GetStyleDict  # import local para evitar ciclos
            ST = GetStyleDict()
        except Exception:
            ST = {}

        def _fallback(key, default):
            return ST.get(key, default)

        self.W_Margin = int(W_Margin if W_Margin is not None else _fallback("Kernel_W_Margin", 16))
        self.H_Margin = int(H_Margin if H_Margin is not None else _fallback("Kernel_H_Margin", 12))
        self.BorderThikness = int(BorderThikness if BorderThikness is not None else _fallback("Kernel_BorderThikness", 2))
        self.BorderColor = tuple(BorderColor if BorderColor is not None else _fallback("Kernel_BorderColor", (0, 0, 0)))

        # 3) Estado de geometría (se fijan en el primer Draw)
        self._outer_rect = None       # Rect total (x,y,Wide,Heigth) que recibe Draw
        self._inner_rect = None       # Rect útil = outer - (bordes + márgenes)
        self._mounted = False         # on_mount hecho

        # 4) Política de eventos
        #    Rueda: SOLO si el cursor está sobre inner_rect (pedido por el usuario)
        #    Teclado: por defecto True si el contenido es interactivo; False si es Surface
        self._wheel_policy_hover_only = True

    # --------------------------------------------------------------------------------
    # Medición (tamaño total de la sección = borde*2 + márgenes*2 + inner_size)
    # --------------------------------------------------------------------------------
    def GetWidthHeigthSurface(self):
        inner_w, inner_h = self._inner_size
        total_w = inner_w + 2 * (self.W_Margin + self.BorderThikness)
        total_h = inner_h + 2 * (self.H_Margin + self.BorderThikness)
        return (total_w, total_h)

    # --------------------------------------------------------------------------------
    def GetWidthHeigthMessage(self):
        # Alias por compatibilidad con PopupDialogWindow antiguo
        return self.GetWidthHeigthSurface()

    # --------------------------------------------------------------------------------
    # Dibujo
    # --------------------------------------------------------------------------------
    def Draw(self, x, y, Wide, Heigth, BorderRadius=0):
        # 1) Fijar outer_rect e inner_rect en primera llamada; después, validar (rect fijo)
        outer = pygame.Rect(int(x), int(y), int(Wide), int(Heigth))
        if self._outer_rect is None:
            self._outer_rect = outer.copy()
            self._inner_rect = self._compute_inner_rect(self._outer_rect)
            self._validate_inner_size_or_raise(self._inner_rect.size)
            # Montaje perezoso del contenido interactivo
            if not self._is_surface and hasattr(self._content, "on_mount"):
                try:
                    self._content.on_mount(self._inner_rect.copy())
                except Exception:
                    # No interrumpimos el render por errores de on_mount
                    pass
            self._mounted = True
        else:
            if outer.size != self._outer_rect.size or outer.topleft != self._outer_rect.topleft:
                # Prohibimos cambios de tamaño/posicionamiento (simplificación central)
                raise ValueError(
                    "SurfacePPsct: redimensionar o reposicionar el kernel está prohibido por diseño. "
                    f"Esperado {self._outer_rect}, recibido {outer}."
                )

        # 2) Dibujar: clip al inner_rect, contenido, restaurar clip, y borde fuera del clip
        screen = pygame.display.get_surface()
        if screen is None:
            return  # nada que hacer si no hay display

        prev_clip = screen.get_clip()
        screen.set_clip(self._inner_rect)

        if self._is_surface:
            self._draw_static_surface(screen)
        else:
            # draw(surface, rect) del contenido interactivo
            if hasattr(self._content, "draw"):
                self._content.draw(screen, self._inner_rect.copy())

        # Restaurar clip
        screen.set_clip(prev_clip)

        # Borde (fuera del clip)
        if self.BorderThikness > 0:
            pygame.draw.rect(
                screen,
                self.BorderColor,
                self._outer_rect,
                width=self.BorderThikness,
                border_radius=int(BorderRadius or 0),
            )

    # --------------------------------------------------------------------------------
    # Update y eventos
    # --------------------------------------------------------------------------------
    def update(self, dt_ms):
        if self._is_surface:
            return
        if hasattr(self._content, "update"):
            self._content.update(dt_ms)

    def handle_event(self, event):
        """
        Devuelve True si el contenido consumió el evento.
        - Ratón: se mapean coords a relativas del inner_rect SOLO si caen dentro.
        - Rueda: SOLO si el cursor está sobre inner_rect (política hover-only).
        - Teclado: se reenvía tal cual si el contenido lo desea.
        """
        if self._is_surface:
            return False
        if not hasattr(self._content, "handle_event"):
            return False
        if self._inner_rect is None:
            return False

        etype = event.type

        # --- Eventos de ratón (solo si la posición está dentro del inner_rect) ---
        if etype in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            if not hasattr(event, "pos"):
                return False
            if not self._inner_rect.collidepoint(event.pos):
                return False
            # Mapear a coords relativas
            rel_event = self._map_mouse_event_to_inner(event, self._inner_rect.topleft)
            return bool(self._content.handle_event(rel_event))

        # --- Rueda del ratón (hover-only) ---
        if etype == pygame.MOUSEWHEEL:
            if self._wheel_policy_hover_only:
                # En Pygame 2, MOUSEWHEEL puede no traer pos. Tomamos pos actual del cursor.
                mouse_pos = pygame.mouse.get_pos()
                if not self._inner_rect.collidepoint(mouse_pos):
                    return False
            return bool(self._content.handle_event(event))

        # --- Teclado u otros ---
        if etype in (pygame.KEYDOWN, pygame.KEYUP):
            if not self.wants_keyboard():
                return False
            return bool(self._content.handle_event(event))

        # Otros tipos: se reenvían tal cual, el contenido decide
        return bool(self._content.handle_event(event))

    def wants_keyboard(self):
        if self._is_surface:
            return False
        if hasattr(self._content, "wants_keyboard"):
            try:
                return bool(self._content.wants_keyboard())
            except Exception:
                return True
        return True

    def wants_wheel(self):
        if self._is_surface:
            return False
        if hasattr(self._content, "wants_wheel"):
            try:
                return bool(self._content.wants_wheel())
            except Exception:
                return True
        return True

    # --------------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------------
    def _compute_inner_rect(self, outer_rect):
        x = outer_rect.x + self.BorderThikness + self.W_Margin
        y = outer_rect.y + self.BorderThikness + self.H_Margin
        w = outer_rect.w - 2 * (self.BorderThikness + self.W_Margin)
        h = outer_rect.h - 2 * (self.BorderThikness + self.H_Margin)
        return pygame.Rect(x, y, max(0, w), max(0, h))

    def _validate_inner_size_or_raise(self, inner_size):
        expected_w, expected_h = int(self._inner_size[0]), int(self._inner_size[1])
        got_w, got_h = int(inner_size[0]), int(inner_size[1])

        if self._is_surface:
            # Para Surface estática: permitir área útil MAYOR (se centra sin escalar).
            # Solo es error si el área útil es MENOR (recorta la surface).
            if got_w < expected_w or got_h < expected_h:
                raise ValueError(
                    "SurfacePPsct: el área útil (inner_rect) es menor que el tamaño de la Surface.\n"
                    f"Esperado al menos inner_size=({expected_w}, {expected_h}), obtenido=({got_w}, {got_h}). "
                    "Esto recortaría la imagen; ajusta el layout o reduce márgenes/botones/título."
                )
            return

        # Para contenido interactivo: exigir igualdad exacta (coords relativas, no resize).
        if (got_w, got_h) != (expected_w, expected_h):
            raise ValueError(
                "SurfacePPsct: el área útil (inner_rect) no coincide con el tamaño lógico esperado.\n"
                f"Esperado inner_size=({expected_w}, {expected_h}), obtenido=({got_w}, {got_h}). "
                "El redimensionado está prohibido por diseño para contenido interactivo."
            )


    @staticmethod
    def _map_mouse_event_to_inner(event, inner_topleft):
        """
        Devuelve una copia del evento con las coordenadas pos/mpos convertidas a relativas
        respecto a inner_topleft. Mantiene otros atributos del evento intactos.
        """
        # Pygame no provee clonación directa, creamos uno nuevo con los mismos dict attrs.
        etype = event.type
        attr = event.dict.copy()
        if "pos" in attr:
            ox, oy = attr["pos"]
            ix, iy = inner_topleft
            attr["pos"] = (ox - ix, oy - iy)
        if "rel" in attr:
            # rel ya es relativo al último pos; lo dejamos como está
            pass
        return pygame.event.Event(etype, attr)

    def _draw_static_surface(self, screen):
        # Centrar la Surface en el inner_rect (sin escalar)
        sw, sh = self._surface.get_size()
        ir = self._inner_rect
        x = ir.x + (ir.w - sw) // 2
        y = ir.y + (ir.h - sh) // 2
        screen.blit(self._surface, (x, y))


################################################################################################################
# HelpPPsct: Sección central que integra un HelpViewer (helpview.help_core) dentro del popup.
# Recibe un texto Markdown y pinta un visor de ayuda con scroll y formato.
class HelpPPsct(PopupSection):
    """
    Sección intermedia para mostrar un visor de ayuda Markdown embebido.
    Proporciona la misma interfaz que MessagePPsct/SurfacePPsct:
        - GetWidthHeigthMessage()
        - Draw(...)
        - handle_event(), update(), wants_keyboard(), wants_wheel()
    """
    def __init__(
        self,
        md_text,
        interactive_size,
        W_Margin,
        H_Margin,
        BorderThikness,
        BorderColor,
        *,
        title="Ayuda",
        style_variant="formal",
        style_json_path=None,
        fonts_dir=None,
        help_font_file=None,
        help_code_font_file=None,
        kernel_bg=None,
        wheel_step=48,
        visual_indent_px=24,
        indent_spaces_per_level=2,
    ):
        # Nota: no llamamos a PopupSection.__init__ porque aquí no hay fuente propia;
        # el render lo hace HelpViewer internamente.
        self.W_Margin = int(W_Margin)
        self.H_Margin = int(H_Margin)
        self.BorderThikness = int(BorderThikness)
        self.BorderColor = tuple(BorderColor)

        # Aliases por compatibilidad con el resto del módulo
        self.WinBorderThikness = self.BorderThikness
        self.WinBorderColor = self.BorderColor

        self._md_text = md_text
        self._interactive_size = (int(interactive_size[0]), int(interactive_size[1]))
        self._viewer = None
        self._mounted_size = None

        # Guardamos kwargs del viewer
        self._viewer_kwargs = dict(
            size=self._interactive_size,
            style_variant=style_variant,
            style_json_path=style_json_path,
            fonts_dir=fonts_dir,
            help_font_file=help_font_file,
            help_code_font_file=help_code_font_file,
            kernel_bg=kernel_bg,
            wheel_step=wheel_step,
            visual_indent_px=visual_indent_px,
            indent_spaces_per_level=indent_spaces_per_level,
            title=title,
        )


    def _ensure_viewer(self) -> None:
        """Crear HelpViewer bajo demanda y dejarlo listo en self._viewer."""
        if self._viewer is not None:
            return

        # 1) Import preferido: help_core_pygame
        try:
            from help_core_pygame import HelpViewer as _HelpViewer
            from help_core_pygame import HelpConfig as _HelpConfig
        except Exception:
            # 2) Fallback legacy: helpview
            try:
                from helpview.help_core import HelpViewer as _HelpViewer
                from helpview.help_core import HelpConfig as _HelpConfig
            except Exception as exc:
                raise ImportError(
                    "HelpPPsct requiere 'help_core_pygame' (preferido) o 'helpview.help_core' (legacy)."
                ) from exc

        # 3) Construir cfg con los campos que HelpViewer usa internamente
        #    Nota: este patrón (HelpConfig(...) y luego HelpViewer(cfg)) ya lo tenías en el código anterior.
        vw = dict(self._viewer_kwargs)

        cfg = _HelpConfig(
            md_text=self._md_text,
            title=vw.get("title", "Ayuda"),
            size=self._interactive_size,

            style_json_path=vw.get("style_json_path"),
            style_variant=vw.get("style_variant"),
            style_overrides=None,

            fonts_dir=vw.get("fonts_dir"),
            help_font_file=vw.get("help_font_file"),
            help_code_font_file=vw.get("help_code_font_file"),

            indent_spaces_per_level=vw.get("indent_spaces_per_level", 2),
            visual_indent_px=vw.get("visual_indent_px", 24),
            wheel_step=vw.get("wheel_step", 48),

            kernel_bg=vw.get("kernel_bg"),
        )

        self._viewer = _HelpViewer(cfg)

        if self._viewer is None:
            raise RuntimeError("HelpViewer quedó en None tras instanciar; esto no es válido.")


    def GetWidthHeigthMessage(self):
        """
        Dimensiones TOTALES de la sección kernel para que PopupDialogWindow dimensione la ventana.
        Debe incluir márgenes (igual que MessagePPsct / SurfacePPsct).
        """
        w, h = self._interactive_size
        return (w + 2 * self.W_Margin, h + 2 * self.H_Margin)

    def Draw(self, x, y, Wide, Heigth, BorderRadius):
        """Dibuja marco y delega el render al HelpViewer dentro del área útil."""
        self._ensure_viewer()

        Rect = (x, y, Wide, Heigth)
        DrawRect((255, 255, 255), self.BorderColor, Rect, self.BorderThikness, BorderRadius)

        inner_rect = pygame.Rect(
            x + self.W_Margin,
            y + self.H_Margin,
            max(0, Wide - 2 * self.W_Margin),
            max(0, Heigth - 2 * self.H_Margin),
        )

        # Montaje (si el viewer soporta on_mount)
        try:
            size_now = (inner_rect.width, inner_rect.height)
            if self._mounted_size != size_now and hasattr(self._viewer, "on_mount"):
                self._viewer.on_mount(inner_rect)

                # Si el viewer no se dimensiona en on_mount, probar métodos típicos:
                if hasattr(self._viewer, "set_size"):
                    try:
                        self._viewer.set_size((inner_rect.width, inner_rect.height))
                    except Exception:
                        pass
                elif hasattr(self._viewer, "resize"):
                    try:
                        self._viewer.resize(inner_rect.width, inner_rect.height)
                    except Exception:
                        pass

                self._mounted_size = size_now
        except Exception:
            pass

        prev_clip = gameDisplay.get_clip()
        gameDisplay.set_clip(inner_rect)
        try:
            self._viewer.draw(gameDisplay, inner_rect)
        finally:
            gameDisplay.set_clip(prev_clip)

    def on_mount(self, rect):
        """Hook opcional si el contenedor lo llama."""
        self._ensure_viewer()
        if hasattr(self._viewer, "on_mount"):
            try:
                self._viewer.on_mount(rect)
            except Exception:
                pass

    def on_unmount(self):
        pass

    def update(self, dt):
        pass

    def handle_event(self, event):
        self._ensure_viewer()
        if hasattr(self._viewer, "handle_event"):
            try:
                return bool(self._viewer.handle_event(event))
            except Exception:
                return False
        return False

    def wants_keyboard(self):
        return True

    def wants_wheel(self):
        return True

# ----- END  class HelpPPsct(PopupSection): -----


################################################################################################################
class ListButtonsPPsct(PopupSection):
    """
    Es la sección del Popup de la lista de botones. Tendrá uno o más botones. (Hereda de PopupSection)
    Los botones se crean con una cadena de texto que hace de identificador y de etiqueta visual del botón.
    """

    #################################### (Constructor) ##############################################
    def __init__(self, W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, \
        BorderThikness, BorderColor, ListIdButt, ButtPadding, ColorBgBut):
        super().__init__( W_Margin, H_Margin, FontType, FontSize, ColorFg, ColorBg, \
        BorderThikness, BorderColor)
        """
        """
        self.ListIdButt=ListIdButt
        self.Font=GetFont(FontType, FontSize) # Carga un fichero de fuente TrueType  (*.ttf) 
        self.ButtPadding=ButtPadding
        self.ColorBgBut=ColorBgBut

    ##############################################################################################################
    def GetWidthHeigthContent(self):
        """
        Implementación del método GetWidthHeigthContent() para obtetenr las dimensiones de esta sección ListButtons. 
        """
        # Obtener los rectángulos para los diferentes botones
        # Obtener el ancho y alto de la superficie que se necesita para poder visualizar la lista de botones con
        # su fuente sin márgenes.
        # Creamos DictButts con información incompleta de los botones (IdButt, Ancho y Alto) dejando la información
        # de la posición definitiva de los botones para el momento de dibujarlos, ya que la expansión de la 
        # PopupWindow a su anchura definitiva afectará a las posiciones de los botones.

        # self.W_Margin es el margen que separa los botones del borde de la sección solo hay dos.

        self.DictButts={} #  Diccionario con elementos (clave=IdButt, Rect=RectButt)

        # self.font_margin es el margen que separa los carateres de texto del borde del boton
        # Calcular el margen entre el texto del botón y sus bordes: un sexto del alto de la fuente
        self.font_margin = self.Font.get_height() // 6

        self.Width=0
        NumButts=0

        for IdBut in self.ListIdButt:
            NumButts +=1
            wBut, hBut= GetWidthHeigthText(IdBut, self.Font) # Calcular las dimensiones del texto del boton
            self.DictButts[IdBut]=(0,0, wBut + self.font_margin*2, hBut + self.font_margin*2 )
            self.Width += wBut + self.font_margin # 

        self.Width += self.ButtPadding * (NumButts-1) # Sumamos el espacio de separacion entre botones
        self.Width += self.W_Margin * 2 + self.font_margin * NumButts  # Sumamos margenes derechos e izquierdos
        self.Heigth = hBut + self.H_Margin * 2 + self.font_margin * 2 # Sumamos los márgenes superiores e inferiores.
        # Memorizamos el valor calculado de la anchura para conservarlo cuando tengamos que dibujar los botones en 
        # su posición, ya que self.Width puede ser modificado (agrandado) 
        self.WidthContent= self.Width 
        self.HeigthContent= self.Heigth
        return self.Width, self.Heigth 

    ##############################################################################################################
    # self.ListButSect.Draw(self.X+self.WinMargin, self.Y+self.WinMargin, self.MaxW, self.H_But, self.BorderSectRadius)
    def Draw(self, x, y, Wide, Heigth, BorderRadius): ## Implementacion particular de Draw() para ListButtonsPPsct
        """
        Implementación específica del método abstracto para dibujar la lista de botones 
        """
        # Dibujar el rectángulo de la seccion en la pantalla
        self.GetWidthHeigthContent()
        Rect=(x, y, Wide, Heigth) # Damos la posicion y el tamaño al rectángulo de la sección ListButtonsPPsct
        #self.DrawRect(self.ColorBg, self.WinBorderColor, Rect, 5, BorderRadius)
        # BUG:  Al sustituir self.ColorBg por rojo se aprecia que los fallos son que el color del fondo del la seccion
        #       y el color de fondo del bontón son idénticos y no se aprecian. Ademas los rectángulos salen en su
        #       posición y los textos de los botones por el contrario sale centrado con la seccion 
        DrawRect(self.ColorBg, self.WinBorderColor, Rect, 5, BorderRadius)
        # Incrementar las posiciones para respetar los márgenes horizontales y verticales
        x=x+self.W_Margin
        y=y+self.H_Margin
        # Para calcular la posición X (posición de la esquina sup. izquierda) del primer botón ya no serviría usar un
        # simple 'X_ButIz=x+self.W_Margin' ya que tras el ajuste de todas las secciones al mismo ancho, la ancgura de
        # esta sección podría haber aumentado para ocupar todo el ancho de la PopupWindow. Debemos partir de la
        # anchura calculada inicialmente self.WidthContent.
        X_Center, Y_Center = (x+(Wide//2), y+(Heigth//2))   # Retornamos las coordenadas del centro de la sección
        X_But= X_Center - (self.WidthContent//2)            # Inicializamos la posición X de primer botón
        Y_But= Y_Center - (self.HeigthContent//2)            # Inicializamos la posición X de primer botón


        # Posicionamos y dibujamos cada uno de los botones
        for IdBut in self.ListIdButt:
            # self.DictButts[IdBut] fue inicializado con (0,0, wBut, hBut) en GetWidthHeigthContent() 
            # Es decir, aún carecen de posición y hay que ir calculando la posición horizonal de cada botón.
            # La posición vertical es 'y'.
            dummy, dummy, wBut, hBut = self.DictButts[IdBut] 
            # Completamos y guardamos la información de este elemento el diccionario y lo transformamos en un 
            # pygame.Rect() porque lo usaremos al verificar el click del mouse dentro del rectángulo de alguno de los 
            # botones.
            RectButt=pygame.Rect(X_But, y, wBut, hBut)         
            self.DictButts[IdBut]=RectButt
            # Dibujamos el botón en su posición
            #pygame.draw.rect(self.ColorBgBut, RectButt)   # Dibujar el fondo del boton


            # Renderizar el texto del botón con el color de primer plano
            text_surface = self.Font.render(IdBut, True, self.ColorFg)

            # Obtener el rectángulo del texto (ancho y alto del texto renderizado)
            text_rect = text_surface.get_rect()

            # Calcular el tamaño total del botón incluyendo márgenes
            wBut = text_rect.width + 2 * self.font_margin  # Ancho del botón: texto + márgenes laterales
            hBut = text_rect.height + 2 * self.font_margin  # Alto del botón: texto + márgenes arriba/abajo

            # Construir el rectángulo del botón en la posición actual (X_But, Y_But)
            RectButt = pygame.Rect(X_But, Y_But, wBut, hBut)

            # Dibujar el rectángulo del botón con colores y borde redondeado
            DrawRect(self.ColorBgBut, self.WinBorderColor, RectButt, self.WinBorderThikness, 5)

            # Centrar el texto dentro del nuevo botón
            text_rect.center = RectButt.center

            # Dibujar el texto centrado dentro del botón
            gameDisplay.blit(text_surface, text_rect)

            # Avanzar la posición X para el siguiente botón (respetando el espaciado entre botones)
            X_But += wBut + self.ButtPadding


            '''
            DrawRect(self.ColorBgBut, self.WinBorderColor, RectButt, self.WinBorderThikness, 5)
            text_surface= self.Font.render(IdBut, True, self.ColorFg)   # Renderizar texto del botón en una superficie
            text_rect = text_surface.get_rect()                         # Obtener el pygame.Rect del texto
            text_rect.center = pygame.Rect(RectButt).center             # Centrar el texto en el rectángulo del botón
            gameDisplay.blit(text_surface, text_rect)                   # Dibujar el texto en el centro del rectángulo
            X_But +=wBut+ self.ButtPadding                              # Posicion X del siguiente botón
            '''
        #pygame.display.update()  # display.update() (sin argumentos) actualiza el contenido de toda la pantalla

# ..... END  class ListButtonsPPsct(PopupSection): -----


################################################################################################################
# Tipo predefinido de Popup para mostrar errores 
################################################################################################################
def PopupERR(Message, IdButt="   Continuar   ", Title="Mensaje de error", FlagAlert="Red"):
    '''
    Tipo predefinido de Popup para mostrar errores. Se considera que tiene un nivel de alerta rojo.
    Por defecto incluirá un solo botón que permita continuar. 

    Parámetros:
    -----------
        Message (str):
            Mensaje de error que deseamos mostrar.

        IdButt (str):
            Etiqueta del botón.
            Podemos dejar el valor por defecto

        Tile (str):
            Título de la ventana.

        FlagAlert (pygame.Color):
            Color de la primera sección y de la última con significado de nivel de alerta.

    Retorno:
    --------
        No retorna nada.

    '''
    ListIdButt=[IdButt]
    ppdw=PopupDialogWindow( Message, ListIdButt=ListIdButt,  Title=Title, FlagAlert=FlagAlert )
    ppdw.Run()
   
################################################################################################################
# Tipo predefinido de Popup para mostrar Advertencias importantes. 
################################################################################################################
def PopupWARN( Message, IdButt="   Continuar   ", Title="Advertencia importante", FlagAlert="Orange"):
    '''
    Tipo predefinido de Popup para mostrar advertencias importantes caon nivel de alerta naranja.

    Veasé PopupERR() para más información ya que son procedimientos casi iguales en los nos limitamos a variar
    los valores por defecto para facilitar la programación con estos popups y el nivel de alerta.
    '''
    ListIdButt=[IdButt]
    ppdw=PopupDialogWindow( Message, ListIdButt=ListIdButt,  Title=Title, FlagAlert=FlagAlert )
    ppdw.Run()
   
################################################################################################################
# Tipo predefinido de Popup para mostrar Avisos 
################################################################################################################
def PopupNOTICE( Message, IdButt="   Continuar   ", Title="Aviso", FlagAlert="Yellow"):
    '''
    Tipo predefinido de Popup para mostrar Avisos con un nivel de alerta amarillo.

    Veasé PopupERR() para más información ya que son procedimientos casi iguales en los nos limitamos a variar
    los valores por defecto para facilitar la programación con estos popups y el nivel de alerta.
    '''
    ListIdButt=[IdButt]
    ppdw=PopupDialogWindow( Message, ListIdButt=ListIdButt,  Title=Title, FlagAlert=FlagAlert )
    ppdw.Run()

################################################################################################################
# Tipo predefinido de Popup para mostrar Mensajes informativos
# De forma automática solo incluirá un botón que permita continuar.
################################################################################################################
def PopupINFO( Message, IdButt="   Continuar   ", Title="Mensaje informativo", FlagAlert="Green"):
    '''
    Tipo predefinido de Popup para mostrar mensajes meramente informativos.

    Veasé PopupERR() para más información ya que son procedimientos casi iguales en los nos limitamos a variar
    los valores por defecto para facilitar la programación con estos popups y el nivel de alerta.
    '''
    ListIdButt=[IdButt]
    ppdw=PopupDialogWindow( Message, ListIdButt=ListIdButt,  Title=Title, FlagAlert=FlagAlert )
    ppdw.Run()


################################################################################################################
# Tipo predefinido de Popup para plantear una pregunta que debe de ser respondida pulsando alguno de los
# botones.
# ListIdButt: Es ina lista que contiene identificadores de los botones que deseamos incluir. Estos 
# identificadores son el texto del botón y han de ser diferentes para cada uno de ellos. El botón pulsado
# retorna su identificador al ser pulsado.
################################################################################################################
def PopupASK( Message, ListIdButt, Title="Pregunta", FlagAlert="Blue"):
    '''
    Tipo predefinido de Popup para presentar preguntas acompañadas de taantos botones como posibles respuestas
    deseemos contemplar.

    Parámetros:
    -----------
        Message (str):
            Mensaje de la pregunta que deseamos plantear al usuario

        ListIdButt (list):
            Lista de cadenas (str) con las posibles respuestas. Usaremos estos valores para etiquetar los botones 
            y tambien se usará como valores de retorno en el caso de pulsar uno de los botones.

        Tile (str):
            Título de la ventana.

        FlagAlert (pygame.Color):
            Color de la primera sección y de la última con significado de nivel de alerta.

    Retorno:
    --------
        (str): Retorna el valor de la etiqueta pulsada.
    '''
    ppdw=PopupDialogWindow( Message, ListIdButt,  Title=Title, FlagAlert=FlagAlert )
    return ppdw.Run()

################################################################################################################
# MenuSelectFiles contruye los datos para generar un menu para poder seleccionar un fichero de la página de ficheros
# actual, permitiendo en su caso retornar una peticion de avance a la siguiente página de fichero o retroceso
# a la página anterior.
################################################################################################################
def MenuSelectFiles( Page, PageNum, TotNumPages):
    TextMenu=""
    ListButtId=[" Cancelar "]
    # Si no es la primera página añadir botón para poder retroceder a la página anterior
    if PageNum>0: 
        ListButtId.append(" Re.Pag ")
    # Añadir la lista numerada de ficheros de la página a TextMenu 
    print(Page)
    for num, filename in Page:
        TextMenu += "%d) %s\n" % (num+1, os.path.basename(filename) )
        ListButtId.append(str(num+1))
    # Si no es la última página añadir botón para poder avanzar página
    if PageNum+1 < TotNumPages: 
        ListButtId.append(" Av.Pag ")
    # Invocar la popup window
    return PopupASK(TextMenu, ListButtId, \
        Title="Seleccione el número del fichero deseado.  <Página (%d/%d)>" % (PageNum+1, TotNumPages)) 
     
################################################################################################################
# MenuScanFiles es similar a la anterior. Construye los datos para generar un menu para visualizar los ficheros
# de la página actual de ficheros permitiendo, en su caso,retroceder, avanzar o terminar la visualizacion gracias
# tres botones. No retorna nada.
################################################################################################################
def MenuScanFiles(Page, PageNum, TotNumPages):
    TextMenu=""
    ListButtId=[]
    # Si no es la primera página añadir botón para poder retroceder a la página anterior
    if PageNum>0: 
        ListButtId.append(" Re.Pag ")
    # Añadir la lista numerada de ficheros de la página a TextMenu 
    # Invocar la popup window
    ListButtId.append(" Finalizar visualización ")
    # Si no es la última página añadir botón para poder avanzar página
    if PageNum+1 < TotNumPages: 
        ListButtId.append(" Av.Pag ")
    # Texto de la página.
    for num, filename in Page:
        TextMenu += "%d) %s\n" % (num+1, os.path.basename(filename) )
    return PopupASK(TextMenu, ListButtId, \
        Title="Lista de ficheros  <Página (%d/%d)>" % (PageNum+1, TotNumPages)) 


################################################################################################################
# Obtiene la lista de ficheros visibles contenidos en un directorio
################################################################################################################
def GetList_Num_Filenames(dir, extension, readable, sort):
    '''
    Obtiene la lista de ficheros visibles contenidos en un directorio que cumplan con los parámetros indicados
    la retorna en forama de lista completa y lista fragmentada en páginas.

    Parámetros:
    -----------
        dir (str):
            Directorio que contiene los ficheros.

        extension (str): (Por ejemplo: '.txt' o '.dat',... etc.)
            Extension de los ficheros que deseamos escanear.

        readable (bool):
            Si vale True solo consideraremos los que son legibles.

        sort:
            Tipo de ordenacion deseado.

    Retorno:
    --------
        (List_Num_Filenames, listPagesFilenames) (tuple): (Es una tupla con dos listas que contienen información
        redundante. Retornamos la lista completa y la lista fragmentada en páginas.

            List_Num_Filenames (list): (Es una lista de tuplas (num, NameFile).)
                En las tuplas 'Num' es el número de la posición en la lista del fichero creado incrementando un 
                contador del número de fichero,  y 'nameFile') es el nombre del fichero con su path completo). 
                Representa la lista completa de ficheros que deseamos mostrar para seleccionar uno de ellos por su 
                número. Como la lista puede ser larga dividiremos la información de este diccionario en páginas.
            listPagesFilenames (list): (Es una lista de listas de tuplas.)
                La misma lista que antes pero paginada con los datos necesarios para poder ser visualizada.
    '''

    ## seleccion de ficheros dentro del directorio indicado
    files = os.listdir(dir)
    print(files)
    #  Filtramos por tipo de fichero == fichero y por extensión.
    for n in range(len(files) - 1, -1, -1):
        print(files[n])
        files[n]= os.path.join(dir, files[n]) # Añadimos el directorio al nombre del fichero
        Eliminar=False #
        if not os.path.isfile(files[n]):
            #print("TRAZA  ", files[n], " Eliminar porque no es un fichero")
            Eliminar=True
        if os.path.basename(files[n]).startswith('.'):
            #print("TRAZA  ", files[n], " Eliminar porque no es un fichero visible")
            Eliminar=True
        if extension!=None: # Si nos viene dada una extensión como obligatoria ...
            root, extFile=os.path.splitext(files[n])
            if extFile!= extension: # ... y si no coincide la extensión
                #print("TRAZA  ", files[n], " Eliminar porque no tiene la extension '%s' != '%s' " % (extFile, extension) )
                Eliminar=True # 
        if Eliminar:
            del(files[n]) # borrar de la lista

    # Ordenación de la lista de ficheros
    if sort[0]=='n': # Ordenación Por Nombre
        if  sort[1]=='d':
            ReverseSort=False 
        elif sort[1]=='a':
            ReverseSort=True
        else:
            raise Exception("El argumento sort vale'%s' pero solo admite: 'na', 'nd', 'da', dd' " % (sort))
        files.sort(reverse=ReverseSort)
    if sort[0]=='d': # Ordenación Por fecha de modificacion (Date)
        if  sort[1]=='d':
            ReverseSort=False 
        elif sort[1]=='a':
            ReverseSort=True
        else:
            raise Exception("El argumento sort vale'%s' pero solo admite: 'na', 'nd', 'da', dd' " % (sort))
        files.sort(reverse=ReverseSort, key=lambda x: os.path.getmtime(x)) 

    List_Num_Filenames=[]
    cont=0
    for fiName in files:
        List_Num_Filenames.append((cont, fiName))
        cont +=1

    ### Construir la estructura de páginas  
    NumLinesPerPag=15
    listPagesFilenames=[] # Lista de páginas donde cada página será un fragmento del diccionario List_Num_Filenames
    Pagina_actual = [] 
    for Num, FiName in List_Num_Filenames:
        Pagina_actual.append((Num, os.path.basename(FiName)))
        if len(Pagina_actual) == NumLinesPerPag: # Pagina actual Llena
            listPagesFilenames.append(Pagina_actual) # añadir la página a la lista de páginas
            Pagina_actual = [] # Nueva página
    if Pagina_actual: # Si hay elementos restantes en el último Pagina incompleto, agregarlos
        listPagesFilenames.append(Pagina_actual)
    return (List_Num_Filenames, listPagesFilenames)


################################################################################################################
# Retorna el nombre de fichero seleccionado de la lista de ficheros
################################################################################################################
def PopupSelectionFiles(dir='.', extension=None, readable=True, sort='nd', \
        Title="Seleccionar Fichero", FlagAlert="Blue"):

    '''
    Llama a la funcion que escanea el directorio que contiene los ficheros. Luego invoca a la función que
    puede presentar esa información en forma de menús por cada página de información, y tras obtener la tupla 
    seleccionada de la lista de ficheros, nos quedamos con el nombre del fichero y lo retornamos 

    Parámetros:
    -----------
        dir (str):
            Directorio que contiene los ficheros.

        extension (str): (Por ejemplo: '.txt' o '.dat',... etc.)
            Extension de los ficheros que deseamos escanear.

        readable (bool):
            Si vale True solo consideraremos los que son legibles.

        sort:
            Tipo de ordenacion deseado.

    Retorno:
    --------
        (str):
            Retorna el nombre del fichero incluyendo el path con el directorio que lo contiene.
    '''
    TestIni()
    # Obtenemos la lista de ficheros numerados y su versión paginada
    List_Num_Filenames, listPagesFilenames=GetList_Num_Filenames(dir, extension, readable, sort)
    ### Bucle de procesado de páginas de ficheros
    PageNum=0
    while True:
        Page=listPagesFilenames[PageNum]
        ret=MenuSelectFiles(Page, PageNum, len(listPagesFilenames))
        if ret==" Cancelar ":
            return ""
        elif ret==" Re.Pag ":
            PageNum -=1
            continue
        elif ret==" Av.Pag ":
            PageNum +=1
            continue
        else: # NumFi contendrá el numero del fichero seleccionado
            Num, fiName = List_Num_Filenames[int(ret)-1] # (OJO! el primer fichero es el List_Num_Filenames[0])
            return fiName # Solo retornamos el nombre del fichero que incluye el directorio

################################################################################################################
# Es parecida a la anterior, pero no selecciona ficheros. Solo permite visualizar la lista paginada de ficheros.
################################################################################################################
def PopupScanFiles( dir='.', extension=None, readable=True, sort='nd', \
        Title="Seleccionar Fichero", FlagAlert="Blue"):
    '''
    Es parecida a la anterior, pero no selecciona ficheros. Solo permite visualizar la lista paginada de ficheros.
    Parámetros:
    -----------
        dir (str):
            Directorio que contiene los ficheros.

        extension (str): (Por ejemplo: '.txt' o '.dat',... etc.)
            Extension de los ficheros que deseamos escanear.

        readable (bool):
            Si vale True solo consideraremos los que son legibles.

        sort:
            Tipo de ordenacion deseado.

    Retorno:
    --------
        (No retorna nada)

    '''
    TestIni()
    List_Num_Filenames, listPagesFilenames=GetList_Num_Filenames(dir, extension, readable, sort)
    ### Bucle de procesado de páginas de ficheros
    PageNum=0
    while True:
        Page=listPagesFilenames[PageNum]
        ret=MenuScanFiles(Page, PageNum, len(listPagesFilenames))
        if ret==" Re.Pag ":
            PageNum -=1
            continue
        elif ret==" Finalizar visualización ":
            return # -->  retornamos
        elif ret==" Av.Pag ":
            PageNum +=1
            continue

   
#################################################################################################################
### Comienza la parte privada del módulo. Usar funciones que aparecen a continuación, podrían verse afectadas ###
### por cambios de versión dentro del módulo.                                                                 ###
#################################################################################################################

################################################################################################################
# Tipo predefinido de Popup para mostrar errores, advertencias e informacion. 
# De forma automática solo incluirá un botón que permita continuar.
################################################################################################################
def PopupMens_ERR_WARN_NOTICE_INFO( Message, Title, FlagAlert):
    TestIni()
    # "Green", "Yellow", "Orange", "Red, "Blue"
    # Valores por defecto para Title para nivel de alerta "Información" "Aviso" "Advertencia", "Error"
    ppdw=PopupDialogWindow( Title, Message, ListIdButt=["   Continuar   "], FlagAlert=FlagAlert )
    ppdw.Run() # No es necesario retornar nada porque hay un solo botón de confirmación.

############################################################################### 
# Tipo predefinido de Popup para mostrar
# De forma automática solo incluirá un botón que permita continuar.
############################################################################### 
def PopupHELP(
    md_text,
    IdButt="   Cerrar ayuda   ",
    Title="Ayuda",
    FlagAlert="Blue",
    *,
    interactive_size=(800, 480),
    W_Margin=None,
    H_Margin=None,
    BorderThikness=None,
    BorderColor=None,
    # Opcionales para el visor (helpview.help_core.HelpViewer)
    title=None,                 # si no se pasa, usa Title
    style_variant="formal",
    style_json_path=None,
    fonts_dir=None,
    help_font_file=None,
    help_code_font_file=None,
    kernel_bg=None,
    wheel_step=48,
    visual_indent_px=24,
):
    """
    Lanza una popup modal de ayuda con contenido Markdown.
    Requiere haber llamado antes a IniPopupDialog(display, style_id).

    Parámetros principales:
        md_text (str): Markdown reducido a renderizar.
        interactive_size (w,h): tamaño lógico del área de ayuda (kernel).
        IdButt (str): etiqueta del único botón (por defecto “Cerrar ayuda”).
        Title (str): título del popup; FlagAlert (str): color de cabecera/pie.

    Opcionales del visor de ayuda:
        style_variant, style_json_path, fonts_dir, help_font_file, help_code_font_file,
        kernel_bg, wheel_step, visual_indent_px, title (interno del visor).
    """
    # Import local para no crear dependencia dura cuando no se usa ayuda
    try:
        _ = HelpPPsct  # definida en este mismo módulo
    except NameError:
        raise RuntimeError("HelpPPsct no está disponible en este módulo.")

    # Valores por defecto tomados del estilo activo si no se indican
    Wm = ST.get("SF_SectW_Margin", 20) if W_Margin is None else W_Margin
    Hm = ST.get("SF_SectH_Margin", 12) if H_Margin is None else H_Margin
    Bth = ST.get("Krn_BorderThikness", 2) if BorderThikness is None else BorderThikness
    Bco = tuple(ST.get("Krn_BorderColor", (0, 0, 0))) if BorderColor is None else BorderColor

    help_kernel = HelpPPsct(
        md_text=md_text,
        interactive_size=interactive_size,
        W_Margin=Wm,
        H_Margin=Hm,
        BorderThikness=Bth,
        BorderColor=Bco,
        # kwargs del visor:
        title=(title or Title),
        style_variant=style_variant,
        style_json_path=style_json_path,
        fonts_dir=fonts_dir,
        help_font_file=help_font_file,
        help_code_font_file=help_code_font_file,
        kernel_bg=kernel_bg,
        wheel_step=wheel_step,
        visual_indent_px=visual_indent_px)

    ppdw = PopupDialogWindow(
        help_kernel,
        [IdButt],
        Title=Title,
        FlagAlert=FlagAlert)
    return ppdw.Run()

############################################################################### 
# Obtiene el alto y el ancho en pixels de un texto con una o varias líneas
# usando la fuente del texto indicada y el porcentaje de separacion entre lineas.
############################################################################### 
def GetWidthHeigthText(Text, Font, PorcSepLines=130):
    """
    Text: Es una cadena de caracteres que puede tener saltos de linea.
    Font: Fuente con el tipo de letra y su tamaño.
    PorcSepLines: SepLines es el porcentaje de separación entre líneas que deberá 
    ser mayor que 100% para que no se amontonen unas líneas encima de otras. 
    El espacio habitual entre líneas de texto para que su lectura sea agradable 
    suele estar entre el 120% al 150% del tamaño de la fuente utilizada. Por ello
    usaremos por defecto el valor 130

    La funcion retornará la tupla (Width, Heigth) que será el ancho y alto 
    en pixels que va a ocupar todo el texto una vez renderizado y lo hará sin
    mostrar nada en pantalla.
    """
    NumLines=len(Text.splitlines())
    if NumLines==0:
        return 0,0
    elif NumLines==1:
        text_surface = Font.render(Text, True, (0, 0, 0))
        w= text_surface.get_width()
        h= text_surface.get_height()
        return w,h
    else: # Texto con varias lineas.
        maxW=0
        maxH=0
        Sep=PorcSepLines/100
        for line in Text.splitlines():
            text_surface = Font.render(line, True, (0, 0, 0))
            w= text_surface.get_width()
            h= text_surface.get_height()
            if w> maxW:
                maxW= w
            if h> maxH:
                maxH=h
            H=int (maxH+Sep)* NumLines
    # Retornamos el ancho y el alto de lo que ocupa el texto (No se consideran los márgenes)
    return maxW,  H
    # END *** def GetWidthHeigthText(Text, Font, PorcSepLines=130):


#####################################################################################################
# Dibujar un rectángulo con borde redondeado. Primero dibuja el fondo y luego el borde.
#####################################################################################################
def DrawRect(BgColor, BorderColor, Rect, BorderThikness, BorderRadius):
    pygame.draw.rect(gameDisplay, BgColor,     Rect, 0, BorderRadius)
    pygame.draw.rect(gameDisplay, BorderColor, Rect, BorderThikness, BorderRadius)

