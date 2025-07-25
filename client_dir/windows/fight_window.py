"""Окно битвы"""

import os.path
import random
from typing import Callable, Optional
from threading import Thread as Thr

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt, QEvent
from PyQt5.QtGui import QPixmap, QMovie, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from battle import Battle, Player
from battle_logging import logging
from client_dir.forms.fight_form import Ui_FightWindow
from client_dir.windows.message_window import MessageWindow
from client_dir.settings import UNIT_STAND, UNIT_ATTACK, \
    UNIT_ATTACKED, UNIT_EFFECTS_ATTACK, BATTLE_GROUND, FRONT, REAR, \
    COMMON, BATTLE_GROUNDS, UNIT_SHADOW_ATTACK, UNIT_SHADOW_STAND, \
    UNIT_SHADOW_ATTACKED, UNIT_EFFECTS_AREA, UNIT_EFFECTS_TARGET, \
    RIGHT_ICONS, LEFT_ICONS, SCREEN_RECT, PANEL_RECT, BATTLE_LOG, \
    BATTLE_ANIM, HEAL_LIST, ALCHEMIST_LIST, POLYMORPH, PLAYER, ENEMY
from client_dir.ui_functions import show_no_frame, \
    show_damage, clear_dot, show_green_frame, \
    show_red_frame, show_blue_frame, update_unit_health, \
    get_unit_image, show_no_circle, ui_lock, ui_unlock, \
    show_dot_icon, show_polymorph
from client_dir.dialogs.unit_dialog import UnitDialog
from units_dir.models import Player2Units
from units_dir.ranking import GOLD_GRADATION
from units_dir.battle_unit import Unit
from units_dir.visual_model import v_model


class Thread(QThread):
    """Класс потока"""
    dataThread = pyqtSignal(str)

    def __init__(self, attacker):
        QThread.__init__(self)
        self.attacker = attacker

    def run(self) -> None:
        """Запуск"""
        if self.attacker is True:
            i = 10_000_000
        else:
            i = 20_000_000

        while i > 1:
            i -= 1
            if i == 5_000:
                self.dataThread.emit("Finished")


