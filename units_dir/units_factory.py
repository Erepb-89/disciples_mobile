"""Units factory"""
import abc

from client_dir.settings import EM, UH, LD, MC
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
        return 'Сквайр'

    @property
    def size(self):
        return 'Обычный'

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
        unit = main_db.get_unit_by_slot(slot)
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
        return 'Ученик'

    @property
    def size(self):
        return 'Обычный'

    @staticmethod
    def add_to_band(slot):
        """Ученик. Найм в отряд игрока"""
        main_db.hire_unit('Ученик', slot)

    @staticmethod
    def lvl_up(slot):
        """Маг Империи. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
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
        return 'Лучник'

    @property
    def size(self):
        return 'Обычный'

    @staticmethod
    def add_to_band(slot):
        """Лучник. Найм в отряд игрока"""
        main_db.hire_unit('Лучник', slot)

    @staticmethod
    def lvl_up(slot):
        """Стрелок Империи. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
        new_unit = empire_archer_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    def say(self):
        """Боевой клич"""
        print('bow')


class EmpireSupport:
    """Поддержка Империи"""

    @property
    def name(self):
        return 'Послушник'

    @property
    def size(self):
        return 'Обычный'

    @staticmethod
    def add_to_band(slot):
        """Послушник. Найм в отряд игрока"""
        main_db.hire_unit('Послушник', slot)

    @staticmethod
    def lvl_up(slot):
        """Поддержка Империи. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
        new_unit = empire_support_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    def say(self):
        """Боевой клич"""
        print('help')


class EmpireSpecial:
    """Особый юнит Империи"""

    @property
    def name(self):
        return 'Титан'

    @property
    def size(self):
        return 'Большой'

    @staticmethod
    def add_to_band(slot):
        """Титан. Найм в отряд игрока"""
        main_db.hire_unit('Титан', slot)

    @staticmethod
    def lvl_up(slot):
        """Особый юнит Империи. Повышение уровня"""
        pass


# Hordes classes

class HordesFighter:
    """Боец Орд нежити"""

    @property
    def name(self):
        return 'Боец'

    @property
    def size(self):
        return 'Обычный'

    @staticmethod
    def add_to_band(slot):
        """Боец. Найм в отряд игрока"""
        main_db.hire_unit('Боец', slot)

    @staticmethod
    def lvl_up(slot):
        """Боец Орд нежити. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
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
        return 'Посвящённый'

    @property
    def size(self):
        return 'Обычный'

    @staticmethod
    def add_to_band(slot):
        """Посвящённый. Найм в отряд игрока"""
        main_db.hire_unit('Посвящённый', slot)

    @staticmethod
    def lvl_up(slot):
        """Маг Орд нежити. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
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
        return 'Привидение'

    @property
    def size(self):
        return 'Обычный'

    @staticmethod
    def add_to_band(slot):
        """Привидение. Найм в отряд игрока"""
        main_db.hire_unit('Привидение', slot)

    @staticmethod
    def lvl_up(slot):
        """Стрелок Орд нежити. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
        new_unit = hordes_archer_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    def say(self):
        """Боевой клич"""
        print('bow')


class HordesSupport:
    """Поддержка Орд нежити"""

    @property
    def name(self):
        return 'Виверна'

    @property
    def size(self):
        return 'Большой'

    @staticmethod
    def add_to_band(slot):
        """Виверна. Найм в отряд игрока"""
        main_db.hire_unit('Виверна', slot)

    @staticmethod
    def lvl_up(slot):
        """Поддержка Орд нежити. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
        new_unit = hordes_support_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    def say(self):
        """Боевой клич"""
        print('help')


class HordesSpecial:
    """Особый юнит Орд нежити"""

    @property
    def name(self):
        return 'Оборотень'

    @property
    def size(self):
        return 'Обычный'

    @staticmethod
    def add_to_band(slot):
        """Оборотень. Найм в отряд игрока"""
        main_db.hire_unit('Оборотень', slot)

    @staticmethod
    def lvl_up(slot):
        """Особый юнит Орд нежити. Повышение уровня"""
        pass


# Legions classes

class LegionsFighter:
    """Боец Легионов проклятых"""

    @property
    def name(self):
        return 'Одержимый'

    @property
    def size(self):
        return 'Обычный'

    @staticmethod
    def add_to_band(slot):
        """Одержимый. Найм в отряд игрока"""
        main_db.hire_unit('Одержимый', slot)

    @staticmethod
    def lvl_up(slot):
        """Боец Легионов проклятых. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
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
        return 'Сектант'

    @property
    def size(self):
        return 'Обычный'

    @staticmethod
    def add_to_band(slot):
        """Сектант. Найм в отряд игрока"""
        main_db.hire_unit('Сектант', slot)

    @staticmethod
    def lvl_up(slot):
        """Маг Легионов проклятых. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
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
        return 'Гаргулья'

    @property
    def size(self):
        return 'Большой'

    @staticmethod
    def add_to_band(slot):
        """Гаргулья. Найм в отряд игрока"""
        main_db.hire_unit('Гаргулья', slot)

    @staticmethod
    def lvl_up(slot):
        """Стрелок Легионов проклятых. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
        new_unit = legions_archer_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    def say(self):
        """Боевой клич"""
        print('bow')


