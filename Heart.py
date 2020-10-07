from tkinter import *
from math import *

resolutionX = 600
resolutionY = 600

root = Tk()
c = Canvas(root, width=resolutionX, height=resolutionY, bg="#3c3f41")
c.pack()


step = 10e-3 * 5
start = -pi / 2
angle = start

heart = lambda x, y: (2 - 2 * sin(y - pi) + sin(y - pi) * abs(cos(y - pi)) ** (1 / 2) / (sin(y - pi) + 1.4)) * x / 3
polar_rose = lambda x, y: sin(6 * y) * x
astroid = lambda x, y: (cos(y) ** 20 + sin(y) ** 20) ** (1 / 2) * x
jmap = lambda x, y: (2 - 0.5 * sin(50 * y) + cos(7 * y)) * x


figures = {"Сердце": heart, 'Полярная роза': polar_rose, 'Астроида': astroid, 'Снежинка': jmap}


def from_polar_system(func, size, ang, x, y):
    r = func(size, ang)
    return r * cos(ang) + x, r * sin(ang) + y


def motion(func, size, width_line=0):
    global angle
    fr = resolutionX / 2, resolutionY / 2
    while angle < start + 2 * pi + step:
        to = from_polar_system(func, size, angle, resolutionX / 2, resolutionY / 2)
        fr_s = fr[0] + step * cos(angle), fr[1] + step * sin(angle)
        c.create_polygon(resolutionX / 2, resolutionY / 2, fr, to, fill='red', outline='red')
        c.create_polygon(fr_s, fr, to, fill='white', outline='white', width=width_line)
        fr = to
        angle += step
        c.update()


def start_motion(func):
    global angle
    c.delete("all")
    motion(func, 200, 3)
    angle = -pi / 2


x = 10
y = resolutionY - 45

for i in figures:
    Button(c, text=i, width=10, fg='white', bg='#3c3f41', command=lambda m=figures[i]: start_motion(m)).place(x=x, y=y)
    x += 100

root.mainloop()