"""Главное окно столицы"""
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.windows.capital_army_window import CapitalArmyWindow
from client_dir.windows.capital_building_window import CapitalBuildingWindow
from client_dir.forms.capital_main_form import Ui_CapitalWindow
from client_dir.settings import TOWNS, SCREEN_RECT, CAPITAL_ANIM, LD, CAPITAL_CONSTRUCTION, OTHERS
from client_dir.ui_functions import get_image
from units_dir.buildings import FACTIONS
from units_dir.ranking import STARTING_FORMS
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
        # self.animate_capital()

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
        self.show_branch_building('archer')

    def show_branch_building(self, branch: str, building: str):
        """"""
        png = QPixmap(os.path.join(
            CAPITAL_CONSTRUCTION,
            self.faction,
            branch,
            f'{building}.png'))
        print('png', png)
        self.ui.buildingMage1.setScaledContents(True)
        self.ui.buildingMage1.setPixmap(png)

    def branch_settings(self, branch) -> dict:
        """Получение настроек ветви"""
        return FACTIONS.get(self.faction)[branch]

    def get_building_graph(self, branch: str, bname: str, graph: list) -> None:
        """Рекурсивное создание графа зданий/построек"""
        branch_settings = self.branch_settings(branch)

        for val in branch_settings.values():
            if val.bname == bname:
                graph.append(bname)
                if val.prev not in ('', 0):
                    self.get_building_graph(branch, val.prev, graph)
                else:
                    return

    def show_already_built(self) -> None:
        """Отметить уже построенные здания"""
        # self.no_built()
        temp_graph = []

        branches = [
            'fighter',
            'archer',
            'mage',
            'support',
            'others'
        ]

        # получение всех построенных зданий игрока
        for branch in branches:
            buildings = main_db.get_buildings(
                main_db.current_player.name,
                self.faction)._asdict()

            # рекурсивное создание графа уже построенных зданий
            self.get_building_graph(branch, buildings[branch], temp_graph)

            # ставим отметки о постройке зданий
            for building in temp_graph:
                if building != '' and building not in STARTING_FORMS:
                    self.show_branch_building(branch, building)

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
