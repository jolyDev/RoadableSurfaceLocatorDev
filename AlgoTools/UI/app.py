import sys
from PyQt5.QtWidgets import *
import time
import numpy as np
import Shared.data_provider as data_manager
import Shared.point_utils as point_utils
from hist_render import HistRender2D
from render2d import Render2D
import math
from AlgoTools.Entropy.entropy import getEntropyFactors

import matplotlib.pyplot as plt

from range_slider import SliderX
from view import View

def axis_log(point, data3d):
    x = point[0][0]
    y = point[0][1]
    z = point[0][2]
    print("[" + str(x) + ", " + str(y) + ", " + str(z) + "] | " + str(data3d[x][y][z]))

def normalize(arr):
    arr_min = np.min(arr)
    return (arr-arr_min)/(np.max(arr)-arr_min)

class Window(QWidget):

    def __init__(self, data):
        super().__init__()
        #plt.set_cmap("gray")

        width = 18
        height = 2

        self.init_data = data
        self.depth_view = Render2D(self, point_utils.ExtractDist(self.init_data), "depth view", width, height)

        entropy = point_utils.ExtractEntropy(self.init_data)
        entropy = point_utils.ExtractEntropy(self.init_data)
        self.segmented_view = Render2D(self, entropy, "segmented area", width, height)
        self.hist_view = HistRender2D(self, entropy, "entropy distribution", width, height)
        self.slider = SliderX(min(entropy.flatten()), max(entropy.flatten()), self.onSliderRelease)
        self.invertion = QCheckBox("Invert segmentation")
        self.invertion.setChecked(False)
        self.invertion.toggled.connect(self.onSliderRelease)
        self.status = QLabel("wait")

        self.UiComponents()
        self.show()

    def UiComponents(self):
        self.setWindowTitle("Multi-Factor Segmentation")

        vbox = QVBoxLayout(self)

        vbox.addWidget(QLabel("depth view"))
        vbox.addWidget(self.depth_view)

        vbox.addWidget(QLabel("segmented area"))
        vbox.addWidget(self.segmented_view)

        vbox.addWidget(QLabel("entropy distribution"))
        vbox.addWidget(self.hist_view)

        vbox.addWidget(self.slider)
        vbox.addWidget(self.invertion)
        vbox.addWidget(self.status)

        self.setLayout(vbox)
        #self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #self.layout().addItem(self.verticalSpacer)

        self.showMaximized()

    def onSliderRelease(self):
        self.status.setText("calculating ...")
        segmented = point_utils.EntropyRemoveOutOfBounds(self.init_data, self.slider.getMin(), self.slider.getMax(), self.invertion.isChecked())
        entropy = point_utils.ExtractEntropy(segmented)
        self.segmented_view.draw(entropy)
        self.hist_view.draw(entropy)
        self.status.setText("wait")
        print("*")

def init():
    app = QApplication(sys.argv)

    data = data_manager.velo_points_2_pano_info(data_manager.get_data())
    data = point_utils.DropEntropy(data)
    for functor in getEntropyFactors():
        data = point_utils.CalcEntropy(data, functor)

    ex = Window(point_utils.CreateEntropyBackGround(data))
    sys.exit(app.exec_())

if __name__ == '__main__':
    init()