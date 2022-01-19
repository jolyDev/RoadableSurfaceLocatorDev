import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class Render2D(QMainWindow):
    def __init__(self, parent, data, title, width=15, height=3):
        super().__init__()

        self.setParent(parent)
        self.setWindowTitle(title)
        self.data = data
        self.canvas = Canvas(self.data, self, width=width, height=height)
        self.canvas.move(0, 0)
        #self.canvas.mpl_connect('button_press_event', self.onClick)

        #init draw
        self.draw(self.data)

    def draw(self, data):
        self.canvas.plot(data)

    def clear(self):
        self.canvas.clear()

class Canvas(FigureCanvas):
    def __init__(self, data, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), frameon=False, dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.data = data
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.overlay = False
        self.plot(data)

    def plot(self, data):
        self.axes.clear()

        frame = np.copy(data)

        for x in range(frame.shape[0]):
            for y in range(frame.shape[1]):
                if frame[x][y] == 0:
                    frame[x][y] = -1000
        # plot data
        self.axes.imshow(data)

        self.draw()

    def clear(self):
        self.axes.clear()

        self.draw()
