"""Фабрика юнитов"""

import abc
import math
import random
from collections import namedtuple
from typing import Dict, List

from battle_logging import logging

from client_dir.settings import EM, UH, LD, MC, BIG, HERO_FIGHTER_EXP, HERO_ARCHER_EXP, HERO_ROD_EXP
from units_dir.buildings import FACTIONS, ELDER_FORMS, PERKS
from units_dir.units import main_db
from units_dir.ranking import empire_mage_lvls, \
    empire_archer_lvls, empire_support_lvls, \
    hordes_fighter_lvls, hordes_mage_lvls, \
    hordes_archer_lvls, hordes_support_lvls, \
    legions_fighter_lvls, legions_mage_lvls, \
    legions_archer_lvls, legions_support_lvls, \
    clans_fighter_lvls, clans_mage_lvls, \
    clans_archer_lvls, clans_support_lvls


# Empire classes

class EmpireFighter:
    """Боец Империи"""

    @property
    def name(self):
        """Имя"""
        return 'Сквайр'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '50'

    @staticmethod
    def add_to_band(slot):
        """Сквайр. Найм в отряд игрока"""
        main_db.hire_unit('Сквайр', slot)

    @staticmethod
    def up_to_base():
        """Обновление характеристик юнита игрока (health, exp)"""
        main_db.update_unit('Сквайр', 70, 50)

    @staticmethod
    def lvl_up(slot):
        """Боец Империи. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = legions_fighter_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('fight')


class EmpireMage:
    """Маг Империи"""

    @property
    def name(self):
        """Имя"""
        return 'Ученик'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '60'

    @staticmethod
    def add_to_band(slot):
        """Ученик. Найм в отряд игрока"""
        main_db.hire_unit('Ученик', slot)

    @staticmethod
    def lvl_up(slot):
        """Маг Империи. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = empire_mage_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('magic')


class EmpireArcher:
    """Стрелок Империи"""

    @property
    def name(self):
        """Имя"""
        return 'Лучник'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '40'

    @staticmethod
    def add_to_band(slot):
        """Лучник. Найм в отряд игрока"""
        main_db.hire_unit('Лучник', slot)

    @staticmethod
    def lvl_up(slot):
        """Стрелок Империи. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = empire_archer_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('bow')


class EmpireSupport:
    """Поддержка Империи"""

    @property
    def name(self):
        """Имя"""
        return 'Послушник'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '50'

    @staticmethod
    def add_to_band(slot):
        """Послушник. Найм в отряд игрока"""
        main_db.hire_unit('Послушник', slot)

    @staticmethod
    def lvl_up(slot):
        """Поддержка Империи. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = empire_support_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('help')


class EmpireSpecial:
    """Особый юнит Империи"""

    @property
    def name(self):
        """Имя"""
        return 'Титан'

    @property
    def size(self):
        """Размер"""
        return 'Большой'

    @property
    def cost(self):
        """Стоимость"""
        return '300'

    @staticmethod
    def add_to_band(slot):
        """Титан. Найм в отряд игрока"""
        main_db.hire_unit('Титан', slot)

    @staticmethod
    def lvl_up(slot):
        """Особый юнит Империи. Повышение уровня"""


# Hordes classes

class HordesFighter:
    """Боец Орд нежити"""

    @property
    def name(self):
        """Имя"""
        return 'Боец'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '50'

    @staticmethod
    def add_to_band(slot):
        """Боец. Найм в отряд игрока"""
        main_db.hire_unit('Боец', slot)

    @staticmethod
    def lvl_up(slot):
        """Боец Орд нежити. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = hordes_fighter_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('fight')


class HordesMage:
    """Маг Орд нежити"""

    @property
    def name(self):
        """Имя"""
        return 'Посвящённый'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '60'

    @staticmethod
    def add_to_band(slot):
        """Посвящённый. Найм в отряд игрока"""
        main_db.hire_unit('Посвящённый', slot)

    @staticmethod
    def lvl_up(slot):
        """Маг Орд нежити. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = hordes_mage_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('magic')


