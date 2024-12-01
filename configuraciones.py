import pygame

# resolucion de pantalla
pygame.init()
PANTALLA_ANCHO = 1280
PANTALLA_LARGO = 720

SIZE_SCREEN = PANTALLA_ANCHO,PANTALLA_LARGO
SCREEN = pygame.display.set_mode(SIZE_SCREEN)

PATH = 'assets'
# fuentes 
FUENTE_1 = pygame.font.Font(f"{PATH}/fuente_texto.otf",25)

FUENTE_2 = pygame.font.SysFont("Arial black",25)
FUENTE_3 = pygame.font.Font(f"{PATH}/fuente_texto.otf",40)
FUENTE_ENCABEZADO = pygame.font.SysFont("Arial black",40)
# FUENTE_8_BIT = pygame.font.Font(f"{PATH}/",25

