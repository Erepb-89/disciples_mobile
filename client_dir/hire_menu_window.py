"""Окно найма юнитов"""

import os.path

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.hire_menu_form import Ui_HireMenu
from client_dir.settings import HIRE_SCREEN, ELVEN_PLUG
from client_dir.ui_functions import get_unit_image, \
    set_size_by_unit, show_gif, slot_frame_update
from client_dir.unit_dialog import UnitNameDialog
from units_dir.units_factory import AbstractFactory


class HireMenuWindow(QMainWindow):
    """
    Класс - окно выбора фракции.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла hire_menu_form.py
    """

    def __init__(self, database, slot):
        super().__init__()
        # основные переменные
        self.database = database
        self.faction = self.database.current_game_faction
        self.factory = AbstractFactory.create_factory(
            self.faction)
        self.fighter = self.factory.create_fighter()
        self.archer = self.factory.create_archer()
        self.mage = self.factory.create_mage()
        self.support = self.factory.create_support()
        self.special = self.factory.create_special()
        self.highlighted_unit = None
        self.unit_slot = slot

        self.InitUI()

    def InitUI(self):
        # Загружаем конфигурацию окна из дизайнера
        self.ui = Ui_HireMenu()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)
        self.update_bg()

        self.ui.pushButtonSelect1.clicked.connect(
            self.highlight_selected_unit1)
        self.ui.pushButtonSelect2.clicked.connect(
            self.highlight_selected_unit2)
        self.ui.pushButtonSelect3.clicked.connect(
            self.highlight_selected_unit3)
        self.ui.pushButtonSelect4.clicked.connect(
            self.highlight_selected_unit4)
        self.ui.pushButtonSelect5.clicked.connect(
            self.highlight_selected_unit5)

        self.ui.pushButtonSlot1.clicked.connect(
            self.hire_slot1_detailed)
        self.ui.pushButtonSlot2.clicked.connect(
            self.hire_slot2_detailed)
        self.ui.pushButtonSlot3.clicked.connect(
            self.hire_slot3_detailed)
        self.ui.pushButtonSlot4.clicked.connect(
            self.hire_slot4_detailed)
        self.ui.pushButtonSlot5.clicked.connect(
            self.hire_slot5_detailed)

        self.unit_list_update()

        self.ui.costUnit1.setText(self.fighter.cost)
        self.ui.costUnit2.setText(self.archer.cost)
        self.ui.costUnit3.setText(self.mage.cost)
        self.ui.costUnit4.setText(self.support.cost)
        self.ui.costUnit5.setText(self.special.cost)

        self.ui.pushButtonBack.clicked.connect(self.back)
        self.ui.pushButtonBuy.clicked.connect(self.buy)
        show_gif(self.fighter, self.ui.gifLabel1)
        show_gif(self.archer, self.ui.gifLabel2)
        show_gif(self.mage, self.ui.gifLabel3)
        show_gif(self.support, self.ui.gifLabel4)
        show_gif(self.special, self.ui.gifLabel5)

        self.show()

    def unlight_all_units(self):
        """Снятие подсветки юнитов"""
        self.ui.labelSelected1.setLineWidth(0)
        self.ui.labelSelected2.setLineWidth(0)
        self.ui.labelSelected3.setLineWidth(0)
        self.ui.labelSelected4.setLineWidth(0)
        self.ui.labelSelected5.setLineWidth(0)

    def highlight_selected_unit1(self):
        """Подсветка выбранного юнита"""
        self.unlight_all_units()
        self.ui.labelSelected1.setLineWidth(2)
        self.highlighted_unit = self.fighter

    def highlight_selected_unit2(self):
        """Подсветка выбранного юнита"""
        self.unlight_all_units()
        self.ui.labelSelected2.setLineWidth(2)
        self.highlighted_unit = self.archer

    def highlight_selected_unit3(self):
        """Подсветка выбранного юнита"""
        self.unlight_all_units()
        self.ui.labelSelected3.setLineWidth(2)
        self.highlighted_unit = self.mage

    def highlight_selected_unit4(self):
        """Подсветка выбранного юнита"""
        self.unlight_all_units()
        self.ui.labelSelected4.setLineWidth(2)
        self.highlighted_unit = self.support

    def highlight_selected_unit5(self):
        """Подсветка выбранного юнита"""
        self.unlight_all_units()
        self.ui.labelSelected5.setLineWidth(2)
        self.highlighted_unit = self.special

    def update_bg(self):
        """Обновление бэкграунда, заполнение картинкой найма"""
        hire_menu_bg = self.ui.hireMenuBG
        hire_menu_bg.setPixmap(
            QPixmap(
                os.path.join(
                    HIRE_SCREEN,
                    "hire_window.png")))
        hire_menu_bg.setGeometry(QtCore.QRect(0, 0, 788, 828))
        self.hbox.addWidget(hire_menu_bg)
        self.setLayout(self.hbox)

    @staticmethod
    def get_image(faction):
        """Достаем картинку найма армии фракции"""
        try:
            return os.path.join(HIRE_SCREEN, f"{faction}.png")
        except BaseException:
            return os.path.join(HIRE_SCREEN, ELVEN_PLUG)

    def back(self):
        """Кнопка возврата"""
        self.close()

    def buy(self):
        """Кнопка найма"""
        print(f'Вы купили воина: {self.highlighted_unit.name}')
        self.hire_unit_action(self.unit_slot)
        self.close()

    def unit_list_update(self):
        """Метод обновляющий список юнитов."""
        self.slot_update(self.fighter, self.ui.slot1)
        self.slot_update(self.archer, self.ui.slot2)
        self.slot_update(self.mage, self.ui.slot3)
        self.slot_update(self.support, self.ui.slot4)
        self.slot_update(self.special, self.ui.slot5)

        self.button_update(self.fighter, self.ui.pushButtonSlot1)
        self.button_update(self.archer, self.ui.pushButtonSlot2)
        self.button_update(self.mage, self.ui.pushButtonSlot3)
        self.button_update(self.support, self.ui.pushButtonSlot4)
        self.button_update(self.special, self.ui.pushButtonSlot5)

        slot_frame_update(self.fighter, self.ui.slotFrame1)
        slot_frame_update(self.archer, self.ui.slotFrame2)
        slot_frame_update(self.mage, self.ui.slotFrame3)
        slot_frame_update(self.support, self.ui.slotFrame4)
        slot_frame_update(self.special, self.ui.slotFrame5)

    def button_update(self, unit, button):
        """Установка размера кнопки на иконке"""
        set_size_by_unit(unit, button)

        self.hbox.addWidget(button)
        self.setLayout(self.hbox)

    def slot_update(self, unit, slot):
        """Установка gif'ки в иконку юнита"""
        set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            get_unit_image(unit)).scaled(
            slot.width(), slot.height()))
        self.hbox.addWidget(slot)
        self.setLayout(self.hbox)

    def hire_unit_action(self, slot):
        """Метод обработчик нажатия кнопки 'Нанять' для игрока"""
        # self.database.hire_unit(
        # self.highlighted_unit.name, int(slot))
        self.highlighted_unit.add_to_band(int(slot))

    def hire_slot_detailed(self, unit_type):
        """Метод создающий окно юнита."""
        try:
            global DETAIL_WINDOW
            DETAIL_WINDOW = UnitNameDialog(
                self.database,
                unit_type.name)
            DETAIL_WINDOW.show()
        except Exception as err:
            print(err)

    def hire_slot1_detailed(self):
        """Метод создающий окно юнита (слот 1)."""
        self.hire_slot_detailed(self.fighter)

    def hire_slot2_detailed(self):
        """Метод создающий окно юнита (слот 2)."""
        self.hire_slot_detailed(self.archer)

    def hire_slot3_detailed(self):
        """Метод создающий окно юнита (слот 3)."""
        self.hire_slot_detailed(self.mage)

    def hire_slot4_detailed(self):
        """Метод создающий окно юнита (слот 4)."""
        self.hire_slot_detailed(self.support)

    def hire_slot5_detailed(self):
        """Метод создающий окно юнита (слот 5)."""
        self.hire_slot_detailed(self.special)
