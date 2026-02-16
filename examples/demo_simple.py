# examples/demo_simple.py
# Descripción breve: Muestra un mensaje. (Prueba básica de Popup_Dialog. Admite elección de estilo)
# Orden tutorial: 1.1

import pygame
import time, os

from popups_dialog_gui.Popup_Dialog import IniPopupDialog, PopupNOTICE

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

Pulse el botón.""" , IdButt=" Finalizar " )
time.sleep(1.5)


