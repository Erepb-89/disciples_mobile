"""Окно битвы"""

import os.path
import random

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QMovie, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from battle import Battle
from client_dir.fight_form import Ui_FightWindow
from client_dir.settings import UNIT_STAND, UNIT_ATTACK, \
    UNIT_ATTACKED, UNIT_EFFECTS_ATTACK, BATTLE_GROUND, FRONT, REAR, \
    COMMON, BATTLE_GROUNDS, UNIT_SHADOW_ATTACK, UNIT_SHADOW_STAND, \
    UNIT_SHADOW_ATTACKED, UNIT_EFFECTS_AREA, UNIT_EFFECTS_TARGET, \
    RIGHT_ICONS, LEFT_ICONS, SCREEN_RECT, PANEL_RECT, BATTLE_LOG
from client_dir.ui_functions import get_unit_image
from client_dir.unit_dialog import UnitDialog
from units_dir.buildings import FACTIONS


class Thread(QThread):
    """Класс потока"""
    dataThread = pyqtSignal(str)

    def __init__(self, attacker):
        QThread.__init__(self)
        self.attacker = attacker

    def run(self):
        if self.attacker is True:
            i = 10_000_000
        else:
            i = 12_000_000

        while i > 1:
            i -= 1
            if i == 5_000:
                self.dataThread.emit("Finished")


