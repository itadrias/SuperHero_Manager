from datetime import *
from .utils import read_json, write_json

# Diccionario que mapea IDs de recursos a cantidades disponibles
cant = {
    "29": 1,
    "30": 3,
    "31": 5,
    "32": 4,
    "33": 4,
    "34": 2,
    "35": 10,
    "36": 6,
    "37": 3,
    "38": 2,
    "39": 2,
    "40": 1
}

def check_overlapping(start, end, resources):
    """
    Verifica si hay conflictos de recursos en un rango de fechas.
    Args:
        start: Fecha de inicio del evento.
        end: Fecha de fin del evento.
        resources: Lista de IDs de recursos necesarios.
    Retorna:
        La fecha de finalización del evento conflictivo más próximo si hay conflicto,
        o None si no hay solapamiento.
    """
    events = read_json("json/events.json")
    disp = { "29": 1,"30": 3,"31": 5,"32": 4,"33": 4,"34": 2,"35": 10,"36": 6,"37": 3,"38": 2,"39": 2,"40": 1 }
    sort = [["3000-01-01 14:00", 1]]
    for i in range (len(events)):
        dates = events[str(i)]
        # Libera recursos de eventos que ya han terminado antes del inicio de este
        while sort[0][0] <= dates["start"]:
            delete = events[str(sort[0][1])]
            for j in delete["resources"]:
                if j >=29 and j <= 40:
                    disp[str(j)] += 1
            sort.pop(0)
        
        d_start = datetime.strptime(dates["start"], "%Y-%m-%d %H:%M")
        d_end = datetime.strptime(dates["end"], "%Y-%m-%d %H:%M")
        found = False
        
        # Ocupa recursos del evento actual iterado
        for j in dates["resources"]:
            if j >=29 and j <= 40:
                disp[str(j)] -= 1
        
        sort.append([dates["end"], i])
        sort = sorted(sort)
        
        # Verifica conflictos
        for j in resources:
            if j in dates["resources"] and j >= 17 and j <= 28:
                found = True # Conflicto con héroes
            if j >=29 and j <= 40:
                if disp[str(j)] == 0:
                    found = True # Conflicto con items/recursos limitados
        
        # Si hay intersección de fechas y conflicto de recursos, retorna la fecha fin
        if ((start < d_end and end >= d_end) or (start <= d_start and end > d_start) or (start >= d_start and end <= d_end)) and found:
            return d_end
    return None

def next_available(start, end, resources):
    """
    Encuentra el siguiente intervalo de fechas disponible para unos recursos dados.
    Args:
        start: Fecha de inicio deseada.
        end: Fecha de fin deseada.
        resources: Lista de recursos.
    Retorna:
        Tupla (start, end) con las fechas disponibles ajustadas.
    """
    diff = end - start
    while True:
        next = check_overlapping(start, start + diff, resources)
        if next == None:
            break
        start = next
    return (start, start+diff)

def sort_events():
    """
    Ordena los eventos cronológicamente y reescribe el JSON de eventos.
    Mantiene la consistencia de los IDs.
    """
    events = read_json("json/events.json")
    copy = read_json("json/events.json")
    sort = []
    for i in copy:
        events.pop(i)
    for i in copy:
        sort.append([copy[i]["start"], copy[i]["end"], copy[i]["id"], copy[i]["resources"]])
    sort = sorted(sort)
    for i in sort:
        events[len(events)] = {
            "start": i[0],
            "end": i[1],
            "id": i[2],
            "resources": i[3]
        }
    write_json("json/events.json", events)

def create_event(start, end, mission, resources):
    """
    Crea un nuevo evento y lo guarda en el JSON.
    Args:
        start: Fecha inicio.
        end: Fecha fin.
        mission: ID de la misión.
        resources: Lista de recursos asignados.
    """
    events = read_json("json/events.json")
    events[len(events)]={
        "start": str(start)[:len(str(start))-3:],
        "end": str(end)[:len(str(end))-3:],
        "id": mission,
        "resources": resources
    }
    write_json("json/events.json", events)
    sort_events()

def delete_event(id):
    """
    Elimina un evento por su ID.
    Args:
        id: El ID del evento a eliminar.
    """
    events = read_json("json/events.json")
    events.pop(str(id))
    write_json("json/events.json", events)
    sort_events()