import pygame
from botones import *
from cargar_archivo import *


def tabla_puntuaciones(screen,lista_puntaje:list,aux):
    lista_puntaje.sort(key= lambda x:x['puntuacion'],reverse=True)
    contador = 20
    encabezados = FUENTE_ENCABEZADO.render("-NOMBRE-                       -PUNTOS-",1,'white')
    
    for i in range(aux,len(lista_puntaje)):
        contador += 100

        
        fuentex = FUENTE_2.render(f'{lista_puntaje[i]['nombre']}',True,'white')
        fuentex2 = FUENTE_2.render(f'{lista_puntaje[i]['puntuacion']}',True,'white')
        screen.blit(fuentex,(100,contador))
        screen.blit(fuentex2,(700,contador))
    screen.blit(encabezados,(90,10))


def ver_puntajes(screen):
    fondo_puntaje = escalar_imagenes_fondo(f"{PATH}/Fondo_puntaje.png",SIZE_SCREEN)
    boton_volver = crear_boton((1000,550,150,37),(20,149,216),'Volver',(123,1,123))
    

    try:
        lista_score = cargar_json("Player score\player_score.json")
    except:
        guardar_archivo_json("Player score\player_score.json",[])

    lista_score = cargar_json("Player score\player_score.json")

    aux = 0
    flag = True
    while flag:
        screen.blit(fondo_puntaje,(0,0))
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


def guardar_puntuacion(screen,puntos_en_pantalla,die,cont_puntos):

    you_die_img = escalar_imagenes_fondo(f"{PATH}/you_die.png",SIZE_SCREEN)
    lose_music = pygame.mixer.Sound(f"{PATH}/Game Over.mp3")
    lose_music.set_volume(0.05)
    prueba = FUENTE_3.render("Ingrese su Nombre",0,"black")
    nombre_ingresado = ""
    flag = True

    while flag:
        
        if die == True:
            lose_music.play()
            screen.blit(you_die_img,(0,0))
            screen.blit(prueba,(460,280))

        else:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    cargar_archivo('Player score/player_score.json',{"nombre":nombre_ingresado,"puntuacion":cont_puntos})
                    flag = False
                    lose_music.stop()
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


