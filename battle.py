"""Battle"""
import random
from collections import deque

from client_dir.settings import ANY_UNIT, CLOSEST_UNIT
from battle_logging import logging
from units_dir.units_factory import Unit

PLAYER1_NAME = 'Erepb-89'
PLAYER2_NAME = 'Computer'


class Player:
    """Класс Игрок"""

    def __init__(self, name):
        self.name = name
        self.units = []
        self.slots = []


class Battle:
    """Класс битвы"""

    def __init__(self, database, dungeon):
        # super().__init__()
        # основные переменные
        self.database = database
        self.autofight = False
        self.units_deque = deque()
        self.target_slots = []
        self.attacked_slots = []
        self.current_unit = None
        self.units_in_round = []
        self.en_exp_killed = 0
        self.target = None
        self.battle_is_over = False
        self.alive_units = []

        self.player1 = Player(PLAYER1_NAME)
        self.player2 = Player(PLAYER2_NAME)

        # self.current_faction = self.database.current_game_faction

        self.dungeon_units = self.database.show_dungeon_units(dungeon)
        # self.dungeon_units = self.database.show_dungeon_units('thieves')
        # self.dungeon_units = self.database.show_dungeon_units('knight')
        # self.dungeon_units = self.database.show_dungeon_units('mirror')

        if self.player2.name == "Computer":
            self.add_dung_units()
        else:
            self.add_player_units(
                self.player2,
                self.database.Player2Units)

        self.add_player_units(
            self.player1,
            self.database.PlayerUnits)
        self.new_round()
        self.next_turn()

    def add_player_units(self,
                         player: Player,
                         database):
        """
        Добавление юнитов игрока в текущую битву.
        Выполняется в начале каждой новой битвы.
        """
        player.units = []
        for pl_slot in range(1, 7):
            unit = self.database.get_unit_by_slot(
                pl_slot,
                database)
            if unit is not None:
                player.units.append(Unit(unit))
                if not unit.curr_health <= 0:
                    player.slots.append(unit.slot)

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
                        self.player2.slots.append(unit.slot)
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
        units_ini = {}
        for unit in all_units:
            ini = unit.attack_ini + random.randrange(-4, 5)
            units_ini[unit] = ini

        sorted_units_by_ini = sorted(
            units_ini, key=units_ini.get, reverse=True)
        return sorted_units_by_ini

    def new_round(self):
        """Высчитывание оставшихся выживших в новом раунде"""
        self.units_deque.clear()

        all_units = self.player1.units + self.player2.units

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

    def next_turn(self):
        """Ход юнита"""
        self.current_unit = self.units_deque.popleft()
        print(
            f'Ходит: {self.current_unit.name}, инициатива: {self.current_unit.attack_ini}')
        line = f'Ходит: {self.current_unit.name}\n'
        logging(line)

        self.target_slots = self.auto_choose_target(self.current_unit)
        print(f'Цели: {self.target_slots}')

    def auto_fight(self):
        """Автобой"""
        self.autofight = True
        if self.units_in_round:

            if self.current_unit.attack_type not in [
                    'Лечение', 'Лечение/Исцеление', 'Лечение/Воскрешение']:

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
                        self.current_unit, self.player1.slots)
                    # for target_slot in heal_targets:
                    #     target = self.get_unit_by_slot(
                    #         target_slot,
                    #         self.player1.units)
                    #     self.current_unit.heal(target)

                elif self.current_unit in self.player2.units:
                    heal_targets = self.choose_healed(
                        self.current_unit, self.player2.slots)
                    for target_slot in heal_targets:
                        target = self.get_unit_by_slot(
                            target_slot,
                            self.player2.units)
                        self.current_unit.heal(target)

            self.units_deque.append(self.current_unit)
        else:
            self.new_round()

        self._alive_getting_experience()

    def _getting_experience(self, player1, player2, pl_database):
        """Получение опыта юнитами"""
        self.alive_units = []
        killed_units = player1.units
        self.get_player_slots(player2)

        for unit in killed_units:
            self.en_exp_killed += unit.exp_per_kill

        for slot in player2.slots:
            alive_unit = self.get_unit_by_slot(
                slot, player2.units)

            if alive_unit.exp != 'Максимальный':
                exp_value = int(self.en_exp_killed / len(player2.slots))
                if exp_value < alive_unit.exp:
                    if alive_unit.curr_exp + exp_value >= alive_unit.exp:
                        alive_unit.lvl_up()
                        self.alive_units.append(alive_unit.slot)
                    else:
                        alive_unit.curr_exp += exp_value

                        # if player2.name == 'Computer':
                        #     print('player Computer')
                        #     self.database.update_unit_exp(
                        #         alive_unit.slot,
                        #         alive_unit.curr_exp,
                        #         self.database.CurrentDungeon
                        #     )
                        if player2.name != 'Computer':
                            self.database.update_unit_exp(
                                alive_unit.slot,
                                alive_unit.curr_exp,
                                pl_database
                            )
                else:
                    alive_unit.lvl_up()
                    self.alive_units.append(alive_unit.slot)

    def _alive_getting_experience(self):
        """Повышение опыта или уровня выжившим юнитам"""
        self.get_player_slots(self.player1)
        self.get_player_slots(self.player2)
        if not self.player1.slots:
            logging('Вы проиграли!\n')

            self._getting_experience(self.player1, self.player2,
                                     self.database.Player2Units)
            self.battle_is_over = True

        if not self.player2.slots:
            logging('Вы победили!\n')

            self._getting_experience(self.player2, self.player1,
                                     self.database.PlayerUnits)
            self.battle_is_over = True

    def player_attack(self, player: Player):
        """Атака по выбранному игроку"""
        if self.autofight:
            if self.target_slots == [None]:
                self.attacked_slots = []
                self.current_unit.defence()

            elif self.current_unit.attack_radius == ANY_UNIT \
                    and self.current_unit.attack_purpose == 6:
                self.attacked_slots = []
                for target_slot in self.target_slots:
                    target = self.get_unit_by_slot(
                        target_slot,
                        player.units)
                    success = self.current_unit.attack(target)

                    if success:
                        self.attacked_slots.append(target.slot)
            else:
                self.attacked_slots = []
                self.target = self.get_unit_by_slot(
                    # self.target_slots[0],
                    random.choice(self.target_slots),
                    player.units)
                success = self.current_unit.attack(self.target)

                if success:
                    self.attacked_slots.append(self.target.slot)

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
            # return random.choice([slot_a, slot_b])
            return [slot_a, slot_b]
        if slot_a in tg_slots:
            return [slot_a]
        if slot_b in tg_slots:
            return [slot_b]
        if slot_a not in tg_slots and slot_b not in tg_slots and slot_c in tg_slots:
            return [slot_c]
        return None

    @staticmethod
    def closest_middle_slot(tg_slots, slot_a: int, slot_b: int, slot_c: int):
        """Вычисление рандомной цели для среднего слота"""
        if slot_a in tg_slots and slot_b in tg_slots and slot_c in tg_slots:
            return [slot_a, slot_b, slot_c]
        if slot_a in tg_slots and slot_b in tg_slots:
            return [slot_a, slot_b]
        if slot_b in tg_slots and slot_c in tg_slots:
            return [slot_b, slot_c]
        if slot_c in tg_slots and slot_a in tg_slots:
            return [slot_c, slot_a]
        if slot_a in tg_slots:
            return [slot_a]
        if slot_b in tg_slots:
            return [slot_b]
        if slot_c in tg_slots:
            return [slot_c]
        return None

    def define_closest_slots(self, unit, target_slots, alies_slots):
        """Определение ближайшего слота для текущего юнита"""
        result = [None]
        vanguard_alies_died = 2 not in alies_slots and \
            4 not in alies_slots and \
            6 not in alies_slots
        vanguard_enemies_died = 2 not in target_slots and \
            4 not in target_slots and \
            6 not in target_slots

        targets_dict = {
            1: self.closest_side_slot(
                target_slots,
                1, 3, 5),
            2: self.closest_side_slot(
                target_slots,
                2, 4, 6),
            3: self.closest_middle_slot(
                target_slots,
                3, 1, 5),
            4: self.closest_middle_slot(
                target_slots,
                4, 2, 6),
            5: self.closest_side_slot(
                target_slots,
                5, 3, 1),
            6: self.closest_side_slot(
                target_slots,
                6, 4, 2),
        }

        if (vanguard_enemies_died and
                vanguard_alies_died):  # Авангард мертв, Авангард врага мертв
            if unit.slot % 2 == 1:
                result = targets_dict[unit.slot]

        elif vanguard_enemies_died:  # Авангард мертв
            if unit.slot % 2 == 0:
                result = targets_dict[unit.slot - 1]

        elif (not vanguard_enemies_died and
              vanguard_alies_died):  # Авангард мертв, Авангард врага жив
            if unit.slot % 2 == 1:
                result = targets_dict[unit.slot + 1]

        elif not vanguard_enemies_died:  # Авангард врага жив
            if unit.slot % 2 == 0:
                result = targets_dict[unit.slot]

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
            targets = self.define_closest_slots(
                unit, target_slots, attacker_slots)
            if targets != [None]:
                return targets
        if unit.attack_radius == ANY_UNIT and unit.attack_purpose == 6:
            return target_slots
        if unit.attack_radius == ANY_UNIT and unit.attack_purpose == 1:
            # target = random.choice(target_slots)
            # return [target]
            return target_slots
        return [None]

    def auto_choose_target(self, unit):
        """Авто определение следующей цели для атаки"""
        self.get_player_slots(self.player1)
        self.get_player_slots(self.player2)

        if unit.attack_type \
                not in ['Лечение', 'Лечение/Исцеление', 'Лечение/Воскрешение']:
            if unit in self.player1.units:
                return self.choose_target(
                    unit, self.player1.slots, self.player2.slots)
            if unit in self.player2.units:
                return self.choose_target(
                    unit, self.player2.slots, self.player1.slots)
        return None

    @staticmethod
    def get_player_slots(player: Player):
        """Получение слотов с живыми юнитами игрока"""
        player.slots = []
        for unit in player.units:
            if unit is not None and not unit.curr_health <= 0:
                player.slots.append(unit.slot)
