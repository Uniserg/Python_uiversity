from tkinter import *
from math import *


class Circle:
    def __init__(self, center_x, center_y, radius):
        self.center = center_x, center_y
        self.radius = radius

    def create_circle_parameters(self):
        return (self.center[0] - self.radius,
                self.center[1] - self.radius,
                self.center[0] + self.radius,
                self.center[1] + self.radius)


angle = pi/2
step = 10e-4 * 5
wave_freq = 20
wave_amp = 30

resolutionX = 600
resolutionY = 600

root = Tk()

c = Canvas(root, width=resolutionX, height=resolutionY, bg="#3c3f41")
c.pack()

circle_big = Circle(center_x=resolutionX // 2, center_y=resolutionY // 2, radius=200)
circle_big_graphics = c.create_oval(*circle_big.create_circle_parameters(), fill='#a44841', outline="#a44841")

circle_little = Circle(center_x=circle_big.center[0] + circle_big.radius, center_y=circle_big.center[1], radius=25)
circle_little_graphics = c.create_oval(*circle_little.create_circle_parameters(), fill='white')


def from_polar_system(obj, ang, origin=Circle(0, 0, 0), func=lambda x: x):
    r = func(origin.radius, ang)
    return r * cos(ang) + origin.center[0] - obj.radius, r * sin(ang) + origin.center[1] - obj.radius


def processor(func, create_line=True, create_inf=False):
    global angle
    fr = from_polar_system(circle_little, angle, circle_big, func)

    def motion():
        nonlocal fr
        global angle
        to = from_polar_system(circle_little, angle, circle_big, func)

        if create_line and (create_inf or abs(angle) <= 2 * pi + step):
            c.create_line(*map(lambda x: x + circle_little.radius, fr + to))
            # c.create_polygon([300, 300], to, fill="gold",smooth=1,outline="black", width=5)
        c.moveto(circle_little_graphics, *to)
        fr = to
        angle += step
        root.after(1, motion)

    motion()


def task1():
    processor(lambda x, y: x, False)


def task2():
    processor(lambda x, y: x + sin(y * 50) * 30)


def task3():
    processor(lambda x, y: x * sin(y * 6))


def task4():
    processor(lambda x, y: y * 5, create_inf=True)


def task5():
    processor(lambda x, y: (1 - sin(y)) * 0.5 * x)


def task6():
    processor(lambda x, y: y * 5 + sin(y * wave_freq) * wave_amp * 5, create_inf=True)


def task7():
    processor(lambda x, y: (2 - 2 * sin(y) + sin(y) * ((abs(cos(y))) ** (1 / 4) / (sin(y) + 1.8))) * x / 4)


def task12():
    processor(lambda x, y: (2 - 2 * sin(y - pi) + sin(y - pi) * abs(cos(y - pi)) ** (1 / 2) / (sin(y - pi) + 1.4)) * x / 4 )


def task8():
    processor(lambda x, y: 4 * sin(2 * y) * x / 4)


def task9():
    processor(lambda x, y: y * 5 + sin(y * wave_freq) * wave_amp / 5 * (-y / 5), create_inf=True)


def task10():
    def lemniscate_bernoulli(x, y):
        global angle, step

        if -pi / 4 <= angle % pi <= pi / 4 or 3 * pi / 4 <= angle % pi <= 5 * pi / 4:
            return sqrt(2 * x ** 2 * cos(2 * y))
        else:
            angle += pi
            step = -step
            return 0

    processor(lemniscate_bernoulli)


def task11():
    processor(lambda x, y: y * 5 + sin(y * wave_freq) * wave_amp / 5 * -y, create_inf=True)


run_task = 12
eval(f'task{run_task}()')
root.mainloop()
