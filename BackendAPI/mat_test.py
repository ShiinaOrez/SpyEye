from spy_eye_app import db
from spy_eye_app.models import Coor

from pylab import *

def run():
    coors = db.session().query(Coor).filter_by(oper_id=846).all()
    data_x = [coor.x for coor in coors]
    data_y = [coor.y for coor in coors]

    length = len(coors)

    l = [([data_x[i], data_x[i+1]], [data_y[i], data_y[i+1]]) for i in range(length-1)]

    d = [math.sqrt((data_x[i]-data_x[i+1])*(data_x[i]-data_x[i+1]) + (data_y[i]-data_y[i+1])*(data_y[i]-data_y[i+1])) for i in range(length-1)]

    v = [(float(coors[i+1].time)-float(coors[i].time)) / d[i] for i in range(length-1)]
    const_v = 916330

    a = [0]
    max_min = 0
    max_max = 0
    for i in [(v[i+1] - v[i]) / (float(coors[i+1].time)-float(coors[i].time)) for i in range(length-2)]:
        if i<max_min:
            max_min = i
        if i>max_max:
            max_max = i
        a.append(i)
#    print(a)
    times = [coor.time for coor in coors]
    for i in range(length-1):
        print(int(times[i+1])-int(times[i]))

    figure(figsize=(19.2, 10.8), frameon=False)
    subplots_adjust(bottom = 0)
    subplots_adjust(top = 1)
    subplots_adjust(right = 1)
    subplots_adjust(left = 0)
    width = 3
    binary = 0.75

    for i in range(length-1):
        r = 0
        b = 0
        if a[i] < 0:
            b = a[i] / max_min
        elif a[i] > 0:
            r = a[i] / max_max
        plot(l[i][0], l[i][1], color=(r, 0, b, 0.8), linewidth=width+0.01*i, linestyle="-")
#        print(width)
        binary -= 0.75/length
#        plot(data_x, data_y, linewidth=width, linestyle="-")
    savefig("test.png", bbox_inches='tight', pad_inches=0, transparent=True)
    show()
