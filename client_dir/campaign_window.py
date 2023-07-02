import os.path

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.campaign_form import Ui_CampaignWindow
from client_dir.fight_window import FightWindow
from client_dir.army_dialog import EnemyArmyDialog
from client_dir.settings import HIRE_SCREEN


class CampaignWindow(QMainWindow):
    """
    Класс - окно выбора Кампании.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла campaign_form.py
    """

    def __init__(self, database):
        super().__init__()
        # основные переменные
        self.database = database
        self.current_faction = self.database.current_game_faction

        self.InitUI()

    def InitUI(self):
        # Загружаем конфигурацию окна из дизайнера
        self.ui = Ui_CampaignWindow()
        self.ui.setupUi(self)
        self.hbox = QHBoxLayout(self)

        self.ui.pushButtonFight.clicked.connect(
            self.show_fight_window)
        self.ui.ExitButton.clicked.connect(self.back)

        self.ui.pushButtonSlot1.clicked.connect(
            self.highlight_selected_1)
        self.ui.pushButtonSlot2.clicked.connect(
            self.highlight_selected_2)
        self.ui.pushButtonSlot3.clicked.connect(
            self.highlight_selected_3)
        self.ui.pushButtonSlot4.clicked.connect(
            self.highlight_selected_4)

        self.show()

    def show_fight_window(self):
        """Метод создающий окно Битвы."""
        global fight_window
        fight_window = FightWindow(self.database, 'darkest')
        fight_window.show()

    def mission_slot_detailed(self, database, slot):
        """Метод создающий окно просмотра армии."""
        try:
            global DETAIL_WINDOW
            DETAIL_WINDOW = EnemyArmyDialog(
                database,
                slot)
            DETAIL_WINDOW.show()
        except Exception as err:
            print(err)

    def unlight_all(self):
        self.ui.labelSelected1.setLineWidth(0)
        self.ui.labelSelected2.setLineWidth(0)
        self.ui.labelSelected3.setLineWidth(0)
        self.ui.labelSelected4.setLineWidth(0)

    def highlight_selected_1(self):
        """Подсветка выбранной миссии"""
        self.unlight_all()
        self.ui.labelSelected1.setLineWidth(2)
        self.mission_slot_detailed(self.database, 1)

    def highlight_selected_2(self):
        """Подсветка выбранной миссии"""
        self.unlight_all()
        self.ui.labelSelected2.setLineWidth(2)
        self.mission_slot_detailed(self.database, 2)

    def highlight_selected_3(self):
        """Подсветка выбранной миссии"""
        self.unlight_all()
        self.ui.labelSelected3.setLineWidth(2)
        self.mission_slot_detailed(self.database, 3)

    def highlight_selected_4(self):
        """Подсветка выбранной миссии"""
        self.unlight_all()
        self.ui.labelSelected4.setLineWidth(2)
        self.mission_slot_detailed(self.database, 4)

    def back(self):
        """Кнопка возврата"""
        self.close()