class HordesArcher:
    """Стрелок Орд нежити"""

    @property
    def name(self):
        """Имя"""
        return 'Привидение'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '50'

    @staticmethod
    def add_to_band(slot):
        """Привидение. Найм в отряд игрока"""
        main_db.hire_unit('Привидение', slot)

    @staticmethod
    def lvl_up(slot):
        """Стрелок Орд нежити. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = hordes_archer_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('bow')


class HordesSupport:
    """Поддержка Орд нежити"""

    @property
    def name(self):
        """Имя"""
        return 'Виверна'

    @property
    def size(self):
        """Размер"""
        return 'Большой'

    @property
    def cost(self):
        """Стоимость"""
        return '100'

    @staticmethod
    def add_to_band(slot):
        """Виверна. Найм в отряд игрока"""
        main_db.hire_unit('Виверна', slot)

    @staticmethod
    def lvl_up(slot):
        """Поддержка Орд нежити. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = hordes_support_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('help')


class HordesSpecial:
    """Особый юнит Орд нежити"""

    @property
    def name(self):
        """Имя"""
        return 'Оборотень'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '1000'

    @staticmethod
    def add_to_band(slot):
        """Оборотень. Найм в отряд игрока"""
        main_db.hire_unit('Оборотень', slot)

    @staticmethod
    def lvl_up(slot):
        """Особый юнит Орд нежити. Повышение уровня"""


# Legions classes

class LegionsFighter:
    """Боец Легионов проклятых"""

    @property
    def name(self):
        """Имя"""
        return 'Одержимый'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '50'

    @staticmethod
    def add_to_band(slot):
        """Одержимый. Найм в отряд игрока"""
        main_db.hire_unit('Одержимый', slot)

    @staticmethod
    def lvl_up(slot):
        """Боец Легионов проклятых. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = legions_fighter_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('fight')


class LegionsMage:
    """Маг Легионов проклятых"""

    @property
    def name(self):
        """Имя"""
        return 'Сектант'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '60'

    @staticmethod
    def add_to_band(slot):
        """Сектант. Найм в отряд игрока"""
        main_db.hire_unit('Сектант', slot)

    @staticmethod
    def lvl_up(slot):
        """Маг Легионов проклятых. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = legions_mage_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('magic')


class LegionsArcher:
    """Стрелок Легионов проклятых"""

    @property
    def name(self):
        """Имя"""
        return 'Гаргулья'

    @property
    def size(self):
        """Размер"""
        return 'Большой'

    @property
    def cost(self):
        """Стоимость"""
        return '80'

    @staticmethod
    def add_to_band(slot):
        """Гаргулья. Найм в отряд игрока"""
        main_db.hire_unit('Гаргулья', slot)

    @staticmethod
    def lvl_up(slot):
        """Стрелок Легионов проклятых. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = legions_archer_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('bow')


class LegionsSupport:
    """Поддержка Легионов проклятых"""

    @property
    def name(self):
        """Имя"""
        return 'Чёрт'

    @property
    def size(self):
        """Размер"""
        return 'Большой'

    @property
    def cost(self):
        """Стоимость"""
        return '100'

    @staticmethod
    def add_to_band(slot):
        """Чёрт. Найм в отряд игрока"""
        main_db.hire_unit('Чёрт', slot)

    @staticmethod
    def lvl_up(slot):
        """Поддержка Легионов проклятых. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = legions_support_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('help')


class LegionsSpecial:
    """Особый юнит Легионов проклятых"""

    @property
    def name(self):
        """Имя"""
        return 'Изверг'

    @property
    def size(self):
        """Размер"""
        return 'Большой'

    @property
    def cost(self):
        """Стоимость"""
        return '300'

    @staticmethod
    def add_to_band(slot):
        """Изверг. Найм в отряд игрока"""
        main_db.hire_unit('Изверг', slot)

    @staticmethod
    def lvl_up(slot):
        """Особый юнит Легионов проклятых. Повышение уровня"""


