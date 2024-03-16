"""Диалог показывает окно вражеской армии"""
import os
from collections import namedtuple

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QMimeData, QVariant, QEvent, Qt
from PyQt5.QtGui import QPixmap, QDrag
from PyQt5.QtWidgets import QDialog, QLabel, QWidget

from client_dir.settings import ARMY_BG, BIG, PORTRAITS
from client_dir.ui_functions import get_unit_image
from client_dir.unit_dialog import UnitDialog
from units_dir.units import main_db


class ArmyDialog(QDialog):
    """Диалог выбранной армии"""

    class Label(QLabel):
        def __init__(self, title, parent_window):
            super().__init__(title, parent_window)
            self.setAcceptDrops(True)
            self.parent_window = parent_window

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
            if event.mimeData().hasImage() \
                    and self.parent_window.player != 'Computer':
                event.accept()
            else:
                event.ignore()

        def dropEvent(self, event) -> None:
            first = int(self.parent_window.current_label[-1])
            second = int(self.objectName()[-1])
            self.parent_window.check_and_swap(
                first,
                second,
                self.parent_window.db_table)

    def __init__(self, units: dict, player: str):
        super().__init__()
        self.units = units
        self.player = player
        self.current_label = ''
        self.source = ''
        self.faction = main_db.current_faction
        self.db_table = main_db.campaigns_dict[self.faction]
        self.res_db_table = main_db.res_campaigns_dict[self.faction]

        self.setFixedSize(607, 554)
        self.setWindowTitle('Окно армии')

        self.armyBG = QtWidgets.QLabel(self)
        self.armyBG.setGeometry(QtCore.QRect(0, 0, 607, 554))
        self.armyBG.setMaximumSize(QtCore.QSize(788, 828))
        self.armyBG.setObjectName("armyBG")
        self.portrait = QtWidgets.QLabel(self)
        self.portrait.setGeometry(QtCore.QRect(30, 60, 300, 380))
        self.portrait.setTextFormat(QtCore.Qt.PlainText)
        self.portrait.setScaledContents(True)
        self.portrait.setAlignment(QtCore.Qt.AlignCenter)
        self.portrait.setObjectName("portrait")

        self.slot1 = self.Label('', self)
        self.slot1.setGeometry(QtCore.QRect(340, 50, 104, 127))
        self.slot1.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot1.setLineWidth(3)
        self.slot1.setMidLineWidth(0)
        self.slot1.setObjectName("Slot1")

        self.slot2 = self.Label('', self)
        self.slot2.setGeometry(QtCore.QRect(457, 50, 104, 127))
        self.slot2.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot2.setLineWidth(3)
        self.slot2.setMidLineWidth(0)
        self.slot2.setObjectName("Slot2")

        self.slot3 = self.Label('', self)
        self.slot3.setGeometry(QtCore.QRect(340, 190, 104, 127))
        self.slot3.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot3.setLineWidth(3)
        self.slot3.setMidLineWidth(0)
        self.slot3.setObjectName("Slot3")

        self.slot4 = self.Label('', self)
        self.slot4.setGeometry(QtCore.QRect(457, 190, 104, 127))
        self.slot4.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot4.setLineWidth(3)
        self.slot4.setMidLineWidth(0)
        self.slot4.setObjectName("Slot4")

        self.slot5 = self.Label('', self)
        self.slot5.setGeometry(QtCore.QRect(340, 330, 104, 127))
        self.slot5.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot5.setLineWidth(3)
        self.slot5.setMidLineWidth(0)
        self.slot5.setObjectName("Slot5")

        self.slot6 = self.Label('', self)
        self.slot6.setGeometry(QtCore.QRect(457, 330, 104, 127))
        self.slot6.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot6.setLineWidth(3)
        self.slot6.setMidLineWidth(0)
        self.slot6.setObjectName("Slot6")

        self.unitName = QtWidgets.QLabel(self)
        self.unitName.setGeometry(QtCore.QRect(30, 420, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.unitName.setFont(font)
        self.unitName.setAlignment(QtCore.Qt.AlignCenter)
        self.unitName.setWordWrap(True)
        self.unitName.setObjectName("unitName")

        self.slot2.raise_()
        self.slot4.raise_()
        self.slot6.raise_()

        self.armyBG.setPixmap(QPixmap(ARMY_BG))

        self.faction = main_db.current_faction

        self.slot1.installEventFilter(self)
        self.slot1.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.slot1.customContextMenuRequested \
            .connect(self.slot1_detailed)

        self.slot2.installEventFilter(self)
        self.slot2.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.slot2.customContextMenuRequested \
            .connect(self.slot2_detailed)

        self.slot3.installEventFilter(self)
        self.slot3.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.slot3.customContextMenuRequested \
            .connect(self.slot3_detailed)

        self.slot4.installEventFilter(self)
        self.slot4.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.slot4.customContextMenuRequested \
            .connect(self.slot4_detailed)

        self.slot5.installEventFilter(self)
        self.slot5.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.slot5.customContextMenuRequested \
            .connect(self.slot5_detailed)

        self.slot6.installEventFilter(self)
        self.slot6.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.slot6.customContextMenuRequested \
            .connect(self.slot6_detailed)

        self.slots_dict = {
            1: self.slot1,
            2: self.slot2,
            3: self.slot3,
            4: self.slot4,
            5: self.slot5,
            6: self.slot6,
        }

        self.right_slots = [
            self.slot2,
            self.slot4,
            self.slot6,
        ]

        if self.player == 'Computer':
            self.dungeon_list_update()
        else:
            self.list_update()
        self.portrait_update()

        QtCore.QMetaObject.connectSlotsByName(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter:
            self.source = source
            self.current_label = source.objectName()
        return super().eventFilter(source, event)

    def portrait_update(self) -> None:
        """Метод обновляющий портрет лидера"""
        # определяем сильнейшее существо в отряде по опыту
        units = [main_db.get_unit_by_name(unit)
                 for unit in self.units.values() if unit is not None]

        units.sort(key=lambda x: x['exp_per_kill'], reverse=True)
        strongest_unit = units[0]

        # если есть лидер, ставим его сильнейшим
        for unit in units:
            if unit.leadership >= 3:
                strongest_unit = unit

        self.portrait.setPixmap(QPixmap(
            os.path.join(PORTRAITS, f"{strongest_unit.name}.gif")))
        self.unitName.setText(strongest_unit.name)

    def set_coords_double_slots(self, ui_obj: any) -> None:
        """Задание координат для 'двойных' слотов"""
        if ui_obj in self.right_slots:
            ui_coords = ui_obj.geometry().getCoords()
            new_coords = list(ui_coords)
            new_coords[0] = 457
            ui_obj.setGeometry(*new_coords)

            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def set_size_by_unit(self, unit, ui_obj: any) -> None:
        """Установка размера иконки по размеру самого юнита"""
        self.set_coords_double_slots(ui_obj)

        try:
            if unit.size == BIG and ui_obj in self.right_slots:
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

    def player_unit_by_slot(self, slot: int) -> namedtuple:
        """Метод получающий юнита игрока по слоту."""
        return main_db.get_unit_by_slot(
            slot,
            self.db_table)

    def get_unit_by_player(self, slot) -> namedtuple:
        """Получние юнита игрока либо компьютера"""
        unit = None
        if self.player == 'Computer':
            unit = main_db.get_unit_by_name(self.units[slot])
        else:
            unit = main_db.get_unit_by_slot(slot, self.db_table)
        return unit

    def check_and_swap(self, num1: int, num2: int, db_table: any):
        """
        Проверить юниты в слотах на наличие и размер.
        Поменять местами вместе с парным юнитом (соседний слот).
        """
        unit1 = main_db.get_unit_by_slot(num1, db_table)
        unit2 = main_db.get_unit_by_slot(num2, db_table)
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

    def swap_unit_action(self, slot1: int, slot2: int) -> None:
        """Меняет слоты двух юнитов игрока"""
        main_db.update_slot(
            slot1,
            slot2,
            self.db_table)
        self.list_update()

    def dungeon_list_update(self) -> None:
        """Метод обновляющий список юнитов подземелья"""
        for num, icon_slot in self.slots_dict.items():
            if num in self.units.keys():
                unit = main_db.get_unit_by_name(self.units[num])
                self.slot_update(unit, icon_slot)

    def list_update(self) -> None:
        """Метод обновляющий список юнитов."""
        for num, slot in self.slots_dict.items():
            self.slot_update(
                self.player_unit_by_slot(num),
                slot)

    def slot_update(self,
                    unit: namedtuple,
                    slot: QLabel) -> None:
        """Установка gif'ки в иконку юнита"""
        self.set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            get_unit_image(unit)).scaled(
            slot.width(), slot.height()))

    @staticmethod
    def slot_detailed(unit: namedtuple, slot_dialog: any) -> None:
        """Метод создающий окно юнита при нажатии на слот."""
        try:
            global DETAIL_WINDOW
            DETAIL_WINDOW = slot_dialog(unit)
            DETAIL_WINDOW.show()
        except AttributeError:
            pass

    def slot1_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 1)."""
        unit = self.get_unit_by_player(1)
        self.slot_detailed(unit, UnitDialog)

    def slot2_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 2)."""
        unit = self.get_unit_by_player(2)
        self.slot_detailed(unit, UnitDialog)

    def slot3_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 3)."""
        unit = self.get_unit_by_player(3)
        self.slot_detailed(unit, UnitDialog)

    def slot4_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 4)."""
        unit = self.get_unit_by_player(4)
        self.slot_detailed(unit, UnitDialog)

    def slot5_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 5)."""
        unit = self.get_unit_by_player(5)
        self.slot_detailed(unit, UnitDialog)

    def slot6_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 6)."""
        unit = self.get_unit_by_player(6)
        self.slot_detailed(unit, UnitDialog)

    def back(self) -> None:
        """Кнопка возврата"""
        self.close()
