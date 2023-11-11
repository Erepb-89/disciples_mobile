"""Окно вопроса"""
import os

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.question_form import Ui_Question
from client_dir.settings import CAPITAL_BUILDING


class QuestionWindow(QMainWindow):
    """
    Класс - окно вопроса.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла question_form.py
    """

    def __init__(self, instance: any):
        super().__init__()
        # основные переменные
        self.instance = instance

        self.InitUI()

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""
        self.ui = Ui_Question()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)
        self.update_bg()

        self.ui.questionText.setText(
            'Вы действительно хотите начать новую игру?'
        )

        self.ui.pushButtonYES.clicked.connect(
            self.yes_action)
        self.ui.pushButtonNO.clicked.connect(
            self.no_action)

        self.show()

    def yes_action(self):

        self.instance.new_game = True
        self.instance.confirmation()
        self.close()

    def no_action(self):

        self.instance.new_game = False
        self.instance.confirmation()
        self.close()

    def update_bg(self) -> None:
        """Обновление бэкграунда, заполнение картинкой найма"""
        question_bg = self.ui.questionBG
        question_bg.setPixmap(
            QPixmap(
                os.path.join(
                    CAPITAL_BUILDING,
                    "question.png")))
        question_bg.setGeometry(QtCore.QRect(0, 0, 552, 461))
        self.hbox.addWidget(question_bg)
        self.setLayout(self.hbox)
