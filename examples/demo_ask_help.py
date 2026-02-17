# examples/demo_ask_help.py
# Descripción breve: Muestra un mensaje, ofrece ayuda y solicita una respuesta. (Prueba básica de Popup_Dialog.)
# Orden tutorial: 1.2

import pygame
import time, os

from help_core_pygame import ShowHelpOverlay
from popups_dialog_gui.Popup_Dialog import IniPopupDialog, PopupNOTICE, PopupASK

def Ayuda(main_display):
    MensAyuda="""
# Ayuda del programa
Esta es una demostración de como
usar un sistema de ayuda básico
usando popups_dialogs_gui.
**Importante:**
El mensaje de ayuada ha de usar
el formato ***Markdown***

## Ventajas
Esto permite:
- Redactar el mensaje de ayuda con cualquier editor de texto.
- Dar estructura al mensaje. (Listas, párrafos, etc.)
- Destacar partes del mensaje.
- Darle un aspecto más profesional a la ayuda.
- etc. Todo sin complicaciones.

Para salir de la ayuda pulse la tecla <ESC>
"""
    # Guardar el frame actual para poder restaurarlo al salir del overlay.
    # (ShowHelpOverlay es modal y el último frame del overlay puede quedarse en pantalla.)
    frozen_frame = main_display.copy()
    ShowHelpOverlay(main_display, MensAyuda, title="Ayuda")
    main_display.blit(frozen_frame, (0, 0)) # Recuperar el frame previo a mostrar la ayuda.
    pygame.display.flip()



################################################################################################################
###########################################   M  A  I  N  ######################################################
################################################################################################################

pygame.init() # Inicializar Pygame
ventana_ancho = 1500 # Configuración de la ventana principal de pygame
ventana_alto = 800
MainDisplay = pygame.display.set_mode((ventana_ancho, ventana_alto)) 
pygame.display.set_caption("1.2) demo_ask_help.py")

print(">>>", MainDisplay.get_size())

# - - - - - - - - - - - INICIALIZAVION DEL MÓDULO  - - - - - - - - - - - #

IniPopupDialog(MainDisplay, 'playful_childlike') # Inicializamos el módulo pasando la ventana principal de Pygame y el eestilo 'playful_childlike'
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

cont=0
mensaje="""
Esta demo demostrará como funciona PopupASK() y
como podemos añadir una pantalla de ayuda.
"""
while True:
    ret=PopupASK( mensaje, [" Confirmar ", " Abortar ", " Reintentar ", " Ayuda "])
    if ret==" Ayuda ":
        Ayuda(MainDisplay)
    elif ret==" Reintentar ":
        cont=cont+1
        PopupNOTICE( "Reintente de nuevo", Title=f"Reintento {cont}")
        pass
    elif ret==" Confirmar " or ret== " Abortar ":
        PopupNOTICE( "Usted pulsó --> '"+ret+"'", Title="Valor retornado")
        break
    else:
        break