# Clans classes

class ClansFighter:
    """Боец Горных кланов"""

    @property
    def name(self):
        """Имя"""
        return 'Гном'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '50'

    @staticmethod
    def add_to_band(slot):
        """Гном. Найм в отряд игрока"""
        main_db.hire_unit('Гном', slot)

    @staticmethod
    def lvl_up(slot):
        """Боец Горных кланов. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = clans_fighter_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('fight')


class ClansMage:
    """Маг Горных кланов"""

    @property
    def name(self):
        """Имя"""
        return 'Желторотик'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '60'

    @staticmethod
    def add_to_band(slot):
        """Желторотик. Найм в отряд игрока"""
        main_db.hire_unit('Желторотик', slot)

    @staticmethod
    def lvl_up(slot):
        """Маг Горных кланов. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = clans_mage_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('magic')


class ClansArcher:
    """Стрелок Горных кланов"""

    @property
    def name(self):
        """Имя"""
        return 'Метатель топоров'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '40'

    @staticmethod
    def add_to_band(slot):
        """Метатель топоров. Найм в отряд игрока"""
        main_db.hire_unit('Метатель топоров', slot)

    @staticmethod
    def lvl_up(slot):
        """Стрелок Горных кланов. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = clans_archer_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('bow')


class ClansSupport:
    """Поддержка Горных кланов"""

    @property
    def name(self):
        """Имя"""
        return 'Холмовой гигант'

    @property
    def size(self):
        """Размер"""
        return 'Большой'

    @property
    def cost(self):
        """Стоимость"""
        return '100'

    @staticmethod
    def add_to_band(slot):
        """Холмовой гигант. Найм в отряд игрока"""
        main_db.hire_unit('Холмовой гигант', slot)

    @staticmethod
    def lvl_up(slot):
        """Поддержка Горных кланов. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = clans_support_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('help')


class ClansSpecial:
    """Особый юнит Горных кланов"""

    @property
    def name(self):
        """Имя"""
        return 'Йети'

    @property
    def size(self):
        """Размер"""
        return 'Большой'

    @property
    def cost(self):
        """Стоимость"""
        return '400'

    @staticmethod
    def add_to_band(slot):
        """Йети. Найм в отряд игрока"""
        main_db.hire_unit('Йети', slot)

    @staticmethod
    def lvl_up(slot):
        """Особый юнит Горных кланов. Повышение уровня"""


class AbstractFactory(abc.ABC):
    """Абстрактная фабрика фракций"""

    @staticmethod
    def create_factory(faction):
        """Создание фракции"""
        factions = {
            EM: EmpireFactory,
            UH: HordesFactory,
            LD: LegionsFactory,
            MC: ClansFactory
        }

        return factions[faction]()

    @abc.abstractmethod
    def create_fighter(self):
        """Создать бойца"""

    @abc.abstractmethod
    def create_mage(self):
        """Создать мага"""

    @abc.abstractmethod
    def create_archer(self):
        """Создать стрелка"""

    @abc.abstractmethod
    def create_support(self):
        """Создать юнита поддержки"""

    @abc.abstractmethod
    def create_special(self):
        """Создать спец-юнита"""


class EmpireFactory(AbstractFactory):
    """Фабрика Империи"""

    def create_fighter(self):
        """Создать бойца"""
        return EmpireFighter()

    def create_archer(self):
        """Создать стрелка"""
        return EmpireArcher()

    def create_mage(self):
        """Создать мага"""
        return EmpireMage()

    def create_support(self):
        """Создать юнита поддержки"""
        return EmpireSupport()

    def create_special(self):
        """Создать спец-юнита"""
        return EmpireSpecial()


class HordesFactory(AbstractFactory):
    """Фабрика Орд нежити"""

    def create_fighter(self):
        """Создать бойца"""
        return HordesFighter()

    def create_archer(self):
        """Создать стрелка"""
        return HordesArcher()

    def create_mage(self):
        """Создать мага"""
        return HordesMage()

    def create_support(self):
        """Создать юнита поддержки"""
        return HordesSupport()

    def create_special(self):
        """Создать спец-юнита"""
        return HordesSpecial()


