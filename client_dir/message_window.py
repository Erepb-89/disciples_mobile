"""Окно сообщения"""
import os

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.message_form import Ui_Message
from client_dir.settings import CAPITAL_BUILDING


class MessageWindow(QMainWindow):
    """
    Класс - окно сообщения.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла message_form.py
    """

    def __init__(self, parent_window: any, text: str):
        super().__init__()
        # основные переменные
        self.parent_window = parent_window
        self.text = text

        self.InitUI()

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""
        self.ui = Ui_Message()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)
        self.update_bg()

        self.ui.messageText.setText(self.text)

        self.ui.pushButtonNO.clicked.connect(
            self.no_action)

        self.show()

    def no_action(self):
        """Закрыть"""
        self.close()

    def update_bg(self) -> None:
        """Обновление бэкграунда, заполнение картинкой"""
        message_bg = self.ui.messageBG
        message_bg.setPixmap(
            QPixmap(
                os.path.join(
                    CAPITAL_BUILDING,
                    "question.png")))
        message_bg.setGeometry(QtCore.QRect(0, 0, 552, 461))
        self.hbox.addWidget(message_bg)
        self.setLayout(self.hbox)
