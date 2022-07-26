import os.path

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.capital_army_form import Ui_CapitalArmyWindow
from client_dir.hire_menu_window import HireMenuWindow
from client_dir.settings import TOWN_ARMY, UNIT_ICONS
from client_dir.unit_dialog import UnitSlotDialog
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
        self.current_faction = self.database.current_game_faction()
        self.factory = AbstractFactory.create_factory(self.current_faction)
        self.fighter = self.factory.create_fighter()
        self.archer = self.factory.create_fighter()
        self.mage = self.factory.create_fighter()
        self.support = self.factory.create_support()
        self.special = self.factory.create_special()

        self.InitUI()

    def InitUI(self):
        # Загружаем конфигурацию окна из дизайнера
        self.ui = Ui_CapitalArmyWindow()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)

        self.ui.pushButtonSlot1.clicked.connect(self.slot1_detailed)
        self.ui.pushButtonSlot2.clicked.connect(self.slot2_detailed)
        self.ui.pushButtonSlot3.clicked.connect(self.slot3_detailed)
        self.ui.pushButtonSlot4.clicked.connect(self.slot4_detailed)
        self.ui.pushButtonSlot5.clicked.connect(self.slot5_detailed)
        self.ui.pushButtonSlot6.clicked.connect(self.slot6_detailed)

        self.ui.pushButtonDelete.clicked.connect(self.delete_unit_action)

        self.player_list_update()
        self.player_slots_update()

        self.update_capital()
        self.ui.pushButtonBack.clicked.connect(self.back)

        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_D:
            self.delete_unit_action()

    def update_capital(self):
        """Обновление лейбла, заполнение картинкой замка"""
        capital_army_bg = self.ui.capitalArmyBG
        capital_army_bg.setPixmap(QPixmap(self.get_image(self.current_faction)))
        capital_army_bg.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        self.hbox.addWidget(capital_army_bg)
        self.setLayout(self.hbox)

    def get_image(self, current_faction):
        """Достаем картинку найма армии фракции"""
        try:
            return os.path.join(TOWN_ARMY, f"{current_faction}.png")
        except:
            return os.path.join(TOWN_ARMY, "Elven Alliance.png")

    def back(self):
        """Кнопка возврата"""
        self.close()

    def set_size_by_unit(self, unit, ui_obj):
        try:
            if unit.size == "Большой":
                ui_obj.setFixedWidth(224)
                ui_obj.setFixedHeight(127)
        except Exception as err:
            # print(err)
            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def button_update(self, unit, button):
        self.set_size_by_unit(unit, button)

        self.hbox.addWidget(button)
        self.setLayout(self.hbox)

    def slot_update(self, unit, slot):
        self.set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            self.get_unit_image(unit)).scaled(
            slot.width(), slot.height()))
        self.hbox.addWidget(slot)
        self.setLayout(self.hbox)

    def get_unit_image(self, unit):
        try:
            return os.path.join(UNIT_ICONS, f"{unit.name} (Disciples II)-иконка.jpg")
        except:
            return os.path.join(UNIT_ICONS, "Заглушка (Disciples II)-иконка.jpg")

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
        player_units = self.database.show_player_units()
        self.player_units_model = QStandardItemModel()
        for i in player_units:
            item = QStandardItem(i.name)
            item.setEditable(False)
            self.player_units_model.appendRow(item)

        self.slot_update(self.database.get_unit_by_slot(1), self.ui.slot1)
        self.slot_update(self.database.get_unit_by_slot(2), self.ui.slot2)
        self.slot_update(self.database.get_unit_by_slot(3), self.ui.slot3)
        self.slot_update(self.database.get_unit_by_slot(4), self.ui.slot4)
        self.slot_update(self.database.get_unit_by_slot(5), self.ui.slot5)
        self.slot_update(self.database.get_unit_by_slot(6), self.ui.slot6)

        self.button_update(self.database.get_unit_by_slot(1), self.ui.pushButtonSlot1)
        self.button_update(self.database.get_unit_by_slot(2), self.ui.pushButtonSlot2)
        self.button_update(self.database.get_unit_by_slot(3), self.ui.pushButtonSlot3)
        self.button_update(self.database.get_unit_by_slot(4), self.ui.pushButtonSlot4)
        self.button_update(self.database.get_unit_by_slot(5), self.ui.pushButtonSlot5)
        self.button_update(self.database.get_unit_by_slot(6), self.ui.pushButtonSlot6)

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
            self.database.delete_unit(int(selected_slot))
            self.player_list_update()
        except Exception as err:
            print(f'Error: {err}')

    def show_available_units(self):
        """Метод показывающий доступных для покупки
        юнитов данной фракции."""
        try:
            global hire_window
            hire_window = HireMenuWindow(self.database)
            hire_window.show()
        except Exception as err:
            print(err)

        print('Показать доступных для покупки юнитов данной фракции')
        # print(self.fighter.add_to_band(5))

    def slot1_detailed(self):
        """Метод создающий окно юнита игрока (слот 1)."""
        try:
            global detail_window
            detail_window = UnitSlotDialog(self.database, 1)
            detail_window.show()
        except:
            self.show_available_units()

    def slot2_detailed(self):
        """Метод создающий окно юнита игрока (слот 2)."""
        try:
            global detail_window
            detail_window = UnitSlotDialog(self.database, 2)
            detail_window.show()
        except:
            self.show_available_units()

    def slot3_detailed(self):
        """Метод создающий окно юнита игрока (слот 3)."""
        try:
            global detail_window
            detail_window = UnitSlotDialog(self.database, 3)
            detail_window.show()
        except:
            self.show_available_units()

    def slot4_detailed(self):
        """Метод создающий окно юнита игрока (слот 4)."""
        try:
            global detail_window
            detail_window = UnitSlotDialog(self.database, 4)
            detail_window.show()
        except:
            self.show_available_units()

    def slot5_detailed(self):
        """Метод создающий окно юнита игрока (слот 5)."""
        try:
            global detail_window
            detail_window = UnitSlotDialog(self.database, 5)
            detail_window.show()
        except:
            self.show_available_units()

    def slot6_detailed(self):
        """Метод создающий окно юнита игрока (слот 6)."""
        try:
            global detail_window
            detail_window = UnitSlotDialog(self.database, 6)
            detail_window.show()
        except:
            self.show_available_units()