class FightWindow(QMainWindow):
    """
    Класс - окно выбора фракции.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла fight_menu_form.py
    """

    def __init__(self, database, dungeon):
        super().__init__()
        # основные переменные
        self.database = database
        self.new_battle = Battle(self.database, dungeon)
        self.player_side = FRONT
        self.enemy_side = REAR
        self.target_is_enemy = False
        self.target_is_friend = False

        # временные словари иконок и кнопок на них
        self.front_icons_dict = {}
        self.front_damaged_dict = {}
        self.front_buttons_dict = {}

        self.rear_icons_dict = {}
        self.rear_damaged_dict = {}
        self.rear_buttons_dict = {}

        # словари иконок и кнопок на них
        self.unit_icons_dict = {}
        self.unit_damaged_dict = {}
        self.unit_buttons_dict = {}

        self.dung_icons_dict = {}
        self.dung_damaged_dict = {}
        self.dung_buttons_dict = {}

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

        self.InitUI()

        with open(BATTLE_LOG, 'w', encoding='utf-8') as log:
            log.write(f'Ходит: {self.new_battle.current_unit.name}\n')
            log.write("Новая битва\n")
        self.update_log()

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""

        self.ui = Ui_FightWindow()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)
        self.update_bg()
        self.update_bp()

        self.ui.leftIcons.setPixmap(
            QPixmap(LEFT_ICONS))
        self.ui.rightIcons.setPixmap(
            QPixmap(RIGHT_ICONS))

        self.ui.pushButtonBack.clicked.connect(self.back)

        self.ui.pushButtonSlot1.clicked.connect(
            self._slot1_detailed)
        self.ui.pushButtonSlot2.clicked.connect(
            self._slot2_detailed)
        self.ui.pushButtonSlot3.clicked.connect(
            self._slot3_detailed)
        self.ui.pushButtonSlot4.clicked.connect(
            self._slot4_detailed)
        self.ui.pushButtonSlot5.clicked.connect(
            self._slot5_detailed)
        self.ui.pushButtonSlot6.clicked.connect(
            self._slot6_detailed)

        self.ui.pushButtonEnemySlot1.clicked.connect(
            self._enemy_slot1_detailed)
        self.ui.pushButtonEnemySlot2.clicked.connect(
            self._enemy_slot2_detailed)
        self.ui.pushButtonEnemySlot3.clicked.connect(
            self._enemy_slot3_detailed)
        self.ui.pushButtonEnemySlot4.clicked.connect(
            self._enemy_slot4_detailed)
        self.ui.pushButtonEnemySlot5.clicked.connect(
            self._enemy_slot5_detailed)
        self.ui.pushButtonEnemySlot6.clicked.connect(
            self._enemy_slot6_detailed)

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

        self.unit_gifs_update()
        self.unit_icons_update()
        self._update_all_unit_health()

        self.ui.battleLog.setStyleSheet("background-color: rgb(65, 3, 2)")

        self.enemy_dam_list = [
            self.ui.damEnemySlot_1,
            self.ui.damEnemySlot_2,
            self.ui.damEnemySlot_3,
            self.ui.damEnemySlot_4,
            self.ui.damEnemySlot_5,
            self.ui.damEnemySlot_6,
        ]

        self.show()
        self.show_frame_attacker()
        self.update_log()
        # self.show_frame_attacked()

    def update_bg(self):
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

    def update_bp(self):
        """Обновление панели битвы"""
        fight_bp = self.ui.batPanel
        fight_bp.setPixmap(
            QPixmap(
                os.path.join(
                    COMMON, 'battle_panel.png')))
        fight_bp.setGeometry(PANEL_RECT)
        self.hbox.addWidget(fight_bp)
        self.setLayout(self.hbox)

    def update_log(self):
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

    def back(self):
        """Кнопка возврата"""
        self.close()

    def change_side(self):
        """Смена сторон"""
        if self.player_side == FRONT:
            self.player_side = REAR
            self.enemy_side = FRONT

            self.set_front_gif_player2_dict()
        else:
            # self.set_front_gif_player1()
            self.player_side = FRONT
            self.enemy_side = REAR

            self.set_front_gif_player1_dict()

        self.unit_gifs_update()
        self._update_all_unit_health()
        self.unit_icons_update()
        self.show_no_damaged()
        self.show_no_frames(self.unit_icons_dict, self.show_no_frame)
        self.show_no_frames(self.dung_icons_dict, self.show_no_frame)
        self.show_frame_attacker()

    def set_front_gif_player1_dict(self):
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

    def set_front_gif_player2_dict(self):
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

    def append_front(self):
        """Основные анимационные GIF юнитов FRONT стороны"""
        self.front_slots_dict = {
            1: self.ui.gifPlayerSlot_1,
            2: self.ui.gifPlayerSlot_2,
            3: self.ui.gifPlayerSlot_3,
            4: self.ui.gifPlayerSlot_4,
            5: self.ui.gifPlayerSlot_5,
            6: self.ui.gifPlayerSlot_6,
        }

    def append_front_shadows(self):
        """Анимационные GIF теней юнитов FRONT стороны"""
        self.front_slots_shad_dict = {
            1: self.ui.gifShadSlot_1,
            2: self.ui.gifShadSlot_2,
            3: self.ui.gifShadSlot_3,
            4: self.ui.gifShadSlot_4,
            5: self.ui.gifShadSlot_5,
            6: self.ui.gifShadSlot_6,
        }

    def append_front_effects(self):
        """Анимационные GIF эффектов атакующий юнитов FRONT стороны"""
        self.front_slots_eff_dict = {
            1: self.ui.gifEffSlot_1,
            2: self.ui.gifEffSlot_2,
            3: self.ui.gifEffSlot_3,
            4: self.ui.gifEffSlot_4,
            5: self.ui.gifEffSlot_5,
            6: self.ui.gifEffSlot_6,
        }

    def append_front_attacked_eff(self):
        """Анимационные GIF эффектов атакованных юнитов FRONT стороны"""
        self.front_slots_attacked_eff_dict = {
            1: self.ui.gifPlayerAttEffSlot_1,
            2: self.ui.gifPlayerAttEffSlot_2,
            3: self.ui.gifPlayerAttEffSlot_3,
            4: self.ui.gifPlayerAttEffSlot_4,
            5: self.ui.gifPlayerAttEffSlot_5,
            6: self.ui.gifPlayerAttEffSlot_6,
        }

    def append_front_hp(self):
        """GIF очков здоровья юнитов FRONT стороны"""
        self.front_hp_slots_dict = {
            1: self.ui.hpSlot1,
            2: self.ui.hpSlot2,
            3: self.ui.hpSlot3,
            4: self.ui.hpSlot4,
            5: self.ui.hpSlot5,
            6: self.ui.hpSlot6,
        }

    def append_rear(self):
        """Анимационные GIF теней юнитов REAR стороны"""
        self.rear_slots_dict = {
            1: self.ui.gifEnemySlot_1,
            2: self.ui.gifEnemySlot_2,
            3: self.ui.gifEnemySlot_3,
            4: self.ui.gifEnemySlot_4,
            5: self.ui.gifEnemySlot_5,
            6: self.ui.gifEnemySlot_6,
        }

    def append_rear_shadows(self):
        """Анимационные GIF теней юнитов REAR стороны"""
        self.rear_slots_shad_dict = {
            1: self.ui.gifEnemyShadSlot_1,
            2: self.ui.gifEnemyShadSlot_2,
            3: self.ui.gifEnemyShadSlot_3,
            4: self.ui.gifEnemyShadSlot_4,
            5: self.ui.gifEnemyShadSlot_5,
            6: self.ui.gifEnemyShadSlot_6,
        }

    def append_rear_effects(self):
        """Анимационные GIF эффектов атакующий юнитов REAR стороны"""
        self.rear_slots_eff_dict = {
            1: self.ui.gifEnemyEffSlot_1,
            2: self.ui.gifEnemyEffSlot_2,
            3: self.ui.gifEnemyEffSlot_3,
            4: self.ui.gifEnemyEffSlot_4,
            5: self.ui.gifEnemyEffSlot_5,
            6: self.ui.gifEnemyEffSlot_6,
        }

    def append_rear_attacked_eff(self):
        """Анимационные GIF эффектов атакованных юнитов REAR стороны"""
        self.rear_slots_attacked_eff_dict = {
            1: self.ui.gifEnemyAttEffSlot_1,
            2: self.ui.gifEnemyAttEffSlot_2,
            3: self.ui.gifEnemyAttEffSlot_3,
            4: self.ui.gifEnemyAttEffSlot_4,
            5: self.ui.gifEnemyAttEffSlot_5,
            6: self.ui.gifEnemyAttEffSlot_6,
        }

    def append_rear_hp(self):
        """GIF очков здоровья юнитов REAR стороны"""
        self.rear_hp_slots_dict = {
            1: self.ui.enemyHPSlot1,
            2: self.ui.enemyHPSlot2,
            3: self.ui.enemyHPSlot3,
            4: self.ui.enemyHPSlot4,
            5: self.ui.enemyHPSlot5,
            6: self.ui.enemyHPSlot6,
        }

    def set_front_gif_player1(self):
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

    def append_front_icons(self):
        """Иконки юнитов FRONT стороны"""
        self.front_icons_dict = {
            1: self.ui.slot1,
            2: self.ui.slot2,
            3: self.ui.slot3,
            4: self.ui.slot4,
            5: self.ui.slot5,
            6: self.ui.slot6,
        }

    def append_front_buttons(self):
        """Кнопки юнитов FRONT стороны"""
        self.front_buttons_dict = {
            1: self.ui.pushButtonSlot1,
            2: self.ui.pushButtonSlot2,
            3: self.ui.pushButtonSlot3,
            4: self.ui.pushButtonSlot4,
            5: self.ui.pushButtonSlot5,
            6: self.ui.pushButtonSlot6,
        }

    def append_front_damaged(self):
        """Иконки атакованных юнитов FRONT стороны"""
        self.front_damaged_dict = {
            1: self.ui.damPlayerSlot_1,
            2: self.ui.damPlayerSlot_2,
            3: self.ui.damPlayerSlot_3,
            4: self.ui.damPlayerSlot_4,
            5: self.ui.damPlayerSlot_5,
            6: self.ui.damPlayerSlot_6,
        }

    def append_rear_icons(self):
        """GIF иконок юнитов REAR стороны"""
        self.rear_icons_dict = {
            1: self.ui.enemySlot1,
            2: self.ui.enemySlot2,
            3: self.ui.enemySlot3,
            4: self.ui.enemySlot4,
            5: self.ui.enemySlot5,
            6: self.ui.enemySlot6,
        }

    def append_rear_buttons(self):
        """GIF кнопок юнитов REAR стороны"""
        self.rear_buttons_dict = {
            1: self.ui.pushButtonEnemySlot1,
            2: self.ui.pushButtonEnemySlot2,
            3: self.ui.pushButtonEnemySlot3,
            4: self.ui.pushButtonEnemySlot4,
            5: self.ui.pushButtonEnemySlot5,
            6: self.ui.pushButtonEnemySlot5,
        }

    def append_rear_damaged(self):
        """Иконки атакованных юнитов REAR стороны"""
        self.rear_damaged_dict = {
            1: self.ui.damEnemySlot_1,
            2: self.ui.damEnemySlot_2,
            3: self.ui.damEnemySlot_3,
            4: self.ui.damEnemySlot_4,
            5: self.ui.damEnemySlot_5,
            6: self.ui.damEnemySlot_6,
        }

    def show_gif_side(self, unit, gif_slot, action, side):
        """Обновление GIF в слоте"""
        if unit is None:
            gif = QMovie(
                os.path.join(
                    UNIT_STAND,
                    f"{side}/empty.gif"))

        elif unit.curr_health == 0:
            unit_faction = self.get_unit_faction(unit)
            gif = QMovie(
                os.path.join(
                    action,
                    f"{side}/{unit_faction}.gif"))
            # unit_faction = self.get_unit_faction(unit)
            # print(unit_faction)
        # if unit.curr_health == 0:
        #     gif = QMovie(os.path.join(COMMON, "skull.png"))
        else:
            gif = QMovie(
                os.path.join(
                    action,
                    f"{side}{unit.name}.gif"))

        gif_slot.setMovie(gif)
        self._update_all_unit_health()
        gif.start()

    @staticmethod
    def show_no_frame(gif_slot):
        """Обновление зеленой рамки в слоте"""
        gif_slot.setStyleSheet("border: 0px;")

    @staticmethod
    def show_green_frame(gif_slot):
        """Обновление зеленой рамки в слоте"""
        gif_slot.setStyleSheet("border: 4px solid green;")

    @staticmethod
    def show_red_frame(gif_slot):
        """Обновление красной рамки в слоте"""
        gif_slot.setStyleSheet("border: 4px solid darkred;")

    def show_splash_area(self, unit, action):
        """Атака по площади"""
        if unit in self.new_battle.player1.units:
            side = self.player_side
        else:
            side = self.enemy_side

        if side == FRONT:
            gif_slot = self.ui.gifPlayerAreaAttack
        else:
            gif_slot = self.ui.gifEnemyAreaAttack

        gif = QMovie(
            os.path.join(
                action,
                f"{side}{unit.name}.gif"))

        gif_slot.setMovie(gif)
        gif.start()

    def get_unit_faction(self, unit):
        """Получение фракции юнита"""
        try:
            for faction, f_building in FACTIONS.items():
                for branch in f_building.values():
                    for building in branch.values():
                        if unit.name == building.unit_name:
                            return faction
            return 'is_dead'
        except:
            pass

    def autofight(self):
        """Автобой"""
        self.new_battle.auto_fight()
        self.update_log()

        if self.new_battle.units_in_round:
            self.who_attack()
            # self.show_frame_attacker()
            self.show_frame_attacked()

            self.worker = Thread(True)
            self.worker.dataThread.connect(self.show_all_attacked)
            self.worker.start()

        # self.unit_gifs_update()

    def show_all_attacked(self, text):
        """Метод обновляющий анимацию всех атакованных юнитов"""
        for target_slot in self.new_battle.attacked_slots:
            self.who_attacked(
                target_slot,
                self.new_battle.current_unit)

        self.show_no_frame_attacker()
        self.show_no_frame_attacked()

        # if text == "Finished":
        #     self.unit_gifs_update()

        if not self.new_battle.battle_is_over:
            self.new_battle.next_turn()
            self.show_frame_attacker()
        else:
            print(self.new_battle.player1.units)
            self.unit_gifs_update()
            self._update_all_unit_health()
            self.unit_icons_update()
        # self.new_battle.autofight = False

        self.update_log()

    def run_autofight(self):
        """Автобой OLD"""
        self.new_battle.auto_fight()
        if self.new_battle.units_in_round:
            self.who_attack()

            for target_slot in self.new_battle.attacked_slots:
                self.who_attacked(
                    target_slot,
                    self.new_battle.current_unit)

    def show_gif_by_side(self, unit, action, slots_dict1, slots_dict2):
        """Отображает GIF в зависимости от стороны и действия"""
        if unit is None:
            pass

        elif unit in self.new_battle.player1.units:
            side = self.player_side
            slots_dict = slots_dict1
            # self.target_is_enemy = True

        elif unit in self.new_battle.player2.units:
            side = self.enemy_side
            slots_dict = slots_dict2
            # self.target_is_enemy = False

        self.show_gif_side(
            unit,
            slots_dict[unit.slot],
            action,
            side)

    def show_frames_by_side(self, unit, slots_dict1, slots_dict2, func):
        """Отображает рамку в зависимости от стороны и действия"""
        if unit is None:
            pass
        elif unit in self.new_battle.player1.units:
            func(slots_dict1[unit.slot])
        elif unit in self.new_battle.player2.units:
            func(slots_dict2[unit.slot])

    def show_no_frames(self, slots_dict, func):
        """Убирает все рамки"""
        for slot in range(1, 7):
            func(slots_dict[slot])

    def show_attacker(self, unit):
        """Прорисовка модели атакующего юнита"""
        self.show_gif_by_side(unit,
                              UNIT_ATTACK,
                              self.pl_slots_dict,
                              self.en_slots_dict)

    def show_frame_attacker(self):
        """Прорисовка рамки вокруг иконки атакующего юнита"""
        # QtCore.QTimer.singleShot(3000, lambda: print(1))
        self.show_frames_by_side(self.new_battle.current_unit,
                                 self.unit_icons_dict,
                                 self.dung_icons_dict,
                                 self.show_green_frame)

    def show_no_frame_attacker(self):
        """Прорисовка рамки вокруг иконки атакующего юнита"""
        self.show_frames_by_side(self.new_battle.current_unit,
                                 self.unit_icons_dict,
                                 self.dung_icons_dict,
                                 self.show_no_frame)

    def show_attacker_eff(self, unit):
        """Прорисовка эффектов атакующего юнита"""
        self.show_gif_by_side(unit,
                              UNIT_EFFECTS_ATTACK,
                              self.pl_slots_eff_dict,
                              self.en_slots_eff_dict)

    def show_shadow_attacker(self, unit):
        """Прорисовка тени атакующего юнита"""
        self.show_gif_by_side(unit,
                              UNIT_SHADOW_ATTACK,
                              self.pl_slots_shad_dict,
                              self.en_slots_shad_dict)

    def show_attacked(self, target):
        """Прорисовка модели атакованного юнита"""
        self.show_gif_by_side(target,
                              UNIT_ATTACKED,
                              self.pl_slots_dict,
                              self.en_slots_dict)

    def show_frame_red(self):
        """Прорисовка рамки вокруг иконки атакованного юнита"""
        for target_slot in self.new_battle.target_slots:
            curr_target = self.get_curr_target(target_slot)

            self.show_frames_by_side(curr_target,
                                     self.unit_icons_dict,
                                     self.dung_icons_dict,
                                     self.show_red_frame)

    def show_frame_attacked(self):
        """Прорисовка рамки вокруг иконки атакованного юнита"""
        for target_slot in self.new_battle.target_slots:
            curr_target = self.get_curr_target(target_slot)

            self.show_frames_by_side(curr_target,
                                     self.unit_icons_dict,
                                     self.dung_icons_dict,
                                     self.show_red_frame)

    def show_no_frame_attacked(self):
        """Прорисовка рамки вокруг иконки атакованного юнита"""
        for target_slot in self.new_battle.target_slots:
            curr_target = self.get_curr_target(target_slot)

            self.show_frames_by_side(curr_target,
                                     self.unit_icons_dict,
                                     self.dung_icons_dict,
                                     self.show_no_frame)

    def show_no_damaged(self):
        """Метод скрывающий нанесенный урон"""
        for icon_slot in self.unit_damaged_dict.values():
            self._show_no_damage(icon_slot)

        for icon_slot in self.dung_damaged_dict.values():
            self._show_no_damage(icon_slot)

    def show_shadow_attacked(self, target):
        """Прорисовка тени атакованного юнита"""
        self.show_gif_by_side(target,
                              UNIT_SHADOW_ATTACKED,
                              self.pl_slots_shad_dict,
                              self.en_slots_shad_dict)

    def get_curr_target(self, target_slot):
        """Получение текущей цели"""
        if self.target_is_enemy:
            curr_target = self._unit_by_slot_and_side(
                target_slot, self.enemy_side)
        else:
            curr_target = self._unit_by_slot_and_side(
                target_slot, self.player_side)
        return curr_target

    def who_attack(self):
        """Метод обновляющий анимацию атакующего юнита"""
        # получение текущего юнита
        curr_unit = self.new_battle.current_unit

        if self.new_battle.autofight:

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

            if curr_unit in self.new_battle.player1.units:
                self.target_is_enemy = True
            else:
                self.target_is_enemy = False

    def who_attacked(self, target_slot, current_unit):
        """Метод обновляющий анимацию атакованного юнита"""
        if target_slot is None:
            return

        # получение текущей цели
        curr_target = self.get_curr_target(target_slot)

        if self.new_battle.autofight:
            if curr_target is None:
                pass
            else:
                # прорисовка модели атакованного юнита
                self.show_attacked(curr_target)

                # прорисовка рамки вокруг слота атакованного юнита
                # self.show_frame_attacked(curr_target)

                # прорисовка тени атакованного юнита
                self.show_shadow_attacked(curr_target)

                if self.target_is_enemy:
                    # прорисовка эффекта на атакованном вражеском юните
                    self.show_gif_side(
                        current_unit,
                        self.en_slots_attacked_eff_dict[curr_target.slot],
                        UNIT_EFFECTS_TARGET,
                        self.enemy_side)

                    # Показывает атакованный вражеский юнит
                    self._show_damage(
                        self.dung_damaged_dict[curr_target.slot])

                    if curr_target.curr_health == 0:
                        self.show_gif_side(
                            curr_target,
                            self.en_slots_eff_dict[curr_target.slot],
                            UNIT_EFFECTS_ATTACK,
                            self.enemy_side)

                else:
                    # прорисовка эффекта на атакованном юните игрока
                    self.show_gif_side(
                        current_unit,
                        self.pl_slots_attacked_eff_dict[curr_target.slot],
                        UNIT_EFFECTS_TARGET,
                        self.player_side)

                    # Показывает атакованный юнит игрока
                    self._show_damage(
                        self.unit_damaged_dict[curr_target.slot])

                    if curr_target.curr_health == 0:
                        self.show_gif_side(
                            curr_target,
                            self.pl_slots_eff_dict[curr_target.slot],
                            UNIT_EFFECTS_ATTACK,
                            self.player_side)

            # если атакованный юнит погиб, удаляем его
            if curr_target.curr_health == 0:
                if curr_target in self.new_battle.units_deque:
                    self.new_battle.units_deque.remove(
                        curr_target)
                if curr_target in self.new_battle.units_in_round:
                    self.new_battle.units_in_round.remove(
                        curr_target)

        # self.new_battle.autofight = False
        # self.new_battle.next_turn()

    @staticmethod
    def _show_damage(icon_slot):
        """Метод показывающий нанесенный урон"""
        icon_slot.setText("40")
        # icon_slot.setPixmap(QPixmap(os.path.join(COMMON, "rose.png")))
        icon_slot.setPixmap(QPixmap(os.path.join(COMMON, "fire.gif")))

    @staticmethod
    def _show_no_damage(icon_slot):
        """Метод скрывающий нанесенный урон на иконке"""
        # icon_slot.setText("0")
        icon_slot.setPixmap(QPixmap(os.path.join(COMMON, "transparent.gif")))

    def update_icons(self,
                     icons_dict,
                     buttons_dict,
                     side):
        """Обновление иконок и кнопок юнитов"""
        for num, icon_slot in icons_dict.items():
            self._slot_update(
                self._unit_by_slot_and_side(num, side),
                icon_slot)

        for num, button_slot in buttons_dict.items():
            self._button_update(
                self._unit_by_slot_and_side(num, side),
                button_slot)

    def set_unit_icons(self):
        """Заполнение временных словарей иконок и кнопок юнитов"""
        # Иконки юнитов FRONT стороны
        self.append_front_icons()

        # Кнопки юнитов FRONT стороны
        self.append_front_buttons()

        # Иконки атакованных юнитов FRONT стороны
        self.append_front_damaged()

        # Иконки юнитов REAR стороны
        self.append_rear_icons()

        # Кнопки юнитов REAR стороны
        self.append_rear_buttons()

        # Иконки атакованных юнитов REAR стороны
        self.append_rear_damaged()

    def unit_icons_update(self):
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

    def set_unit_icons_player1(self):
        """Заполнение словарей иконок и кнопок юнитов FRONT - игрок 1"""
        self.unit_icons_dict = self.front_icons_dict
        self.unit_damaged_dict = self.front_damaged_dict
        self.unit_buttons_dict = self.front_buttons_dict

        self.dung_icons_dict = self.rear_icons_dict
        self.dung_damaged_dict = self.rear_damaged_dict
        self.dung_buttons_dict = self.rear_buttons_dict

    def set_unit_icons_player2(self):
        """Заполнение словарей иконок и кнопок юнитов FRONT - игрок 2"""
        self.dung_icons_dict = self.front_icons_dict
        self.dung_damaged_dict = self.front_damaged_dict
        self.dung_buttons_dict = self.front_buttons_dict

        self.unit_icons_dict = self.rear_icons_dict
        self.unit_damaged_dict = self.rear_damaged_dict
        self.unit_buttons_dict = self.rear_buttons_dict

    def animate_action_side(self, slots_dict, unit_action, side):
        """Анимации юнитов игрока"""
        for num, gif_slot in slots_dict.items():
            self.show_gif_side(
                self._unit_by_slot_and_side(num, side),
                gif_slot,
                unit_action,
                side)

    def unit_gifs_update(self):
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

    @staticmethod
    def _update_unit_health(unit, slot):
        """Обновление здоровья юнита"""
        try:
            slot.setText(f'{unit.curr_health}/{unit.health}')
        except AttributeError:
            slot.setText('')

    def _update_all_unit_health(self):
        """Метод обновляющий текущее здоровье всех юнитов"""

        # прорисовка здоровья юнитов со стороны FRONT
        for num, hp_slot in self.pl_hp_slots_dict.items():
            self._update_unit_health(
                self._unit_by_slot_and_side(num, self.player_side),
                hp_slot)

        # прорисовка здоровья юнитов со стороны REAR
        for num, hp_slot in self.en_hp_slots_dict.items():
            self._update_unit_health(
                self._unit_by_slot_and_side(num, self.enemy_side),
                hp_slot)

    def set_coords_double_slots(self, ui_obj):
        """Задание координат для 'двойных' слотов либо кнопок"""
        if ui_obj in [
            self.ui.slot2,
            self.ui.slot4,
            self.ui.slot6,
            self.ui.damPlayerSlot_2,
            self.ui.damPlayerSlot_4,
            self.ui.damPlayerSlot_6,
            self.ui.pushButtonSlot2,
            self.ui.pushButtonSlot4,
            self.ui.pushButtonSlot6,
        ]:
            ui_coords = ui_obj.geometry().getCoords()
            new_coords = list(ui_coords)
            new_coords[0] = 147
            ui_obj.setGeometry(*new_coords)

            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def _set_size_by_unit(self, unit, ui_obj):
        """Установка размера иконки по размеру самого юнита"""
        self.set_coords_double_slots(ui_obj)

        try:
            if unit.size == "Большой" and ui_obj in [
                self.ui.slot2,
                self.ui.slot4,
                self.ui.slot6,
                self.ui.damPlayerSlot_2,
                self.ui.damPlayerSlot_4,
                self.ui.damPlayerSlot_6,
                self.ui.pushButtonSlot2,
                self.ui.pushButtonSlot4,
                self.ui.pushButtonSlot6,
            ]:
                ui_coords = ui_obj.geometry().getCoords()
                new_coords = list(ui_coords)
                new_coords[0] -= 117
                new_coords[2] = 224
                new_coords[3] = 126
                ui_obj.setGeometry(*new_coords)

            if unit.size == "Большой":
                ui_obj.setFixedWidth(225)
                ui_obj.setFixedHeight(127)

            elif unit.size == "Обычный":
                ui_obj.setFixedWidth(105)
                ui_obj.setFixedHeight(127)
        except AttributeError:
            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def _button_update(self, unit, button):
        """Установка размера кнопки на иконке"""
        self._set_size_by_unit(unit, button)

        self.hbox.addWidget(button)
        self.setLayout(self.hbox)

    def _slot_update(self, unit, slot):
        """Метод обновления иконки"""
        self._set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            get_unit_image(unit)).scaled(
            slot.width(), slot.height()))
        self.hbox.addWidget(slot)
        self.setLayout(self.hbox)

    def _slot_detailed(self, unit, slot_dialog):
        """Метод создающий окно юнита игрока при нажатии на слот."""
        try:
            global DETAIL_WINDOW
            DETAIL_WINDOW = slot_dialog(
                self.database,
                unit)
            DETAIL_WINDOW.show()
        except AttributeError:
            pass

    def _slot1_detailed(self):
        """Метод создающий окно юнита игрока (слот 1)."""
        unit = self._unit_by_slot_and_side(1, FRONT)
        self._slot_detailed(unit, UnitDialog)

    def _slot2_detailed(self):
        """Метод создающий окно юнита игрока (слот 2)."""
        unit = self._unit_by_slot_and_side(2, FRONT)
        self._slot_detailed(unit, UnitDialog)

    def _slot3_detailed(self):
        """Метод создающий окно юнита игрока (слот 3)."""
        unit = self._unit_by_slot_and_side(3, FRONT)
        self._slot_detailed(unit, UnitDialog)

    def _slot4_detailed(self):
        """Метод создающий окно юнита игрока (слот 4)."""
        unit = self._unit_by_slot_and_side(4, FRONT)
        self._slot_detailed(unit, UnitDialog)

    def _slot5_detailed(self):
        """Метод создающий окно юнита игрока (слот 5)."""
        unit = self._unit_by_slot_and_side(5, FRONT)
        self._slot_detailed(unit, UnitDialog)

    def _slot6_detailed(self):
        """Метод создающий окно юнита игрока (слот 6)."""
        unit = self._unit_by_slot_and_side(6, FRONT)
        self._slot_detailed(unit, UnitDialog)

    def _enemy_slot1_detailed(self):
        """Метод создающий окно юнита (слот 1)."""
        unit = self._unit_by_slot_and_side(1, REAR)
        self._slot_detailed(unit, UnitDialog)

    def _enemy_slot2_detailed(self):
        """Метод создающий окно юнита (слот 2)."""
        unit = self._unit_by_slot_and_side(2, REAR)
        self._slot_detailed(unit, UnitDialog)

    def _enemy_slot3_detailed(self):
        """Метод создающий окно юнита (слот 3)."""
        unit = self._unit_by_slot_and_side(3, REAR)
        self._slot_detailed(unit, UnitDialog)

    def _enemy_slot4_detailed(self):
        """Метод создающий окно юнита (слот 4)."""
        unit = self._unit_by_slot_and_side(4, REAR)
        self._slot_detailed(unit, UnitDialog)

    def _enemy_slot5_detailed(self):
        """Метод создающий окно юнита (слот 5)."""
        unit = self._unit_by_slot_and_side(5, REAR)
        self._slot_detailed(unit, UnitDialog)

    def _enemy_slot6_detailed(self):
        """Метод создающий окно юнита (слот 6)."""
        unit = self._unit_by_slot_and_side(6, REAR)
        self._slot_detailed(unit, UnitDialog)

    def _unit_by_slot_and_side(self, slot, side):
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
