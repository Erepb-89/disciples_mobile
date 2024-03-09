"""Генератор миссий"""
import random

from client_dir.settings import BIG, SMALL, ACTIVE_UNITS, SUPPORT, ADDITIONAL_ATTACK, INCREASE_DMG, HEAL
from units_dir.units import main_db

setup_6 = [
    {
        1: None, 2: BIG,
        3: SMALL, 4: SMALL,
        5: None, 6: BIG,
    },
    {
        1: SMALL, 2: SMALL,
        3: SMALL, 4: SMALL,
        5: SMALL, 6: SMALL,
    },
    {
        1: SMALL, 2: SMALL,
        3: None, 4: BIG,
        5: SMALL, 6: SMALL,
    },
    {
        1: None, 2: BIG,
        3: SUPPORT, 4: SMALL,
        5: None, 6: BIG,
    },
    {
        1: SMALL, 2: SMALL,
        3: SUPPORT, 4: SMALL,
        5: SMALL, 6: SMALL,
    },
    {
        1: SUPPORT, 2: SMALL,
        3: None, 4: BIG,
        5: SMALL, 6: SMALL,
    }
]
setup_5 = [
    {
        1: None, 2: BIG,
        3: None, 4: SMALL,
        5: None, 6: BIG,
    },
    {
        1: None, 2: BIG,
        3: SMALL, 4: None,
        5: None, 6: BIG,
    },
    {
        1: None, 2: BIG,
        3: SUPPORT, 4: None,
        5: None, 6: BIG,
    },
    {
        1: SMALL, 2: None,
        3: None, 4: BIG,
        5: SMALL, 6: SMALL,
    },
    {
        1: SUPPORT, 2: None,
        3: None, 4: BIG,
        5: SMALL, 6: SMALL,
    },
    {
        1: SMALL, 2: SMALL,
        3: None, 4: BIG,
        5: SUPPORT, 6: None,
    },
    {
        1: SMALL, 2: SMALL,
        3: None, 4: BIG,
        5: SMALL, 6: None,
    },
    {
        1: SMALL, 2: SMALL,
        3: None, 4: BIG,
        5: None, 6: SMALL,
    }
]
setup_4 = [
    {
        1: SMALL, 2: None,
        3: None, 4: BIG,
        5: SMALL, 6: None,
    },
    {
        1: None, 2: SMALL,
        3: None, 4: BIG,
        5: SMALL, 6: None,
    },
    {
        1: SMALL, 2: None,
        3: None, 4: BIG,
        5: None, 6: SMALL,
    },
    {
        1: None, 2: SMALL,
        3: None, 4: BIG,
        5: None, 6: SMALL,
    },
    {
        1: None, 2: BIG,
        3: None, 4: None,
        5: None, 6: BIG,
    },
    {
        1: None, 2: BIG,
        3: None, 4: BIG,
        5: None, 6: None,
    },
    {
        1: None, 2: None,
        3: None, 4: BIG,
        5: None, 6: BIG,
    },
    {
        1: SMALL, 2: None,
        3: SUPPORT, 4: SMALL,
        5: SMALL, 6: None,
    },
    {
        1: SMALL, 2: None,
        3: SMALL, 4: SMALL,
        5: SMALL, 6: None,
    },
    {
        1: None, 2: SMALL,
        3: SMALL, 4: SMALL,
        5: SMALL, 6: None,
    },
    {
        1: None, 2: SMALL,
        3: SUPPORT, 4: SMALL,
        5: SMALL, 6: None,
    },
    {
        1: SMALL, 2: None,
        3: SMALL, 4: SMALL,
        5: None, 6: SMALL,
    },
    {
        1: SMALL, 2: None,
        3: SUPPORT, 4: SMALL,
        5: None, 6: SMALL,
    },
    {
        1: None, 2: SMALL,
        3: SMALL, 4: SMALL,
        5: None, 6: SMALL,
    },
    {
        1: None, 2: SMALL,
        3: SUPPORT, 4: SMALL,
        5: None, 6: SMALL,
    },
    {
        1: SMALL, 2: SMALL,
        3: None, 4: None,
        5: None, 6: BIG,
    },
    {
        1: None, 2: BIG,
        3: SMALL, 4: SMALL,
        5: None, 6: None,
    },
    {
        1: None, 2: None,
        3: None, 4: BIG,
        5: SMALL, 6: SMALL,
    },
    {
        1: None, 2: None,
        3: None, 4: BIG,
        5: SUPPORT, 6: SMALL,
    },
    {
        1: SMALL, 2: SMALL,
        3: None, 4: None,
        5: SMALL, 6: SMALL,
    },
    {
        1: SUPPORT, 2: SMALL,
        3: None, 4: None,
        5: SMALL, 6: SMALL,
    },
    {
        1: SMALL, 2: SMALL,
        3: SMALL, 4: SMALL,
        5: None, 6: None,
    },
    {
        1: SMALL, 2: SMALL,
        3: SUPPORT, 4: SMALL,
        5: None, 6: None,
    },
    {
        1: None, 2: None,
        3: SMALL, 4: SMALL,
        5: SMALL, 6: SMALL,
    },
    {
        1: None, 2: None,
        3: SUPPORT, 4: SMALL,
        5: SMALL, 6: SMALL,
    },
]
setup_3 = [
    {
        1: SMALL, 2: None,
        3: None, 4: BIG,
        5: None, 6: None,
    },
    {
        1: SMALL, 2: None,
        3: None, 4: BIG,
        5: None, 6: None,
    },
    {
        1: None, 2: None,
        3: None, 4: BIG,
        5: SMALL, 6: None,
    },
    {
        1: None, 2: SMALL,
        3: None, 4: BIG,
        5: None, 6: None,
    },
    {
        1: None, 2: None,
        3: None, 4: BIG,
        5: None, 6: SMALL,
    },
    {
        1: SMALL, 2: None,
        3: SMALL, 4: SMALL,
        5: None, 6: None,
    },
    {
        1: SMALL, 2: None,
        3: SUPPORT, 4: SMALL,
        5: None, 6: None,
    },
    {
        1: None, 2: None,
        3: SMALL, 4: SMALL,
        5: SMALL, 6: None,
    },
    {
        1: None, 2: SMALL,
        3: SMALL, 4: SMALL,
        5: None, 6: None,
    },
    {
        1: None, 2: None,
        3: SMALL, 4: SMALL,
        5: None, 6: SMALL,
    },
    {
        1: None, 2: SMALL,
        3: SMALL, 4: None,
        5: None, 6: SMALL,
    },
    {
        1: None, 2: SMALL,
        3: SUPPORT, 4: None,
        5: None, 6: SMALL,
    },
    {
        1: None, 2: SMALL,
        3: None, 4: SMALL,
        5: None, 6: SMALL,
    },
]
setup_2 = [
    {
        1: None, 2: None,
        3: None, 4: BIG,
        5: None, 6: None,
    },
    {
        1: None, 2: None,
        3: SMALL, 4: SMALL,
        5: None, 6: None,
    },
    {
        1: SMALL, 2: None,
        3: None, 4: SMALL,
        5: None, 6: None,
    },
    {
        1: None, 2: None,
        3: None, 4: SMALL,
        5: SMALL, 6: None,
    },
    {
        1: None, 2: SMALL,
        3: None, 4: None,
        5: None, 6: SMALL,
    },
    {
        1: None, 2: SMALL,
        3: None, 4: SMALL,
        5: None, 6: None,
    },
    {
        1: None, 2: None,
        3: None, 4: SMALL,
        5: None, 6: SMALL,
    },
]
boss_setup = [
    # {
    #     1: None, 2: None,
    #     3: None, 4: BIG,
    #     5: None, 6: None,
    # },
    {
        1: None, 2: None,
        3: None, 4: BIG,
        5: None, 6: SMALL,
    },
    {
        1: None, 2: None,
        3: None, 4: BIG,
        5: SMALL, 6: None,
    },
    {
        1: SUPPORT, 2: None,
        3: None, 4: BIG,
        5: None, 6: None,
    },
    {
        1: None, 2: SMALL,
        3: None, 4: BIG,
        5: None, 6: None,
    },
    {
        1: SMALL, 2: None,
        3: None, 4: BIG,
        5: None, 6: None,
    },
    {
        1: SUPPORT, 2: None,
        3: None, 4: BIG,
        5: None, 6: None,
    }
]

