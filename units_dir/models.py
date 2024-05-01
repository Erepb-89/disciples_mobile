class AllUnits:
    """Класс - отображение таблицы всех юнитов."""

    def __init__(self,
                 id: int,
                 name: str,
                 level: int,
                 size: str,
                 price: int,
                 exp: int,
                 curr_exp: int,
                 exp_per_kill: int,
                 health: int,
                 curr_health: int,
                 armor: int,
                 immune: str,
                 ward: str,
                 attack_type: str,
                 attack_chance: str,
                 attack_dmg: int,
                 dot_dmg: int,
                 attack_source: str,
                 attack_ini: int,
                 attack_radius: str,
                 attack_purpose: int,
                 prev_level: str,
                 desc: str,
                 photo: str,
                 gif: str,
                 slot: int,
                 subrace: str,
                 branch: str,
                 attack_twice: int,
                 regen: int,
                 dyn_upd_level: int,
                 upgrade_b: str,
                 leadership: int,
                 leader_cat: str,
                 nat_armor: int,
                 might: int,
                 weapon_master: int,
                 endurance: int,
                 first_strike: int,
                 accuracy: int,
                 water_resist: int,
                 air_resist: int,
                 fire_resist: int,
                 earth_resist: int,
                 dotted: int
                 ):
        self.id = None
        self.name = name
        self.level = level
        self.size = size
        self.price = price
        self.exp = exp
        self.curr_exp = curr_exp
        self.exp_per_kill = exp_per_kill
        self.health = health
        self.curr_health = curr_health
        self.armor = armor
        self.immune = immune
        self.ward = ward
        self.attack_type = attack_type
        self.attack_chance = attack_chance
        self.attack_dmg = attack_dmg
        self.dot_dmg = dot_dmg
        self.attack_source = attack_source
        self.attack_ini = attack_ini
        self.attack_radius = attack_radius
        self.attack_purpose = attack_purpose
        self.prev_level = prev_level
        self.desc = desc
        self.photo = photo
        self.gif = gif
        self.slot = slot
        self.subrace = subrace
        self.branch = branch
        self.attack_twice = attack_twice
        self.regen = regen
        self.dyn_upd_level = dyn_upd_level
        self.upgrade_b = upgrade_b
        self.leadership = leadership
        self.leader_cat = leader_cat
        self.nat_armor = nat_armor
        self.might = might
        self.weapon_master = weapon_master
        self.endurance = endurance
        self.first_strike = first_strike
        self.accuracy = accuracy
        self.water_resist = water_resist
        self.air_resist = air_resist
        self.fire_resist = fire_resist
        self.earth_resist = earth_resist
        self.dotted = dotted


class PlayerUnits(AllUnits):
    """Класс - отображение таблицы юнитов игрока."""

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'unit: {self.name!r},'
                f' slot: {self.slot!r})')

    def __str__(self):
        return f'Юнит игрока 1: {self.name}'


class Player2Units(AllUnits):
    """Класс - отображение таблицы юнитов игрока 2."""

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'unit: {self.name!r},'
                f' slot: {self.slot!r})')

    def __str__(self):
        return f'Юнит игрока 2: {self.name}'


class CurrentDungeon(AllUnits):
    """Класс - подземелье."""

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'unit: {self.name!r},'
                f' slot: {self.slot!r})')

    def __str__(self):
        return f'Юнит подземелья: {self.name}'


class EmpireUnits(AllUnits):
    """
    Класс - отображение таблицы юнитов игрока
    в кампании при игре за Империю.
    """

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'unit: {self.name!r},'
                f' slot: {self.slot!r})')

    def __str__(self):
        return f'Юнит Империи: {self.name}'


class ReserveEmpireUnits(AllUnits):
    """
    Класс - отображение таблицы резервных юнитов игрока
    в кампании в окне столицы при игре за Империю.
    """

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'unit: {self.name!r},'
                f' slot: {self.slot!r})')

    def __str__(self):
        return f'Юнит Империи: {self.name}'


class HordesUnits(AllUnits):
    """
    Класс - отображение таблицы юнитов игрока
    в кампании при игре за Орды нежити.
    """

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'unit: {self.name!r},'
                f' slot: {self.slot!r})')

    def __str__(self):
        return f'Юнит Орд нежити: {self.name}'


class ReserveHordesUnits(AllUnits):
    """
    Класс - отображение таблицы резервных юнитов игрока
    в кампании в окне столицы при игре за Орды нежити.
    """

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'unit: {self.name!r},'
                f' slot: {self.slot!r})')

    def __str__(self):
        return f'Юнит Орд нежити: {self.name}'


class LegionsUnits(AllUnits):
    """
    Класс - отображение таблицы юнитов игрока
    в кампании при игре за Легионы проклятых.
    """

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'unit: {self.name!r},'
                f' slot: {self.slot!r})')

    def __str__(self):
        return f'Юнит Легионов проклятых: {self.name}'


class ReserveLegionsUnits(AllUnits):
    """
    Класс - отображение таблицы резервных юнитов игрока
    в кампании в окне столицы при игре за Легионы проклятых.
    """

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'unit: {self.name!r},'
                f' slot: {self.slot!r})')

    def __str__(self):
        return f'Юнит Легионов проклятых: {self.name}'


class ClansUnits(AllUnits):
    """
    Класс - отображение таблицы юнитов игрока
    в кампании при игре за Горные кланы.
    """

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'unit: {self.name!r},'
                f' slot: {self.slot!r})')

    def __str__(self):
        return f'Юнит Горных кланов: {self.name}'


class ReserveClansUnits(AllUnits):
    """
    Класс - отображение таблицы резервных юнитов игрока
    в кампании в окне столицы при игре за Горные кланы.
    """

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'unit: {self.name!r},'
                f' slot: {self.slot!r})')

    def __str__(self):
        return f'Юнит Горных кланов: {self.name}'


class Players:
    """Класс - игроки."""

    def __init__(self, name: str, email: str):
        self.id = None
        self.name = name
        self.email = email


class PlayerBuildings:
    """Класс - постройки игрока."""

    def __init__(
            self,
            name: str,
            faction: str,
            gold: int,
            fighter: str,
            mage: str,
            archer: str,
            support: str,
            special: str,
            thieves_guild: str,
            temple: str,
            magic_guild: str):
        self.id = None
        self.name = name
        self.faction = faction
        self.gold = gold
        self.fighter = fighter
        self.mage = mage
        self.archer = archer
        self.support = support
        self.special = special
        self.thieves_guild = thieves_guild
        self.temple = temple
        self.magic_guild = magic_guild


class GameSessions:
    """Класс - игровые сессии."""

    def __init__(self,
                 player_id: int,
                 faction: str,
                 campaign_level: int,
                 campaign_mission: int,
                 prev_mission: int,
                 day: int,
                 built: int,
                 difficulty: int
                 ):
        self.session_id = None
        self.player_id = player_id
        self.faction = faction
        self.campaign_level = campaign_level
        self.campaign_mission = campaign_mission
        self.prev_mission = prev_mission
        self.day = day
        self.built = built
        self.difficulty = difficulty


class Dungeons:
    """Класс - подземелья."""

    def __init__(self, name: str,
                 unit1: str,
                 unit2: str,
                 unit3: str,
                 unit4: str,
                 unit5: str,
                 unit6: str):
        self.id = None
        self.name = name
        self.unit1 = unit1
        self.unit2 = unit2
        self.unit3 = unit3
        self.unit4 = unit4
        self.unit5 = unit5
        self.unit6 = unit6
