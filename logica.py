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


def crear_bombas(cantidad,matriz):
    """crea una lista de bombas aleatorias 

    Args:
        cantidad (int): cantidad de bomvas
        matriz (list): matriz
    """
    lista_bombas = set()
#  y fila , x columna
    while cantidad > len(lista_bombas):
        y = random.randint(0,len(matriz)-1) 
        x = random.randint(0,len(matriz[0])-1) 

        lista_bombas.add((y,x))

    return lista_bombas


def cargar_bomba(matriz, lista_bombas):
    for y,x in lista_bombas:
        matriz[y][x] = -1

#                               Lista de seters
def detectar_bombas(matriz,lista_bombas):
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



def parseo_dato(matriz):
    for y in range(len(matriz)):
        for x in range(len(matriz)):
            matriz[y][x] = str(matriz[y][x])


def mostrar_matriz(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(f'{matriz[i][j]:^1}',end=" ")
        print(" ")