boss_mc_setup = [
    {
        1: SMALL, 2: SMALL,
        3: None, 4: BIG,
        5: None, 6: None,
    },
    {
        1: None, 2: SMALL,
        3: None, 4: BIG,
        5: SMALL, 6: None,
    },
    {
        1: SUPPORT, 2: None,
        3: None, 4: BIG,
        5: SMALL, 6: None,
    },
    {
        1: None, 2: SMALL,
        3: None, 4: BIG,
        5: None, 6: SMALL,
    },
    {
        1: SMALL, 2: None,
        3: None, 4: BIG,
        5: SMALL, 6: None,
    },
    {
        1: SUPPORT, 2: None,
        3: None, 4: BIG,
        5: None, 6: SMALL,
    }
]


def unit_is_active(unit):
    """Проверяет активность юнита (по наличию моделек))"""
    return f'{unit.name}.gif' in ACTIVE_UNITS


def get_big(units: list) -> list:
    """Получить большие иниты из списка юнитов"""
    big = [unit.name for unit in units
           if unit.size == BIG
           and unit_is_active(unit)
           ]
    return big


def get_fighters(branch: str, level: int) -> list:
    """Получить бойцов из списка юнитов"""
    fighters = main_db.get_units_by_branch_and_level(branch, level)
    fighters = [unit.name for unit in fighters if unit_is_active(unit)]

    return fighters


