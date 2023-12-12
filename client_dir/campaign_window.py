"""Окно кампании"""

from typing import Callable, Dict

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.campaign_form import Ui_CampaignWindow
from client_dir.fight_window import FightWindow
from client_dir.army_dialog import EnemyArmyDialog
from client_dir.settings import BACKGROUND, MC
from client_dir.ui_functions import slot_update, button_update, \
    ui_lock, ui_unlock, show_opened, show_closed
from units_dir.mission_generator import unit_selector, \
    setup_6, setup_5, setup_4, setup_3, setup_2, boss_setup, \
    boss_mc_setup
from units_dir.units import main_db
from units_dir.units_factory import Unit


class CampaignWindow(QMainWindow):
    """
    Класс - окно выбора Кампании.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла campaign_form.py
    """

    def __init__(self, instance: any):
        super().__init__()
        # основные переменные
        self.name = 'CampaignWindow'
        self.main = instance
        self.difficulty = instance.difficulty
        self.faction = main_db.current_faction
        self.dungeon = ''
        self.curr_mission = 0
        self.prev_mission = 0
        self.campaign_buttons_dict = {}
        self.campaign_icons_dict = {}
        self.all_missions = {}
        self.level = main_db.campaign_level

        self.InitUI()

    def InitUI(self):
        # Загружаем конфигурацию окна из дизайнера
        self.ui = Ui_CampaignWindow()
        self.ui.setupUi(self)
        self.hbox = QHBoxLayout(self)

        self.ui.pushButtonFight.clicked.connect(
            self.show_fight_window)
        self.ui.ExitButton.clicked.connect(self.back)

        self.ui.pushButtonSlot_1.clicked.connect(
            self.highlight_selected_1)
        self.ui.pushButtonSlot_2.clicked.connect(
            self.highlight_selected_2)
        self.ui.pushButtonSlot_3.clicked.connect(
            self.highlight_selected_3)
        self.ui.pushButtonSlot_4.clicked.connect(
            self.highlight_selected_4)
        self.ui.pushButtonSlot_5.clicked.connect(
            self.highlight_selected_5)
        self.ui.pushButtonSlot_6.clicked.connect(
            self.highlight_selected_6)
        self.ui.pushButtonSlot_7.clicked.connect(
            self.highlight_selected_7)
        self.ui.pushButtonSlot_8.clicked.connect(
            self.highlight_selected_8)
        self.ui.pushButtonSlot_9.clicked.connect(
            self.highlight_selected_9)
        self.ui.pushButtonSlot_10.clicked.connect(
            self.highlight_selected_10)
        self.ui.pushButtonSlot_11.clicked.connect(
            self.highlight_selected_11)
        self.ui.pushButtonSlot_12.clicked.connect(
            self.highlight_selected_12)
        self.ui.pushButtonSlot_13.clicked.connect(
            self.highlight_selected_13)
        self.ui.pushButtonSlot_14.clicked.connect(
            self.highlight_selected_14)
        self.ui.pushButtonSlot_15.clicked.connect(
            self.highlight_selected_15)

        self.set_campaign_image()
        self.append_campaign_buttons()
        self.append_campaign_icons()
        self.append_campaign_arrows()

        # если в базе нет готовых миссий
        if not main_db.show_dungeon_units(
                f'{self.faction}_{self.level}_1'):
            # генерируем их
            self.update_all_missions(self.level, self.difficulty)
        else:
            # иначе берем из базы готовые
            for mission_num in range(1, 16):
                dung_name = f'{self.faction}_{self.level}_' \
                            f'{mission_num}'
                units = main_db.show_dungeon_units(dung_name)
                self.all_missions[dung_name] = {
                    1: units[0],
                    2: units[1],
                    3: units[2],
                    4: units[3],
                    5: units[4],
                    6: units[5]
                }

        # обновляем иконки миссий кампании
        self.mission_list_update()

        self.show_available_missions()

        self.show()

    def reset(self) -> None:
        """Обновить"""
        pass

    def set_campaign_image(self) -> None:
        """Установить картинку кампании"""
        self.ui.campaignBG.setPixmap(QPixmap(BACKGROUND))
        self.ui.campaignBG.setGeometry(QtCore.QRect(0, 0, 1500, 827))

    def update_all_missions(self, level, diff) -> None:
        """Обновляет состав армии для каждой миссии"""
        squad_dict = {
            1: (setup_4, setup_4, setup_5),
            2: (setup_4, setup_5, setup_5),
            3: (setup_4, setup_5, setup_6),
        }
        squad_mc_dict = {
            1: (setup_4, setup_5, setup_6),
            2: (setup_5, setup_6, setup_6),
            3: (setup_5, setup_6, setup_6),
        }

        # миссии с 1 по 15 (сгенерированные рандомно)
        name = f'{self.faction}_{level}'

        if self.faction == MC:
            self.all_missions = {
                f'{name}_1': unit_selector(level, setup_3),
                f'{name}_2': unit_selector(level, setup_3),
                f'{name}_3': unit_selector(level, setup_4),
                f'{name}_4': unit_selector(level, setup_4),
                f'{name}_5': unit_selector(level, setup_4),
                f'{name}_6': unit_selector(level, squad_mc_dict[diff][0]),
                f'{name}_7': unit_selector(level, squad_mc_dict[diff][0]),
                f'{name}_8': unit_selector(level, squad_mc_dict[diff][0]),
                f'{name}_9': unit_selector(level, squad_mc_dict[diff][0]),
                f'{name}_10': unit_selector(level, squad_mc_dict[diff][1]),
                f'{name}_11': unit_selector(level, squad_mc_dict[diff][1]),
                f'{name}_12': unit_selector(level, squad_mc_dict[diff][1]),
                f'{name}_13': unit_selector(level, squad_mc_dict[diff][2]),
                f'{name}_14': unit_selector(level, squad_mc_dict[diff][2]),
                f'{name}_15': unit_selector(level, boss_mc_setup)
            }
        else:
            self.all_missions = {
                f'{name}_1': unit_selector(level, setup_2),
                f'{name}_2': unit_selector(level, setup_2),
                f'{name}_3': unit_selector(level, setup_3),
                f'{name}_4': unit_selector(level, setup_3),
                f'{name}_5': unit_selector(level, setup_3),
                f'{name}_6': unit_selector(level, squad_dict[diff][0]),
                f'{name}_7': unit_selector(level, squad_dict[diff][0]),
                f'{name}_8': unit_selector(level, squad_dict[diff][0]),
                f'{name}_9': unit_selector(level, squad_dict[diff][0]),
                f'{name}_10': unit_selector(level, squad_dict[diff][1]),
                f'{name}_11': unit_selector(level, squad_dict[diff][1]),
                f'{name}_12': unit_selector(level, squad_dict[diff][1]),
                f'{name}_13': unit_selector(level, squad_dict[diff][2]),
                f'{name}_14': unit_selector(level, squad_dict[diff][2]),
                f'{name}_15': unit_selector(level, boss_setup)
            }

        main_db.add_dungeons(self.all_missions, self.level)

    def show_fight_window(self) -> None:
        """Метод создающий окно Битвы."""
        self.back()

        global FIGHT_WINDOW
        FIGHT_WINDOW = FightWindow(self.dungeon, self)
        FIGHT_WINDOW.show()

    @staticmethod
    def mission_slot_detailed(dungeon_units: dict) -> None:
        """Метод создающий окно просмотра армии."""
        global DETAIL_WINDOW
        DETAIL_WINDOW = EnemyArmyDialog(
            dungeon_units)
        DETAIL_WINDOW.show()

    @staticmethod
    def dungeon_unit_by_slot(slot: int) -> Unit:
        """Метод получающий юнита подземелья по слоту."""
        return main_db.get_unit_by_slot(
            slot,
            main_db.CurrentDungeon)

    def append_campaign_buttons(self) -> None:
        """Кнопки миссий в кампании"""
        self.campaign_buttons_dict = {
            1: self.ui.pushButtonSlot_1,
            2: self.ui.pushButtonSlot_2,
            3: self.ui.pushButtonSlot_3,
            4: self.ui.pushButtonSlot_4,
            5: self.ui.pushButtonSlot_5,
            6: self.ui.pushButtonSlot_6,
            7: self.ui.pushButtonSlot_7,
            8: self.ui.pushButtonSlot_8,
            9: self.ui.pushButtonSlot_9,
            10: self.ui.pushButtonSlot_10,
            11: self.ui.pushButtonSlot_11,
            12: self.ui.pushButtonSlot_12,
            13: self.ui.pushButtonSlot_13,
            14: self.ui.pushButtonSlot_14,
            15: self.ui.pushButtonSlot_15,
        }

    def append_campaign_icons(self) -> None:
        """Иконки миссий в кампании"""
        self.campaign_icons_dict = {
            1: self.ui.slot1,
            2: self.ui.slot2,
            3: self.ui.slot3,
            4: self.ui.slot4,
            5: self.ui.slot5,
            6: self.ui.slot6,
            7: self.ui.slot7,
            8: self.ui.slot8,
            9: self.ui.slot9,
            10: self.ui.slot10,
            11: self.ui.slot11,
            12: self.ui.slot12,
            13: self.ui.slot13,
            14: self.ui.slot14,
            15: self.ui.slot15,
        }

    def append_campaign_arrows(self) -> None:
        """Иконки доступности миссий в кампании"""
        self.campaign_arrows_dict = {
            1: self.ui.line_1,
            2: self.ui.line_2,
            3: self.ui.line_3,
            4: self.ui.line_4,
            5: self.ui.line_5,
            6: self.ui.line_6,
            7: self.ui.line_7,
            8: self.ui.line_8,
            9: self.ui.line_9,
            10: self.ui.line_10,
            11: self.ui.line_11,
            12: self.ui.line_12,
            13: self.ui.line_13,
            14: self.ui.line_14,
            15: self.ui.line_15,
        }

    def mission_list_update(self) -> None:
        """Обновление иконок миссий кампании"""
        for number, mission in self.all_missions.items():
            num = int(number.split('_')[-1])
            units = [main_db.get_unit_by_name(unit)
                     for unit in mission.values() if unit is not None]

            # определяем сильнейшее существо в отряде по опыту
            units.sort(key=lambda x: x['exp_per_kill'], reverse=True)
            strongest_unit = units[0]

            slot_update(
                strongest_unit,
                self.campaign_icons_dict[num])

            button_update(
                strongest_unit,
                self.campaign_buttons_dict[num])

    @staticmethod
    def show_red_frame(gif_slot: QtWidgets.QPushButton) -> None:
        """Обновление красной рамки в слоте"""
        gif_slot.setStyleSheet("border: 4px solid darkred;")

    @staticmethod
    def show_green_frame(gif_slot: QtWidgets.QPushButton) -> None:
        """Обновление зеленой рамки в слоте"""
        gif_slot.setStyleSheet("border: 4px solid darkgreen;")

    @staticmethod
    def show_no_frames(slots_dict: Dict[int, QtWidgets.QPushButton],
                       func: Callable) -> None:
        """Убирает все рамки"""
        for slot in range(1, 16):
            func(slots_dict[slot])

    @staticmethod
    def show_no_frame(gif_slot: QtWidgets.QPushButton) -> None:
        """Убрать рамки в слоте"""
        gif_slot.setStyleSheet("border: 0px;")

    def unlight_all(self) -> None:
        """Снять выделение миссии"""
        self.show_no_frames(self.campaign_buttons_dict, self.show_no_frame)

    def highlight_selected(self, number) -> None:
        """Подсветка выбранной миссии"""
        self.unlight_all()
        self.show_active_point()

        for num, button in self.campaign_buttons_dict.items():
            if num == number:
                mission_name = f'{self.faction}_{self.level}_{num}'
                self.dungeon = mission_name

                self.show_red_frame(button)
                self.mission_slot_detailed(
                    self.all_missions[mission_name])

        # self.dungeon = f'{self.faction}_{self.level}_{number}'
        ui_unlock(self.ui.pushButtonFight)

    def highlight_selected_1(self) -> None:
        """Подсветка миссии 1"""
        self.highlight_selected(1)

    def highlight_selected_2(self) -> None:
        """Подсветка миссии 2"""
        self.highlight_selected(2)

    def highlight_selected_3(self) -> None:
        """Подсветка миссии 3"""
        self.highlight_selected(3)

    def highlight_selected_4(self) -> None:
        """Подсветка миссии 4"""
        self.highlight_selected(4)

    def highlight_selected_5(self) -> None:
        """Подсветка миссии 5"""
        self.highlight_selected(5)

    def highlight_selected_6(self) -> None:
        """Подсветка миссии 6"""
        self.highlight_selected(6)

    def highlight_selected_7(self) -> None:
        """Подсветка миссии 7"""
        self.highlight_selected(7)

    def highlight_selected_8(self) -> None:
        """Подсветка миссии 8"""
        self.highlight_selected(8)

    def highlight_selected_9(self) -> None:
        """Подсветка миссии 9"""
        self.highlight_selected(9)

    def highlight_selected_10(self) -> None:
        """Подсветка миссии 10"""
        self.highlight_selected(10)

    def highlight_selected_11(self) -> None:
        """Подсветка миссии 11"""
        self.highlight_selected(11)

    def highlight_selected_12(self) -> None:
        """Подсветка миссии 12"""
        self.highlight_selected(12)

    def highlight_selected_13(self) -> None:
        """Подсветка миссии 13"""
        self.highlight_selected(13)

    def highlight_selected_14(self) -> None:
        """Подсветка миссии 14"""
        self.highlight_selected(14)

    def highlight_selected_15(self) -> None:
        """Подсветка миссии 15"""
        self.highlight_selected(15)

    def show_available_missions(self):
        """
        Определение активности миссий согласно текущему
        положению на карте приключений. Используется граф.
        """
        session = main_db.session_by_faction(
            main_db.current_player.id,
            self.faction)
        self.curr_mission = session.campaign_mission
        self.prev_mission = session.prev_mission

        self.show_active_point()

        graph = [
            {1, 2},  # 0
            {2, 3, 4},  # 1
            {1, 4, 5},  # 2
            {4, 6, 7},  # 3
            {3, 5, 7, 8},  # 4
            {4, 8, 9},  # 5
            {7, 10},  # 6
            {6, 8, 10, 11},  # 7
            {7, 9, 11, 12},  # 8
            {8, 12},  # 9
            {11, 13},  # 10
            {10, 12, 13, 14},  # 11
            {11, 14},  # 12
            {14, 15},  # 13
            {13, 15},  # 14
            {},  # 15
        ]
        if self.prev_mission != 0 \
                and self.prev_mission in graph[self.curr_mission]:
            graph[self.curr_mission].remove(self.prev_mission)

        for key, val in self.campaign_buttons_dict.items():
            if key in graph[self.curr_mission]:
                ui_unlock(val)
                show_opened(self.campaign_arrows_dict[key])
            else:
                ui_lock(val)
                show_closed(self.campaign_arrows_dict[key])

        if self.dungeon == '':
            ui_lock(self.ui.pushButtonFight)

    def show_active_point(self):
        """Отображение текущего местоположения на карте приключений"""
        if self.curr_mission > 0:
            button = self.campaign_buttons_dict[self.curr_mission]
            icon = self.campaign_icons_dict[self.curr_mission]

            # определяем лидера отряда
            player_units = main_db.show_player_units()
            leader = player_units[0]

            for unit in player_units:
                if unit.leadership >= 3:
                    leader = unit

            # обновляем иконку
            slot_update(leader, icon)

            # обновляем размер рамки вокруг кнопки
            button_update(leader, button)

            # отображаем рамку
            self.show_green_frame(button)

    def back(self) -> None:
        """Кнопка возврата"""
        self.close()
