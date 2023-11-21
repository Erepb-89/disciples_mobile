"""Battle"""
import random
from collections import deque
from typing import List, Optional

from client_dir.settings import ANY_UNIT, CLOSEST_UNIT, \
    HEAL_LIST, ALCHEMIST_LIST
from battle_logging import logging
from units_dir.units import main_db
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
    """
    Класс - битва.
    Содержит всю основную логику битвы,
    очередность ходов, действия игроков и т.д.
    """

    def __init__(self, dungeon: str):
        # super().__init__()
        # основные переменные
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
        self.dotted_units = {}
        self.boosted_units = {}

        self.player1 = Player(PLAYER1_NAME)
        self.player2 = Player(PLAYER2_NAME)

        self.dungeon_units = main_db.show_dungeon_units(dungeon)

        if self.player2.name == "Computer":
            self.add_dung_units()
        else:
            self.add_player_units(
                self.player2,
                main_db.Player2Units)

        self.add_player_units(
            self.player1,
            main_db.PlayerUnits)
        self.new_round()
        self.next_turn()

    @staticmethod
    def add_player_unit(slot: int,
                        player: Player,
                        database: any) -> None:
        """
        Добавление одного юнита игрока по слоту в текущую битву.
        """
        unit = main_db.get_unit_by_slot(
            slot,
            database)

        player.units.append(Unit(unit))
        player.slots.append(unit.slot)

    @staticmethod
    def add_player_units(player: Player,
                         database: any) -> None:
        """
        Добавление юнитов игрока в текущую битву.
        Выполняется в начале каждой новой битвы.
        """
        player.units = []
        for pl_slot in range(1, 7):
            unit = main_db.get_unit_by_slot(
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
                unit = main_db.get_unit_by_name(
                    self.dungeon_units[unit_slot])[:25]
                unit_cols_after_slot = main_db.get_unit_by_name(
                    self.dungeon_units[unit_slot])[26:45]

                main_db.add_dungeon_unit(
                    *unit,
                    unit_slot + 1,
                    *unit_cols_after_slot)

                unit = self.dungeon_unit_by_slot(unit_slot + 1)
                if unit is not None:
                    self.player2.units.append(Unit(unit))
                    if not unit.curr_health <= 0:
                        self.player2.slots.append(unit.slot)
            except (TypeError, AttributeError):
                pass

    @staticmethod
    def dungeon_unit_by_slot(slot) -> Unit:
        """Метод получающий юнита подземелья по слоту."""
        return main_db.get_unit_by_slot(
            slot,
            main_db.CurrentDungeon)

    @staticmethod
    def get_unit_by_slot(slot: int,
                         player_units: List[Unit]) -> Optional[Unit]:
        """Метод получающий юнита по слоту."""
        for player_unit in player_units:
            if player_unit.slot == slot:
                return player_unit
        return None

    @staticmethod
    def sorting_ini(all_units: list) -> List[Unit]:
        """Сортировка юнитов по инициативе"""
        units_ini = {}
        for unit in all_units:
            ini = unit.attack_ini + random.randrange(-4, 5)
            units_ini[unit] = ini

        sorted_units_by_ini = sorted(
            units_ini, key=units_ini.get, reverse=True)
        return sorted_units_by_ini

    @staticmethod
    def sorting_health_percentage(units: list) -> List[Unit]:
        """Сортировка юнитов по процентам оставшегося здоровья"""
        percentage = {}
        for unit in units:
            perc = unit.curr_health / unit.health
            percentage[unit] = perc

        sorted_units_by_perc = sorted(
            percentage, key=percentage.get, reverse=False)
        return sorted_units_by_perc

    @staticmethod
    def sorting_health(units: list) -> List[Unit]:
        """Сортировка юнитов по текущему здоровью в единицах"""
        health = {}
        for unit in units:
            health[unit] = unit.curr_health

        sorted_units_by_health = sorted(
            health, key=health.get, reverse=False)
        return sorted_units_by_health

    @staticmethod
    def sorting_damage(units: list) -> List[Unit]:
        """Сортировка юнитов по урону"""
        damage = {}
        for unit in units:
            if unit.attack_type not in HEAL_LIST and \
                    unit.attack_type not in ALCHEMIST_LIST:
                damage[unit] = unit.attack_dmg

        sorted_units_by_damage = sorted(
            damage, key=damage.get, reverse=True)
        return sorted_units_by_damage

    @staticmethod
    def sorting_unit_types(units: list) -> List[Unit]:
        """Сортировка юнитов по типам/ветвям: Маги, Стрелки и т.д."""
        branches = {}
        for unit in units:
            branch = unit.curr_health / unit.health # тут править
            branches[unit] = branch

        sorted_units_by_branch = sorted(
            branches, key=branches.get, reverse=False)
        return sorted_units_by_branch

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
        sorted_units_by_ini = self.sorting_ini(all_units)

        for unit in sorted_units_by_ini:
            self.units_deque.append(unit)
            self.units_in_round.append(unit)

    def next_turn(self) -> None:
        """Ход юнита"""
        self.current_unit = self.units_deque.popleft()
        self.current_unit.undefence()

        line = f'Ходит: {self.current_unit.name}\n'
        logging(line)

        if self.current_unit in self.dotted_units:
            dot_dmg = self.dotted_units[self.current_unit]
            dot_dmg = min(self.current_unit.curr_health, dot_dmg)

            self.current_unit.curr_health -= dot_dmg

            line = f'{self.current_unit.name} получает урон {dot_dmg} ядом. ' \
                   f'Осталось ХП: {self.current_unit.curr_health}\n'
            logging(line)

        # если юнит жив
        if self.current_unit.curr_health > 0:

            if self.current_unit in self.player1.units:
                self.current_player = self.player1
                if self.current_unit.attack_type not in HEAL_LIST and \
                        self.current_unit.attack_type not in ALCHEMIST_LIST:
                    self.target_player = self.player2
                else:
                    self.target_player = self.player1
            else:
                self.current_player = self.player2
                if self.current_unit.attack_type not in HEAL_LIST and \
                        self.current_unit.attack_type not in ALCHEMIST_LIST:
                    self.target_player = self.player1
                else:
                    self.target_player = self.player2

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
        exp_enhanced = 0
        self.get_player_slots(player2)

        for unit in player2.units:
            if unit.weapon_master:
                exp_enhanced = 1

        for unit in killed_units:
            self.en_exp_killed += unit.exp_per_kill

        extra_exp = self.en_exp_killed * exp_enhanced * 0.25

        for slot in player2.slots:
            alive_unit = self.get_unit_by_slot(
                slot, player2.units)

            if alive_unit.exp != 'Максимальный':
                exp_value = int((self.en_exp_killed + extra_exp)
                                / len(player2.slots))
                if exp_value < alive_unit.exp:
                    if alive_unit.curr_exp + exp_value >= alive_unit.exp:
                        alive_unit.lvl_up()
                        self.alive_units.append(alive_unit.slot)
                    else:
                        alive_unit.curr_exp += exp_value

                        # if player2.name == 'Computer':
                        #     print('player Computer')
                        #     main_db.update_unit_exp(
                        #         alive_unit.slot,
                        #         alive_unit.curr_exp,
                        #         main_db.CurrentDungeon
                        #     )
                        if player2.name != 'Computer':
                            main_db.update_unit_exp(
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
                                     main_db.Player2Units)
            self.battle_is_over = True

        if not self.player2.slots:
            logging('Вы победили!\n')

            self._getting_experience(self.player2, self.player1,
                                     main_db.PlayerUnits)
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
        # Если текущий юнит - атакующий
        if self.current_unit.attack_type not in HEAL_LIST and \
                self.current_unit.attack_type not in ALCHEMIST_LIST:
            success = self.current_unit.attack(target)

            if success and self.current_unit.dot_dmg:
                dot_success = self.current_unit.dot_attack(target)

                if dot_success:
                    self.dotted_units[target] = self.current_unit.dot_dmg
                    print(self.dotted_units)

                    line = f'{target.name} отравлен ядом\n'
                    logging(line)

        # Если текущий юнит - лекарь
        elif self.current_unit.attack_type in HEAL_LIST:
            success = self.current_unit.heal(target)

        # Если текущий юнит - Друид/Алхимик
        elif self.current_unit.attack_type in ALCHEMIST_LIST:
            if 'Увеличение урона' in self.current_unit.attack_type:
                # поправить, сейчас можно увеличивать дмг бесконечно
                success = self.current_unit.increase_damage(target)

                self.boosted_units[target] = self.current_unit.attack_dmg
            else:
                success = False
                self.current_unit.defence()

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
            # рандомная атака
            # target = self.get_unit_by_slot(
            #     random.choice(self.target_slots),
            #     self.target_player.units)

            # атака/лечение определенного юнита
            if self.current_unit.attack_type not in HEAL_LIST and \
                    self.current_unit.attack_type not in ALCHEMIST_LIST:
                # определяем приоритет для атаки
                target = self.getting_attack_target(
                    self.current_unit, self.target_slots)

                self.attack_1_unit(target)

            elif self.current_unit.attack_type in HEAL_LIST:
                # определяем приоритет для лечения
                target = self.getting_heal_target(self.target_slots)
                if target.curr_health == target.health:
                    self.current_unit.defence()
                else:
                    self.attack_1_unit(target)

            elif self.current_unit.attack_type in ALCHEMIST_LIST:
                # определяем приоритет для друидов/алхимиков
                # self.current_unit.defence()

                target = self.getting_druid_target(self.target_slots)
                if not target:
                    self.current_unit.defence()
                else:
                    self.attack_1_unit(target[0])

    def getting_attack_target(self, unit, target_slots) -> Unit:
        """Приоритет для атаки"""
        prior1_targets = []
        prior2_targets = []
        prior3_targets = []
        target_units = []

        for slot in target_slots:
            unit_ = self.get_unit_by_slot(slot, self.target_player.units)
            target_units.append(unit_)

        for target_unit in target_units:
            target_armor = (1 - target_unit.armor * 0.01)

            # убьет цель за 1 ход
            if target_unit.curr_health <= \
                    unit.attack_dmg * target_armor:
                prior1_targets.append(target_unit)

            # убьет цель за 2 хода
            elif target_unit.curr_health <= \
                    unit.attack_dmg * 2 * target_armor:
                prior2_targets.append(target_unit)

            # иначе добавляем всех попавшихся
            else:
                prior3_targets.append(target_unit)

        if prior1_targets:
            target = self.attack_priority(prior1_targets)
        elif not prior1_targets and prior2_targets:
            target = self.attack_priority(prior2_targets)
        else:
            target = self.attack_priority(prior3_targets)

        return target

    def attack_priority(self, prior_targets: list) -> Unit:
        """Приоритет для атаки"""
        result_target = None

        for target in prior_targets:
            # В первую очередь бьем лекарей
            if target.branch == 'support' and \
                    target.attack_source in HEAL_LIST:
                result_target = target

            # Во вторую - бьем магов
            elif target.branch == 'mage':
                result_target = target

            # Во третью - бьем стрелков
            elif target.branch == 'archer':
                result_target = target

        # В остальных случаях
        if result_target is None:
            # выбираем слабейшего из оставшихся (по абсолютному здоровью)
            weakest_unit = self.sorting_health(prior_targets)[0]
            result_target = weakest_unit

        return result_target

    def getting_heal_target(self, target_slots) -> Unit:
        """Приоритет для лечения"""
        target_units = []

        for slot in target_slots:
            unit = self.get_unit_by_slot(slot, self.target_player.units)
            target_units.append(unit)

        health_sorted_units = self.sorting_health_percentage(target_units)

        return health_sorted_units[0]

    def getting_druid_target(self, target_slots) -> List[Unit]:
        """Приоритет для Друида/Алхимика"""
        target_units = []

        for slot in target_slots:
            unit = self.get_unit_by_slot(slot, self.target_player.units)
            if unit not in self.boosted_units:
                target_units.append(unit)

        damage_sorted_units = self.sorting_damage(target_units)

        return damage_sorted_units

    @staticmethod
    def clear_dungeon() -> None:
        """Очистка текущего подземелья от вражеских юнитов"""
        main_db.delete_dungeon_unit(1)
        main_db.delete_dungeon_unit(2)
        main_db.delete_dungeon_unit(3)
        main_db.delete_dungeon_unit(4)
        main_db.delete_dungeon_unit(5)
        main_db.delete_dungeon_unit(6)

    @staticmethod
    def regen() -> None:
        """Восстановление здоровья всех юнитов игрока"""
        # self.clear_dungeon()
        main_db.autoregen(1)
        main_db.autoregen(2)
        main_db.autoregen(3)
        main_db.autoregen(4)
        main_db.autoregen(5)
        main_db.autoregen(6)

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
