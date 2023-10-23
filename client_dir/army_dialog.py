"""Диалог показывает окно вражеской армии"""
from collections import namedtuple

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog

from client_dir.settings import BACKGROUND
from client_dir.ui_functions import slot_update
from client_dir.unit_dialog import UnitDialog
from units_dir.mission_generator import unit_selector, setup_6


class EnemyArmyDialog(QDialog):
    def __init__(self, database: any, slot: int):
        super().__init__()
        self.database = database

        self.setFixedSize(320, 490)
        self.setWindowTitle('Окно армии противника')

        self.armyBG = QtWidgets.QLabel(self)
        self.armyBG.setGeometry(QtCore.QRect(0, 0, 320, 490))
        self.armyBG.setMinimumSize(QtCore.QSize(13, 13))
        self.armyBG.setMaximumSize(QtCore.QSize(320, 490))
        self.armyBG.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.armyBG.setAutoFillBackground(True)
        self.armyBG.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.armyBG.setFrameShadow(QtWidgets.QFrame.Plain)
        self.armyBG.setLineWidth(3)
        self.armyBG.setMidLineWidth(0)
        self.armyBG.setObjectName("armyBG")

        self.EnemySlot1 = QtWidgets.QLabel(self)
        self.EnemySlot1.setGeometry(QtCore.QRect(170, 40, 104, 127))
        self.EnemySlot1.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot1.setLineWidth(3)
        self.EnemySlot1.setMidLineWidth(0)
        self.EnemySlot1.setObjectName("EnemySlot1")
        self.EnemySlot5 = QtWidgets.QLabel(self)
        self.EnemySlot5.setGeometry(QtCore.QRect(170, 320, 104, 127))
        self.EnemySlot5.setMinimumSize(QtCore.QSize(104, 127))
        self.EnemySlot5.setMaximumSize(QtCore.QSize(224, 127))
        self.EnemySlot5.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot5.setLineWidth(3)
        self.EnemySlot5.setMidLineWidth(0)
        self.EnemySlot5.setObjectName("EnemySlot5")
        self.EnemySlot3 = QtWidgets.QLabel(self)
        self.EnemySlot3.setGeometry(QtCore.QRect(170, 180, 104, 127))
        self.EnemySlot3.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot3.setLineWidth(3)
        self.EnemySlot3.setMidLineWidth(0)
        self.EnemySlot3.setObjectName("EnemySlot3")
        self.EnemySlot4 = QtWidgets.QLabel(self)
        self.EnemySlot4.setGeometry(QtCore.QRect(50, 180, 104, 127))
        self.EnemySlot4.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot4.setLineWidth(3)
        self.EnemySlot4.setMidLineWidth(0)
        self.EnemySlot4.setObjectName("EnemySlot4")
        self.EnemySlot2 = QtWidgets.QLabel(self)
        self.EnemySlot2.setGeometry(QtCore.QRect(50, 40, 104, 127))
        self.EnemySlot2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.EnemySlot2.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot2.setLineWidth(3)
        self.EnemySlot2.setMidLineWidth(0)
        self.EnemySlot2.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.EnemySlot2.setObjectName("EnemySlot2")
        self.EnemySlot6 = QtWidgets.QLabel(self)
        self.EnemySlot6.setGeometry(QtCore.QRect(50, 320, 104, 127))
        self.EnemySlot6.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot6.setLineWidth(3)
        self.EnemySlot6.setMidLineWidth(0)
        self.EnemySlot6.setObjectName("EnemySlot6")
        self.pushButtonSlot_2 = QtWidgets.QPushButton(self)
        self.pushButtonSlot_2.setGeometry(QtCore.QRect(50, 40, 104, 127))
        self.pushButtonSlot_2.setText("")
        self.pushButtonSlot_2.setFlat(True)
        self.pushButtonSlot_2.setObjectName("pushButtonSlot_2")
        self.pushButtonSlot_3 = QtWidgets.QPushButton(self)
        self.pushButtonSlot_3.setGeometry(QtCore.QRect(170, 180, 104, 127))
        self.pushButtonSlot_3.setText("")
        self.pushButtonSlot_3.setFlat(True)
        self.pushButtonSlot_3.setObjectName("pushButtonSlot_3")
        self.pushButtonSlot_4 = QtWidgets.QPushButton(self)
        self.pushButtonSlot_4.setGeometry(QtCore.QRect(50, 180, 104, 127))
        self.pushButtonSlot_4.setText("")
        self.pushButtonSlot_4.setFlat(True)
        self.pushButtonSlot_4.setObjectName("pushButtonSlot_4")
        self.pushButtonSlot_5 = QtWidgets.QPushButton(self)
        self.pushButtonSlot_5.setGeometry(QtCore.QRect(170, 320, 104, 127))
        self.pushButtonSlot_5.setText("")
        self.pushButtonSlot_5.setFlat(True)
        self.pushButtonSlot_5.setObjectName("pushButtonSlot_5")
        self.pushButtonSlot_6 = QtWidgets.QPushButton(self)
        self.pushButtonSlot_6.setGeometry(QtCore.QRect(50, 320, 104, 127))
        self.pushButtonSlot_6.setText("")
        self.pushButtonSlot_6.setFlat(True)
        self.pushButtonSlot_6.setObjectName("pushButtonSlot_6")
        self.pushButtonSlot_1 = QtWidgets.QPushButton(self)
        self.pushButtonSlot_1.setGeometry(QtCore.QRect(170, 40, 104, 127))
        self.pushButtonSlot_1.setText("")
        self.pushButtonSlot_1.setFlat(True)
        self.pushButtonSlot_1.setObjectName("pushButtonSlot_1")

        self.armyBG.setPixmap(QPixmap(BACKGROUND))
        self.pushButtonSlot_1.clicked.connect(self.en_slot1_detailed)
        self.pushButtonSlot_2.clicked.connect(self.en_slot2_detailed)
        self.pushButtonSlot_3.clicked.connect(self.en_slot3_detailed)
        self.pushButtonSlot_4.clicked.connect(self.en_slot4_detailed)
        self.pushButtonSlot_5.clicked.connect(self.en_slot5_detailed)
        self.pushButtonSlot_6.clicked.connect(self.en_slot6_detailed)

        self.faction = self.database.current_game_faction
        # self.dungeon = f'{self.faction}_{slot}'
        # self.dungeon_units = self.database.show_dungeon_units(self.dungeon)

        self.dungeon_units = unit_selector(slot, setup_6)
        # print(self.dungeon_units)
        self._dungeon_list_update(self.dungeon_units)

        QtCore.QMetaObject.connectSlotsByName(self)


    def dungeon_list_update(self) -> None:
        """Метод обновляющий список юнитов подземелья"""

        dung_icons_dict = {
            1: self.EnemySlot1,
            2: self.EnemySlot2,
            3: self.EnemySlot3,
            4: self.EnemySlot4,
            5: self.EnemySlot5,
            6: self.EnemySlot6,
        }

        units_dict = {}
        for num, unit_name in enumerate(self.dungeon_units):
            unit = self.database.get_unit_by_name(unit_name)
            units_dict[num + 1] = unit

        for num, icon_slot in dung_icons_dict.items():
            slot_update(
                units_dict[num],
                icon_slot)

    def _dungeon_list_update(self, dungeon_units: dict) -> None:
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
            slot_update(
                self.database.get_unit_by_name(dungeon_units[num]),
                icon_slot)

    def slot_detailed(self, unit: namedtuple, slot_dialog: any) -> None:
        """Метод создающий окно юнита игрока при нажатии на слот."""
        try:
            global DETAIL_WINDOW
            DETAIL_WINDOW = slot_dialog(
                self.database,
                unit)
            DETAIL_WINDOW.show()
        except AttributeError:
            pass

    def en_slot1_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 1)."""
        unit = self.database.get_unit_by_name(self.dungeon_units[1])
        self.slot_detailed(unit, UnitDialog)

    def en_slot2_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 2)."""
        unit = self.database.get_unit_by_name(self.dungeon_units[2])
        self.slot_detailed(unit, UnitDialog)

    def en_slot3_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 3)."""
        unit = self.database.get_unit_by_name(self.dungeon_units[3])
        self.slot_detailed(unit, UnitDialog)

    def en_slot4_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 4)."""
        unit = self.database.get_unit_by_name(self.dungeon_units[4])
        self.slot_detailed(unit, UnitDialog)

    def en_slot5_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 5)."""
        unit = self.database.get_unit_by_name(self.dungeon_units[5])
        self.slot_detailed(unit, UnitDialog)

    def en_slot6_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 6)."""
        unit = self.database.get_unit_by_name(self.dungeon_units[6])
        self.slot_detailed(unit, UnitDialog)
