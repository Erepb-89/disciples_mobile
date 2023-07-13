"""Главное окно клиента"""

import os.path
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem, QMovie, QDrag
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QPushButton

from client_dir.capital_window import CapitalWindow
from client_dir.choose_window import ChooseRaceWindow
from client_dir.fight_window import FightWindow
from client_dir.campaign_window import CampaignWindow
from client_dir.client_main_form import Ui_MainWindow
from client_dir.hire_menu_window import HireMenuWindow
from client_dir.settings import UNIT_ICONS, GIF_ANIMATIONS, TOWN_IMG, PLUG, ICON, COMMON, UNIT_ATTACK, FRONT
from client_dir.ui_functions import get_unit_image
from client_dir.unit_dialog import UnitDialog
from units_dir.units import main_db


class ClientMainWindow(QMainWindow):
    """
    Класс - основное окно пользователя.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла client_main_form.py
    """

    def __init__(self, database):
        super().__init__()
        # основные переменные
        self.database = database

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

        self.ui.listAllUnits.clicked.connect(self.on_listView_clicked)

        self.ui.listAllUnits.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn)
        self.ui.listAllUnits.setWordWrap(True)

        self.ui.pushButtonHire.clicked.connect(self.hire_unit_action)
        self.ui.pushButtonDelete.clicked.connect(self.delete_unit_action)
        self.ui.pushButtonCapital.clicked.connect(self.show_capital)
        self.ui.pushButtonChooseRace.clicked.connect(self.show_choose_race)
        self.ui.pushButtonFight.clicked.connect(self.show_fight_window)
        self.ui.pushButtonCampaign.clicked.connect(self.show_campaign_window)
        self.ui.pushButtonVersus.clicked.connect(self.show_versus_window)

        self.ui.pushButtonHireEn.clicked.connect(self.hire_enemy_unit_action)
        self.ui.pushButtonDeleteEn.clicked.connect(
            self.delete_enemy_unit_action)

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

        # self.ui.copyUnit.clicked.connect(self.swap_units_action)
        self.ui.pushButtonAddPlayer.clicked.connect(self.add_player_action)
        self.ui.pushButtonDelPlayer.clicked.connect(self.delete_player_action)
        self.ui.pushButtonChoosePlayer.clicked.connect(self.choose_player_action)

        self.all_players_list_update()
        self.units_list_update()
        self.player_list_update()
        self.player_slots_update()
        self.get_current_faction()
        self.set_capital_image()

        self.enemy_list_update()
        self.enemy_slots_update()

        self.show()

    @staticmethod
    def closeEvent(event):
        """Закрытие всех окон по выходу из главного"""
        os.sys.exit(0)

    # def mousePressEvent(self, event):
    #     """re-implemented to suppress Right-Clicks from selecting items."""
    #
    #     if event.type() == QtCore.QEvent.MouseButtonPress:
    #         if event.button() == QtCore.Qt.RightButton:
    #             print('right click')
    #             return
    #
    #         else:
    #             super(ClientMainWindow, self).mousePressEvent(event)

    def on_listView_clicked(self):
        """Показывает gif'ку выбранного из списка юнита"""
        selected = self.ui.listAllUnits.currentIndex().data()
        self.define_hire_active(selected)
        lbl = self.ui.iconLabel
        lbl.setPixmap(QPixmap(
            os.path.join(UNIT_ICONS, f"{selected} {ICON}")))

        self.show_gif(selected)
        self.hbox.addWidget(lbl)
        self.setLayout(self.hbox)

    def set_coords_for_slots(self, ui_obj):
        if ui_obj in self.right_slots:
            ui_coords = ui_obj.geometry().getCoords()
            new_coords = list(ui_coords)
            new_coords[0] = 160
            ui_obj.setGeometry(*new_coords)

            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def set_size_by_unit(self, unit, ui_obj):
        """Установка размера иконки по размеру самого юнита"""
        self.set_coords_for_slots(ui_obj)

        try:
            if unit.size == "Большой" and ui_obj in self.right_slots:
                ui_coords = ui_obj.geometry().getCoords()
                new_coords = list(ui_coords)
                new_coords[0] -= 120
                new_coords[2] = 224
                new_coords[3] = 126
                ui_obj.setGeometry(*new_coords)

            if unit.size == "Большой":
                ui_obj.setFixedWidth(225)
                ui_obj.setFixedHeight(127)

            elif unit.size == "Обычный":
                ui_obj.setFixedWidth(105)
                ui_obj.setFixedHeight(127)
        except BaseException:
            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def button_update(self, unit, button):
        """Установка размера кнопки на иконке"""
        self.set_size_by_unit(unit, button)

        self.hbox.addWidget(button)
        self.setLayout(self.hbox)

    def slot_update(self, unit, slot):
        """Установка gif'ки в иконку юнита"""
        self.set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            get_unit_image(unit)).scaled(
            slot.width(), slot.height()))
        self.hbox.addWidget(slot)
        self.setLayout(self.hbox)

    def get_current_faction(self):
        self.faction = self.database.current_game_faction
        self.ui.currentFaction.setText(self.faction)

    def set_capital_image(self):
        # self.ui.capital.setPixmap(QPixmap(
        #     self.get_capital_image(self.faction)))
        self.ui.capital.setPixmap(QPixmap(
            os.path.join(COMMON, 'breathing.png')))
        self.ui.capital.setGeometry(QtCore.QRect(0, 0, 4, 4))
        # self.ui.capital.setGeometry(QtCore.QRect(0, 0, 1380, 718))

    @staticmethod
    def get_capital_image(faction):
        """Отображение городского фона"""
        try:
            return os.path.join(TOWN_IMG, f"{faction}.png")
        except AttributeError as err:
            print(err)
            return None

    # def get_unit_image(self, unit):
    #     """Получение иконки юнита"""
    #     try:
    #         return os.path.join(UNIT_ICONS,
    #                             f"{unit.name} {ICON}")
    #     except AttributeError:
    #         return os.path.join(
    #             UNIT_ICONS, PLUG)

    def show_gif(self, unit_name):
        """Отображение gif-файла"""
        gif_label = self.ui.gifLabel
        # print(unit.name)
        try:
            gif = QMovie(os.path.join(GIF_ANIMATIONS, f"{unit_name}.gif"))
            gif_label.setMovie(gif)
            gif.start()
        except AttributeError:
            gif_label.setPixmap(QPixmap(os.path.join(
                UNIT_ICONS, PLUG)))

    def player_slots_update(self):
        """Метод обновляющий список слотов игрока."""
        player_slots = [1, 2, 3, 4, 5, 6]
        self.player_slots_model = QStandardItemModel()
        for slot in player_slots:
            item = QStandardItem(str(slot))
            item.setEditable(False)
            self.player_slots_model.appendRow(item)
        self.ui.listPlayerSlots.setModel(self.player_slots_model)

    def enemy_slots_update(self):
        """Метод обновляющий список слотов противника."""
        enemy_slots = [1, 2, 3, 4, 5, 6]
        self.enemy_slots_model = QStandardItemModel()
        for slot in enemy_slots:
            item = QStandardItem(str(slot))
            item.setEditable(False)
            self.enemy_slots_model.appendRow(item)
        self.ui.listEnemySlots.setModel(self.enemy_slots_model)

    def player_list_update(self):
        """Метод обновляющий список юнитов игрока."""
        self.universal_list_update(
            self.database.show_player_units,
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

    def enemy_list_update(self):
        """Метод обновляющий список юнитов противника."""
        self.universal_list_update(
            self.database.show_enemy_units,
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

    def units_list_update(self):
        """Метод обновляющий список юнитов."""
        self.universal_list_update(
            self.database.show_all_units,
            self.ui.listAllUnits)

    # def copy_unit_action(self):
    #     try:
    #         selected_slot = self.ui.listPlayerSlots.currentIndex().data()
    #         selected_slot_2 = self.ui.listEnemySlots.currentIndex().data()
    #         self.database.copy_player_unit(int(selected_slot), int(selected_slot_2))
    #         self.player_list_update()
    #     except TypeError:
    #         print('Выберите слот')

    def swap_unit_action(self, slot1, slot2):
        self.database.update_slot(
            slot1,
            slot2,
            self.database.PlayerUnits)
        self.player_list_update()

    def swap_enemy_unit_action(self, slot1, slot2):
        self.database.update_slot(
            slot1,
            slot2,
            self.database.CurrentDungeon)
        self.enemy_list_update()

    def swap_unit_action_12(self):
        self.swap_unit_action(1, 2)

    def swap_unit_action_13(self):
        self.swap_unit_action(1, 3)

    def swap_unit_action_24(self):
        self.swap_unit_action(2, 4)

    def swap_unit_action_34(self):
        self.swap_unit_action(3, 4)

    def swap_unit_action_35(self):
        self.swap_unit_action(3, 5)

    def swap_unit_action_46(self):
        self.swap_unit_action(4, 6)

    def swap_unit_action_56(self):
        self.swap_unit_action(5, 6)

    def swap_enemy_action_12(self):
        self.swap_enemy_unit_action(1, 2)

    def swap_enemy_action_13(self):
        self.swap_enemy_unit_action(1, 3)

    def swap_enemy_action_24(self):
        self.swap_enemy_unit_action(2, 4)

    def swap_enemy_action_34(self):
        self.swap_enemy_unit_action(3, 4)

    def swap_enemy_action_35(self):
        self.swap_enemy_unit_action(3, 5)

    def swap_enemy_action_46(self):
        self.swap_enemy_unit_action(4, 6)

    def swap_enemy_action_56(self):
        self.swap_enemy_unit_action(5, 6)

    def delete_unit_action(self):
        """Метод обработчик нажатия кнопки 'Уволить' у игрока"""
        try:
            selected_slot = self.ui.listPlayerSlots.currentIndex().data()
            self.database.delete_player_unit(int(selected_slot))
            self.player_list_update()
        except TypeError:
            print('Выберите слот, который хотите освободить')

    def delete_enemy_unit_action(self):
        """Метод обработчик нажатия кнопки 'Уволить' у противника"""
        try:
            selected_slot = self.ui.listEnemySlots.currentIndex().data()
            self.database.delete_dungeon_unit(int(selected_slot))
            self.enemy_list_update()
        except TypeError:
            print('Выберите слот, который хотите освободить')

    def define_hire_active(self, selected):
        """Определение активности кнопок 'Нанять'"""
        active_units = os.listdir(f'{UNIT_ATTACK}{FRONT}')

        if f'{selected}.gif' not in active_units:
            self.ui.pushButtonHire.setEnabled(False)
            self.ui.pushButtonHireEn.setEnabled(False)
        else:
            self.ui.pushButtonHire.setEnabled(True)
            self.ui.pushButtonHireEn.setEnabled(True)

    def hire_unit_action(self):
        """Метод обработчик нажатия кнопки 'Нанять' для игрока"""
        try:
            selected_slot = self.ui.listPlayerSlots.currentIndex().data()
            selected = self.ui.listAllUnits.currentIndex().data()
            self.database.hire_unit(selected, int(selected_slot))
            self.player_list_update()
        except TypeError:
            print('Выберите номер слота для найма')

    def hire_enemy_unit_action(self):
        """Метод обработчик нажатия кнопки 'Нанять' для противника"""
        try:
            selected_slot = self.ui.listEnemySlots.currentIndex().data()
            selected = self.ui.listAllUnits.currentIndex().data()
            self.database.hire_enemy_unit(selected, int(selected_slot))
            self.enemy_list_update()
        except TypeError:
            print('Выберите номер слота для найма')

    def show_available_units(self):
        """Метод показывающий доступных для покупки
        юнитов данной фракции."""
        global HIRE_WINDOW
        HIRE_WINDOW = HireMenuWindow(self.database)
        HIRE_WINDOW.show()

        print('Показать доступных для покупки юнитов данной фракции')
        # print(self.fighter.add_to_band(5))

    def show_fight_window(self):
        """Метод создающий окно Битвы."""
        global fight_window
        fight_window = FightWindow(self.database, 'darkest')
        fight_window.show()

    def show_campaign_window(self):
        """Метод создающий окно выбора Кампаний."""
        global campaign_window
        campaign_window = CampaignWindow(self.database)
        campaign_window.show()

    def show_versus_window(self):
        """Метод создающий окно Битвы."""
        self.database.transfer_units()

        global fight_window
        fight_window = FightWindow(self.database, 'versus')
        fight_window.show()

    def show_capital(self):
        """Метод создающий окно Столицы игрока."""
        if self.database.current_player is not None:
            global capital_window
            capital_window = CapitalWindow(self.database)
            capital_window.show()
        else:
            print('Сначала выберите игрока')

    def show_choose_race(self):
        """Метод создающий окно выбора фракции игрока."""
        if self.database.current_player is not None:
            global choose_window
            choose_window = ChooseRaceWindow(self.database)
            choose_window.show()
        else:
            print('Сначала выберите игрока')

    def all_players_list_update(self):
        self.universal_list_update(
            self.database.show_all_players,
            self.ui.PlayersList)

    def universal_list_update(self, function, ui_items_list):
        """Метод обновляющий список чего-нибудь."""
        all_items = function()

        self.items_model = QStandardItemModel()
        for i in all_items:
            item = QStandardItem(i.name)
            item.setEditable(False)
            self.items_model.appendRow(item)
        ui_items_list.setModel(self.items_model)

    def add_player_action(self):
        """Метод обработчик нажатия кнопки 'Добавить игрока'"""
        self.database.create_player(
            self.ui.PlayerName.toPlainText(),
            self.ui.Email.toPlainText())
        self.all_players_list_update()

    def delete_player_action(self):
        """Метод обработчик нажатия кнопки 'Удалить игрока'"""
        selected = self.ui.PlayersList.currentIndex().data()
        self.database.delete_player(selected)
        self.all_players_list_update()

    def choose_player_action(self):
        """Метод обработчик нажатия кнопки 'Выбрать игрока'"""
        selected = self.ui.PlayersList.currentIndex().data()
        self.database.choose_player(selected)
        self.all_players_list_update()

    def slot_detailed(self, unit, slot_dialog):
        """Метод создающий окно юнита игрока при нажатии на слот."""
        try:
            global DETAIL_WINDOW
            DETAIL_WINDOW = slot_dialog(
                self.database,
                unit)
            DETAIL_WINDOW.show()
        except AttributeError:
            pass

    def slot1_detailed(self):
        """Метод создающий окно юнита игрока (слот 1)."""
        unit = self.database.get_unit_by_slot(1, self.database.PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot2_detailed(self):
        """Метод создающий окно юнита игрока (слот 2)."""
        unit = self.database.get_unit_by_slot(2, self.database.PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot3_detailed(self):
        """Метод создающий окно юнита игрока (слот 3)."""
        unit = self.database.get_unit_by_slot(3, self.database.PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot4_detailed(self):
        """Метод создающий окно юнита игрока (слот 4)."""
        unit = self.database.get_unit_by_slot(4, self.database.PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot5_detailed(self):
        """Метод создающий окно юнита игрока (слот 5)."""
        unit = self.database.get_unit_by_slot(5, self.database.PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot6_detailed(self):
        """Метод создающий окно юнита игрока (слот 6)."""
        unit = self.database.get_unit_by_slot(6, self.database.PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def en_slot1_detailed(self):
        """Метод создающий окно вражеского юнита (слот 1)."""
        unit = self.database.get_unit_by_slot(1, self.database.CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot2_detailed(self):
        """Метод создающий окно вражеского юнита (слот 2)."""
        unit = self.database.get_unit_by_slot(2, self.database.CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot3_detailed(self):
        """Метод создающий окно вражеского юнита (слот 3)."""
        unit = self.database.get_unit_by_slot(3, self.database.CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot4_detailed(self):
        """Метод создающий окно вражеского юнита (слот 4)."""
        unit = self.database.get_unit_by_slot(4, self.database.CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot5_detailed(self):
        """Метод создающий окно вражеского юнита (слот 5)."""
        unit = self.database.get_unit_by_slot(5, self.database.CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot6_detailed(self):
        """Метод создающий окно вражеского юнита (слот 6)."""
        unit = self.database.get_unit_by_slot(6, self.database.CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def player_unit_by_slot(self, slot):
        """Метод получающий юнита игрока по слоту."""
        return self.database.get_unit_by_slot(
            slot,
            self.database.PlayerUnits)

    def enemy_unit_by_slot(self, slot):
        """Метод получающий вражеского юнита по слоту."""
        return self.database.get_unit_by_slot(
            slot,
            self.database.CurrentDungeon)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClientMainWindow(main_db)
    sys.exit(app.exec_())
