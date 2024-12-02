import pygame

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
            if not boton.get('clicado', False):
                if not boton.get('marcado', False):
                    boton['marcado'] = True  # Marcar con signo de pregunta
                else:
                    boton['marcado'] = False

# def obtener_resultado(win):
#     if win == False:
#         lose_music.play()
#         screen.blit(lose_img,(0,0))
#         screen.blit(prueba,(460,280))

#     else:
#         pass