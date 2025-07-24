"""Окно выбора фракции"""

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.forms.choose_faction_form import Ui_FactionWindow
from client_dir.windows.choose_hero_window import ChooseHeroWindow
from client_dir.windows.question_window import QuestionWindow
from client_dir.settings import FACTIONS, EM, UH, LD, MC, SCREEN_RECT
from client_dir.ui_functions import get_image
from units_dir.visual_model import v_model


class ChooseRaceWindow(QMainWindow):
    """
    Класс - окно выбора фракции.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла choose_faction_form.py
    """

    def __init__(self, parent_window: any):
        super().__init__()
        # основные переменные
        self.main = parent_window
        self.question = True  # Новая игра
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

    def update_race(self) -> None:
        """Обновление лейбла, заполнение картинкой фракции"""
        self.faction = self.factions.get(self.faction_number)
        faction = self.ui.faction
        faction.setPixmap(QPixmap(get_image(FACTIONS, self.faction)))
        faction.setGeometry(SCREEN_RECT)
        self.hbox.addWidget(faction)
        self.setLayout(self.hbox)

    def next_race(self) -> None:
        """Следующая фракция"""
        if self.faction_number < 4:
            self.faction_number += 1
        else:
            self.faction_number = 1
        self.update_race()

    def prev_race(self) -> None:
        """Предыдущая фракция"""
        if self.faction_number > 1:
            self.faction_number -= 1
        else:
            self.faction_number = 4
        self.update_race()

    @property
    def in_progress(self) -> bool:
        """Определение новой игры"""
        self.faction = self.factions.get(self.faction_number)
        session = v_model.get_session_by_faction(self.faction)

        if session is not None:
            return True
        return

    def choose_race(self) -> None:
        """Выбор фракции (нажатие кнопки ОК)"""
        # Если найдена начатая игра за фракцию
        if self.in_progress:
            self.show_question_window()
        else:
            # Новая игра
            self.question = True
            v_model.set_built_to_0()
            self.confirmation()

    def confirmation(self) -> None:
        """Подтверждение начала новой игры"""
        # Если выбрана Новая игра
        if self.question:
            self.new_game()

        # Иначе продолжаем сохраненную игру
        else:
            self.continue_game()
        self.main.reset()

        self.close()

    def new_game(self) -> None:
        """Новая игра"""
        v_model.set_current_faction(self.faction)

        # удаление старых построек за данную фракцию
        v_model.clear_buildings(v_model.current_player_name)

        # удаление старых кампаний за данную фракцию
        v_model.delete_dungeons()
        v_model.clear_session()

        v_model.set_session_for_faction_to_0(self.faction)
        v_model.set_built_to_0()

        v_model.update_game_session()

        v_model.build_default(self.faction)
        v_model.set_campaign_level_to_1()

        v_model.clear_units(self.faction)

        self.main.faction = self.faction
        self.main.check_campaign_session()

        self.choose_hero()
        self.add_capital_guard()
        self.close()

    def continue_game(self) -> None:
        """Продолжение игры"""
        v_model.set_current_faction(self.faction)
        v_model.update_game_session()

        self.main.faction = self.faction
        self.main.check_campaign_session()
        self.main.update_diff_checkbox()

    def choose_hero(self) -> None:
        """Метод создающий окно выбора героя"""
        global HERO_CHOOSE_WINDOW
        HERO_CHOOSE_WINDOW = ChooseHeroWindow(self)
        HERO_CHOOSE_WINDOW.show()

    def show_question_window(self) -> None:
        """Метод создающий окно вопроса"""
        global QUESTION_WINDOW
        text = 'Вы действительно хотите начать новую игру? ' \
               'Да - начать новую. ' \
               'Нет - продолжить сохраненную.'
        QUESTION_WINDOW = QuestionWindow(self, text)
        QUESTION_WINDOW.show()

    @staticmethod
    def add_capital_guard() -> None:
        """Метод добавляющий стража столицы"""
        v_model.hire_guard()

    def back(self) -> None:
        """Кнопка возврата"""
        self.close()
