"""Настройки"""

import os

from PyQt5.QtCore import QRect

BATTLE_LOG = '../battle_log.txt'

BATTLE_ANIM = '../images/gif/battle_anim/'
UNIT_ICONS = '../images/icons/'
UNIT_FACES = '../images/faces/'
CURSOR = '../images/cursor/'
TOWN_IMG = '../images/towns/'
PORTRAITS = '../images/portraits/'
GIF_ANIMATIONS = '../images/gif/full_size/'
UNIT_FRAME = '../images/frames/frame_details.png'
FACTIONS = '../images/factions/'
TOWNS = '../images/towns/'
TOWN_ARMY = '../images/towns/army/'
CAPITAL_BUILDING = '../images/towns/capital_building/'
CAPITAL_ANIM = '../images/towns/capital_anim/'
CAPITAL_CONSTRUCTION = '../images/towns/capital_construction/'
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

TESTING_UNIT_STAND = '../images/testing/new/unit_stand/'
TESTING_UNIT_ATTACK = '../images/testing/new/unit_attack/'
TESTING_UNIT_ATTACKED = '../images/testing/new/unit_attacked/'
TESTING_UNIT_EFFECTS_ATTACK = '../images/testing/new/unit_effects_attack/'
TESTING_UNIT_EFFECTS_ATTACKED = '../images/testing/new/unit_effects_attacked/'
TESTING_UNIT_EFFECTS_STAND = '../images/testing/new/unit_effects_stand/'
TESTING_UNIT_EFFECTS_TARGET = '../images/testing/new/unit_effects_target/'
TESTING_UNIT_EFFECTS_AREA = '../images/testing/new/unit_effects_area/'
TESTING_UNIT_SHADOW_ATTACK = '../images/testing/new/unit_shadow_attack/'
TESTING_UNIT_SHADOW_ATTACKED = '../images/testing/new/unit_shadow_attacked/'
TESTING_UNIT_SHADOW_STAND = '../images/testing/new/unit_shadow_stand/'

BATTLE_GROUND = '../images/grounds/'
BATTLE_GROUNDS = os.listdir(BATTLE_GROUND)
COMMON = '../images/common/'
ORIGINAL_GIFS = '../images/gif/original/'
TOWN_ICONS = '../images/towns/capital_building/town_icons/'
ORIGINAL_PNGS = '../images/towns/capital_building/town_icons_original/'
RIGHT_ICONS = os.path.join(COMMON, "right_icons.png")
LEFT_ICONS = os.path.join(COMMON, "left_icons.png")
BACKGROUND = os.path.join(COMMON, "background.png")
ARMY_BG = os.path.join(COMMON, "enemy_army.png")
PLUG = "Заглушка (Disciples II)-иконка.jpg"
ICON = "(Disciples II)-иконка.jpg"
ELVEN_PLUG = "Elven Alliance.png"
ANY_UNIT = 'Любой юнит'
CLOSEST_UNIT = 'Ближайший юнит'

PLAYER = 'player'
ENEMY = 'enemy'

FRONT = 'front/'
REAR = 'rear/'
OTHERS = 'others'

BIG = 'Большой'
SMALL = 'Обычный'
SUPPORT = 'support'

GUARDS = ('Мизраэль',
          'Ашган',
          'Ашкаэль',
          'Видар')

HEAL_LIST = ('Лечение',
             'Лечение/Исцеление',
             'Лечение/Воскрешение')

ALCHEMIST_LIST = ('Увеличение урона',
                  'Увеличение урона/Исцеление',
                  'Дополнительная атака')

PARALYZE_LIST = ('Паралич',
                 'Окаменение')

VAMPIRE_LIST = ('Высасывание жизни',
                'Избыточное высасывание жизни')

POLYMORPH = 'Полиморф'
INCREASE_DMG = 'Увеличение урона'
ADDITIONAL_ATTACK = 'Дополнительная атака'
HEAL = 'Лечение'

PARALYZE_UNITS = ['Баньши',
                  'Привидение',
                  'Призрак',
                  'Тень',
                  'Инкуб',
                  'Русалка',
                  'Шаманка',
                  'Медуза',
                  'Тёмный эльф-гаст']

# races
EM = 'Empire'
UH = 'Undead Hordes'
LD = 'Legions of the Damned'
MC = 'Mountain Clans'

# active units
ACTIVE_UNITS = os.listdir(f'{UNIT_ATTACK}{FRONT}')

# animation speed
SPEED = 200

# hero exp
HERO_FIGHTER_EXP = 300  # 500
HERO_ARCHER_EXP = 250  # 450
HERO_ROD_EXP = 200  # 300

# coordinates
X_COORD_1 = 40
X_COORD_2 = 160
X_COORD_3 = 880
X_COORD_4 = 1000

SCREEN_RECT = QRect(0, 0, 1600, 900)
PANEL_RECT = QRect(0, 500, 0, 0)

# building descriptions
ALREADY_BUILT = 'Это здание уже построено'
READY_TO_BUILD = 'Это здание можно построить'
NOT_ENOUGH_GOLD = 'Недостаточно золота'
NEED_TO_BUILD_PREV = 'Сначала нужно построить здание, предшествующее этому'
ANOTHER_BRANCH = 'Это здание нельзя построить, поскольку была выбрана ' \
                 'другая ветвь развития'

GUILD_DESC = 'Гильдия нужна, чтобы нанимать воров'
MAGIC_DESC = 'Башня магии необходима для изучения заклинаний'
TEMPLE_DESC = 'Храм может лечить и воскрешать воинов в городах и в столице'
COMMON_DESC = 'Эта постройка позволит юнитам совершенствовать свои навыки. ' \
              'Накопив достаточно опыта,'
SPECIAL_DESC = 'Эта постройка нужна, чтобы нанимать '
SPECIAL_BUILDINGS = ['Разрушенный храм',
                     'Логово оборотней',
                     'Храм Горестей',
                     'Горное логово']

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