class LegionsSupport:
    """Поддержка Легионов проклятых"""

    @property
    def name(self):
        return 'Чёрт'

    @property
    def size(self):
        return 'Большой'

    @staticmethod
    def add_to_band(slot):
        """Чёрт. Найм в отряд игрока"""
        main_db.hire_unit('Чёрт', slot)

    @staticmethod
    def lvl_up(slot):
        """Поддержка Легионов проклятых. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
        new_unit = legions_support_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    def say(self):
        """Боевой клич"""
        print('help')


class LegionsSpecial:
    """Особый юнит Легионов проклятых"""

    @property
    def name(self):
        return 'Изверг'

    @property
    def size(self):
        return 'Большой'

    @staticmethod
    def add_to_band(slot):
        """Изверг. Найм в отряд игрока"""
        main_db.hire_unit('Изверг', slot)

    @staticmethod
    def lvl_up(slot):
        """Особый юнит Легионов проклятых. Повышение уровня"""
        pass


# Clans classes

class ClansFighter:
    """Боец Горных кланов"""

    @property
    def name(self):
        return 'Гном'

    @property
    def size(self):
        return 'Обычный'

    @staticmethod
    def add_to_band(slot):
        """Гном. Найм в отряд игрока"""
        main_db.hire_unit('Гном', slot)

    @staticmethod
    def lvl_up(slot):
        """Боец Горных кланов. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
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
        return 'Желторотик'

    @property
    def size(self):
        return 'Обычный'

    @staticmethod
    def add_to_band(slot):
        """Желторотик. Найм в отряд игрока"""
        main_db.hire_unit('Желторотик', slot)

    @staticmethod
    def lvl_up(slot):
        """Маг Горных кланов. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
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
        return 'Метатель топоров'

    @property
    def size(self):
        return 'Обычный'

    @staticmethod
    def add_to_band(slot):
        """Метатель топоров. Найм в отряд игрока"""
        main_db.hire_unit('Метатель топоров', slot)

    @staticmethod
    def lvl_up(slot):
        """Стрелок Горных кланов. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
        new_unit = clans_archer_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    def say(self):
        """Боевой клич"""
        print('bow')


class ClansSupport:
    """Поддержка Горных кланов"""

    @property
    def name(self):
        return 'Холмовой гигант'

    @property
    def size(self):
        return 'Большой'

    @staticmethod
    def add_to_band(slot):
        """Холмовой гигант. Найм в отряд игрока"""
        main_db.hire_unit('Холмовой гигант', slot)

    @staticmethod
    def lvl_up(slot):
        """Поддержка Горных кланов. Повышение уровня"""
        unit = main_db.get_unit_by_slot(slot)
        new_unit = clans_support_lvls[unit.level + 1]
        print(unit.name, 'повысил уровень до', new_unit)
        main_db.replace_unit(slot, new_unit)

    def say(self):
        """Боевой клич"""
        print('help')


class ClansSpecial:
    """Особый юнит Горных кланов"""

    @property
    def name(self):
        return 'Йети'

    @property
    def size(self):
        return 'Большой'

    @staticmethod
    def add_to_band(slot):
        """Йети. Найм в отряд игрока"""
        main_db.hire_unit('Йети', slot)

    @staticmethod
    def lvl_up(slot):
        """Особый юнит Горных кланов. Повышение уровня"""
        pass


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
        pass

    @abc.abstractmethod
    def create_mage(self):
        pass

    @abc.abstractmethod
    def create_archer(self):
        pass

    @abc.abstractmethod
    def create_support(self):
        pass

    @abc.abstractmethod
    def create_special(self):
        pass


class EmpireFactory(AbstractFactory):
    """Фабрика Империи"""

    def create_fighter(self):
        return EmpireFighter()

    def create_archer(self):
        return EmpireArcher()

    def create_mage(self):
        return EmpireMage()

    def create_support(self):
        return EmpireSupport()

    def create_special(self):
        return EmpireSpecial()


class HordesFactory(AbstractFactory):
    """Фабрика Орд нежити"""

    def create_fighter(self):
        return HordesFighter()

    def create_archer(self):
        return HordesArcher()

    def create_mage(self):
        return HordesMage()

    def create_support(self):
        return HordesSupport()

    def create_special(self):
        return HordesSpecial()


class LegionsFactory(AbstractFactory):
    """Фабрика Легионов Проклятых"""

    def create_fighter(self):
        return LegionsFighter()

    def create_archer(self):
        return LegionsArcher()

    def create_mage(self):
        return LegionsMage()

    def create_support(self):
        return LegionsSupport()

    def create_special(self):
        return LegionsSpecial()


class ClansFactory(AbstractFactory):
    """Фабрика Горных кланов"""

    def create_fighter(self):
        return ClansFighter()

    def create_archer(self):
        return ClansArcher()

    def create_mage(self):
        return ClansMage()

    def create_support(self):
        return ClansSupport()

    def create_special(self):
        return ClansSpecial()


# Отладка
if __name__ == '__main__':
    empire_factory = AbstractFactory.create_factory('Em')

    fighter = empire_factory.create_fighter()
    # archer = empire_factory.create_archer()
    # mage = empire_factory.create_mage()
    #
    # fighter.add_to_band(3)
    # archer.add_to_band(6)
    # mage.add_to_band(5)

    fighter.lvl_up(3)
    # fighter.say()
    # archer.say()