def get_archers(branch: str, level: int) -> list:
    """Получить стрелков из списка юнитов"""
    archers = main_db.get_units_by_branch_and_level(branch, level)
    archers = [unit.name for unit in archers
               if unit_is_active(unit) and unit.size != BIG]

    return archers


def get_mages(branch: str, level: int) -> list:
    """Получить магов из списка юнитов"""
    mages = main_db.get_units_by_branch_and_level(branch, level)
    mages = [unit.name for unit in mages
             if unit_is_active(unit) and unit.attack_purpose == 6]

    return mages


def get_supports(branch: str, level: int) -> list:
    """Получить юнитов поддержки (без масс хила) из списка юнитов"""
    supports = main_db.get_units_by_branch_and_level(branch, level)
    supports = [unit.name for unit in supports
                if unit_is_active(unit) and unit.attack_purpose == 1
                and unit.size != BIG]

    return supports


def get_mass_supports(branch: str, level: int) -> list:
    """Получить юнитов поддержки (масс хил) из списка юнитов"""
    mass_supports = main_db.get_units_by_branch_and_level(branch, level)
    mass_supports = [unit.name for unit in mass_supports
                     if unit_is_active(unit) and unit.attack_purpose == 6
                     and unit.size != BIG]

    return mass_supports


def get_curr_level_units(level: int) -> dict:
    """Получение юнитов текущего уровня"""
    units = main_db.get_units_by_level(level)
    curr_level_units = {}

    big_units = get_big(units)
    fighters = get_fighters('fighter', level)
    mages = get_mages('mage', level)
    archers = get_archers('archer', level)
    supports = get_supports('support', level)
    mass_supports = get_mass_supports('support', level)

    # если нет ни стрелков, ни саппортов нужного уровня
    if not archers and not supports and not mass_supports:
        # берем нужных с уровня ниже
        archers = get_archers('archer', level - 1)
        supports = get_supports('support', level - 1)
        mass_supports = get_mass_supports('support', level - 1)

    # заполняем словарь
    curr_level_units[BIG] = big_units
    curr_level_units['fighter'] = fighters
    curr_level_units['mage'] = mages
    curr_level_units['archer'] = archers
    curr_level_units['support'] = supports
    curr_level_units['mass_support'] = mass_supports

    return curr_level_units


def unit_selector(level: int, setup: list) -> dict:
    """Получение юнитов по местоположению и типу"""
    # получаем юнитов заданного уровня
    units = get_curr_level_units(level)

    result_dict = {}
    mask = random.choice(setup)
    for slot, unit_type in mask.items():
        # если это Босс
        if unit_type == BIG \
                and setup in (boss_setup, boss_mc_setup):
            unit = random.choice(
                get_curr_level_units(level + 2)[BIG])
            result_dict[slot] = unit

        # если юнит большой
        elif unit_type == BIG:
            unit = random.choice(units[BIG])
            result_dict[slot] = unit

        # если юнит обычный и не None
        elif unit_type is not None:
            # для четных слотов
            if slot % 2 == 0:
                unit = random.choice(units['fighter'])
                result_dict[slot] = unit

            # для нечетных слотов
            else:
                # если сетап маленький, исключаем масс хилеров
                if small_support_setup(level, setup, unit_type):
                    unit = random.choice(units[unit_type])
                    result_dict[slot] = unit

                    # если нет юнитов выбранного типа нужного уровня
                    units = lower_level_units(level, unit_type, units)

                # иначе включаем возможность добавления в отряд масс хилеров
                elif big_support_setup(level, setup, unit_type):
                    unit_type = random.choice(['support',
                                               'mass_support'])
                    unit = random.choice(units[unit_type])
                    result_dict[slot] = unit

                    # если нет юнитов выбранного типа нужного уровня
                    units = lower_level_units(level, unit_type, units)

                # выбор из магов и стрелков
                elif unit_type == SMALL:
                    unit_type = random.choice(['mage',
                                               'archer'])
                    if units['archer']:
                        unit = random.choice(units[unit_type])
                    else:
                        unit = random.choice(units['mage'])
                    result_dict[slot] = unit

                    # если нет юнитов выбранного типа нужного уровня
                    units = lower_level_units(level, unit_type, units)

        # если None
        else:
            result_dict[slot] = None

    return result_dict


def lower_level_units(level, unit_type, units) -> dict:
    if not units[unit_type]:
        # получаем юнита уровнем ниже
        units[unit_type] = get_lower_level_unit(unit_type, level)
    return units


def small_support_setup(level: int,
                        setup: list,
                        unit_type: str) -> bool:
    return (setup
            in (setup_2, setup_3)
            or level == 1) \
           and unit_type == SUPPORT


def big_support_setup(level: int,
                      setup: list,
                      unit_type: str) -> bool:
    return setup \
           not in (setup_2, setup_3) \
           and level != 1 \
           and unit_type == SUPPORT


def get_lower_level_unit(unit_type: str, level: int) -> any:
    """Получение юнита уровнем ниже"""
    units = get_curr_level_units(level - 1)
    unit = random.choice(units[unit_type])

    return unit
