import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm
import numpy as np
import cv2
import math
import time
from spy_eye_app import db
from spy_eye_app.models import Coor

# arr = np.random.rand(16, 16)
# plt.imshow(arr, interpolation='nearset', cmap='bone', origin='lower')

# plt.colorbar()
# plt.xticks(())
# plt.yticks(())
# plt.show()

coors = db.session().query(Coor).filter_by(oper_id=846).all()
data = [((coor.x, coor.y), float(coor.time)) for coor in coors]
default = 16581375
factor = 30.0
k = 0.0001
img = np.zeros((1080, 1920, 3), np.uint8)


def drawImage(img, data):
    colorNow = 0.0
    averange = int(getLength(data)/1.414)  # int
    if averange == 0:
        averange = default
    colorStep = default/averange  # float
    color = int(colorNow)
    print(data)
    for index in range(len(data)):
#        cv2.imwrite("/home/song-ruyang/SpyEye/test.jpg", img)
#        time.sleep(2)
        print(index)
        img[data[index][0][0], data[index][0][1]] = [color / 65025, int(color / 255) % 256, color % 256]
        if index == 0 or index == len(data)-1:
            a = 0
        else:
            v1 = math.sqrt(
                pow((data[index - 1][0][0] - data[index][0][0]), 2) +
                pow((data[index - 1][0][1] - data[index][0][1]), 2)) / (data[index][1] - data[index-1][1])
            v2 = math.sqrt(
                pow((data[index + 1][0][0] - data[index][0][0]), 2) +
                pow((data[index + 1][0][1] - data[index][0][1]), 2)) / (data[index+1][1] - data[index][1])
            a = 2 * abs(v2 - v1) / (data[index + 1][1] - data[index - 1][1])
        print("[Point]", index, "| a=", a)
        # a is right, but to large
        if index != len(data)-1:
            no = data[index]             # 当前节点
            ne = data[index+1]           # 下一个节点
            ddx = ne[0][0] - no[0][0]    # 横坐标之差（有符号）
            ddy = ne[0][1] - no[0][1]    # 纵坐标之差（有符号）
            dx = abs(ddx)                # 横坐标之差（无符号）
            dy = abs(ddy)                # 纵坐标之差（无符号）
            if ddx == 0:
                v = 1.41
            else:
                v = ddy * 1.0 / (ddx * 1.0)  # 斜率（浮点数）
            if (dy < dx or dx == 0) and dy != 0:                  # 斜率绝对值小于１时，遍历纵坐标之差
                for i in range(int(dy) + 1):  # ｉ遍历整形纵坐标之差的所有单位
                    i = int(ddy/dy) * i       # ｉ乘相应的符号
                    colorNow += colorStep     # 当前小节点的颜色发生变化，浮点数为了保存细节
                    color = int(colorNow)     # 整形color为了上色
                    d = int(i * ddx / ddy)    # delta 为相对应的变化量，此处为横坐标随纵坐标偏移量
                    # 当前节点坐标偏移后上色（小节点上色）
                    img[no[0][0] + d, no[0][1] + i] = [color / 65025, int(color / 255) % 256, color % 256]
                    # 与当前斜率垂直渲染
                    drawSlash(img, no[0][0]+d, no[0][1]+i, a, v, color)
            else:
                for i in range(int(dx) + 1):
                    i = int(ddx/dx) * i
                    colorNow += colorStep
                    color = int(colorNow)
                    d = int(i * ddy / ddx)
                    img[no[0][0] + i, no[0][1] + d] = [color / 65025, int(color / 255) % 256, color % 256]
                    drawSlash(img, no[0][0]+i, no[0][1]+d, a, v, color)


def drawSlash(img, x, y, a, v, color):
    if v == 0:
        rev = 1.41
    else:
        rev = (-1.0)/v
    a = a * k
    if a == 0:
        a = 5
    r = factor / a
#    print ("[r]: ", r)
    dy = abs(r*rev/(math.sqrt(1+rev*rev)))
    dx = abs(r/(math.sqrt(1+rev*rev)))
#    print ("[dy]:", dy, "[dx]:", dx)
    if dy < dx:
        for i in range(int(dy)+1):
            d = int(rev*i)
            if (0 < x-d < 1920) and (0 < y-i < 1080):
                img[x-d, y-i] = [color/65025, int(color/255) % 256, color % 256]
            if (0 < x+d < 1920) and (0 < y+i < 1080):
                img[x+d, y+i] = [color/65025, int(color/255) % 256, color % 256]
    else:
        for i in range(int(dx)+1):
            d = int((rev)*i)
            if (0 < x-i < 1920) and (0 < y-d < 1080):
                img[x-i, y-d] = [color/65025, int(color/255) % 256, color % 256]
            if (0 < x+i < 1920) and (0 < y+d < 1080):
                img[x+i, y+d] = [color/65025, int(color/255) % 256, color % 256]


def getAverLength(length):
    return int(length/default)


def getLength(origin):
    l = 0.0
    for i in range(len(origin)-1):
        no = origin[i]
        ne = origin[i+1]
        l = l + (no[0][0]-ne[0][0])*(no[0][0]-ne[0][0])
        l = l + (no[0][1]-ne[0][1])*(no[0][1]-ne[0][1])
        l = int(math.sqrt(l))
    return l

def run():
    drawImage(img, data)

    cv2.imwrite("/home/song-ruyang/SpyEye/test.jpg", img)

run()
