import os.path

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.campaign_form import Ui_CampaignWindow
from client_dir.fight_window import FightWindow
from client_dir.army_dialog import EnemyArmyDialog
from client_dir.settings import HIRE_SCREEN, MISSION_UNITS
from client_dir.ui_functions import set_size_by_unit, get_unit_image


class CampaignWindow(QMainWindow):
    """
    Класс - окно выбора Кампании.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла campaign_form.py
    """

    def __init__(self, database):
        super().__init__()
        # основные переменные
        self.database = database
        self.current_faction = self.database.current_game_faction
        self.dungeon = None

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

    def show_fight_window(self):
        """Метод создающий окно Битвы."""
        global fight_window
        fight_window = FightWindow(self.database, self.dungeon)
        fight_window.show()

    def mission_slot_detailed(self, database, slot):
        """Метод создающий окно просмотра армии."""
        try:
            global DETAIL_WINDOW
            DETAIL_WINDOW = EnemyArmyDialog(
                database,
                slot)
            DETAIL_WINDOW.show()
        except Exception as err:
            print(err)

    def dungeon_unit_by_slot(self, slot):
        """Метод получающий юнита подземелья по слоту."""
        return self.database.get_unit_by_slot(
            slot,
            self.database.CurrentDungeon)

    def append_campaign_buttons(self):
        """Кнопки миссий в кампании"""
        self.campaign_buttons_dict = {
            1: self.ui.pushButtonSlot_1,
            2: self.ui.pushButtonSlot_2,
            3: self.ui.pushButtonSlot_3,
            4: self.ui.pushButtonSlot_4,
            5: self.ui.pushButtonSlot_5,
            6: self.ui.pushButtonSlot_6,
        }

    def append_campaign_icons(self):
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
    def show_red_frame(gif_slot):
        """Обновление красной рамки в слоте"""
        gif_slot.setStyleSheet("border: 4px solid darkred;")

    @staticmethod
    def show_no_frames(slots_dict, func):
        """Убирает все рамки"""
        for slot in range(1, 7):
            func(slots_dict[slot])

    @staticmethod
    def show_no_frame(gif_slot):
        """Убрать рамки в слоте"""
        gif_slot.setStyleSheet("border: 0px;")

    def unlight_all(self):
        """Снять выделение миссии"""
        self.show_no_frames(self.campaign_buttons_dict, self.show_no_frame)

    def highlight_selected_1(self):
        """Подсветка выбранной миссии"""
        self.unlight_all()
        self.show_red_frame(self.ui.pushButtonSlot_1)

        self.mission_slot_detailed(self.database, 1)
        self.dungeon = f'{self.current_faction}_{1}'

    def highlight_selected_2(self):
        """Подсветка выбранной миссии"""
        self.unlight_all()
        self.show_red_frame(self.ui.pushButtonSlot_2)

        self.mission_slot_detailed(self.database, 2)
        self.dungeon = f'{self.current_faction}_{2}'

    def highlight_selected_3(self):
        """Подсветка выбранной миссии"""
        self.unlight_all()
        self.show_red_frame(self.ui.pushButtonSlot_3)

        self.mission_slot_detailed(self.database, 3)
        self.dungeon = f'{self.current_faction}_{3}'

    def highlight_selected_4(self):
        """Подсветка выбранной миссии"""
        self.unlight_all()
        self.show_red_frame(self.ui.pushButtonSlot_4)

        self.mission_slot_detailed(self.database, 4)
        self.dungeon = f'{self.current_faction}_{4}'

    def highlight_selected_5(self):
        """Подсветка выбранной миссии"""
        self.unlight_all()
        self.show_red_frame(self.ui.pushButtonSlot_5)

        self.mission_slot_detailed(self.database, 5)
        self.dungeon = f'{self.current_faction}_{5}'

    def highlight_selected_6(self):
        """Подсветка выбранной миссии"""
        self.unlight_all()
        self.show_red_frame(self.ui.pushButtonSlot_6)

        self.mission_slot_detailed(self.database, 6)
        self.dungeon = f'{self.current_faction}_{6}'

    @staticmethod
    def _slot_update(unit, slot):
        """Метод обновления иконки"""
        set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            get_unit_image(unit)).scaled(
            slot.width(), slot.height()))

    def mission_list_update(self):
        """Обновление иконок миссий кампании"""
        for num, icon_slot in self.campaign_icons_dict.items():
            unit = self.database.get_unit_by_name(
                MISSION_UNITS[self.current_faction][num])

            self._slot_update(
                unit,
                icon_slot)

    def back(self):
        """Кнопка возврата"""
        self.close()
