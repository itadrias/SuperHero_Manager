from datetime import *
from .utils import read_json, write_json

def check_overlapping(start, end, resources):
    events = read_json("json/events.json")
    for i in range (len(events)):
        dates = events[str(i)]
        d_start = datetime.strptime(dates["start"], "%Y-%m-%d %H:%M")
        d_end = datetime.strptime(dates["end"], "%Y-%m-%d %H:%M")
        found = False
        for j in resources:
            if j in dates["resources"] and j >= 17:
                found = True
        if ((start < d_end and end >= d_end) or (start <= d_start and end > d_start) or (start > d_start and end < d_end)) and found:
            return d_end
    return None

def next_available(start, end, resources):
    diff = end - start
    while True:
        next = check_overlapping(start, start + diff, resources)
        if next == None:
            break
        start = next
    return (start, start+diff)

def sort_events():
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
    events = read_json("json/events.json")
    events.pop(str(id))
    write_json("json/events.json", events)
    sort_events()