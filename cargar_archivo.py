import json
def guardar_archivo_json(ruta:str, dato:any):
    """Guarda el archivo dado en parametro "dato" en la direccion de carpeta "ruta"

    Args:
        ruta (str): ruta a donde guardar el dato
        dato (any): dato a guardar
    """
    with open(ruta,"w") as archivo:
        json.dump(dato,archivo,indent=2)


def cargar_json(ruta:str)->list:
    """  carga los datos de un archivo .json
    Args:
        ruta (str): path

    Returns:
        list: devuelve una lista 
    """
    with open(ruta,"r") as archivo:
        datos = json.load(archivo)
    return datos

# print((cargar_json('JUEGO_EN_CONJUNTO/Player score/player_score.json')))

def cargar_archivo(path:str,dato:any):
    """
        guarda el dato dado en .json si no hay crea el archivo segun el (path) dado
    Args:
        path (str): Dirrecion donde guardara el dato
        dato (any): dato a guardar
    """
    lista_score = []
    try:
        lista_score = cargar_json(path)
    except:
        guardar_archivo_json(path,[])
    lista_score.append(dato)
    guardar_archivo_json(path,lista_score)