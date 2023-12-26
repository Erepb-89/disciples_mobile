"""Battle"""
import random
from collections import deque
from typing import List, Optional, Callable

from client_dir.settings import ANY_UNIT, CLOSEST_UNIT, \
    HEAL_LIST, ALCHEMIST_LIST, PARALYZE_LIST, PARALYZE_UNITS, POLYMORPH
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

    def __init__(self, dungeon: str, db_table: any):
        # super().__init__()
        # основные переменные
        self.autofight = False
        self.units_deque = deque()
        self.waiting_units = []
        self.target_slots = []
        self.targets = []
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
        self.db_table = db_table
        self.enemy_db_table = main_db.CurrentDungeon

        self.next_unit = None

        self.player1 = Player(PLAYER1_NAME)
        self.player2 = Player(PLAYER2_NAME)

        self.dungeon_units = main_db.show_dungeon_units(dungeon)

        if self.player2.name == "Computer":
            self.enemy_db_table = main_db.CurrentDungeon
            self.add_dung_units()
        else:
            self.enemy_db_table = main_db.Player2Units
            self.add_player_units(
                self.player2,
                self.enemy_db_table)

        self.add_player_units(
            self.player1,
            self.db_table)
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
            if unit.attack_type not in (*HEAL_LIST, *ALCHEMIST_LIST):
                if unit.attack_purpose == 6:
                    damage[unit] = unit.attack_dmg * 1.51
                else:
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
        """
        Подсчет оставшихся выживших в новом раунде.
        Создание очередности ходов юнитов согласно инициативе.
        """
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
        if self.next_unit:
            self.current_unit = self.next_unit
            self.next_unit = None
        else:
            self.current_unit = self.units_deque.popleft()

        self.current_unit.off_defence()

        line = f'Ходит: {self.current_unit.name}\n'
        logging(line)

        # Получение периодического урона
        if self.current_unit in self.dotted_units \
                and self.current_unit.dotted:
            self.take_dot_damage()

        # если юнит жив
        if self.current_unit.curr_health > 0:

            if self.current_unit in self.player1.units:
                self.define_target_player(self.player1, self.player2)

            else:
                self.define_target_player(self.player2, self.player1)

        self.target_slots = self._auto_choose_targets(self.current_unit)
        if not self.target_slots:
            self.targets = []

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

                    # Если Паралич или Полиморф
                    elif dot_source in PARALYZE_LIST \
                            or dot_source == POLYMORPH:
                        # уменьшаем кол-во раундов
                        self.current_unit.dotted -= 1

                        if dot_source in PARALYZE_LIST:
                            paralyzed = True

                            # логирование
                            self.logging_paralyze(dot_source)

                    # уменьшаем раунды на 1
                    dot_rounds = max(0, dot_rounds - 1)

                # # Если Полиморф закончил действие
                # if dot_rounds == 0 and dot_source == POLYMORPH:
                #     self.return_shape()

                if self.current_unit.dotted != 0:
                    self.dotted_units[self.current_unit][dot_source] = \
                        [dot_dmg, dot_rounds]

        # Если Паралич, пропускаем ход
        if paralyzed:
            self.are_units_in_round()

    def return_shape(self):
        """
        Возвращение прежней формы юнита
        (после воздействия Полиморфа)
        """
        if self.current_unit in self.player1.units:
            db_table = self.db_table
            self.player1.units.remove(self.current_unit)

        elif self.current_unit in self.player2.units:
            db_table = self.enemy_db_table
            self.player2.units.remove(self.current_unit)

        unit = main_db.get_unit_by_slot(
            self.current_unit.slot, db_table)

        changed_unit = self.replace_polymorph_unit(
            self.current_unit,
            unit.name,
            main_db.unit_by_name_set_params,
            db_table)

        if self.current_unit in self.player1.units:
            self.player1.units.append(changed_unit)

        elif self.current_unit in self.player2.units:
            self.player2.units.append(changed_unit)

        self.units_deque.append(changed_unit)

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

        elif self.next_unit:
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
                          db_table: any) -> None:
        """
        Получение опыта, либо уровня выжившим юнитом.
        Добавление юнита в alive_units для отображения на fight_window
        """
        if player.name != 'Computer':
            # полученный опыт < макс. опыт выжившего юнита
            if exp_value < alive_unit.exp:
                # полученного опыта достаточно для повышения уровня
                if alive_unit.curr_exp + exp_value >= alive_unit.exp:
                    alive_unit.lvl_up(db_table)
                    self.alive_units.append(alive_unit.slot)
                else:
                    alive_unit.curr_exp += exp_value

                    main_db.update_unit_exp(
                        alive_unit.slot,
                        alive_unit.curr_exp,
                        db_table)

                # полученный опыт > макс. опыт выжившего юнита
            else:
                alive_unit.lvl_up(db_table)
                self.alive_units.append(alive_unit.slot)

    def _getting_experience(self,
                            player1: Player,
                            player2: Player,
                            db_table: any) -> None:
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
                                       db_table)

    def alive_getting_experience(self) -> None:
        """Повышение опыта или уровня выжившим юнитам"""
        self.get_player_slots(self.player1)
        self.get_player_slots(self.player2)
        if not self.player1.slots:
            logging('Вы проиграли!\n')

            self._getting_experience(self.player1,
                                     self.player2,
                                     self.enemy_db_table)
            self.battle_is_over = True

        if not self.player2.slots:
            logging('Вы победили!\n')

            self._getting_experience(self.player2,
                                     self.player1,
                                     self.db_table)
            self.battle_is_over = True

    def dot_calculations(self,
                         dot_source: str,
                         target: Unit) -> None:
        """Вычисление периодического урона и раундов"""
        # урон
        dot_dmg = self.current_unit.dot_dmg

        if dot_source in PARALYZE_LIST or \
                dot_source == POLYMORPH:
            dot_dmg = 0

        # раунды
        dot_rounds = self.define_dot_rounds(target, dot_source)

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

        if dot_source != 'Снижение урона':
            target.dotted = max(dot_rounds, target.dotted)

        line = f"На {target.name} будет оказывать воздействие " \
               f"{dot_source} в течение " \
               f"{dot_rounds} раунд(ов)\n"
        logging(line)

    def define_dot_rounds(self, target: Unit, dot_source: str) -> int:
        """
        Определение количества раундов действия эффекта на цель.
        Устанавливает пониженный урон/инициативу.
        """
        if dot_source in PARALYZE_LIST or dot_source == POLYMORPH:
            if self.current_unit.name in PARALYZE_UNITS:
                dot_rounds = 1
            else:
                dot_rounds = random.choice(range(1, 4))

        elif dot_source == 'Снижение урона':
            dot_rounds = 999
            if target in self.dotted_units:
                if not self.dotted_units[target].get(dot_source):
                    target.attack_dmg -= int(target.attack_dmg * 0.325)
            else:
                target.attack_dmg -= int(target.attack_dmg * 0.325)

        elif dot_source == 'Снижение инициативы':
            dot_rounds = random.choice(range(2, 5))

            if target in self.dotted_units:
                if not self.dotted_units[target].get(dot_source):
                    target.attack_ini -= int(target.attack_ini * 0.5)
            else:
                target.attack_ini -= int(target.attack_ini * 0.5)
        else:
            dot_rounds = random.choice(range(2, 6))

        return dot_rounds

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
                not in (*HEAL_LIST,
                        *ALCHEMIST_LIST,
                        *PARALYZE_LIST,
                        POLYMORPH):
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
                self.cure_target(target)
                success = curr_unit.cure(target)

        # Если текущий юнит - Друид/Алхимик
        elif attack_type in ALCHEMIST_LIST:
            # Друид
            if 'Увеличение урона' in attack_type:
                if target not in self.boosted_units \
                        and target.attack_type \
                        not in (*HEAL_LIST, *ALCHEMIST_LIST):

                    success = curr_unit.increase_damage(target)
                    self.boosted_units[target] = curr_unit.attack_dmg

                # если воина уже бафали
                elif self.boosted_units.get(target):
                    if self.boosted_units[target] < curr_unit.attack_dmg:
                        target.attack_dmg = \
                            int((target.attack_dmg + 1) * 100 /
                                (100 + self.boosted_units[target]))

                        success = curr_unit.increase_damage(target)
                        self.boosted_units[target] = curr_unit.attack_dmg

                    elif (target in self.boosted_units
                          or self.boosted_units[target] >=
                          curr_unit.attack_dmg) \
                            and 'Исцеление' not in attack_type:
                        success = False
                        curr_unit.defence()

                # Друид с исцелением
                if 'Исцеление' in attack_type and target.dotted:
                    self.cure_target(target)
                    success = curr_unit.cure(target)

                if target is None:
                    curr_unit.defence()

            # Алхимик
            elif 'Дополнительная атака' in attack_type:
                success = True
                self.next_unit = target

                line = f"{self.current_unit.name} дает дополнительную " \
                       f"атаку воину {target.name}.\n"
                logging(line)

        # Для воинов с основной атакой типа Паралич и Окаменение
        elif attack_type in PARALYZE_LIST:
            success = curr_unit.dot_attack(target)
            dot_source = attack_type

            if success:
                self.dot_calculations(dot_source, target)

        # Для воинов с основной атакой типа Полиморф
        elif attack_type == POLYMORPH:
            success = curr_unit.dot_attack(target)
            dot_source = attack_type

            if success:
                if target.double:
                    changed_unit_name = 'Толстый бес'
                    line = f"{target.name} превращен в Толстого беса.\n"
                else:
                    changed_unit_name = 'Бес'
                    line = f"{target.name} превращён в Беса.\n"

                logging(line)

                changed_unit = self.replace_polymorph_unit(
                    target,
                    changed_unit_name,
                    main_db.unit_by_name_set_params,
                    main_db.AllUnits)

                self.units_deque.append(changed_unit)

                if target in self.player1.units:
                    self.player1.units.remove(target)
                    self.player1.units.append(changed_unit)

                elif target in self.player2.units:
                    self.player2.units.remove(target)
                    self.player2.units.append(changed_unit)

                self.dot_calculations(dot_source, changed_unit)


                # if target in self.units_deque:
                #     self.units_deque.remove(target)
                # if target in self.units_in_round:
                #     self.units_in_round.remove(target)
                # if target in self.waiting_units:
                #     self.waiting_units.remove(target)
                #
                # # Процент (%) оставшегося здоровья цели
                # target_perc_hp = int(target.curr_health / target.health * 100)
                #
                # # Получаем Беса с заданными параметрами
                # changed_unit = Unit(main_db.unit_by_name_set_params(
                #     changed_unit_name,
                #     target.slot,
                #     target_perc_hp))
                #
                # if target in self.player1.units:
                #     self.player1.units.append(changed_unit)
                #     self.player1.units.remove(target)
                #
                # elif target in self.player2.units:
                #     self.player2.units.append(changed_unit)
                #     self.player2.units.remove(target)

        if success:
            self.attacked_slots.append(target.slot)

    def replace_polymorph_unit(self,
                               target: Unit,
                               changed_unit_name: str,
                               func: Callable,
                               db_table: any) -> Unit:
        """Замена юнита на полиморф"""
        if target in self.units_deque:
            self.units_deque.remove(target)
        if target in self.units_in_round:
            self.units_in_round.remove(target)
        if target in self.waiting_units:
            self.waiting_units.remove(target)

        # Процент (%) оставшегося здоровья цели
        target_perc_hp = int(target.curr_health / target.health * 100)

        # Получаем юнит с заданными параметрами
        changed_unit = Unit(func(
            changed_unit_name,
            target.slot,
            target_perc_hp,
            db_table))

        return changed_unit

    def cure_target(self, target: Optional[Unit]) -> None:
        """
        Проверка на исцеление от вредных эффектов.
        Убираются все эффекты, кроме снижения урона
        """
        if target in self.player1.units:
            pl_database = self.db_table
        else:
            pl_database = self.enemy_db_table

        if self.dotted_units[target].get('Снижение урона'):
            if self.dotted_units[target].get('Снижение инициативы'):
                target.off_initiative(pl_database)

            self.dotted_units.pop(target)
            self.dotted_units[target] = {['Снижение урона']: [0, 999]}

        elif self.dotted_units[target].get('Снижение инициативы'):
            target.off_initiative(pl_database)
            self.dotted_units.pop(target)
        else:
            self.dotted_units.pop(target)

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

    @staticmethod
    def find_target(target_slots: List[int],
                    getting_units_func: Callable,
                    sorting_func: Callable) -> Optional[Unit]:
        """Определяет приоритетную цель"""
        target_units = getting_units_func(target_slots)
        sorted_units = sorting_func(target_units)
        if sorted_units:
            target = sorted_units[0]

            return target
        return None

    def find_target_for_all(self, target_slots: List[int]) -> Optional[Unit]:
        """Атака/лечение/усиление/паралич определенного юнита"""
        target = []
        # атака/лечение определенного юнита
        if self.current_unit.attack_type \
                not in (*HEAL_LIST, *ALCHEMIST_LIST, *PARALYZE_LIST):
            # определяем приоритет для атаки
            target = self.get_priority_target(
                self.current_unit, target_slots)

        elif self.current_unit.attack_type in HEAL_LIST:
            # определяем приоритет для лекарей
            target = self.find_target(
                target_slots,
                self.get_heal_targets,
                self.sorting_health_percentage)

        elif self.current_unit.attack_type in ALCHEMIST_LIST:
            # определяем приоритет для друидов/алхимиков
            target = self.find_target(
                target_slots,
                self.get_druid_targets,
                self.sorting_damage)
            if target is None:
                target = self.find_target(
                    target_slots,
                    self.get_druid_targets,
                    self.sorting_health_percentage)

        elif self.current_unit.attack_type in PARALYZE_LIST:
            # определяем приоритет для парализаторов и ведьм
            target = self.find_target(
                target_slots,
                self.get_paralyze_targets,
                self.sorting_damage)

        return target

    def auto_attack(self) -> None:
        """Автоматическая атака игрока по противнику"""
        if not self.targets:
            self.attacked_slots = []
            self.current_unit.defence()

        elif self.current_unit.attack_radius == ANY_UNIT \
                and self.current_unit.attack_purpose == 6:
            # 6 целей
            self.attack_6_units(self.target_player)

        else:
            self.attacked_slots = []
            # 1 цель
            target = self.find_target_for_all(self.targets)
            self.attack_1_unit(target)

    def get_priority_target(self,
                            unit: Unit,
                            target_slots: List[int]) -> Unit:
        """Получить приоритетную для атаки цель"""
        first_priority = []
        second_priority = []
        third_priority = []
        target_units = []
        self.targets = []
        target = None

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
                self.targets.append(target_unit.slot)

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
            target = self.damage_priority(first_priority, 1)

        elif not first_priority and second_priority:
            target = self.damage_priority(second_priority, 2)

        if target is None:
            target = self.get_third_priority_target(
                target_units,
                third_priority)

        return target

    def get_third_priority_target(self,
                                  target_units: List[Unit],
                                  third_priority: List[Unit]):
        """Получить цель третьего приоритета для атаки"""
        # если второстепенная атака - Паралич/Окаменение
        if self.current_unit.dot_dmg == 0:
            # ищем цель по макс. урону с учетом иммунитетов цели
            attack_source = self.current_unit.attack_source.split('/')[1]
            i = 0
            targets = self.sorting_damage(target_units)
            target = targets[0]
            not_immune_target = bool(attack_source not in target.immune)

            while not_immune_target is False and i < len(target_units) - 1:
                i += 1
                target = targets[i]
                not_immune_target = bool(attack_source not in target.immune)

            # ищем цель с наименьшим здоровьем
            if not not_immune_target:
                target = self.hp_priority(third_priority)

        # если обычная атака
        else:
            target = self.hp_priority(third_priority)

        return target

    def damage_priority(self, targets: list, hits) -> Unit:
        """Определение приоритета для атаки"""
        result_target = None

        for target in targets:
            target_armor = (1 - target.armor * 0.01)
            damage = self.current_unit.attack_dmg * hits * target_armor

            # В первую очередь бьем лекарей
            if target.branch == 'support' \
                    and target.attack_source in HEAL_LIST \
                    and target.curr_health <= damage:
                result_target = target

            # Во вторую - бьем магов
            elif target.branch == 'mage' \
                    and target.curr_health <= damage:
                result_target = target

            # В третью - бьем стрелков
            elif target.branch == 'archer' \
                    and target.curr_health <= damage:
                result_target = target

        if result_target is None:
            result_target = self.hp_priority(targets)

        return result_target

    def hp_priority(self, targets):
        """Выбор слабейшего из оставшихся юнитов (по абсолютному здоровью)"""
        if targets:
            weakest_unit = self.sorting_health(targets)[0]
            return weakest_unit
        return None

    def get_heal_targets(self, target_slots: List[int]) -> List[Optional[Unit]]:
        """Получить цели для лечения"""
        target_units = []
        self.targets = []

        for slot in target_slots:
            unit = self.get_unit_by_slot(slot, self.target_player.units)
            if unit.curr_health < unit.health:
                target_units.append(unit)
                self.targets.append(unit.slot)

            if 'Исцеление' in self.current_unit.attack_type and unit.dotted:
                target_units.append(unit)
                self.targets.append(unit.slot)

        return target_units

    def get_druid_targets(self, target_slots: List[int]) -> List[Unit]:
        """Получение целей для Друида/Алхимика"""
        target_units = []
        self.targets = []

        for slot in target_slots:
            unit = self.get_unit_by_slot(
                slot,
                self.target_player.units)

            if (unit.dotted
                and 'Исцеление' in self.current_unit.attack_type) \
                    or \
                    (unit not in self.boosted_units
                     and unit.attack_dmg != 0
                     and unit.attack_type
                     not in (*HEAL_LIST, *ALCHEMIST_LIST, *PARALYZE_LIST)):
                target_units.append(unit)
                self.targets.append(unit.slot)

            # усиленный юнит усилен на меньший процент
            if self.boosted_units.get(unit):
                if self.boosted_units[unit] < self.current_unit.attack_dmg:
                    target_units.append(unit)
                    self.targets.append(unit.slot)

        return target_units

    def get_paralyze_targets(self, target_slots: List[int]) -> \
            List[Optional[Unit]]:
        """Получение приоритетной для парализатора цели"""
        target_units = []
        self.targets = []
        already_paralyzed = False

        for slot in target_slots:
            unit = self.get_unit_by_slot(
                slot,
                self.target_player.units)

            if unit in self.dotted_units and unit.dotted:
                for dot_source, dot_params in self.dotted_units[unit].items():
                    dot_rounds = dot_params[1]  # раунды

                    # если остались раунды, и это паралич/окаменение/полиморф
                    if dot_source in PARALYZE_LIST:
                        already_paralyzed = bool(dot_rounds)
            else:
                already_paralyzed = False

            if self.current_unit.attack_source \
                    not in unit.immune \
                    and not already_paralyzed:
                target_units.append(unit)
                self.targets.append(unit.slot)

        return target_units

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
        """Вычисление цели для крайних слотов"""
        if slot_a in tg_slots and slot_b in tg_slots:
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
        """Вычисление цели для среднего слота"""
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

        # Юнит в заднем ряду, авангард жив
        if unit.slot not in [2, 4, 6] and not vanguard_alies_died:
            result = []

        # Авангард врага мертв, Наш авангард мертв
        elif vanguard_enemies_died and vanguard_alies_died:
            if unit.slot % 2 == 1:
                result = targets_dict[unit.slot]

        # Авангард мертв
        elif vanguard_enemies_died:
            if unit.slot % 2 == 0:
                result = targets_dict[unit.slot - 1]

        # Авангард врага жив, Наш авангард мертв
        elif not vanguard_enemies_died and vanguard_alies_died:
            if unit.slot % 2 == 1:
                result = targets_dict[unit.slot + 1]

        # Авангард врага жив
        elif not vanguard_enemies_died:
            if unit.slot % 2 == 0:
                result = targets_dict[unit.slot]

        return result

    def _choose_targets(self,
                        unit: Unit,
                        attacker_slots: List[int],
                        slots: List[int]) -> Optional[List[int]]:
        """Определение следующих целей для атаки"""
        # для контактных юнитов
        if unit.attack_radius == CLOSEST_UNIT:
            target_slots = self._define_closest_slots(
                unit,
                slots,
                attacker_slots)
            if target_slots:
                self.find_target_for_all(target_slots)

                return target_slots

        # Для дальнобойных юнитов
        if unit.attack_radius == ANY_UNIT \
                and unit.attack_purpose in [1, 6]:
            self.find_target_for_all(slots)

            return slots

        return []

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
