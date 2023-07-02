# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'army.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog

from client_dir.settings import UNIT_FRAME, UNIT_ICONS, PLUG, ICON
from client_dir.ui_functions import get_unit_image, set_size_by_unit


class EnemyArmyDialog(QDialog):
    def __init__(self, database, slot):
        super().__init__()
        self.database = database
        self.mission_slot = slot

        self.setFixedSize(320, 490)
        self.setWindowTitle('Окно армии противника')

        self.EnemySlot4 = QtWidgets.QLabel(self)
        self.EnemySlot4.setGeometry(QtCore.QRect(50, 180, 104, 127))
        self.EnemySlot4.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot4.setLineWidth(3)
        self.EnemySlot4.setMidLineWidth(0)
        self.EnemySlot4.setObjectName("EnemySlot4")
        self.pushButtonEnSlot5 = QtWidgets.QPushButton(self)
        self.pushButtonEnSlot5.setGeometry(QtCore.QRect(170, 320, 104, 127))
        self.pushButtonEnSlot5.setMinimumSize(QtCore.QSize(104, 127))
        self.pushButtonEnSlot5.setMaximumSize(QtCore.QSize(224, 127))
        self.pushButtonEnSlot5.setText("")
        self.pushButtonEnSlot5.setFlat(True)
        self.pushButtonEnSlot5.setObjectName("pushButtonEnSlot5")
        self.EnemySlot2 = QtWidgets.QLabel(self)
        self.EnemySlot2.setGeometry(QtCore.QRect(50, 40, 104, 127))
        self.EnemySlot2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.EnemySlot2.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot2.setLineWidth(3)
        self.EnemySlot2.setMidLineWidth(0)
        self.EnemySlot2.setAlignment(
            QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.EnemySlot2.setObjectName("EnemySlot2")
        self.EnemySlot1 = QtWidgets.QLabel(self)
        self.EnemySlot1.setGeometry(QtCore.QRect(170, 40, 104, 127))
        self.EnemySlot1.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot1.setLineWidth(3)
        self.EnemySlot1.setMidLineWidth(0)
        self.EnemySlot1.setObjectName("EnemySlot1")
        self.pushButtonEnSlot3 = QtWidgets.QPushButton(self)
        self.pushButtonEnSlot3.setGeometry(QtCore.QRect(170, 180, 104, 127))
        self.pushButtonEnSlot3.setText("")
        self.pushButtonEnSlot3.setFlat(True)
        self.pushButtonEnSlot3.setObjectName("pushButtonEnSlot3")
        self.EnemySlot5 = QtWidgets.QLabel(self)
        self.EnemySlot5.setGeometry(QtCore.QRect(170, 320, 104, 127))
        self.EnemySlot5.setMinimumSize(QtCore.QSize(104, 127))
        self.EnemySlot5.setMaximumSize(QtCore.QSize(224, 127))
        self.EnemySlot5.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot5.setLineWidth(3)
        self.EnemySlot5.setMidLineWidth(0)
        self.EnemySlot5.setObjectName("EnemySlot5")
        self.EnemySlot6 = QtWidgets.QLabel(self)
        self.EnemySlot6.setGeometry(QtCore.QRect(50, 320, 104, 127))
        self.EnemySlot6.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot6.setLineWidth(3)
        self.EnemySlot6.setMidLineWidth(0)
        self.EnemySlot6.setObjectName("EnemySlot6")
        self.EnemySlot3 = QtWidgets.QLabel(self)
        self.EnemySlot3.setGeometry(QtCore.QRect(170, 180, 104, 127))
        self.EnemySlot3.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot3.setLineWidth(3)
        self.EnemySlot3.setMidLineWidth(0)
        self.EnemySlot3.setObjectName("EnemySlot3")
        self.pushButtonEnSlot6 = QtWidgets.QPushButton(self)
        self.pushButtonEnSlot6.setGeometry(QtCore.QRect(50, 320, 104, 127))
        self.pushButtonEnSlot6.setText("")
        self.pushButtonEnSlot6.setFlat(True)
        self.pushButtonEnSlot6.setObjectName("pushButtonEnSlot6")

        self.armyBG = QtWidgets.QLabel(self)
        self.armyBG.setGeometry(QtCore.QRect(0, 0, 41, 41))
        self.armyBG.setMinimumSize(QtCore.QSize(13, 13))
        self.armyBG.setMaximumSize(QtCore.QSize(320, 490))
        self.armyBG.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.armyBG.setAutoFillBackground(True)
        self.armyBG.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.armyBG.setFrameShadow(QtWidgets.QFrame.Plain)
        self.armyBG.setLineWidth(3)
        self.armyBG.setMidLineWidth(0)
        self.armyBG.setObjectName("armyBG")

        unit_frame = QPixmap(UNIT_FRAME)
        self.armyBG.setPixmap(unit_frame)

        self.faction = self.database.current_game_faction
        self.dungeon = f'{self.faction}_{slot}'
        print(self.dungeon)
        self.dungeon_units = self.database.show_dungeon_units(self.dungeon)
        print(self.dungeon_units)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.dungeon_list_update()

    def dungeon_list_update(self):
        """Метод обновляющий список юнитов подземелья"""

        self.dung_icons_dict = {
            1: self.EnemySlot1,
            2: self.EnemySlot2,
            3: self.EnemySlot3,
            4: self.EnemySlot4,
            5: self.EnemySlot5,
            6: self.EnemySlot6,
        }

        for num, icon_slot in self.dung_icons_dict.items():
            try:
                self._slot_update(
                    self._enemy_unit_by_slot(num),
                    icon_slot)
            except Exception as err:
                print(err)


    def _slot_update(self, unit, slot):
        """Метод обновления иконки"""
        set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            get_unit_image(unit)).scaled(
            slot.width(), slot.height()))


    def _enemy_unit_by_slot(self, slot):
        """Метод получающий вражеского юнита по слоту."""
        unit = self.database.get_unit_by_slot(
            slot,
            self.dungeon)
        print(unit)
        return unit
