"""Battle"""
import random
from collections import deque
from typing import List, Optional

from client_dir.settings import ANY_UNIT, CLOSEST_UNIT, \
    HEAL_LIST, ALCHEMIST_LIST, PARALYZE_LIST, PARALYZE_UNITS
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
            branch = unit.curr_health / unit.health  # тут править
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
        self.current_unit.off_defence()

        line = f'Ходит: {self.current_unit.name}\n'
        logging(line)

        # Получение периодического урона
        if self.current_unit in self.dotted_units and \
                self.current_unit.dotted:
            self.take_dot_damage()

        # если юнит жив
        if self.current_unit.curr_health > 0:

            if self.current_unit in self.player1.units:
                self.define_target_player(self.player1, self.player2)

            else:
                self.define_target_player(self.player2, self.player1)

        self.target_slots = self._auto_choose_targets(self.current_unit)

    def logging_dot(self, dot_source, dot_dmg) -> None:
        """Логирование периодического урона"""
        line = f'{dot_source} наносит урон {dot_dmg} воину ' \
               f'{self.current_unit.name}. ' \
               f'Осталось ХП: {self.current_unit.curr_health}\n'
        logging(line)

    def logging_paralyze(self, dot_source) -> None:
        """Логирование паралича и окаменения"""
        line = f'На воина {self.current_unit.name} ' \
               f'действует {dot_source}. ' \
               f'{self.current_unit.name} пропускает ход\n'
        logging(line)

    def take_dot_damage(self):
        """Получение периодического урона от эффектов текущим юнитом"""
        # флаг паралича, нужен для того, чтобы сначала отработали все доты
        paralyzed = False

        for dot_source, dot_params in \
                self.dotted_units[self.current_unit].items():
            # если юнит все еще жив
            if self.current_unit.curr_health > 0:
                dot_dmg = dot_params[0]  # урон
                dot_rounds = dot_params[1]  # раунды

                # если остались раунды у текущего эффекта
                if dot_rounds:
                    # Если периодический урон
                    if dot_dmg != 0:
                        dot_dmg = min(self.current_unit.curr_health, dot_dmg)

                        self.current_unit.curr_health -= dot_dmg
                        # логирование
                        self.logging_dot(dot_source, dot_dmg)

                    # Если Паралич
                    else:
                        paralyzed = True

                        # уменьшаем кол-во раундов
                        self.current_unit.dotted -= 1

                        # логирование
                        self.logging_paralyze(dot_source)

                # уменьшаем раунды на 1
                dot_rounds = max(0, dot_rounds - 1)
                if self.current_unit.dotted == 0:
                    self.dotted_units.pop(self.current_unit)
                else:
                    self.dotted_units[self.current_unit][dot_source] = \
                        [dot_dmg, dot_rounds]

        # Если Паралич, пропускаем ход
        if paralyzed:
            self.are_units_in_round()

    def are_units_in_round(self) -> None:
        """Проверка на наличие юнитов в раунде"""
        if self.current_unit in self.units_in_round:
            self.units_in_round.remove(
                self.current_unit)

        # есть не ходившие юниты в текущем раунде
        if self.units_in_round:
            self.next_turn()

        # есть юниты, ожидающие лучшего момента
        elif self.waiting_units:
            self.waiting_round()
            self.next_turn()

        else:
            # новый раунд
            self.new_round()
            # следующий ход
            self.next_turn()

    def define_target_player(self,
                             allied_player: Player,
                             enemy_player: Player) -> None:
        """
        Определение цели для текущего юнита в зависимости
        от типа атаки (сам игрок или противник)
        """
        self.current_player = allied_player
        if self.current_unit.attack_type not in HEAL_LIST and \
                self.current_unit.attack_type not in ALCHEMIST_LIST:
            self.target_player = enemy_player
        else:
            self.target_player = allied_player

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

        self.alive_getting_experience()

    def append_alive_unit(self,
                          alive_unit: Unit,
                          exp_value: int,
                          player: Player,
                          pl_database: any) -> None:
        """
        Получение опыта, либо уровня выжившим юнитом.
        Добавление юнита в alive_units для отображения на fight_window
        """
        # полученный опыт < макс. опыт выжившего юнита
        if exp_value < alive_unit.exp:
            # полученного опыта достаточно для повышения уровня
            if alive_unit.curr_exp + exp_value >= alive_unit.exp:
                alive_unit.lvl_up()
                self.alive_units.append(alive_unit.slot)
            else:
                alive_unit.curr_exp += exp_value

                if player.name != 'Computer':
                    main_db.update_unit_exp(
                        alive_unit.slot,
                        alive_unit.curr_exp,
                        pl_database)

            # полученный опыт > макс. опыт выжившего юнита
        else:
            alive_unit.lvl_up()
            self.alive_units.append(alive_unit.slot)

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

                self.append_alive_unit(alive_unit,
                                       exp_value,
                                       player2,
                                       pl_database)

    def alive_getting_experience(self) -> None:
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

    def dot_calculations(self,
                         dot_source: str,
                         target: Unit) -> None:
        """Вычисление периодического урона и раундов"""
        # урон
        dot_dmg = self.current_unit.dot_dmg

        # раунды
        if dot_source in PARALYZE_LIST:
            dot_dmg = 0
            if self.current_unit.name in PARALYZE_UNITS:
                dot_rounds = 1
            else:
                dot_rounds = random.choice(range(1, 4))
        else:
            dot_rounds = random.choice(range(2, 6))

        if self.dotted_units.get(target):
            dot_dict = self.dotted_units[target]

            if dot_dict.get(dot_source):
                if dot_dict[dot_source][0] < dot_dmg:
                    dot_dict[dot_source][0] = dot_dmg

                if dot_dict[dot_source][1] < dot_rounds:
                    dot_dict[dot_source][1] = dot_rounds
            else:
                dot_dict[dot_source] = [dot_dmg, dot_rounds]
        else:
            dot_dict = {dot_source: [dot_dmg, dot_rounds]}

        self.dotted_units[target] = dot_dict

        target.dotted = max(dot_rounds, target.dotted)

        line = f"На {target.name} будет оказывать воздействие " \
               f"{dot_source} в течение " \
               f"{dot_rounds} раунд(ов)\n"
        logging(line)

    def attack_6_units(self, player: Player) -> None:
        """Если цели - 6 юнитов"""
        self.attacked_slots = []
        for target_slot in self.target_slots:
            target = self.get_unit_by_slot(
                target_slot,
                player.units)
            self.attack_1_unit(target)

    def attack_1_unit(self, target: Optional[Unit]) -> None:
        """Если цель - 1 юнит"""
        attack_type = self.current_unit.attack_type
        curr_unit = self.current_unit

        # Если текущий юнит - атакующий
        if attack_type \
                not in [*HEAL_LIST, *ALCHEMIST_LIST, *PARALYZE_LIST]:
            success = curr_unit.attack(target)

            if (success and curr_unit.dot_dmg) \
                    or (success and curr_unit.dot_dmg == 0):
                dot_success = curr_unit.dot_attack(target)
                dot_source = attack_type.split('/')[1]

                if dot_success:
                    self.dot_calculations(dot_source, target)

        # Если текущий юнит - лекарь
        elif attack_type in HEAL_LIST:
            success = curr_unit.heal(target)

            if 'Исцеление' in attack_type and target.dotted:
                self.dotted_units.pop(target)
                success = curr_unit.cure(target)

        # Если текущий юнит - Друид/Алхимик
        elif attack_type in ALCHEMIST_LIST:
            if 'Увеличение урона' in attack_type:
                if target not in self.boosted_units:

                    success = curr_unit.increase_damage(target)
                    self.boosted_units[target] = curr_unit.attack_dmg

                elif self.boosted_units.get(target):
                    if self.boosted_units[target] < curr_unit.attack_dmg:
                        target.attack_dmg = \
                            int(target.attack_dmg * 100 /
                                (100 + self.boosted_units[target]))

                        success = curr_unit.increase_damage(target)
                        self.boosted_units[target] = curr_unit.attack_dmg

                    elif (target in self.boosted_units
                        or self.boosted_units[target] >=
                        curr_unit.attack_dmg) \
                            and 'Исцеление' not in attack_type:
                        success = False
                        curr_unit.defence()

                if 'Исцеление' in attack_type and target.dotted:

                    self.dotted_units.pop(target)
                    success = curr_unit.cure(target)

        # Для воинов с основной атакой типа Паралич и Окаменение
        elif attack_type in PARALYZE_LIST:
            success = curr_unit.dot_attack(target)
            dot_source = attack_type

            if success:
                self.dot_calculations(dot_source, target)

        if success:
            self.attacked_slots.append(target.slot)

    def player_attack(self, target: Unit) -> None:
        """Атака игрока по цели"""
        if self.units_in_round:

            if self.current_unit.attack_radius == ANY_UNIT \
                    and self.current_unit.attack_purpose == 6:
                self.attack_6_units(self.target_player)
            else:
                self.attacked_slots = []
                self.attack_1_unit(target)

        else:
            self.new_round()
            self.next_turn()

        self.alive_getting_experience()

    def auto_attack(self) -> None:
        """Автоматическая атака игрока по противнику"""
        # if self.autofight:

        if not self.target_slots:
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
            if self.current_unit.attack_type \
                    not in [*HEAL_LIST, *ALCHEMIST_LIST, *PARALYZE_LIST]:
                # определяем приоритет для атаки
                target = self.get_priority_target(
                    self.current_unit, self.target_slots)

                if not target:
                    # self.current_unit.defence()
                    self.target_slots = []
                else:
                    self.attack_1_unit(target)

            elif self.current_unit.attack_type in HEAL_LIST:
                # определяем приоритет для лекарей
                target = self.get_heal_target(self.target_slots)

                if target.curr_health == target.health:
                    # self.current_unit.defence()
                    self.target_slots = []
                else:
                    self.attack_1_unit(target)

            elif self.current_unit.attack_type in ALCHEMIST_LIST:
                # определяем приоритет для друидов/алхимиков
                target = self.get_druid_target(self.target_slots)

                if not target:
                    # self.current_unit.defence()
                    self.target_slots = []
                else:
                    self.attack_1_unit(target[0])

            elif self.current_unit.attack_type in PARALYZE_LIST:
                # определяем приоритет для парализаторов
                target = self.get_paralyze_target(self.target_slots)

                if not target:
                    # self.current_unit.defence()
                    self.target_slots = []
                else:
                    self.attack_1_unit(target)

    def get_priority_target(self,
                              unit: Unit,
                              target_slots: List[int]) -> Unit:
        """Получить приоритетную для атаки цель"""
        first_priority = []
        second_priority = []
        third_priority = []
        target_units = []

        for slot in target_slots:
            unit_ = self.get_unit_by_slot(slot, self.target_player.units)
            target_units.append(unit_)

        for target_unit in target_units:
            try:
                attack_source = unit.attack_source.split('/')[0]
            except IndexError:
                attack_source = unit.attack_source

            target_armor = (1 - target_unit.armor * 0.01)

            if attack_source not in target_unit.immune:

                # убьет цель за 1 ход
                if target_unit.curr_health <= \
                        unit.attack_dmg * target_armor:
                    first_priority.append(target_unit)

                # убьет цель за 2 хода
                elif target_unit.curr_health <= \
                        unit.attack_dmg * 2 * target_armor:
                    second_priority.append(target_unit)

                # иначе добавляем всех попавшихся
                else:
                    third_priority.append(target_unit)

        if first_priority:
            target = self.attack_priority(first_priority)

        elif not first_priority and second_priority:
            target = self.attack_priority(second_priority)

        else:
            target = self.attack_priority(third_priority)

        return target

    def attack_priority(self, targets: list) -> Unit:
        """Определение приоритета для атаки"""
        result_target = None

        for target in targets:
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
            if targets:
                weakest_unit = self.sorting_health(targets)[0]
                result_target = weakest_unit
            else:
                result_target = None

        return result_target

    def get_heal_target(self, target_slots: List[int]) -> Unit:
        """Получить приоритетную для лечения цель"""
        target_units = []

        for slot in target_slots:
            unit = self.get_unit_by_slot(slot, self.target_player.units)
            target_units.append(unit)

        health_sorted_units = self.sorting_health_percentage(target_units)

        return health_sorted_units[0]

    def get_druid_target(self, target_slots: List[int]) -> List[Unit]:
        """Получение приоритетной для Друида/Алхимика цели"""
        target_units = []

        for slot in target_slots:
            unit = self.get_unit_by_slot(
                slot,
                self.target_player.units)

            if (unit.dotted
                and 'Исцеление' in self.current_unit.attack_type) \
                    or \
                    (unit not in self.boosted_units \
                     and unit.attack_dmg != 0):
                # if unit not in self.boosted_units:
                target_units.append(unit)

            # усиленный юнит усилен на меньший процент
            if self.boosted_units.get(unit):
                if self.boosted_units[unit] < self.current_unit.attack_dmg:
                    target_units.append(unit)

        damage_sorted_units = self.sorting_damage(target_units)

        return damage_sorted_units

    def get_paralyze_target(self, target_slots: List[int]) -> Unit:
        """Получение приоритетной для парализатора цели"""
        target_units = []

        for slot in target_slots:
            unit = self.get_unit_by_slot(
                slot,
                self.target_player.units)
            if self.current_unit.attack_type not in unit.immune:
                target_units.append(unit)

        damage_sorted_units = self.sorting_damage(target_units)

        return damage_sorted_units[0]

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
        return []

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
        return []

    def _define_closest_slots(self,
                              unit: Unit,
                              target_slots: List[int],
                              alies_slots: List[int]) -> Optional[List[int]]:
        """Определение ближайшего слота для текущего юнита"""
        result = []
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

        if (vanguard_enemies_died
                and vanguard_alies_died):  # Авангард мертв, Авангард врага мертв
            if unit.slot % 2 == 1:
                result = targets_dict[unit.slot]

        elif vanguard_enemies_died:  # Авангард мертв
            if unit.slot % 2 == 0:
                result = targets_dict[unit.slot - 1]

        elif (not vanguard_enemies_died
              and vanguard_alies_died):  # Авангард мертв, Авангард врага жив
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
                unit,
                target_slots,
                attacker_slots)
            if targets:
                return targets

        # Для дальнобойных юнитов
        if unit.attack_radius == ANY_UNIT \
                and unit.attack_purpose in [1, 6]:
            return target_slots

        return []

        #     # ----------------------------------------------------------
        #     target_units = []
        #
        #     for slot in target_slots:
        #         unit_ = self.get_unit_by_slot(slot, self.target_player.units)
        #         target_units.append(unit_)
        #
        #     for target_unit in target_units:
        #         try:
        #             attack_source = unit.attack_source.split('/')[0]
        #         except IndexError:
        #             attack_source = unit.attack_source
        #
        #         if attack_source in target_unit.immune:
        #             targets.remove(target_unit.slot)
        # ----------------------------------------------------------


    def _auto_choose_targets(self, unit: Unit) -> Optional[List[int]]:
        """Авто определение следующих целей для атаки"""
        self.get_player_slots(self.player1)
        self.get_player_slots(self.player2)

        return self._choose_targets(
            unit,
            self.current_player.slots,
            self.target_player.slots)

    @staticmethod
    def get_player_slots(player: Player) -> None:
        """Получение слотов с живыми юнитами игрока"""
        player.slots = []
        for unit in player.units:
            if unit is not None and not unit.curr_health <= 0:
                player.slots.append(unit.slot)
