"""Окно выбора фракции"""

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.campaign_window import CampaignWindow
from client_dir.choose_faction_form import Ui_FactionWindow
from client_dir.settings import FACTIONS, EM, UH, LD, MC, SCREEN_RECT
from client_dir.ui_functions import get_image


class ChooseRaceWindow(QMainWindow):
    """
    Класс - окно выбора фракции.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла choose_faction_form.py
    """

    def __init__(self, database: any, instance: any):
        super().__init__()
        # основные переменные
        self.main = instance
        self.database = database
        self.faction_number = 1
        self.faction = EM
        self.factions = {
            1: EM,
            2: UH,
            3: LD,
            4: MC,
        }

        self.InitUI()

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""
        self.ui = Ui_FactionWindow()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)

        self.update_race()
        self.ui.pushButtonNext.clicked.connect(self.next_race)
        self.ui.pushButtonPrev.clicked.connect(self.prev_race)
        self.ui.pushButtonOK.clicked.connect(self.choose_race)
        self.ui.pushButtonBack.clicked.connect(self.back)

        self.show()

    def update_race(self):
        """Обновление лейбла, заполнение картинкой фракции"""
        self.faction = self.factions.get(self.faction_number)
        faction = self.ui.faction
        faction.setPixmap(QPixmap(get_image(FACTIONS, self.faction)))
        faction.setGeometry(SCREEN_RECT)
        self.hbox.addWidget(faction)
        self.setLayout(self.hbox)

    def next_race(self):
        """Следующая фракция"""
        if self.faction_number < 4:
            self.faction_number += 1
        else:
            self.faction_number = 1
        self.update_race()

    def prev_race(self):
        """Предыдущая фракция"""
        if self.faction_number > 1:
            self.faction_number -= 1
        else:
            self.faction_number = 4
        self.update_race()

    def choose_race(self):
        """Выбор фракции (нажатие кнопки ОК)"""
        self.database.set_faction(
            self.database.current_player.id, self.faction)
        self.database.build_default(self.faction)
        self.main.reset()

        self.close()

    def show_campaign_window(self):
        """Метод создающий окно выбора миссий в Кампании."""
        global CAMPAIGN_WINDOW
        CAMPAIGN_WINDOW = CampaignWindow(self.database)
        CAMPAIGN_WINDOW.show()

    def back(self):
        """Кнопка возврата"""
        self.close()
