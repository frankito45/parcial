import pygame
# from configuraciones import JUGAR_MUSIC

def escalar_imagenes_fondo (direc_imagen:str,tamanio:tuple):
    """escala la imagen sugun el tamaño dado 

    Args:
        direc_imagen (str): directorio de la imagen
        tamanio (tuple): tapaño a escalar

    Returns:
        superficie 
    """    
    imagen = pygame.image.load(direc_imagen)
    imagen = pygame.transform.scale(imagen,(tamanio))
    return imagen

def banderas(casillas:list):
    for boton in casillas:
        if boton['boton_rec'].collidepoint(pygame.mouse.get_pos()):
            print(boton)
            if boton['clicado'] == False:
                if boton['marcado'] == False:
                    boton['marcado'] = True
                else:
                    boton['marcado'] = False

