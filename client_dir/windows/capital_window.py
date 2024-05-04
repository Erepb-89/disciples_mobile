"""Главное окно столицы"""
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.windows.capital_army_window import CapitalArmyWindow
from client_dir.windows.capital_building_window import CapitalBuildingWindow
from client_dir.forms.capital_main_form import Ui_CapitalWindow
from client_dir.settings import TOWNS, SCREEN_RECT, CAPITAL_ANIM, LD
from client_dir.ui_functions import get_image
from units_dir.units import main_db


class CapitalWindow(QMainWindow):
    """
    Класс - окно столицы.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла capital_main_form.py
    """

    def __init__(self, main: any):
        super().__init__()
        # основные переменные
        self.main = main
        self.faction = main_db.current_faction

        self.InitUI()

    def keyPressEvent(self, event):
        """Метод обработки нажатия клавиш P, S"""
        if event.key() == Qt.Key_P:
            self.show_army()
        if event.key() == Qt.Key_S:
            self.show_building()

    def InitUI(self):
        # Загружаем конфигурацию окна из дизайнера
        self.ui = Ui_CapitalWindow()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)

        self.update_capital()
        if self.faction != LD:
            self.ui.animation.setScaledContents(True)
        else:
            self.ui.animation.setScaledContents(False)
        self.animate_capital()

        self.ui.pushButtonBack.clicked.connect(self.back)
        self.ui.pushButtonArmy.clicked.connect(self.show_army)
        self.ui.pushButtonBuild.clicked.connect(self.show_building)

        self.show()

    def update_capital(self):
        """Обновление лейбла, заполнение картинкой столицы"""
        capital_bg = self.ui.capitalBG
        capital_bg.setPixmap(
            QPixmap(get_image(TOWNS, self.faction)))
        capital_bg.setGeometry(SCREEN_RECT)
        self.hbox.addWidget(capital_bg)
        self.setLayout(self.hbox)

    def animate_capital(self):
        """Отображение GIF-анимации столицы"""
        gif = QMovie(os.path.join(
            CAPITAL_ANIM,
            f"{self.faction}.gif"))
        self.ui.animation.setMovie(gif)
        gif.start()

    def show_army(self):
        """Метод создающий окно армии."""
        global CAPITAL_ARMY_WINDOW
        CAPITAL_ARMY_WINDOW = CapitalArmyWindow(self)
        CAPITAL_ARMY_WINDOW.show()

    def show_building(self):
        """Метод создающий окно строительства."""
        global CAPITAL_BUILDING_WINDOW
        CAPITAL_BUILDING_WINDOW = CapitalBuildingWindow()
        CAPITAL_BUILDING_WINDOW.show()

    def back(self):
        """Кнопка возврата"""
        self.close()
