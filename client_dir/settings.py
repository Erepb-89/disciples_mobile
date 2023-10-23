"""Настройки"""

import os

from PyQt5.QtCore import QRect

BATTLE_LOG = '../battle_log.txt'

BATTLE_ANIM = '../images/gif/battle_anim/'
UNIT_ICONS = '../images/icons/'
UNIT_FACES = '../images/faces/'
TOWN_IMG = '../images/towns/'
PORTRAITS = '../images/portraits/'
GIF_ANIMATIONS = '../images/gif/full_size/'
UNIT_FRAME = '../images/frames/frame_details.png'
FACTIONS = '../images/factions/'
TOWNS = '../images/towns/'
TOWN_ARMY = '../images/towns/army/'
CAPITAL_BUILDING = '../images/towns/capital_building/'
HIRE_SCREEN = '../images/towns/hire_screen/'
INTERF = '../images/interf/'

UNIT_STAND = '../images/gif/unit_stand/'
UNIT_ATTACK = '../images/gif/unit_attack/'
UNIT_ATTACKED = '../images/gif/unit_attacked/'
UNIT_EFFECTS_ATTACK = '../images/gif/unit_effects_attack/'
UNIT_EFFECTS_ATTACKED = '../images/gif/unit_effects_attacked/'
UNIT_EFFECTS_STAND = '../images/gif/unit_effects_stand/'
UNIT_EFFECTS_TARGET = '../images/gif/unit_effects_target/'
UNIT_EFFECTS_AREA = '../images/gif/unit_effects_area/'
UNIT_SHADOW_ATTACK = '../images/gif/unit_shadow_attack/'
UNIT_SHADOW_ATTACKED = '../images/gif/unit_shadow_attacked/'
UNIT_SHADOW_STAND = '../images/gif/unit_shadow_stand/'

TESTING_UNIT_STAND = '../images/testing/unit_stand/'
TESTING_UNIT_ATTACK = '../images/testing/unit_attack/'
TESTING_UNIT_ATTACKED = '../images/testing/unit_attacked/'
TESTING_UNIT_EFFECTS_ATTACK = '../images/testing/unit_effects_attack/'
TESTING_UNIT_EFFECTS_ATTACKED = '../images/testing/unit_effects_attacked/'
TESTING_UNIT_EFFECTS_STAND = '../images/testing/unit_effects_stand/'
TESTING_UNIT_EFFECTS_TARGET = '../images/testing/unit_effects_target/'
TESTING_UNIT_EFFECTS_AREA = '../images/testing/unit_effects_area/'
TESTING_UNIT_SHADOW_ATTACK = '../images/testing/unit_shadow_attack/'
TESTING_UNIT_SHADOW_ATTACKED = '../images/testing/unit_shadow_attacked/'
TESTING_UNIT_SHADOW_STAND = '../images/testing/unit_shadow_stand/'

BATTLE_GROUND = '../images/grounds/'
BATTLE_GROUNDS = os.listdir(BATTLE_GROUND)
COMMON = '../images/common/'
ORIGINAL_GIFS = '../images/gif/original/'
TOWN_ICONS = '../images/towns/capital_building/town_icons/'
ORIGINAL_PNGS = '../images/towns/capital_building/town_icons_original/'
RIGHT_ICONS = os.path.join(COMMON, "right_icons.png")
LEFT_ICONS = os.path.join(COMMON, "left_icons.png")
BACKGROUND = os.path.join(COMMON, "background.png")
PLUG = "Заглушка (Disciples II)-иконка.jpg"
ICON = "(Disciples II)-иконка.jpg"
ELVEN_PLUG = "Elven Alliance.png"
ANY_UNIT = 'Любой юнит'
CLOSEST_UNIT = 'Ближайший юнит'

FRONT = 'front/'
REAR = 'rear/'
OTHERS = 'others'

BIG = 'Большой'
SMALL = 'Обычный'

# races
EM = 'Empire'
UH = 'Undead Hordes'
LD = 'Legions of the Damned'
MC = 'Mountain Clans'

# active units
ACTIVE_UNITS = os.listdir(f'{UNIT_ATTACK}{FRONT}')

# coordinates
X_COORD_1 = 40
X_COORD_2 = 160
X_COORD_3 = 880
X_COORD_4 = 1000

SCREEN_RECT = QRect(0, 0, 1600, 900)
PANEL_RECT = QRect(0, 500, 0, 0)

# building descriptions
ALREADY_BUILT = 'Это здание уже построено'
POSSIBLE_TO_BUILD = 'Это здание можно построить'
NEED_TO_BUILD_PREV = 'Сначала нужно построить здание, предшествующее этому'
ANOTHER_BRANCH = 'Это здание нельзя построить, поскольку была выбрана ' \
                 'другая ветвь развития'

GUILD_DESC = 'Гильдия нужна, чтобы нанимать воров'
MAGIC_DESC = 'Башня магии необходима для изучения заклинаний'
TWMPLE_DESC = 'Храм может лечить и воскрешать воинов в городах и в столице'
COMMON_DESC = 'Эта постройка позволит юнитам совершенствовать свои навыки. ' \
              'Накопив достаточно опыта,'
SPECIAL_DESC = 'Эта постройка нужна, чтобы нанимать '

WORD_EXCEPTIONS = ['']

DECLINATIONS = {
    'Драколич': 'Драколичем',
    'Дрейк Рока': 'Дрейком Рока',
    'Лич': 'Личем',
    'Архилич': 'Архиличем',
    'Вирм Ужаса': 'Вирмом ужаса',
    'Ледяной гигант': 'Ледяным гигантом',
    'Сын Имира': 'Сыном Имира',
    'Стрелок': 'Стрелком',
    'Охотник на ведьм': 'Охотником на ведьм',
    'Повелитель демонов': 'Повелителем демонов',
    'Мраморная гаргулья': 'Мраморной гаргульей',
    'Ониксовая гаргулья': 'Ониксовой гаргульей',
    'Король гномов': 'Королём гномов',
    'Повелитель волков': 'Повелителем волков',
}

MISSION_UNITS = {
    EM: {
        1: 'Гаргулья',
        2: 'Антипаладин',
        3: 'Мраморная гаргулья',
        4: 'Антипаладин',
        5: 'Молох',
        6: 'Повелитель демонов',
    },
    UH: {
        1: 'Мастер-головорез',
        2: 'Рыцарь',
        3: 'Копейщик',
        4: 'Паладин',
        5: 'Ангел',
        6: 'Защитник веры',
    },
    LD: {
        1: 'Мастер-головорез',
        2: 'Рыцарь',
        3: 'Копейщик',
        4: 'Паладин',
        5: 'Ангел',
        6: 'Защитник веры',
    },
    MC: {
        1: 'Мастер-головорез',
        2: 'Зомби',
        3: 'Тёмный властелин',
        4: 'Умертвие',
        5: 'Скелет-чемпион',
        6: 'Лич',
    },

}
