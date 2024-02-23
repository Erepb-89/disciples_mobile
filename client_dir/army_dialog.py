"""Диалог показывает окно вражеской армии"""
import os
from collections import namedtuple

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog

from client_dir.settings import BACKGROUND, ARMY_BG, BIG, PORTRAITS
from client_dir.ui_functions import slot_update, button_update, \
    get_unit_image, ui_lock, ui_unlock
from client_dir.unit_dialog import UnitDialog
from units_dir.units import main_db


class EnemyArmyDialog(QDialog):
    def __init__(self, dungeon_units: dict):
        super().__init__()
        self.dungeon_units = dungeon_units

        self.setFixedSize(607, 554)
        self.setWindowTitle('Окно армии противника')

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
        self.pushButtonSlot_1 = QtWidgets.QPushButton(self)
        self.pushButtonSlot_1.setGeometry(QtCore.QRect(340, 50, 104, 127))
        self.pushButtonSlot_1.setText("")
        self.pushButtonSlot_1.setFlat(True)
        self.pushButtonSlot_1.setObjectName("pushButtonSlot_1")
        self.pushButtonSlot_5 = QtWidgets.QPushButton(self)
        self.pushButtonSlot_5.setGeometry(QtCore.QRect(340, 330, 104, 127))
        self.pushButtonSlot_5.setText("")
        self.pushButtonSlot_5.setFlat(True)
        self.pushButtonSlot_5.setObjectName("pushButtonSlot_5")
        self.EnemySlot6 = QtWidgets.QLabel(self)
        self.EnemySlot6.setGeometry(QtCore.QRect(457, 330, 104, 127))
        self.EnemySlot6.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot6.setLineWidth(3)
        self.EnemySlot6.setMidLineWidth(0)
        self.EnemySlot6.setObjectName("EnemySlot6")
        self.EnemySlot3 = QtWidgets.QLabel(self)
        self.EnemySlot3.setGeometry(QtCore.QRect(340, 190, 104, 127))
        self.EnemySlot3.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot3.setLineWidth(3)
        self.EnemySlot3.setMidLineWidth(0)
        self.EnemySlot3.setObjectName("EnemySlot3")
        self.pushButtonSlot_4 = QtWidgets.QPushButton(self)
        self.pushButtonSlot_4.setGeometry(QtCore.QRect(457, 190, 104, 127))
        self.pushButtonSlot_4.setText("")
        self.pushButtonSlot_4.setFlat(True)
        self.pushButtonSlot_4.setObjectName("pushButtonSlot_4")
        self.EnemySlot2 = QtWidgets.QLabel(self)
        self.EnemySlot2.setGeometry(QtCore.QRect(457, 50, 104, 127))
        self.EnemySlot2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.EnemySlot2.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot2.setLineWidth(3)
        self.EnemySlot2.setMidLineWidth(0)
        self.EnemySlot2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.EnemySlot2.setObjectName("EnemySlot2")
        self.pushButtonSlot_2 = QtWidgets.QPushButton(self)
        self.pushButtonSlot_2.setGeometry(QtCore.QRect(457, 50, 104, 127))
        self.pushButtonSlot_2.setText("")
        self.pushButtonSlot_2.setFlat(True)
        self.pushButtonSlot_2.setObjectName("pushButtonSlot_2")
        self.pushButtonSlot_6 = QtWidgets.QPushButton(self)
        self.pushButtonSlot_6.setGeometry(QtCore.QRect(457, 330, 104, 127))
        self.pushButtonSlot_6.setText("")
        self.pushButtonSlot_6.setFlat(True)
        self.pushButtonSlot_6.setObjectName("pushButtonSlot_6")
        self.EnemySlot1 = QtWidgets.QLabel(self)
        self.EnemySlot1.setGeometry(QtCore.QRect(340, 50, 104, 127))
        self.EnemySlot1.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot1.setLineWidth(3)
        self.EnemySlot1.setMidLineWidth(0)
        self.EnemySlot1.setObjectName("EnemySlot1")
        self.EnemySlot5 = QtWidgets.QLabel(self)
        self.EnemySlot5.setGeometry(QtCore.QRect(340, 330, 104, 127))
        self.EnemySlot5.setMinimumSize(QtCore.QSize(104, 127))
        self.EnemySlot5.setMaximumSize(QtCore.QSize(224, 127))
        self.EnemySlot5.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot5.setLineWidth(3)
        self.EnemySlot5.setMidLineWidth(0)
        self.EnemySlot5.setObjectName("EnemySlot5")
        self.pushButtonSlot_3 = QtWidgets.QPushButton(self)
        self.pushButtonSlot_3.setGeometry(QtCore.QRect(340, 190, 104, 127))
        self.pushButtonSlot_3.setText("")
        self.pushButtonSlot_3.setFlat(True)
        self.pushButtonSlot_3.setObjectName("pushButtonSlot_3")
        self.EnemySlot4 = QtWidgets.QLabel(self)
        self.EnemySlot4.setGeometry(QtCore.QRect(457, 190, 104, 127))
        self.EnemySlot4.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot4.setLineWidth(3)
        self.EnemySlot4.setMidLineWidth(0)
        self.EnemySlot4.setObjectName("EnemySlot4")
        self.unitName = QtWidgets.QLabel(self)
        self.unitName.setGeometry(QtCore.QRect(30, 420, 301, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.unitName.setFont(font)
        self.unitName.setAlignment(QtCore.Qt.AlignCenter)
        self.unitName.setObjectName("unitName")

        self.EnemySlot1.raise_()
        self.EnemySlot5.raise_()
        self.EnemySlot3.raise_()
        self.EnemySlot2.raise_()
        self.EnemySlot4.raise_()
        self.EnemySlot6.raise_()

        self.pushButtonSlot_1.raise_()
        self.pushButtonSlot_2.raise_()
        self.pushButtonSlot_3.raise_()
        self.pushButtonSlot_4.raise_()
        self.pushButtonSlot_5.raise_()
        self.pushButtonSlot_6.raise_()

        # self.armyBG.setPixmap(QPixmap(BACKGROUND))
        self.armyBG.setPixmap(QPixmap(ARMY_BG))
        self.pushButtonSlot_1.clicked.connect(self.en_slot1_detailed)
        self.pushButtonSlot_2.clicked.connect(self.en_slot2_detailed)
        self.pushButtonSlot_3.clicked.connect(self.en_slot3_detailed)
        self.pushButtonSlot_4.clicked.connect(self.en_slot4_detailed)
        self.pushButtonSlot_5.clicked.connect(self.en_slot5_detailed)
        self.pushButtonSlot_6.clicked.connect(self.en_slot6_detailed)

        self.faction = main_db.current_faction

        self.dung_buttons_dict = {
            1: self.pushButtonSlot_1,
            2: self.pushButtonSlot_2,
            3: self.pushButtonSlot_3,
            4: self.pushButtonSlot_4,
            5: self.pushButtonSlot_5,
            6: self.pushButtonSlot_6,
        }

        self._dungeon_list_update()
        self._dungeon_buttons_update()
        self.dungeon_portrait_update()

        QtCore.QMetaObject.connectSlotsByName(self)

    def dungeon_portrait_update(self) -> None:
        """Метод обновляющий портрет лидера подземелья"""
        # определяем сильнейшее существо в отряде по опыту
        units = [main_db.get_unit_by_name(unit)
                 for unit in self.dungeon_units.values() if unit is not None]

        units.sort(key=lambda x: x['exp_per_kill'], reverse=True)
        strongest_unit = units[0]

        self.portrait.setPixmap(QPixmap(
            os.path.join(PORTRAITS, f"{strongest_unit.name}.gif")))
        self.unitName.setText(strongest_unit.name)

    def dungeon_buttons_update(self) -> None:
        """Метод обновляющий кнопки юнитов подземелья"""
        for num, icon_slot in self.dung_buttons_dict.items():
            button_update(
                main_db.get_unit_by_name(self.dungeon_units[num]),
                icon_slot)

    def _dungeon_buttons_update(self) -> None:
        """Метод обновляющий кнопки юнитов подземелья"""
        for num, unit in self.dungeon_units.items():
            if unit is not None:
                button_update(
                    main_db.get_unit_by_name(unit),
                    self.dung_buttons_dict[num])

    def _dungeon_list_update(self) -> None:
        """Метод обновляющий список юнитов подземелья"""
        dung_icons_dict = {
            1: self.EnemySlot1,
            2: self.EnemySlot2,
            3: self.EnemySlot3,
            4: self.EnemySlot4,
            5: self.EnemySlot5,
            6: self.EnemySlot6,
        }

        for num, icon_slot in dung_icons_dict.items():
            if num in self.dungeon_units.keys():
                unit = main_db.get_unit_by_name(self.dungeon_units[num])

                try:
                    if unit.size == BIG:
                        ui_coords = icon_slot.geometry().getCoords()
                        new_coords = list(ui_coords)
                        new_coords[0] -= 119
                        new_coords[2] = 224
                        new_coords[3] = 126
                        icon_slot.setGeometry(*new_coords)
                        self.dung_buttons_dict[num].setGeometry(*new_coords)
                    else:
                        icon_slot.setFixedWidth(105)
                        icon_slot.setFixedHeight(127)
                except AttributeError:
                    icon_slot.setFixedWidth(105)
                    icon_slot.setFixedHeight(127)

                slot_update(
                    unit,
                    icon_slot)
                ui_unlock(self.dung_buttons_dict[num])
            else:
                icon_slot.setPixmap(QPixmap(
                    get_unit_image(None)).scaled(
                    icon_slot.width(), icon_slot.height()))
                ui_lock(self.dung_buttons_dict[num])

    def slot_detailed(self, unit: namedtuple, slot_dialog: any) -> None:
        """Метод создающий окно юнита игрока при нажатии на слот."""
        try:
            global DETAIL_WINDOW
            DETAIL_WINDOW = slot_dialog(
                unit)
            DETAIL_WINDOW.show()
        except AttributeError:
            pass

    def en_slot1_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 1)."""
        unit = main_db.get_unit_by_name(self.dungeon_units[1])
        self.slot_detailed(unit, UnitDialog)

    def en_slot2_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 2)."""
        unit = main_db.get_unit_by_name(self.dungeon_units[2])
        self.slot_detailed(unit, UnitDialog)

    def en_slot3_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 3)."""
        unit = main_db.get_unit_by_name(self.dungeon_units[3])
        self.slot_detailed(unit, UnitDialog)

    def en_slot4_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 4)."""
        unit = main_db.get_unit_by_name(self.dungeon_units[4])
        self.slot_detailed(unit, UnitDialog)

    def en_slot5_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 5)."""
        unit = main_db.get_unit_by_name(self.dungeon_units[5])
        self.slot_detailed(unit, UnitDialog)

    def en_slot6_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 6)."""
        unit = main_db.get_unit_by_name(self.dungeon_units[6])
        self.slot_detailed(unit, UnitDialog)

    def back(self) -> None:
        """Кнопка возврата"""
        self.close()
