import os.path
import random

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from battle import Battle
from client_dir.fight_form import Ui_FightWindow
from client_dir.settings import UNIT_ICONS, UNIT_STAND, UNIT_ATTACK, UNIT_ATTACKED, \
    UNIT_EFFECTS, BATTLE_GROUND, FRONT, REAR, COMMON, BATTLE_GROUNDS
from client_dir.unit_dialog import EnemyUnitSlotDialog, UnitSlotDialog


class FightWindow(QMainWindow):
    """
    Класс - окно выбора фракции.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла fight_menu_form.py
    """

    def __init__(self, database):
        super().__init__()
        # основные переменные
        self.database = database
        self.new_battle = Battle(self.database)
        self.player_side = FRONT
        self.enemy_side = REAR

        self.InitUI()

    def InitUI(self):
        # Загружаем конфигурацию окна из дизайнера

        self.ui = Ui_FightWindow()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)
        self.update_bg()

        self.unit_list_update()
        self.unit_gifs_update()
        self.dungeon_list_update()
        self.update_all_unit_health()

        self.ui.leftIcons.setPixmap(QPixmap(os.path.join(COMMON, "left_icons.png")))
        self.ui.rightIcons.setPixmap(QPixmap(os.path.join(COMMON, "right_icons.png")))

        self.ui.pushButtonBack.clicked.connect(self.back)
        self.ui.pushButtonAttack.clicked.connect(self.attack)
        self.ui.pushButtonAttacked.clicked.connect(self.attacked)
        # self.ui.pushButtonAttack.clicked.connect(self.attack_eff)

        self.ui.pushButtonSlot1.clicked.connect(self.slot1_detailed)
        self.ui.pushButtonSlot2.clicked.connect(self.slot2_detailed)
        self.ui.pushButtonSlot3.clicked.connect(self.slot3_detailed)
        self.ui.pushButtonSlot4.clicked.connect(self.slot4_detailed)
        self.ui.pushButtonSlot5.clicked.connect(self.slot5_detailed)
        self.ui.pushButtonSlot6.clicked.connect(self.slot6_detailed)

        self.ui.pushButtonEnemySlot1.clicked.connect(self.enemy_slot1_detailed)
        self.ui.pushButtonEnemySlot2.clicked.connect(self.enemy_slot2_detailed)
        self.ui.pushButtonEnemySlot3.clicked.connect(self.enemy_slot3_detailed)
        self.ui.pushButtonEnemySlot4.clicked.connect(self.enemy_slot4_detailed)
        self.ui.pushButtonEnemySlot5.clicked.connect(self.enemy_slot5_detailed)
        self.ui.pushButtonEnemySlot6.clicked.connect(self.enemy_slot6_detailed)

        self.ui.pushButtonAutoFight.clicked.connect(self.run_autofight)
        self.ui.pushButtonClear.clicked.connect(self.new_battle.regen)

        self.pl_slots_dict = {
            1: self.ui.gifSlot_1,
            2: self.ui.gifSlot_2,
            3: self.ui.gifSlot_3,
            4: self.ui.gifSlot_4,
            5: self.ui.gifSlot_5,
            6: self.ui.gifSlot_6,
        }
        self.en_slots_dict = {
            1: self.ui.gifEnemySlot_1,
            2: self.ui.gifEnemySlot_2,
            3: self.ui.gifEnemySlot_3,
            4: self.ui.gifEnemySlot_4,
            5: self.ui.gifEnemySlot_5,
            6: self.ui.gifEnemySlot_6,
        }

        # self.check_autofight()
        self.show()

    def update_bg(self):
        """Обновление бэкграунда, заполнение картинкой поля сражения"""
        fight_bg = self.ui.FightBG
        # hire_menu_bg.setPixmap(QPixmap(self.get_image(self.current_faction)))
        # fight_bg.setPixmap(QPixmap(os.path.join(BATTLE_GROUND, "ImageMap03.png")))
        fight_bg.setPixmap(QPixmap(os.path.join(BATTLE_GROUND, random.choice(BATTLE_GROUNDS))))
        fight_bg.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        self.hbox.addWidget(fight_bg)
        self.setLayout(self.hbox)

    def back(self):
        """Кнопка возврата"""
        self.close()

    def attack_slot(self, unit, gif_slot, command):
        """Атака юнита в слоте"""
        try:
            if unit.curr_health == 0:
                gif = QMovie(os.path.join(command, f"{self.player_side}/is_dead.gif"))
            else:
                gif = QMovie(os.path.join(command, f"{self.player_side}{unit.name}.gif"))

            gif_slot.setMovie(gif)
            self.update_all_unit_health()
            gif.start()
        except Exception as err:
            print(err)

    def attack_enemy_slot(self, unit, gif_slot, command):
        """Атака вражеского юнита в слоте"""
        try:
            if unit.curr_health == 0:
                gif = QMovie(os.path.join(command, f"{self.enemy_side}/is_dead.gif"))
            else:
                gif = QMovie(os.path.join(command, f"{self.enemy_side}{unit.name}.gif"))
            gif_slot.setMovie(gif)
            self.update_all_unit_health()
            gif.start()
        except Exception as err:
            print(err)

    def attack(self):
        """Кнопка атаки"""
        try:
            gif = QMovie(os.path.join(UNIT_ATTACK, "Сын Имира.gif"))
            self.ui.gifSlot_2.setMovie(gif)
            gif.start()
        except Exception as err:
            print(err)

    def run_autofight(self):
        self.new_battle.auto_fight()
        self.who_attack()
        self.who_attacked()

    def who_attack(self):
        curr_unit = self.new_battle.current_unit

        if self.new_battle.autofight:
            if curr_unit.id in self.new_battle.player_ids:
                self.attack_slot(curr_unit, self.pl_slots_dict[curr_unit.slot], UNIT_ATTACK)
                self.target_is_enemy = 1
            elif curr_unit.id in self.new_battle.enemy_ids:
                self.attack_enemy_slot(curr_unit, self.en_slots_dict[curr_unit.slot], UNIT_ATTACK)
                self.target_is_enemy = 0

    def who_attacked(self):
        if self.target_is_enemy:
            curr_target = self.database.get_dungeon_unit_by_slot(self.new_battle.target_slot)
        else:
            curr_target = self.database.get_unit_by_slot(self.new_battle.target_slot)

        if self.new_battle.autofight:
            if self.target_is_enemy:
                self.attack_enemy_slot(curr_target, self.en_slots_dict[curr_target.slot], UNIT_ATTACKED)
            else:
                self.attack_slot(curr_target, self.pl_slots_dict[curr_target.slot], UNIT_ATTACKED)

    def attacked(self):
        """Кнопка Атакован"""
        try:
            gif = QMovie(os.path.join("../images/gif/battle_attacked/front/Сын Имира.gif"))
            self.ui.gifSlot_2.setMovie(gif)
            gif.start()
        except:
            pass

    def attack_eff(self):
        """Кнопка атаки"""
        try:
            gif = QMovie(os.path.join(UNIT_EFFECTS, f"{self.player_side}Сын Имира.gif"))
            self.ui.gifSlot2_2.setMovie(gif)
            gif.start()
        except Exception as err:
            print(err)

    def unit_list_update(self):
        """Метод обновляющий список юнитов игрока"""

        self.slot_update(self.database.get_unit_by_slot(1), self.ui.slot1)
        self.slot_update(self.database.get_unit_by_slot(2), self.ui.slot2)
        self.slot_update(self.database.get_unit_by_slot(3), self.ui.slot3)
        self.slot_update(self.database.get_unit_by_slot(4), self.ui.slot4)
        self.slot_update(self.database.get_unit_by_slot(5), self.ui.slot5)
        self.slot_update(self.database.get_unit_by_slot(6), self.ui.slot6)

        self.button_update(self.database.get_unit_by_slot(1), self.ui.pushButtonSlot1)
        self.button_update(self.database.get_unit_by_slot(2), self.ui.pushButtonSlot2)
        self.button_update(self.database.get_unit_by_slot(3), self.ui.pushButtonSlot3)
        self.button_update(self.database.get_unit_by_slot(4), self.ui.pushButtonSlot4)
        self.button_update(self.database.get_unit_by_slot(5), self.ui.pushButtonSlot5)
        self.button_update(self.database.get_unit_by_slot(6), self.ui.pushButtonSlot6)

    def unit_gifs_update(self):
        """Метод обновляющий анимацию юнитов игрока"""
        # for slot, gif in self.pl_slots_dict.items():
        #     try:
        #         unit = self.database.get_unit_by_slot(slot)
        #         if unit is not None and unit.curr_health != 0:
        #             self.show_gif(unit, gif, self.player_side)
        #     except Exception as err:
        #         print(err)

        self.show_gif(self.database.get_unit_by_slot(1), self.ui.gifSlot_1, self.player_side)
        self.show_gif(self.database.get_unit_by_slot(2), self.ui.gifSlot_2, self.player_side)
        self.show_gif(self.database.get_unit_by_slot(3), self.ui.gifSlot_3, self.player_side)
        self.show_gif(self.database.get_unit_by_slot(4), self.ui.gifSlot_4, self.player_side)
        self.show_gif(self.database.get_unit_by_slot(5), self.ui.gifSlot_5, self.player_side)
        self.show_gif(self.database.get_unit_by_slot(6), self.ui.gifSlot_6, self.player_side)

        self.show_gif(self.new_battle.enemy_unit_1, self.ui.gifEnemySlot_1, self.enemy_side)
        self.show_gif(self.new_battle.enemy_unit_2, self.ui.gifEnemySlot_2, self.enemy_side)
        self.show_gif(self.new_battle.enemy_unit_3, self.ui.gifEnemySlot_3, self.enemy_side)
        self.show_gif(self.new_battle.enemy_unit_4, self.ui.gifEnemySlot_4, self.enemy_side)
        self.show_gif(self.new_battle.enemy_unit_5, self.ui.gifEnemySlot_5, self.enemy_side)
        self.show_gif(self.new_battle.enemy_unit_6, self.ui.gifEnemySlot_6, self.enemy_side)

    def dungeon_list_update(self):
        """Метод обновляющий список юнитов подземелья"""

        self.slot_update(self.new_battle.enemy_unit_1, self.ui.enemySlot1)
        self.slot_update(self.new_battle.enemy_unit_2, self.ui.enemySlot2)
        self.slot_update(self.new_battle.enemy_unit_3, self.ui.enemySlot3)
        self.slot_update(self.new_battle.enemy_unit_4, self.ui.enemySlot4)
        self.slot_update(self.new_battle.enemy_unit_5, self.ui.enemySlot5)
        self.slot_update(self.new_battle.enemy_unit_6, self.ui.enemySlot6)

        self.button_update(self.new_battle.enemy_unit_1, self.ui.pushButtonEnemySlot1)
        self.button_update(self.new_battle.enemy_unit_2, self.ui.pushButtonEnemySlot2)
        self.button_update(self.new_battle.enemy_unit_3, self.ui.pushButtonEnemySlot3)
        self.button_update(self.new_battle.enemy_unit_4, self.ui.pushButtonEnemySlot4)
        self.button_update(self.new_battle.enemy_unit_5, self.ui.pushButtonEnemySlot5)
        self.button_update(self.new_battle.enemy_unit_6, self.ui.pushButtonEnemySlot6)

    def update_unit_health(self, unit, slot):
        try:
            slot.setText(f'{unit.curr_health}/{unit.health}')
        except:
            slot.setText('')

    def update_all_unit_health(self):
        self.update_unit_health(self.database.get_dungeon_unit_by_slot(1), self.ui.enemyHPSlot1)
        self.update_unit_health(self.database.get_dungeon_unit_by_slot(2), self.ui.enemyHPSlot2)
        self.update_unit_health(self.database.get_dungeon_unit_by_slot(3), self.ui.enemyHPSlot3)
        self.update_unit_health(self.database.get_dungeon_unit_by_slot(4), self.ui.enemyHPSlot4)
        self.update_unit_health(self.database.get_dungeon_unit_by_slot(5), self.ui.enemyHPSlot5)
        self.update_unit_health(self.database.get_dungeon_unit_by_slot(6), self.ui.enemyHPSlot6)

        self.update_unit_health(self.database.get_unit_by_slot(1), self.ui.hpSlot1)
        self.update_unit_health(self.database.get_unit_by_slot(2), self.ui.hpSlot2)
        self.update_unit_health(self.database.get_unit_by_slot(3), self.ui.hpSlot3)
        self.update_unit_health(self.database.get_unit_by_slot(4), self.ui.hpSlot4)
        self.update_unit_health(self.database.get_unit_by_slot(5), self.ui.hpSlot5)
        self.update_unit_health(self.database.get_unit_by_slot(6), self.ui.hpSlot6)

    def set_size_by_unit(self, unit, button):
        try:
            if unit.size == "Большой":
                button.setFixedWidth(224)
                button.setFixedHeight(127)
        except:
            button.setFixedWidth(105)
            button.setFixedHeight(127)

    def button_update(self, unit, button):
        self.set_size_by_unit(unit, button)

        self.hbox.addWidget(button)
        self.setLayout(self.hbox)

    def slot_update(self, unit, slot):
        self.set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            self.get_unit_image(unit)).scaled(
            slot.width(), slot.height()))
        self.hbox.addWidget(slot)
        self.setLayout(self.hbox)

    def get_unit_image(self, unit):
        try:
            return os.path.join(UNIT_ICONS, f"{unit.name} (Disciples II)-иконка.jpg")
        except:
            return os.path.join(UNIT_ICONS, "Заглушка (Disciples II)-иконка.jpg")

    def show_gif(self, unit, gif_label, side):
        try:
            if unit.curr_health == 0:
                gif_label.setPixmap(QPixmap(os.path.join(COMMON, "skull.png")))
            elif unit.curr_health > 0:
                gif = QMovie(os.path.join(UNIT_STAND, f"{side}{unit.name}.gif"))
                gif_label.setMovie(gif)
                gif.start()
        except Exception as err:
            print(err)

    def slot1_detailed(self):
        """Метод создающий окно юнита игрока (слот 1)."""
        try:
            global detail_window
            detail_window = UnitSlotDialog(self.database, 1)
            detail_window.show()
        except:
            pass

    def slot2_detailed(self):
        """Метод создающий окно юнита игрока (слот 2)."""
        try:
            global detail_window
            detail_window = UnitSlotDialog(self.database, 2)
            detail_window.show()
        except:
            pass

    def slot3_detailed(self):
        """Метод создающий окно юнита игрока (слот 3)."""
        try:
            global detail_window
            detail_window = UnitSlotDialog(self.database, 3)
            detail_window.show()
        except:
            pass

    def slot4_detailed(self):
        """Метод создающий окно юнита игрока (слот 4)."""
        try:
            global detail_window
            detail_window = UnitSlotDialog(self.database, 4)
            detail_window.show()
        except:
            pass

    def slot5_detailed(self):
        """Метод создающий окно юнита игрока (слот 5)."""
        try:
            global detail_window
            detail_window = UnitSlotDialog(self.database, 5)
            detail_window.show()
        except:
            pass

    def slot6_detailed(self):
        """Метод создающий окно юнита игрока (слот 6)."""
        try:
            global detail_window
            detail_window = UnitSlotDialog(self.database, 6)
            detail_window.show()
        except:
            pass

    def enemy_slot1_detailed(self):
        """Метод создающий окно юнита (слот 1)."""
        try:
            global detail_window
            detail_window = EnemyUnitSlotDialog(self.database, 1)
            detail_window.show()
        except Exception as err:
            print(err)

    def enemy_slot2_detailed(self):
        """Метод создающий окно юнита (слот 2)."""
        try:
            global detail_window
            detail_window = EnemyUnitSlotDialog(self.database, 2)
            detail_window.show()
        except Exception as err:
            print(err)

    def enemy_slot3_detailed(self):
        """Метод создающий окно юнита (слот 3)."""
        try:
            global detail_window
            detail_window = EnemyUnitSlotDialog(self.database, 3)
            detail_window.show()
        except Exception as err:
            print(err)

    def enemy_slot4_detailed(self):
        """Метод создающий окно юнита (слот 4)."""
        try:
            global detail_window
            detail_window = EnemyUnitSlotDialog(self.database, 4)
            detail_window.show()
        except Exception as err:
            print(err)

    def enemy_slot5_detailed(self):
        """Метод создающий окно юнита (слот 5)."""
        try:
            global detail_window
            detail_window = EnemyUnitSlotDialog(self.database, 5)
            detail_window.show()
        except:
            self.show_available_units()
            self.slot5_update()

    def enemy_slot6_detailed(self):
        """Метод создающий окно юнита (слот 6)."""
        try:
            global detail_window
            detail_window = EnemyUnitSlotDialog(self.database, 6)
            detail_window.show()
        except:
            self.show_available_units()
            self.slot6_update()
