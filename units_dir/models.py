class AllUnits:
    """Класс - отображение таблицы всех юнитов."""

    def __init__(self, unit):
        self.id = None
        self.name = unit.name
        self.level = unit.level
        self.size = unit.size
        self.price = unit.price
        self.exp = unit.exp
        self.curr_exp = unit.curr_exp
        self.exp_per_kill = unit.exp_per_kill
        self.health = unit.health
        self.curr_health = unit.curr_health
        self.armor = unit.armor
        self.immune = unit.immune
        self.ward = unit.ward
        self.attack_type = unit.attack_type
        self.attack_chance = unit.attack_chance
        self.attack_dmg = unit.attack_dmg
        self.dot_dmg = unit.dot_dmg
        self.attack_source = unit.attack_source
        self.attack_ini = unit.attack_ini
        self.attack_radius = unit.attack_radius
        self.attack_purpose = unit.attack_purpose
        self.prev_level = unit.prev_level
        self.desc = unit.desc
        self.photo = unit.photo
        self.gif = unit.gif
        self.slot = unit.slot
        self.subrace = unit.subrace
        self.branch = unit.branch
        self.attack_twice = unit.attack_twice
        self.regen = unit.regen
        self.dyn_upd_level = unit.dyn_upd_level
        self.upgrade_b = unit.upgrade_b
        self.leadership = unit.leadership
        self.leader_cat = unit.leader_cat
        self.nat_armor = unit.nat_armor
        self.might = unit.might
        self.weapon_master = unit.weapon_master
        self.endurance = unit.endurance
        self.first_strike = unit.first_strike
        self.accuracy = unit.accuracy
        self.water_resist = unit.water_resist
        self.air_resist = unit.air_resist
        self.fire_resist = unit.fire_resist
        self.earth_resist = unit.earth_resist
        self.dotted = unit.dotted
        self.locked = unit.locked


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

    session_id = None

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
                 unit6: str,
                 level_unit1: int,
                 level_unit2: int,
                 level_unit3: int,
                 level_unit4: int,
                 level_unit5: int,
                 level_unit6: int):
        self.id = None
        self.name = name
        self.unit1 = unit1
        self.unit2 = unit2
        self.unit3 = unit3
        self.unit4 = unit4
        self.unit5 = unit5
        self.unit6 = unit6
        self.level_unit1 = level_unit1
        self.level_unit2 = level_unit2
        self.level_unit3 = level_unit3
        self.level_unit4 = level_unit4
        self.level_unit5 = level_unit5
        self.level_unit6 = level_unit6
