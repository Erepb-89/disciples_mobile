"""Окно найма юнитов"""

import os.path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QMessageBox

from client_dir.hire_menu_form import Ui_HireMenu
from client_dir.settings import HIRE_SCREEN
from client_dir.ui_functions import show_gif,\
    slot_frame_update, slot_update, button_update
from client_dir.unit_dialog import UnitNameDialog
from units_dir.units_factory import AbstractFactory


class HireMenuWindow(QMainWindow):
    """
    Класс - окно найма юнитов фракции.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла hire_menu_form.py
    """

    def __init__(self, database: any, slot: int, instance: any):
        super().__init__()
        # основные переменные
        self.database = database
        self.capital_army = instance
        self.faction = self.database.current_faction
        self.factory = AbstractFactory.create_factory(
            self.faction)
        self.fighter = self.factory.create_fighter()
        self.archer = self.factory.create_archer()
        self.mage = self.factory.create_mage()
        self.support = self.factory.create_support()
        self.special = self.factory.create_special()
        self.highlighted_unit = None
        self.unit_slot = slot
        self.player_gold = 0

        self.InitUI()

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""
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

        self.player_gold = self.database.get_gold(
            self.database.current_player.name, self.faction)
        self.ui.gold.setText(str(self.player_gold))
        self.ui.pushButtonBuy.setEnabled(False)

        self.show()

    def unlight_all_units(self) -> None:
        """Снятие подсветки юнитов"""
        self.ui.labelSelected1.setLineWidth(0)
        self.ui.labelSelected2.setLineWidth(0)
        self.ui.labelSelected3.setLineWidth(0)
        self.ui.labelSelected4.setLineWidth(0)
        self.ui.labelSelected5.setLineWidth(0)

    def highlight_selected_unit(self,
                                ui_obj: QtWidgets.QLabel,
                                unit_type: any) -> None:
        """Подсветка выбранного юнита"""
        self.unlight_all_units()
        ui_obj.setLineWidth(2)
        ui_obj.setStyleSheet("color: rgb(65, 3, 2)")
        self.highlighted_unit = unit_type
        self.ui.pushButtonBuy.setEnabled(True)

    def highlight_selected_unit1(self) -> None:
        """Подсветка выбранного юнита"""
        self.highlight_selected_unit(self.ui.labelSelected1,
                                     self.fighter)

    def highlight_selected_unit2(self) -> None:
        """Подсветка выбранного юнита"""
        self.highlight_selected_unit(self.ui.labelSelected2,
                                     self.archer)

    def highlight_selected_unit3(self) -> None:
        """Подсветка выбранного юнита"""
        self.highlight_selected_unit(self.ui.labelSelected3,
                                     self.mage)

    def highlight_selected_unit4(self) -> None:
        """Подсветка выбранного юнита"""
        self.highlight_selected_unit(self.ui.labelSelected4,
                                     self.support)

    def highlight_selected_unit5(self) -> None:
        """Подсветка выбранного юнита"""
        self.highlight_selected_unit(self.ui.labelSelected5,
                                     self.special)

    def update_bg(self) -> None:
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

    def back(self) -> None:
        """Кнопка возврата"""
        self.close()

    def buy(self) -> None:
        """Кнопка найма"""
        print(f'Вы купили воина: {self.highlighted_unit.name}')
        self.hire_unit_action(self.unit_slot)
        self.capital_army.reset()
        self.capital_army.capital.main.reset()
        self.close()

    def unit_list_update(self) -> None:
        """Метод обновляющий список юнитов."""
        slot_update(self.fighter, self.ui.slot1)
        slot_update(self.archer, self.ui.slot2)
        slot_update(self.mage, self.ui.slot3)
        slot_update(self.support, self.ui.slot4)
        slot_update(self.special, self.ui.slot5)

        button_update(self.fighter, self.ui.pushButtonSlot1)
        button_update(self.archer, self.ui.pushButtonSlot2)
        button_update(self.mage, self.ui.pushButtonSlot3)
        button_update(self.support, self.ui.pushButtonSlot4)
        button_update(self.special, self.ui.pushButtonSlot5)

        slot_frame_update(self.fighter, self.ui.slotFrame1)
        slot_frame_update(self.archer, self.ui.slotFrame2)
        slot_frame_update(self.mage, self.ui.slotFrame3)
        slot_frame_update(self.support, self.ui.slotFrame4)
        slot_frame_update(self.special, self.ui.slotFrame5)

    def hire_unit_action(self, slot: int) -> None:
        """Метод обработчик нажатия кнопки 'Нанять' для игрока"""
        if self.player_gold < int(self.highlighted_unit.cost):

            msg = QMessageBox()
            msg.setWindowTitle("Предупреждение")
            msg.setText("Недостаточно золота")
            msg.setIcon(QMessageBox.Warning)

            msg.exec_()
        else:
        # if self.player_gold >= int(self.highlighted_unit.cost):
            changed_gold = self.player_gold - int(self.highlighted_unit.cost)

            # обновление золота в базе
            self.database.update_gold(
                self.database.current_player.name,
                self.faction,
                changed_gold)
            self.highlighted_unit.add_to_band(int(slot))

            self.capital_army.ui.gold.setText(str(changed_gold))

    def hire_slot_detailed(self, unit_type: any) -> None:
        """Метод создающий окно юнита."""
        global DETAIL_WINDOW
        DETAIL_WINDOW = UnitNameDialog(
            self.database,
            unit_type.name)
        DETAIL_WINDOW.show()

    def hire_slot1_detailed(self) -> None:
        """Метод создающий окно юнита (слот 1)."""
        self.hire_slot_detailed(self.fighter)

    def hire_slot2_detailed(self) -> None:
        """Метод создающий окно юнита (слот 2)."""
        self.hire_slot_detailed(self.archer)

    def hire_slot3_detailed(self) -> None:
        """Метод создающий окно юнита (слот 3)."""
        self.hire_slot_detailed(self.mage)

    def hire_slot4_detailed(self) -> None:
        """Метод создающий окно юнита (слот 4)."""
        self.hire_slot_detailed(self.support)

    def hire_slot5_detailed(self) -> None:
        """Метод создающий окно юнита (слот 5)."""
        self.hire_slot_detailed(self.special)
