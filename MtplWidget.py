import sys
import random
import matplotlib

matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MyMplCanvas(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""

    def __init__(self, parent=None, data=None):
        self.data = data
        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure(figsize=(5, 4), dpi=100)  # 新建一个figure
        self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.start_static_plot()

    def get_pots(self):
        pots = []
        for x in self.data.split(","):
            pots.append(int(x))
        return pots

    def start_static_plot(self):
        self.fig.suptitle('测试静态图')
        t = [1,2,3,4]
        self.axes.plot(t, self.get_pots())
        self.axes.set_xticks([1,2,3,4])
        self.axes.set_xticklabels(["1月", "2月", "3月", "4月"])
        # self.axes.grid(True)
        self.axes.set_ylabel('score')
        self.axes.set_xlabel('time')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.exit(app.exec_())