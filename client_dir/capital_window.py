import os.path

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.capital_army_window import CapitalArmyWindow
from client_dir.capital_building_window import CapitalBuildingWindow
from client_dir.capital_main_form import Ui_CapitalWindow
from client_dir.settings import TOWNS, ELVEN_PLUG, SCREEN_RECT


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
            self.show_army()

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
            QPixmap(self.get_image(self.faction)))
        capital_bg.setGeometry(SCREEN_RECT)
        self.hbox.addWidget(capital_bg)
        self.setLayout(self.hbox)

    def get_image(self, faction):
        """Достаем картинку фракции"""
        try:
            return os.path.join(TOWNS, f"{faction}.png")
        except:
            return os.path.join(TOWNS, ELVEN_PLUG)

    def show_army(self):
        """Метод создающий окно армии."""
        global capital_army_window
        capital_army_window = CapitalArmyWindow(self.database)
        capital_army_window.show()

    def show_building(self):
        """Метод создающий окно строительства."""
        # try:
        global capital_building_window
        capital_building_window = CapitalBuildingWindow(self.database)
        capital_building_window.show()
        # except Exception as err:
        #     print(err)

    def back(self):
        """Кнопка возврата"""
        self.close()
