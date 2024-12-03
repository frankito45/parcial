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
    """determina si el boton esta clicado,en caso de no estarlo marcado paso true,
    en caso de estarlo pasa a false

    Args:
        casillas (list): lista de tuplas
    """
    for boton in casillas:
        if boton['boton_rec'].collidepoint(pygame.mouse.get_pos()):
            print(boton)
            if boton['clicado'] == False:
                if boton['marcado'] == False:
                    boton['marcado'] = True
                else:
                    boton['marcado'] = False

def boton_clicado(juego:list,music_stop:pygame.mixer.Sound,cont_puntos:int,flag1:bool,flag2:bool)->tuple:
    """Verifica e interactúa con los botones en el juego según la posición del mouse y su estado actual.

    Args:
        juego (list): lista de botones
        music_stop (pygame.mixer.Sound): detiene la musica
        cont_puntos (int): Contador de puntos que se incrementará si se clica en un botón válido.
        flag1 (bool): cambia las banderas
        flag2 (bool): cambia las banderas

    Returns:
        tuple: _description_
    """
    for boton in juego:
                    if boton['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                        if boton['clicado'] == False:
                            if boton['marcado'] == False: # si no fue clicado
                                boton['evento'] = True  # Marcado como clik
                                if boton['texto'] == "-1":
                                    music_stop.stop()
                                    flag1 = True
                                    flag2 = False
                                else:
                                    cont_puntos += 1
                                    boton['clicado'] = True
    return flag1,flag2,cont_puntos