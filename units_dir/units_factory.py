"""Фабрика юнитов"""

import abc

from client_dir.settings import EM, UH, LD, MC
from units_dir.units import main_db


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
        return '200'

    @property
    def upgrade_b(self):
        return 'Разрушенный храм'

    @staticmethod
    def add_to_band(slot):
        """Титан. Найм в отряд игрока"""
        main_db.hire_unit('Титан', slot)


# герои Империи
class EmpireHeroFighter:
    """Герой-боец Империи"""

    @property
    def name(self):
        """Имя"""
        return 'Рыцарь на пегасе'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '500'

    @staticmethod
    def add_to_band(slot):
        """Рыцарь на пегасе. Найм в отряд игрока"""
        main_db.hire_unit('Рыцарь на пегасе', slot)


class EmpireHeroMage:
    """Герой-маг Империи"""

    @property
    def name(self):
        """Имя"""
        return 'Архимаг'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '500'

    @staticmethod
    def add_to_band(slot):
        """Архимаг. Найм в отряд игрока"""
        main_db.hire_unit('Архимаг', slot)


class EmpireHeroArcher:
    """Герой-стрелок Империи"""

    @property
    def name(self):
        """Имя"""
        return 'Рейнджер'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '500'

    @staticmethod
    def add_to_band(slot):
        """Рейнджер. Найм в отряд игрока"""
        main_db.hire_unit('Рейнджер', slot)


class EmpireHeroRog:
    """Герой-жезловик Империи"""

    @property
    def name(self):
        """Имя"""
        return 'Архангел'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '300'

    @staticmethod
    def add_to_band(slot):
        """Архангел. Найм в отряд игрока"""
        main_db.hire_unit('Архангел', slot)


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
        return '200'

    @property
    def upgrade_b(self):
        return 'Логово оборотней'

    @staticmethod
    def add_to_band(slot):
        """Оборотень. Найм в отряд игрока"""
        main_db.hire_unit('Оборотень', slot)


# герои Орд нежити
class HordesHeroFighter:
    """Герой-боец Орд нежити"""

    @property
    def name(self):
        """Имя"""
        return 'Рыцарь смерти'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '500'

    @staticmethod
    def add_to_band(slot):
        """Рыцарь смерти. Найм в отряд игрока"""
        main_db.hire_unit('Рыцарь смерти', slot)


class HordesHeroMage:
    """Герой-маг Орд нежити"""

    @property
    def name(self):
        """Имя"""
        return 'Королева личей'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '500'

    @staticmethod
    def add_to_band(slot):
        """Королева личей. Найм в отряд игрока"""
        main_db.hire_unit('Королева личей', slot)


class HordesHeroArcher:
    """Герой-стрелок Орд нежити"""

    @property
    def name(self):
        """Имя"""
        return 'Носферату'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '500'

    @staticmethod
    def add_to_band(slot):
        """Носферату. Найм в отряд игрока"""
        main_db.hire_unit('Носферату', slot)


class HordesHeroRog:
    """Герой-жезловик Орд нежити"""

    @property
    def name(self):
        """Имя"""
        return 'Баньши'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '300'

    @staticmethod
    def add_to_band(slot):
        """Баньши. Найм в отряд игрока"""
        main_db.hire_unit('Баньши', slot)


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
        return '200'

    @property
    def upgrade_b(self):
        return 'Храм Горестей'

    @staticmethod
    def add_to_band(slot):
        """Изверг. Найм в отряд игрока"""
        main_db.hire_unit('Изверг', slot)


# герои Легионов проклятых
class LegionsHeroFighter:
    """Герой-боец Легионов проклятых"""

    @property
    def name(self):
        """Имя"""
        return 'Герцог'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '500'

    @staticmethod
    def add_to_band(slot):
        """Герцог. Найм в отряд игрока"""
        main_db.hire_unit('Герцог', slot)


class LegionsHeroMage:
    """Герой-маг Легионов проклятых"""

    @property
    def name(self):
        """Имя"""
        return 'Архидьявол'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '500'

    @staticmethod
    def add_to_band(slot):
        """Архидьявол. Найм в отряд игрока"""
        main_db.hire_unit('Архидьявол', slot)


class LegionsHeroArcher:
    """Герой-стрелок Легионов проклятых"""

    @property
    def name(self):
        """Имя"""
        return 'Советник'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '500'

    @staticmethod
    def add_to_band(slot):
        """Советник. Найм в отряд игрока"""
        main_db.hire_unit('Советник', slot)


