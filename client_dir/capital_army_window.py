"""Окно армии в столице"""

from collections import namedtuple

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.capital_army_form import Ui_CapitalArmyWindow
from client_dir.hire_menu_window import HireMenuWindow
from client_dir.question_window import QuestionWindow
from client_dir.settings import TOWN_ARMY, SCREEN_RECT, BIG
from client_dir.ui_functions import get_unit_image, update_unit_health, \
    get_image, set_beige_colour, ui_lock, ui_unlock
from client_dir.unit_dialog import UnitDialog
from units_dir.units import main_db
from units_dir.units_factory import AbstractFactory


class CapitalArmyWindow(QMainWindow):
    """
    Класс - окно армии столицы.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла capital_army_form.py
    """

    def __init__(self, instance: any):
        super().__init__()
        # основные переменные
        self.capital = instance
        self.question = False
        self.faction = main_db.current_faction
        self.db_table = main_db.campaigns_dict[self.faction]
        self.factory = AbstractFactory.create_factory(
            self.faction)
        self.support = self.factory.create_support()
        self.special = self.factory.create_special()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.player_gold = 0

        self.InitUI()

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""
        self.ui = Ui_CapitalArmyWindow()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)

        self.ui.pushButtonSlot1.clicked.connect(self._slot1_detailed)
        self.ui.pushButtonSlot2.clicked.connect(self._slot2_detailed)
        self.ui.pushButtonSlot3.clicked.connect(self._slot3_detailed)
        self.ui.pushButtonSlot4.clicked.connect(self._slot4_detailed)
        self.ui.pushButtonSlot5.clicked.connect(self._slot5_detailed)
        self.ui.pushButtonSlot6.clicked.connect(self._slot6_detailed)

        self.ui.swap12.clicked.connect(self.swap_unit_action_12)
        self.ui.swap13.clicked.connect(self.swap_unit_action_13)
        self.ui.swap24.clicked.connect(self.swap_unit_action_24)
        self.ui.swap34.clicked.connect(self.swap_unit_action_34)
        self.ui.swap35.clicked.connect(self.swap_unit_action_35)
        self.ui.swap46.clicked.connect(self.swap_unit_action_46)
        self.ui.swap56.clicked.connect(self.swap_unit_action_56)

        # подкраска элементов
        set_beige_colour(self.ui.swap12)
        set_beige_colour(self.ui.swap13)
        set_beige_colour(self.ui.swap24)
        set_beige_colour(self.ui.swap34)
        set_beige_colour(self.ui.swap35)
        set_beige_colour(self.ui.swap46)
        set_beige_colour(self.ui.swap56)

        set_beige_colour(self.ui.listPlayerUnits)
        set_beige_colour(self.ui.listPlayerSlots)

        self.ui.pushButtonDelete.clicked.connect(
            self.delete_unit_action)

        # self.player_list_update()
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

        self.player_gold = main_db.get_gold(
            main_db.current_player.name, self.faction)
        self.ui.gold.setText(str(self.player_gold))

        self.reset()

        self.show()

    def keyPressEvent(self, event) -> None:
        """Метод обработки нажатия клавиши D"""
        if event.key() == QtCore.Qt.Key_D:
            self.delete_unit_action()

    def update_capital(self) -> None:
        """Обновление лейбла, заполнение картинкой замка"""
        capital_army_bg = self.ui.capitalArmyBG
        capital_army_bg.setPixmap(
            QPixmap(get_image(TOWN_ARMY, self.faction)))
        capital_army_bg.setGeometry(SCREEN_RECT)
        self.hbox.addWidget(capital_army_bg)
        self.setLayout(self.hbox)

    def _update_all_unit_health(self) -> None:
        """Метод обновляющий текущее здоровье всех юнитов"""

        # прорисовка здоровья юнитов игрока
        for num, hp_slot in self.pl_hp_slots_dict.items():
            update_unit_health(
                self.player_unit_by_slot(num),
                hp_slot)

    def back(self) -> None:
        """Кнопка возврата"""
        self.close()

    def button_update(self, unit, button: QtWidgets.QPushButton) -> None:
        """Установка размера кнопки на иконке"""
        self._set_size_by_unit(unit, button)

        self.hbox.addWidget(button)
        self.setLayout(self.hbox)

    def slot_update(self, unit: namedtuple, slot: QtWidgets.QLabel) -> None:
        """Установка gif'ки в иконку юнита"""
        self._set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            get_unit_image(unit)).scaled(
            slot.width(), slot.height()))
        self.hbox.addWidget(slot)
        self.setLayout(self.hbox)

    def player_slots_update(self) -> None:
        """Метод обновляющий список слотов игрока."""
        player_slots = [1, 2, 3, 4, 5, 6]
        self.player_slots_model = QStandardItemModel()
        for slot in player_slots:
            item = QStandardItem(str(slot))
            item.setEditable(False)
            self.player_slots_model.appendRow(item)
        self.ui.listPlayerSlots.setModel(self.player_slots_model)

    def player_list_update(self) -> None:
        """Метод обновляющий список юнитов игрока."""
        # player_units = main_db.show_player_units()
        player_units = main_db.show_db_units(self.db_table)
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

    def reset(self) -> None:
        """Обновить"""
        self._update_all_unit_health()
        self.player_list_update()
        # self.player_slots_update()

        self.is_button_enabled(self.ui.swap12, self.db_table, 2)
        self.is_button_enabled(self.ui.swap34, self.db_table, 4)
        self.is_button_enabled(self.ui.swap56, self.db_table, 6)

    def delete_unit_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Уволить'"""
        selected_slot = self.ui.listPlayerSlots.currentIndex().data()
        unit = main_db.get_unit_by_slot(selected_slot, self.db_table)

        if unit is not None:
            global QUESTION_WINDOW
            text = f'Вы действительно хотите уволить {unit.name}?'
            QUESTION_WINDOW = QuestionWindow(self, text)
            QUESTION_WINDOW.show()

    def confirmation(self) -> None:
        """Подтверждение 'Увольнения' юнита"""
        if self.question:
            selected_slot = self.ui.listPlayerSlots.currentIndex().data()
            main_db.delete_campaign_unit(int(selected_slot))
            self.reset()
            self.capital.main.reset()

    def show_available_units(self, slot: int) -> None:
        """Метод показывающий доступных для покупки
        юнитов данной фракции."""
        global HIRE_WINDOW
        HIRE_WINDOW = HireMenuWindow(slot, self)
        HIRE_WINDOW.show()

        print('Доступные для покупки юниты данной фракции')

    def set_coords_double_slots(self, ui_obj: any) -> None:
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

    def _set_size_by_unit(self, unit: namedtuple, ui_obj: any) -> None:
        """Установка размера иконки по размеру самого юнита"""
        self.set_coords_double_slots(ui_obj)

        try:
            if unit.size == BIG and ui_obj in [
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

            if unit.size == BIG:
                ui_obj.setFixedWidth(225)
                ui_obj.setFixedHeight(127)

            else:
                ui_obj.setFixedWidth(105)
                ui_obj.setFixedHeight(127)
        except AttributeError:
            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def check_and_swap(self, num1: int, num2: int) -> bool:
        """
        Проверить юниты в слотах на наличие и размер.
        Поменять местами вместе с парным юнитом (соседний слот)
        """
        unit1 = main_db.get_unit_by_slot(num1, self.db_table)
        unit2 = main_db.get_unit_by_slot(num2, self.db_table)

        if unit1 is not None \
                and unit2 is not None \
                and unit1.size == BIG \
                and unit2.size == BIG:
            self.swap_unit_action(num1, num2)
            return True

        if unit1 is not None and unit1.size == BIG:
            self.swap_unit_action(num1 - 1, num2 - 1)
            self.swap_unit_action(num1, num2)
            return True

        if unit2 is not None and unit2.size == BIG:
            self.swap_unit_action(num1 - 1, num2 - 1)
            self.swap_unit_action(num1, num2)
            return True

        return False

    def swap_unit_action(self, slot1: int, slot2: int) -> None:
        """Меняет слоты двух юнитов игрока"""
        main_db.update_slot(
            slot1,
            slot2,
            self.db_table)
        self.player_list_update()
        self.reset()
        self._update_all_unit_health()

    def swap_unit_action_12(self) -> None:
        """Меняет местами юнитов игрока в слотах 1 и 2"""
        self.swap_unit_action(1, 2)

    def swap_unit_action_13(self) -> None:
        """Меняет местами юнитов игрока в слотах 1 и 3"""
        if not self.check_and_swap(2, 4):
            self.swap_unit_action(1, 3)

    def swap_unit_action_24(self) -> None:
        """Меняет местами юнитов игрока в слотах 2 и 4"""
        if not self.check_and_swap(2, 4):
            self.swap_unit_action(2, 4)

    def swap_unit_action_34(self) -> None:
        """Меняет местами юнитов игрока в слотах 3 и 4"""
        self.swap_unit_action(3, 4)

    def swap_unit_action_35(self) -> None:
        """Меняет местами юнитов игрока в слотах 3 и 5"""
        if not self.check_and_swap(4, 6):
            self.swap_unit_action(3, 5)

    def swap_unit_action_46(self) -> None:
        """Меняет местами юнитов игрока в слотах 4 и 6"""
        if not self.check_and_swap(4, 6):
            self.swap_unit_action(4, 6)

    def swap_unit_action_56(self) -> None:
        """Меняет местами юнитов игрока в слотах 5 и 6"""
        self.swap_unit_action(5, 6)

    def slot_detailed(self, slot: int) -> None:
        """Метод создающий окно юнита игрока при нажатии на слот."""
        try:
            unit = self.player_unit_by_slot(slot)
            global DETAIL_WINDOW
            DETAIL_WINDOW = UnitDialog(
                unit)
            DETAIL_WINDOW.show()
        except AttributeError:
            self.show_available_units(slot)

    def _slot1_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 1)."""
        self.slot_detailed(1)

    def _slot2_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 2)."""
        self.slot_detailed(2)

    def _slot3_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 3)."""
        self.slot_detailed(3)

    def _slot4_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 4)."""
        self.slot_detailed(4)

    def _slot5_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 5)."""
        self.slot_detailed(5)

    def _slot6_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 6)."""
        self.slot_detailed(6)

    def player_unit_by_slot(self, slot: int) -> namedtuple:
        """Метод получающий юнита игрока по слоту."""
        return main_db.get_unit_by_slot(
            slot,
            self.db_table)

    @staticmethod
    def is_button_enabled(button, db_table, num2):
        """Определяет доступность кнопки по юнитам в слотах"""
        try:
            if main_db.get_unit_by_slot(
                    num2, db_table).size == BIG:
                ui_lock(button)
            else:
                ui_unlock(button)
        except AttributeError:
            ui_unlock(button)
