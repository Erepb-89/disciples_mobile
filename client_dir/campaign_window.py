from typing import Callable, Dict

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.campaign_form import Ui_CampaignWindow
from client_dir.fight_window import FightWindow
from client_dir.army_dialog import EnemyArmyDialog
from client_dir.settings import MISSION_UNITS
from client_dir.ui_functions import slot_update
from units_dir.units_factory import Unit


class CampaignWindow(QMainWindow):
    """
    Класс - окно выбора Кампании.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла campaign_form.py
    """

    def __init__(self, database: any):
        super().__init__()
        # основные переменные
        self.database = database
        self.current_faction = self.database.current_game_faction
        self.dungeon = None
        self.campaign_buttons_dict = {}
        self.campaign_icons_dict = {}

        self.InitUI()

    def InitUI(self):
        # Загружаем конфигурацию окна из дизайнера
        self.ui = Ui_CampaignWindow()
        self.ui.setupUi(self)
        self.hbox = QHBoxLayout(self)

        self.ui.pushButtonFight.clicked.connect(
            self.show_fight_window)
        self.ui.ExitButton.clicked.connect(self.back)

        self.ui.pushButtonSlot_1.clicked.connect(
            self.highlight_selected_1)
        self.ui.pushButtonSlot_2.clicked.connect(
            self.highlight_selected_2)
        self.ui.pushButtonSlot_3.clicked.connect(
            self.highlight_selected_3)
        self.ui.pushButtonSlot_4.clicked.connect(
            self.highlight_selected_4)
        self.ui.pushButtonSlot_5.clicked.connect(
            self.highlight_selected_5)
        self.ui.pushButtonSlot_6.clicked.connect(
            self.highlight_selected_6)

        self.append_campaign_buttons()
        self.append_campaign_icons()
        self.show_red_frame(self.ui.pushButtonSlot_1)
        self.dungeon = f'{self.current_faction}_{1}'

        self.mission_list_update()

        self.show()

    def show_fight_window(self) -> None:
        """Метод создающий окно Битвы."""
        global FIGHT_WINDOW
        FIGHT_WINDOW = FightWindow(self.database, self.dungeon)
        FIGHT_WINDOW.show()

    @staticmethod
    def mission_slot_detailed(database: any, slot: int) -> None:
        """Метод создающий окно просмотра армии."""
        global DETAIL_WINDOW
        DETAIL_WINDOW = EnemyArmyDialog(
            database,
            slot)
        DETAIL_WINDOW.show()

    def dungeon_unit_by_slot(self, slot: int) -> Unit:
        """Метод получающий юнита подземелья по слоту."""
        return self.database.get_unit_by_slot(
            slot,
            self.database.CurrentDungeon)

    def append_campaign_buttons(self) -> None:
        """Кнопки миссий в кампании"""
        self.campaign_buttons_dict = {
            1: self.ui.pushButtonSlot_1,
            2: self.ui.pushButtonSlot_2,
            3: self.ui.pushButtonSlot_3,
            4: self.ui.pushButtonSlot_4,
            5: self.ui.pushButtonSlot_5,
            6: self.ui.pushButtonSlot_6,
        }

    def append_campaign_icons(self) -> None:
        """Иконки миссий в кампании"""
        self.campaign_icons_dict = {
            1: self.ui.slot1,
            2: self.ui.slot2,
            3: self.ui.slot3,
            4: self.ui.slot4,
            5: self.ui.slot5,
            6: self.ui.slot6,
        }

    @staticmethod
    def show_red_frame(gif_slot: QtWidgets.QPushButton) -> None:
        """Обновление красной рамки в слоте"""
        gif_slot.setStyleSheet("border: 4px solid darkred;")

    @staticmethod
    def show_no_frames(slots_dict: Dict[int, QtWidgets.QPushButton],
                       func: Callable) -> None:
        """Убирает все рамки"""
        for slot in range(1, 7):
            func(slots_dict[slot])

    @staticmethod
    def show_no_frame(gif_slot: QtWidgets.QPushButton) -> None:
        """Убрать рамки в слоте"""
        gif_slot.setStyleSheet("border: 0px;")

    def unlight_all(self) -> None:
        """Снять выделение миссии"""
        self.show_no_frames(self.campaign_buttons_dict, self.show_no_frame)

    def highlight_selected_1(self) -> None:
        """Подсветка выбранной миссии"""
        number = 1
        self.unlight_all()
        self.show_red_frame(self.ui.pushButtonSlot_1)

        self.mission_slot_detailed(self.database, number)
        self.dungeon = f'{self.current_faction}_{number}'

    def highlight_selected_2(self) -> None:
        """Подсветка выбранной миссии"""
        number = 2
        self.unlight_all()
        self.show_red_frame(self.ui.pushButtonSlot_2)

        self.mission_slot_detailed(self.database, number)
        self.dungeon = f'{self.current_faction}_{number}'

    def highlight_selected_3(self) -> None:
        """Подсветка выбранной миссии"""
        number = 3
        self.unlight_all()
        self.show_red_frame(self.ui.pushButtonSlot_3)

        self.mission_slot_detailed(self.database, number)
        self.dungeon = f'{self.current_faction}_{number}'

    def highlight_selected_4(self) -> None:
        number = 4
        """Подсветка выбранной миссии"""
        self.unlight_all()
        self.show_red_frame(self.ui.pushButtonSlot_4)

        self.mission_slot_detailed(self.database, number)
        self.dungeon = f'{self.current_faction}_{number}'

    def highlight_selected_5(self) -> None:
        """Подсветка выбранной миссии"""
        number = 5
        self.unlight_all()
        self.show_red_frame(self.ui.pushButtonSlot_5)

        self.mission_slot_detailed(self.database, number)
        self.dungeon = f'{self.current_faction}_{number}'

    def highlight_selected_6(self) -> None:
        """Подсветка выбранной миссии"""
        number = 6
        self.unlight_all()
        self.show_red_frame(self.ui.pushButtonSlot_6)

        self.mission_slot_detailed(self.database, number)
        self.dungeon = f'{self.current_faction}_{number}'

    def mission_list_update(self) -> None:
        """Обновление иконок миссий кампании"""
        for num, icon_slot in self.campaign_icons_dict.items():
            unit = self.database.get_unit_by_name(
                MISSION_UNITS[self.current_faction][num])

            slot_update(
                unit,
                icon_slot)

    def back(self) -> None:
        """Кнопка возврата"""
        self.close()
