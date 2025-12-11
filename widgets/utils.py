import json

def look_for_master(child, type):
    while not isinstance(child, type) and child is not None:
        child = child.parent
    return child

def look_for_child(rec, type):
    for child in rec.children:
        if isinstance(child, type):
            return child
    return None

def get_index_widget(master, type):
    if master is not None:
        for i in range(len(master.children)):
            if isinstance(master.children[i], type):
                return i
    return -1

def read_json(link):
    with open(link, 'r', encoding='utf-8') as file:
        return json.load(file)