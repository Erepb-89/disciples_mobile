import os.path

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.choose_faction_form import Ui_FactionWindow
from client_dir.settings import FACTIONS, EM, UH, LD, MC
from units_dir.units_factory import AbstractFactory


class ChooseRaceWindow(QMainWindow):
    """
    Класс - окно выбора фракции.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла choose_faction_form.py
    """

    def __init__(self, database):
        super().__init__()
        # основные переменные
        self.database = database
        self.factory = None
        self.faction_number = 1
        self.current_faction = EM
        self.factions = {
            1: EM,
            2: UH,
            3: LD,
            4: MC,
        }

        self.InitUI()

    def InitUI(self):
        # Загружаем конфигурацию окна из дизайнера
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
        self.current_faction = self.factions[self.faction_number]
        faction = self.ui.faction
        faction.setPixmap(QPixmap(self.get_image(self.current_faction)))
        faction.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        self.hbox.addWidget(faction)
        self.setLayout(self.hbox)

    def get_image(self, current_faction):
        """Достаем картинку фракции"""
        try:
            return os.path.join(FACTIONS, f"{current_faction}.png")
        except:
            return os.path.join(FACTIONS, "Elven Alliance.png")

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
        self.database.set_faction(1, self.current_faction)
        self.close()

    def back(self):
        """Кнопка возврата"""
        self.close()

