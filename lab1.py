from typing import List, Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from tkinter import *

window = Tk()

labels = []
# entries = [[], [], [], [], []]
entries = []
paramfull = ["Начальная скорость", "Угол", "Постоянная g", "Начальное положение по х", "Начальное положение по y"]
param = []
values = {}
data_x = []
data_y = []
data_lmax = []
data_hmax = []
lines = []
times = 0


def addrows():
    localentries = []
    global param
    try:
        for i in range(5):
            entry = Entry(window)
            entry.grid(row=i + 1, column=1 + (len(param)))
            localentries.append(entry)
        param.append(len(param) + 1)
        entries.append(localentries)
    except IndexError:
        pass


def addlabels():
    for i in range(len(paramfull)):
        label = Label(window, text=paramfull[i])
        label.grid(row=i + 1, column=0)
        labels.append(label)


def getvalues():
    global values
    for i in range(len(param)):
        localentries = []
        for j in range(5):
            try:
                localentries.append(float(entries[i][j].get()))
            except IndexError:
                pass
        values[i] = localentries
    print(values)


def make_graph():
    global data_lmax
    global data_hmax
    global data_x
    global data_y
    global times
    x = [values[times][3] + values[times][0] * np.cos((values[times][1] * np.pi) / 180) * t
         for t in np.linspace(0, 100, 1000)]
    data_x.append(x)
    y = [values[times][4] + values[times][0] * np.sin((values[times][1] * np.pi) / 180) * t
         - (values[times][2] * t * t) / 2 for t in np.linspace(0, 100, 1000)]
    data_y.append(y)

    print(data_x, data_y, data_hmax, data_lmax)
    times += 1
    return x, y

def findmax():
    for i in range(len(param)):
        lmax = (values[i][0] ** 2 * np.sin(2 * (values[i][1] * np.pi) / 180)) / values[i][2]
        data_lmax.append(lmax)
        hmax = (values[i][0] ** 2 * np.sin((values[i][1] * np.pi) / 180) ** 2) / (2 * values[i][2])
        data_hmax.append(hmax)
    maxl = max(data_lmax)
    maxh = max(data_hmax)
    return maxl, maxh

def showgraph():
    fig, ax = plt.subplots()
    (line,) = ax.plot([], [])
    print(values)
    x, y = make_graph()
    maxl, maxh = findmax()
    ax.set(xlim=(0, maxl + 2), ylim=(0, maxh))

    def animate(i):
        line.set_data(x[:i], y[:i])
        return line,

    anim = FuncAnimation(fig, animate, frames=100, interval=300, blit=True)

    plt.show()


Button(window, text="Добавить измерение", command=addrows).grid(row=0, column=1)
Button(window, text="Ввод данных", command=getvalues).grid(row=0, column=2)
Button(window, text="Показать график движения тела", command=showgraph).grid(row=0, column=0)

# Сразу добавляем одну строку

addrows()
addlabels()
window.mainloop()
print(entries)
print(labels)
print(values)
