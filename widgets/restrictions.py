from .utils import read_json, write_json

def check_restrictions(ids, sum):
    atributes = ["Fuerza", "Inteligencia", "Sigilo", "Carisma", "Movilidad", "Resistencia"]
    parameters = read_json("json/events_parameters.json")
    try:
        total = parameters[str(min(ids))]
    except:
        total = parameters["3"]
    ids = sorted(ids)
    founded = False
    for i in ids:
        if i >= 17 and i <= 28:
            founded = True
    if len(ids)==1 or not founded:
        return False, "Requisito de Misión: Necesitas al menos 1 héroe para iniciar el evento."
    if min(ids)==16:
        if max(ids)>28:
            return False, "Requisito de Misión: No puedes llevar ítems a este evento."
        if len(ids)>2:
            return False, "Requisito de Misión: Solo puedes llevar 1 héroe a este evento. Elige bien."
        return True, ""
    founded = False
    for i in ids:
        if i >= 29 and i <= 40:
            founded = True
    if not founded:
        return False, "Requisito de Misión: Necesitas al menos 1 ítem para iniciar el evento."
    restrictions = read_json("json/restrictions.json")
    for id in ids:
        str_id = str(id)
        if str_id in restrictions:
            needed = restrictions[str_id]
            if "forbidden" in needed:
                for restriction in needed["forbidden"]:
                    f_id = restriction["id"]
                    if f_id in ids:
                        reason = restriction.get("reason")
                        return False, reason
            if "required" in needed:
                for restriction in needed["required"]:
                    r_id = restriction["id"]
                    if r_id not in ids:
                        reason = restriction.get("reason")
                        return False, reason
    for x, y in total:
        if sum[x] < y:
            return False, f"Requisito de Atributo: Necesitas al menos {y} puntos en el atributo {atributes[x]} para iniciar el evento."
    return True, ""