class LegionsHeroRog:
    """Герой-жезловик Легионов проклятых"""

    @property
    def name(self):
        """Имя"""
        return 'Баронесса'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '300'

    @staticmethod
    def add_to_band(slot):
        """Баронесса. Найм в отряд игрока"""
        main_db.hire_unit('Баронесса', slot)


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
        pass

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
        return '250'

    @property
    def upgrade_b(self):
        return 'Горное логово'

    @staticmethod
    def add_to_band(slot):
        """Йети. Найм в отряд игрока"""
        main_db.hire_unit('Йети', slot)

    @staticmethod
    def lvl_up(slot):
        """Особый юнит Горных кланов. Повышение уровня"""


# герои Горных кланов
class ClansHeroFighter:
    """Герой-боец Горных кланов"""

    @property
    def name(self):
        """Имя"""
        return 'Королевский страж'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '500'

    @staticmethod
    def add_to_band(slot):
        """Королевский страж. Найм в отряд игрока"""
        main_db.hire_unit('Королевский страж', slot)


class ClansHeroMage:
    """Герой-маг Горных кланов"""

    @property
    def name(self):
        """Имя"""
        return 'Хранитель знаний'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '500'

    @staticmethod
    def add_to_band(slot):
        """Хранитель знаний. Найм в отряд игрока"""
        main_db.hire_unit('Хранитель знаний', slot)


class ClansHeroArcher:
    """Герой-стрелок Горных кланов"""

    @property
    def name(self):
        """Имя"""
        return 'Инженер'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '500'

    @staticmethod
    def add_to_band(slot):
        """Инженер. Найм в отряд игрока"""
        main_db.hire_unit('Инженер', slot)


class ClansHeroRog:
    """Герой-жезловик Горных кланов"""

    @property
    def name(self):
        """Имя"""
        return 'Гном-чемпион'

    @property
    def size(self):
        """Размер"""
        return 'Обычный'

    @property
    def cost(self):
        """Стоимость"""
        return '300'

    @staticmethod
    def add_to_band(slot):
        """Гном-чемпион. Найм в отряд игрока"""
        main_db.hire_unit('Гном-чемпион', slot)


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

    @abc.abstractmethod
    def create_hero_fighter(self):
        """Создать героя-бойца"""

    @abc.abstractmethod
    def create_hero_mage(self):
        """Создать героя-мага"""

    @abc.abstractmethod
    def create_hero_archer(self):
        """Создать героя-стрелка"""

    @abc.abstractmethod
    def create_hero_rog(self):
        """Создать героя-жезловика"""


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

    def create_hero_fighter(self):
        """Создать героя-бойца"""
        return EmpireHeroFighter()

    def create_hero_mage(self):
        """Создать героя-мага"""
        return EmpireHeroMage()

    def create_hero_archer(self):
        """Создать героя-стрелка"""
        return EmpireHeroArcher()

    def create_hero_rog(self):
        """Создать героя-жезловика"""
        return EmpireHeroRog()


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

    def create_hero_fighter(self):
        """Создать героя-бойца"""
        return HordesHeroFighter()

    def create_hero_mage(self):
        """Создать героя-мага"""
        return HordesHeroMage()

    def create_hero_archer(self):
        """Создать героя-стрелка"""
        return HordesHeroArcher()

    def create_hero_rog(self):
        """Создать героя-жезловика"""
        return HordesHeroRog()


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

    def create_hero_fighter(self):
        """Создать героя-бойца"""
        return LegionsHeroFighter()

    def create_hero_mage(self):
        """Создать героя-мага"""
        return LegionsHeroMage()

    def create_hero_archer(self):
        """Создать героя-стрелка"""
        return LegionsHeroArcher()

    def create_hero_rog(self):
        """Создать героя-жезловика"""
        return LegionsHeroRog()


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

    def create_hero_fighter(self):
        """Создать героя-бойца"""
        return ClansHeroFighter()

    def create_hero_mage(self):
        """Создать героя-мага"""
        return ClansHeroMage()

    def create_hero_archer(self):
        """Создать героя-стрелка"""
        return ClansHeroArcher()

    def create_hero_rog(self):
        """Создать героя-жезловика"""
        return ClansHeroRog()
