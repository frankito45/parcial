import pygame
from botones import *
from cargar_archivo import *
from estados import banderas,boton_clicado


def tabla_puntuaciones(screen:pygame.Surface,lista_puntaje:list,aux:int):
    """
    Renderiza la tabla de jugadores
    screen:superficie donde lo dibuja 
    lista_puntaje:lista de puntuaciones
    aux:desde donde empieza a iterar la lista
    """

    lista_puntaje.sort(key= lambda x:x['puntuacion'],reverse=True)
    pading = 20
    encabezados = FUENTE_ENCABEZADO.render("-NOMBRE-                       -PUNTOS-",1,'white')
    
    for i in range(aux,len(lista_puntaje)):
        pading += 100
        fuentex = FUENTE_2.render(f'{lista_puntaje[i]['nombre']}',True,'white')
        fuentex2 = FUENTE_2.render(f'{lista_puntaje[i]['puntuacion']}',True,'white')
        screen.blit(fuentex,(100,pading))
        screen.blit(fuentex2,(700,pading))
    screen.blit(encabezados,(90,10))

def ver_puntajes(screen:pygame.Surface):
    """
    obtiene los valores de puntuacion e inicializa la tabla de puntuaciones,
    Arg:
        screen:superficie donde empiza a renderizar
    """
    boton_volver = crear_boton((1000,550,150,37),(20,149,216),'Volver',(123,1,123))
    try:
        lista_score = cargar_json("Player score\player_score.json")
    except:
        guardar_archivo_json("Player score\player_score.json",[])

    lista_score = cargar_json("Player score\player_score.json")

    aux = 0
    flag = True
    while flag:
        screen.blit(FONDO_PUNTAJE,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                flag = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if boton_volver['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                    flag = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 and aux < len(lista_score):
                aux += 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 and   aux  > 0:
                aux -=1

        tabla_puntuaciones(screen,lista_score,aux)

        animacion_boton(screen,boton_volver,FUENTE_1,'boton_rec',boton_volver['color'],20,("white"))
        pygame.display.update()
    menu(screen)

def guardar_puntuacion(screen:pygame.Surface,puntos_en_pantalla:pygame.Surface,die:bool,cont_puntos:int):
    """
    Maneja la pantalla de final de juego, permitiendo al jugador ingresar su nombre
    y guardar la puntuación obtenida.

    Args:
        screen (pygame.Surface): superficie donde se dubujan los elementos
        puntos_en_pantalla (pygame.Surface):superficie donde contiene los puntos 
        die (bool): indica si el jugador perdio o gano
        cont_puntos (int): la puntuacion final del jugador
    """
    WIN_MUSIC.set_volume(0.07)
    LOSE_MUSIC.set_volume(0.07)
    
    prueba = FUENTE_3.render("Ingrese su Nombre",0,"black")
    nombre_ingresado = ""
    flag = True

    while flag:
        
        if die == True:
            LOSE_MUSIC.play()
            screen.blit(LOSE_IMAGE,(0,0))
            screen.blit(prueba,(460,280))

        else:
            WIN_MUSIC.play()
            screen.blit(WIN_IMAGE,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    cargar_archivo('Player score/player_score.json',{"nombre":nombre_ingresado,"puntuacion":cont_puntos})
                    flag = False
                    LOSE_MUSIC.stop()
                    niveles(screen)
                elif event.key == pygame.K_BACKSPACE:
                        nombre_ingresado = nombre_ingresado[0:-1]                                      
                else:   #no supera la cantidad de 13 caracteres
                    if len(nombre_ingresado) < 13:
                        nombre_ingresado += event.unicode
            
        nombre_usuario = FUENTE_2.render(nombre_ingresado,True,"black")  
        
        screen.blit(puntos_en_pantalla,(100,100))
        screen.blit(nombre_usuario,(450,350))


        pygame.display.update()

def verificar_victoria(juego)->bool:
    """Ganas de forma predeterminada, mientras que todos los botones que NO sean -1 esten en False
    aun no ganaste

    Args:
        juego (_type_): Lista de botones de matriz

    Returns:
        _type_: True si ganaste, False si un no lo hiciste
    """
    retorno = True
    for boton in juego:
        if boton['texto'] != "-1" and not boton['clicado']:
            retorno = False
    return retorno

def actualizar_tiempo(cont_min:int, cont_seg:int)->tuple:
    """suma 1 al cont_seg, si este llega a 60 se le suma 1 al cont_minutos

    Args:
        cont_min (_type_): contador de minutos
        cont_seg (_type_): Contadopr de segundos

    Returns:
        _type_: retorna los contadores cont_min, cont_seg
    """
    cont_seg += 1
    if cont_seg == 60:
        cont_min += 1
        cont_seg = 0
    return cont_min, cont_seg

def pausar_play_musica(botton_music,flag_musica:bool,musica) -> bool:
    """detiene o inicializa la musica del juego

    Args:
        botton_music (dict): boton de musica
        flag_musica (bool): determina si se reproduce la musica
        musica (_type_): cancion de reproducir o pausar

    Returns:
        bool:devuelve un boleano  
    """
    if botton_music['boton_rec'].collidepoint(pygame.mouse.get_pos()):
        if flag_musica:
            musica.play()
            botton_music['texto'] = 'Pause'
            flag_musica = False
        else:
            musica.stop()
            botton_music['texto'] = 'Play'
            flag_musica = True
    return flag_musica

def jugar(screen:pygame.Surface,dificultad:tuple):
    """
    maneja la pantalla de juego inicializando los botones dependiendo de la dificultad

    Args:
        screen (pygame.Surface): superficies a donde dibuja los elementos
        dificultad (tuple): tamaño de la matriz y cantidad de bombas
    """
    boton_reiniciar = crear_boton((50,650,150,37),(20,149,216),'Reiniciar',(123,1,123))
    boton_volver = crear_boton((1000,650,150,37),(20,149,216),'Volver',(123,1,123))
    boton_musica = crear_boton((50,100,100,37),(20,149,216),'Play',(123,1,123))
    
    fuente_matriz = pygame.font.SysFont('arial black',24)
    musica_pausada = False

    matriz = tablero(dificultad)
    lista_bomba = crear_bombas(dificultad[2],matriz)
    cargar_bomba(matriz,lista_bomba)
    detectar_bombas(matriz,lista_bomba)
    
    juego = crear_botones_matriz(matriz)
    
    #------------------------------------------------
    mi_evento = pygame.USEREVENT + 1
    un_segundo = 1000
    pygame.time.set_timer(mi_evento,un_segundo)
    cont_seg = 0
    cont_min = 0
    contador_puntos = 0
    
    you_die = False
    JUGAR_MUSIC.play()
    JUGAR_MUSIC.set_volume(0.05)
    
    #------------------------------------------------
    
    flag = True
    while flag:
        screen.blit(FONDO_JUGAR,(0,0))
        
        relog_contador = FUENTE_2.render(f"Time: {cont_min:02d} : {cont_seg:02d}",True,"Red","black")
        puntos_en_pantalla = FUENTE_2.render(f"Score: {contador_puntos:03d}",True,"Red","black")
        
        for boton in juego:
            animacion_cacilla(screen,boton,fuente_matriz,'boton_rec',(150, 150, 150),0,'white')
            if boton['marcado']:
                screen.blit(BANDERA, (boton['boton_rec'].x,boton['boton_rec'].y))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()
            
            if event.type == mi_evento:
                cont_min,cont_seg = actualizar_tiempo(cont_min,cont_seg)
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                you_die,flag,contador_puntos = boton_clicado(juego,JUGAR_MUSIC,contador_puntos,you_die,flag)
                
                if boton_reiniciar['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                    JUGAR_MUSIC.stop()
                    flag = False
                    jugar(screen,dificultad)
                
                if boton_volver['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                    JUGAR_MUSIC.stop()
                    flag = False
                    niveles(screen)

                        
                musica_pausada = pausar_play_musica(boton_musica,musica_pausada,JUGAR_MUSIC)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                banderas(juego)
            
            if verificar_victoria(juego):
                JUGAR_MUSIC.stop()
                flag = False
            
        
        screen.blit(relog_contador,(900,100))    
        screen.blit(puntos_en_pantalla,(200,100))
        animacion_boton(screen,boton_volver,FUENTE_1,'boton_rec',boton_volver['color'],20,("white"))
        animacion_boton(screen,boton_reiniciar,FUENTE_1,'boton_rec',boton_reiniciar['color'],20,("white"))
        
        animacion_boton(screen,boton_musica,FUENTE_1,'boton_rec',boton_musica['color'],20,("white"))
        pygame.display.update()
    guardar_puntuacion(screen,puntos_en_pantalla,you_die,contador_puntos)

def niveles(screen:pygame.Surface):
    """maneja la pantalla de niveles 

    Args:
        screen (pygame.Surface):  superficies a donde dibuja los elementos
    """

    boton_volver = crear_boton((1000,550,150,37),(20,149,216),'Volver',(123,1,123))
    boton_facil = crear_boton((570,150,150,37), ("white"), 'FACIL', (123,1,123))
    boton_medio = crear_boton((570,335,150,37), ("white"), 'MEDIO', (123,1,123))
    boton_dificil = crear_boton((570,540,150,37), ("white"), 'DIFICIL', (123,1,123))
    
    flag = True 
    while flag:
        screen.blit(FONDO_NIVELES,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                flag = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if boton_facil['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                    retorno = 8,8,10
                    jugar(screen,retorno)
                if boton_medio['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                    retorno = 16,16,40
                    jugar(screen,retorno)
                if boton_dificil['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                    retorno = 16,30,100
                    jugar(screen,retorno)
                if boton_volver['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                    flag = False
                    menu(screen)
        
        animacion_boton(screen,boton_facil,FUENTE_1,'boton_rec',boton_facil['color'],0,("black"))
        animacion_boton(screen,boton_medio,FUENTE_1,'boton_rec',boton_medio['color'],0,("black"))
        animacion_boton(screen,boton_dificil,FUENTE_1,'boton_rec',boton_dificil['color'],0,("black"))
        animacion_boton(screen,boton_volver,FUENTE_1,'boton_rec',boton_volver['color'],20,("white"))
        pygame.display.update()

def menu(screen:pygame.Surface):
    """maneja la pantalla de niveles

    Args:
        screen (pygame.Surface):  superficies a donde dibuja los elementos
    """
    boton_jugar = crear_boton((565,250,150,37), (20,149,216), 'Jugar', (123,1,123))
    boton_ver_puntajes = crear_boton((565,350,150,37), (20,149,216), 'Ver Puntaje', (123,1,123))
    boton_salir = crear_boton((565,450,150,37), (20,149,216), 'Salir', (123,1,123))

    MENU_MUSIC.play()
    MENU_MUSIC.set_volume(0.05)
    clock = pygame.time.Clock()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if boton_jugar['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                    MENU_MUSIC.stop()
                    niveles(screen)

                if boton_ver_puntajes['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                    run = False
                    MENU_MUSIC.stop()
                    ver_puntajes(screen)

                if boton_salir['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                    run = False

            screen.blit(IMAGEN_MENU,(0,0))
            animacion_boton(screen,boton_jugar,FUENTE_1,'boton_rec',boton_jugar['color'],20,("white"))
            animacion_boton(screen,boton_ver_puntajes,FUENTE_1,'boton_rec',boton_ver_puntajes['color'],20,("white"))
            animacion_boton(screen,boton_salir,FUENTE_1,'boton_rec',boton_salir['color'],20,("white"))
        
        # actualiza la pantalla
        pygame.display.flip()
        clock.tick(60)
    # Salgo de pygame
    pygame.quit()