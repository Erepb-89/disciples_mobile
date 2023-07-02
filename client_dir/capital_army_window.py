"""Окно армии в столице"""

import os.path

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.capital_army_form import Ui_CapitalArmyWindow
from client_dir.hire_menu_window import HireMenuWindow
from client_dir.settings import TOWN_ARMY, ELVEN_PLUG, SCREEN_RECT
from client_dir.ui_functions import get_unit_image, set_size_by_unit
from client_dir.unit_dialog import UnitDialog
from units_dir.units_factory import AbstractFactory


class CapitalArmyWindow(QMainWindow):
    """
    Класс - окно выбора фракции.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла capital_army_form.py
    """

    def __init__(self, database):
        super().__init__()
        # основные переменные
        self.database = database
        self.faction = self.database.current_game_faction
        self.factory = AbstractFactory.create_factory(
            self.faction)
        self.support = self.factory.create_support()
        self.special = self.factory.create_special()

        self.InitUI()

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""
        self.ui = Ui_CapitalArmyWindow()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)

        self.ui.pushButtonSlot1.clicked.connect(
            self.slot1_detailed)
        self.ui.pushButtonSlot2.clicked.connect(
            self.slot2_detailed)
        self.ui.pushButtonSlot3.clicked.connect(
            self.slot3_detailed)
        self.ui.pushButtonSlot4.clicked.connect(
            self.slot4_detailed)
        self.ui.pushButtonSlot5.clicked.connect(
            self.slot5_detailed)
        self.ui.pushButtonSlot6.clicked.connect(
            self.slot6_detailed)

        self.ui.pushButtonDelete.clicked.connect(
            self.delete_unit_action)

        self.player_list_update()
        self.player_slots_update()

        self.update_capital()
        self.ui.pushButtonBack.clicked.connect(self.back)

        self.pl_hp_slots_dict = {
            1: self.ui.hpSlot1,
            2: self.ui.hpSlot2,
            3: self.ui.hpSlot3,
            4: self.ui.hpSlot4,
            5: self.ui.hpSlot5,
            6: self.ui.hpSlot6,
        }

        self._update_all_unit_health()
        self.show()

    def keyPressEvent(self, event):
        """Метод обработки нажатия клавиши D"""
        if event.key() == QtCore.Qt.Key_D:
            self.delete_unit_action()

    def update_capital(self):
        """Обновление лейбла, заполнение картинкой замка"""
        capital_army_bg = self.ui.capitalArmyBG
        capital_army_bg.setPixmap(
            QPixmap(self.get_image(self.faction)))
        capital_army_bg.setGeometry(SCREEN_RECT)
        self.hbox.addWidget(capital_army_bg)
        self.setLayout(self.hbox)

    @staticmethod
    def get_image(faction):
        """Достаем картинку найма армии фракции"""
        try:
            return os.path.join(TOWN_ARMY, f"{faction}.png")
        except BaseException:
            return os.path.join(TOWN_ARMY, ELVEN_PLUG)

    def _update_all_unit_health(self):
        """Метод обновляющий текущее здоровье всех юнитов"""

        # прорисовка здоровья юнитов игрока
        for num, hp_slot in self.pl_hp_slots_dict.items():
            self._update_unit_health(
                self.player_unit_by_slot(num),
                hp_slot)

    @staticmethod
    def _update_unit_health(unit, slot):
        """Обновление здоровья юнита"""
        try:
            slot.setText(f'{unit.curr_health}/{unit.health}')
        except BaseException:
            slot.setText('')

    def back(self):
        """Кнопка возврата"""
        self.close()

    def button_update(self, unit, button):
        """Установка размера кнопки на иконке"""
        self._set_size_by_unit(unit, button)

        self.hbox.addWidget(button)
        self.setLayout(self.hbox)

    def slot_update(self, unit, slot):
        """Установка gif'ки в иконку юнита"""
        self._set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            get_unit_image(unit)).scaled(
            slot.width(), slot.height()))
        self.hbox.addWidget(slot)
        self.setLayout(self.hbox)

    # @staticmethod
    # def get_unit_image(unit):
    #     """Метод получающий лицо юнита"""
    #     try:
    #         return os.path.join(UNIT_ICONS, f"{unit.name} {ICON}")
    #     except BaseException:
    #         return os.path.join(UNIT_ICONS, PLUG)

    def player_slots_update(self):
        """Метод обновляющий список слотов игрока."""
        player_slots = [1, 2, 3, 4, 5, 6]
        self.player_slots_model = QStandardItemModel()
        for slot in player_slots:
            item = QStandardItem(str(slot))
            item.setEditable(False)
            self.player_slots_model.appendRow(item)
        self.ui.listPlayerSlots.setModel(self.player_slots_model)

    def player_list_update(self):
        """Метод обновляющий список юнитов игрока."""
        # player_units = self.database.show_player_units()
        player_units = self.database.show_db_units(self.database.PlayerUnits)
        self.player_units_model = QStandardItemModel()
        for i in player_units:
            item = QStandardItem(i.name)
            item.setEditable(False)
            self.player_units_model.appendRow(item)

        self.slot_update(self.player_unit_by_slot(1),
                         self.ui.slot1)
        self.slot_update(self.player_unit_by_slot(2),
                         self.ui.slot2)
        self.slot_update(self.player_unit_by_slot(3),
                         self.ui.slot3)
        self.slot_update(self.player_unit_by_slot(4),
                         self.ui.slot4)
        self.slot_update(self.player_unit_by_slot(5),
                         self.ui.slot5)
        self.slot_update(self.player_unit_by_slot(6),
                         self.ui.slot6)

        self.button_update(
            self.player_unit_by_slot(1),
            self.ui.pushButtonSlot1)
        self.button_update(
            self.player_unit_by_slot(2),
            self.ui.pushButtonSlot2)
        self.button_update(
            self.player_unit_by_slot(3),
            self.ui.pushButtonSlot3)
        self.button_update(
            self.player_unit_by_slot(4),
            self.ui.pushButtonSlot4)
        self.button_update(
            self.player_unit_by_slot(5),
            self.ui.pushButtonSlot5)
        self.button_update(
            self.player_unit_by_slot(6),
            self.ui.pushButtonSlot6)

        self.ui.listPlayerUnits.setModel(self.player_units_model)

    def units_list_update(self):
        """Метод обновляющий список юнитов."""
        all_units = self.database.show_all_units()

        self.units_model = QStandardItemModel()
        for i in all_units:
            item = QStandardItem(i.name)
            item.setEditable(False)
            self.units_model.appendRow(item)
        self.ui.listAllUnits.setModel(self.units_model)

    def delete_unit_action(self):
        """Метод обработчик нажатия кнопки 'Уволить'"""
        try:
            selected_slot = self.ui.listPlayerSlots.currentIndex().data()
            self.database.delete_player_unit(int(selected_slot))
            self.player_list_update()
        except Exception as err:
            print(f'Error: {err}')

    def show_available_units(self, slot):
        """Метод показывающий доступных для покупки
        юнитов данной фракции."""
        try:
            global HIRE_WINDOW
            HIRE_WINDOW = HireMenuWindow(self.database, slot)
            HIRE_WINDOW.show()
            self.close()
        except Exception as err:
            print(err)

        print('Доступные для покупки юниты данной фракции')
        # print(self.fighter.add_to_band(5))


    def set_coords_double_slots(self, ui_obj):
        """Задание координат для 'двойных' слотов либо кнопок"""
        if ui_obj in [
            self.ui.slot2,
            self.ui.slot4,
            self.ui.slot6,
            self.ui.pushButtonSlot2,
            self.ui.pushButtonSlot4,
            self.ui.pushButtonSlot6,
        ]:
            ui_coords = ui_obj.geometry().getCoords()
            new_coords = list(ui_coords)
            new_coords[0] = 606
            ui_obj.setGeometry(*new_coords)

            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def _set_size_by_unit(self, unit, ui_obj):
        """Установка размера иконки по размеру самого юнита"""
        self.set_coords_double_slots(ui_obj)

        try:
            if unit.size == "Большой" and ui_obj in [
                self.ui.slot2,
                self.ui.slot4,
                self.ui.slot6,
                self.ui.pushButtonSlot2,
                self.ui.pushButtonSlot4,
                self.ui.pushButtonSlot6,
            ]:
                ui_coords = ui_obj.geometry().getCoords()
                new_coords = list(ui_coords)
                new_coords[0] -= 117
                new_coords[2] = 224
                new_coords[3] = 126
                ui_obj.setGeometry(*new_coords)

            if unit.size == "Большой":
                ui_obj.setFixedWidth(225)
                ui_obj.setFixedHeight(127)

            elif unit.size == "Обычный":
                ui_obj.setFixedWidth(105)
                ui_obj.setFixedHeight(127)
        except AttributeError:
            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def slot_detailed(self, database, slot):
        """Метод создающий окно юнита игрока при нажатии на слот."""
        try:
            unit = self.player_unit_by_slot(slot)
            global DETAIL_WINDOW
            DETAIL_WINDOW = UnitDialog(
                database,
                unit)
            DETAIL_WINDOW.show()
        except BaseException:
            self.show_available_units(slot)

    def slot1_detailed(self):
        """Метод создающий окно юнита игрока (слот 1)."""
        self.slot_detailed(self.database.PlayerUnits, 1)

    def slot2_detailed(self):
        """Метод создающий окно юнита игрока (слот 2)."""
        self.slot_detailed(self.database.PlayerUnits, 2)

    def slot3_detailed(self):
        """Метод создающий окно юнита игрока (слот 3)."""
        self.slot_detailed(self.database.PlayerUnits, 3)

    def slot4_detailed(self):
        """Метод создающий окно юнита игрока (слот 4)."""
        self.slot_detailed(self.database.PlayerUnits, 4)

    def slot5_detailed(self):
        """Метод создающий окно юнита игрока (слот 5)."""
        self.slot_detailed(self.database.PlayerUnits, 5)

    def slot6_detailed(self):
        """Метод создающий окно юнита игрока (слот 6)."""
        self.slot_detailed(self.database.PlayerUnits, 6)

    def player_unit_by_slot(self, slot):
        """Метод получающий юнита игрока по слоту."""
        return self.database.get_unit_by_slot(
            slot,
            self.database.PlayerUnits)
