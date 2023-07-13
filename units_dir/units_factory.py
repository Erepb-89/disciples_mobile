"""Фабрика юнитов"""

import abc
import random
from battle_logging import logging

from client_dir.settings import EM, UH, LD, MC, BATTLE_LOG
from units_dir.units import main_db
from units_dir.ranking import empire_fighter_lvls, empire_mage_lvls, \
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
    # @level_up(empire_fighter_lvls)
    def lvl_up(slot):
        """Боец Империи. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = empire_fighter_lvls[unit.level + 1]
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

    def __init__(self, unit: tuple):
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

    @property
    def is_dead(self):
        """Проверка на живость"""
        return False

    @property
    def is_double(self):
        """Проверка на двухслотовость"""
        return True if self.size == "Большой" else False

    @staticmethod
    def skip_turn(self):
        """Пропуск хода юнита в битве"""
        print(self.name, 'пропускает ход')

    @staticmethod
    def defence(self):
        """Пропуск хода и защита в битве"""
        print(self.name, 'защищается')


    def add_to_band(self, slot):
        """Найм в отряд игрока"""
        main_db.hire_unit(self.name, slot)

    @staticmethod
    def lvl_up(slot):
        """Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot, main_db.PlayerUnits)
        new_unit = hordes_fighter_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    @staticmethod
    def say():
        """Боевой клич"""
        print('fight')

    def attack(self, target):
        """Атака"""
        # Вычисление вероятности попадания
        try:
            accuracy = self.attack_chance.split(
                '/')[0].split('%')[0] / 100
            poison = self.attack_chance.split(
                '/')[1].split('%')[0] / 100
        except BaseException:
            accuracy = int(self.attack_chance.split('%')[0]) / 100

        attack_successful = True if random.random() <= accuracy else False
        # print(attack_successful)

        if attack_successful:
            print(f"{self.name}: Атака успешна")
        else:
            print(f"{self.name}: Промах")

        # Если атака успешна
        if attack_successful:
            # Вычисление урона с учетом брони
            try:
                damage = int(int(self.attack_dmg.split(
                    '/')[0]) * (1 - target.armor * 0.01)) + random.randrange(5)
            except BaseException:
                damage = int(self.attack_dmg *
                             (1 - target.armor * 0.01)) + random.randrange(5)

            # если урон больше, чем здоровье врага, приравниваем урон к
            # здоровью
            damage = min(damage, target.curr_health)

            # вычисление текущего здоровья цели после получения урона
            target.curr_health -= damage

            # если есть вампиризм у атакующего:
            if self.attack_type in ['Высасывание жизни', 'Избыточное высасывание жизни']:
                self.curr_health += int(damage / 2)
                if self.curr_health > self.health:
                    self.curr_health = self.health

                # main_db.update_unit_hp(
                #     self.slot, self.curr_health, main_db.attacker_db)

            line = f"{self.name} наносит урон {damage} воину {target.name}. " \
                   f"Осталось ХП: {target.curr_health}\n"
            logging(line)

            # print(
            #     f"{self.name} наносит урон {damage} воину "
            #     f"{target.name}. Осталось ХП: {target.curr_health}")
        else:
            logging(f"{self.name} промахивается по {target.name}\n")

        # Если текущий юнит - лекарь
        if self.attack_type \
                in ['Лечение', 'Лечение/Исцеление', 'Лечение/Воскрешение']:
            self.skip_turn()

    def heal(self, target):
        """Атака"""
        # print('ходит:', self.name)

        hp = int(self.attack_dmg)
        # если размер лечения больше, чем здоровье цели,
        # приравниваем урон к здоровью
        hp = min(hp, target.curr_health)

        # вычисление текущего здоровья цели после получения лечения
        target.curr_health = hp

# Отладка
if __name__ == '__main__':
    # empire_factory = AbstractFactory.create_factory('Em')

    # fighter = empire_factory.create_fighter()
    # archer = empire_factory.create_archer()
    # mage = empire_factory.create_mage()
    #
    # fighter.add_to_band(3)
    # archer.add_to_band(6)
    # mage.add_to_band(5)

    # fighter.lvl_up(3)
    # fighter.say()
    # archer.say()

    new_unit = Unit(main_db.get_unit_by_name('Адский рыцарь'))
    new_unit2 = Unit(main_db.get_unit_by_name('Мраморная гаргулья'))

    # new_unit.attack(new_unit2)
    # new_unit2.attack(new_unit)

    # new_unit.attack(new_unit2)
    # new_unit2.attack(new_unit)
    #
    # new_unit.attack(new_unit2)
    # new_unit2.attack(new_unit)
    #
    # new_unit.attack(new_unit2)
    # new_unit2.attack(new_unit)

