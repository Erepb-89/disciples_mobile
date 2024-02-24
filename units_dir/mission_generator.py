"""Генератор миссий"""
import random

from client_dir.settings import BIG, SMALL, ACTIVE_UNITS, SUPPORT
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


def get_big(units: list) -> list:
    """Получить большие иниты из списка юнитов"""
    big = [unit.name for unit in units
           if unit.size == BIG
           and f'{unit.name}.gif' in ACTIVE_UNITS
           ]
    return big


def get_fighters(units: list) -> list:
    """Получить бойцов из списка юнитов"""
    fighter = [unit.name for unit in units
               if unit.size == SMALL
               and unit.attack_radius == 'Ближайший юнит'
               and f'{unit.name}.gif' in ACTIVE_UNITS
               ]
    return fighter


def get_mages(units: list) -> list:
    """Получить магов из списка юнитов"""
    mage = [unit.name for unit in units
            if unit.size == SMALL
            and unit.attack_radius == 'Любой юнит'
            and unit.attack_purpose == 6
            and 'Лечение' not in unit.attack_type
            and 'Увеличение урона' not in unit.attack_type
            and 'Дополнительная атака' not in unit.attack_type
            and f'{unit.name}.gif' in ACTIVE_UNITS
            ]
    return mage


def get_archers(units: list) -> list:
    """Получить стрелков из списка юнитов"""
    archer = [unit.name for unit in units if unit.size == SMALL
              and unit.attack_radius == 'Любой юнит'
              and unit.attack_purpose == 1
              and 'Лечение' not in unit.attack_type
              and 'Увеличение урона' not in unit.attack_type
              and 'Дополнительная атака' not in unit.attack_type
              and f'{unit.name}.gif' in ACTIVE_UNITS
              ]
    return archer


def get_supports(units: list) -> list:
    """Получить юнитов поддержки (без масс хила) из списка юнитов"""
    support = [unit.name for unit in units if unit.size == SMALL
               and unit.attack_radius == 'Любой юнит'
               and unit.attack_purpose == 1
               and ('Лечение' in unit.attack_type
                    or 'Увеличение урона' in unit.attack_type
                    or 'Дополнительная атака' in unit.attack_type)
               and f'{unit.name}.gif' in ACTIVE_UNITS
               ]
    return support


def get_mass_supports(units: list) -> list:
    """Получить юнитов поддержки (масс хил) из списка юнитов"""
    mass_support = [unit.name for unit in units if unit.size == SMALL
                    and unit.attack_purpose == 6
                    and 'Лечение' in unit.attack_type
                    and f'{unit.name}.gif' in ACTIVE_UNITS
                    ]
    return mass_support


def get_curr_level_units(level: int) -> dict:
    """Получение юнитов текущего уровня"""
    units = main_db.get_units_by_level(level)
    curr_level_units = {}

    big_units = get_big(units)
    fighter = get_fighters(units)
    mage = get_mages(units)
    archer = get_archers(units)
    support = get_supports(units)
    mass_support = get_mass_supports(units)

    # если нет ни стрелков, ни саппортов нужного уровня
    if not archer and not support and not mass_support:
        # берем нужных с уровня ниже
        units = main_db.get_units_by_level(level - 1)
        archer = get_archers(units)
        support = get_supports(units)
        mass_support = get_mass_supports(units)

    # заполняем словарь
    curr_level_units[BIG] = big_units
    curr_level_units['fighter'] = fighter
    curr_level_units['mage'] = mage
    curr_level_units['archer'] = archer
    curr_level_units['support'] = support
    curr_level_units['mass_support'] = mass_support

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
                and (setup == boss_setup or setup == boss_mc_setup):
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
                if (setup
                    in (setup_2, setup_3)
                    or level == 1) \
                        and unit_type == SUPPORT:
                    unit = random.choice(units[SUPPORT])
                    result_dict[slot] = unit

                    # если нет юнитов выбранного типа нужного уровня
                    if not units[unit_type]:
                        # получаем юнитов уровнем ниже
                        units[unit_type] = get_lower_level_units(unit_type, level)

                # иначе включаем возможность добавления в отряд масс хилеров
                elif setup \
                        not in (setup_2, setup_3) \
                        and level != 1 \
                        and unit_type == SUPPORT:
                    unit_type = random.choice(['support',
                                               'mass_support'])
                    unit = random.choice(units[unit_type])
                    result_dict[slot] = unit

                    # если нет юнитов выбранного типа нужного уровня
                    if not units[unit_type]:
                        # получаем юнитов уровнем ниже
                        units[unit_type] = get_lower_level_units(unit_type, level)

                # выбор из магов и стрелков
                elif unit_type == SMALL:
                    unit_type = random.choice(['mage',
                                               'archer'])
                    unit = random.choice(units[unit_type])
                    result_dict[slot] = unit

                    # если нет юнитов выбранного типа нужного уровня
                    if not units[unit_type]:
                        # получаем юнитов уровнем ниже
                        units[unit_type] = get_lower_level_units(unit_type, level)

        # если None
        else:
            result_dict[slot] = None

    return result_dict

def get_lower_level_units(unit_type: str, level: int) -> any:
    """Получение юнитов уровнем ниже"""
    units = get_curr_level_units(level - 1)
    unit = random.choice(units[unit_type])

    return unit
