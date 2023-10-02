import os.path

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.capital_army_window import CapitalArmyWindow
from client_dir.capital_building_window import CapitalBuildingWindow
from client_dir.capital_main_form import Ui_CapitalWindow
from client_dir.settings import TOWNS, SCREEN_RECT
from client_dir.ui_functions import get_image


class CapitalWindow(QMainWindow):
    """
    Класс - окно выбора фракции.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла choose_faction_form.py
    """

    def __init__(self, database):
        super().__init__()
        # основные переменные
        self.database = database
        self.faction = self.database.current_game_faction

        self.InitUI()

    def keyPPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_P:
            self.show_army()

    def keySPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_S:
            self.show_building()

    def InitUI(self):
        # Загружаем конфигурацию окна из дизайнера
        self.ui = Ui_CapitalWindow()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)

        self.update_capital()
        self.ui.pushButtonBack.clicked.connect(self.back)
        self.ui.pushButtonArmy.clicked.connect(self.show_army)
        self.ui.pushButtonBuild.clicked.connect(self.show_building)

        self.show()

    def update_capital(self):
        """Обновление лейбла, заполнение картинкой замка"""
        capital_bg = self.ui.capitalBG
        capital_bg.setPixmap(
            QPixmap(get_image(TOWNS, self.faction)))
        capital_bg.setGeometry(SCREEN_RECT)
        self.hbox.addWidget(capital_bg)
        self.setLayout(self.hbox)

    def show_army(self):
        """Метод создающий окно армии."""
        global CAPITAL_ARMY_WINDOW
        CAPITAL_ARMY_WINDOW = CapitalArmyWindow(self.database)
        CAPITAL_ARMY_WINDOW.show()

    def show_building(self):
        """Метод создающий окно строительства."""
        global CAPITAL_BUILDING_WINDOW
        CAPITAL_BUILDING_WINDOW = CapitalBuildingWindow(self.database)
        CAPITAL_BUILDING_WINDOW.show()

    def back(self):
        """Кнопка возврата"""
        self.close()
