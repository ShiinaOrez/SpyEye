import os
import numpy

class Position:
    X = 0
    Y = 0
    def __init__(self, x, y):
        self.X = x
        self.Y = y

class Report:
    Time = 0
    IsBtn = False
    Pos = Position(0, 0)
    Width = 0
    def __init__(self, time, is_btn):
        self.Time = time
        self.IsBtn = is_btn

class Track:
    ID = 0
    Reports = []
    def __init__(self, id, reports):
        self.ID = id
        self.Reports = reports

class Slot:
    Tracks = []
    Used = False
    def __init__(self, tracks, used):
        self.Tracks = tracks
        self.Used = used

class Collection:
    Slots = []

class Event:
    Time = 0
    Statu = ""
    Info = ""
    Value = 0
    def __init__(self, statu, info):
        self.Statu = statu
        self.Info = info

def factory(text):
    pieces = text.split(" ")
    segs = [x for x in pieces if x != ""]
    newEvent = Event(segs[3], segs[4])
    if segs[5] == "DOWN":
        newEvent.Value = -333
    elif segs[5] == "UP":
        newEvent.Value = -444
    elif segs[5] == "ffffffff":
        newEvent.Value = -1
    else:
        num = 0
        try:
            num = int(segs[5], 16)
        except Exception as e:
            print(e)
            os._exit(0)
        else:
            newEvent.Value = num
    newEvent.Time = float(segs[1].rstrip("]"))
    return newEvent

def main(file_name):
    store = {}
    counter = 0
    f = open(file_name)
    line = f.readline()
    while line:
        # using line
        if line.startswith("["):
            # line = line.lstrip("[")
            store[counter] = factory(line)
            counter += 1
        line = f.readline()
    f.close()
    collection = Collection()
    slot_now = 0
    collection.Slots.append(Slot([], True))
    for i in range(9):
        collection.Slots.append(Slot([], False))
    track_now = Track(0, [])
    pos_now = [Position(0, 0)] * 10
    width_now = [0] * 10
    track_counter = 0
    point_counter = 0
    max_slot = 0
    for i in range(counter):
        event_now = store[i]
        if event_now.Statu == "EV_ABS":
            if event_now.Info == "ABS_MT_TRACKING_ID":
                if event_now.Value == -1:
                    if i < counter-1 and store[i+1].Statu == "EV_KEY":
                        track_now.Reports.append(Report(store[i+1].Time, True))
                        collection.Slots[slot_now].Tracks.append(track_now)
                        track_now = Track(0, [])
                    collection.Slots[slot_now].Tracks.append(track_now)
                    pos_now[slot_now] = Position(0, 0)
                    width_now[slot_now] = 0
                    track_counter += 1
                else:
                    track_now = Track(event_now.Value, [])
            elif event_now.Info == "ABS_MT_SLOT":
                if slot_now != event_now.Value:
                    slot_now = event_now.Value
                if not collection.Slots[slot_now].Used:
                    collection.Slots[slot_now] = Slot([], True)
            elif event_now.Info == "ABS_MT_POSITION_X":
                pos_now[slot_now].X = event_now.Value
            elif event_now.Info == "ABS_MT_POSITION_Y":
                pos_now[slot_now].Y = event_now.Value
            elif event_now.Info == "ABS_MT_WIDTH_MAJOR":
                width_now[slot_now] = event_now.Value
        else:
            if i > 0 and store[i-1].Info.startswith("ABS_MT_POSITION"):
                new_report = Report(store[i-1].Time, False)
                new_report.Pos = Position(pos_now[slot_now].X, pos_now[slot_now].Y)
                new_report.Width = width_now[slot_now]
                track_now.Reports.append(new_report)
                point_counter += 1
    while collection.Slots[max_slot].Used:
        max_slot += 1

    print(counter, int(store[counter-1].Time-store[0].Time)/1000, point_counter, track_counter, max_slot)

if __name__ == "__main__":
    main("out.txt")
