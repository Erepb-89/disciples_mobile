"""Класс Unit"""

import math
import random
from collections import namedtuple
from typing import Dict, List

from battle_logging import logging

from client_dir.settings import BIG, \
    HERO_FIGHTER_EXP, HERO_ARCHER_EXP, HERO_ROD_EXP, \
    VAMPIRE_LIST, ALCHEMIST_LIST
from units_dir.buildings import FACTIONS
from units_dir.models import PlayerUnits, CurrentDungeon
from units_dir.ranking import PERKS, ELDER_FORMS
from units_dir.visual_model import v_model


class Unit:
    """Юнит"""

    def __init__(self, unit: namedtuple):
        # self.unit = unit

        self.id = unit[0]
        self.name = unit[1]
        self.level = unit[2]
        self.size = unit[3]
        self.price = unit[4]
        self.exp = unit[5]
        self.curr_exp = unit[6]
        self.exp_per_kill = unit[7]
        self.health = unit[8]
        self.curr_health = unit[9]
        self.armor = unit[10]
        self.immune = unit[11]
        self.ward = unit[12]
        self.attack_type = unit[13]
        self.attack_chance = unit[14]
        self.attack_dmg = unit[15]
        self.dot_dmg = unit[16]
        self.attack_source = unit[17]
        self.attack_ini = unit[18]
        self.attack_radius = unit[19]
        self.attack_purpose = unit[20]
        self.prev_level = unit[21]
        self.desc = unit[22]
        self.photo = unit[23]
        self.gif = unit[24]
        self.slot = unit[25]
        self.subrace = unit[26]
        self.branch = unit[27]
        self.attack_twice = unit[28]
        self.regen = unit[29]
        self.dyn_upd_level = unit[30]
        self.upgrade_b = unit[31]
        self.leadership = unit[32]
        self.leader_cat = unit[33]
        self.nat_armor = unit[34]
        self.might = unit[35]
        self.weapon_master = unit[36]
        self.endurance = unit[37]
        self.first_strike = unit[38]
        self.accuracy = unit[39]
        self.water_resist = unit[40]
        self.air_resist = unit[41]
        self.fire_resist = unit[42]
        self.earth_resist = unit[43]
        self.dotted = unit[44]
        self.locked = unit[45]

    @property
    def is_dead(self) -> bool:
        """Проверка на живость"""
        return self.curr_health == 0

    @property
    def double(self) -> bool:
        """Проверка на двухслотовость"""
        return self.size == BIG

    def off_defence(self) -> None:
        """Сброс защиты в битве"""
        self.armor = v_model.get_unit_by_name(self.name).armor + \
                     self.nat_armor * 20

    def off_initiative(self, pl_database) -> None:
        """Сброс инициативы в битве"""
        unit = v_model.get_unit_by_id(self.id,
                                      pl_database)
        if unit is not None:
            self.attack_ini = int(
                unit.attack_ini + unit.attack_ini * self.first_strike * 0.5)

    def off_boosts(self, pl_database) -> None:
        """Сброс усиления атаки в битве"""
        unit = v_model.get_unit_by_id(self.id,
                                      pl_database)
        if unit is not None:
            self.attack_dmg = unit.attack_dmg

    def minus_dot_round(self):
        """Уменьшение количества раундов действия на 1"""
        self.dotted -= 1

    def defence(self) -> None:
        """Пропуск хода и защита в битве"""
        self.armor = round(self.armor / 2 + 50)

        line = f"{self.name} защищается\n"
        logging(line)

    def waiting(self) -> None:
        """Ожидание в битве"""

        line = f"{self.name} ждет удачного момента\n"
        logging(line)

    def add_to_band(self, slot) -> None:
        """Найм в отряд игрока"""
        v_model.hire_unit(self.name, slot)

    def upgrade_stats(self, db_table) -> None:
        """Увеличение характеристик юнита"""
        # Уровень
        next_level = self.level + 1

        # Опыт
        next_exp = self.get_next_exp()

        # Здоровье
        if next_level - 10 < v_model.get_unit_by_name(self.name).level:
            next_hp = self.get_next_hp(10)
        else:
            next_hp = self.get_next_hp(5)
        self.health = next_hp

        # Шанс на попадание
        try:
            spitted_chance = self.attack_chance.split('/')
            chance = int(spitted_chance[0])
            # яды и т.д.
            dot_chance = int(spitted_chance[1])
            base_dot = f'{chance + 1}/{dot_chance + 1}'

            next_chance = base_dot if chance < 100 else 100
        except IndexError:
            chance = int(self.attack_chance)

            next_chance = chance + 1 if chance < 100 else 100

        # Урон
        damage = self.attack_dmg

        # Урон для героев
        if self.branch == 'hero':
            if self.leader_cat == 'fighter':
                next_damage = int(damage) + 10
            else:
                next_damage = int(damage) + 5
        # Для юнитов
        else:
            if self.attack_type not in ALCHEMIST_LIST:
                next_damage = math.ceil(damage * 1.10)
            else:
                next_damage = damage

        next_damage = min(next_damage, 300)

        # Увеличение доп. урона
        if self.dot_dmg:
            next_additional = self.dot_dmg + 6
        else:
            next_additional = None

        # Опыт за убийство
        if self.level <= 10:
            next_killed_exp = math.ceil(self.exp_per_kill * 1.10)
        else:
            next_killed_exp = math.ceil(self.exp_per_kill * 1.05)

        # Осталось возможных повышений уровня
        updates_left = self.dyn_upd_level - 1

        characteristics = {
            'level': next_level,
            'exp': next_exp,
            'health': next_hp,
            'curr_health': next_hp,
            'armor': self.armor,
            'curr_exp': 0,
            'exp_per_kill': next_killed_exp,
            'attack_chance': next_chance,
            'attack_dmg': next_damage,
            'dot_dmg': next_additional,
            'dyn_upd_level': updates_left
        }

        v_model.update_unit(
            self.id,
            characteristics,
            db_table)

    def downgrade_player_stats(self) -> None:
        """Снижение характеристик юнита"""
        self.downgrade_stats(PlayerUnits)

    def downgrade_enemy_stats(self) -> None:
        """Снижение характеристик юнита"""
        self.downgrade_stats(CurrentDungeon)

    def downgrade_stats(self, db_table) -> None:
        """Снижение характеристик юнита"""
        # Уровень
        basic_level = v_model.get_unit_by_name(self.name).level
        if basic_level >= self.level:
            pass
        else:
            prev_level = self.level - 1

            # Опыт
            prev_exp = self.get_prev_exp()

            # Здоровье
            if self.level - basic_level < 10:
                prev_hp = self.get_prev_hp(10)
            else:
                prev_hp = self.get_prev_hp(5)
            self.health = prev_hp

            # Шанс на попадание
            try:
                spitted_chance = self.attack_chance.split('/')
                chance = int(spitted_chance[0])
                # яды и т.д.
                dot_chance = int(spitted_chance[1])
                prev_chance = f'{chance - 1}/{dot_chance - 1}'
            except IndexError:
                prev_chance = int(self.attack_chance) - 1

            # Урон
            damage = self.attack_dmg

            # Урон для героев
            if self.branch == 'hero':
                if self.leader_cat == 'fighter':
                    prev_damage = int(damage) - 10
                else:
                    prev_damage = int(damage) - 5
            # Для юнитов
            else:
                if self.attack_type not in ALCHEMIST_LIST:
                    prev_damage = math.floor(damage / 1.10)
                else:
                    prev_damage = damage

            prev_damage = min(prev_damage, 300)

            # Увеличение доп. урона
            if self.dot_dmg:
                prev_additional = self.dot_dmg - 6
            else:
                prev_additional = None

            # Опыт за убийство
            if self.level <= 10:
                prev_killed_exp = math.floor(self.exp_per_kill / 1.10)
            else:
                prev_killed_exp = math.floor(self.exp_per_kill / 1.05)

            # Осталось возможных повышений уровня
            updates_left = self.dyn_upd_level + 1

            characteristics = {
                'level': prev_level,
                'exp': prev_exp,
                'health': prev_hp,
                'curr_health': prev_hp,
                'armor': self.armor,
                'curr_exp': 0,
                'exp_per_kill': prev_killed_exp,
                'attack_chance': prev_chance,
                'attack_dmg': prev_damage,
                'dot_dmg': prev_additional,
                'dyn_upd_level': updates_left
            }

            v_model.update_unit(
                self.id,
                characteristics,
                db_table)

    def get_next_exp(self) -> int:
        """Вычисление требуемого опыта при повышении (для героев)"""
        next_exp = self.exp
        if self.branch == 'hero' and self.level < 10:
            if self.leader_cat in ('fighter', 'mage'):
                next_exp = self.exp + HERO_FIGHTER_EXP
            elif self.leader_cat == 'archer':
                next_exp = self.exp + HERO_ARCHER_EXP
            elif self.leader_cat == 'rod':
                next_exp = self.exp + HERO_ROD_EXP
        return next_exp

    def get_prev_exp(self) -> int:
        """Вычисление требуемого опыта при понижении (для героев)"""
        prev_exp = self.exp
        if self.branch == 'hero' and self.level < 10:
            if self.leader_cat in ('fighter', 'mage'):
                prev_exp = self.exp - HERO_FIGHTER_EXP
            elif self.leader_cat == 'archer':
                prev_exp = self.exp - HERO_ARCHER_EXP
            elif self.leader_cat == 'rod':
                prev_exp = self.exp - HERO_ROD_EXP
        return prev_exp

    def get_next_hp(self, multiplier: int) -> int:
        """Увеличение здоровья"""
        next_hp = self.health
        plus_hp = math.floor(self.health * multiplier * 0.01)

        # Здоровье для героев
        if self.branch == 'hero':
            plus_hp = max(plus_hp, 10)

        next_hp += plus_hp

        while next_hp % 5 != 0:
            next_hp += 1

        return next_hp

    def get_prev_hp(self, multiplier: int) -> int:
        """Уменьшение здоровья"""
        prev_hp = math.ceil(self.health / (1 + multiplier * 0.01))

        # Здоровье для героев
        if self.branch == 'hero':
            while prev_hp % 10 != 0:
                prev_hp -= 1
        else:
            while prev_hp % 5 != 0:
                prev_hp -= 1

        return prev_hp

    def get_perks(self, db_table):
        """Получение перков героем"""
        # Рандомное получение перков
        all_perks = []

        perks = {
            # 'leadership': self.leadership,
            'nat_armor': self.nat_armor,
            'might': self.might,
            'weapon_master': self.weapon_master,
            'endurance': self.endurance,
            'first_strike': self.first_strike,
            'accuracy': self.accuracy,
            'water_resist': self.water_resist,
            'air_resist': self.air_resist,
            'fire_resist': self.fire_resist,
            'earth_resist': self.earth_resist
        }

        # определение оставшихся свободных перков
        for perk in PERKS.keys():
            if perk != 'leadership' and perks[perk] != 1:
                all_perks.append(perk)

        if all_perks:
            element_dict = {
                'water_resist': 'Вода',
                'air_resist': 'Воздух',
                'fire_resist': 'Огонь',
                'earth_resist': 'Земля'
            }

            perk = random.choice(all_perks)

            line = f"{self.name} получает перк {PERKS[perk]}\n"
            logging(line)

            if self.leadership < 5 and self.level % 2 == 0:
                perks['leadership'] = self.leadership + 1
                line = f"{self.name} получает перк Лидерство\n"
                logging(line)

            elif self.leadership == 5 or self.level % 2 == 1:
                perks['leadership'] = self.leadership

            perks[perk] = 1

            v_model.update_perks(
                self.id,
                perks,
                db_table)

            # Природная броня
            if perk == 'nat_armor':
                v_model.update_unit_armor(
                    self.id,
                    20,
                    db_table)

            # Мощь
            if perk == 'might':
                v_model.update_unit_dmg(
                    self.id,
                    0.25,
                    db_table)

            # Выносливость
            if perk == 'endurance':
                next_hp = self.get_next_hp(20)

                v_model.update_unit_health(
                    self.id,
                    next_hp,
                    db_table)

            # Первый удар
            if perk == 'first_strike':
                v_model.update_unit_ini(
                    self.id,
                    self.attack_ini * 1.5,
                    db_table)

            # Стихийный перк
            if 'resist' in perk:
                v_model.update_ward(
                    self.id,
                    element_dict[perk],
                    db_table)

    @property
    def race_settings(self) -> Dict[str, dict]:
        """Получение настроек фракции"""
        return FACTIONS.get(v_model.current_faction)

    def get_building_graph(self,
                           bname: str,
                           branch: str,
                           graph: list) -> None:
        """Рекурсивное создание словаря графов зданий/построек"""
        for building in self.race_settings[branch].values():
            if building.bname == bname and bname != '':
                graph.append(building)
                if building.prev not in ('', 0):
                    self.get_building_graph(building.prev, branch, graph)
                else:
                    return

    def get_faction_units(self,
                          graph_dict: Dict[str, list]) -> List[str]:
        """Получние всех фракционных юнитов"""
        # Постройки
        buildings = v_model.buildings._asdict()

        for bld in buildings.values():
            for branch in graph_dict:
                self.get_building_graph(
                    bld,
                    branch,
                    graph_dict[branch])

        # фракционные юниты
        faction_units = []
        for branch, b_value in FACTIONS.get(
                v_model.current_faction).items():
            if branch != 'others':
                for building in b_value.values():
                    faction_units.append(building.unit_name)

        return faction_units

    def lvl_up(self, db_table: any) -> None:
        """Повышение уровня"""
        next_unit = ''

        branch_dict = {
            'fighter': v_model.get_fighter_branch,
            'mage': v_model.get_mage_branch,
            'archer': v_model.get_archer_branch,
            'support': v_model.get_support_branch,
        }

        # снимаем защиту
        self.off_defence()

        # снимаем бонусы атаки
        self.off_boosts(db_table)

        # сбрасываем инициативу к изначальной
        self.off_initiative(db_table)

        if self.branch == 'hero':
            if self.dyn_upd_level != 0:
                self.upgrade_stats(db_table)
                self.get_perks(db_table)

                line = f"{self.name} повысил свой уровень\n"
                logging(line)
            else:
                line = f"{self.name} достиг предела развития\n"
                logging(line)

        elif self.branch in ('null', 'special', 'boss'):
            self.upgrade_stats(db_table)

        else:
            # Вызываем нужную функцию в зависимости от ветви
            branch_buildings = branch_dict[self.branch]()

            # находим следующую стадию юнита, если здание для апгрейда
            # построено
            for building \
                    in FACTIONS[v_model.current_faction][self.branch].values():
                if building.prev == self.upgrade_b \
                        and building.bname in branch_buildings:
                    # Следующая стадия
                    next_unit = building.unit_name

            self.upgrade_unit(next_unit, branch_buildings, db_table)

    def upgrade_unit(self,
                     next_unit: str,
                     branch_buildings: List[str],
                     db_table: any):
        """Метод апгрейда юнита"""
        # здание для апгрейда еще не построено
        if next_unit == '' \
                and self.curr_exp <= self.exp - 1 \
                and self.upgrade_b in branch_buildings \
                and self.name not in ELDER_FORMS:
            # ожидает апгрейда, поднять опыт до (exp - 1)
            v_model.update_unit_exp(
                self.slot, self.exp - 1)
            line = f"{self.name} ожидает повышения в столице\n"
            logging(line)

        # если следующая стадия найдена
        elif next_unit != '':
            # Меняем юнит на следующую стадию согласно постройкам
            # в столице
            v_model.replace_unit(self.slot, next_unit)

            line = f"{self.name} повысил уровень до {next_unit}\n"
            logging(line)

        # если следующей стадии нет
        else:
            # Апгрейд характеристик юнита
            if self.dyn_upd_level != 0:
                self.upgrade_stats(db_table)

                line = f"{self.name} повысил свой уровень\n"
                logging(line)
            else:
                line = f"{self.name} достиг предела развития\n"
                logging(line)

    @staticmethod
    def say() -> None:
        """Боевой клич"""
        print('fight')

    def damage_calculating(self,
                           target: any,
                           attack_dict: dict) -> None:
        """
        Расчет урона в случае успешной атаки. Учет брони у цели.
        Расчет здоровья цели после нанесения урона.
        Логирование удачного попадания.
        """
        # Если атака успешна
        if attack_dict['attack_successful'] \
                and not attack_dict['immune_activated'] \
                and not attack_dict['ward_activated']:

            if self.attack_dmg > 0:
                # Вычисление урона с учетом брони
                damage = min(
                    int(
                        (self.attack_dmg +
                         (self.attack_dmg * self.might * 0.25) +
                         random.randrange(6)
                         ) * (1 - target.armor * 0.01)
                    ),
                    300)

                # если урон больше, чем здоровье врага, приравниваем урон к
                # здоровью
                damage = min(damage, target.curr_health)

                # вычисление текущего здоровья цели после получения урона
                target.curr_health -= damage

                # если есть вампиризм у атакующего:
                if self.attack_type in VAMPIRE_LIST:
                    self.curr_health += int(damage / 2)
                    self.curr_health = min(self.curr_health, self.health)

                line = f"{self.name} наносит урон {damage} воину " \
                       f"{target.name}. Осталось ХП: {target.curr_health}\n"
                logging(line)

    def miss_logging(self, target: any, attack_dict: dict):
        """Логирование промахов"""
        attack_source = attack_dict['attack_source']

        if attack_dict['immune_activated']:
            logging(
                f"{target.name} имеет иммунитет к {attack_source} \n")

        elif attack_dict['ward_activated']:
            logging(
                f"{target.name} имеет защиту от {attack_source} \n")

        elif not attack_dict['attack_successful']:
            logging(f"{self.name} промахивается по {target.name}\n")

    def attack(self, target: any) -> bool:
        """Обычная атака."""

        attack_dict = {
            'attack_successful': False,
            'immune_activated': False,
            'ward_activated': False,
            'attack_source': '',
            'attack_type': ''
        }

        # Вычисление вероятности попадания
        try:
            acc = int(self.attack_chance.split('/')[0])
            chance = (acc + self.accuracy * 0.2 * acc) / 100

        except IndexError:
            extra_chance = self.accuracy * 0.2 * int(self.attack_chance)
            chance = (int(self.attack_chance) + extra_chance) / 100

        # источник атаки
        try:
            attack_source = self.attack_source.split('/')[0]
        except IndexError:
            attack_source = self.attack_source

        attack_dict['attack_source'] = attack_source

        attack_dict = self.checking_immune_ward(
            target,
            chance,
            attack_dict)

        # Вычисление урона атакующего и здоровья цели.
        # Логирование удачного попадания
        self.damage_calculating(target,
                                attack_dict)

        # Логирование промахов
        self.miss_logging(target,
                          attack_dict)

        return attack_dict['attack_successful']

    def dot_attack(self, target: any) -> bool:
        """Атака доп уроном."""
        attack_dict = {
            'attack_successful': False,
            'immune_activated': False,
            'ward_activated': False,
            'attack_source': '',
            'attack_type': ''
        }

        # Вычисление вероятности попадания
        try:
            acc = int(self.attack_chance.split('/')[1])
            chance = (acc + self.accuracy * 0.2 * acc) / 100
        except IndexError:
            extra_chance = self.accuracy * 0.2 * int(self.attack_chance)
            chance = (int(self.attack_chance) + extra_chance) / 100

        # источник атаки
        try:
            attack_source = self.attack_source.split('/')[1]
            attack_dict['attack_source'] = attack_source

        except IndexError:
            attack_source = self.attack_source
            attack_dict['attack_source'] = attack_source

        # тип атаки (для Яда и Раскола)
        try:
            attack_type = self.attack_type.split('/')[1]
            attack_dict['attack_type'] = attack_type
        except IndexError:
            attack_type = self.attack_type
            attack_dict['attack_type'] = attack_type

        attack_dict = self.checking_immune_ward(target, chance, attack_dict)

        # Логирование промахов
        self.miss_logging(target,
                          attack_dict)

        return attack_dict['attack_successful']

    @staticmethod
    def checking_immune_ward(target: any,
                             chance: float,
                             attack_dict: dict) -> dict:
        """Проверка успешности атаки. Проверка на иммунитеты, защиты."""
        # источник атаки
        attack_source = attack_dict['attack_source']

        # тип атаки (для Яда и раскола)
        attack_type = attack_dict['attack_type']

        # иммунитеты и защиты
        target_immune = target.immune.split(', ')
        target_wards = target.ward.split(', ')

        # у цели нет иммунитета и защиты от источника атаки
        if attack_source not in target_immune \
                and attack_type not in target_immune \
                and attack_source not in target_wards:

            # атака удачна или неудачна / промах
            attack_successful = \
                bool(random.random() <= chance)
            attack_dict['attack_successful'] = attack_successful

        # у цели есть иммунитет от источника атаки
        elif attack_source in target_immune \
                or attack_type in target_immune:
            # иммунитет остается всегда
            attack_dict['immune_activated'] = True

        # у цели есть защита от источника атаки
        elif attack_source in target_wards \
                or attack_type in target_wards:
            # -1 защита из списка
            target_wards.remove(attack_source)
            target.ward = ''

            for ward in target_wards:
                if target_wards.index(ward) == len(target_wards) - 1:
                    target.ward += ward
                else:
                    target.ward += ward + ", "

            attack_dict['ward_activated'] = True

        return attack_dict

    def heal(self, target: any) -> bool:
        """Лечение"""
        health = int(self.attack_dmg)

        # если размер лечения больше, чем макс. здоровье цели,
        if target.curr_health + health > target.health:
            health = target.health - target.curr_health

        if health != 0:
            target.curr_health += health

            line = f"{self.name} лечит {health} " \
                   f"единиц здоровья воину {target.name}. " \
                   f"Стало ХП: {target.curr_health}\n"
            logging(line)

        return True

    def cure(self, target: any) -> bool:
        """Исцеление"""
        if target.dotted:
            target.dotted = 0

        line = f"{self.name} исцеляет воина {target.name}.\n"
        logging(line)

        return True

    def increase_damage(self, target: any) -> bool:
        """Увеличение урона Друидом"""
        if 'Увеличение урона' in self.attack_type:
            dmg_boost = math.floor(self.attack_dmg * 0.01 * target.attack_dmg)
            target.attack_dmg = min(300, target.attack_dmg + dmg_boost)

            line = f"{self.name} увеличивает урон на " \
                   f"{self.attack_dmg}% воину {target.name}.\n"
            logging(line)

        return True


# Отладка
if __name__ == '__main__':
    # empire_factory = AbstractFactory.create_factory('Em')

    # fighter = empire_factory.create_fighter()
    # fighter.add_to_band(3)

    new_unit1 = Unit(v_model.get_unit_by_name('Антипаладин'))
    new_unit2 = Unit(v_model.get_unit_by_name('Мраморная гаргулья'))

    # new_unit1.lvl_up()

    new_unit1.attack(new_unit2)
    # new_unit2.attack(new_unit1)
