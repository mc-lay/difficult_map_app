import math
import sys

from main_design import Ui_MainWindow as MainUi
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize
from map_working import MapParams, load_map, get_coordinates


class MainApp(QMainWindow, MainUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setFixedSize(800, 600)

        self.map_types = ["map", "sat", "sat,skl"]

        self.comboBox.addItems(["Схема", "Спутник", "Гибрид"])

        self.mp = MapParams()
        self.map_file = load_map(self.mp)

        self.pixmap = QPixmap("map.png")
        self.label.setPixmap(self.pixmap)
        self.label.setFixedSize(self.pixmap.width(), self.pixmap.height())
        self.label.setFocus()

        self.comboBox.setCurrentIndex(0)
        self.comboBox.currentTextChanged.connect(self.change_map_type)

        self.seatch_btn.clicked.connect(self.search_obj)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_PageUp and self.mp.zoom < 20:
            self.mp.zoom += 1
            self.map_file = load_map(self.mp)
        elif event.key() == QtCore.Qt.Key_PageDown and self.mp.zoom > 2:
            self.mp.zoom -= 1
            self.map_file = load_map(self.mp)
        elif event.key() == QtCore.Qt.Key_Left:
            self.mp.lon -= self.mp.step * math.pow(2, 15 - self.mp.zoom)
            self.map_file = load_map(self.mp)
        elif event.key() == QtCore.Qt.Key_Right:
            self.mp.lon += self.mp.step * math.pow(2, 15 - self.mp.zoom)
            self.map_file = load_map(self.mp)
        elif event.key() == QtCore.Qt.Key_Up and self.mp.lat < 85:
            self.mp.lat += self.mp.step * math.pow(2, 15 - self.mp.zoom)
            self.map_file = load_map(self.mp)
        elif event.key() == QtCore.Qt.Key_Down and self.mp.lat > -85:
            self.mp.lat -= self.mp.step * math.pow(2, 15 - self.mp.zoom)
            self.map_file = load_map(self.mp)
        self.pixmap = QPixmap("map.png")
        self.label.setPixmap(self.pixmap)
        event.accept()

    def change_map_type(self):
        self.mp.type = self.map_types[self.comboBox.currentIndex()]
        self.map_file = load_map(self.mp)
        self.pixmap = QPixmap("map.png")
        self.label.setPixmap(self.pixmap)
        self.label.setFocus()

    def search_obj(self):

        print("+".join(self.find_obj.text().split()))
        coords = get_coordinates("+".join(self.find_obj.text().split()))
        print(coords)
        self.mp.lon = coords[0]
        self.mp.lat = coords[1]
        self.mp.cur_lon = coords[0]
        self.mp.cur_lat = coords[1]
        self.map_file = load_map(self.mp)
        self.pixmap = QPixmap("map.png")
        self.label.setPixmap(self.pixmap)
        self.label.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec())
