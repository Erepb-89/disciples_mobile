import os.path

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem, QMovie
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.hire_menu_form import Ui_HireMenu
from client_dir.settings import UNIT_ICONS, GIF_ANIMATIONS, HIRE_SCREEN
from client_dir.unit_dialog import UnitNameDialog
from units_dir.units_factory import AbstractFactory


class HireMenuWindow(QMainWindow):
    """
    Класс - окно выбора фракции.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла hire_menu_form.py
    """

    def __init__(self, database):
        super().__init__()
        # основные переменные
        self.database = database
        self.current_faction = self.database.current_game_faction()
        self.factory = AbstractFactory.create_factory(self.current_faction)
        self.fighter = self.factory.create_fighter()
        self.archer = self.factory.create_archer()
        self.mage = self.factory.create_mage()
        self.support = self.factory.create_support()
        self.special = self.factory.create_special()

        self.InitUI()

    def InitUI(self):
        # Загружаем конфигурацию окна из дизайнера
        self.ui = Ui_HireMenu()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)
        self.update_bg()

        self.ui.pushButtonSlot1.clicked.connect(self.slot1_detailed)
        self.ui.pushButtonSlot2.clicked.connect(self.slot2_detailed)
        self.ui.pushButtonSlot3.clicked.connect(self.slot3_detailed)
        self.ui.pushButtonSlot4.clicked.connect(self.slot4_detailed)
        self.ui.pushButtonSlot5.clicked.connect(self.slot5_detailed)

        self.unit_list_update()
        self.show_gif(self.fighter, self.ui.gifLabel1)
        self.show_gif(self.archer, self.ui.gifLabel2)
        self.show_gif(self.mage, self.ui.gifLabel3)
        self.show_gif(self.support, self.ui.gifLabel4)
        self.show_gif(self.special, self.ui.gifLabel5)

        self.ui.pushButtonBack.clicked.connect(self.back)

        self.show()

    def update_bg(self):
        """Обновление бэкграунда, заполнение картинкой найма"""
        hire_menu_bg = self.ui.hireMenuBG
        # hire_menu_bg.setPixmap(QPixmap(self.get_image(self.current_faction)))
        hire_menu_bg.setPixmap(QPixmap(os.path.join(HIRE_SCREEN, "hire_window.png")))
        hire_menu_bg.setGeometry(QtCore.QRect(0, 0, 788, 828))
        self.hbox.addWidget(hire_menu_bg)
        self.setLayout(self.hbox)

    def get_image(self, current_faction):
        """Достаем картинку найма армии фракции"""
        try:
            return os.path.join(HIRE_SCREEN, f"{current_faction}.png")
        except:
            return os.path.join(HIRE_SCREEN, "Elven Alliance.png")

    def back(self):
        """Кнопка возврата"""
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

        self.slot_frame_update(self.fighter, self.ui.slotFrame1)
        self.slot_frame_update(self.archer, self.ui.slotFrame2)
        self.slot_frame_update(self.mage, self.ui.slotFrame3)
        self.slot_frame_update(self.support, self.ui.slotFrame4)
        self.slot_frame_update(self.special, self.ui.slotFrame5)

    def slot_frame_update(self, unit, slot_frame):
        try:
            if unit.size == "Большой":
                slot_frame.setPixmap(QPixmap(os.path.join(HIRE_SCREEN, "hire_lbl_big.png")))
                slot_frame.setFixedWidth(246)
                slot_frame.setFixedHeight(149)
            else:
                slot_frame.setPixmap(QPixmap(os.path.join(HIRE_SCREEN, "hire_lbl_small.png")))
                slot_frame.setFixedWidth(125)
                slot_frame.setFixedHeight(149)
        except Exception as err:
            print(err)

    # def slot_update(self, unit, slot):
    #     slot.setPixmap(QPixmap(self.get_unit_image(unit)))
    #     self.hbox.addWidget(slot)
    #     self.setLayout(self.hbox)

    def set_size_by_unit(self, unit, button):
        if unit.size == "Большой":
            button.setFixedWidth(224)
            button.setFixedHeight(127)
        else:
            button.setFixedWidth(105)
            button.setFixedHeight(127)

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

    def show_gif(self, unit, gif_label):
        try:
            gif = QMovie(os.path.join(GIF_ANIMATIONS, f"{unit.name}.gif"))
            gif_label.setMovie(gif)
            gif.start()
        except:
            gif_label.setPixmap(QPixmap(os.path.join(
                UNIT_ICONS, "Заглушка (Disciples II)-иконка.jpg")))

    def slot1_detailed(self):
        """Метод создающий окно юнита (слот 1)."""
        try:
            global detail_window
            detail_window = UnitNameDialog(self.database, self.fighter.name)
            detail_window.show()
        except Exception as err:
            print(err)

    def slot2_detailed(self):
        """Метод создающий окно юнита (слот 2)."""
        try:
            global detail_window
            detail_window = UnitNameDialog(self.database, self.archer.name)
            detail_window.show()
        except Exception as err:
            print(err)

    def slot3_detailed(self):
        """Метод создающий окно юнита (слот 3)."""
        try:
            global detail_window
            detail_window = UnitNameDialog(self.database, self.mage.name)
            detail_window.show()
        except Exception as err:
            print(err)

    def slot4_detailed(self):
        """Метод создающий окно юнита (слот 4)."""
        try:
            global detail_window
            detail_window = UnitNameDialog(self.database, self.support.name)
            detail_window.show()
        except Exception as err:
            print(err)

    def slot5_detailed(self):
        """Метод создающий окно юнита (слот 5)."""
        try:
            global detail_window
            detail_window = UnitNameDialog(self.database, self.special.name)
            detail_window.show()
        except:
            self.show_available_units()
            self.slot5_update()
