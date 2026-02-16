# demos/demo_Popup_Dialog.py
from __future__ import annotations

# Descripción breve: Ofrece un amplio menú de demos de Popup_Dialog (salvo las que usan contenidos interactivos) 
# Orden tutorial: 1.3

import pygame
import time, os
from pathlib import Path
from typing import Union

from popups_dialog_gui.Popup_Dialog import IniPopupDialog, PopupNOTICE, PopupASK, PopupERR, PopupWARN, PopupINFO, \
        PopupScanFiles, PopupSelectionFiles, GetStyleDict
from popups_dialog_gui.asset_locator import resolve_asset_layout

#####################################################################################################################
def generar_99_ficheros():
    ruta = '/tmp/' # Ruta donde se guardarán los ficheros
    for i in range(1, 100): # Iterar sobre el rango de 1 a 100 (99 ficheros)
        nombre_fichero = f'Fich{i:03d}.txt'                 # Formatear el número para obtener el nombre del fichero
        ruta_fichero = os.path.join(ruta, nombre_fichero)   # Ruta completa del fichero
        with open(ruta_fichero, 'w') as f:                  # Crear el fichero vacío
            f.write(f'Contenido del {nombre_fichero}')


#####################################################################################################################
def abbreviate_path_left_ellipsis(
    path_value: Union[str, Path],
    max_len: int = 45,
    right_to_left_ratio: float = 2.0,
    replace_home_with_tilde: bool = True,
    min_left: int = 8,
    min_right: int = 16,
) -> str:
    """
    Devuelve una versión abreviada de un path para mostrar en UI y lo hace con una elipsis asimétrica,
    es decir descentrada a la izquierda.  Ejemplo:
        PathFonts = str(layout.fonts_dir)  # absoluto para lógica
        PathFonts_UI = abbreviate_path_left_ellipsis( PathFonts,
            max_len=45, right_to_left_ratio=2.0,  # derecha = 2x izquierda)
        MenuPrincipal = f"... '{PathFonts_UI}' ..."

    Criterio:
    - Si replace_home_with_tilde=True y el path está bajo HOME, sustituye HOME por '~'.
    - Si la longitud excede max_len, aplica elipsis asimétrica: conserva una parte izquierda
      y una parte derecha, donde la derecha es más larga (right_to_left_ratio).

    Parámetros:
        path_value: Ruta (str o Path).
        max_len: Longitud máxima de salida (incluyendo '...').
        right_to_left_ratio: Relación derecha/izquierda. Ej.: 2.0 => derecha doble.
        replace_home_with_tilde: Sustituye HOME por '~' cuando procede.
        min_left: Mínimo de caracteres a conservar a la izquierda.
        min_right: Mínimo de caracteres a conservar a la derecha.

    Retorna:
        Cadena abreviada (o el path original si no excede max_len).
    """
    path_obj = Path(path_value).expanduser()
    pretty_text = str(path_obj)

    if replace_home_with_tilde:
        home_dir = Path.home()
        try:
            relative_to_home = path_obj.relative_to(home_dir)
            pretty_text = str(Path("~") / relative_to_home)
        except ValueError:
            pass

    if len(pretty_text) <= max_len:
        return pretty_text

    ellipsis = "..."
    if max_len <= len(ellipsis) + 2:
        # Caso extremo: no hay espacio real; devolvemos una forma mínima segura.
        return ellipsis[:max_len]

    available = max_len - len(ellipsis)

    # Reparto asimétrico: right = ratio * left  => left + right = available
    left = int(round(available / (1.0 + right_to_left_ratio)))
    right = available - left

    # Garantizar mínimos, ajustando sin pasarnos del disponible
    left = max(min_left, left)
    right = max(min_right, right)

    if left + right > available:
        # Si los mínimos no caben, prioriza conservar la derecha (más informativa)
        right = min(available - 1, right)
        left = available - right

        # Si aún así left queda en 0 o negativo, fuerza al menos 1 carácter a la izquierda
        if left < 1:
            left = 1
            right = available - left

    return f"{pretty_text[:left]}{ellipsis}{pretty_text[-right:]}"




################################################################################################################
###########################################   M  A  I  N  ######################################################
################################################################################################################
estilo=None
while not estilo:
    print("""

Puede elegir el estilo de visualizción.  Seleccione una opción.
    1) Estilo 'playful_childlike'   (Para juegos infantiles)
    2) Estilo 'formal'              (para otros programas más serios)
""")
    estilo=input("Elija el número de la opción ('1' o '2'): ")
    if (estilo == '1'):
        estilo='playful_childlike'
    elif (estilo == '2'):
        estilo='formal'
    else:
        estilo == None

