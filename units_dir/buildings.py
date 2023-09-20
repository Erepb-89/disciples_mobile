"""Постройки"""

from collections import namedtuple
from client_dir.settings import LD, EM, UH, MC, GUILD_DESC, MAGIC_DESC, TWMPLE_DESC, COMMON_DESC, SPECIAL_DESC

Building = namedtuple('Building', ['bname', 'unit_name', 'cost', 'prev', 'coords', 'desc'])

guild = Building('Гильдия', '', 150, '', [480, 30, 118, 114], GUILD_DESC)
magic_guild = Building('Башня магии', '', 150, '', [480, 287, 118, 114], MAGIC_DESC)
temple = Building('Храм', '', 300, '', [480, 555, 118, 114], TWMPLE_DESC)

BRANCHES = {
    'fighter': 0,
    'mage': 1,
    'archer': 2,
    'support': 3,
    'special': 4,
    'others': 5
}

ELDER_FORMS = [
    'Священный мститель', 'Защитник веры', 'Ангел', 'Великий инквизитор',
    'Имперский ассасин',
    'Белый волшебник', 'Элементалист', 'Титан',
    'Иерофант', 'Прорицательница',
    'Воин-фантом', 'Тёмный властелин',
    'Тень',
    'Старший вампир', 'Архилич', 'Смерть', 'Сущий',
    'Вирм Ужаса', 'Драколич', 'Оборотень',
    'Адский рыцарь', 'Изверг',
    'Ониксовая гаргулья',
    'Модеус', 'Доппельгангер', 'Инкуб', 'Суккуб',
    'Тиамат', 'Владыка', 'Дьявол Бездны',
    'Король гномов', 'Владыка рун', 'Отшельник', 'Повелитель волков',
    'Хранитель кузни', 'Заклинатель огня',
    'Архидруидесса', 'Алхимик', 'Йети',
    'Старейший', 'Сын Имира'
]

