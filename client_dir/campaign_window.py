import os
from typing import Callable, Dict

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.campaign_form import Ui_CampaignWindow
from client_dir.fight_window import FightWindow
from client_dir.army_dialog import EnemyArmyDialog
from client_dir.settings import MISSION_UNITS, BACKGROUND
from client_dir.ui_functions import slot_update, button_update
from units_dir.mission_generator import unit_selector, \
    setup_6, setup_5, setup_4, setup_3, setup_2, boss_setup
from units_dir.units_factory import Unit


class CampaignWindow(QMainWindow):
    """
    Класс - окно выбора Кампании.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла campaign_form.py
    """

    def __init__(self, database: any, instance: any):
        super().__init__()
        # основные переменные
        self.name = 'CampaignWindow'
        self.database = database
        self.main = instance
        self.current_faction = self.database.current_game_faction
        self.dungeon = ''
        self.dungeon_num = 1
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
        self.ui.pushButtonSlot_7.clicked.connect(
            self.highlight_selected_7)
        self.ui.pushButtonSlot_8.clicked.connect(
            self.highlight_selected_8)
        self.ui.pushButtonSlot_9.clicked.connect(
            self.highlight_selected_9)
        self.ui.pushButtonSlot_10.clicked.connect(
            self.highlight_selected_10)
        self.ui.pushButtonSlot_11.clicked.connect(
            self.highlight_selected_11)
        self.ui.pushButtonSlot_12.clicked.connect(
            self.highlight_selected_12)
        self.ui.pushButtonSlot_13.clicked.connect(
            self.highlight_selected_13)
        self.ui.pushButtonSlot_14.clicked.connect(
            self.highlight_selected_14)
        self.ui.pushButtonSlot_15.clicked.connect(
            self.highlight_selected_15)

        self.set_campaign_image()
        self.append_campaign_buttons()
        self.append_campaign_icons()
        self.show_red_frame(self.ui.pushButtonSlot_1)
        self.dungeon = f'{self.current_faction}_{1}'

        self.update_all_missions()

        self.mission_list_update()
        # self.mission_buttons_update()

        self.show()

    def reset(self) -> None:
        """Обновить"""
        pass

    def set_campaign_image(self) -> None:
        """Установить картинку кампании"""
        self.ui.campaignBG.setPixmap(QPixmap(BACKGROUND))
        # self.ui.campaignBG.setGeometry(QtCore.QRect(0, 0, 4, 4))
        self.ui.campaignBG.setGeometry(QtCore.QRect(0, 0, 1500, 827))

    def update_all_missions(self) -> None:
        """Обновляет состав армии для каждой миссии"""
        start_level = 1
        mid_level = 2

        self.mission_1 = unit_selector(start_level, setup_4)
        self.mission_2 = unit_selector(start_level, setup_4)
        self.mission_3 = unit_selector(start_level, setup_5)
        self.mission_4 = unit_selector(start_level, setup_5)
        self.mission_5 = unit_selector(start_level, setup_5)
        self.mission_6 = unit_selector(mid_level, setup_3)
        self.mission_7 = unit_selector(mid_level, setup_3)
        self.mission_8 = unit_selector(mid_level, setup_3)
        self.mission_9 = unit_selector(mid_level, setup_3)
        self.mission_10 = unit_selector(mid_level, setup_4)
        self.mission_11 = unit_selector(mid_level, setup_4)
        self.mission_12 = unit_selector(mid_level, setup_4)
        self.mission_13 = unit_selector(mid_level, setup_5)
        self.mission_14 = unit_selector(mid_level, setup_5)
        self.mission_15 = unit_selector(6, boss_setup)

        self.all_missions = {
            1: self.mission_1,
            2: self.mission_2,
            3: self.mission_3,
            4: self.mission_4,
            5: self.mission_5,
            6: self.mission_6,
            7: self.mission_7,
            8: self.mission_8,
            9: self.mission_9,
            10: self.mission_10,
            11: self.mission_11,
            12: self.mission_12,
            13: self.mission_13,
            14: self.mission_14,
            15: self.mission_15,
        }

        # self.database.add_dungeons(self.all_missions)

    def show_fight_window(self) -> None:
        """Метод создающий окно Битвы."""
        # curr_dungeon = self.all_missions[self.dungeon_num]

        global FIGHT_WINDOW
        FIGHT_WINDOW = FightWindow(self.database, self.dungeon, self)
        FIGHT_WINDOW.show()

    @staticmethod
    def mission_slot_detailed(database: any,
                              dungeon_units: dict) -> None:
        """Метод создающий окно просмотра армии."""
        global DETAIL_WINDOW
        DETAIL_WINDOW = EnemyArmyDialog(
            database,
            dungeon_units)
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
            7: self.ui.pushButtonSlot_7,
            8: self.ui.pushButtonSlot_8,
            9: self.ui.pushButtonSlot_9,
            10: self.ui.pushButtonSlot_10,
            11: self.ui.pushButtonSlot_11,
            12: self.ui.pushButtonSlot_12,
            13: self.ui.pushButtonSlot_13,
            14: self.ui.pushButtonSlot_14,
            15: self.ui.pushButtonSlot_15,
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
            7: self.ui.slot7,
            8: self.ui.slot8,
            9: self.ui.slot9,
            10: self.ui.slot10,
            11: self.ui.slot11,
            12: self.ui.slot12,
            13: self.ui.slot13,
            14: self.ui.slot14,
            15: self.ui.slot15,
        }

    def mission_list_update(self) -> None:
        """Обновление иконок миссий кампании"""
        for num, mission in self.all_missions.items():
            # сделать добавление миссий в базу в таблицу dungeons
            # f'{self.current_faction}_{number}'

            units = [self.database.get_unit_by_name(unit)
                     for unit in mission.values()]

            # определяем сильнейшее существо в отряде по опыту
            units.sort(key=lambda x: x['exp_per_kill'], reverse=True)
            strongest_unit = units[0]

            slot_update(
                strongest_unit,
                self.campaign_icons_dict[num])

            button_update(
                strongest_unit,
                self.campaign_buttons_dict[num])

    def mission_buttons_update(self) -> None:
        """Обновление кнопок миссий кампании"""
        for num, button in self.campaign_buttons_dict.items():
            unit = self.database.get_unit_by_name(
                MISSION_UNITS[self.current_faction][num])

            button_update(
                unit,
                button)

    @staticmethod
    def show_red_frame(gif_slot: QtWidgets.QPushButton) -> None:
        """Обновление красной рамки в слоте"""
        gif_slot.setStyleSheet("border: 4px solid darkred;")

    @staticmethod
    def show_no_frames(slots_dict: Dict[int, QtWidgets.QPushButton],
                       func: Callable) -> None:
        """Убирает все рамки"""
        for slot in range(1, 16):
            func(slots_dict[slot])

    @staticmethod
    def show_no_frame(gif_slot: QtWidgets.QPushButton) -> None:
        """Убрать рамки в слоте"""
        gif_slot.setStyleSheet("border: 0px;")

    def unlight_all(self) -> None:
        """Снять выделение миссии"""
        self.show_no_frames(self.campaign_buttons_dict, self.show_no_frame)

    def highlight_selected(self, number) -> None:
        """Подсветка выбранной миссии"""
        self.unlight_all()

        for num, button in self.campaign_buttons_dict.items():
            if num == number:
                self.show_red_frame(button)
                self.mission_slot_detailed(self.database, self.all_missions[num])

        self.dungeon = f'{self.current_faction}_{number}'
        self.dungeon_num = number

    def highlight_selected_1(self) -> None:
        """Подсветка миссии 1"""
        self.highlight_selected(1)

    def highlight_selected_2(self) -> None:
        """Подсветка миссии 2"""
        self.highlight_selected(2)

    def highlight_selected_3(self) -> None:
        """Подсветка миссии 3"""
        self.highlight_selected(3)

    def highlight_selected_4(self) -> None:
        """Подсветка миссии 4"""
        self.highlight_selected(4)

    def highlight_selected_5(self) -> None:
        """Подсветка миссии 5"""
        self.highlight_selected(5)

    def highlight_selected_6(self) -> None:
        """Подсветка миссии 6"""
        self.highlight_selected(6)

    def highlight_selected_7(self) -> None:
        """Подсветка миссии 7"""
        self.highlight_selected(7)

    def highlight_selected_8(self) -> None:
        """Подсветка миссии 8"""
        self.highlight_selected(8)

    def highlight_selected_9(self) -> None:
        """Подсветка миссии 9"""
        self.highlight_selected(9)

    def highlight_selected_10(self) -> None:
        """Подсветка миссии 10"""
        self.highlight_selected(10)

    def highlight_selected_11(self) -> None:
        """Подсветка миссии 11"""
        self.highlight_selected(11)

    def highlight_selected_12(self) -> None:
        """Подсветка миссии 12"""
        self.highlight_selected(12)

    def highlight_selected_13(self) -> None:
        """Подсветка миссии 13"""
        self.highlight_selected(13)

    def highlight_selected_14(self) -> None:
        """Подсветка миссии 14"""
        self.highlight_selected(14)

    def highlight_selected_15(self) -> None:
        """Подсветка миссии 15"""
        self.highlight_selected(15)

    def back(self) -> None:
        """Кнопка возврата"""
        self.close()
