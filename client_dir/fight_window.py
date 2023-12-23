"""Окно битвы"""

import os.path
import random
from typing import Callable, Optional

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QMovie, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from battle import Battle, Player
from client_dir.fight_form import Ui_FightWindow
from client_dir.settings import UNIT_STAND, UNIT_ATTACK, \
    UNIT_ATTACKED, UNIT_EFFECTS_ATTACK, BATTLE_GROUND, FRONT, REAR, \
    COMMON, BATTLE_GROUNDS, UNIT_SHADOW_ATTACK, UNIT_SHADOW_STAND, \
    UNIT_SHADOW_ATTACKED, UNIT_EFFECTS_AREA, UNIT_EFFECTS_TARGET, \
    RIGHT_ICONS, LEFT_ICONS, SCREEN_RECT, PANEL_RECT, BATTLE_LOG, \
    BATTLE_ANIM, BIG, HEAL_LIST, ALCHEMIST_LIST
from client_dir.ui_functions import show_no_frame, \
    show_damage, show_no_damage, show_green_frame, \
    show_red_frame, show_blue_frame, update_unit_health, \
    get_unit_image, show_no_circle, ui_lock, ui_unlock, \
    show_dot_icon
from client_dir.unit_dialog import UnitDialog
from units_dir.ranking import GOLD_GRADATION
from units_dir.units import main_db
from units_dir.units_factory import Unit


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
            i = 15_000_000

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
                 db_table: str,
                 instance: any):
        super().__init__()
        # основные переменные
        self.parent = instance
        self.db_table = db_table
        self.new_battle = Battle(dungeon, self.db_table)
        self.dungeon = dungeon
        self.computer_name = 'Computer'
        self.player_side = FRONT
        self.enemy_side = REAR
        self.speed = 300

        # временные словари иконок и кнопок на них
        self.front_icons_dict = {}
        self.front_damaged_dict = {}
        self.front_buttons_dict = {}
        self.front_circles_dict = {}
        # self.front_field_buttons_dict = {}

        self.rear_icons_dict = {}
        self.rear_damaged_dict = {}
        self.rear_buttons_dict = {}
        self.rear_circles_dict = {}
        # self.rear_field_buttons_dict = {}

        # словари иконок и кнопок на них
        self.unit_icons_dict = {}
        self.unit_damaged_dict = {}
        self.unit_buttons_dict = {}

        self.dung_icons_dict = {}
        self.dung_damaged_dict = {}
        self.dung_buttons_dict = {}

        # словари для кругов под юнитами
        self.unit_circles_dict = {}
        self.dung_circles_dict = {}

        # словари кнопок с поля боя
        # self.unit_field_buttons_dict = {}
        # self.dung_field_buttons_dict = {}

        # временные словари лейблов для анимаций и hp юнитов игрока 1
        self.front_slots_dict = {}
        self.front_slots_shad_dict = {}
        self.front_slots_eff_dict = {}
        self.front_slots_attacked_eff_dict = {}
        self.front_hp_slots_dict = {}

        # временные словари лейблов для анимаций и hp юнитов игрока 2
        self.rear_slots_dict = {}
        self.rear_slots_shad_dict = {}
        self.rear_slots_eff_dict = {}
        self.rear_slots_attacked_eff_dict = {}
        self.rear_hp_slots_dict = {}

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
            log.write(f'Ходит: {self.new_battle.current_unit.name}\n')
            log.write("Новая битва\n")
        self.update_log()

        self.check_ai()

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
            self.ui.pushButtonSlot2,
            self.ui.pushButtonSlot4,
            self.ui.pushButtonSlot6,
        ]

        self.ui.leftIcons.setPixmap(
            QPixmap(LEFT_ICONS))
        self.ui.rightIcons.setPixmap(
            QPixmap(RIGHT_ICONS))

        self.ui.pushButtonBack.clicked.connect(self.back)

        self.ui.pushButtonDefence.clicked.connect(self.unit_defence)
        self.ui.pushButtonWaiting.clicked.connect(self.unit_waiting)

        self.ui.pushButtonSlot1.clicked.connect(
            self._attack_player_slot1)
        self.ui.pushButtonSlot2.clicked.connect(
            self._attack_player_slot2)
        self.ui.pushButtonSlot3.clicked.connect(
            self._attack_player_slot3)
        self.ui.pushButtonSlot4.clicked.connect(
            self._attack_player_slot4)
        self.ui.pushButtonSlot5.clicked.connect(
            self._attack_player_slot5)
        self.ui.pushButtonSlot6.clicked.connect(
            self._attack_player_slot6)

        self.ui.pushButtonUnit_1.clicked.connect(
            self._attack_player_slot1)
        self.ui.pushButtonUnit_2.clicked.connect(
            self._attack_player_slot2)
        self.ui.pushButtonUnit_3.clicked.connect(
            self._attack_player_slot3)
        self.ui.pushButtonUnit_4.clicked.connect(
            self._attack_player_slot4)
        self.ui.pushButtonUnit_5.clicked.connect(
            self._attack_player_slot5)
        self.ui.pushButtonUnit_6.clicked.connect(
            self._attack_player_slot6)

        self.ui.pushButtonEnemySlot1.clicked.connect(
            self._attack_enemy_slot1)
        self.ui.pushButtonEnemySlot2.clicked.connect(
            self._attack_enemy_slot2)
        self.ui.pushButtonEnemySlot3.clicked.connect(
            self._attack_enemy_slot3)
        self.ui.pushButtonEnemySlot4.clicked.connect(
            self._attack_enemy_slot4)
        self.ui.pushButtonEnemySlot5.clicked.connect(
            self._attack_enemy_slot5)
        self.ui.pushButtonEnemySlot6.clicked.connect(
            self._attack_enemy_slot6)

        self.ui.pushButtonEnemyUnit_1.clicked.connect(
            self._attack_enemy_slot1)
        self.ui.pushButtonEnemyUnit_2.clicked.connect(
            self._attack_enemy_slot2)
        self.ui.pushButtonEnemyUnit_3.clicked.connect(
            self._attack_enemy_slot3)
        self.ui.pushButtonEnemyUnit_4.clicked.connect(
            self._attack_enemy_slot4)
        self.ui.pushButtonEnemyUnit_5.clicked.connect(
            self._attack_enemy_slot5)
        self.ui.pushButtonEnemyUnit_6.clicked.connect(
            self._attack_enemy_slot6)

        # контекстное меню для 1 слота игрока
        self.ui.pushButtonSlot1.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.pushButtonSlot1.customContextMenuRequested\
            .connect(self._slot1_detailed)

        # контекстное меню для 2 слота игрока
        self.ui.pushButtonSlot2.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.pushButtonSlot2.customContextMenuRequested\
            .connect(self._slot2_detailed)

        # контекстное меню для 3 слота игрока
        self.ui.pushButtonSlot3.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.pushButtonSlot3.customContextMenuRequested\
            .connect(self._slot3_detailed)

        # контекстное меню для 4 слота игрока
        self.ui.pushButtonSlot4.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.pushButtonSlot4.customContextMenuRequested\
            .connect(self._slot4_detailed)

        # контекстное меню для 5 слота игрока
        self.ui.pushButtonSlot5.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.pushButtonSlot5.customContextMenuRequested\
            .connect(self._slot5_detailed)

        # контекстное меню для 6 слота игрока
        self.ui.pushButtonSlot6.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.pushButtonSlot6.customContextMenuRequested\
            .connect(self._slot6_detailed)

        # контекстное меню для 1 слота противника
        self.ui.pushButtonEnemySlot1.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.pushButtonEnemySlot1.customContextMenuRequested\
            .connect(self._enemy_slot1_detailed)

        # контекстное меню для 2 слота противника
        self.ui.pushButtonEnemySlot2.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.pushButtonEnemySlot2.customContextMenuRequested\
            .connect(self._enemy_slot2_detailed)

        # контекстное меню для 3 слота противника
        self.ui.pushButtonEnemySlot3.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.pushButtonEnemySlot3.customContextMenuRequested\
            .connect(self._enemy_slot3_detailed)

        # контекстное меню для 4 слота противника
        self.ui.pushButtonEnemySlot4.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.pushButtonEnemySlot4.customContextMenuRequested\
            .connect(self._enemy_slot4_detailed)

        # контекстное меню для 5 слота противника
        self.ui.pushButtonEnemySlot5.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.pushButtonEnemySlot5.customContextMenuRequested\
            .connect(self._enemy_slot5_detailed)

        # контекстное меню для 6 слота противника
        self.ui.pushButtonEnemySlot6.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.pushButtonEnemySlot6.customContextMenuRequested \
            .connect(self._enemy_slot6_detailed)

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
        self.set_front_gif_player1_dict()

        self.set_unit_icons()
        self.set_unit_icons_player1()

        self.ui.battleLog.setStyleSheet("background-color: rgb(65, 3, 2)")

        self.update_speed_checkbox()
        self.show_target_frame()
        self.show_frame_attacker()
        self.update_log()

        self.ui.pushButtonSlot1.installEventFilter(self)
        self.ui.pushButtonSlot2.installEventFilter(self)
        self.ui.pushButtonSlot3.installEventFilter(self)
        self.ui.pushButtonSlot4.installEventFilter(self)
        self.ui.pushButtonSlot5.installEventFilter(self)
        self.ui.pushButtonSlot6.installEventFilter(self)

        self.ui.pushButtonEnemySlot1.installEventFilter(self)
        self.ui.pushButtonEnemySlot2.installEventFilter(self)
        self.ui.pushButtonEnemySlot3.installEventFilter(self)
        self.ui.pushButtonEnemySlot4.installEventFilter(self)
        self.ui.pushButtonEnemySlot5.installEventFilter(self)
        self.ui.pushButtonEnemySlot6.installEventFilter(self)

        # self.ui.pushButtonUnit_1.installEventFilter(self)
        # self.ui.pushButtonUnit_2.installEventFilter(self)
        # self.ui.pushButtonUnit_3.installEventFilter(self)
        # self.ui.pushButtonUnit_4.installEventFilter(self)
        # self.ui.pushButtonUnit_5.installEventFilter(self)
        # self.ui.pushButtonUnit_6.installEventFilter(self)

        # self.ui.pushButtonEnemyUnit_1.installEventFilter(self)
        # self.ui.pushButtonEnemyUnit_2.installEventFilter(self)
        # self.ui.pushButtonEnemyUnit_3.installEventFilter(self)
        # self.ui.pushButtonEnemyUnit_4.installEventFilter(self)
        # self.ui.pushButtonEnemyUnit_5.installEventFilter(self)
        # self.ui.pushButtonEnemyUnit_6.installEventFilter(self)

        self.unit_gifs_update()

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.show()

    def eventFilter(self, source, event):
        """Обработчик событий"""
        if self.player_side == FRONT:
            # front side
            self.show_circle_by_unit(self.unit_buttons_dict,
                                     self.unit_circles_dict,
                                     FRONT,
                                     source,
                                     event)

            # self.show_circle_by_unit(self.unit_field_buttons_dict,
            #                          self.unit_circles_dict,
            #                          FRONT,
            #                          source,
            #                          event)

            # rear side
            self.show_circle_by_unit(self.dung_buttons_dict,
                                     self.dung_circles_dict,
                                     REAR,
                                     source,
                                     event)

            # self.show_circle_by_unit(self.dung_field_buttons_dict,
            #                          self.dung_circles_dict,
            #                          REAR,
            #                          source,
            #                          event)

        elif self.player_side == REAR:
            # rear side
            self.show_circle_by_unit(self.unit_buttons_dict,
                                     self.unit_circles_dict,
                                     REAR,
                                     source,
                                     event)

            # front side
            self.show_circle_by_unit(self.dung_buttons_dict,
                                     self.dung_circles_dict,
                                     FRONT,
                                     source,
                                     event)

        return super().eventFilter(source, event)

    def show_circle_by_unit(self,
                            buttons_dict: dict,
                            ui_dict: dict,
                            side: str,
                            source: any,
                            event: any):
        """Установка gif'ки круга под юнитом"""
        for num, item in buttons_dict.items():
            unit = self._unit_by_slot_and_side(num, side)

            if source == item \
                    and unit is not None \
                    and unit.curr_health != 0:

                if event.type() == QtCore.QEvent.Enter:
                    if unit not in self.new_battle.current_player.units:
                        self.show_circle_r(unit, ui_dict.get(num))

                    if unit in self.new_battle.current_player.units:
                        self.show_circle_y(unit, ui_dict.get(num))

                elif event.type() == QtCore.QEvent.Leave:
                    show_no_circle(ui_dict.get(num))
                    # битва еще не закончена
                    if not self.new_battle.battle_is_over:
                        self.show_circle_attacker()

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

        speed_slots = [0.5, 1, 1.5, 2, 2.5,
                       3, 3.5, 4, 4.5, 5]
        self.speed_model = QStandardItemModel()
        for slot in speed_slots:
            item = QStandardItem(str(slot))
            item.setEditable(False)
            self.speed_model.appendRow(item)
        self.ui.comboSpeed.setModel(self.speed_model)

        self.ui.comboSpeed.setCurrentIndex(5)
        self.check_speed()
        self.ui.comboSpeed.currentIndexChanged.connect(self.check_speed)

    def check_speed(self) -> None:
        """Устанавливает выбранную скорость анимации"""
        multiplier = self.ui.comboSpeed.currentText()
        self.speed = 100 * float(multiplier)
        # self.unit_gifs_update()

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
        self.parent.reset()
        if self.parent.name == 'CampaignWindow':
            self.parent.main.reset()
        self.close()

    def change_side(self) -> None:
        """Смена сторон"""
        if self.player_side == FRONT:
            self.player_side = REAR
            self.enemy_side = FRONT

            self.set_front_gif_player2_dict()
        else:
            self.player_side = FRONT
            self.enemy_side = REAR

            self.set_front_gif_player1_dict()

        self.unit_gifs_update()
        self.show_no_damaged()
        self.clear_frames_circles()

        self.check_ai()

        if not self.new_battle.battle_is_over:
            self.show_target_frame()
            self.show_frame_attacker()
            self.show_circle_attacker()

    def set_front_gif_player1_dict(self) -> None:
        """Задание FRONT стороны для анимационных GIF игрока 1"""
        self.pl_slots_dict = self.front_slots_dict
        self.pl_slots_shad_dict = self.front_slots_shad_dict
        self.pl_slots_eff_dict = self.front_slots_eff_dict
        self.pl_slots_attacked_eff_dict = self.front_slots_attacked_eff_dict
        self.pl_hp_slots_dict = self.front_hp_slots_dict

        self.en_slots_dict = self.rear_slots_dict
        self.en_slots_shad_dict = self.rear_slots_shad_dict
        self.en_slots_eff_dict = self.rear_slots_eff_dict
        self.en_slots_attacked_eff_dict = self.rear_slots_attacked_eff_dict
        self.en_hp_slots_dict = self.rear_hp_slots_dict

    def set_front_gif_player2_dict(self) -> None:
        """Задание FRONT стороны для анимационных GIF игрока 2"""
        self.pl_slots_dict = self.rear_slots_dict
        self.pl_slots_shad_dict = self.rear_slots_shad_dict
        self.pl_slots_eff_dict = self.rear_slots_eff_dict
        self.pl_slots_attacked_eff_dict = self.rear_slots_attacked_eff_dict
        self.pl_hp_slots_dict = self.rear_hp_slots_dict

        self.en_slots_dict = self.front_slots_dict
        self.en_slots_shad_dict = self.front_slots_shad_dict
        self.en_slots_eff_dict = self.front_slots_eff_dict
        self.en_slots_attacked_eff_dict = self.front_slots_attacked_eff_dict
        self.en_hp_slots_dict = self.front_hp_slots_dict

    def append_front(self) -> None:
        """Основные анимационные GIF юнитов FRONT стороны"""
        self.front_slots_dict = {
            1: self.ui.gifPlayerSlot_1,
            2: self.ui.gifPlayerSlot_2,
            3: self.ui.gifPlayerSlot_3,
            4: self.ui.gifPlayerSlot_4,
            5: self.ui.gifPlayerSlot_5,
            6: self.ui.gifPlayerSlot_6,
        }

    def append_front_shadows(self) -> None:
        """Анимационные GIF теней юнитов FRONT стороны"""
        self.front_slots_shad_dict = {
            1: self.ui.gifShadSlot_1,
            2: self.ui.gifShadSlot_2,
            3: self.ui.gifShadSlot_3,
            4: self.ui.gifShadSlot_4,
            5: self.ui.gifShadSlot_5,
            6: self.ui.gifShadSlot_6,
        }

    def append_front_effects(self) -> None:
        """Анимационные GIF эффектов атакующий юнитов FRONT стороны"""
        self.front_slots_eff_dict = {
            1: self.ui.gifEffSlot_1,
            2: self.ui.gifEffSlot_2,
            3: self.ui.gifEffSlot_3,
            4: self.ui.gifEffSlot_4,
            5: self.ui.gifEffSlot_5,
            6: self.ui.gifEffSlot_6,
        }

    def append_front_attacked_eff(self) -> None:
        """Анимационные GIF эффектов атакованных юнитов FRONT стороны"""
        self.front_slots_attacked_eff_dict = {
            1: self.ui.gifPlayerAttEffSlot_1,
            2: self.ui.gifPlayerAttEffSlot_2,
            3: self.ui.gifPlayerAttEffSlot_3,
            4: self.ui.gifPlayerAttEffSlot_4,
            5: self.ui.gifPlayerAttEffSlot_5,
            6: self.ui.gifPlayerAttEffSlot_6,
        }

    def append_front_hp(self) -> None:
        """GIF очков здоровья юнитов FRONT стороны"""
        self.front_hp_slots_dict = {
            1: self.ui.hpSlot1,
            2: self.ui.hpSlot2,
            3: self.ui.hpSlot3,
            4: self.ui.hpSlot4,
            5: self.ui.hpSlot5,
            6: self.ui.hpSlot6,
        }

    def append_rear(self) -> None:
        """Анимационные GIF теней юнитов REAR стороны"""
        self.rear_slots_dict = {
            1: self.ui.gifEnemySlot_1,
            2: self.ui.gifEnemySlot_2,
            3: self.ui.gifEnemySlot_3,
            4: self.ui.gifEnemySlot_4,
            5: self.ui.gifEnemySlot_5,
            6: self.ui.gifEnemySlot_6,
        }

    def append_rear_shadows(self) -> None:
        """Анимационные GIF теней юнитов REAR стороны"""
        self.rear_slots_shad_dict = {
            1: self.ui.gifEnemyShadSlot_1,
            2: self.ui.gifEnemyShadSlot_2,
            3: self.ui.gifEnemyShadSlot_3,
            4: self.ui.gifEnemyShadSlot_4,
            5: self.ui.gifEnemyShadSlot_5,
            6: self.ui.gifEnemyShadSlot_6,
        }

    def append_rear_effects(self) -> None:
        """Анимационные GIF эффектов атакующий юнитов REAR стороны"""
        self.rear_slots_eff_dict = {
            1: self.ui.gifEnemyEffSlot_1,
            2: self.ui.gifEnemyEffSlot_2,
            3: self.ui.gifEnemyEffSlot_3,
            4: self.ui.gifEnemyEffSlot_4,
            5: self.ui.gifEnemyEffSlot_5,
            6: self.ui.gifEnemyEffSlot_6,
        }

    def append_rear_attacked_eff(self) -> None:
        """Анимационные GIF эффектов атакованных юнитов REAR стороны"""
        self.rear_slots_attacked_eff_dict = {
            1: self.ui.gifEnemyAttEffSlot_1,
            2: self.ui.gifEnemyAttEffSlot_2,
            3: self.ui.gifEnemyAttEffSlot_3,
            4: self.ui.gifEnemyAttEffSlot_4,
            5: self.ui.gifEnemyAttEffSlot_5,
            6: self.ui.gifEnemyAttEffSlot_6,
        }

    def append_rear_hp(self) -> None:
        """GIF очков здоровья юнитов REAR стороны"""
        self.rear_hp_slots_dict = {
            1: self.ui.enemyHPSlot1,
            2: self.ui.enemyHPSlot2,
            3: self.ui.enemyHPSlot3,
            4: self.ui.enemyHPSlot4,
            5: self.ui.enemyHPSlot5,
            6: self.ui.enemyHPSlot6,
        }

    def set_front_gif_player1(self) -> None:
        """Задание FRONT стороны для анимационных GIF игрока 1 (по умолчанию)"""
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
        self.front_icons_dict = {
            1: self.ui.slot1,
            2: self.ui.slot2,
            3: self.ui.slot3,
            4: self.ui.slot4,
            5: self.ui.slot5,
            6: self.ui.slot6,
        }

    def append_front_buttons(self) -> None:
        """Кнопки юнитов FRONT стороны"""
        self.front_buttons_dict = {
            1: self.ui.pushButtonSlot1,
            2: self.ui.pushButtonSlot2,
            3: self.ui.pushButtonSlot3,
            4: self.ui.pushButtonSlot4,
            5: self.ui.pushButtonSlot5,
            6: self.ui.pushButtonSlot6,
        }

        # self.front_field_buttons_dict = {
        #     1: self.ui.pushButtonUnit_1,
        #     2: self.ui.pushButtonUnit_2,
        #     3: self.ui.pushButtonUnit_3,
        #     4: self.ui.pushButtonUnit_4,
        #     5: self.ui.pushButtonUnit_5,
        #     6: self.ui.pushButtonUnit_6,
        # }

    def append_front_damaged(self) -> None:
        """Иконки атакованных юнитов FRONT стороны"""
        self.front_damaged_dict = {
            1: self.ui.damPlayerSlot_1,
            2: self.ui.damPlayerSlot_2,
            3: self.ui.damPlayerSlot_3,
            4: self.ui.damPlayerSlot_4,
            5: self.ui.damPlayerSlot_5,
            6: self.ui.damPlayerSlot_6,
        }

    def append_front_circles(self) -> None:
        """Круги юнитов FRONT стороны"""
        self.front_circles_dict = {
            1: self.ui.gifCircleSlot_1,
            2: self.ui.gifCircleSlot_2,
            3: self.ui.gifCircleSlot_3,
            4: self.ui.gifCircleSlot_4,
            5: self.ui.gifCircleSlot_5,
            6: self.ui.gifCircleSlot_6,
        }

    def append_rear_icons(self) -> None:
        """GIF иконок юнитов REAR стороны"""
        self.rear_icons_dict = {
            1: self.ui.enemySlot1,
            2: self.ui.enemySlot2,
            3: self.ui.enemySlot3,
            4: self.ui.enemySlot4,
            5: self.ui.enemySlot5,
            6: self.ui.enemySlot6,
        }

    def append_rear_buttons(self) -> None:
        """GIF кнопок юнитов REAR стороны"""
        self.rear_buttons_dict = {
            1: self.ui.pushButtonEnemySlot1,
            2: self.ui.pushButtonEnemySlot2,
            3: self.ui.pushButtonEnemySlot3,
            4: self.ui.pushButtonEnemySlot4,
            5: self.ui.pushButtonEnemySlot5,
            6: self.ui.pushButtonEnemySlot6,
        }

        # self.rear_field_buttons_dict = {
        #     1: self.ui.pushButtonEnemyUnit_1,
        #     2: self.ui.pushButtonEnemyUnit_2,
        #     3: self.ui.pushButtonEnemyUnit_3,
        #     4: self.ui.pushButtonEnemyUnit_4,
        #     5: self.ui.pushButtonEnemyUnit_5,
        #     6: self.ui.pushButtonEnemyUnit_6,
        # }

    def append_rear_damaged(self) -> None:
        """Иконки атакованных юнитов REAR стороны"""
        self.rear_damaged_dict = {
            1: self.ui.damEnemySlot_1,
            2: self.ui.damEnemySlot_2,
            3: self.ui.damEnemySlot_3,
            4: self.ui.damEnemySlot_4,
            5: self.ui.damEnemySlot_5,
            6: self.ui.damEnemySlot_6,
        }

    def append_rear_circles(self) -> None:
        """Круги юнитов REAR стороны"""
        self.rear_circles_dict = {
            1: self.ui.gifEnemyCircleSlot_1,
            2: self.ui.gifEnemyCircleSlot_2,
            3: self.ui.gifEnemyCircleSlot_3,
            4: self.ui.gifEnemyCircleSlot_4,
            5: self.ui.gifEnemyCircleSlot_5,
            6: self.ui.gifEnemyCircleSlot_6,
        }

    def show_splash_area(self, unit: any, action: str) -> None:
        """Атака по площади"""
        if unit in self.new_battle.player1.units:
            side = self.player_side
        else:
            side = self.enemy_side

        if side == FRONT:
            gif_slot = self.ui.gifPlayerAreaAttack
        else:
            gif_slot = self.ui.gifEnemyAreaAttack

        gif = QMovie(os.path.join(
            action,
            f"{side}{unit.name}.gif"))

        gif_slot.setMovie(gif)
        gif.start()

    def show_poisoned_unit(self):
        """Если ходящий юнит отравлен и т.д."""
        curr_unit = self.new_battle.current_unit
        dot_units = self.new_battle.dotted_units

        if curr_unit in dot_units and \
                curr_unit.dotted:
            if not dot_units[curr_unit].get('Снижение инициативы') \
                    and not dot_units[curr_unit].get('Снижение урона'):
                # прорисовка модели атакованного юнита
                self.show_attacked(curr_unit)

                # прорисовка тени атакованного юнита
                self.show_shadow_attacked(curr_unit)

                # обновляем здоровье
                self._update_all_unit_health()

            # уменьшаем кол-во раундов
            curr_unit.dotted -= 1

            # если отравленный юнит погиб, удаляем его
            if curr_unit.curr_health == 0:
                self.removing_dead_unit(curr_unit)

                if curr_unit in dot_units:
                    dot_units.pop(curr_unit)

                # прорисовка модели атакованного юнита
                self.show_attacked(curr_unit)

                self.new_battle.alive_getting_experience()

                # битва еще не закончена
                if not self.new_battle.battle_is_over:
                    # self._update_all_unit_health()
                    self.are_units_in_round()

                # битва закончена
                else:
                    self.show_no_frames(self.unit_circles_dict, show_no_circle)
                    self.show_no_frames(self.dung_circles_dict, show_no_circle)
                    self.show_lvl_up_animations()

                self._update_all_unit_health()

            if curr_unit.dotted == 0 and curr_unit in dot_units:
                if curr_unit in self.new_battle.player1.units:
                    pl_database = self.db_table
                else:
                    pl_database = main_db.CurrentDungeon

                curr_unit.off_initiative(pl_database)
                dot_units.pop(curr_unit)

        # показать иконки эффектов
        self.define_dotted_units()

    def are_units_in_round(self) -> None:
        """Проверка на наличие юнитов в раунде"""
        if self.new_battle.current_unit in self.new_battle.units_in_round:
            self.new_battle.units_in_round.remove(
                self.new_battle.current_unit)

        # есть не ходившие юниты в текущем раунде
        if self.new_battle.units_in_round:
            self.new_battle.next_turn()

            # если ходящий юнит отравлен и т.д.
            self.show_poisoned_unit()

        # есть юниты, ожидающие лучшего момента
        elif self.new_battle.waiting_units:
            if self.new_battle.current_unit in self.new_battle.waiting_units:
                # кнопка ожидания недоступна
                ui_lock(self.ui.pushButtonWaiting)

            self.new_battle.waiting_round()
            self.new_battle.next_turn()

            # если ходящий юнит отравлен и т.д.
            self.show_poisoned_unit()

        else:
            # новый раунд
            self.new_battle.new_round()
            # кнопка ожидания снова доступна
            ui_unlock(self.ui.pushButtonWaiting)
            # следующий ход
            self.new_battle.next_turn()

            # если ходящий юнит отравлен и т.д.
            self.show_poisoned_unit()

        # битва еще не закончена
        if not self.new_battle.battle_is_over:
            # Показать рамки
            self.show_target_frame()
            self.show_frame_attacker()
            self.show_circle_attacker()

        self.check_ai()

    def check_ai(self):
        """Проверка, если ходит ИИ, включаем автобой"""
        if self.new_battle.current_player.name == 'Computer':
            # блокировка кнопок
            self.lock_buttons_for_ai()

            timer = QTimer(self)
            timer.singleShot(700, self.autofight)
            del timer
        else:
            # Разблокировка кнопок
            self.unlock_buttons_for_player()

    def lock_buttons_for_ai(self):
        """Блокировка кнопок на ходе компьютера"""
        ui_lock(self.ui.pushButtonAutoFight)
        ui_lock(self.ui.pushButtonDefence)
        ui_lock(self.ui.pushButtonWaiting)

        if self.player_side == FRONT:
            ui_lock(self.ui.pushButtonSlot1)
            ui_lock(self.ui.pushButtonSlot2)
            ui_lock(self.ui.pushButtonSlot3)
            ui_lock(self.ui.pushButtonSlot4)
            ui_lock(self.ui.pushButtonSlot5)
            ui_lock(self.ui.pushButtonSlot6)
        else:
            ui_lock(self.ui.pushButtonEnemySlot1)
            ui_lock(self.ui.pushButtonEnemySlot2)
            ui_lock(self.ui.pushButtonEnemySlot3)
            ui_lock(self.ui.pushButtonEnemySlot4)
            ui_lock(self.ui.pushButtonEnemySlot5)
            ui_lock(self.ui.pushButtonEnemySlot6)

    def unlock_buttons_for_player(self):
        """Разблокировка кнопок на ходе игрока"""
        ui_unlock(self.ui.pushButtonAutoFight)
        ui_unlock(self.ui.pushButtonDefence)
        ui_unlock(self.ui.pushButtonWaiting)

        if self.player_side == FRONT:
            ui_unlock(self.ui.pushButtonSlot1)
            ui_unlock(self.ui.pushButtonSlot2)
            ui_unlock(self.ui.pushButtonSlot3)
            ui_unlock(self.ui.pushButtonSlot4)
            ui_unlock(self.ui.pushButtonSlot5)
            ui_unlock(self.ui.pushButtonSlot6)
        else:
            ui_unlock(self.ui.pushButtonEnemySlot1)
            ui_unlock(self.ui.pushButtonEnemySlot2)
            ui_unlock(self.ui.pushButtonEnemySlot3)
            ui_unlock(self.ui.pushButtonEnemySlot4)
            ui_unlock(self.ui.pushButtonEnemySlot5)
            ui_unlock(self.ui.pushButtonEnemySlot6)

    def unit_defence(self) -> None:
        """Встать в Защиту выбранным юнитом"""
        self.new_battle.current_unit.defence()
        self.update_log()
        self.show_no_damaged()
        self.clear_frames_circles()
        self.are_units_in_round()

        self.update_log()

    def unit_waiting(self) -> None:
        """Ожидать выбранным юнитом"""
        self.new_battle.current_unit.waiting()

        self.update_log()
        self.show_no_damaged()
        self.clear_frames_circles()

        self.new_battle.waiting_units.append(self.new_battle.current_unit)

        self.are_units_in_round()

        self.update_log()

    def show_attack_and_attacked(self) -> None:
        """Анимация атакующей и атакованной стороны"""
        self.update_log()

        if self.new_battle.units_in_round:
            self.show_no_frames(self.unit_circles_dict, show_no_circle)
            self.show_no_frames(self.dung_circles_dict, show_no_circle)

            self.who_attack()

            if 'жизни' in self.new_battle.current_unit.attack_type:
                self.worker = Thread(False)
            else:
                self.worker = Thread(True)

            self.worker.dataThread.connect(self.show_all_attacked)
            self.worker.start()

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
                self.new_battle.current_unit)

        self.clear_frames_circles()

        # Очистка целей, чтобы в конце боя нельзя было атаковать повторно
        self.new_battle.target_slots = []

        # битва еще не закончена
        if not self.new_battle.battle_is_over:
            if 'жизни' in self.new_battle.current_unit.attack_type:
                self.show_life_drain()

            self._update_all_unit_health()

            self.are_units_in_round()

        # битва закончена
        else:
            self.show_no_frames(self.unit_circles_dict, show_no_circle)
            self.show_no_frames(self.dung_circles_dict, show_no_circle)

            self.show_lvl_up_animations()

            self.parent.reset()
            if self.parent.name == 'CampaignWindow':
                self.parent.main.player_list_update()
                self.parent.main.player_slots_update()

            self.worker = Thread(False)
            self.worker.dataThread.connect(self.unit_gifs_update)
            self.worker.start()

            if not self.new_battle.player1.slots:
                self.show_need_upgrade_effect(self.dung_damaged_dict,
                                      self.new_battle.player2)
            if not self.new_battle.player2.slots:
                self.show_need_upgrade_effect(self.unit_damaged_dict,
                                      self.new_battle.player1)

        self.update_log()
        self.new_battle.autofight = False

    @staticmethod
    def add_gold(mission_number: any) -> None:
        """Добавление золота за победу"""
        player_gold = main_db.get_gold(
            main_db.current_player.name,
            main_db.current_faction)

        changed_gold = player_gold + GOLD_GRADATION[mission_number]

        # обновление золота в базе
        main_db.update_gold(
            main_db.current_player.name,
            main_db.current_faction,
            changed_gold)

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
        # если юниты игрока1 мертвы
        if not self.new_battle.player1.slots:
            self.add_upgraded_units(
                self.new_battle.player2,
                main_db.Player2Units,
                self.enemy_side,
                self.en_slots_eff_dict
            )

        # если юниты игрока2 мертвы
        elif not self.new_battle.player2.slots:

            self.add_upgraded_units(
                self.new_battle.player1,
                self.db_table,
                self.player_side,
                self.pl_slots_eff_dict
            )

            if self.new_battle.player2.name == 'Computer':
                mission_number = self.dungeon.split('_')[-1]
                self.add_gold(mission_number)

                # после каждой победы день увеличивается на 1
                main_db.campaign_day += 1
                main_db.already_built = 0

                # победили босса - повысился уровень кампании, день + 1
                if '15' in self.dungeon and main_db.campaign_level != 5:
                    main_db.update_session(
                        main_db.game_session_id,
                        main_db.campaign_level + 1,
                        0,
                        0,
                        main_db.campaign_day,
                        main_db.already_built)

                    main_db.campaign_level += 1
                # иначе просто прибавляем день
                else:
                    main_db.update_session(
                        main_db.game_session_id,
                        main_db.campaign_level,
                        mission_number,
                        self.parent.curr_mission,
                        main_db.campaign_day,
                        main_db.already_built)

    def show_gif_side(self,
                      unit: any,
                      gif_slot: QtWidgets.QLabel,
                      action: str,
                      side: str) -> None:
        """Обновление GIF в слоте"""
        if unit is None:
            gif = QMovie(os.path.join(
                UNIT_STAND,
                f"{side}/empty.gif"))

        # анимация смерти
        elif unit.curr_health == 0:
            if 'neutral' in unit.subrace:
                gif = QMovie(os.path.join(
                    action,
                    f"{side}/neutral.gif"))
            else:
                gif = QMovie(os.path.join(
                    action,
                    f"{side}/{unit.subrace}.gif"))

        # if unit.curr_health == 0:
        #     gif = QMovie(os.path.join(COMMON, "skull.png"))

        # анимация действия
        else:
            gif = QMovie(os.path.join(
                action,
                f"{side}{unit.name}.gif"))

        gif.setSpeed(self.speed)
        gif_slot.setMovie(gif)
        gif.start()

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

        elif unit in self.new_battle.player1.units:
            slots_dict = slots_dict1

        elif unit in self.new_battle.player2.units:
            side = self.enemy_side
            slots_dict = slots_dict2

        self.show_gif_side(
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
        elif unit in self.new_battle.player1.units:
            func(slots_dict1[unit.slot])
        elif unit in self.new_battle.player2.units:
            func(slots_dict2[unit.slot])

    def show_circles_by_side(self,
                             unit: Unit,
                             slots_dict1: dict,
                             slots_dict2: dict,
                             func: Callable) -> None:
        """Отображает круги в зависимости от стороны и действия"""
        if unit is None:
            pass
        elif unit in self.new_battle.player1.units:
            func(unit,
                 slots_dict1[unit.slot])
        elif unit in self.new_battle.player2.units:
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
        # QtCore.QTimer.singleShot(3000, lambda: print(1))
        self.show_frames_by_side(self.new_battle.current_unit,
                                 self.unit_icons_dict,
                                 self.dung_icons_dict,
                                 show_green_frame)

    def show_circle_attacker(self) -> None:
        """Прорисовка круга под активным юнитом"""
        self.show_circles_by_side(self.new_battle.current_unit,
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
        curr_unit = self.new_battle.current_unit

        for target_slot in self.new_battle.targets:
            target = self.get_curr_target(target_slot)

            # цель и текущий юнит принадлежат одному игроку
            if target in self.new_battle.target_player.units and \
                    curr_unit in self.new_battle.target_player.units:

                if curr_unit.attack_type in (*ALCHEMIST_LIST, *HEAL_LIST):
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

    def show_no_damaged(self) -> None:
        """Метод скрывающий нанесенный урон"""
        for icon_slot in self.unit_damaged_dict.values():
            show_no_damage(icon_slot)

        for icon_slot in self.dung_damaged_dict.values():
            show_no_damage(icon_slot)

    def show_shadow_attacked(self, target: Unit) -> None:
        """Прорисовка тени атакованного юнита"""
        self.show_gif_by_side(target,
                              UNIT_SHADOW_ATTACKED,
                              self.pl_slots_shad_dict,
                              self.en_slots_shad_dict)

    def get_curr_target(self, target_slot: int) -> Unit:
        """Получение текущей цели"""
        if self.new_battle.target_player == self.new_battle.player2:
            curr_target = self._unit_by_slot_and_side(
                target_slot, self.enemy_side)
        else:
            curr_target = self._unit_by_slot_and_side(
                target_slot, self.player_side)
        return curr_target

    def show_life_drain(self) -> None:
        """Прорисовка анимации высасывания жизни"""
        slots_dict = {}

        if self.new_battle.current_unit in self.new_battle.player1.units:
            slots_dict = self.pl_slots_eff_dict

        elif self.new_battle.current_unit in self.new_battle.player2.units:
            slots_dict = self.en_slots_eff_dict

        unit_gif = "life_drain.gif"
        gif = QMovie(os.path.join(
            BATTLE_ANIM,
            unit_gif))

        slots_dict[self.new_battle.current_unit.slot].setMovie(gif)
        gif.start()

    def who_attack(self) -> None:
        """Метод обновляющий анимацию атакующего юнита"""
        # получение текущего юнита
        curr_unit = self.new_battle.current_unit

        # очищает иконки атакованных юнитов
        self.show_no_damaged()

        # прорисовка модели атакующего юнита
        self.show_attacker(curr_unit)

        # прорисовка эффектов атакующего юнита
        self.show_attacker_eff(curr_unit)

        # прорисовка тени атакующего юнита
        self.show_shadow_attacker(curr_unit)

        # прорисовка атаки по области для атакующего юнита
        if curr_unit.attack_purpose == 6:
            self.show_splash_area(
                curr_unit,
                UNIT_EFFECTS_AREA)

    def who_attacked(self, target_slot: int, current_unit: Unit) -> None:
        """Метод обновляющий анимацию атакованного юнита"""
        if target_slot is None:
            return

        # получение текущей цели
        curr_target = self.get_curr_target(target_slot)

        if curr_target is None:
            pass

        # цель и текущий юнит принадлежат одному игроку
        elif curr_target in self.new_battle.target_player.units and \
                self.new_battle.current_unit in self.new_battle.target_player.units:

            if self.new_battle.target_player == self.new_battle.player2:
                self.animate_action_side(
                    self.en_slots_dict,
                    UNIT_STAND,
                    self.enemy_side)

                # прорисовка эффекта на атакованном вражеском юните
                self.show_gif_side(
                    current_unit,
                    self.en_slots_attacked_eff_dict[curr_target.slot],
                    UNIT_EFFECTS_TARGET,
                    self.enemy_side)
            else:
                self.animate_action_side(
                    self.pl_slots_dict,
                    UNIT_STAND,
                    self.player_side)

                # прорисовка эффекта на атакованном юните игрока
                self.show_gif_side(
                    current_unit,
                    self.pl_slots_attacked_eff_dict[curr_target.slot],
                    UNIT_EFFECTS_TARGET,
                    self.player_side)

        else:
            # прорисовка модели атакованного юнита
            self.show_attacked(curr_target)

            # прорисовка тени атакованного юнита
            self.show_shadow_attacked(curr_target)

            if self.new_battle.target_player == self.new_battle.player2:
                # прорисовка эффекта на атакованном вражеском юните
                self.show_gif_side(
                    current_unit,
                    self.en_slots_attacked_eff_dict[curr_target.slot],
                    UNIT_EFFECTS_TARGET,
                    self.enemy_side)

                # Показывает атакованный вражеский юнит
                show_damage(
                    self.dung_damaged_dict[curr_target.slot])

            else:
                # прорисовка эффекта на атакованном юните игрока
                self.show_gif_side(
                    current_unit,
                    self.pl_slots_attacked_eff_dict[curr_target.slot],
                    UNIT_EFFECTS_TARGET,
                    self.player_side)

                # Показывает атакованный юнит игрока
                show_damage(
                    self.unit_damaged_dict[curr_target.slot])

        # если атакованный юнит погиб, удаляем его
        if curr_target.curr_health == 0:
            self.removing_dead_unit(curr_target)

    def removing_dead_unit(self, target):
        """Удаление погибшего юнита из битвы"""
        if target in self.new_battle.units_deque:
            self.new_battle.units_deque.remove(
                target)
        if target in self.new_battle.units_in_round:
            self.new_battle.units_in_round.remove(
                target)
        if target in self.new_battle.waiting_units:
            self.new_battle.waiting_units.remove(
                target)

    def show_dot_effect(self, unit, dot_type, icons_dict):
        """Показывает действующий отрицательный эффект на юните"""
        if unit.dotted and self.new_battle.dotted_units[unit].get(dot_type):
            rounds = self.new_battle.dotted_units[unit][dot_type][1]
            if rounds:
                show_dot_icon(
                    icons_dict[unit.slot], dot_type)
            else:
                show_dot_icon(
                    icons_dict[unit.slot], 'spare_dot')

    def show_might_effect(self, unit, dot_type, icons_dict):
        """Показывает действующий положительный эффект на юните"""
        if self.new_battle.boosted_units.get(unit):
            show_dot_icon(
                icons_dict[unit.slot], dot_type)

    @staticmethod
    def show_need_upgrade_effect(icons_dict, player):
        """Показывает ограничение в апгрейде на юните"""
        for unit in player.units:
            if unit.exp == 'Максимальный':
                pass
            elif unit.curr_exp == unit.exp - 1:
                show_dot_icon(
                    icons_dict[unit.slot], 'waiting_next')

    def define_priority_effect(self, unit, icons_dict):
        """Отобразить один приоритетный эффект"""
        self.show_dot_effect(unit, 'Увеличение урона', icons_dict)
        self.show_dot_effect(unit, 'Снижение урона', icons_dict)
        self.show_dot_effect(unit, 'Снижение инициативы', icons_dict)
        self.show_dot_effect(unit, 'Яд', icons_dict)
        self.show_dot_effect(unit, 'Ожог', icons_dict)
        self.show_dot_effect(unit, 'Обморожение', icons_dict)
        self.show_dot_effect(unit, 'Паралич', icons_dict)
        self.show_dot_effect(unit, 'Окаменение', icons_dict)

    def define_dotted_units(self):
        """Определяет юнитов с наложенными эффектами"""
        for unit in self.new_battle.player1.units:
            if unit in self.new_battle.dotted_units:
                # Показывает эффект на юните игрока
                self.define_priority_effect(unit, self.unit_damaged_dict)

            elif unit in self.new_battle.boosted_units:
                self.show_might_effect(
                    unit, 'Увеличение урона', self.unit_damaged_dict)

        for unit in self.new_battle.player2.units:
            if unit in self.new_battle.dotted_units:
                # Показывает эффект на вражеском юните
                self.define_priority_effect(unit, self.dung_damaged_dict)

            elif unit in self.new_battle.boosted_units:
                self.show_might_effect(
                    unit, 'Увеличение урона', self.dung_damaged_dict)

    def update_icons(self,
                     icons_dict: dict,
                     buttons_dict: dict,
                     side: str) -> None:
        """Обновление иконок и кнопок юнитов"""
        for num, icon_slot in icons_dict.items():
            unit = self._unit_by_slot_and_side(num, side)
            self._slot_update(
                unit,
                icon_slot,
                side)

        for num, button_slot in buttons_dict.items():
            unit = self._unit_by_slot_and_side(num, side)
            self._button_update(
                unit,
                button_slot,
                side)

    def set_unit_icons(self) -> None:
        """Заполнение временных словарей иконок и кнопок юнитов"""
        # Иконки юнитов FRONT стороны
        self.append_front_icons()

        # Кнопки юнитов FRONT стороны
        self.append_front_buttons()

        # Иконки атакованных юнитов FRONT стороны
        self.append_front_damaged()

        # Иконки кругов FRONT стороны
        self.append_front_circles()

        # Иконки юнитов REAR стороны
        self.append_rear_icons()

        # Кнопки юнитов REAR стороны
        self.append_rear_buttons()

        # Иконки атакованных юнитов REAR стороны
        self.append_rear_damaged()

        # Иконки кругов REAR стороны
        self.append_rear_circles()

    def unit_icons_update(self) -> None:
        """Метод обновляющий иконки и кнопки юнитов игроков"""
        if self.player_side == FRONT:
            self.set_unit_icons_player1()

            self.update_icons(self.unit_icons_dict,
                              self.unit_buttons_dict,
                              FRONT)
            self.update_icons(self.dung_icons_dict,
                              self.dung_buttons_dict,
                              REAR)

        else:
            self.set_unit_icons_player2()

            self.update_icons(self.unit_icons_dict,
                              self.unit_buttons_dict,
                              REAR)
            self.update_icons(self.dung_icons_dict,
                              self.dung_buttons_dict,
                              FRONT)

    def set_unit_icons_player1(self) -> None:
        """Заполнение словарей иконок и кнопок юнитов FRONT - игрок 1"""
        self.unit_icons_dict = self.front_icons_dict
        self.unit_damaged_dict = self.front_damaged_dict
        self.unit_buttons_dict = self.front_buttons_dict
        self.unit_circles_dict = self.front_circles_dict
        # self.unit_field_buttons_dict = self.front_field_buttons_dict

        self.dung_icons_dict = self.rear_icons_dict
        self.dung_damaged_dict = self.rear_damaged_dict
        self.dung_buttons_dict = self.rear_buttons_dict
        self.dung_circles_dict = self.rear_circles_dict
        # self.dung_field_buttons_dict = self.rear_field_buttons_dict

    def set_unit_icons_player2(self) -> None:
        """Заполнение словарей иконок и кнопок юнитов FRONT - игрок 2"""
        self.dung_icons_dict = self.front_icons_dict
        self.dung_damaged_dict = self.front_damaged_dict
        self.dung_buttons_dict = self.front_buttons_dict
        self.dung_circles_dict = self.front_circles_dict
        # self.dung_field_buttons_dict = self.front_field_buttons_dict

        self.unit_icons_dict = self.rear_icons_dict
        self.unit_damaged_dict = self.rear_damaged_dict
        self.unit_buttons_dict = self.rear_buttons_dict
        self.unit_circles_dict = self.rear_circles_dict
        # self.unit_field_buttons_dict = self.rear_field_buttons_dict

    def animate_action_side(self,
                            slots_dict: dict,
                            unit_action: str,
                            side: str) -> None:
        """Анимации юнитов игрока"""
        for num, gif_slot in slots_dict.items():
            self.show_gif_side(
                self._unit_by_slot_and_side(num, side),
                gif_slot,
                unit_action,
                side)

    def unit_gifs_update(self) -> None:
        """Метод обновляющий анимацию юнитов"""
        # прорисовка модели бездействующего юнита игрока
        self.animate_action_side(
            self.pl_slots_dict,
            UNIT_STAND,
            self.player_side)

        # прорисовка тени бездействующего юнита игрока
        self.animate_action_side(
            self.pl_slots_shad_dict,
            UNIT_SHADOW_STAND,
            self.player_side)

        # прорисовка модели бездействующего юнита врага
        self.animate_action_side(
            self.en_slots_dict,
            UNIT_STAND,
            self.enemy_side)

        # прорисовка тени бездействующего юнита врага
        self.animate_action_side(
            self.en_slots_shad_dict,
            UNIT_SHADOW_STAND,
            self.enemy_side)

        self.show_circle_attacker()
        self._update_all_unit_health()
        self.unit_icons_update()

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

    def _button_update(self,
                       unit: Unit,
                       button: QtWidgets.QPushButton,
                       side: str) -> None:
        """Установка размера кнопки на иконке"""
        self._set_size_by_unit(unit, button, side)

        self.hbox.addWidget(button)
        self.setLayout(self.hbox)

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
        # self.unit_gifs_update()
        target = self._unit_by_slot_and_side(slot, side)
        curr_unit = self.new_battle.current_unit

        # невозможность атаковать своих
        if target is not None:
            if target not in self.new_battle.current_player.units \
                    and curr_unit.attack_type \
                    not in [*HEAL_LIST, *ALCHEMIST_LIST]:

                self.new_battle.player_attack(target)
                self.show_attack_and_attacked()

            # если текущий юнит лекарь - можно выбрать целью свой юнит
            elif target in self.new_battle.current_player.units \
                    and curr_unit.attack_type \
                    in [*HEAL_LIST, *ALCHEMIST_LIST]:

                self.new_battle.player_attack(target)
                self.show_attack_and_attacked()

    def _attack_player_slot1(self) -> None:
        """Атаковать юнита игрока в слоте 1"""
        if 1 in self.new_battle.target_slots:
            self.attack_enemy_by_slot(1, FRONT)

    def _attack_player_slot2(self) -> None:
        """Атаковать юнита игрока в слоте 2"""
        if 2 in self.new_battle.target_slots:
            self.attack_enemy_by_slot(2, FRONT)

    def _attack_player_slot3(self) -> None:
        """Атаковать юнита игрока в слоте 3"""
        if 3 in self.new_battle.target_slots:
            self.attack_enemy_by_slot(3, FRONT)

    def _attack_player_slot4(self) -> None:
        """Атаковать юнита игрока в слоте 4"""
        if 4 in self.new_battle.target_slots:
            self.attack_enemy_by_slot(4, FRONT)

    def _attack_player_slot5(self) -> None:
        """Атаковать юнита игрока в слоте 5"""
        if 5 in self.new_battle.target_slots:
            self.attack_enemy_by_slot(5, FRONT)

    def _attack_player_slot6(self) -> None:
        """Атаковать юнита игрока в слоте 6"""
        if 6 in self.new_battle.target_slots:
            self.attack_enemy_by_slot(6, FRONT)

    def _attack_enemy_slot1(self) -> None:
        """Атаковать вражеского юнита в слоте 1"""
        if 1 in self.new_battle.target_slots:
            self.attack_enemy_by_slot(1, REAR)

    def _attack_enemy_slot2(self) -> None:
        """Атаковать вражеского юнита в слоте 2"""
        if 2 in self.new_battle.target_slots:
            self.attack_enemy_by_slot(2, REAR)

    def _attack_enemy_slot3(self) -> None:
        """Атаковать вражеского юнита в слоте 3"""
        if 3 in self.new_battle.target_slots:
            self.attack_enemy_by_slot(3, REAR)

    def _attack_enemy_slot4(self) -> None:
        """Атаковать вражеского юнита в слоте 4"""
        if 4 in self.new_battle.target_slots:
            self.attack_enemy_by_slot(4, REAR)

    def _attack_enemy_slot5(self) -> None:
        """Атаковать вражеского юнита в слоте 5"""
        if 5 in self.new_battle.target_slots:
            self.attack_enemy_by_slot(5, REAR)

    def _attack_enemy_slot6(self) -> None:
        """Атаковать вражеского юнита в слоте 6"""
        if 6 in self.new_battle.target_slots:
            self.attack_enemy_by_slot(6, REAR)

    def _slot1_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 1)."""
        unit = self._unit_by_slot_and_side(1, FRONT)
        self._slot_detailed(unit, UnitDialog)

    def _slot2_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 2)."""
        unit = self._unit_by_slot_and_side(2, FRONT)
        self._slot_detailed(unit, UnitDialog)

    def _slot3_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 3)."""
        unit = self._unit_by_slot_and_side(3, FRONT)
        self._slot_detailed(unit, UnitDialog)

    def _slot4_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 4)."""
        unit = self._unit_by_slot_and_side(4, FRONT)
        self._slot_detailed(unit, UnitDialog)

    def _slot5_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 5)."""
        unit = self._unit_by_slot_and_side(5, FRONT)
        self._slot_detailed(unit, UnitDialog)

    def _slot6_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 6)."""
        unit = self._unit_by_slot_and_side(6, FRONT)
        self._slot_detailed(unit, UnitDialog)

    def _enemy_slot1_detailed(self) -> None:
        """Метод создающий окно юнита (слот 1)."""
        unit = self._unit_by_slot_and_side(1, REAR)
        self._slot_detailed(unit, UnitDialog)

    def _enemy_slot2_detailed(self) -> None:
        """Метод создающий окно юнита (слот 2)."""
        unit = self._unit_by_slot_and_side(2, REAR)
        self._slot_detailed(unit, UnitDialog)

    def _enemy_slot3_detailed(self) -> None:
        """Метод создающий окно юнита (слот 3)."""
        unit = self._unit_by_slot_and_side(3, REAR)
        self._slot_detailed(unit, UnitDialog)

    def _enemy_slot4_detailed(self) -> None:
        """Метод создающий окно юнита (слот 4)."""
        unit = self._unit_by_slot_and_side(4, REAR)
        self._slot_detailed(unit, UnitDialog)

    def _enemy_slot5_detailed(self) -> None:
        """Метод создающий окно юнита (слот 5)."""
        unit = self._unit_by_slot_and_side(5, REAR)
        self._slot_detailed(unit, UnitDialog)

    def _enemy_slot6_detailed(self) -> None:
        """Метод создающий окно юнита (слот 6)."""
        unit = self._unit_by_slot_and_side(6, REAR)
        self._slot_detailed(unit, UnitDialog)

    def _unit_by_slot_and_side(self, slot: int, side: str) -> Optional[Unit]:
        """Метод получающий юнита игрока по слоту и стороне."""
        if side == self.player_side:
            for unit in self.new_battle.player1.units:
                if unit.slot == slot:
                    return unit
        else:
            for unit in self.new_battle.player2.units:
                if unit.slot == slot:
                    return unit
        return None