FACTIONS = {
    EM: {
        'others': {
            1: guild,
            2: magic_guild,
            3: temple,
        },
        'fighter': {
            0: Building('', 'Сквайр', 0, '', [319, 32, 118, 114], ''),
            1: Building('Конюшня', 'Рыцарь', 200, '', [319, 32, 118, 114], COMMON_DESC),
            2: Building('Конюшня Империи', 'Имперский рыцарь', 500, 'Конюшня', [320, 259, 118, 114], COMMON_DESC),
            3: Building('Алтарь', 'Паладин', 1500, 'Конюшня Империи', [424, 499, 118, 114], COMMON_DESC),
            4: Building('Священная Статуя', 'Священный мститель', 3000, 'Алтарь', [296, 745, 118, 114], COMMON_DESC),
            5: Building('Часовня', 'Защитник веры', 3000, 'Алтарь', [554, 745, 118, 114], COMMON_DESC),
            6: Building('Фонтан Жизни', 'Ангел', 1500, 'Конюшня Империи', [236, 499, 118, 114], COMMON_DESC),
            7: Building('Подземелье', 'Охотник на ведьм', 200, '', [646, 33, 118, 114], COMMON_DESC),
            8: Building('Камера пыток', 'Инквизитор', 500, 'Подземелье', [646, 260, 118, 114], COMMON_DESC),
            9: Building('Магистрат', 'Великий инквизитор', 1500, 'Камера пыток', [646, 500, 118, 114], COMMON_DESC),
        },
        'mage': {
            0: Building('', 'Ученик', 0, '', [329, 32, 118, 114], COMMON_DESC),
            1: Building('Библиотека', 'Маг', 200, '', [329, 32, 118, 114], COMMON_DESC),
            2: Building('Башня', 'Волшебник', 500, 'Библиотека', [236, 298, 118, 114], COMMON_DESC),
            3: Building('Башня таинств', 'Белый волшебник', 1500, 'Башня', [236, 540, 118, 114], COMMON_DESC),
            4: Building('Круг Стихий', 'Элементалист', 500, 'Библиотека', [435, 298, 118, 114], COMMON_DESC),
        },
        'archer': {
            0: Building('', 'Лучник', 0, '', [440, 32, 118, 114], ''),
            1: Building('Стрельбище', 'Стрелок', 200, '', [440, 32, 118, 114], COMMON_DESC),
            2: Building('Гильдия Империи', 'Имперский ассасин', 500, 'Стрельбище', [441, 259, 118, 114], COMMON_DESC),
        },
        'support': {
            0: Building('', 'Послушник', 0, '', [329, 32, 118, 114], COMMON_DESC),
            1: Building('Монастырь', 'Жрец', 200, '', [329, 32, 118, 114], COMMON_DESC),
            2: Building('Святилище', 'Имперский жрец', 500, 'Монастырь', [330, 259, 118, 114], COMMON_DESC),
            3: Building('Молельня', 'Иерофант', 1500, 'Святилище', [330, 502, 118, 114], COMMON_DESC),
            4: Building('Церковь', 'Клирик', 200, '', [596, 33, 118, 114], COMMON_DESC),
            5: Building('Собор', 'Матриарх', 500, 'Церковь', [596, 260, 118, 114], COMMON_DESC),
            6: Building('Базилика', 'Прорицательница', 1500, 'Собор', [596, 502, 118, 114], COMMON_DESC),
        },
        'special': {
            0: Building('', '', 0, '', [], ''),
            1: Building('Разрушенный храм', 'Титан', 750, 'Библиотека', [], SPECIAL_DESC),
        }
    },
    UH: {
        'others': {
            1: guild,
            2: magic_guild,
            3: temple,
        },
        'fighter': {
            0: Building('', 'Боец', 0, '', [321, 33, 119, 114], ''),
            1: Building('Нечистая земля', 'Зомби', 200, '', [321, 33, 119, 114], COMMON_DESC),
            2: Building('Кладбище', 'Скелет-воин', 500, 'Нечистая земля', [322, 277, 118, 114], COMMON_DESC),
            3: Building('Убежище духов', 'Скелет-чемпион', 1500, 'Кладбище', [322, 511, 118, 114], COMMON_DESC),
            4: Building('Крематорий', 'Воин-фантом', 3000, 'Убежище духов', [322, 747, 118, 115], COMMON_DESC),
            5: Building('Капище', 'Храмовник', 200, '', [590, 33, 118, 114], COMMON_DESC),
            6: Building('Идол Тьмы', 'Тёмный властелин', 500, 'Капище', [590, 278, 118, 114], COMMON_DESC),
        },
        'mage': {
            0: Building('', 'Посвящённый', 0, '', [470, 33, 118, 114], ''),
            1: Building('Храм Тьмы', 'Чернокнижник', 200, '', [470, 33, 118, 114], COMMON_DESC),
            2: Building('Оскверненный храм', 'Некромант', 500, 'Храм Тьмы', [340, 257, 118, 114], COMMON_DESC),
            3: Building('Склеп', 'Вампир', 1500, 'Оскверненный храм', [222, 504, 118, 114], COMMON_DESC),
            4: Building('Цитадель', 'Старший вампир', 3000, 'Склеп', [222, 747, 118, 114], COMMON_DESC),
            5: Building('Башня тьмы', 'Лич', 1500, 'Оскверненный храм', [380, 504, 118, 114], COMMON_DESC),
            6: Building('Башня колдовства', 'Архилич', 3000, 'Башня тьмы', [380, 747, 118, 114], COMMON_DESC),
            7: Building('Часовня проклятых', 'Умертвие', 620, 'Храм Тьмы', [595, 257, 118, 114], COMMON_DESC),
            8: Building('Обитель Мортис', 'Смерть', 1875, 'Часовня проклятых', [537, 504, 118, 114], COMMON_DESC),
            9: Building('Обитель душ', 'Сущий', 2250, 'Часовня проклятых', [697, 504, 118, 114], COMMON_DESC),
        },
        'archer': {
            0: Building('', 'Привидение', 0, '', [480, 30, 118, 114], ''),
            1: Building('Гробница', 'Призрак', 200, '', [480, 30, 118, 114], COMMON_DESC),
            2: Building('Катакомбы', 'Тень', 1000, 'Гробница', [480, 306, 118, 116], COMMON_DESC),
        },
        'support': {
            0: Building('', 'Виверна', 0, '', [373, 33, 118, 114], COMMON_DESC),
            1: Building('Пещера', 'Дрейк Рока', 300, '', [373, 33, 118, 114], COMMON_DESC),
            2: Building('Кладбище', 'Дракон Смерти', 750, 'Пещера', [373, 274, 118, 114], COMMON_DESC),
            3: Building('Проклятое кладбище', 'Вирм Ужаса', 2250, 'Кладбище', [250, 534, 118, 114], COMMON_DESC),
            4: Building('Драконье кладбище', 'Драколич', 2250, 'Кладбище', [497, 534, 118, 114], COMMON_DESC),
        },
        'special': {
            0: Building('', '', 0, '', [], ''),
            1: Building('Логово оборотней', 'Оборотень', 750, 'Пещера', [624, 35, 0, 0], SPECIAL_DESC),
        }
    },
    LD: {
        'others': {
            1: guild,
            2: magic_guild,
            3: temple,
        },
        'fighter': {
            0: Building('', 'Одержимый', 0, '', [339, 33, 118, 114], ''),
            1: Building('Портал Скверны', 'Берсерк', 200, '', [339, 33, 118, 114], COMMON_DESC),
            2: Building('Башня Духов', 'Антипаладин', 500, 'Портал Скверны', [339, 285, 118, 114], COMMON_DESC),
            3: Building('Идол Бетрезена', 'Адский рыцарь', 1500, 'Башня Духов', [339, 553, 118, 114], COMMON_DESC),
        },
        'mage': {
            0: Building('', 'Сектант', 0, '', [338, 32, 118, 114], ''),
            1: Building('Аббатство Тьмы', 'Чародей', 200, '', [338, 32, 118, 114], COMMON_DESC),
            2: Building('Темное Святилище', 'Демонолог', 500, 'Аббатство Тьмы', [441, 258, 118, 114], COMMON_DESC),
            3: Building('Алтарь', 'Пандемонеус', 1500, 'Темное Святилище', [441, 528, 118, 114], COMMON_DESC),
            4: Building('Священный алтарь', 'Модеус', 3000, 'Алтарь', [441, 747, 118, 114], COMMON_DESC),
            5: Building('Замок духов', 'Доппельгангер', 500, 'Аббатство Тьмы', [238, 258, 118, 114], COMMON_DESC),
            6: Building('Чертог Обмана', 'Инкуб', 1500, 'Темное Святилище', [238, 528, 118, 114], COMMON_DESC),
            7: Building('Дворец Пороков', 'Ведьма', 200, '', [660, 33, 118, 114], COMMON_DESC),
            8: Building('Дворец Греха', 'Колдунья', 500, 'Дворец Пороков', [660, 260, 118, 114], COMMON_DESC),
            9: Building('Высший храм', 'Суккуб', 1500, 'Дворец Греха', [660, 528, 118, 114], COMMON_DESC),
        },
        'archer': {
            0: Building('', 'Гаргулья', 0, '', [478, 33, 118, 114], ''),
            1: Building('Шпиль', 'Мраморная гаргулья', 300, '', [478, 33, 118, 114], COMMON_DESC),
            2: Building('Черный шпиль', 'Ониксовая гаргулья', 750, 'Шпиль', [478, 309, 118, 114], COMMON_DESC),
        },
        'support': {
            0: Building('', 'Чёрт', 0, '', [439, 33, 118, 114], ''),
            1: Building('Врата Скверны', 'Демон', 300, '', [439, 33, 118, 114], COMMON_DESC),
            2: Building('Часовня Мучений', 'Молох', 750, 'Врата Скверны', [439, 260, 118, 114], COMMON_DESC),
            3: Building('Алтарь Скверны', 'Зверь', 2550, 'Часовня Мучений', [250, 477, 118, 114], COMMON_DESC),
            4: Building('Темница', 'Тиамат', 4500, 'Алтарь Скверны', [250, 695, 118, 114], COMMON_DESC),
            5: Building('Адские Врата', 'Повелитель демонов', 2250, 'Часовня Мучений', [580, 477, 118, 114], COMMON_DESC),
            6: Building('Чертоги Скверны', 'Владыка', 4500, 'Адские Врата', [476, 695, 118, 114], COMMON_DESC),
            7: Building('Мавзолей', 'Дьявол Бездны', 4500, 'Адские Врата', [668, 695, 118, 114], COMMON_DESC),
        },
        'special': {
            0: Building('', '', 0, '', [], ''),
            1: Building('Храм Горестей', 'Изверг', 750, 'Портал Скверны', [], SPECIAL_DESC),
        }
    },
    MC: {
        'others': {
            1: guild,
            2: magic_guild,
            3: temple,
        },
        'fighter': {
            0: Building('', 'Гном', 0, '', [455, 29, 118, 114], ''),
            1: Building('Пивоварня', 'Воин', 200, '', [455, 29, 118, 114], COMMON_DESC),
            2: Building('Арсенал', 'Ветеран', 500, 'Пивоварня', [282, 258, 118, 114], COMMON_DESC),
            3: Building('Храм Предков', 'Почтенный воин', 1500, 'Арсенал', [282, 507, 118, 114], COMMON_DESC),
            4: Building('Дворец', 'Король гномов', 4500, 'Храм Предков', [220, 744, 118, 114], COMMON_DESC),
            5: Building('Рунный Зал', 'Владыка рун', 3000, 'Храм Предков', [424, 744, 118, 114], COMMON_DESC),
            6: Building('Застава', 'Горец', 500, 'Пивоварня', [607, 258, 118, 114], COMMON_DESC),
            7: Building('Берлога', 'Отшельник', 1500, 'Застава', [499, 507, 118, 114], COMMON_DESC),
            8: Building('Зал Фенрира', 'Повелитель волков', 1500, 'Застава', [693, 507, 118, 114], COMMON_DESC),
        },
        'mage': {
            0: Building('', 'Желторотик', 0, '', [341, 31, 118, 114], ''),
            1: Building('Хижина', 'Новичок', 200, '', [341, 31, 118, 114], COMMON_DESC),
            2: Building('Сад Мудрости', 'Друидесса', 500, 'Хижина', [235, 307, 118, 114], COMMON_DESC),
            3: Building('Древо Старейшин', 'Архидруидесса', 1500, 'Сад Мудрости', [234, 568, 118, 114], COMMON_DESC),
            4: Building('Башня алхимии', 'Алхимик', 500, 'Хижина', [443, 307, 118, 114], COMMON_DESC),
        },
        'archer': {
            0: Building('', 'Метатель топоров', 0, '', [464, 29, 118, 114], ''),
            1: Building('Стрельбище', 'Арбалетчик', 200, '', [464, 29, 118, 114], COMMON_DESC),
            2: Building('Горн Предков', 'Хранитель кузни', 500, 'Стрельбище', [288, 256, 118, 115], COMMON_DESC),
            3: Building('Гильдия инженеров', 'Заклинатель огня', 700, 'Стрельбище', [629, 256, 118, 115], COMMON_DESC),
        },
        'support': {
            0: Building('', 'Холмовой гигант', 0, '', [464, 32, 118, 114], ''),
            1: Building('Горный пик', 'Горный гигант', 300, '', [464, 32, 118, 114], COMMON_DESC),
            2: Building('Небесный замок', 'Штормовой гигант', 750, 'Горный пик', [287, 258, 118, 114], COMMON_DESC),
            3: Building('Мост Бифрост', 'Старейший', 2250, 'Небесный замок', [282, 505, 118, 114], COMMON_DESC),
            4: Building('Снежные горы', 'Ледяной гигант', 750, 'Горный пик', [630, 258, 118, 114], COMMON_DESC),
            5: Building('Ледяные пещеры', 'Сын Имира', 2250, 'Снежные горы', [631, 505, 120, 114], COMMON_DESC),
        },
        'special': {
            0: Building('', '', 0, '', [], ''),
            1: Building('Горное логово', 'Йети', 750, 'Хижина', [], SPECIAL_DESC),
        }
    }
}
