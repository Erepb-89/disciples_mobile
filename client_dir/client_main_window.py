import os.path
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem, QMovie
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QMessageBox

from battle import Battle
from client_dir.capital_window import CapitalWindow
from client_dir.choose_window import ChooseRaceWindow
from client_dir.fight_window import FightWindow
from client_dir.client_main_form import Ui_MainWindow
from client_dir.hire_menu_window import HireMenuWindow
from client_dir.settings import UNIT_ICONS, GIF_ANIMATIONS, TOWN_IMG
from client_dir.unit_dialog import UnitSlotDialog
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
        self.curr_faction = ''
        self.factory = None

        self.InitUI()

    def InitUI(self):
        # Загружаем конфигурацию окна из дизайнера
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # all_units = self.database.show_all_units()[0]
        # photo = all_units.photo

        self.hbox = QHBoxLayout(self)
        self.ui.listAllUnits.clicked.connect(self.on_listView_clicked)

        self.ui.listAllUnits.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn)
        self.ui.listAllUnits.setWordWrap(True)

        self.ui.pushButtonHire.clicked.connect(self.hire_unit_action)
        self.ui.pushButtonDelete.clicked.connect(self.delete_unit_action)
        self.ui.pushButtonCapital.clicked.connect(self.show_capital)
        self.ui.pushButtonChooseRace.clicked.connect(self.show_choose_race)
        self.ui.pushButtonFight.clicked.connect(self.show_fight_window)

        self.ui.pushButtonSlot1.clicked.connect(self.slot1_detailed)
        self.ui.pushButtonSlot2.clicked.connect(self.slot2_detailed)
        self.ui.pushButtonSlot3.clicked.connect(self.slot3_detailed)
        self.ui.pushButtonSlot4.clicked.connect(self.slot4_detailed)
        self.ui.pushButtonSlot5.clicked.connect(self.slot5_detailed)
        self.ui.pushButtonSlot6.clicked.connect(self.slot6_detailed)

        self.ui.swap12.clicked.connect(self.unit_swap_action)

        self.units_list_update()
        self.player_list_update()
        self.player_slots_update()
        self.get_current_faction()
        self.set_capital_image()

        self.show()

    def closeEvent(self, event):
        """Закрытие всех окон по выходу из главного"""
        os.sys.exit(0)

    def mousePressEvent(self, event):
        """re-implemented to suppress Right-Clicks from selecting items."""

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                print('right click')
                return

            else:
                super(ClientMainWindow, self).mousePressEvent(event)

    def on_listView_clicked(self):
        selected = self.ui.listAllUnits.currentIndex().data()
        lbl = self.ui.iconLabel
        lbl.setPixmap(QPixmap(
            os.path.join(UNIT_ICONS, f"{selected} (Disciples II)-иконка.jpg")))

        self.show_gif(selected)
        self.hbox.addWidget(lbl)
        self.setLayout(self.hbox)

    def set_size_by_unit(self, unit, ui_obj):
        try:
            if unit.size == "Большой":
                ui_obj.setFixedWidth(225)
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

    # def slot1_update(self):
    #     unit = self.database.get_unit_by_slot(1)
    #     slot = self.ui.slot1
    #     slot.setPixmap(QPixmap(self.get_unit_image(unit)))
    #     self.hbox.addWidget(slot)
    #     self.setLayout(self.hbox)

    def get_current_faction(self):
        self.curr_faction = self.database.current_game_faction()
        self.ui.currentFaction.setText(self.curr_faction)

    def set_capital_image(self):
        self.ui.capital.setPixmap(QPixmap(
            self.get_capital_image(self.curr_faction)))
        self.ui.capital.setGeometry(QtCore.QRect(0, 0, 12, 12))

    def get_capital_image(self, faction):
        try:
            return os.path.join(TOWN_IMG, f"{faction}.png")
        except Exception as err:
            print(err)

    def get_unit_image(self, unit):
        try:
            return os.path.join(UNIT_ICONS, f"{unit.name} (Disciples II)-иконка.jpg")
        # except Exception as err:
        #     print(err)
        except:
            return os.path.join(UNIT_ICONS, "Заглушка (Disciples II)-иконка.jpg")

    def show_gif(self, unit_name):
        gif_label = self.ui.gifLabel
        # print(unit.name)
        try:
            gif = QMovie(os.path.join(GIF_ANIMATIONS, f"{unit_name}.gif"))
            gif_label.setMovie(gif)
            gif.start()
        except:
            gif_label.setPixmap(QPixmap(os.path.join(
                UNIT_ICONS, "Заглушка (Disciples II)-иконка.jpg")))

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
        # self.slot1_update()

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

    def unit_swap_action(self):
        self_unit = self.database.get_unit_by_slot(1)
        print(self_unit)
        other_unit = self.database.get_unit_by_slot(2)
        print(other_unit.slot)

        try:
            self.database.update_unit_slot(1, 2)
        except AttributeError as err:
            print(f'Error: {err}')

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
            # selected = self.ui.listPlayerUnits.currentIndex().data()
            selected_slot = self.ui.listPlayerSlots.currentIndex().data()
            self.database.delete_unit(int(selected_slot))

            self.player_list_update()
        except Exception as err:
            print(f'Error: {err}')

    def hire_unit_action(self):
        """Метод обработчик нажатия кнопки 'Нанять'"""
        try:
            selected_slot = self.ui.listPlayerSlots.currentIndex().data()
            selected = self.ui.listAllUnits.currentIndex().data()
            self.database.hire_unit(selected, int(selected_slot))
            self.player_list_update()
        except Exception as err:
            print(f'Error: {err}')

    def add_unit_in_dungeon(self):
        """Метод обработчик нажатия кнопки 'Добавить'"""
        try:
            selected_slot = self.ui.listPlayerSlots.currentIndex().data()
            selected = self.ui.listAllUnits.currentIndex().data()
            self.database.hire_unit(selected, int(selected_slot))
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

    def show_fight_window(self):
        """Метод создающий окно Битвы."""
        try:
            global fight_window
            fight_window = FightWindow(self.database)
            fight_window.show()
        except Exception as err:
            print(err)

    def show_capital(self):
        """Метод создающий окно Столицы игрока."""
        global capital_window
        capital_window = CapitalWindow(self.database)
        capital_window.show()

    def show_choose_race(self):
        """Метод создающий окно выбора фракции игрока."""
        global choose_window
        try:
            choose_window = ChooseRaceWindow(self.database)
            choose_window.show()
        except Exception as err:
            print(err)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClientMainWindow(main_db)
    sys.exit(app.exec_())
