"""Окно найма юнитов"""

import os.path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.forms.choose_hero_form import Ui_ChooseHeroMenu
from client_dir.windows.question_window import QuestionWindow
from client_dir.settings import HIRE_SCREEN
from client_dir.ui_functions import show_gif, slot_frame_update, \
    slot_update, button_update
from client_dir.dialogs.unit_dialog import UnitNameDialog
from units_dir.units import main_db
from units_dir.units_factory import AbstractFactory


class ChooseHeroWindow(QMainWindow):
    """
    Класс - окно выбора героев фракции.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла choose_hero_form.py
    """

    def __init__(self, parent_window: any):
        super().__init__()
        # основные переменные
        self.choose_faction = parent_window
        self.question = False  # Выбор героя
        self.faction = main_db.get_current_faction()
        self.factory = AbstractFactory.create_factory(
            self.faction)
        self.fighter = self.factory.create_hero_fighter()
        self.archer = self.factory.create_hero_archer()
        self.mage = self.factory.create_hero_mage()
        self.rog = self.factory.create_hero_rog()
        self.highlighted_hero = None
        self.unit_slot = 4
        self.player_gold = 0

        self.InitUI()

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""
        self.ui = Ui_ChooseHeroMenu()
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

        self.ui.pushButtonSlot1.clicked.connect(
            self.hire_slot1_detailed)
        self.ui.pushButtonSlot2.clicked.connect(
            self.hire_slot2_detailed)
        self.ui.pushButtonSlot3.clicked.connect(
            self.hire_slot3_detailed)
        self.ui.pushButtonSlot4.clicked.connect(
            self.hire_slot4_detailed)

        self.hero_list_update()

        self.ui.costUnit1.setText(self.fighter.cost)
        self.ui.costUnit2.setText(self.archer.cost)
        self.ui.costUnit3.setText(self.mage.cost)
        self.ui.costUnit4.setText(self.rog.cost)

        self.ui.nameHero1.setText(self.fighter.name)
        self.ui.nameHero2.setText(self.archer.name)
        self.ui.nameHero3.setText(self.mage.name)
        self.ui.nameHero4.setText(self.rog.name)

        self.ui.pushButtonBuy.clicked.connect(self.buy)
        show_gif(self.fighter, self.ui.gifLabel1)
        show_gif(self.archer, self.ui.gifLabel2)
        show_gif(self.mage, self.ui.gifLabel3)
        show_gif(self.rog, self.ui.gifLabel4)

        self.player_gold = main_db.get_gold()
        self.ui.gold.setText(str(self.player_gold))

        self.show()

    def unlight_all_units(self) -> None:
        """Снятие подсветки юнитов"""
        self.ui.labelSelected1.setLineWidth(0)
        self.ui.labelSelected2.setLineWidth(0)
        self.ui.labelSelected3.setLineWidth(0)
        self.ui.labelSelected4.setLineWidth(0)

    def highlight_selected_unit(self,
                                ui_obj: QtWidgets.QLabel,
                                hero_type: any) -> None:
        """Подсветка выбранного юнита"""
        self.unlight_all_units()
        ui_obj.setLineWidth(4)
        ui_obj.setStyleSheet("color: yellow")
        self.highlighted_hero = hero_type

    def highlight_selected_unit1(self) -> None:
        """Подсветка выбранного героя 1"""
        self.highlight_selected_unit(self.ui.labelSelected1,
                                     self.fighter)

    def highlight_selected_unit2(self) -> None:
        """Подсветка выбранного героя 2"""
        self.highlight_selected_unit(self.ui.labelSelected2,
                                     self.archer)

    def highlight_selected_unit3(self) -> None:
        """Подсветка выбранного героя 3"""
        self.highlight_selected_unit(self.ui.labelSelected3,
                                     self.mage)

    def highlight_selected_unit4(self) -> None:
        """Подсветка выбранного героя 4"""
        self.highlight_selected_unit(self.ui.labelSelected4,
                                     self.rog)

    def update_bg(self) -> None:
        """Обновление бэкграунда, заполнение картинкой найма"""
        hire_menu_bg = self.ui.heroMenuBG
        hire_menu_bg.setPixmap(
            QPixmap(
                os.path.join(
                    HIRE_SCREEN,
                    "hire_window.png")))
        hire_menu_bg.setGeometry(QtCore.QRect(0, 0, 788, 828))
        self.hbox.addWidget(hire_menu_bg)
        self.setLayout(self.hbox)

    def buy(self) -> None:
        """Кнопка подтверждения"""
        global QUESTION_WINDOW
        text = 'Вы хотите выбрать этого героя?'
        QUESTION_WINDOW = QuestionWindow(self, text)
        QUESTION_WINDOW.show()

    def confirmation(self) -> None:
        """Подтверждение найма выбранного героя"""
        # Если ОК, добавляем героя в базу
        if self.question:
            self.hire_hero_action(self.unit_slot)
            self.choose_faction.main.reset()
            self.choose_faction.main.update_diff_checkbox()
            self.choose_faction.main.unlock_campaign()
            self.close()

    def hero_list_update(self) -> None:
        """Метод обновляющий список героев."""
        slot_update(self.fighter, self.ui.slot1)
        slot_update(self.archer, self.ui.slot2)
        slot_update(self.mage, self.ui.slot3)
        slot_update(self.rog, self.ui.slot4)

        button_update(self.fighter, self.ui.pushButtonSlot1)
        button_update(self.archer, self.ui.pushButtonSlot2)
        button_update(self.mage, self.ui.pushButtonSlot3)
        button_update(self.rog, self.ui.pushButtonSlot4)

        slot_frame_update(self.fighter, self.ui.slotFrame1)
        slot_frame_update(self.archer, self.ui.slotFrame2)
        slot_frame_update(self.mage, self.ui.slotFrame3)
        slot_frame_update(self.rog, self.ui.slotFrame4)

    def hire_hero_action(self, slot: int) -> None:
        """Метод обработчик нажатия кнопки 'ОК' для игрока"""
        changed_gold = self.player_gold - int(self.highlighted_hero.cost)

        # обновление золота в базе
        main_db.update_gold(changed_gold)

        self.highlighted_hero.add_to_band(int(slot))

    @staticmethod
    def hire_slot_detailed(hero_type: any) -> None:
        """Метод создающий окно юнита."""
        global DETAIL_WINDOW
        DETAIL_WINDOW = UnitNameDialog(
            hero_type.name)
        DETAIL_WINDOW.show()

    def hire_slot1_detailed(self) -> None:
        """Метод создающий детальное окно героя (слот 1)."""
        self.hire_slot_detailed(self.fighter)

    def hire_slot2_detailed(self) -> None:
        """Метод создающий детальное окно героя (слот 2)."""
        self.hire_slot_detailed(self.archer)

    def hire_slot3_detailed(self) -> None:
        """Метод создающий детальное окно героя (слот 3)."""
        self.hire_slot_detailed(self.mage)

    def hire_slot4_detailed(self) -> None:
        """Метод создающий детальное окно героя (слот 4)."""
        self.hire_slot_detailed(self.rog)