class LegionsFactory(AbstractFactory):
    """Фабрика Легионов Проклятых"""

    def create_fighter(self):
        """Создать бойца"""
        return LegionsFighter()

    def create_archer(self):
        """Создать стрелка"""
        return LegionsArcher()

    def create_mage(self):
        """Создать мага"""
        return LegionsMage()

    def create_support(self):
        """Создать юнита поддержки"""
        return LegionsSupport()

    def create_special(self):
        """Создать спец-юнита"""
        return LegionsSpecial()


class ClansFactory(AbstractFactory):
    """Фабрика Горных кланов"""

    def create_fighter(self):
        """Создать бойца"""
        return ClansFighter()

    def create_archer(self):
        """Создать стрелка"""
        return ClansArcher()

    def create_mage(self):
        """Создать мага"""
        return ClansMage()

    def create_support(self):
        """Создать юнита поддержки"""
        return ClansSupport()

    def create_special(self):
        """Создать спец-юнита"""
        return ClansSpecial()


# класс Unit

class Unit:
    """Юнит"""

    def __init__(self, unit: namedtuple):
        self.unit = unit

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
        self.attack_source = unit[16]
        self.attack_ini = unit[17]
        self.attack_radius = unit[18]
        self.attack_purpose = unit[19]
        self.prev_level = unit[20]
        self.desc = unit[21]
        self.photo = unit[22]
        self.gif = unit[23]
        self.slot = unit[24]
        self.subrace = unit[25]
        self.branch = unit[26]
        self.attack_twice = unit[27]
        self.regen = unit[28]
        self.dyn_upd_level = unit[29]
        self.upgrade_b = unit[30]
        self.leadership = unit[31]
        self.leader_cat = unit[32]
        self.nat_armor = unit[33]
        self.might = unit[34]
        self.weapon_master = unit[35]
        self.endurance = unit[36]
        self.first_strike = unit[37]
        self.accuracy = unit[38]
        self.water_resist = unit[39]
        self.air_resist = unit[40]
        self.fire_resist = unit[41]
        self.earth_resist = unit[42]

    @property
    def is_dead(self) -> bool:
        """Проверка на живость"""
        return False

    @property
    def is_double(self) -> bool:
        """Проверка на двухслотовость"""
        return self.size == BIG

    def skip_turn(self) -> None:
        """Пропуск хода юнита в битве"""
        print(self.name, 'пропускает ход')

    def undefence(self) -> None:
        """Сброс защиты в битве"""
        self.armor = main_db.get_unit_by_name(self.name).armor + \
                     self.might * 20

    def defence(self) -> None:
        """Пропуск хода и защита в битве"""
        self.armor = round(self.armor / 2 + 50)
        # self.armor = round(
        #     main_db.get_unit_by_name(self.name).armor +
        #     (self.might * 20) / 2 + 50)

        line = f"{self.name} защищается\n"
        logging(line)

    def waiting(self) -> None:
        """Ожидание в битве"""

        line = f"{self.name} ждет удачного момента\n"
        logging(line)

    def add_to_band(self, slot) -> None:
        """Найм в отряд игрока"""
        main_db.hire_unit(self.name, slot)

    def upgrade_stats(self) -> None:
        """Увеличение характеристик юнита"""
        # Уровень
        next_level = self.level + 1

        # Опыт
        next_exp = self.get_next_exp()

        # Здоровье
        next_hp = self.get_next_hp()
        self.health = next_hp

        # Шанс на попадание
        try:
            chance = int(self.attack_chance.split('/')[0])
            # яды и т.д.
            dot_chance = int(self.attack_chance.split('/')[1])

            next_chance = f'{chance + 1}/{dot_chance + 1}' \
                if chance < 100 else 100
        except IndexError:
            chance = int(self.attack_chance)

            next_chance = chance + 1 if chance < 100 else 100

        # Урон
        try:
            splitted_dmg = self.attack_dmg.split('/')
            damage = int(splitted_dmg[0])

            # Добавить увеличение доп. урона
            additional = int(splitted_dmg[1])
            next_additional = additional + 6

            # Урон для героев
            if self.branch == 'hero':
                if self.leader_cat == 'fighter':
                    next_damage = int(damage) + 10
                else:
                    next_damage = int(damage) + 5
            # Для юнитов
            else:
                next_damage = int(damage * 1.10)

            next_damage = f'{min(next_damage, 300)}/{next_additional}'
        except AttributeError:  # IndexError
            # Урон для героев
            if self.branch == 'hero':
                if self.leader_cat == 'fighter':
                    next_damage = int(self.attack_dmg) + 10
                else:
                    next_damage = int(self.attack_dmg) + 5
            # Для юнитов
            else:
                next_damage = int(self.attack_dmg * 1.10)

            next_damage = min(next_damage, 300)

        # Опыт за убийство
        if self.level <= 10:
            next_killed_exp = math.ceil(self.exp_per_kill * 1.10)
        else:
            next_killed_exp = math.ceil(self.exp_per_kill * 1.05)

        # Осталось возможных повышений уровня
        updates_left = self.dyn_upd_level - 1

        main_db.update_unit(
            self.id,
            next_level,
            next_exp,
            next_hp,
            next_hp,
            self.armor,
            0,
            next_killed_exp,
            next_chance,
            next_damage,
            updates_left)

    def get_next_exp(self):
        """Увеличение требуемого опыта для повышения (для героев)"""
        next_exp = self.exp
        # Увеличение требуемого опыта для повышения (для героев)
        if self.branch == 'hero' and self.level < 10:
            if self.leader_cat in ('fighter', 'mage'):
                next_exp = self.exp + HERO_FIGHTER_EXP
            elif self.leader_cat == 'archer':
                next_exp = self.exp + HERO_ARCHER_EXP
            elif self.leader_cat == 'rod':
                next_exp = self.exp + HERO_ROD_EXP
        return next_exp

    def get_next_hp(self):
        """Увеличение здоровья"""
        next_hp = int(self.health * 1.10)

        # Здоровье для героев
        if self.branch == 'hero':
            next_hp = max(next_hp, 10)

        while next_hp % 5 != 0:
            next_hp += 1

        return next_hp

    def give_perks(self):
        """Получение перков героем"""
        # Рандомное получение перков
        all_perks = []

        perks = {
            'leadership': self.leadership,
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
            if (perk == 'leadership' and self.leadership < 5) \
                    or (perk != 'leadership' and perks[perk] != 1):
                all_perks.append(perk)

        if all_perks:
            perk = random.choice(all_perks)
            line = f"{self.name} получает перк {PERKS[perk]}\n"
            logging(line)

            if perk == 'leadership' and self.leadership < 5:
                perks[perk] = self.leadership + 1
            else:
                perks[perk] = 1

            main_db.update_perks(
                self.id,
                perks)

            # Природная броня
            if perk == 'nat_armor':
                main_db.update_unit_armor(self.id, self.armor + 20)

            # Выносливость
            if perk == 'endurance':
                main_db.update_unit_health(
                    self.id, self.health + self.health * 0.2)

            # Первый удар
            if perk == 'first_strike':
                main_db.update_unit_ini(
                    self.id, self.attack_ini + self.attack_ini * 0.5)

            self.element_perk(perk, 'water_resist', 'Вода')
            self.element_perk(perk, 'air_resist', 'Воздух')
            self.element_perk(perk, 'fire_resist', 'Огонь')
            self.element_perk(perk, 'earth_resist', 'Земля')

    def element_perk(self, perk, resist, element):
        """Проверка на стихийный перк"""
        if perk == resist and self.ward != 'Нет':
            main_db.update_ward(self.id, f'{self.ward}, {element}')
        elif perk == resist and self.ward == 'Нет':
            main_db.update_ward(self.id, element)

    @property
    def race_settings(self) -> Dict[str, dict]:
        """Получение настроек фракции"""
        return FACTIONS.get(main_db.current_faction)

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
                          faction: str,
                          graph_dict: Dict[str, list]) -> List[str]:
        """Получние всех фракционных юнитов"""
        # Постройки
        buildings = main_db.get_buildings(
            main_db.current_player.name,
            faction)._asdict()

        for bld in buildings.values():
            for branch in graph_dict:
                self.get_building_graph(bld, branch, graph_dict[branch])

        # фракционные юниты
        faction_units = []
        for branch, b_value in FACTIONS.get(
                main_db.current_faction).items():
            if branch != 'others':
                for building in b_value.values():
                    faction_units.append(building.unit_name)

        return faction_units

    def lvl_up(self) -> None:
        """Повышение уровня"""
        next_unit = ''

        branch_dict = {
            'fighter': main_db.get_fighter_branch,
            'mage': main_db.get_mage_branch,
            'archer': main_db.get_archer_branch,
            'support': main_db.get_support_branch,
        }

        if self.branch == 'hero':
            if self.dyn_upd_level != 0:
                self.upgrade_stats()
                self.give_perks()

                line = f"{self.name} повысил свой уровень\n"
                logging(line)
            else:
                line = f"{self.name} достиг предела развития\n"
                logging(line)
        else:
            # Вызываем нунную функцию в зависимости от ветви
            branch_buildings = branch_dict[self.branch]()

            # находим следующую стадию юнита, если здание для апгрейда
            # построено
            for building in \
                    FACTIONS[main_db.current_faction][self.branch].values():
                if building.prev == self.upgrade_b and \
                        building.bname in branch_buildings:
                    # Следующая стадия
                    next_unit = building.unit_name

            self.upgrade_unit(next_unit, branch_buildings)

    def upgrade_unit(self, next_unit: str, branch_buildings: List[str]):
        """Метод апгрейда юнита"""
        # здание для апгрейда еще не построено
        if next_unit == '' and self.curr_exp != self.exp - 1 and \
                self.upgrade_b in branch_buildings \
                and self.name not in ELDER_FORMS:
            # ожидает апгрейда, поднять опыт до (exp - 1)
            main_db.update_unit_exp(
                self.slot, self.exp - 1, main_db.PlayerUnits)
            line = f"{self.name} ожидает повышения в столице\n"
            logging(line)

        # здание для апгрейда еще не построено
        elif next_unit == '' and self.curr_exp == self.exp - 1 and \
                self.upgrade_b in branch_buildings \
                and self.name not in ELDER_FORMS:
            # ожидает апгрейда
            line = f"{self.name} ожидает повышения в столице\n"
            logging(line)

        # если следующая стадия найдена
        elif next_unit != '':
            # Меняем юнит на следующую стадию согласно постройкам
            # в столице
            main_db.replace_unit(self.slot, next_unit)

            line = f"{self.name} повысил уровень до {next_unit}\n"
            logging(line)

        # если следующей стадии нет
        else:
            # Апгрейд юнита по характеристикам
            if self.dyn_upd_level != 0:
                self.upgrade_stats()

                line = f"{self.name} повысил свой уровень\n"
                logging(line)
            else:
                line = f"{self.name} достиг предела развития\n"
                logging(line)

    @staticmethod
    def say() -> None:
        """Боевой клич"""
        print('fight')

    def is_attack_successful(self,
                             target: any,
                             attack_successful: bool,
                             immune_activated: bool,
                             ward_activated: bool,
                             attack_source: str) -> None:
        """
        Проверка успешности атаки. Проверка на иммунитеты, защиты.
        Расчет урона в случае успешной атаки.
        Логирование.
        """

        # Если атака успешна
        if attack_successful and not immune_activated and not ward_activated:
            # Вычисление урона с учетом брони
            try:
                dmg = int(self.attack_dmg.split('/')[0])
                damage = min(int(
                    (dmg + (dmg * self.might * 0.25) +
                     random.randrange(6)) * (1 - target.armor * 0.01)),
                    300)
            except AttributeError:
                damage = min(
                    int((self.attack_dmg +
                         (self.attack_dmg * self.might * 0.25) +
                         random.randrange(6)) * (1 - target.armor * 0.01)),
                    300)

            # если урон больше, чем здоровье врага, приравниваем урон к
            # здоровью
            damage = min(damage, target.curr_health)

            # вычисление текущего здоровья цели после получения урона
            target.curr_health -= damage

            # если есть вампиризм у атакующего:
            if self.attack_type in [
                'Высасывание жизни',
                    'Избыточное высасывание жизни']:
                self.curr_health += int(damage / 2)
                self.curr_health = min(self.curr_health, self.health)

                # main_db.update_unit_curr_hp(
                #     self.slot, self.curr_health, main_db.attacker_db)

            line = f"{self.name} наносит урон {damage} воину " \
                   f"{target.name}. Осталось ХП: {target.curr_health}\n"
            logging(line)

        elif immune_activated:
            logging(
                f"{target.name} имеет иммунитет к {attack_source} \n")

        elif ward_activated:
            logging(
                f"{target.name} имеет защиту от {attack_source} \n")

        elif not attack_successful:
            logging(f"{self.name} промахивается по {target.name}\n")

    def attack(self, target: any) -> bool:
        """Атака"""
        attack_successful = False
        immune_activated = False
        ward_activated = False

        # Вычисление вероятности попадания
        try:
            acc = int(self.attack_chance.split(
                '/')[0])
            chance = (acc + self.accuracy * 0.2 * acc) / 100

            # Добавить урон ядом / ожогом и т.п.
            # poison = int(self.attack_chance.split(
            #     '/')[1]) / 100
        except IndexError:
            chance = (int(self.attack_chance) +
                      self.accuracy * 0.2) / 100

        # источник атаки
        try:
            attack_source = self.attack_source.split('/')[0]
            # Добавить урон ядом / ожогом и т.п.

        except IndexError:
            attack_source = self.attack_source

        # иммунитеты и защиты
        target_immunes = target.immune.split(', ')
        target_wards = target.ward.split(', ')

        # у цели нет иммунитета и защиты от источника атаки
        if attack_source not in target_immunes \
                and attack_source not in target_wards:

            # атака удачна или неудачна / промах
            attack_successful = bool(random.random() <= chance)

        # у цели есть иммунитет от источника атаки
        elif attack_source in target_immunes:
            # иммунитет остается всегда
            immune_activated = True

        # у цели есть защита от источника атаки
        elif attack_source in target_wards:
            # -1 защита из списка
            target_wards.remove(attack_source)
            target.ward = ''

            for ward in target_wards:
                if target_wards.index(ward) == len(target_wards) - 1:
                    target.ward += ward
                else:
                    target.ward += ward + ", "

            ward_activated = True

        # проверка успешности атаки
        self.is_attack_successful(target,
                                  attack_successful,
                                  immune_activated,
                                  ward_activated,
                                  attack_source)

        return attack_successful

    def heal(self, target: any) -> bool:
        """Лечение"""
        health = int(self.attack_dmg)

        # если размер лечения больше, чем макс. здоровье цели,
        if target.curr_health + health > target.health:
            health = target.health - target.curr_health

        target.curr_health += health

        line = f"{self.name} лечит {health} воину {target.name}. " \
               f"Стало ХП: {target.curr_health}\n"
        logging(line)

        return True


# Отладка
if __name__ == '__main__':
    # empire_factory = AbstractFactory.create_factory('Em')

    # fighter = empire_factory.create_fighter()
    # fighter.add_to_band(3)

    new_unit1 = Unit(main_db.get_unit_by_name('Антипаладин'))
    new_unit2 = Unit(main_db.get_unit_by_name('Мраморная гаргулья'))

    new_unit1.lvl_up()

    new_unit1.attack(new_unit2)
    # new_unit2.attack(new_unit1)