def jugar(screen,dificultad):
    
    jugar_music = pygame.mixer.Sound(f"{PATH}/wolf_play.mp3")
    fondo_jugar = escalar_imagenes_fondo(f"{PATH}/imagen_fondo_jugar.png",SIZE_SCREEN)
    bandera = escalar_imagenes_fondo(f"{PATH}/bandera_mina.png",(20,20))
    
    boton_reiniciar = crear_boton((50,650,150,37),(20,149,216),'Reiniciar',(123,1,123))
    boton_volver = crear_boton((1000,650,150,37),(20,149,216),'Volver',(123,1,123))
    
    fuente_matriz = pygame.font.SysFont('arial black',24)
    
    matriz = tablero(dificultad)
    lista_bomba = crear_bombas(dificultad[2],matriz)
    cargar_bomba(matriz,lista_bomba)
    detectar_bombas(matriz,lista_bomba)
    if len(matriz) > 15:
        juego = crear_botones_matriz(matriz,270,150)
    else:
        juego = crear_botones_matriz(matriz,470,180)
    
    #------------------------------------------------
    mi_evento = pygame.USEREVENT + 1
    un_segundo = 1000
    pygame.time.set_timer(mi_evento,un_segundo)
    cont_seg = 0
    cont_min = 0

    
    contador_puntos = 0000
    
    you_die = False
    jugar_music.play()
    jugar_music.set_volume(0.05)
    
    #------------------------------------------------
    

    flag = True
    while flag:
        if you_die == False:
            screen.blit(fondo_jugar,(0,0))
            
            relog_contador = FUENTE_2.render(f"Tiempo: 0{cont_min} : {cont_seg}",True,"white","black")
            puntos_en_pantalla = FUENTE_2.render(f"Puntos: {contador_puntos}",True,"white","black")
            

            for boton in juego:
                animacion_cacilla(screen,boton,fuente_matriz,'boton_rec',(150, 150, 150),0,'white')
                if boton['marcado']:
                    screen.blit(bandera, (boton['boton_rec'].x,boton['boton_rec'].y))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    flag = False
                    pygame.quit()
                if event.type == mi_evento:
                        cont_seg += 1
                        if cont_seg  == 60:
                            cont_min += 1
                            cont_seg = 0
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for boton in juego:
                        if boton['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                            if not boton.get('clicado', False):
                                if not boton.get('marcado', False) : # si no fue clicado
                                    boton['evento'] = True  # Marcado como clik
                                    if boton['texto'] == "-1":
                                        jugar_music.stop()
                                        you_die = True
                                        flag = False
                                    else:
                                        contador_puntos += 1
                                        boton['clicado'] = True
                    
                    if boton_reiniciar['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                        jugar_music.stop()
                        flag = False
                        jugar(screen,dificultad)
                        
                    if boton_volver['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                        jugar_music.stop()
                        flag = False
                        niveles(screen)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    for boton in juego:
                        if boton['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                            if not boton.get('clicado', False):
                                if not boton.get('marcado', False):
                                    boton['marcado'] = True  # Marcar con signo de pregunta
                                else:
                                    boton['marcado'] = False

            

            
            screen.blit(relog_contador,(900,100))    
            screen.blit(puntos_en_pantalla,(200,100))
            animacion_boton(screen,boton_volver,FUENTE_1,'boton_rec',boton_volver['color'],20,("white"))
            animacion_boton(screen,boton_reiniciar,FUENTE_1,'boton_rec',boton_reiniciar['color'],20,("white"))
            
        pygame.display.update()
    guardar_puntuacion(screen,puntos_en_pantalla,you_die,contador_puntos)


def niveles(screen):
    
    fondo_niveles = escalar_imagenes_fondo(f"{PATH}/Fondo_selector_nivel.png",SIZE_SCREEN)
    boton_volver = crear_boton((1000,550,150,37),(20,149,216),'Volver',(123,1,123))
    boton_facil = crear_boton((570,150,150,37), ("white"), 'FACIL', (123,1,123))
    boton_medio = crear_boton((570,335,150,37), ("white"), 'MEDIO', (123,1,123))
    boton_dificil = crear_boton((570,540,150,37), ("white"), 'DIFICIL', (123,1,123))
    # boton_siguiente = crear_boton((950,500,250,37),(20,149,216),'EMPEZAR PARTIDA',(123,1,123))
    
    flag = True 
    while flag:
        screen.blit(fondo_niveles,(0,0))
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
                # if boton_siguiente['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                #     flag = False
                #     jugar(retorno)
        
        animacion_boton(screen,boton_facil,FUENTE_1,'boton_rec',boton_facil['color'],0,("black"))
        animacion_boton(screen,boton_medio,FUENTE_1,'boton_rec',boton_medio['color'],0,("black"))
        animacion_boton(screen,boton_dificil,FUENTE_1,'boton_rec',boton_dificil['color'],0,("black"))
        animacion_boton(screen,boton_volver,FUENTE_1,'boton_rec',boton_volver['color'],20,("white"))
        # animacion_boton(screen,boton_siguiente,FUENTE_1,'boton_rec',boton_volver['color'],20,("white"))
        pygame.display.update()


def menu(screen):
    fondo_main_menu = escalar_imagenes_fondo(f"{PATH}/Fondo_bordo.png",SIZE_SCREEN)
    boton_jugar = crear_boton((565,250,150,37), (20,149,216), 'Jugar', (123,1,123))
    boton_ver_puntajes = crear_boton((565,350,150,37), (20,149,216), 'Ver Puntaje', (123,1,123))
    boton_salir = crear_boton((565,450,150,37), (20,149,216), 'Salir', (123,1,123))
    
    menu_music = pygame.mixer.Sound(f"{PATH}/Toxicity.mp3")
    menu_music.play()
    menu_music.set_volume(0.05)
    clock = pygame.time.Clock()


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if boton_jugar['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                    menu_music.stop()
                    niveles(screen)

                if boton_ver_puntajes['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                    run = False
                    menu_music.stop()
                    ver_puntajes(screen)

                if boton_salir['boton_rec'].collidepoint(pygame.mouse.get_pos()):
                    run = False

            screen.blit(fondo_main_menu,(0,0))
            animacion_boton(screen,boton_jugar,FUENTE_1,'boton_rec',boton_jugar['color'],20,("white"))
            animacion_boton(screen,boton_ver_puntajes,FUENTE_1,'boton_rec',boton_ver_puntajes['color'],20,("white"))
            animacion_boton(screen,boton_salir,FUENTE_1,'boton_rec',boton_salir['color'],20,("white"))
        # actualiza la pantalla
        pygame.display.flip()

        clock.tick(60)
    # Salgo de pygame
    pygame.quit()