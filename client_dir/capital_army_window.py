"""Окно армии в столице"""

from collections import namedtuple

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QMimeData, QVariant, Qt, QEvent
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem, QDrag
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QLabel, QWidget

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
    class Label(QLabel):
        def __init__(self, title, parent):
            super().__init__(title, parent)
            self.setAcceptDrops(True)
            self.parent = parent

        def mouseMoveEvent(self, event) -> None:
            mime_data = QMimeData()
            mime_data.setImageData(QVariant(self.pixmap()))
            pixmap = QWidget.grab(self)

            drag = QDrag(self)
            drag.setMimeData(mime_data)

            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())

            if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
                print('moved')

        def dragEnterEvent(self, event) -> None:
            if event.mimeData().hasImage():
                event.accept()
            else:
                event.ignore()

        def dropEvent(self, event) -> None:
            first = int(self.parent.current_label[-1])
            second = int(self.objectName()[-1])
            self.parent.check_and_swap(
                first,
                second,
                self.parent.db_table)

    def __init__(self, parent: any):
        super().__init__()
        # основные переменные
        self.capital = parent
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

        self.ui.slot1 = self.Label('', self)
        self.ui.slot1.setGeometry(QtCore.QRect(488, 100, 105, 127))
        self.ui.slot1.setFrameShape(QtWidgets.QFrame.Panel)
        self.ui.slot1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ui.slot1.setLineWidth(1)
        self.ui.slot1.setMidLineWidth(0)
        self.ui.slot1.setObjectName("slot1")

        self.ui.slot2 = self.Label('', self)
        self.ui.slot2.setGeometry(QtCore.QRect(605, 100, 105, 127))
        self.ui.slot2.setFrameShape(QtWidgets.QFrame.Panel)
        self.ui.slot2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ui.slot2.setLineWidth(1)
        self.ui.slot2.setMidLineWidth(0)
        self.ui.slot2.setObjectName("slot2")

        self.ui.slot3 = self.Label('', self)
        self.ui.slot3.setGeometry(QtCore.QRect(488, 260, 105, 127))
        self.ui.slot3.setFrameShape(QtWidgets.QFrame.Panel)
        self.ui.slot3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ui.slot3.setLineWidth(1)
        self.ui.slot3.setMidLineWidth(0)
        self.ui.slot3.setObjectName("slot3")

        self.ui.slot4 = self.Label('', self)
        self.ui.slot4.setGeometry(QtCore.QRect(605, 260, 105, 127))
        self.ui.slot4.setFrameShape(QtWidgets.QFrame.Panel)
        self.ui.slot4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ui.slot4.setLineWidth(1)
        self.ui.slot4.setMidLineWidth(0)
        self.ui.slot4.setObjectName("slot4")

        self.ui.slot5 = self.Label('', self)
        self.ui.slot5.setGeometry(QtCore.QRect(488, 420, 105, 127))
        self.ui.slot5.setFrameShape(QtWidgets.QFrame.Panel)
        self.ui.slot5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ui.slot5.setLineWidth(1)
        self.ui.slot5.setMidLineWidth(0)
        self.ui.slot5.setObjectName("slot5")

        self.ui.slot6 = self.Label('', self)
        self.ui.slot6.setGeometry(QtCore.QRect(605, 420, 105, 127))
        self.ui.slot6.setFrameShape(QtWidgets.QFrame.Panel)
        self.ui.slot6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ui.slot6.setLineWidth(1)
        self.ui.slot6.setMidLineWidth(0)
        self.ui.slot6.setObjectName("slot6")

        self.ui.slot1.installEventFilter(self)
        self.ui.slot1.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.slot1.customContextMenuRequested \
            .connect(self.slot1_detailed)

        self.ui.slot2.installEventFilter(self)
        self.ui.slot2.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.slot2.customContextMenuRequested \
            .connect(self.slot2_detailed)

        self.ui.slot3.installEventFilter(self)
        self.ui.slot3.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.slot3.customContextMenuRequested \
            .connect(self.slot3_detailed)

        self.ui.slot4.installEventFilter(self)
        self.ui.slot4.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.slot4.customContextMenuRequested \
            .connect(self.slot4_detailed)

        self.ui.slot5.installEventFilter(self)
        self.ui.slot5.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.slot5.customContextMenuRequested \
            .connect(self.slot5_detailed)

        self.ui.slot6.installEventFilter(self)
        self.ui.slot6.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.slot6.customContextMenuRequested \
            .connect(self.slot6_detailed)

        # подкраска элементов
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

        self.current_label = ''
        self.source = ''

        self.show()

    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter:
            self.source = source
            self.current_label = source.objectName()
        return super().eventFilter(source, event)

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

        self.ui.listPlayerUnits.setModel(self.player_units_model)

    def reset(self) -> None:
        """Обновить"""
        self._update_all_unit_health()
        self.player_list_update()

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
        """
        Метод показывающий доступных для покупки
        юнитов данной фракции.
        """
        global HIRE_WINDOW
        HIRE_WINDOW = HireMenuWindow(slot, self)
        HIRE_WINDOW.show()

    def set_coords_double_slots(self, ui_obj: any) -> None:
        """Задание координат для 'двойных' слотов"""
        if ui_obj in [
            self.ui.slot2,
            self.ui.slot4,
            self.ui.slot6,
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
            ]:
                ui_coords = ui_obj.geometry().getCoords()
                new_coords = list(ui_coords)
                new_coords[0] -= 118
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

    def check_and_swap(self, num1: int, num2: int, database: any):
        """
        Проверить юниты в слотах на наличие и размер.
        Поменять местами вместе с парным юнитом (соседний слот).
        """
        unit1 = main_db.get_unit_by_slot(num1, database)
        unit2 = main_db.get_unit_by_slot(num2, database)
        func = self.swap_unit_action

        if unit1 is not None \
                and unit2 is not None \
                and unit1.size == BIG \
                and unit2.size == BIG:
            func(num1, num2)

        elif unit1 is not None \
                and unit1.size == BIG:
            if num2 % 2 != 0:
                func(num2, num1 - 1)
                func(num2 + 1, num1)
            elif num2 % 2 == 0:
                func(num2 - 1, num1 - 1)
                func(num2, num1)

        elif unit1 is not None and unit2 is not None \
                and unit2.size == BIG:
            if num1 % 2 != 0:
                func(num1, num2 - 1)
                func(num1 + 1, num2)
            elif num1 % 2 == 0:
                func(num1 - 1, num2 - 1)
                func(num1, num2)

        elif unit1 is not None:
            func(num1, num2)

    # def check_and_swap(self, num1: int, num2: int) -> bool:
    #     """
    #     Проверить юниты в слотах на наличие и размер.
    #     Поменять местами вместе с парным юнитом (соседний слот)
    #     """
    #     unit1 = main_db.get_unit_by_slot(num1, self.db_table)
    #     unit2 = main_db.get_unit_by_slot(num2, self.db_table)
    #
    #     if unit1 is not None \
    #             and unit2 is not None \
    #             and unit1.size == BIG \
    #             and unit2.size == BIG:
    #         self.swap_unit_action(num1, num2)
    #         return True
    #
    #     if unit1 is not None and unit1.size == BIG:
    #         self.swap_unit_action(num1 - 1, num2 - 1)
    #         self.swap_unit_action(num1, num2)
    #         return True
    #
    #     if unit2 is not None and unit2.size == BIG:
    #         self.swap_unit_action(num1 - 1, num2 - 1)
    #         self.swap_unit_action(num1, num2)
    #         return True
    #
    #     return False

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

    def slot1_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 1)."""
        self.slot_detailed(1)

    def slot2_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 2)."""
        self.slot_detailed(2)

    def slot3_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 3)."""
        self.slot_detailed(3)

    def slot4_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 4)."""
        self.slot_detailed(4)

    def slot5_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 5)."""
        self.slot_detailed(5)

    def slot6_detailed(self) -> None:
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
