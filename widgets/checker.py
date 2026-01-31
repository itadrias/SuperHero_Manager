from datetime import *
from .utils import read_json, write_json

def check_overlapping(start, end):
    events = read_json("json/events.json")
    for i in range (len(events)):
        dates = events[str(i)]
        d_start = datetime.strptime(dates["start"], "%Y-%m-%d %H:%M")
        d_end = datetime.strptime(dates["end"], "%Y-%m-%d %H:%M")
        if (start < d_end and end >= d_end) or (start <= d_start and end > d_start) or (start > d_start and end < d_end):
            return d_end
    return None

def next_available(start, end):
    diff = end - start
    while True:
        next = check_overlapping(start, start + diff)
        if next == None:
            break
        start = next
    return (start, start+diff)
