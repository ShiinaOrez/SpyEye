import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm
import numpy as np
import cv2
import math

# arr = np.random.rand(16, 16)
# plt.imshow(arr, interpolation='nearset', cmap='bone', origin='lower')

# plt.colorbar()
# plt.xticks(())
# plt.yticks(())
# plt.show()

data = (
    ((1, 1), 1.0),
    ((389, 500), 3.0),
    ((700, 207), 4.0),
    ((665, 544), 4.1),
    ((1023, 1023), 4.7)
)
default = 16581375
factor = 10.0
img = np.zeros((1080, 1920, 3), np.uint8)

def drawImage(img, data):
    averange = getAverLength(getLength(data))  # int
    colorStep = default/averange  # float
    for index in range(data):
        if index == 0 or index == len(data)-1:
            a = 0
        else:
            v1 = math.sqrt(
                pow((data[index - 1][0][0] - data[index][0][0]), 2) +
                pow((data[index - 1][0][1] - data[index][0][1]), 2)) / (data[index][1] - data[index-1][1])
            v2 = math.sqrt(
                pow((data[index + 1][0][0] - data[index][0][0]), 2) +
                pow((data[index + 1][0][1] - data[index][0][1]), 2)) / (data[index+1][1] - data[index][1])
            a = 2 * abs(v2 - v1) / (data[index + 1] - data[index - 1])
#        color = int(colorStep * index)
#        img[data[index][0][0], data[index][0][1]] = [color/65025, int(color/255) % 256, color % 256]
#        drawSlash(img, data[index][0][0], data[index][0][1], a, )

def drawSlash(img, x, y, a, v, color):
    rev = (-1.0)/v
    r = factor/a
    dy = abs(r*rev/(math.sqrt(1+rev*rev)))
    dx = abs(r/(math.sqrt(1+rev*rev)))
#    if dy < dx:
#        dx, dy = dy, dx
    for i in range(int(dx)+1):
        d = int(abs(rev)*i)
        img[x-dx, y-d] = [color/65025, int(color/255) % 256, color % 256]
        img[x+dx, y+d] = [color/65025, int(color/255) % 256, color % 256]


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

drawImage(img, data)

cv2.imwrite("/home/song-ruyang/SpyEye/test.jpg", img)