"""Главное окно клиента"""

import os.path
import sys
from collections import namedtuple
from typing import Callable, Optional

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QStandardItemModel, \
    QStandardItem, QMovie
from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QHBoxLayout

from client_dir.capital_window import CapitalWindow
from client_dir.choose_window import ChooseRaceWindow
from client_dir.fight_window import FightWindow
from client_dir.campaign_window import CampaignWindow
from client_dir.client_main_form import Ui_MainWindow
from client_dir.hire_menu_window import HireMenuWindow
from client_dir.question_window import QuestionWindow
from client_dir.settings import UNIT_ICONS, GIF_ANIMATIONS, \
    TOWN_IMG, PLUG, ICON, PORTRAITS, BACKGROUND, BIG, \
    ACTIVE_UNITS
from client_dir.ui_functions import get_unit_image, \
    set_beige_colour, set_borders, ui_lock, ui_unlock
from client_dir.unit_dialog import UnitDialog
from units_dir.units import main_db


class ClientMainWindow(QMainWindow):
    """
    Класс - основное окно пользователя.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла client_main_form.py
    """

    def __init__(self):
        super().__init__()
        # основные переменные
        self.name = 'ClientMainWindow'
        self.question = False  # увольнение
        self.difficulty = 2

        self.player_units_model = None
        self.player_slots_model = None
        self.enemy_units_model = None
        self.enemy_slots_model = None
        self.faction = ''
        self.factory = None

        self.InitUI()

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.hbox = QHBoxLayout(self)

        self.right_slots = [
            self.ui.slot2,
            self.ui.slot4,
            self.ui.slot6,
            self.ui.pushButtonSlot2,
            self.ui.pushButtonSlot4,
            self.ui.pushButtonSlot6,
        ]

        self.ui.listAllUnits.clicked.connect(self.on_list_clicked)

        self.ui.listAllUnits.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn)
        self.ui.listAllUnits.setWordWrap(True)

        self.ui.pushButtonHire.clicked.connect(self.hire_unit_action)
        self.ui.pushButtonHire.setStatusTip('Выберите номер слота для найма')
        self.ui.pushButtonDelete.clicked.connect(self.delete_unit_action)
        self.ui.pushButtonDelete.setStatusTip(
            'Выберите слот, который хотите освободить')
        self.ui.pushButtonCapital.clicked.connect(self.show_capital)
        self.ui.pushButtonChooseRace.clicked.connect(self.show_choose_race)
        self.ui.pushButtonFight.clicked.connect(self.show_fight_window)
        self.ui.pushButtonCampaign.clicked.connect(self.show_campaign_window)
        self.ui.pushButtonVersus.clicked.connect(self.show_versus_window)

        self.ui.pushButtonHireEn.clicked.connect(self.hire_enemy_unit_action)
        self.ui.pushButtonHireEn.setStatusTip(
            'Выберите номер слота для найма')
        self.ui.pushButtonDeleteEn.clicked.connect(
            self.delete_enemy_unit_action)
        self.ui.pushButtonDeleteEn.setStatusTip(
            'Выберите слот, который хотите освободить')

        self.ui.pushButtonSlot1.clicked.connect(self.slot1_detailed)
        self.ui.pushButtonSlot2.clicked.connect(self.slot2_detailed)
        self.ui.pushButtonSlot3.clicked.connect(self.slot3_detailed)
        self.ui.pushButtonSlot4.clicked.connect(self.slot4_detailed)
        self.ui.pushButtonSlot5.clicked.connect(self.slot5_detailed)
        self.ui.pushButtonSlot6.clicked.connect(self.slot6_detailed)

        self.ui.pushButtonEnSlot1.clicked.connect(self.en_slot1_detailed)
        self.ui.pushButtonEnSlot2.clicked.connect(self.en_slot2_detailed)
        self.ui.pushButtonEnSlot3.clicked.connect(self.en_slot3_detailed)
        self.ui.pushButtonEnSlot4.clicked.connect(self.en_slot4_detailed)
        self.ui.pushButtonEnSlot5.clicked.connect(self.en_slot5_detailed)
        self.ui.pushButtonEnSlot6.clicked.connect(self.en_slot6_detailed)

        self.ui.swap12.clicked.connect(self.swap_unit_action_12)
        self.ui.swap13.clicked.connect(self.swap_unit_action_13)
        self.ui.swap24.clicked.connect(self.swap_unit_action_24)
        self.ui.swap34.clicked.connect(self.swap_unit_action_34)
        self.ui.swap35.clicked.connect(self.swap_unit_action_35)
        self.ui.swap46.clicked.connect(self.swap_unit_action_46)
        self.ui.swap56.clicked.connect(self.swap_unit_action_56)

        self.ui.enSwap12.clicked.connect(self.swap_enemy_action_12)
        self.ui.enSwap13.clicked.connect(self.swap_enemy_action_13)
        self.ui.enSwap24.clicked.connect(self.swap_enemy_action_24)
        self.ui.enSwap34.clicked.connect(self.swap_enemy_action_34)
        self.ui.enSwap35.clicked.connect(self.swap_enemy_action_35)
        self.ui.enSwap46.clicked.connect(self.swap_enemy_action_46)
        self.ui.enSwap56.clicked.connect(self.swap_enemy_action_56)

        self.ui.pushButtonAddPlayer.clicked.connect(self.add_player_action)
        self.ui.pushButtonDelPlayer.clicked.connect(self.delete_player_action)
        self.ui.pushButtonChoosePlayer.clicked.connect(
            self.choose_player_action)

        # подкраска элементов
        set_beige_colour(self.ui.swap12)
        set_beige_colour(self.ui.swap13)
        set_beige_colour(self.ui.swap24)
        set_beige_colour(self.ui.swap34)
        set_beige_colour(self.ui.swap35)
        set_beige_colour(self.ui.swap46)
        set_beige_colour(self.ui.swap56)

        set_beige_colour(self.ui.enSwap12)
        set_beige_colour(self.ui.enSwap13)
        set_beige_colour(self.ui.enSwap24)
        set_beige_colour(self.ui.enSwap34)
        set_beige_colour(self.ui.enSwap35)
        set_beige_colour(self.ui.enSwap46)
        set_beige_colour(self.ui.enSwap56)

        set_beige_colour(self.ui.pushButtonAddPlayer)
        set_beige_colour(self.ui.pushButtonDelPlayer)
        set_beige_colour(self.ui.pushButtonChoosePlayer)
        set_beige_colour(self.ui.pushButtonHire)
        set_beige_colour(self.ui.pushButtonHireEn)
        set_beige_colour(self.ui.pushButtonDelete)
        set_beige_colour(self.ui.pushButtonDeleteEn)
        set_beige_colour(self.ui.pushButtonCapital)
        set_beige_colour(self.ui.pushButtonChooseRace)
        set_beige_colour(self.ui.pushButtonFight)
        set_beige_colour(self.ui.pushButtonCampaign)
        set_beige_colour(self.ui.pushButtonVersus)

        set_beige_colour(self.ui.listAllUnits)
        set_beige_colour(self.ui.listPlayerUnits)
        set_beige_colour(self.ui.listPlayerSlots)
        set_beige_colour(self.ui.listEnemyUnits)
        set_beige_colour(self.ui.listEnemySlots)
        set_beige_colour(self.ui.PlayerName)
        set_beige_colour(self.ui.Email)
        set_beige_colour(self.ui.PlayersList)

        set_borders(self.ui.gifLabel)
        set_borders(self.ui.iconLabel)
        set_borders(self.ui.portraitLabel)

        self.ui.currentPlayer.setText(main_db.current_player.name)
        self.ui.currentPlayer.setStyleSheet('color: white')

        main_db.update_game_session()
        self.update_diff_checkbox()

        self.all_players_list_update()
        self.units_list_update()
        self.player_slots_update()
        self.reset()
        self.reset_enemy_buttons()

        self.show()

    @staticmethod
    def closeEvent(event) -> None:
        """Закрытие всех окон по выходу из главного"""
        os.sys.exit(0)

    def reset(self) -> None:
        """Обновить"""
        self.player_list_update()

        self.get_current_faction()
        self.set_capital_image()

        self.enemy_list_update()
        self.enemy_slots_update()

        self.reset_player_buttons()

    def update_diff_checkbox(self) -> None:
        """Метод заполнения выпадающего списка доступных сложностей."""
        self.ui.difficultyText.setStyleSheet('color: white')

        diff_slots = [1, 2, 3]
        self.diff_model = QStandardItemModel()
        for slot in diff_slots:
            item = QStandardItem(str(slot))
            item.setEditable(False)
            self.diff_model.appendRow(item)
        self.ui.comboDifficulty.setModel(self.diff_model)

        self.ui.comboDifficulty.setCurrentIndex(1)
        self.check_difficulty()
        self.ui.comboDifficulty.currentIndexChanged.connect(self.check_difficulty)

    def check_difficulty(self) -> None:
        """Устанавливает выбранную сложность"""
        self.difficulty = int(self.ui.comboDifficulty.currentText())

    def reset_player_buttons(self):
        """Обновление доступности кнопок игрока"""
        self.button_enabled(self.ui.swap12, main_db.PlayerUnits, 2)
        self.button_enabled(self.ui.swap34, main_db.PlayerUnits, 4)
        self.button_enabled(self.ui.swap56, main_db.PlayerUnits, 6)

    def reset_enemy_buttons(self):
        """Обновление доступности кнопок противника"""
        self.button_enabled(self.ui.enSwap12, main_db.CurrentDungeon, 2)
        self.button_enabled(self.ui.enSwap34, main_db.CurrentDungeon, 4)
        self.button_enabled(self.ui.enSwap56, main_db.CurrentDungeon, 6)

    def button_enabled(self, button, database, num2):
        """Определяет доступность кнопки по юнитам в слотах"""
        try:
            if main_db.get_unit_by_slot(
                    num2,
                    database).size == BIG:
                ui_lock(button)
            else:
                ui_unlock(button)
        except AttributeError:
            ui_unlock(button)

    def on_list_clicked(self) -> None:
        """Показывает иконку и портрет выбранного из списка юнита"""
        selected = self.ui.listAllUnits.currentIndex().data()
        self.define_hire_active(selected)

        # показываем иконку юнита
        lbl = self.ui.iconLabel
        lbl.setPixmap(QPixmap(
            os.path.join(UNIT_ICONS, f"{selected} {ICON}")))

        # показываем портрет юнита
        prt = self.ui.portraitLabel
        prt.setPixmap(QPixmap(
            os.path.join(PORTRAITS, f"{selected}.gif")))

        self.show_gif(selected)
        self.hbox.addWidget(lbl)
        self.setLayout(self.hbox)

    def set_coords_for_slots(self, ui_obj: any) -> None:
        """Установить координаты для правых слотов"""
        if ui_obj in self.right_slots:
            ui_coords = ui_obj.geometry().getCoords()
            new_coords = list(ui_coords)
            new_coords[0] = 160
            ui_obj.setGeometry(*new_coords)

            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def set_size_by_unit(self, unit, ui_obj: any) -> None:
        """Установка размера иконки по размеру самого юнита"""
        self.set_coords_for_slots(ui_obj)

        try:
            if unit.size == BIG and ui_obj in self.right_slots:
                ui_coords = ui_obj.geometry().getCoords()
                new_coords = list(ui_coords)
                new_coords[0] -= 120
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

    def button_update(self,
                      unit: namedtuple,
                      button: QtWidgets.QPushButton) -> None:
        """Установка размера кнопки на иконке"""
        self.set_size_by_unit(unit, button)

        self.hbox.addWidget(button)
        self.setLayout(self.hbox)

    def slot_update(self,
                    unit: namedtuple,
                    slot: QtWidgets.QLabel) -> None:
        """Установка gif'ки в иконку юнита"""
        self.set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            get_unit_image(unit)).scaled(
            slot.width(), slot.height()))
        self.hbox.addWidget(slot)
        self.setLayout(self.hbox)

    def get_current_faction(self) -> None:
        """Получение текущей фракции"""
        self.faction = main_db.current_faction
        self.ui.currentFaction.setText(self.faction)
        self.ui.currentFaction.setStyleSheet('color: white')

    def set_capital_image(self) -> None:
        """Установить картинку как в столице"""
        self.ui.capital.setPixmap(QPixmap(BACKGROUND))
        # self.ui.capital.setGeometry(QtCore.QRect(0, 0, 4, 4))
        self.ui.capital.setGeometry(QtCore.QRect(0, 0, 1380, 742))

    @staticmethod
    def get_capital_image(faction: str) -> Optional[str]:
        """Отображение городского фона"""
        try:
            return os.path.join(TOWN_IMG, f"{faction}.png")
        except AttributeError:
            return None

    def show_gif(self, unit_name: str) -> None:
        """Отображение gif-файла выбранного юнита"""
        gif_label = self.ui.gifLabel
        try:
            gif = QMovie(os.path.join(GIF_ANIMATIONS, f"{unit_name}.gif"))
            gif_label.setMovie(gif)
            gif.start()
        except AttributeError:
            gif_label.setPixmap(QPixmap(os.path.join(
                UNIT_ICONS, PLUG)))

    def player_slots_update(self) -> None:
        """Метод обновляющий список слотов игрока."""
        player_slots = [1, 2, 3, 4, 5, 6]
        self.player_slots_model = QStandardItemModel()
        for slot in player_slots:
            item = QStandardItem(str(slot))
            item.setEditable(False)
            self.player_slots_model.appendRow(item)
        self.ui.listPlayerSlots.setModel(self.player_slots_model)

    def enemy_slots_update(self) -> None:
        """Метод обновляющий список слотов противника."""
        enemy_slots = [1, 2, 3, 4, 5, 6]
        self.enemy_slots_model = QStandardItemModel()
        for slot in enemy_slots:
            item = QStandardItem(str(slot))
            item.setEditable(False)
            self.enemy_slots_model.appendRow(item)
        self.ui.listEnemySlots.setModel(self.enemy_slots_model)

    def player_list_update(self) -> None:
        """Метод обновляющий список юнитов игрока."""
        self.universal_list_update(
            main_db.show_player_units,
            self.ui.listPlayerUnits)

        self.player_slots_dict = {
            1: self.ui.slot1,
            2: self.ui.slot2,
            3: self.ui.slot3,
            4: self.ui.slot4,
            5: self.ui.slot5,
            6: self.ui.slot6,
        }

        self.player_buttons_dict = {
            1: self.ui.pushButtonSlot1,
            2: self.ui.pushButtonSlot2,
            3: self.ui.pushButtonSlot3,
            4: self.ui.pushButtonSlot4,
            5: self.ui.pushButtonSlot5,
            6: self.ui.pushButtonSlot6,
        }

        for num, slot in self.player_slots_dict.items():
            self.slot_update(
                self.player_unit_by_slot(num),
                slot)

        for num, button in self.player_buttons_dict.items():
            self.button_update(
                self.player_unit_by_slot(num),
                button)

        # self.ui.listPlayerUnits.setModel(self.player_units_model)

    def enemy_list_update(self) -> None:
        """Метод обновляющий список юнитов противника."""
        self.universal_list_update(
            main_db.show_enemy_units,
            self.ui.listEnemyUnits)

        self.enemy_slots_dict = {
            1: self.ui.EnemySlot1,
            2: self.ui.EnemySlot2,
            3: self.ui.EnemySlot3,
            4: self.ui.EnemySlot4,
            5: self.ui.EnemySlot5,
            6: self.ui.EnemySlot6,
        }

        self.enemy_buttons_dict = {
            1: self.ui.pushButtonEnSlot1,
            2: self.ui.pushButtonEnSlot2,
            3: self.ui.pushButtonEnSlot3,
            4: self.ui.pushButtonEnSlot4,
            5: self.ui.pushButtonEnSlot5,
            6: self.ui.pushButtonEnSlot6,
        }

        for num, slot in self.enemy_slots_dict.items():
            self.slot_update(
                self.enemy_unit_by_slot(num),
                slot)

        for num, button in self.enemy_buttons_dict.items():
            self.button_update(
                self.enemy_unit_by_slot(num),
                button)

        # self.ui.listEnemyUnits.setModel(self.enemy_units_model)

    def units_list_update(self) -> None:
        """Метод обновляющий список юнитов."""
        self.universal_list_update(
            main_db.show_all_units,
            self.ui.listAllUnits)

    def check_and_swap(self, num1: int, num2: int, database: any) -> bool:
        """
        Проверить юниты в слотах на наличие и размер.
        Поменять местами вместе с парным юнитом (соседний слот)
        """
        unit1 = main_db.get_unit_by_slot(num1, database)
        unit2 = main_db.get_unit_by_slot(num2, database)
        func = self.swap_unit_action

        if database == main_db.CurrentDungeon:
            func = self.swap_enemy_action

        if unit1 is not None \
                and unit2 is not None \
                and unit1.size == BIG \
                and unit2.size == BIG:
            func(num1, num2)
            return True

        if unit1 is not None \
                and unit1.size == BIG:
            func(num1 - 1, num2 - 1)
            func(num1, num2)
            return True

        if unit2 is not None \
                and unit2.size == BIG:
            func(num1 - 1, num2 - 1)
            func(num1, num2)
            return True

        return False

    def swap_unit_action(self, slot1: int, slot2: int) -> None:
        """Меняет слоты двух юнитов игрока"""
        main_db.update_slot(
            slot1,
            slot2,
            main_db.PlayerUnits)
        self.player_list_update()
        self.reset_player_buttons()

    def swap_enemy_action(self, slot1: int, slot2: int) -> None:
        """Меняет слоты двух юнитов подземелья"""
        main_db.update_slot(
            slot1,
            slot2,
            main_db.CurrentDungeon)
        self.enemy_list_update()
        self.reset_enemy_buttons()

    def swap_unit_action_12(self) -> None:
        """Меняет местами юнитов игрока в слотах 1 и 2"""
        self.swap_unit_action(1, 2)

    def swap_unit_action_13(self) -> None:
        """Меняет местами юнитов игрока в слотах 1 и 3"""
        if not self.check_and_swap(2, 4, main_db.PlayerUnits):
            self.swap_unit_action(1, 3)

    def swap_unit_action_24(self) -> None:
        """Меняет местами юнитов игрока в слотах 2 и 4"""
        if not self.check_and_swap(2, 4, main_db.PlayerUnits):
            self.swap_unit_action(2, 4)

    def swap_unit_action_34(self) -> None:
        """Меняет местами юнитов игрока в слотах 3 и 4"""
        self.swap_unit_action(3, 4)

    def swap_unit_action_35(self) -> None:
        """Меняет местами юнитов игрока в слотах 3 и 5"""
        if not self.check_and_swap(4, 6, main_db.PlayerUnits):
            self.swap_unit_action(3, 5)

    def swap_unit_action_46(self) -> None:
        """Меняет местами юнитов игрока в слотах 4 и 6"""
        if not self.check_and_swap(4, 6, main_db.PlayerUnits):
            self.swap_unit_action(4, 6)

    def swap_unit_action_56(self) -> None:
        """Меняет местами юнитов игрока в слотах 5 и 6"""
        self.swap_unit_action(5, 6)

    def swap_enemy_action_12(self) -> None:
        """Меняет местами юнитов подземелья в слотах 1 и 2"""
        self.swap_enemy_action(1, 2)

    def swap_enemy_action_13(self) -> None:
        """Меняет местами юнитов подземелья в слотах 1 и 3"""
        if not self.check_and_swap(2, 4, main_db.CurrentDungeon):
            self.swap_enemy_action(1, 3)

    def swap_enemy_action_24(self) -> None:
        """Меняет местами юнитов подземелья в слотах 2 и 4"""
        if not self.check_and_swap(2, 4, main_db.CurrentDungeon):
            self.swap_enemy_action(2, 4)

    def swap_enemy_action_34(self) -> None:
        """Меняет местами юнитов подземелья в слотах 3 и 4"""
        self.swap_enemy_action(3, 4)

    def swap_enemy_action_35(self) -> None:
        """Меняет местами юнитов подземелья в слотах 3 и 5"""
        if not self.check_and_swap(4, 6, main_db.CurrentDungeon):
            self.swap_enemy_action(3, 5)

    def swap_enemy_action_46(self) -> None:
        """Меняет местами юнитов подземелья в слотах 4 и 6"""
        if not self.check_and_swap(4, 6, main_db.CurrentDungeon):
            self.swap_enemy_action(4, 6)

    def swap_enemy_action_56(self) -> None:
        """Меняет местами юнитов подземелья в слотах 5 и 6"""
        self.swap_enemy_action(5, 6)

    def delete_unit_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Уволить' у игрока"""
        selected_slot = self.ui.listPlayerSlots.currentIndex().data()
        unit = main_db.get_unit_by_slot(
            selected_slot,
            main_db.PlayerUnits)

        if unit is not None:
            global QUESTION_WINDOW
            text = f'Вы действительно хотите уволить {unit.name}?'
            QUESTION_WINDOW = QuestionWindow(self, text)
            QUESTION_WINDOW.show()

    def confirmation(self):
        """Подтверждение 'Увольнения' юнита игрока"""
        if self.question:
            selected_slot = self.ui.listPlayerSlots.currentIndex().data()
            main_db.delete_player_unit(int(selected_slot))
            self.player_list_update()
            self.reset_player_buttons()

    def delete_enemy_unit_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Уволить' у противника"""
        try:
            selected_slot = self.ui.listEnemySlots.currentIndex().data()
            main_db.delete_dungeon_unit(int(selected_slot))
            self.enemy_list_update()
            self.reset_enemy_buttons()
        except TypeError:
            print('Выберите слот, который хотите освободить')

    def define_hire_active(self, selected: str) -> None:
        """Определение активности кнопок 'Нанять'"""
        if f'{selected}.gif' not in ACTIVE_UNITS:
            ui_lock(self.ui.pushButtonHire)
            ui_lock(self.ui.pushButtonHireEn)
        else:
            ui_unlock(self.ui.pushButtonHire)
            ui_unlock(self.ui.pushButtonHireEn)

    def hire_unit_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Нанять' для игрока"""
        try:
            selected_slot = self.ui.listPlayerSlots.currentIndex().data()
            selected = self.ui.listAllUnits.currentIndex().data()
            main_db.hire_unit(
                selected,
                int(selected_slot))
            self.player_list_update()
        except TypeError:
            print('Выберите номер слота для найма')

    def hire_enemy_unit_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Нанять' для противника"""
        try:
            selected_slot = self.ui.listEnemySlots.currentIndex().data()
            selected = self.ui.listAllUnits.currentIndex().data()
            main_db.hire_enemy_unit(
                selected,
                int(selected_slot))
            self.enemy_list_update()
        except TypeError:
            print('Выберите номер слота для найма')

    def show_available_units(self, slot: int) -> None:
        """Метод показывающий доступных для покупки
        юнитов данной фракции."""
        global HIRE_WINDOW
        HIRE_WINDOW = HireMenuWindow(slot, self)
        HIRE_WINDOW.show()

        print('Показать доступных для покупки юнитов данной фракции')

    def show_fight_window(self) -> None:
        """Метод создающий окно Битвы."""
        global FIGHT_WINDOW
        FIGHT_WINDOW = FightWindow('darkest', self)
        FIGHT_WINDOW.show()

    def show_campaign_window(self) -> None:
        """Метод создающий окно выбора Кампаний."""
        global CAMPAIGN_WINDOW
        CAMPAIGN_WINDOW = CampaignWindow(self)
        CAMPAIGN_WINDOW.show()

    def show_versus_window(self) -> None:
        """Метод создающий окно Битвы."""
        main_db.transfer_units()
        self.reset()

        global FIGHT_WINDOW
        FIGHT_WINDOW = FightWindow('versus', self)
        FIGHT_WINDOW.show()

    def show_capital(self) -> None:
        """Метод создающий окно Столицы игрока."""
        if main_db.current_player is not None:
            global CAPITAL_WINDOW
            CAPITAL_WINDOW = CapitalWindow(self)
            CAPITAL_WINDOW.show()
        else:
            print('Сначала выберите игрока')

    def show_choose_race(self) -> None:
        """Метод создающий окно выбора фракции игрока."""
        if main_db.current_player is not None:
            global CHOOSE_WINDOW
            CHOOSE_WINDOW = ChooseRaceWindow(self)
            CHOOSE_WINDOW.show()
        else:
            print('Сначала выберите игрока')

    def all_players_list_update(self) -> None:
        """Обновление списка всех игроков"""
        self.universal_list_update(
            main_db.show_all_players,
            self.ui.PlayersList)

    def universal_list_update(self,
                              function: Callable,
                              ui_items_list: QtWidgets.QListView) -> None:
        """Метод обновляющий список чего-нибудь."""
        all_items = function()

        self.items_model = QStandardItemModel()
        for i in all_items:
            item = QStandardItem(i.name)
            item.setEditable(False)
            self.items_model.appendRow(item)
        ui_items_list.setModel(self.items_model)

    def add_player_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Добавить игрока'"""
        main_db.create_player(
            self.ui.PlayerName.toPlainText(),
            self.ui.Email.toPlainText())
        self.all_players_list_update()

    def delete_player_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Удалить игрока'"""
        selected = self.ui.PlayersList.currentIndex().data()
        main_db.delete_player(selected)
        self.all_players_list_update()

    def choose_player_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Выбрать игрока'"""
        selected = self.ui.PlayersList.currentIndex().data()
        main_db.choose_player(selected)

        self.ui.currentPlayer.setText(selected)
        self.ui.currentPlayer.setStyleSheet('color: white')
        self.all_players_list_update()

    def slot_detailed(self, unit: namedtuple, slot_dialog: any) -> None:
        """Метод создающий окно юнита игрока при нажатии на слот."""
        try:
            global DETAIL_WINDOW
            DETAIL_WINDOW = slot_dialog(
                unit)
            DETAIL_WINDOW.show()
        except AttributeError:
            pass

    def slot1_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 1)."""
        unit = main_db.get_unit_by_slot(1, main_db.PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot2_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 2)."""
        unit = main_db.get_unit_by_slot(2, main_db.PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot3_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 3)."""
        unit = main_db.get_unit_by_slot(3, main_db.PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot4_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 4)."""
        unit = main_db.get_unit_by_slot(4, main_db.PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot5_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 5)."""
        unit = main_db.get_unit_by_slot(5, main_db.PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot6_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 6)."""
        unit = main_db.get_unit_by_slot(6, main_db.PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def en_slot1_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 1)."""
        unit = main_db.get_unit_by_slot(1, main_db.CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot2_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 2)."""
        unit = main_db.get_unit_by_slot(2, main_db.CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot3_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 3)."""
        unit = main_db.get_unit_by_slot(3, main_db.CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot4_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 4)."""
        unit = main_db.get_unit_by_slot(4, main_db.CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot5_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 5)."""
        unit = main_db.get_unit_by_slot(5, main_db.CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot6_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 6)."""
        unit = main_db.get_unit_by_slot(6, main_db.CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    @staticmethod
    def player_unit_by_slot(slot: int) -> namedtuple:
        """Метод получающий юнита игрока по слоту."""
        return main_db.get_unit_by_slot(
            slot,
            main_db.PlayerUnits)

    @staticmethod
    def enemy_unit_by_slot(slot: int) -> namedtuple:
        """Метод получающий вражеского юнита по слоту."""
        return main_db.get_unit_by_slot(
            slot,
            main_db.CurrentDungeon)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClientMainWindow()
    sys.exit(app.exec_())
