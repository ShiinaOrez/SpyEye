import os
import numpy as np

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
    StartTime = 0
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
    tracks = []
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
                        if track_now.StartTime == 0 and len(track_now.Reports) == 1:
                            track_now.StartTime = track_now.Reports[0].Time
                        track_now.Reports[-1].Time -= track_now.StartTime
                        
                        tracks.append(track_now)
                        track_now = Track(0, [])

                    tracks.append(track_now)
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
                if track_now.StartTime == 0 and len(track_now.Reports) == 1:
                    track_now.StartTime = track_now.Reports[0].Time
                track_now.Reports[-1].Time -= track_now.StartTime
                point_counter += 1
    return tracks

d_position = np.dtype([('x', np.int16), ('y', np.int16)])
d_report = np.dtype([('time', np.float16), ('is_btn', 'b'), ('pos', d_position), ('width', np.int16)])

def save_as_np(tracks, name):
    np_tracks_list = []
    for track in tracks:
        np_reports_list = [(report.Time, report.IsBtn, (report.Pos.X, report.Pos.Y,), report.Width,) for report in track.Reports]
        np_tracks_list.append(np.array(np_reports_list, dtype=d_report))
    np_tracks = np.array(np_tracks_list)
    np.save(name, np_tracks)

if __name__ == "__main__":
    fixs = ["alipay", "kfc", "zhihu", "chrome", "qq"]
    names = ["szy-"+fix for fix in fixs]
    for name in names:
        try:
            save_as_np(main(name+".txt"), name)
        except Exception as e:
            pass