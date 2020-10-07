import tkinter as tk
from random import randint


class SortsVisualisation(tk.Frame):
    sorters = ["bubble_sort", "insertion_sort", "sel_sort", "shell_sort", "quick_sort", "heapsort"]

    def __init__(self, root, width, height, bg="white"):
        super().__init__(root, width=width, height=height, bg=bg)
        self.root = root
        self.root.title("Sorts visualization")
        self.cnv = tk.Canvas(root, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.array = []
        self.graphic_array = []
        self.steps = False
        self.latency = 0
        self.changer = tk.Button(root, text="by steps on", command=self.steps_change, fg="#0fab60", bg="#3c3f41")
        self.changer.place(x=width - 90, y=height - 100)

        x = 10
        y = height - 45

        for sort in SortsVisualisation.sorters:
            tk.Button(self.cnv, text=sort, width=10, fg="white", bg="#3c3f41",
                      command=lambda s=sort: self.start_sort(eval(f"self.{s}"))).place(x=x, y=y)
            x += 100

    def generate(self):
        self.array.clear()
        self.graphic_array.clear()

        set_array = [i for i in range(self.width)]
        while set_array:
            self.array.append(set_array.pop(randint(0, len(set_array) - 1)))
        self.graphic_array = [self.cnv.create_line(i, 0, i, self.array[i], fill="#91313d") for i in
                              range(len(self.array))]

    def _mark(self, obj1, obj2, color):
        self.cnv.itemconfig(obj1, fill=color)
        self.cnv.itemconfig(obj2, fill=color)

    def motion(func):
        def wrapper(self, *args):
            for l1, l2 in func(self, *args):
                self.cnv.move(self.graphic_array[l1], l2 - l1, 0)
                self.cnv.move(self.graphic_array[l2], l1 - l2, 0)
                if self.steps:
                    self._mark(self.graphic_array[l1], self.graphic_array[l2], "yellow")
                    self.cnv.update()
                    self._mark(self.graphic_array[l1], self.graphic_array[l2], "#91313d")
                self.cnv.after(self.latency)
                self.graphic_array[l1], self.graphic_array[l2] = self.graphic_array[l2], self.graphic_array[l1]

        return wrapper

    @motion
    def bubble_sort(self):
        for i in range(len(self.array)):
            for j in range(len(self.array) - i - 1):
                if self.array[j] < self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    yield j, j + 1
            self.cnv.update()

    @motion
    def sel_sort(self):
        for i in range(len(self.array) - 1):
            mi = i
            for j in range(i + 1, len(self.array)):
                if self.array[mi] < self.array[j]:
                    mi = j
            self.array[i], self.array[mi] = self.array[mi], self.array[i]
            yield i, mi
            self.cnv.update()

    @motion
    def insertion_sort(self, start=0, gap=1):
        for i in range(start + gap, len(self.array), gap):
            j = i
            while j >= gap and self.array[j] > self.array[j - gap]:
                self.array[j - gap], self.array[j] = self.array[j], self.array[j - gap]
                j -= gap
                yield j, j + gap
            self.cnv.update()

    def shell_sort(self):
        subl_count = (len(self.array) - 1) // 3
        while subl_count > 0:
            for start_position in range(subl_count):
                self.insertion_sort(start_position, subl_count)
            subl_count = (subl_count - 1) // 3

    def partition(self, low, high):
        pivot = self.array[(low + high) // 2]
        if self.steps:
            self.cnv.itemconfig(self.graphic_array[-pivot], fill="green")
            self.cnv.update()
        i = low - 1
        j = high + 1
        while True:
            i += 1
            while self.array[i] > pivot:
                i += 1
            j -= 1
            while self.array[j] < pivot:
                j -= 1
            if i >= j:
                self.cnv.itemconfig(self.graphic_array[-pivot], fill="#91313d")
                return j
            self.array[i], self.array[j] = self.array[j], self.array[i]
            yield i, j
            self.cnv.update()

    def quick_sort(self):
        @SortsVisualisation.motion
        def _quick_sort(self, low, high):
            if low < high:
                it = iter(self.partition(low, high))
                while True:
                    try:
                        yield next(it)
                    except StopIteration as e:
                        split_index = e.value
                        break
                _quick_sort(self, low, split_index)
                _quick_sort(self, split_index + 1, high)

        _quick_sort(self, 0, len(self.array) - 1)

    @motion
    def heapify(self, arr, n, i):
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

            self.heapify(arr, n, largest)
        self.cnv.update()

    @motion
    def heapsort(self):
        n = len(self.array)

        for i in range(n, -1, -1):
            self.heapify(self.array, n, i)

        for i in range(n - 1, 0, -1):
            self.array[i], self.array[0] = self.array[0], self.array[i]
            yield i, 0
            self.heapify(self.array, i, 0)

    def start_sort(self, func):
        self.cnv.delete("all")
        self.generate()
        self.cnv.update()
        func()

    def steps_change(self):
        if self.steps:
            self.steps = False
            self.changer.config(fg="#0fab60", text="by steps on")
        else:
            self.steps = True
            self.changer.config(fg="#91313d", text="by steps off")
        self.changer.update()

    def run(self):
        self.cnv.pack()
        self.root.mainloop()


if __name__ == "__main__":
    SortsVisualisation(tk.Tk(), 600, 600, "#2b2b2b").run()
