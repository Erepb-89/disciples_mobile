import os.path

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.capital_building_form import Ui_CapitalBuildingWindow
from client_dir.settings import CAPITAL_BUILDING, UNIT_ICONS
from client_dir.unit_dialog import UnitNameDialog
from units_dir.buildings import legion_fighters, factions
from units_dir.units_factory import AbstractFactory


class CapitalBuildingWindow(QMainWindow):
    """
    Класс - окно выбора фракции.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла capital_building_form.py
    """

    def __init__(self, database):
        super().__init__()
        # основные переменные
        self.database = database
        self.current_faction = self.database.current_game_faction()
        self.factory = AbstractFactory.create_factory(self.current_faction)
        self.fighter = self.factory.create_fighter()
        self.archer = self.factory.create_fighter()
        self.mage = self.factory.create_fighter()
        self.support = self.factory.create_support()
        self.special = self.factory.create_special()
        self.current_factory = 'fighter'
        # self.current_unit = self.get_unit_by_building_slot(1)

        self.InitUI()

    def InitUI(self):
        # Загружаем конфигурацию окна из дизайнера
        self.ui = Ui_CapitalBuildingWindow()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)

        self.update_capital()
        self.ui.pushButtonBack.clicked.connect(self.back)
        self.ui.pushButtonSlot.clicked.connect(self.slot_detailed)
        self.ui.pushButtonFighters.clicked.connect(self.change_factory_fighters)
        self.ui.pushButtonMages.clicked.connect(self.change_factory_mages)
        self.ui.pushButtonArchers.clicked.connect(self.change_factory_archers)
        self.ui.pushButtonSupport.clicked.connect(self.change_factory_support)
        self.ui.pushButtonOthers.clicked.connect(self.change_factory_others)
        # self.ui.radioButton_1.clicked.connect(self.show_unit1_picture)
        # self.ui.radioButton_2.clicked.connect(self.show_unit2_picture)

        self.show()

    def update_capital(self):
        """Обновление лейбла, заполнение картинкой замка"""
        capital_building_bg = self.ui.capitalBuildingBG
        capital_building_bg.setPixmap(QPixmap(self.get_image(self.current_faction)))
        capital_building_bg.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        self.hbox.addWidget(capital_building_bg)
        self.setLayout(self.hbox)

    def get_image(self, current_faction):
        """Достаем картинку строительства текущей фракции"""
        try:
            return os.path.join(CAPITAL_BUILDING, f"{self.current_factory}/{current_faction}.png")
        except:
            return os.path.join(CAPITAL_BUILDING, "Elven Alliance.png")

    def back(self):
        """Кнопка возврата"""
        self.close()

    def change_factory_fighters(self):
        self.current_factory = 'fighter'
        self.update_capital()
        # self.current_unit = self.get_unit_by_building_slot(1)

    def change_factory_mages(self):
        self.current_factory = 'mage'
        self.update_capital()

    def change_factory_archers(self):
        self.current_factory = 'archer'
        self.update_capital()
        # self.current_unit = self.get_unit_by_building_slot(1)

    def change_factory_support(self):
        self.current_factory = 'support'
        self.update_capital()

    def change_factory_others(self):
        self.current_factory = 'others'
        self.update_capital()

    def get_unit_by_building_slot(self, building_slot):
        # unit = self.database.get_unit_by_name(legion_fighters[building_slot][1])
        unit = self.database.get_unit_by_name(
            factions[self.current_faction][self.current_factory][building_slot][1])
        return unit

    def show_unit1_picture(self):
        try:
            self.current_unit = self.get_unit_by_building_slot(1)
            self.slot_update(self.current_unit)
        except Exception as err:
            print(err)

    def show_unit2_picture(self):
        try:
            self.current_unit = self.get_unit_by_building_slot(2)
            self.slot_update(self.current_unit)
        except Exception as err:
            print(err)

    def slot_update(self, unit):
        slot = self.ui.slot
        self.set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            self.get_unit_image(unit)).scaled(
            slot.width(), slot.height()))
        self.hbox.addWidget(slot)
        self.setLayout(self.hbox)

    def slot_detailed(self):
        """Метод создающий окно юнита (слот)."""
        try:
            global detail_window
            detail_window = UnitNameDialog(self.database, self.current_unit.name)
            detail_window.show()
        except Exception as err:
            print(err)

    def get_unit_image(self, unit):
        try:
            return os.path.join(UNIT_ICONS, f"{unit.name} (Disciples II)-иконка.jpg")
        except:
            return os.path.join(UNIT_ICONS, "Заглушка (Disciples II)-иконка.jpg")

    def set_size_by_unit(self, unit, ui_obj):
        try:
            if unit.size == "Большой":
                ui_obj.setFixedWidth(224)
                ui_obj.setFixedHeight(127)
        except Exception as err:
            # print(err)
            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)
