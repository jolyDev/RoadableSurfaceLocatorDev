from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
from range_slider import SliderX
import matplotlib
import datetime
import os.path
import hist_render
from time import gmtime, strftime

def array_to_qimage(im: np.ndarray, copy=False):
    gray_color_table = [qRgb(i, i, i) for i in range(256)]

    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
    qim.setColorTable(gray_color_table)
    return qim.copy() if copy else qim

def array_to_pixmap(im):
    return QPixmap(array_to_qimage(im))

class View(QWidget):
    def __init__(self, parent, data, title):
        super().__init__()

        self.setParent(parent)
        self.image = hist_render.HistRender2D(parent, data, title)
        self.slider = SliderX(10, 100, self.onDataChanged)
        self.UiComponents()
        self.show()

    def onDataChanged(self):
        #self.image.draw(data2d)
        print("x")

    def UiComponents(self):
        vbox = QVBoxLayout(self)

        vbox.addWidget(self.image)
        vbox.addWidget(self.slider)

        self.setLayout(vbox)

    def getView(self):
        return self.view

    def getImage(self):
        min, max = self.getMinBoundForView()
        return self.dicom.getSlice(self.slider.getIndex() - int(min), self.view)