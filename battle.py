"""Battle"""
import random
from collections import deque
from typing import List, Optional

from client_dir.settings import ANY_UNIT, CLOSEST_UNIT
from battle_logging import logging
from units_dir.units_factory import Unit

PLAYER1_NAME = 'Erepb-89'
PLAYER2_NAME = 'Computer'


class Player:
    """Класс Игрок"""

    def __init__(self, name: str):
        self.name = name
        self.units = []
        self.slots = []

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.name!r},'
                f' units: {self.units!r},'
                f' slots: {self.slots!r})')

    def __str__(self):
        return f'Игрок: {self.name}'


class Battle:
    """Класс битвы"""

    def __init__(self, database: any, dungeon: str):
        # super().__init__()
        # основные переменные
        self.database = database
        self.autofight = False
        self.units_deque = deque()
        self.waiting_units = []
        self.target_slots = []
        self.attacked_slots = []
        self.current_unit = None
        self.current_player = None
        self.target_player = None
        self.units_in_round = []
        self.en_exp_killed = 0
        self.target = None
        self.battle_is_over = False
        self.alive_units = []
        self.curr_target_slot = 1

        self.player1 = Player(PLAYER1_NAME)
        self.player2 = Player(PLAYER2_NAME)

        # self.current_faction = self.database.current_game_faction

        self.dungeon_units = self.database.show_dungeon_units(dungeon)

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

    def add_player_unit(self,
                        slot: int,
                        player: Player,
                        database: any) -> None:
        """
        Добавление юнита игрока в текущую битву.
        """
        unit = self.database.get_unit_by_slot(
            slot,
            database)

        player.units.append(Unit(unit))
        player.slots.append(unit.slot)

    def add_player_units(self,
                         player: Player,
                         database: any) -> None:
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

    def add_dung_units(self) -> None:
        """
        Добавление юнитов подземелья в текущую битву.
        Выполняется в начале новой битвы с компьютером.
        """
        self.clear_dungeon()
        for unit_slot in range(6):
            try:
                unit = self.database.get_unit_by_name(
                    self.dungeon_units[unit_slot])[:24]

                self.database.add_dungeon_unit(
                    *unit,
                    unit_slot + 1)

                unit = self.dungeon_unit_by_slot(unit_slot + 1)
                if unit is not None:
                    self.player2.units.append(Unit(unit))
                    if not unit.curr_health <= 0:
                        self.player2.slots.append(unit.slot)
            except (TypeError, AttributeError):
                pass

    def dungeon_unit_by_slot(self, slot) -> Unit:
        """Метод получающий юнита подземелья по слоту."""
        return self.database.get_unit_by_slot(
            slot,
            self.database.CurrentDungeon)

    def player_unit_by_slot(self, slot: int) -> Unit:
        """Метод получающий юнита игрока по слоту."""
        return self.database.get_unit_by_slot(
            slot,
            self.database.PlayerUnits)

    @staticmethod
    def get_unit_by_slot(slot: int,
                         player_units: List[Unit]) -> Optional[Unit]:
        """Метод получающий юнита по слоту."""
        for player_unit in player_units:
            if player_unit.slot == slot:
                return player_unit
        return None

    @staticmethod
    def sorting_units(all_units: list) -> List[Unit]:
        """Сортировка юнитов по инициативе"""
        units_ini = {}
        for unit in all_units:
            ini = unit.attack_ini + random.randrange(-4, 5)
            units_ini[unit] = ini

        sorted_units_by_ini = sorted(
            units_ini, key=units_ini.get, reverse=True)
        return sorted_units_by_ini

    def waiting_round(self) -> None:
        """Раунд для ожидающих юнитов"""
        self.units_deque.clear()

        sorted_units_by_ini = reversed(self.waiting_units)

        for unit in sorted_units_by_ini:
            self.units_deque.append(unit)
            self.units_in_round.append(unit)

        self.waiting_units = []

    def new_round(self) -> None:
        """Высчитывание оставшихся выживших в новом раунде"""
        logging('Новый раунд\n')

        self.units_deque.clear()

        units_pl1 = [
            unit for unit in self.player1.units if unit.curr_health != 0]
        units_pl2 = [
            unit for unit in self.player2.units if unit.curr_health != 0]

        all_units = units_pl1 + units_pl2
        sorted_units_by_ini = self.sorting_units(all_units)

        for unit in sorted_units_by_ini:
            self.units_deque.append(unit)
            self.units_in_round.append(unit)

    def next_turn(self) -> None:
        """Ход юнита"""
        self.current_unit = self.units_deque.popleft()
        self.current_unit.undefence()

        if self.current_unit in self.player1.units:
            self.current_player = self.player1
            if self.current_unit.attack_type not in [
                'Лечение', 'Лечение/Исцеление', 'Лечение/Воскрешение']:
                self.target_player = self.player2
            else:
                self.target_player = self.player1
        else:
            self.current_player = self.player2
            if self.current_unit.attack_type not in [
                'Лечение', 'Лечение/Исцеление', 'Лечение/Воскрешение']:
                self.target_player = self.player1
            else:
                self.target_player = self.player2
        line = f'Ходит: {self.current_unit.name}\n'
        logging(line)

        self.target_slots = self._auto_choose_targets(self.current_unit)

    def _get_battle_unit_by_id(self, _id: int) -> Optional[Unit]:
        """Метод возвращает юнита из deque по id"""
        for unit in self.units_deque:
            if unit.id == _id:
                return unit
        return None

    def auto_fight(self) -> None:
        """Автобой"""
        self.autofight = True
        if self.units_in_round:

            self.auto_attack()
        else:
            self.new_round()
            self.next_turn()

        self._alive_getting_experience()

    def _getting_experience(self,
                            player1: Player,
                            player2: Player,
                            pl_database: any) -> None:
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

    def _alive_getting_experience(self) -> None:
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

    def attack_6_units(self, player: Player) -> None:
        """Если цели - 6 юнитов"""
        self.attacked_slots = []
        for target_slot in self.target_slots:
            target = self.get_unit_by_slot(
                target_slot,
                player.units)
            self.attack_1_unit(target)

    def attack_1_unit(self, target: Unit) -> None:
        """Если цель - 1 юнит"""
        if self.current_unit.attack_type \
                not in ['Лечение',
                        'Лечение/Исцеление',
                        'Лечение/Воскрешение']:
            success = self.current_unit.attack(target)
        else:
            # Если текущий юнит - лекарь
            success = self.current_unit.heal(target)

        if success:
            self.attacked_slots.append(target.slot)

    def player_attack(self, curr_target: Unit) -> None:
        """Атака игрока по цели"""
        if self.units_in_round:

            if self.current_unit.attack_radius == ANY_UNIT \
                    and self.current_unit.attack_purpose == 6:
                self.attack_6_units(self.target_player)
            else:
                self.attacked_slots = []
                self.attack_1_unit(curr_target)

        else:
            self.new_round()
            self.next_turn()

        self._alive_getting_experience()

    def auto_attack(self) -> None:
        """Автоматическая атака игрока по противнику"""
        # if self.autofight:

        if self.target_slots == [None]:
            self.attacked_slots = []
            self.current_unit.defence()

        elif self.current_unit.attack_radius == ANY_UNIT \
                and self.current_unit.attack_purpose == 6:
            self.attack_6_units(self.target_player)

        else:
            self.attacked_slots = []
            target = self.get_unit_by_slot(
                random.choice(self.target_slots),
                self.target_player.units)
            self.attack_1_unit(target)

    def clear_dungeon(self) -> None:
        """Очистка текущего подземелья от вражеских юнитов"""
        self.database.delete_dungeon_unit(1)
        self.database.delete_dungeon_unit(2)
        self.database.delete_dungeon_unit(3)
        self.database.delete_dungeon_unit(4)
        self.database.delete_dungeon_unit(5)
        self.database.delete_dungeon_unit(6)

    def regen(self) -> None:
        """Восстановление здоровья всех юнитов игрока"""
        # self.clear_dungeon()
        self.database.autoregen(1)
        self.database.autoregen(2)
        self.database.autoregen(3)
        self.database.autoregen(4)
        self.database.autoregen(5)
        self.database.autoregen(6)

    @staticmethod
    def _closest_side_slot(tg_slots: List[int],
                           slot_a: int,
                           slot_b: int,
                           slot_c: int) -> Optional[List[int]]:
        """Вычисление рандомной цели для крайних слотов"""
        if slot_a in tg_slots and slot_b in tg_slots:
            # return random.choice([slot_a, slot_b])
            return [slot_a, slot_b]
        if slot_a in tg_slots:
            return [slot_a]
        if slot_b in tg_slots:
            return [slot_b]
        if slot_a not in tg_slots and slot_b not in tg_slots \
                and slot_c in tg_slots:
            return [slot_c]
        return [None]

    @staticmethod
    def _closest_middle_slot(tg_slots: List[int],
                             slot_a: int,
                             slot_b: int,
                             slot_c: int) -> Optional[List[int]]:
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
        return [None]

    def _define_closest_slots(self,
                              unit: Unit,
                              target_slots: List[int],
                              alies_slots: List[int]) -> Optional[List[int]]:
        """Определение ближайшего слота для текущего юнита"""
        result = [None]
        vanguard_alies_died = 2 not in alies_slots and \
                              4 not in alies_slots and \
                              6 not in alies_slots
        vanguard_enemies_died = 2 not in target_slots and \
                                4 not in target_slots and \
                                6 not in target_slots

        targets_dict = {
            1: self._closest_side_slot(
                target_slots,
                1, 3, 5),
            2: self._closest_side_slot(
                target_slots,
                2, 4, 6),
            3: self._closest_middle_slot(
                target_slots,
                3, 1, 5),
            4: self._closest_middle_slot(
                target_slots,
                4, 2, 6),
            5: self._closest_side_slot(
                target_slots,
                5, 3, 1),
            6: self._closest_side_slot(
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

    def _choose_targets(self,
                        unit: Unit,
                        attacker_slots: List[int],
                        target_slots: List[int]) -> Optional[List[int]]:
        """Определение следующих целей для атаки"""
        # для контактных юнитов
        if unit.attack_radius == CLOSEST_UNIT:
            targets = self._define_closest_slots(
                unit, target_slots, attacker_slots)
            if targets != [None]:
                return targets

        # Для дальнобойных юнитов
        if unit.attack_radius == ANY_UNIT and unit.attack_purpose in [1, 6]:
            return target_slots

        return [None]

    def _auto_choose_targets(self, unit: Unit) -> Optional[List[int]]:
        """Авто определение следующих целей для атаки"""
        self.get_player_slots(self.player1)
        self.get_player_slots(self.player2)

        return self._choose_targets(
            unit, self.current_player.slots, self.target_player.slots)

    @staticmethod
    def get_player_slots(player: Player) -> None:
        """Получение слотов с живыми юнитами игрока"""
        player.slots = []
        for unit in player.units:
            if unit is not None and not unit.curr_health <= 0:
                player.slots.append(unit.slot)
