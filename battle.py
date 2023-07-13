"""Battle"""
import random
from collections import deque

from client_dir.settings import ANY_UNIT, CLOSEST_UNIT
from battle_logging import logging
from units_dir.units_factory import Unit

player1_name = 'Erepb-89'
# player2_name = 'Erepb'
player2_name = 'Computer'


class Player:
    """Класс Игрок"""
    def __init__(self, name):
        self.name = name
        self.units = []
        self.initiative_order = sorted(
            self.units, key=lambda u: u.attack_ini, reverse=True)


class Battle:
    """Класс битвы"""

    def __init__(self, database, dungeon):
        # super().__init__()
        # основные переменные
        self.database = database
        self.autofight = False
        self.units_deque = deque()
        self.target_slots = []
        self.current_unit = None
        self.player_slots = []
        self.enemy_slots = []
        self.units_in_round = []
        self.en_exp_killed = 0

        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)

        # self.current_faction = self.database.current_game_faction

        self.dungeon_units = self.database.show_dungeon_units(dungeon)
        # self.dungeon_units = self.database.show_dungeon_units('thieves')
        # self.dungeon_units = self.database.show_dungeon_units('knight')
        # self.dungeon_units = self.database.show_dungeon_units('mirror')

        if player2_name == "Computer":
            self.add_dung_units()
        else:
            self.add_player_units(
                self.player2,
                self.enemy_slots,
                self.database.Player2Units)

        self.add_player_units(
            self.player1,
            self.player_slots,
            self.database.PlayerUnits)
        self.new_round()

    # def add_player_slots(self, player):
    #     for pl_slot in range(1, 7):

    def add_player_units(self, player, slots_list, database):
        """
        Добавление юнитов игрока в текущую битву.
        Выполняется в начале каждой новой битвы.
        """
        for pl_slot in range(1, 7):
            unit = self.database.get_unit_by_slot(
                pl_slot,
                database)
            if unit is not None:
                player.units.append(Unit(unit))
                if not unit.curr_health <= 0:
                    slots_list.append(unit.slot)

    def add_dung_units(self):
        """
        Добавление юнитов подземелья в текущую битву.
        Выполняется в начале новой битвы с компьютером.
        """
        self.clear_dungeon()
        for unit_slot in range(6):
            try:
                unit = self.database.get_unit_by_id(
                    self.dungeon_units[unit_slot],
                    self.database.AllUnits)[:24]
                self.database.add_dungeon_unit(
                    *unit,
                    unit_slot + 1)

                unit = self.dungeon_unit_by_slot(unit_slot + 1)
                if unit is not None:
                    self.player2.units.append(Unit(unit))
                    if not unit.curr_health <= 0:
                        self.enemy_slots.append(unit.slot)
            except (TypeError, AttributeError) as err:
                print(err)

    def dungeon_unit_by_slot(self, slot):
        """Метод получающий юнита подземелья по слоту."""
        return self.database.get_unit_by_slot(
            slot,
            self.database.CurrentDungeon)

    def player_unit_by_slot(self, slot):
        """Метод получающий юнита игрока по слоту."""
        return self.database.get_unit_by_slot(
            slot,
            self.database.PlayerUnits)

    @staticmethod
    def get_unit_by_slot(slot, player_units):
        """Метод получающий юнита по слоту."""
        for player_unit in player_units:
            if player_unit.slot == slot:
                return player_unit
        return None

    @staticmethod
    def sorting_units(all_units):
        """Сортировка юнитов по инициативе"""
        sorted_units_by_ini = sorted(
            all_units, key=lambda u: u.attack_ini, reverse=True)

        return sorted_units_by_ini

    def new_round(self):
        """Высчитывание оставшихся выживших в новом раунде"""
        self.units_deque.clear()

        all_units = self.get_player_units(self.player1) + \
                    self.get_player_units(self.player2)

        sorted_units_by_ini = self.sorting_units(all_units)

        for unit in sorted_units_by_ini:
            self.units_deque.append(unit)
            self.units_in_round.append(unit)

    def _get_battle_unit_by_id(self, _id):
        """Метод возвращает юнита из deque по id"""
        for unit in self.units_deque:
            if unit.id == _id:
                return unit
        return None

    # def defense(self, unit):
    #     unit.armor = 50

    def auto_fight(self):
        """Автобой"""
        self.autofight = True
        if self.units_in_round:

            self.current_unit = self.units_deque.popleft()
            if self.current_unit.attack_type \
                not in ['Лечение', 'Лечение/Исцеление', 'Лечение/Воскрешение']:

                self.target_slots = self.auto_choose_target(self.current_unit)

                # атака игрока player1 по игроку player2
                if self.current_unit in self.player1.units:
                    self.player_attack(self.player2)

                # атака игрока player2 по игроку player1
                elif self.current_unit in self.player2.units:
                    self.player_attack(self.player1)

            else:
                if self.current_unit in self.player1.units:
                    heal_targets = self.choose_healed(
                        self.current_unit, self.player_slots)
                    # for target_slot in heal_targets:
                    #     target = self.get_unit_by_slot(
                    #         target_slot,
                    #         self.player1.units)
                    #     self.current_unit.heal(target)

                elif self.current_unit in self.player2.units:
                    heal_targets = self.choose_healed(
                        self.current_unit, self.enemy_slots)
                for target_slot in heal_targets:
                    target = self.get_unit_by_slot(
                        target_slot,
                        self.player2.units)
                    self.current_unit.heal(target)

            if not self.player1.units:
                print('You lose!')
            if not self.player2.units:
                print('You won!')

            self.units_in_round.remove(self.current_unit)
            self.units_deque.append(self.current_unit)
        else:
            self.new_round()

    def player_attack(self, player):
        if self.current_unit.attack_radius == ANY_UNIT \
                and self.current_unit.attack_purpose == 6:
            for target_slot in self.target_slots:
                target = self.get_unit_by_slot(
                    target_slot,
                    player.units)
                self.current_unit.attack(target)
        elif self.target_slots == [None]:
            line = f'{self.current_unit.name}, пропускает ход\n'
            logging(line)
            # print(self.current_unit.name, 'пропускает ход')
        else:
            self.current_unit.attack(
                self.get_unit_by_slot(
                    self.target_slots[0],
                    player.units))
        if not player.units:
            print(f'{player.name} lose!')

    def clear_dungeon(self):
        """Очистка текущего подземелья от вражеских юнитов"""
        self.database.delete_dungeon_unit(1)
        self.database.delete_dungeon_unit(2)
        self.database.delete_dungeon_unit(3)
        self.database.delete_dungeon_unit(4)
        self.database.delete_dungeon_unit(5)
        self.database.delete_dungeon_unit(6)

    def regen(self):
        """Восстановление здоровья всех юнитов игрока"""
        # self.clear_dungeon()
        self.database.autoregen(1)
        self.database.autoregen(2)
        self.database.autoregen(3)
        self.database.autoregen(4)
        self.database.autoregen(5)
        self.database.autoregen(6)

    @staticmethod
    def closest_side_slot(tg_slots, slot_a: int, slot_b: int, slot_c: int):
        """Вычисление рандомной цели для крайних слотов"""
        if slot_a in tg_slots and slot_b in tg_slots:
            return random.choice([slot_a, slot_b])
        if slot_a in tg_slots:
            return slot_a
        if slot_b in tg_slots:
            return slot_b
        if slot_a not in tg_slots and slot_b not in tg_slots and slot_c in tg_slots:
            return slot_c
        return None

    @staticmethod
    def closest_middle_slot(tg_slots, slot_a: int, slot_b: int, slot_c: int):
        """Вычисление рандомной цели для среднего слота"""
        if slot_a in tg_slots and slot_b in tg_slots and slot_c in tg_slots:
            return random.choice([slot_a, slot_b, slot_c])
        if slot_a in tg_slots:
            return slot_a
        if slot_b in tg_slots:
            return slot_b
        if slot_c in tg_slots:
            return slot_c
        return None

    def define_closest_slot(self, unit, target_slots, alies_slots):
        """Определение ближайшего слота для текущего юнита"""
        result = None
        vanguard_alies_died = 2 not in alies_slots and \
                              4 not in alies_slots and \
                              6 not in alies_slots
        vanguard_enemies_died = 2 not in target_slots and \
                                4 not in target_slots and \
                                6 not in target_slots

        targets_dict = {
            1: self.closest_side_slot(
                target_slots,
                unit.slot,
                unit.slot + 2,
                unit.slot + 4),
            2: self.closest_side_slot(
                target_slots,
                unit.slot + 1,
                unit.slot + 3,
                unit.slot + 5),
            3: self.closest_middle_slot(
                target_slots,
                unit.slot,
                unit.slot - 2,
                unit.slot + 2),
            4: self.closest_middle_slot(
                target_slots,
                unit.slot - 1,
                unit.slot - 3,
                unit.slot + 1),
            5: self.closest_side_slot(
                target_slots,
                unit.slot,
                unit.slot - 2,
                unit.slot - 4),
            6: self.closest_side_slot(
                target_slots,
                unit.slot - 1,
                unit.slot - 3,
                unit.slot - 5),
        }

        if (
                vanguard_enemies_died and
                vanguard_alies_died and
                unit.slot % 2 == 1
        ):
            result = targets_dict[unit.slot]
        elif (
                vanguard_enemies_died and
                unit.slot % 2 == 0):
            result = targets_dict[unit.slot]
        elif (
                not vanguard_enemies_died and
                vanguard_alies_died and
                unit.slot % 2 == 1
        ):
            result = targets_dict[unit.slot + 1]
        elif (
                not vanguard_enemies_died and
                unit.slot % 2 == 0):
            result = targets_dict[unit.slot - 1]
        elif (
                not vanguard_enemies_died and
                not vanguard_alies_died and
                unit.slot % 2 == 1):
            result = None

        return result

    @staticmethod
    def choose_healed(unit, target_slots):
        """Определение следующей цели для лечения"""
        if unit.attack_radius == ANY_UNIT and unit.attack_purpose == 6:
            print('choose_healed targets:', target_slots)
            return target_slots
        if unit.attack_radius == ANY_UNIT and unit.attack_purpose == 1:
            target = random.choice(target_slots)
            print('choose_healed targets:', [target])
            return [target]
        return None

    def choose_target(self, unit, attacker_slots, target_slots):
        """Определение следующей цели для атаки"""
        if unit.attack_radius == CLOSEST_UNIT:
            target = self.define_closest_slot(
                unit, target_slots, attacker_slots)
            return [target]
        if unit.attack_radius == ANY_UNIT and unit.attack_purpose == 6:
            return target_slots
        if unit.attack_radius == ANY_UNIT and unit.attack_purpose == 1:
            target = random.choice(target_slots)
            return [target]
        return None

    def auto_choose_target(self, unit):
        """Авто определение следующей цели для атаки"""
        # print('enemy_slots', self.enemy_slots)
        # print('player_slots', self.player_slots)
        self.player_slots = self.get_player_slots(self.player1)
        self.enemy_slots = self.get_player_slots(self.player2)

        if unit.attack_type \
                not in ['Лечение', 'Лечение/Исцеление', 'Лечение/Воскрешение']:
            if unit in self.player1.units:
                # print(f'Ходит {player1_name}')
                # line = f'Ходит {player1_name}\n'
                # logging(line)
                return self.choose_target(
                    unit, self.player_slots, self.enemy_slots)

            if unit in self.player2.units:
                # print(f'Ходит {player2_name}')
                # line = f'Ходит {player2_name}\n'
                # logging(line)
                return self.choose_target(
                    unit, self.enemy_slots, self.player_slots)
        return None

    @staticmethod
    def get_player_slots(player):
        """Получение слотов с живыми юнитами игрока"""
        player_slots = []
        for unit in player.units:
            if unit is not None and not unit.curr_health <= 0:
                player_slots.append(unit.slot)

        return player_slots

    @staticmethod
    def get_player_units(player):
        """Получение живых юнитов игрока"""
        player_units = []
        for unit in player.units:
            if unit is not None and not unit.curr_health <= 0:
                player_units.append(unit)

        return player_units
