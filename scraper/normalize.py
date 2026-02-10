from dateutil import parser
from collections import defaultdict

def normalize_slots(meetings):
    slots = set()

    for start, end in meetings:
        start_dt = parser.isoparse(start)
        end_dt = parser.isoparse(end)

        weekday = start_dt.strftime("%A")
        start_time = start_dt.strftime("%H:%M")
        end_time = end_dt.strftime("%H:%M")

        slots.add((weekday, start_time, end_time))

    return slots
