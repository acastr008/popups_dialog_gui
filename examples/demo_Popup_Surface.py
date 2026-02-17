# examples/demo_Popup_Surface.py
# Descripción breve: Esta demo es un ejemplo muy sencillo de demostración del funcionamiento de SurfacePPsct
# Orden tutorial: 2.1

import pygame
import time
from popups_dialog_gui.Popup_Dialog import PopupDialogWindow, IniPopupDialog, SurfacePPsct

def SampleSurface(w, h, Title):
    # Crear superficie con fondo azul oscuro y un círculo naranja
    AZUL    = (0, 0, 200)
    NARANJA = (255, 140, 0) 
    NEGRO   = (0,0,0)
    superficie = pygame.Surface((w,h))
    superficie.fill(AZUL) # Fondo azul
    marginW= w//20
    marginH= h//20
    pygame.draw.ellipse(superficie, NARANJA, (marginW, marginH, w-(marginW*2), h-(marginH*2) ) )
    letra = pygame.font.SysFont("Arial", w//15)
    text_surface = letra.render(f"{Title} ({w}x{h})", True, NEGRO, NARANJA )
    text_rect = text_surface.get_rect() # Obtener el rectángulo que contiene el texto
    text_rect.center = (w // 2, h // 2) # Centrar el rectángulo en la pantalla
    superficie.blit(text_surface, text_rect)
    return superficie


pygame.init()
ancho, alto = 800, 800
MainDisplay = pygame.display.set_mode((ancho, alto))
MainDisplay.fill((30, 30, 30))
pygame.display.set_caption("2.1) demo_Popup_Surface.py")
pygame.display.flip()
time.sleep(1)

IniPopupDialog(MainDisplay, "playful_childlike")

lista=[ 
    (700,200, " Imagen 01 "),
    (200,600, " Imagen 02 "),
    (600,600, " Imagen 03 ")
  ]

for w,h,tit in lista: 
    superficie= SampleSurface(w,h, tit)
    popup = PopupDialogWindow(
        superficie,
        ["Salir"],
        Title="<<<<< " + tit + " >>>>>",
        FlagAlert="Blue"  # Debe existir en tu Style (evita "None")
    )
    respuesta = popup.Run()

pygame.quit()
