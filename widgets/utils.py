import json

def look_for_master(child, type):
    """
    Busca un widget ascendente (padre, abuelo, etc.) de un tipo específico.
    Args:
        child: El widget desde el cual empezar la búsqueda.
        type: El tipo de clase del widget que se busca.
    Retorna:
        El widget encontrado o None si no se encuentra.
    """
    while not isinstance(child, type) and child is not None:
        child = child.parent
    return child

def look_for_child(rec, type):
    """
    Busca un hijo directo de un tipo específico dentro de un widget contenedor.
    Args:
        rec: El widget contenedor donde buscar.
        type: El tipo de clase del widget hijo que se busca.
    Retorna:
        El primer widget hijo encontrado o None si no existe.
    """
    for child in rec.children:
        if isinstance(child, type):
            return child
    return None

def get_index_widget(master, type):
    """
    Obtiene el índice de un widget de un tipo específico dentro de los hijos de un contenedor.
    Args:
        master: El widget contenedor.
        type: El tipo de clase del widget a buscar.
    Retorna:
        El índice (int) del widget en la lista de hijos, o -1 si no se encuentra.
    """
    if master is not None:
        for i in range(len(master.children)):
            if isinstance(master.children[i], type):
                return i
    return -1

def read_json(link):
    """
    Lee un archivo JSON y devuelve su contenido.
    Args:
        link: La ruta del archivo JSON.
    Retorna:
        Dict: El contenido del archivo JSON.
    """
    with open(link, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json(link, data):
    """
    Escribe datos en un archivo JSON con formato legible.
    Args:
        link: La ruta del archivo JSON.
        data: Los datos a escribir (diccionario o lista).
    """
    with open(link, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)