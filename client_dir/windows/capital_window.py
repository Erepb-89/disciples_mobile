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
        self.animate_capital()

        self.ui.pushButtonBack.clicked.connect(self.back)
        self.ui.pushButtonArmy.clicked.connect(self.show_army)
        self.ui.pushButtonBuild.clicked.connect(self.show_building)

        self.show_already_built()
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

    def show_branch_building(self, building: str, ui_item):
        """"""
        png = QPixmap(os.path.join(
            CAPITAL_CONSTRUCTION,
            self.faction,
            f'{building}.png'))
        ui_item.setScaledContents(True)
        ui_item.setPixmap(png)

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
        branches = [
            'fighter',
            'archer',
            'mage',
            'support',
            # 'others'
        ]

        slot_dict = {'mage':
                         {0: self.ui.buildingMage_1,
                          1: self.ui.buildingMage_2,
                          2: self.ui.buildingMage_3,
                          3: self.ui.buildingMage_4,
                          4: self.ui.buildingMage_5},
                     'fighter':
                         {0: self.ui.buildingFighter_1,
                          1: self.ui.buildingFighter_2,
                          2: self.ui.buildingFighter_3,
                          3: self.ui.buildingFighter_4,
                          4: self.ui.buildingFighter_5},
                     'archer':
                         {0: self.ui.buildingArcher_1,
                          1: self.ui.buildingArcher_2,
                          2: self.ui.buildingArcher_3,
                          3: self.ui.buildingArcher_4,
                          4: self.ui.buildingArcher_5},
                     'support':
                         {0: self.ui.buildingSupport_1,
                          1: self.ui.buildingSupport_2,
                          2: self.ui.buildingSupport_3,
                          3: self.ui.buildingSupport_4,
                          4: self.ui.buildingSupport_5},
                     'others':
                         {0: self.ui.buildingOthers_1,
                          1: self.ui.buildingOthers_2,
                          2: self.ui.buildingOthers_3},
                     }

        # получение всех построенных зданий игрока
        for branch in branches:
            buildings = main_db.get_buildings(
                main_db.current_player.name,
                self.faction)._asdict()

            temp_graph = []
            # рекурсивное создание графа уже построенных зданий
            self.get_building_graph(branch, buildings[branch], temp_graph)
            reversed_graph = reversed(temp_graph)

            # ставим отметки о постройке зданий
            for num, building in enumerate(reversed_graph):
                if building != '' and building not in STARTING_FORMS:
                    ui_item = slot_dict[branch][num]
                    self.show_branch_building(building, ui_item)

    def show_army(self):
        """Метод создающий окно армии."""
        global CAPITAL_ARMY_WINDOW
        CAPITAL_ARMY_WINDOW = CapitalArmyWindow(self)
        CAPITAL_ARMY_WINDOW.show()

    def show_building(self):
        """Метод создающий окно строительства."""
        global CAPITAL_BUILDING_WINDOW
        CAPITAL_BUILDING_WINDOW = CapitalBuildingWindow(self)
        CAPITAL_BUILDING_WINDOW.show()

    def back(self):
        """Кнопка возврата"""
        self.close()
