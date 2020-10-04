from tkinter import *
from random import randint

resolutionX = 600
resolutionY = 600
root = Tk()
cnv = Canvas(root, width=resolutionX, height=resolutionY, bg="#2b2b2b")
cnv.pack()

array = []
graphic_array = []
steps = False
trap = 0


def steps_change():
    global steps, changer

    if steps:
        steps = False
        changer.config(fg="#0fab60", text="by steps on")
    else:
        steps = True
        changer.config(fg="#91313d", text="by steps off")

    changer.update()


def generate():
    global array, graphic_array
    array.clear()
    graphic_array.clear()

    set_array = [i for i in range(resolutionX)]
    while set_array:
        array.append(set_array.pop(randint(0, len(set_array) - 1)))
    graphic_array = [cnv.create_line(i, 0, i, array[i], fill="#91313d") for i in range(len(array))]
    i = 0


def mark(obj1, obj2, color):
    cnv.itemconfig(obj1, fill=color)
    cnv.itemconfig(obj2, fill=color)


def motion(func):
    def wrapper(*args):
        for l1, l2 in func(*args):
            cnv.move(graphic_array[l1], l2 - l1, 0)
            cnv.move(graphic_array[l2], l1 - l2, 0)
            if steps:
                mark(graphic_array[l1], graphic_array[l2], "yellow")
                cnv.update()
                mark(graphic_array[l1], graphic_array[l2], "#91313d")
            cnv.after(trap)
            graphic_array[l1], graphic_array[l2] = graphic_array[l2], graphic_array[l1]
    return wrapper


@motion
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield j, j + 1
        cnv.update()


@motion
def sel_sort(arr):
    for i in range(len(arr) - 1):
        mi = i
        for j in range(i + 1, len(arr)):
            if arr[mi] < arr[j]:
                mi = j
        arr[i], arr[mi] = arr[mi], arr[i]
        yield i, mi
        cnv.update()


@motion
def insertion_sort(arr, start=0, gap=1):
    for i in range(start + gap, len(arr), gap):
        j = i
        while j >= gap and arr[j] > arr[j - gap]:
            arr[j - gap], arr[j] = arr[j], arr[j - gap]
            j -= gap
            yield j, j + gap
        cnv.update()


def shell_sort(arr):
    subl_count = (len(arr) - 1) // 3
    while subl_count > 0:
        for start_position in range(subl_count):
            insertion_sort(arr, start_position, subl_count)
        subl_count = (subl_count - 1) // 3


def partition(nums, low, high):
    pivot = nums[(low + high) // 2]
    # cnv.itemconfig(graphic_array[-pivot], fill="green")
    # cnv.update()
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while nums[i] > pivot:
            i += 1
        j -= 1
        while nums[j] < pivot:
            j -= 1
        if i >= j:
            cnv.itemconfig(graphic_array[-pivot], fill="#91313d")
            return j
        nums[i], nums[j] = nums[j], nums[i]
        yield i, j
        cnv.update()


def quick_sort(nums):
    @motion
    def _quick_sort(items, low, high):
        if low < high:
            it = iter(partition(items, low, high))
            while True:
                try:
                    yield next(it)
                except StopIteration as e:
                    split_index = e.value
                    break
            _quick_sort(items, low, split_index)
            _quick_sort(items, split_index + 1, high)
    _quick_sort(nums, 0, len(nums) - 1)


@motion
def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[i] > arr[l]:
        largest = l

    if r < n and arr[largest] > arr[r]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        yield i, largest

        heapify(arr, n, largest)
    cnv.update()


@motion
def heapsort(arr):
    n = len(arr)

    for i in range(n, -1, -1):
        heapify(arr, n, i)

    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield i, 0
        heapify(arr, i, 0)


def start_sort(func):
    cnv.delete("all")
    generate()
    cnv.update()
    func(array)


sorters = ["bubble_sort", "insertion_sort", "sel_sort", "shell_sort", "quick_sort", "heapsort"]

x = 10
y = resolutionY - 45
for sort in sorters:
    btn = Button(root, text=sort, width=10, fg="white", bg="#3c3f41", command=lambda s=sort: start_sort(eval(s)))
    btn.place(x=x, y=y)
    x += 100

changer = Button(root, text="by steps on", command=steps_change, fg="#0fab60", bg="#3c3f41")
changer.place(x=resolutionX - 90, y=resolutionY - 100)
root.mainloop()