pygame.init() # Inicializar Pygame
ventana_ancho = 1500 # Configuración de la ventana principal de pygame
ventana_alto = 800
MainDisplay = pygame.display.set_mode((ventana_ancho, ventana_alto)) 
print(">>>", MainDisplay.get_size())

# - - - - - - - - - - - INICIALIZAVION DEL MÓDULO  - - - - - - - - - - - #

IniPopupDialog(MainDisplay, estilo) # Inicializamos el módulo pasando la ventana principal de Pygame y el estilo 

print("TRAZA  (main) "+'>'*23, MainDisplay)
MainDisplay.fill((170,170,170))
pygame.draw.circle(MainDisplay, "Blue", (700,400), 100 )
pygame.draw.circle(MainDisplay, "Yellow", (700,600), 170 )
pygame.draw.circle(MainDisplay, "Red", (500,200), 270 )
pygame.draw.circle(MainDisplay, "Green", (1200,100), 100 )
pygame.draw.circle(MainDisplay, "Orange", (1200,600), 300 )
pygame.draw.circle(MainDisplay, "White", (150,150), 150 )
pygame.draw.circle(MainDisplay, "Black", (1000,300), 170 )
pygame.display.flip()
time.sleep(1.5)
PopupNOTICE( f"""
Ha elegido probar la demo usando
el estilo '{estilo}'.

La demo va a empezar.
Pulse el botón.""" , IdButt=" Comenzar " )
time.sleep(1)

# Mensaje estrecho con bastantes lineas
Ejemplo1="""    
linea
linea
linea
linea
linea
linea
linea
linea
linea
linea
linea
linea
"""

# Mensaje ancho con pocas lineas
Ejemplo2="""
Linea bastante mas larga que el título para verificar la anchura de la ventana
Linea bastante mas larga que el título para verificar la anchura de la ventana
Linea bastante mas larga que el título para verificar la anchura de la ventana
"""

layout = resolve_asset_layout()
PathFonts = layout.fonts_dir
PathFonts_UI = abbreviate_path_left_ellipsis(PathFonts)

MenuPrincipal=f"""
Este es un primer ejemplo del módulo Popup_Dialog y lo usamos para mostrar un menú principal de
la Demo de este módulo. Para ello basta incluir una serie de opciones numeradas acompañadas de 
los botones adecuados y plantear la "pregunta" con PopupASK(). Observe que al igual que la opción 
[5], un menú puede ser tratado como una pregunta. (Hemos personalizado el título de la pregunta).

En esta demo usaremos la respuesta para mostrarla en una PopupINFO(). Observe que las ventanas
popup aparecen centradas y con el tamaño optimizado para su contenido. Observe que cada ventana
popup termina con el cierre de la misma, por lo que no es posible apilarlas unas encima de otras.

[1] PopupERR() (Mostrar un error)
[2] PopupWARN() (Mostrar una advertencia importante)
[3] PopupNOTICE() (Mostrar un aviso)
[4] PopupINFO() (Mostrar una información)
[5] PopupASK() (Mostrar una pregunta)
[6] PopupScanFiles() (Escanear ficheros '*.ttf' del directorio '{PathFonts_UI}') 
[7] PopupSelectionFiles() (Seleccionar un fichero '*.txt' del directorio '/tmp')"""
EndDemo=" * Terminar * "
generar_99_ficheros() # Genera 88 ficheros en /tmp para la demo de selccion de ficheros
while True:
    ret=PopupASK( MenuPrincipal, ["1","2","3","4","5","6", "7", EndDemo], \
        Title="Menú de la demo para el módulo Popup_Dialog")
    if ret=="1":
        PopupERR( Ejemplo2)
    elif ret=="2":
        PopupWARN( Ejemplo1)
    elif ret=="3":
        PopupNOTICE( Ejemplo1)
    elif ret=="4":
        PopupINFO( Ejemplo2)
    elif ret=="5":
        ret=PopupASK( Ejemplo1, [" Confirmar ", " Abortar ", " Reintentar "])
        PopupNOTICE( "Usted pulsó -->"+ret, Title="Valor retornado")
    elif ret=="6":
        PopupScanFiles( dir=PathFonts, extension='.ttf')
    elif ret=="7":
        ret=PopupSelectionFiles( dir='/tmp', extension='.txt')
        if ret=='':
            PopupNOTICE( "Usted ha cancelado la selección de ficheros.\n"+
                "Lamentamos profundamente que no encontrara nada que le sirviera.", Title="Valor retornado.")
        else:
            PopupNOTICE( "\nUsted pulsó -->"+ret+\
                "\n\nRetornamos el nombre del fichero junto al directorio\n"+\
                "para poder abrirlo y acceder a su información.", Title="Valor retornado.")
    else:
        break
print('<'*33, ret, '>'*33)
PopupNOTICE( "\nFin demo.\nEsto es todo.\n", IdButt=" Finalizar " )
time.sleep(1.5)