class FightWindow(QMainWindow):
    """
    Класс - окно битвы.
    Содержит всю основную логику отображения боевой анимации.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла fight_form.py
    """

    def __init__(self,
                 dungeon: str,
                 db_table: any,
                 parent_window: any):
        super().__init__()
        # основные переменные
        self.parent_window = parent_window
        self.db_table = db_table
        self.new_battle = Battle(dungeon, self.db_table)
        self.dungeon = dungeon
        self.computer_name = 'Computer'
        self.player_side = FRONT
        self.enemy_side = REAR

        # словари иконок
        self.unit_icons_dict = {}
        self.unit_damaged_dict = {}

        self.dung_icons_dict = {}
        self.dung_damaged_dict = {}

        # словари для кругов под юнитами
        self.unit_circles_dict = {}
        self.dung_circles_dict = {}

        # словари юнитов на поле боя
        self.unit_field_dict = {}
        self.dung_field_dict = {}

        # словари лейблов для анимаций и hp юнитов игрока1
        self.pl_slots_dict = {}
        self.pl_slots_shad_dict = {}
        self.pl_slots_eff_dict = {}
        self.pl_slots_attacked_eff_dict = {}
        self.pl_hp_slots_dict = {}

        # словари лейблов для анимаций и hp юнитов игрока2
        self.en_slots_dict = {}
        self.en_slots_shad_dict = {}
        self.en_slots_eff_dict = {}
        self.en_slots_attacked_eff_dict = {}
        self.en_hp_slots_dict = {}

        self.mouse_press = None

        self.InitUI()

        with open(BATTLE_LOG, 'w', encoding='utf-8') as log:
            log.write(f'Ходит: {self.curr_unit.name}\n')
            log.write("Новая битва\n")
        self.update_log()

        timer = QTimer(self)
        timer.singleShot(1000, self.check_ai)
        del timer

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""

        self.ui = Ui_FightWindow()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)
        self.update_bg()
        # self.update_bp()

        self.right_slots = [
            self.ui.slot2,
            self.ui.slot4,
            self.ui.slot6,
            self.ui.damPlayerSlot_2,
            self.ui.damPlayerSlot_4,
            self.ui.damPlayerSlot_6,
        ]

        self.ui.leftIcons.setPixmap(
            QPixmap(LEFT_ICONS))
        self.ui.rightIcons.setPixmap(
            QPixmap(RIGHT_ICONS))

        self.ui.pushButtonBack.clicked.connect(self.back)

        self.ui.pushButtonDefence.clicked.connect(self.unit_defence)
        self.ui.pushButtonWaiting.clicked.connect(self.unit_waiting)

        self.ui.damPlayerSlot_1.installEventFilter(self)
        self.ui.damPlayerSlot_2.installEventFilter(self)
        self.ui.damPlayerSlot_3.installEventFilter(self)
        self.ui.damPlayerSlot_4.installEventFilter(self)
        self.ui.damPlayerSlot_5.installEventFilter(self)
        self.ui.damPlayerSlot_6.installEventFilter(self)

        self.ui.damEnemySlot_1.installEventFilter(self)
        self.ui.damEnemySlot_2.installEventFilter(self)
        self.ui.damEnemySlot_3.installEventFilter(self)
        self.ui.damEnemySlot_4.installEventFilter(self)
        self.ui.damEnemySlot_5.installEventFilter(self)
        self.ui.damEnemySlot_6.installEventFilter(self)

        self.ui.Unit_1.installEventFilter(self)
        self.ui.Unit_2.installEventFilter(self)
        self.ui.Unit_3.installEventFilter(self)
        self.ui.Unit_4.installEventFilter(self)
        self.ui.Unit_5.installEventFilter(self)
        self.ui.Unit_6.installEventFilter(self)

        self.ui.EnemyUnit_1.installEventFilter(self)
        self.ui.EnemyUnit_2.installEventFilter(self)
        self.ui.EnemyUnit_3.installEventFilter(self)
        self.ui.EnemyUnit_4.installEventFilter(self)
        self.ui.EnemyUnit_5.installEventFilter(self)
        self.ui.EnemyUnit_6.installEventFilter(self)

        self.ui.pushButtonAutoFight.clicked.connect(
            self.autofight)
        self.ui.pushButtonClear.clicked.connect(
            self.new_battle.regen)
        self.ui.pushButtonChange.clicked.connect(
            self.change_side)
        self.ui.ChangeSideSlot.setPixmap(
            QPixmap(
                os.path.join(
                    COMMON,
                    'reverse.png')))
        self.ui.EscapeSlot.setPixmap(
            QPixmap(
                os.path.join(
                    COMMON,
                    'back.png')))

        self.set_front_gif_player1()
        self.set_unit_icons()

        self.ui.battleLog.setStyleSheet("background-color: rgb(65, 3, 2)")

        self.update_speed_checkbox()
        self.show_target_frame()
        self.show_frame_attacker()
        self.update_log()

        self.ui.Unit_1.raise_()
        self.ui.Unit_2.raise_()
        self.ui.Unit_3.raise_()
        self.ui.Unit_4.raise_()
        self.ui.Unit_5.raise_()
        self.ui.Unit_6.raise_()

        self.ui.EnemyUnit_2.raise_()
        self.ui.EnemyUnit_1.raise_()
        self.ui.EnemyUnit_4.raise_()
        self.ui.EnemyUnit_3.raise_()
        self.ui.EnemyUnit_6.raise_()
        self.ui.EnemyUnit_5.raise_()

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.show()
        self.unit_gifs_update()

    def eventFilter(self, source, event):
        """Обработчик событий"""
        self.show_circle_by_unit(self.unit_damaged_dict,
                                 PLAYER,
                                 source,
                                 event)
        self.show_circle_by_unit(self.unit_field_dict,
                                 PLAYER,
                                 source,
                                 event)
        self.show_circle_by_unit(self.dung_damaged_dict,
                                 ENEMY,
                                 source,
                                 event)
        self.show_circle_by_unit(self.dung_field_dict,
                                 ENEMY,
                                 source,
                                 event)

        return super().eventFilter(source, event)

    def show_circle_by_unit(self,
                            icons_dict: dict,
                            player: str,
                            source: any,
                            event: any):
        """Определение события при наведении/нажатии мыши на юнит"""
        ui_dict = self.unit_circles_dict

        if player == PLAYER:
            ui_dict = self.unit_circles_dict
            side = self.player_side
        elif player == ENEMY:
            ui_dict = self.dung_circles_dict
            side = self.enemy_side

        for num, item in icons_dict.items():
            unit = self._unit_by_slot_and_side(num, side)

            if source == item \
                    and unit is not None \
                    and unit.curr_health != 0:

                if event.type() == QEvent.Enter:
                    self.enter_thread = Thr(target=self.event_enter(
                        unit, side, ui_dict, num),
                        name="Enter Thread")
                    self.enter_thread.start()

                    # self.event_enter(unit, side, ui_dict, num)

                elif event.type() == QEvent.Leave:
                    self.leave_thread = Thr(target=self.event_leave(ui_dict),
                                            name="Leave Thread")
                    self.leave_thread.start()

                    # self.event_leave(ui_dict)

                elif event.type() == QEvent.MouseButtonPress:
                    if event.button() == Qt.LeftButton:
                        self.event_left_button(num, side)

            if source == item and unit is not None:
                if event.type() == QEvent.MouseButtonPress:
                    self.event_right_button(event, unit)

    def event_right_button(self, event, unit):
        """Правый клик мышью"""
        if event.button() == Qt.RightButton:
            self._slot_detailed(unit, UnitDialog)

    def event_left_button(self, num, side):
        """Левый клик мышью"""
        if num in self.new_battle.target_slots:
            self.attack_enemy_by_slot(num, side)

    def event_leave(self, ui_dict):
        """Отведение курсора мыши"""
        for key in ui_dict.keys():
            show_no_circle(ui_dict.get(key))
        # битва еще не закончена
        if not self.new_battle.battle_is_over:
            self.show_circle_attacker()

    def event_enter(self,
                    unit: Unit,
                    side: str,
                    ui_dict: dict,
                    num: int):
        """
        Проверка юнита на свой/чужой при наведении курсора.
        Установка gif'ки круга определенног цвета под юнитом
        """
        if unit not in self.new_battle.current_player.units:
            if self.curr_unit.attack_purpose == 6:
                for key in ui_dict.keys():
                    unit = self._unit_by_slot_and_side(key, side)
                    if unit is not None \
                            and unit.curr_health != 0 \
                            and unit.slot in self.new_battle.targets:
                        self.show_circle_r(unit, ui_dict.get(key))
            else:
                self.show_circle_r(unit, ui_dict.get(num))

        if unit in self.new_battle.current_player.units:
            self.show_circle_y(unit, ui_dict.get(num))

    def keyPressEvent(self, event):
        """Метод обработки нажатия клавиш A, D, W"""
        if self.new_battle.current_player.name != 'Computer':
            if event.key() == Qt.Key_A:
                self.autofight()
            if event.key() == Qt.Key_D:
                self.unit_defence()
            if event.key() == Qt.Key_W:
                self.unit_waiting()
            # if event.key() == Qt.Key_C:
            #    self.new_battle.regen()

    def update_bg(self) -> None:
        """Обновление бэкграунда, заполнение картинкой поля сражения"""
        fight_bg = self.ui.FightBG
        fight_bg.setPixmap(
            QPixmap(
                os.path.join(
                    BATTLE_GROUND,
                    random.choice(BATTLE_GROUNDS))))
        fight_bg.setGeometry(SCREEN_RECT)
        self.hbox.addWidget(fight_bg)
        self.setLayout(self.hbox)

    def update_bp(self) -> None:
        """Обновление панели битвы"""
        fight_bp = self.ui.batPanel
        fight_bp.setPixmap(
            QPixmap(
                os.path.join(
                    COMMON, 'battle_panel.png')))
        fight_bp.setGeometry(PANEL_RECT)
        self.hbox.addWidget(fight_bp)
        self.setLayout(self.hbox)

    def update_speed_checkbox(self) -> None:
        """
        Метод заполнения выпадающего списка доступных скоростей
        анимации.
        """
        self.ui.speedText.setStyleSheet('color: white')

        speed_slots = [1, 2, 3, 4, 5,
                       6, 7, 8, 9, 10]
        self.speed_model = QStandardItemModel()
        for slot in speed_slots:
            item = QStandardItem(str(slot))
            item.setEditable(False)
            self.speed_model.appendRow(item)
        self.ui.comboSpeed.setModel(self.speed_model)

        self.ui.comboSpeed.setCurrentIndex(4)
        self.check_speed()
        self.ui.comboSpeed.currentIndexChanged.connect(self.check_speed)

    def check_speed(self) -> None:
        """Устанавливает выбранную скорость анимации"""
        multiplier = self.ui.comboSpeed.currentText()
        self.speed = 100 * float(multiplier)
        self.unit_gifs_update()

    def update_log(self) -> None:
        """Обновление лога"""
        self.log_model = QStandardItemModel()

        with open(BATTLE_LOG, 'r', encoding='utf-8') as log:
            text_lines = log.readlines()
            for line in text_lines:
                item = QStandardItem(line.strip('\n'))
                item.setEditable(False)
                self.log_model.appendRow(item)
            self.ui.battleLog.setModel(self.log_model)
        self.ui.battleLog.setStyleSheet(
            "background-color: rgb(65, 3, 2); color: white")

    def back(self) -> None:
        """Кнопка возврата"""
        self.parent_window.reset()
        if self.parent_window.name == 'CampaignWindow':
            self.parent_window.main.reset()
        self.close()

    def change_side(self) -> None:
        """Смена сторон"""
        self.change_icons()
        self.change_gifs()

        self.player_side, self.enemy_side = self.enemy_side, self.player_side

        self.unit_gifs_update()
        # self.gifs_thread.start()
        self.clear_effects()
        self.clear_frames_circles()
        self.define_dotted_units()

        self.check_ai()

        if not self.new_battle.battle_is_over:
            self.show_target_frame()
            self.show_frame_attacker()
            self.show_circle_attacker()

    def change_gifs(self) -> None:
        """Меняет местами FRONT/REAR анимационные GIF юнитов игроков"""
        self.pl_slots_dict, self.en_slots_dict = \
            self.en_slots_dict, self.pl_slots_dict
        self.pl_slots_shad_dict, self.en_slots_shad_dict = \
            self.en_slots_shad_dict, self.pl_slots_shad_dict
        self.pl_slots_eff_dict, self.en_slots_eff_dict = \
            self.en_slots_eff_dict, self.pl_slots_eff_dict
        self.pl_slots_attacked_eff_dict, self.en_slots_attacked_eff_dict = \
            self.en_slots_attacked_eff_dict, self.pl_slots_attacked_eff_dict
        self.pl_hp_slots_dict, self.en_hp_slots_dict = \
            self.en_hp_slots_dict, self.pl_hp_slots_dict

    def append_front(self) -> None:
        """Основные анимационные GIF юнитов FRONT стороны"""
        self.pl_slots_dict = {
            1: self.ui.gifPlayerSlot_1,
            2: self.ui.gifPlayerSlot_2,
            3: self.ui.gifPlayerSlot_3,
            4: self.ui.gifPlayerSlot_4,
            5: self.ui.gifPlayerSlot_5,
            6: self.ui.gifPlayerSlot_6,
        }

    def append_front_shadows(self) -> None:
        """Анимационные GIF теней юнитов FRONT стороны"""
        self.pl_slots_shad_dict = {
            1: self.ui.gifShadSlot_1,
            2: self.ui.gifShadSlot_2,
            3: self.ui.gifShadSlot_3,
            4: self.ui.gifShadSlot_4,
            5: self.ui.gifShadSlot_5,
            6: self.ui.gifShadSlot_6,
        }

    def append_front_effects(self) -> None:
        """Анимационные GIF эффектов атакующий юнитов FRONT стороны"""
        self.pl_slots_eff_dict = {
            1: self.ui.gifEffSlot_1,
            2: self.ui.gifEffSlot_2,
            3: self.ui.gifEffSlot_3,
            4: self.ui.gifEffSlot_4,
            5: self.ui.gifEffSlot_5,
            6: self.ui.gifEffSlot_6,
        }

    def append_front_attacked_eff(self) -> None:
        """Анимационные GIF эффектов атакованных юнитов FRONT стороны"""
        self.pl_slots_attacked_eff_dict = {
            1: self.ui.gifPlayerAttEffSlot_1,
            2: self.ui.gifPlayerAttEffSlot_2,
            3: self.ui.gifPlayerAttEffSlot_3,
            4: self.ui.gifPlayerAttEffSlot_4,
            5: self.ui.gifPlayerAttEffSlot_5,
            6: self.ui.gifPlayerAttEffSlot_6,
        }

    def append_front_hp(self) -> None:
        """GIF очков здоровья юнитов FRONT стороны"""
        self.pl_hp_slots_dict = {
            1: self.ui.hpSlot1,
            2: self.ui.hpSlot2,
            3: self.ui.hpSlot3,
            4: self.ui.hpSlot4,
            5: self.ui.hpSlot5,
            6: self.ui.hpSlot6,
        }

    def append_rear(self) -> None:
        """Анимационные GIF теней юнитов REAR стороны"""
        self.en_slots_dict = {
            1: self.ui.gifEnemySlot_1,
            2: self.ui.gifEnemySlot_2,
            3: self.ui.gifEnemySlot_3,
            4: self.ui.gifEnemySlot_4,
            5: self.ui.gifEnemySlot_5,
            6: self.ui.gifEnemySlot_6,
        }

    def append_rear_shadows(self) -> None:
        """Анимационные GIF теней юнитов REAR стороны"""
        self.en_slots_shad_dict = {
            1: self.ui.gifEnemyShadSlot_1,
            2: self.ui.gifEnemyShadSlot_2,
            3: self.ui.gifEnemyShadSlot_3,
            4: self.ui.gifEnemyShadSlot_4,
            5: self.ui.gifEnemyShadSlot_5,
            6: self.ui.gifEnemyShadSlot_6,
        }

    def append_rear_effects(self) -> None:
        """Анимационные GIF эффектов атакующий юнитов REAR стороны"""
        self.en_slots_eff_dict = {
            1: self.ui.gifEnemyEffSlot_1,
            2: self.ui.gifEnemyEffSlot_2,
            3: self.ui.gifEnemyEffSlot_3,
            4: self.ui.gifEnemyEffSlot_4,
            5: self.ui.gifEnemyEffSlot_5,
            6: self.ui.gifEnemyEffSlot_6,
        }

    def append_rear_attacked_eff(self) -> None:
        """Анимационные GIF эффектов атакованных юнитов REAR стороны"""
        self.en_slots_attacked_eff_dict = {
            1: self.ui.gifEnemyAttEffSlot_1,
            2: self.ui.gifEnemyAttEffSlot_2,
            3: self.ui.gifEnemyAttEffSlot_3,
            4: self.ui.gifEnemyAttEffSlot_4,
            5: self.ui.gifEnemyAttEffSlot_5,
            6: self.ui.gifEnemyAttEffSlot_6,
        }

    def append_rear_hp(self) -> None:
        """GIF очков здоровья юнитов REAR стороны"""
        self.en_hp_slots_dict = {
            1: self.ui.enemyHPSlot1,
            2: self.ui.enemyHPSlot2,
            3: self.ui.enemyHPSlot3,
            4: self.ui.enemyHPSlot4,
            5: self.ui.enemyHPSlot5,
            6: self.ui.enemyHPSlot6,
        }

    def set_front_gif_player1(self) -> None:
        """
        Задание FRONT стороны для анимационных GIF игрока 1 (по умолчанию)
        """
        self.player_side = FRONT
        self.enemy_side = REAR

        # Основные анимационные GIF юнитов FRONT стороны
        self.append_front()

        # Анимационные GIF теней юнитов FRONT стороны
        self.append_front_shadows()

        # Анимационные GIF эффектов атакующий юнитов FRONT стороны
        self.append_front_effects()

        # Анимационные GIF эффектов атакованных юнитов FRONT стороны
        self.append_front_attacked_eff()

        # GIF очков здоровья юнитов FRONT стороны
        self.append_front_hp()

        # Основные анимационные GIF юнитов REAR стороны
        self.append_rear()

        # Анимационные GIF теней юнитов REAR стороны
        self.append_rear_shadows()

        # Анимационные GIF эффектов атакующий юнитов REAR стороны
        self.append_rear_effects()

        # Анимационные GIF эффектов атакованных юнитов REAR стороны
        self.append_rear_attacked_eff()

        # GIF очков здоровья юнитов REAR стороны
        self.append_rear_hp()

    def append_front_icons(self) -> None:
        """Иконки юнитов FRONT стороны"""
        self.unit_icons_dict = {
            1: self.ui.slot1,
            2: self.ui.slot2,
            3: self.ui.slot3,
            4: self.ui.slot4,
            5: self.ui.slot5,
            6: self.ui.slot6,
        }

    def append_front_field(self) -> None:
        """Полевые юниты FRONT стороны"""
        self.unit_field_dict = {
            1: self.ui.Unit_1,
            2: self.ui.Unit_2,
            3: self.ui.Unit_3,
            4: self.ui.Unit_4,
            5: self.ui.Unit_5,
            6: self.ui.Unit_6,
        }

    def append_front_damaged(self) -> None:
        """Иконки атакованных юнитов FRONT стороны"""
        self.unit_damaged_dict = {
            1: self.ui.damPlayerSlot_1,
            2: self.ui.damPlayerSlot_2,
            3: self.ui.damPlayerSlot_3,
            4: self.ui.damPlayerSlot_4,
            5: self.ui.damPlayerSlot_5,
            6: self.ui.damPlayerSlot_6,
        }

    def append_front_circles(self) -> None:
        """Круги юнитов FRONT стороны"""
        self.unit_circles_dict = {
            1: self.ui.gifCircleSlot_1,
            2: self.ui.gifCircleSlot_2,
            3: self.ui.gifCircleSlot_3,
            4: self.ui.gifCircleSlot_4,
            5: self.ui.gifCircleSlot_5,
            6: self.ui.gifCircleSlot_6,
        }

    def append_rear_icons(self) -> None:
        """GIF иконок юнитов REAR стороны"""
        self.dung_icons_dict = {
            1: self.ui.enemySlot1,
            2: self.ui.enemySlot2,
            3: self.ui.enemySlot3,
            4: self.ui.enemySlot4,
            5: self.ui.enemySlot5,
            6: self.ui.enemySlot6,
        }

    def append_rear_field(self) -> None:
        """Полевые юниты REAR стороны"""
        self.dung_field_dict = {
            1: self.ui.EnemyUnit_1,
            2: self.ui.EnemyUnit_2,
            3: self.ui.EnemyUnit_3,
            4: self.ui.EnemyUnit_4,
            5: self.ui.EnemyUnit_5,
            6: self.ui.EnemyUnit_6,
        }

    def append_rear_damaged(self) -> None:
        """Иконки атакованных юнитов REAR стороны"""
        self.dung_damaged_dict = {
            1: self.ui.damEnemySlot_1,
            2: self.ui.damEnemySlot_2,
            3: self.ui.damEnemySlot_3,
            4: self.ui.damEnemySlot_4,
            5: self.ui.damEnemySlot_5,
            6: self.ui.damEnemySlot_6,
        }

    def append_rear_circles(self) -> None:
        """Круги юнитов REAR стороны"""
        self.dung_circles_dict = {
            1: self.ui.gifEnemyCircleSlot_1,
            2: self.ui.gifEnemyCircleSlot_2,
            3: self.ui.gifEnemyCircleSlot_3,
            4: self.ui.gifEnemyCircleSlot_4,
            5: self.ui.gifEnemyCircleSlot_5,
            6: self.ui.gifEnemyCircleSlot_6,
        }

    def show_splash_area(self, unit: any, action: str) -> None:
        """Атака по площади"""
        if unit in self.player1.units:
            side = self.player_side
        else:
            side = self.enemy_side

        if side == FRONT:
            gif_slot = self.ui.gifPlayerAreaAttack
        else:
            gif_slot = self.ui.gifEnemyAreaAttack

        gif = self.action_gif(action, side, unit)

        gif_slot.setMovie(gif)
        gif.start()

    @staticmethod
    def action_gif(action: str, side: str, unit: Unit):
        """Анимация действия"""
        return QMovie(os.path.join(
            action,
            f"{side}{unit.name}.gif"))

    def unit_is_dead(self, unit):
        """Если атакованный/отравленный юнит погибает"""
        # прорисовка модели атакованного юнита
        self.show_attacked(unit)
        self.show_shadow_attacked(unit)

        # удаление юнита из битвы
        self.new_battle.remove_unit(unit)

        # анимация Полиморфа, если нужно
        if unit.dotted:
            self.show_polymorph_animation(unit)

        if unit in self.dotted_units:
            self.pop_dotted_unit(unit)

        self.new_battle.check_player_is_alive()

        if self.new_battle.battle_is_over:
            # возвращаем прежнюю форму
            for unit in (*self.player1.units,
                         *self.player2.units):
                self.show_polymorph_animation(unit)

            self.new_battle.alive_getting_experience()

    def pop_dotted_unit(self, unit):
        """Убирает юнит из словаря dotted_units"""
        self.new_battle.dotted_units.pop(unit)

    @property
    def player1(self):
        """Игрок 1"""
        return self.new_battle.player1

    @property
    def player2(self):
        """Игрок 2"""
        return self.new_battle.player2

    @property
    def target_player(self):
        """Целевой игрок"""
        return self.new_battle.target_player

    @property
    def curr_unit(self):
        """Текущий юнит"""
        return self.new_battle.current_unit

    @property
    def dotted_units(self):
        """Юниты под воздействием доп эффектов"""
        return self.new_battle.dotted_units

    def show_poisoned_unit(self):
        """Если ходящий юнит отравлен и т.д."""
        unit = self.curr_unit
        dot_units = self.dotted_units

        if unit in dot_units and unit.dotted:
            if self.dot_not_cause_damage(dot_units, unit):
                self.show_attacked(unit)
                self.show_shadow_attacked(unit)

            unit.minus_dot_round()
            self._update_all_unit_health()

            if unit.dotted == 0 and unit in dot_units:
                unit.off_initiative(self.get_db_table(unit))
                dot_units.pop(unit)

                # отображение анимации Полиморфа
                # ------------------------------
                # анимация Полиморфа, если нужно
                # self.show_polymorph_animation(unit)
                # self.curr_unit = self.new_battle.new_unit

            # если отравленный юнит погиб
            if unit.curr_health == 0:
                self.unit_is_dead(unit)

                # битва еще не закончена
                if not self.new_battle.battle_is_over:
                    # проверка, если отравленный юнит умер в раунде последним
                    self.new_battle.are_units_in_round()

                # битва закончена
                elif self.new_battle.battle_is_over:
                    # убирает рамки
                    self.show_no_frames(self.unit_circles_dict, show_no_circle)
                    self.show_no_frames(self.dung_circles_dict, show_no_circle)

                    # возвращаем прежнюю форму
                    for unit in (*self.player1.units,
                                 *self.player2.units):
                        self.show_polymorph_animation(unit)

                    self.show_lvl_up_animations()

        # показать иконки эффектов
        self.define_dotted_units()

    def get_db_table(self, unit: Unit):
        """Определение текущей таблицы БД для игрока"""
        if unit in self.player1.units:
            pl_database = self.db_table
        else:
            pl_database = self.new_battle.enemy_db_table
        return pl_database

    @staticmethod
    def dot_not_cause_damage(dot_units: dict, unit: Unit):
        """Проверка что доп эффект не наносит урона"""
        return not dot_units[unit].get('Снижение инициативы') \
               and not dot_units[unit].get('Снижение урона') \
               and not dot_units[unit].get('Паралич') \
               and not dot_units[unit].get('Полиморф')

    def next_unit_turn(self) -> None:
        """Ход следующего юнита"""
        self.new_battle.are_units_in_round()
        # если ходящий юнит отравлен и т.д.
        self.show_poisoned_unit()

        # битва еще не закончена
        if not self.new_battle.battle_is_over:
            # Показать рамки
            self.show_target_frame()
            self.show_frame_attacker()
            self.show_circle_attacker()

        self.check_ai()
        self.unit_icons_update()

    def check_ai(self):
        """Проверка, если ходит ИИ, включаем автобой"""
        if self.new_battle.current_player.name == 'Computer':
            # блокировка кнопок
            self.lock_buttons_for_ai()

            timer = QTimer(self)
            timer.singleShot(1500, self.autofight)
            del timer
        else:
            # Разблокировка кнопок
            self.unlock_buttons_for_player()

    def lock_buttons_for_ai(self):
        """Блокировка кнопок на ходе компьютера"""
        ui_lock(self.ui.pushButtonAutoFight)
        ui_lock(self.ui.pushButtonDefence)
        ui_lock(self.ui.pushButtonWaiting)
        ui_lock(self.ui.pushButtonChange)

    def unlock_buttons_for_player(self):
        """Разблокировка кнопок на ходе игрока"""
        ui_unlock(self.ui.pushButtonAutoFight)
        ui_unlock(self.ui.pushButtonDefence)
        ui_unlock(self.ui.pushButtonWaiting)
        ui_unlock(self.ui.pushButtonChange)

    def unit_defence(self) -> None:
        """Встать в Защиту выбранным юнитом"""
        self.curr_unit.defence()
        self.update_log()
        self.clear_effects()
        self.clear_frames_circles()
        self.next_unit_turn()

        self.update_log()

    def unit_waiting(self) -> None:
        """Ожидать выбранным юнитом"""
        self.curr_unit.waiting()

        self.update_log()
        self.clear_effects()
        self.clear_frames_circles()

        self.new_battle.waiting_units.append(self.curr_unit)

        self.next_unit_turn()

        self.update_log()

    def show_attack_and_attacked(self) -> None:
        """Анимация атакующей и атакованной стороны"""
        self.update_log()

        if self.new_battle.units_in_round or (
                not self.new_battle.units_in_round and self.curr_unit):
            self.show_no_frames(self.unit_circles_dict, show_no_circle)
            self.show_no_frames(self.dung_circles_dict, show_no_circle)

            self.who_attack()

            if 'жизни' in self.curr_unit.attack_type:
                self.worker = Thread(False)
            else:
                self.worker = Thread(True)

            self.worker.dataThread.connect(self.show_all_attacked)
            self.worker.start()

            timer = QTimer(self)
            timer.singleShot(2000, self.unit_gifs_update)
            del timer

    def autofight(self) -> None:
        """Автобой"""
        # пока битва не окончена
        if not self.new_battle.battle_is_over:

            # если некого атаковать, защита
            if not self.new_battle.targets:
                self.unit_defence()

            # иначе атака
            else:
                self.new_battle.auto_fight()
                self.show_attack_and_attacked()

    def show_all_attacked(self, text) -> None:
        """Метод обновляющий анимацию всех атакованных юнитов"""
        for target_slot in self.new_battle.attacked_slots:
            self.who_attacked(
                target_slot,
                self.curr_unit)

        self.clear_frames_circles()

        # Очистка целей, чтобы в конце боя нельзя было атаковать повторно
        self.new_battle.target_slots = []

        if 'жизни' in self.curr_unit.attack_type:
            self.show_life_drain()

        if not self.new_battle.battle_is_over:
            self.battle_not_over()
        else:
            timer = QTimer(self)
            timer.singleShot(1000, self.battle_over_animations)
            del timer

            self.new_battle.alive_getting_experience()

        self.update_log()
        self.new_battle.autofight = False

    def battle_over_animations(self):
        """Битва закончена"""
        self.show_no_frames(self.unit_circles_dict, show_no_circle)
        self.show_no_frames(self.dung_circles_dict, show_no_circle)
        # возвращаем прежнюю форму
        for unit in (*self.player1.units,
                     *self.player2.units):
            self.show_polymorph_animation(unit)
        self.show_lvl_up_animations()
        self.parent_window.reset()

        if self.parent_window.name == 'CampaignWindow':
            self.parent_window.main.player_list_update()
            self.parent_window.main.player_slots_update()

        if not self.player1.slots:
            self.show_need_upgrade_effect(self.dung_damaged_dict,
                                          self.player2)
        if not self.player2.slots:
            self.show_need_upgrade_effect(self.unit_damaged_dict,
                                          self.player1)

        self.unit_gifs_update()

    def battle_not_over(self):
        """Битва не закончена"""
        self._update_all_unit_health()
        self.next_unit_turn()

    @staticmethod
    def add_gold(mission_number: any) -> None:
        """Добавление золота за победу"""
        player_gold = v_model.gold

        mission_gold = GOLD_GRADATION[v_model.campaign_level][mission_number]

        changed_gold = player_gold + mission_gold

        # обновление золота в базе
        v_model.set_gold(changed_gold)

    def add_upgraded_units(self,
                           player: Player,
                           database: any,
                           side: str,
                           slots_dict: dict) -> None:
        """Добавление в битву получивших опыт юнитов (из базы)"""
        for unit_slot in self.new_battle.alive_units:
            player.slots.remove(unit_slot)
            player.units.remove(
                self._unit_by_slot_and_side(
                    unit_slot,
                    side)
            )

        for unit_slot in self.new_battle.alive_units:
            if player.name == "Computer":
                self.new_battle.add_dung_units()
            else:
                self.new_battle.add_player_unit(
                    unit_slot,
                    player,
                    database)

                self.show_level_up(
                    self._unit_by_slot_and_side(
                        unit_slot,
                        side),
                    slots_dict)

    def show_lvl_up_animations(self) -> None:
        """Анимация всех получивших уровень юнитов"""
        # если юниты игрока 1 мертвы
        if not self.player1.slots:
            self.upgrade_player2_units()

        # если юниты игрока 2 мертвы
        elif not self.player2.slots:
            self.upgrade_player1_units()

            if self.player2.name == 'Computer' \
                    and self.dungeon != 'versus':
                mission_number = self.dungeon.split('_')[-1]
                self.add_gold(mission_number)

                if self.boss_killed():
                    self.__next_campaign_level()
                elif self.last_boss_killed():
                    self.finish_campaign()
                else:
                    self.__next_mission(mission_number)

        self.unlock_buttons_for_player()

    def last_boss_killed(self):
        """Последний Босс кампании повержен"""
        return '15' in self.dungeon \
               and (v_model.campaign_level == 5
                    or
                    (v_model.difficulty == 3
                     and v_model.campaign_level == 4))

    def boss_killed(self):
        """Босс кампании повержен"""
        return '15' in self.dungeon \
               and (v_model.campaign_level != 5
                    or
                    (v_model.difficulty == 3
                     and v_model.campaign_level != 4))

    def __next_campaign_level(self):
        """Повышение уровня кампании, день + 1, генерация миссий"""
        v_model.increase_campaign_level()
        # генерируем миссии
        self.parent_window.update_all_missions(
            v_model.campaign_level, v_model.difficulty)

    def finish_campaign(self):
        """Кампания пройдена"""
        line = f"Поздравляем! Вы прошли кампанию за " \
               f"{v_model.current_faction}.\n"
        logging(line)
        global MES_END_CAMPAIGN
        MES_END_CAMPAIGN = MessageWindow(self, line)
        MES_END_CAMPAIGN.show()

    def __next_mission(self, mission_number):
        """Переходит на следующую миссию кампании"""
        v_model.increase_campaign_mission(
            mission_number,
            self.parent_window.curr_mission)

    def upgrade_player1_units(self):
        """Левел ап юнитов Игрока 1"""
        self.add_upgraded_units(
            self.player1,
            self.db_table,
            self.player_side,
            self.pl_slots_eff_dict
        )

    def upgrade_player2_units(self):
        """Левел ап юнитов Игрока 2"""
        self.add_upgraded_units(
            self.player2,
            Player2Units,
            self.enemy_side,
            self.en_slots_eff_dict
        )

    def show_gif(self,
                 unit: any,
                 gif_slot: QtWidgets.QLabel,
                 action: str,
                 side: str) -> None:
        """Обновление GIF в слоте"""
        if unit is None:
            gif = self.empty_gif(side)

        elif unit.curr_health == 0:
            gif = self.death_animation(action, side, unit)

        # if unit.curr_health == 0:
        #     gif = QMovie(os.path.join(COMMON, "skull.png"))

        else:
            gif = self.action_gif(action, side, unit)

        gif.setSpeed(self.speed)
        gif_slot.setMovie(gif)
        gif.start()

    @staticmethod
    def empty_gif(side):
        gif = QMovie(os.path.join(
            UNIT_STAND,
            f"{side}/empty.gif"))
        return gif

    @staticmethod
    def death_animation(action: str,
                        side: str,
                        unit: Unit) -> QMovie:
        """Анимация смерти"""
        if 'neutral' in unit.subrace:
            gif = QMovie(os.path.join(
                action,
                f"{side}/neutral.gif"))
        else:
            gif = QMovie(os.path.join(
                action,
                f"{side}/{unit.subrace}.gif"))
        return gif

    def show_gif_by_side(self,
                         unit: Unit,
                         action: str,
                         slots_dict1: dict,
                         slots_dict2: dict) -> None:
        """Отображает GIF в зависимости от стороны и действия"""
        slots_dict = {}
        side = self.player_side

        if unit is None:
            pass

        elif unit in self.player1.units:
            slots_dict = slots_dict1

        elif unit in self.player2.units:
            side = self.enemy_side
            slots_dict = slots_dict2

        self.show_gif(
            unit,
            slots_dict[unit.slot],
            action,
            side)

    def show_frames_by_side(self,
                            unit: Unit,
                            slots_dict1: dict,
                            slots_dict2: dict,
                            func: Callable) -> None:
        """Отображает рамку в зависимости от стороны и действия"""
        if unit is None:
            pass
        elif unit in self.player1.units:
            func(slots_dict1[unit.slot])
        elif unit in self.player2.units:
            func(slots_dict2[unit.slot])

    def show_circles_by_side(self,
                             unit: Unit,
                             slots_dict1: dict,
                             slots_dict2: dict,
                             func: Callable) -> None:
        """Отображает круги в зависимости от стороны и действия"""
        if unit is None:
            pass
        elif unit in self.player1.units:
            func(unit,
                 slots_dict1[unit.slot])
        elif unit in self.player2.units:
            func(unit,
                 slots_dict2[unit.slot])

    @staticmethod
    def show_no_frames(slots_dict: dict, func: Callable) -> None:
        """Убирает все рамки"""
        for slot in range(1, 7):
            func(slots_dict[slot])

    def show_circle_g(self, unit, gif_label: QtWidgets.QLabel) -> None:
        """Установка gif'ки круга под юнитом (зеленый)"""
        if unit is not None:
            circle_gif = "big_circle_y.gif" if unit.double \
                else "circle_g.gif"

            gif = QMovie(os.path.join(
                BATTLE_ANIM, circle_gif))

            gif.setSpeed(self.speed)
            gif_label.setMovie(gif)
            gif.start()

    def show_circle_y(self, unit, gif_label: QtWidgets.QLabel) -> None:
        """Установка gif'ки круга под юнитом (желтый)"""
        if unit is not None:
            circle_gif = "big_circle_y.gif" if unit.double \
                else "circle_y.gif"

            gif = QMovie(os.path.join(
                BATTLE_ANIM, circle_gif))

            gif.setSpeed(self.speed)
            gif_label.setMovie(gif)
            gif.start()

    def show_circle_r(self, unit, gif_label: QtWidgets.QLabel) -> None:
        """Установка gif'ки круга под юнитом (красный)"""
        if unit is not None:
            circle_gif = "big_circle_r.gif" if unit.double \
                else "circle_r.gif"

            gif = QMovie(os.path.join(
                BATTLE_ANIM, circle_gif))

            gif.setSpeed(self.speed)
            gif_label.setMovie(gif)
            gif.start()

    def clear_frames_circles(self):
        """Очистить рамки вокруг иконок юнитов и круги под юнитами"""
        self.show_no_frames(self.unit_icons_dict, show_no_frame)
        self.show_no_frames(self.dung_icons_dict, show_no_frame)

        self.show_no_frames(self.unit_circles_dict, show_no_circle)
        self.show_no_frames(self.dung_circles_dict, show_no_circle)

    def show_level_up(self, unit: Unit, slots_dict: dict) -> None:
        """Прорисовка модели юнита, получившего уровень"""
        if unit.slot in self.new_battle.alive_units and \
                self.new_battle.battle_is_over:
            if unit.double:
                unit_gif = "lvl_up_big.gif"
            else:
                unit_gif = "lvl_up.gif"
            gif = QMovie(os.path.join(
                BATTLE_ANIM,
                unit_gif))

            slots_dict[unit.slot].setMovie(gif)
            gif.start()

    def show_attacker(self, unit: Unit) -> None:
        """Прорисовка модели атакующего юнита"""
        self.show_gif_by_side(unit,
                              UNIT_ATTACK,
                              self.pl_slots_dict,
                              self.en_slots_dict)

    def show_frame_attacker(self) -> None:
        """Прорисовка рамки вокруг иконки атакующего юнита"""
        self.show_frames_by_side(self.curr_unit,
                                 self.unit_icons_dict,
                                 self.dung_icons_dict,
                                 show_green_frame)

    def show_circle_attacker(self) -> None:
        """Прорисовка круга под активным юнитом"""
        self.show_circles_by_side(self.curr_unit,
                                  self.unit_circles_dict,
                                  self.dung_circles_dict,
                                  self.show_circle_g)

    def show_attacker_eff(self, unit: Unit) -> None:
        """Прорисовка эффектов атакующего юнита"""
        self.show_gif_by_side(unit,
                              UNIT_EFFECTS_ATTACK,
                              self.pl_slots_eff_dict,
                              self.en_slots_eff_dict)

    def show_shadow_attacker(self, unit: Unit) -> None:
        """Прорисовка тени атакующего юнита"""
        self.show_gif_by_side(unit,
                              UNIT_SHADOW_ATTACK,
                              self.pl_slots_shad_dict,
                              self.en_slots_shad_dict)

    def show_attacked(self, target) -> None:
        """Прорисовка модели атакованного юнита"""
        self.show_gif_by_side(target,
                              UNIT_ATTACKED,
                              self.pl_slots_dict,
                              self.en_slots_dict)

    def show_target_frame(self) -> None:
        """Прорисовка рамки вокруг иконки цели"""
        unit = self.curr_unit

        for target_slot in self.new_battle.targets:
            target = self.get_curr_target(target_slot)

            # цель и текущий юнит принадлежат одному игроку
            if target in self.target_player.units and \
                    unit in self.target_player.units:

                if unit.attack_type in (*ALCHEMIST_LIST, *HEAL_LIST):
                    # синяя рамка
                    self.show_frames_by_side(target,
                                             self.unit_icons_dict,
                                             self.dung_icons_dict,
                                             show_blue_frame)

            else:
                # красная рамка
                self.show_frames_by_side(target,
                                         self.unit_icons_dict,
                                         self.dung_icons_dict,
                                         show_red_frame)

    def clear_effects(self) -> None:
        """Метод скрывающий доты и нанесенный урон"""
        for icon_slot in self.unit_damaged_dict.values():
            clear_dot(icon_slot)

        for icon_slot in self.dung_damaged_dict.values():
            clear_dot(icon_slot)

    def show_shadow_attacked(self, target: Unit) -> None:
        """Прорисовка тени атакованного юнита"""
        self.show_gif_by_side(target,
                              UNIT_SHADOW_ATTACKED,
                              self.pl_slots_shad_dict,
                              self.en_slots_shad_dict)

    def get_curr_target(self, target_slot: int) -> Unit:
        """Получение текущей цели"""
        if self.target_player == self.player2:
            target = self._unit_by_slot_and_side(
                target_slot, self.enemy_side)
        else:
            target = self._unit_by_slot_and_side(
                target_slot, self.player_side)
        return target

    def show_life_drain(self) -> None:
        """Прорисовка анимации высасывания жизни"""
        slots_dict = {}

        if self.curr_unit in self.player1.units:
            slots_dict = self.pl_slots_eff_dict

        elif self.curr_unit in self.player2.units:
            slots_dict = self.en_slots_eff_dict

        unit_gif = "life_drain.gif"
        gif = QMovie(os.path.join(
            BATTLE_ANIM,
            unit_gif))

        gif.setSpeed(self.speed)
        slots_dict[self.curr_unit.slot].setMovie(gif)
        gif.start()

    def who_attack(self) -> None:
        """Метод обновляющий анимацию атакующего юнита"""
        # очищает иконки атакованных юнитов
        self.clear_effects()

        # прорисовка модели атакующего юнита
        self.attacker_thread = Thr(target=self.show_attacker(self.curr_unit),
                                   name="Attacker Thread")
        self.attacker_thread.start()

        # self.show_attacker(self.curr_unit)

        # прорисовка эффектов атакующего юнита
        self.attacker_eff_thread = Thr(
            target=self.show_attacker_eff(self.curr_unit),
            name="Attacker Effect Thread")
        self.attacker_eff_thread.start()

        # self.show_attacker_eff(self.curr_unit)

        # прорисовка тени атакующего юнита
        self.attacker_shadow_thread = Thr(
            target=self.show_shadow_attacker(self.curr_unit),
            name="Attacker Shadow Thread")
        self.attacker_shadow_thread.start()

        # self.show_shadow_attacker(self.curr_unit)

        # прорисовка атаки по области для атакующего юнита
        if self.curr_unit.attack_purpose == 6:
            self.attacker_splash_thread = Thr(
                target=self.show_splash_area(
                    self.curr_unit,
                    UNIT_EFFECTS_AREA),
                name="Attacker Splash Thread")
            self.attacker_splash_thread.start()

            # self.show_splash_area(
            #     self.curr_unit,
            #     UNIT_EFFECTS_AREA)

    def who_attacked(self, target_slot: int, current_unit: Unit) -> None:
        """Метод обновляющий анимацию атакованного юнита"""
        if target_slot is None:
            return

        # получение текущей цели
        target = self.get_curr_target(target_slot)

        if target is None:
            pass

        # цель и текущий юнит принадлежат одному игроку
        elif self.unit_is_allied(target):
            self.show_effects(target, current_unit)
        else:
            self.show_attacked(target)
            self.show_shadow_attacked(target)
            self.show_effects(target, current_unit)

            if self.target_player == self.player1:
                show_damage(
                    self.unit_damaged_dict[target.slot])
            else:
                show_damage(
                    self.dung_damaged_dict[target.slot])

        # если атакованный юнит погиб
        if target.is_dead:
            if target.dotted:
                self.show_polymorph_animation(target)

            self.new_battle.check_player_is_alive()

            if self.new_battle.battle_is_over:
                # возвращаем прежнюю форму
                for unit in (*self.player1.units,
                             *self.player2.units):
                    self.show_polymorph_animation(unit)

            # удаляем цель
            self.new_battle.remove_unit(target)

    def show_effects(self,
                     target: Unit,
                     current_unit: Unit):
        """Показывает эффекты от атаки на юните"""
        icons_dict = self.pl_slots_attacked_eff_dict
        side = self.player_side

        if self.target_player == self.player1:
            icons_dict = self.pl_slots_attacked_eff_dict
            side = self.player_side
        elif self.target_player == self.player2:
            icons_dict = self.en_slots_attacked_eff_dict
            side = self.enemy_side

        self.show_gif(
            current_unit,
            icons_dict[target.slot],
            UNIT_EFFECTS_TARGET,
            side)

    def unit_is_allied(self, target: Unit):
        return target in self.target_player.units and \
               self.curr_unit in self.target_player.units

    def show_polymorph_animation(self, unit: Unit) -> None:
        """Отображает анимацию возвращения юнита в прежнюю форму
        (до Полиморфа). Обновляет иконки юнитов. Замена юнита в битве."""
        if self.dotted_units.get(unit):
            if self.dotted_units[unit].get(POLYMORPH):
                ui_label = self.pl_slots_dict[unit.slot]

                if unit in self.player1.units:
                    ui_label = self.pl_slots_dict[unit.slot]

                elif unit in self.player2.units:
                    ui_label = self.en_slots_dict[unit.slot]

                # Сначала отображаем анимацию Полиморфа
                show_polymorph(ui_label)

                # Меняем иконку
                self.unit_icons_update()

                # Возвращаем юнит к прежней форме
                self.new_battle.back_to_prev_form(unit)

    def show_dot_effect(self, unit: Unit, dot_type: str, icons_dict: dict):
        """Показывает действующий отрицательный эффект на юните"""
        if self.dotted_units[unit].get(dot_type):
            rounds = self.dotted_units[unit][dot_type][1]
            if rounds:
                show_dot_icon(
                    icons_dict[unit.slot], dot_type)
            else:
                show_dot_icon(
                    icons_dict[unit.slot], 'spare_dot')

    def show_might_effect(self, unit: Unit, dot_type: str, icons_dict: dict):
        """Показывает действующий положительный эффект на юните"""
        if self.new_battle.boosted_units.get(unit):
            show_dot_icon(
                icons_dict[unit.slot], dot_type)

    @staticmethod
    def show_need_upgrade_effect(icons_dict: dict, player: Player):
        """Показывает ограничение в апгрейде на юните"""
        for unit in player.units:
            # if unit.exp == 'Максимальный':
            if unit.exp is None:
                pass
            else:
                if unit.curr_exp == unit.exp - 1:
                    show_dot_icon(
                        icons_dict[unit.slot], 'waiting_next')

    def define_priority_effect(self, unit: Unit, icons_dict: dict):
        """Отобразить один приоритетный эффект"""
        self.show_dot_effect(unit, 'Снижение урона', icons_dict)
        self.show_dot_effect(unit, 'Снижение инициативы', icons_dict)
        self.show_dot_effect(unit, 'Полиморф', icons_dict)
        self.show_dot_effect(unit, 'Яд', icons_dict)
        self.show_dot_effect(unit, 'Ожог', icons_dict)
        self.show_dot_effect(unit, 'Обморожение', icons_dict)
        self.show_dot_effect(unit, 'Паралич', icons_dict)
        self.show_dot_effect(unit, 'Окаменение', icons_dict)

    def define_dotted_units(self):
        """Определяет юнитов с наложенными эффектами"""
        self.show_dot_on_units(self.player1.units,
                               self.unit_damaged_dict)

        self.show_dot_on_units(self.player2.units,
                               self.dung_damaged_dict)

    def show_dot_on_units(self, units, units_dict):
        """Показывает эффекты на юнитах"""
        for unit in units:
            if unit in self.dotted_units:
                # Показывает эффект на юните
                self.define_priority_effect(unit, units_dict)

            elif unit in self.new_battle.boosted_units:
                self.show_might_effect(
                    unit, 'Увеличение урона', units_dict)

    def update_icons(self, player: str) -> None:
        """Обновление иконок и кнопок юнитов"""
        icons_dict = self.unit_icons_dict
        damage_dict = self.unit_damaged_dict
        side = self.player_side

        if player == PLAYER:
            icons_dict = self.unit_icons_dict
            damage_dict = self.unit_damaged_dict
            side = self.player_side
        elif player == ENEMY:
            icons_dict = self.dung_icons_dict
            damage_dict = self.dung_damaged_dict
            side = self.enemy_side

        for num, icon_slot in icons_dict.items():
            unit = self._unit_by_slot_and_side(num, side)
            self._slot_update(
                unit,
                icon_slot,
                side)
            self._set_size_by_unit(
                unit,
                damage_dict[num],
                side)

    def set_unit_icons(self) -> None:
        """Заполнение временных словарей иконок и кнопок юнитов"""
        # Иконки юнитов FRONT стороны
        self.append_front_icons()

        # Кнопки юнитов FRONT стороны
        self.append_front_field()

        # Иконки атакованных юнитов FRONT стороны
        self.append_front_damaged()

        # Иконки кругов FRONT стороны
        self.append_front_circles()

        # Иконки юнитов REAR стороны
        self.append_rear_icons()

        # Кнопки юнитов REAR стороны
        self.append_rear_field()

        # Иконки атакованных юнитов REAR стороны
        self.append_rear_damaged()

        # Иконки кругов REAR стороны
        self.append_rear_circles()

    def unit_icons_update(self) -> None:
        """Метод обновляющий иконки юнитов игроков"""
        self.update_icons(PLAYER)
        self.update_icons(ENEMY)

    def change_icons(self) -> None:
        """Меняет местами FRONT/REAR иконки юнитов игроков"""
        self.unit_icons_dict, self.dung_icons_dict = \
            self.dung_icons_dict, self.unit_icons_dict
        self.unit_damaged_dict, self.dung_damaged_dict = \
            self.dung_damaged_dict, self.unit_damaged_dict
        self.unit_circles_dict, self.dung_circles_dict = \
            self.dung_circles_dict, self.unit_circles_dict
        self.unit_field_dict, self.dung_field_dict = \
            self.dung_field_dict, self.unit_field_dict

    def animate_action(self,
                       slots_dict: dict,
                       unit_action: str,
                       side: str) -> None:
        """Анимации юнитов игрока"""
        for num, gif_slot in slots_dict.items():
            self.show_gif(
                self._unit_by_slot_and_side(num, side),
                gif_slot,
                unit_action,
                side)

    def unit_gifs_in_thread(self):
        """Метод обновляющий анимацию юнитов"""
        self.show_circle_attacker()
        self._update_all_unit_health()
        self.unit_icons_update()

    def unit_gifs_update(self) -> None:
        """Метод обновляющий анимацию юнитов. Вызов потока"""
        self.animate_action(
            self.pl_slots_dict,
            UNIT_STAND,
            self.player_side)

        # прорисовка тени бездействующего юнита игрока
        self.animate_action(
            self.pl_slots_shad_dict,
            UNIT_SHADOW_STAND,
            self.player_side)

        # прорисовка модели бездействующего юнита врага
        self.animate_action(
            self.en_slots_dict,
            UNIT_STAND,
            self.enemy_side)

        # прорисовка тени бездействующего юнита врага
        self.animate_action(
            self.en_slots_shad_dict,
            UNIT_SHADOW_STAND,
            self.enemy_side)

        self.gifs_thread = Thr(target=self.unit_gifs_in_thread,
                               name="Gifs Thread")
        self.gifs_thread.start()

    def _update_all_unit_health(self) -> None:
        """Метод обновляющий текущее здоровье всех юнитов"""

        # прорисовка здоровья юнитов со стороны FRONT
        for num, hp_slot in self.pl_hp_slots_dict.items():
            update_unit_health(
                self._unit_by_slot_and_side(num, self.player_side),
                hp_slot)

        # прорисовка здоровья юнитов со стороны REAR
        for num, hp_slot in self.en_hp_slots_dict.items():
            update_unit_health(
                self._unit_by_slot_and_side(num, self.enemy_side),
                hp_slot)

        # показать иконки эффектов
        self.define_dotted_units()

    def set_coords_double_slots(self, ui_obj) -> None:
        """Задание координат для 'двойных' слотов либо кнопок"""
        if ui_obj in self.right_slots:
            ui_coords = ui_obj.geometry().getCoords()
            new_coords = list(ui_coords)
            new_coords[0] = 147
            ui_obj.setGeometry(*new_coords)

            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def _set_size_by_unit(self, unit: Unit, ui_obj: any, side: str) -> None:
        """Установка размера иконки по размеру самого юнита"""
        self.set_coords_double_slots(ui_obj)

        try:
            if unit.double \
                    and ui_obj in self.right_slots \
                    and side == FRONT:
                ui_coords = ui_obj.geometry().getCoords()
                new_coords = list(ui_coords)
                new_coords[0] -= 117
                new_coords[2] = 224
                new_coords[3] = 126
                ui_obj.setGeometry(*new_coords)

            if unit.double:
                ui_obj.setFixedWidth(225)
                ui_obj.setFixedHeight(127)

            else:
                ui_obj.setFixedWidth(105)
                ui_obj.setFixedHeight(127)
        except AttributeError:
            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def _slot_update(self,
                     unit: Unit,
                     slot: QtWidgets.QLabel,
                     side: str) -> None:
        """Метод обновления иконки"""
        self._set_size_by_unit(unit, slot, side)

        slot.setPixmap(QPixmap(
            get_unit_image(unit)).scaled(
            slot.width(), slot.height()))
        self.hbox.addWidget(slot)
        self.setLayout(self.hbox)

    @staticmethod
    def _slot_detailed(unit: Unit, slot_dialog: any) -> None:
        """Метод создающий окно юнита игрока при нажатии на слот."""
        try:
            global DETAIL_WINDOW
            DETAIL_WINDOW = slot_dialog(
                unit)
            DETAIL_WINDOW.show()
        except AttributeError:
            pass

    def attack_enemy_by_slot(self, slot: int, side: str) -> None:
        """Атака и анимация по выбранному слоту противника"""
        target = self._unit_by_slot_and_side(slot, side)

        # невозможность атаковать своих
        if target is not None:
            if target not in self.new_battle.current_player.units \
                    and self.curr_unit.attack_type \
                    not in [*HEAL_LIST, *ALCHEMIST_LIST]:

                self.new_battle.player_attack(target)
                self.show_attack_and_attacked()

            # если текущий юнит лекарь - можно выбрать целью свой юнит
            elif target in self.new_battle.current_player.units \
                    and self.curr_unit.attack_type \
                    in [*HEAL_LIST, *ALCHEMIST_LIST]:

                self.new_battle.player_attack(target)
                self.show_attack_and_attacked()

    def _unit_by_slot_and_side(self,
                               slot: int,
                               side: str) -> Optional[Unit]:
        """Метод получающий юнита игрока по слоту и стороне."""
        if side == self.player_side:
            for unit in self.player1.units:
                if unit.slot == slot:
                    return unit
        else:
            for unit in self.player2.units:
                if unit.slot == slot:
                    return unit
        return None
