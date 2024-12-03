import random

def inicializar_matriz(cant_filas:int, cant_columnas:int)->list:
    """crea una matriz 

    Args:
        cant_filas (int): cantidad de fila
        cant_columnas (int): camtodad de columnas

    Returns:
        list: matriz
    """
    matriz = []
    for _ in range(cant_filas):
        matriz += [[0] * cant_columnas]
    return matriz


def crear_bombas(cantidad:int,matriz:list) -> set:
    """crea una lista de bombas aleatorias 

    Args:
        cantidad (int): cantidad de bombas
        matriz (list): matriz
    """
    lista_bombas = set()
#  y fila , x columna
    while cantidad > len(lista_bombas):
        y = random.randint(0,len(matriz)-1) 
        x = random.randint(0,len(matriz[0])-1) 

        lista_bombas.add((y,x))

    return lista_bombas


def cargar_bomba(matriz:list, lista_bombas:set):
    """Coloca bombas en una matriz de juego basada en las posiciones especificadas

    Args:
        matriz (list): matriz
        lista_bombas (set):conjunto de tuplas `(y, x)` que representan las coordenadas de las bombas.
                            Cada tupla indica la fila (`y`) y la columna (`x`) donde se colocará una bomba
    """

    for y,x in lista_bombas:
        matriz[y][x] = -1

#                               Lista de seters
def detectar_bombas(matriz:list,lista_bombas:set):
    """Calcula el número de bombas adyacentes

    Args:
        matriz (list): matriz
        lista_bombas (set): conjunto de tuplas que representa la pocicion de las bombas
    """
    filas = len(matriz)
    columnas = len(matriz[0])
    
    for y,x in lista_bombas:
        
        direcciones = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0), (1, 1)
            ]
        
        
        for dy, dx in direcciones:
            ny, nx = y + dy, x + dx
            # Verificar que no salga de los límites
            # evitamos index error sin try except

            if 0 <= ny < filas and 0 <= nx < columnas:
                # Incrementar solo si no es una bomba
                
                if matriz[ny][nx] != -1:
                    matriz[ny][nx] += 1



# def parseo_dato(matriz):
#     for y in range(len(matriz)):
#         for x in range(len(matriz)):
#             matriz[y][x] = str(matriz[y][x])


def mostrar_matriz(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(f'{matriz[i][j]:^1}',end=" ")
        print(" ")

