"""База. Классы юнитов"""

from collections import namedtuple
from typing import Callable, List

from sqlalchemy import create_engine, Table, update, Column, Integer, \
    String, MetaData
from sqlalchemy.orm import mapper, sessionmaker

from client_dir.settings import BIG, EM, UH, LD, MC, GUARDS
from units_dir.buildings import FACTIONS


class ServerStorage:
    """
    Класс - оболочка для работы с базой данных сервера.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется классический подход.
    """

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

    def __init__(self, path):
        # Создаём движок базы данных
        self.database_engine = create_engine(
            f'sqlite:///{path}',
            echo=False,
            pool_recycle=7200,
            connect_args={
                'check_same_thread': False})

        # Создаём объект MetaData
        self.metadata = MetaData()

        units_table = self.create_units_table('units')
        player_units_table = self.create_units_table('player_units')
        player2_units_table = self.create_units_table('player2_units')
        current_dungeon_table = self.create_units_table('current_dungeon')
        empire_units_table = self.create_units_table('empire_units')
        hordes_units_table = self.create_units_table('hordes_units')
        legions_units_table = self.create_units_table('legions_units')
        clans_units_table = self.create_units_table('clans_units')
        reserve_empire_table = self.create_units_table('reserve_empire_units')
        reserve_hordes_table = self.create_units_table('reserve_hordes_units')
        reserve_legions_table = self.create_units_table('reserve_legions_units')
        reserve_clans_table = self.create_units_table('reserve_clans_units')

        # Создаём таблицу игроков
        players_table = Table('players', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('name', String),
                              Column('email', String)
                              )

        # Создаём таблицу построек игрока
        player_buildings_table = Table('player_buildings', self.metadata,
                                       Column('id', Integer, primary_key=True),
                                       Column('name', String),
                                       Column('faction', String),
                                       Column('gold', Integer),
                                       Column('fighter', String),
                                       Column('mage', String),
                                       Column('archer', String),
                                       Column('support', String),
                                       Column('special', String),
                                       Column('thieves_guild', String),
                                       Column('temple', String),
                                       Column('magic_guild', String)
                                       )

        # Создаём таблицу игровых сессий
        game_sessions_table = Table(
            'game_sessions', self.metadata,
            Column('session_id', Integer, primary_key=True),
            Column('player_id', Integer),
            Column('faction', String),
            Column('campaign_level', Integer),
            Column('campaign_mission', Integer),
            Column('prev_mission', Integer),
            Column('day', Integer),
            Column('built', Integer),
            Column('difficulty', Integer)
        )

        # Создаём таблицу всех подземелий
        dungeons_table = Table('dungeons', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('name', String, unique=True),
                               Column('unit1', String),
                               Column('unit2', String),
                               Column('unit3', String),
                               Column('unit4', String),
                               Column('unit5', String),
                               Column('unit6', String)
                               )

        # Создаём таблицы
        self.metadata.create_all(self.database_engine)

        # Создаём отображения
        mapper(self.AllUnits, units_table)
        mapper(self.PlayerUnits, player_units_table)
        mapper(self.Player2Units, player2_units_table)
        mapper(self.Players, players_table)
        mapper(self.PlayerBuildings, player_buildings_table)
        mapper(self.GameSessions, game_sessions_table)
        mapper(self.Dungeons, dungeons_table)
        mapper(self.CurrentDungeon, current_dungeon_table)
        mapper(self.EmpireUnits, empire_units_table)
        mapper(self.HordesUnits, hordes_units_table)
        mapper(self.LegionsUnits, legions_units_table)
        mapper(self.ClansUnits, clans_units_table)
        mapper(self.ReserveEmpireUnits, reserve_empire_table)
        mapper(self.ReserveHordesUnits, reserve_hordes_table)
        mapper(self.ReserveLegionsUnits, reserve_legions_table)
        mapper(self.ReserveClansUnits, reserve_clans_table)

        # Создаём сессию
        session = sessionmaker(bind=self.database_engine)
        self.session = session()

        self.current_player = self.get_player('Erepb-89')

        self.campaigns_dict = {
            EM: self.EmpireUnits,
            UH: self.HordesUnits,
            LD: self.LegionsUnits,
            MC: self.ClansUnits,
        }

        self.res_campaigns_dict = {
            EM: self.ReserveEmpireUnits,
            UH: self.ReserveHordesUnits,
            LD: self.ReserveLegionsUnits,
            MC: self.ReserveClansUnits,
        }

        self.guards_dict = {
            EM: "Мизраэль",
            UH: "Ашган",
            LD: "Ашкаэль",
            MC: "Видар",
        }

    def create_units_table(self, table_name):
        return Table(table_name, self.metadata,
                     Column('id', Integer, primary_key=True),
                     Column('name', String),
                     Column('level', Integer),
                     Column('size', String),
                     Column('price', Integer),
                     Column('exp', Integer),
                     Column('curr_exp', Integer),
                     Column('exp_per_kill', Integer),
                     Column('health', Integer),
                     Column('curr_health', Integer),
                     Column('armor', Integer),
                     Column('immune', String),
                     Column('ward', String),
                     Column('attack_type', String),
                     Column('attack_chance', String),
                     Column('attack_dmg', Integer),
                     Column('dot_dmg', Integer),
                     Column('attack_source', String),
                     Column('attack_ini', Integer),
                     Column('attack_radius', String),
                     Column('attack_purpose', Integer),
                     Column('prev_level', String),
                     Column('desc', String),
                     Column('photo', String),
                     Column('gif', String),
                     Column('slot', Integer),
                     Column('subrace', String),
                     Column('branch', String),
                     Column('attack_twice', Integer),
                     Column('regen', Integer),
                     Column('dyn_upd_level', Integer),
                     Column('upgrade_b', String),
                     Column('leadership', Integer),
                     Column('leader_cat', String),
                     Column('nat_armor', Integer),
                     Column('might', Integer),
                     Column('weapon_master', Integer),
                     Column('endurance', Integer),
                     Column('first_strike', Integer),
                     Column('accuracy', Integer),
                     Column('water_resist', Integer),
                     Column('air_resist', Integer),
                     Column('fire_resist', Integer),
                     Column('earth_resist', Integer),
                     Column('dotted', Integer),
                     )

    def increase_campaign_level(self):
        """Увеличивает уровень кампании"""
        self.campaign_level += 1
        self.campaign_day += 1
        self.already_built = 0

        self.update_session(
            self.game_session_id,
            self.campaign_level,
            0,
            0,
            self.campaign_day,
            self.already_built)

    def increase_campaign_mission(self,
                                  mission_number: int,
                                  curr_mission: int):
        """Переходит на следующую миссию кампании"""
        self.campaign_day += 1
        self.already_built = 0

        self.update_session(
            self.game_session_id,
            self.campaign_level,
            mission_number,
            curr_mission,
            self.campaign_day,
            self.already_built)

    def update_game_session(self):
        """Обновить игровую сессию"""
        curr_game_session = self.current_game_session(
            self.current_player.id)
        if curr_game_session is not None:
            self.current_faction = curr_game_session.faction
            self.campaign_level = curr_game_session.campaign_level
            self.campaign_mission = curr_game_session.campaign_mission
            self.prev_mission = curr_game_session.prev_mission
            self.campaign_day = curr_game_session.day
            self.already_built = curr_game_session.built
            self.game_session_id = curr_game_session.session_id
            self.difficulty = curr_game_session.difficulty
        else:
            self.current_faction = 'Empire'
            self.campaign_level = 1
            self.campaign_mission = 0
            self.prev_mission = 0
            self.campaign_day = 1
            self.already_built = 0
            self.difficulty = 2

    def add_dungeon_unit(
            self,
            id,
            name,
            level,
            size,
            price,
            exp,
            curr_exp,
            exp_per_kill,
            health,
            curr_health,
            armor,
            immune,
            ward,
            attack_type,
            attack_chance,
            attack_dmg,
            dot_dmg,
            attack_source,
            attack_ini,
            attack_radius,
            attack_purpose,
            prev_level,
            desc,
            photo,
            gif,
            slot,
            subrace,
            branch,
            attack_twice,
            regen,
            dyn_upd_level,
            upgrade_b,
            leadership,
            leader_cat,
            nat_armor,
            might,
            weapon_master,
            endurance,
            first_strike,
            accuracy,
            water_resist,
            air_resist,
            fire_resist,
            earth_resist,
            dotted):
        """
        Метод регистрации юнита.
        Создаёт запись в таблице CurrentDungeon.
        """
        unit_row = self.CurrentDungeon(
            id,
            name,
            level,
            size,
            price,
            exp,
            curr_exp,
            exp_per_kill,
            health,
            curr_health,
            armor,
            immune,
            ward,
            attack_type,
            attack_chance,
            attack_dmg,
            dot_dmg,
            attack_source,
            attack_ini,
            attack_radius,
            attack_purpose,
            prev_level,
            desc,
            photo,
            gif,
            slot,
            subrace,
            branch,
            attack_twice,
            regen,
            dyn_upd_level,
            upgrade_b,
            leadership,
            leader_cat,
            nat_armor,
            might,
            weapon_master,
            endurance,
            first_strike,
            accuracy,
            water_resist,
            air_resist,
            fire_resist,
            earth_resist,
            dotted
        )
        self.session.add(unit_row)
        self.session.commit()

    def get_unit_by_name(self, name: str) -> namedtuple:
        """Метод получающий юнита из таблицы AllUnits по имени."""
        query = self.session.query(
            self.AllUnits.id,
            self.AllUnits.name,
            self.AllUnits.level,
            self.AllUnits.size,
            self.AllUnits.price,
            self.AllUnits.exp,
            self.AllUnits.curr_exp,
            self.AllUnits.exp_per_kill,
            self.AllUnits.health,
            self.AllUnits.curr_health,
            self.AllUnits.armor,
            self.AllUnits.immune,
            self.AllUnits.ward,
            self.AllUnits.attack_type,
            self.AllUnits.attack_chance,
            self.AllUnits.attack_dmg,
            self.AllUnits.dot_dmg,
            self.AllUnits.attack_source,
            self.AllUnits.attack_ini,
            self.AllUnits.attack_radius,
            self.AllUnits.attack_purpose,
            self.AllUnits.prev_level,
            self.AllUnits.desc,
            self.AllUnits.photo,
            self.AllUnits.gif,
            self.AllUnits.slot,
            self.AllUnits.subrace,
            self.AllUnits.branch,
            self.AllUnits.attack_twice,
            self.AllUnits.regen,
            self.AllUnits.dyn_upd_level,
            self.AllUnits.upgrade_b,
            self.AllUnits.leadership,
            self.AllUnits.leader_cat,
            self.AllUnits.nat_armor,
            self.AllUnits.might,
            self.AllUnits.weapon_master,
            self.AllUnits.endurance,
            self.AllUnits.first_strike,
            self.AllUnits.accuracy,
            self.AllUnits.water_resist,
            self.AllUnits.air_resist,
            self.AllUnits.fire_resist,
            self.AllUnits.earth_resist,
            self.AllUnits.dotted
        ).filter_by(name=name)
        # Возвращаем кортеж
        return query.first()

    def get_units_by_branch_and_level(self,
                                      branch: str,
                                      level: int) -> namedtuple:
        """Метод получающий юнита из таблицы AllUnits по ветви."""
        query = self.session.query(
            self.AllUnits.id,
            self.AllUnits.name,
            self.AllUnits.level,
            self.AllUnits.size,
            self.AllUnits.price,
            self.AllUnits.exp,
            self.AllUnits.curr_exp,
            self.AllUnits.exp_per_kill,
            self.AllUnits.health,
            self.AllUnits.curr_health,
            self.AllUnits.armor,
            self.AllUnits.immune,
            self.AllUnits.ward,
            self.AllUnits.attack_type,
            self.AllUnits.attack_chance,
            self.AllUnits.attack_dmg,
            self.AllUnits.dot_dmg,
            self.AllUnits.attack_source,
            self.AllUnits.attack_ini,
            self.AllUnits.attack_radius,
            self.AllUnits.attack_purpose,
            self.AllUnits.prev_level,
            self.AllUnits.desc,
            self.AllUnits.photo,
            self.AllUnits.gif,
            self.AllUnits.slot,
            self.AllUnits.subrace,
            self.AllUnits.branch,
            self.AllUnits.attack_twice,
            self.AllUnits.regen,
            self.AllUnits.dyn_upd_level,
            self.AllUnits.upgrade_b,
            self.AllUnits.leadership,
            self.AllUnits.leader_cat,
            self.AllUnits.nat_armor,
            self.AllUnits.might,
            self.AllUnits.weapon_master,
            self.AllUnits.endurance,
            self.AllUnits.first_strike,
            self.AllUnits.accuracy,
            self.AllUnits.water_resist,
            self.AllUnits.air_resist,
            self.AllUnits.fire_resist,
            self.AllUnits.earth_resist,
            self.AllUnits.dotted
        ).filter_by(branch=branch, level=level)
        # return query.order_by(self.AllUnits.level.desc()).first()
        # Возвращаем кортеж
        return query.all()

    def unit_by_name_set_params(self,
                                unit: any,
                                name: str,
                                db_table: any) -> namedtuple:
        """
        Метод получающий юнита из таблицы AllUnits по имени
        с новыми заданными параметрами и слотом.
        """
        query = self.session.query(
            db_table.id,
            db_table.name,
            db_table.level,
            db_table.size,
            db_table.price,
            db_table.exp,
            db_table.curr_exp,
            db_table.exp_per_kill,
            unit.health,
            unit.curr_health,
            db_table.armor,
            db_table.immune,  # нужно брать у исходного юнита
            db_table.ward,  # нужно брать у исходного юнита
            db_table.attack_type,
            db_table.attack_chance,
            db_table.attack_dmg,
            db_table.dot_dmg,
            db_table.attack_source,
            db_table.attack_ini,
            db_table.attack_radius,
            db_table.attack_purpose,
            db_table.prev_level,
            db_table.desc,
            db_table.photo,
            db_table.gif,
            unit.slot,
            db_table.subrace,
            db_table.branch,
            db_table.attack_twice,
            db_table.regen,
            db_table.dyn_upd_level,
            db_table.upgrade_b,
            db_table.leadership,
            db_table.leader_cat,
            db_table.nat_armor,
            db_table.might,
            db_table.weapon_master,
            db_table.endurance,
            db_table.first_strike,
            db_table.accuracy,
            db_table.water_resist,
            db_table.air_resist,
            db_table.fire_resist,
            db_table.earth_resist,
            db_table.dotted
        ).filter_by(name=name)
        # Возвращаем кортеж
        return query.first()

    def session_by_faction(self, player_id: int, faction: str) -> any:
        """Метод получающий игровую сессию по игроку и фракции."""
        query = self.session.query(
            self.GameSessions.session_id,
            self.GameSessions.player_id,
            self.GameSessions.faction,
            self.GameSessions.campaign_level,
            self.GameSessions.campaign_mission,
            self.GameSessions.prev_mission,
            self.GameSessions.day,
            self.GameSessions.built,
            self.GameSessions.difficulty
        ).filter_by(player_id=player_id, faction=faction)
        # Возвращаем кортеж
        return query.order_by(self.GameSessions.session_id.desc()).first()

    def current_game_session(self, player_id: int) -> any:
        """Метод получающий текущую игровую сессию
        (последнюю запись из таблицы GameSessions)."""
        query = self.session.query(
            self.GameSessions.session_id,
            self.GameSessions.player_id,
            self.GameSessions.faction,
            self.GameSessions.campaign_level,
            self.GameSessions.campaign_mission,
            self.GameSessions.prev_mission,
            self.GameSessions.day,
            self.GameSessions.built,
            self.GameSessions.difficulty
        ).filter_by(player_id=player_id)
        # Возвращаем кортеж
        return query.order_by(self.GameSessions.session_id.desc()).first()

    def get_unit_by_id(self, _id: int, db_table: AllUnits) -> namedtuple:
        """Метод получающий юнита из общей таблица юнитов по id."""
        query = self.session.query(
            db_table.id,
            db_table.name,
            db_table.level,
            db_table.size,
            db_table.price,
            db_table.exp,
            db_table.curr_exp,
            db_table.exp_per_kill,
            db_table.health,
            db_table.curr_health,
            db_table.armor,
            db_table.immune,
            db_table.ward,
            db_table.attack_type,
            db_table.attack_chance,
            db_table.attack_dmg,
            db_table.dot_dmg,
            db_table.attack_source,
            db_table.attack_ini,
            db_table.attack_radius,
            db_table.attack_purpose,
            db_table.prev_level,
            db_table.desc,
            db_table.photo,
            db_table.gif,
            db_table.slot,
            db_table.subrace,
            db_table.branch,
            db_table.attack_twice,
            db_table.regen,
            db_table.dyn_upd_level,
            db_table.upgrade_b,
            db_table.leadership,
            db_table.leader_cat,
            db_table.nat_armor,
            db_table.might,
            db_table.weapon_master,
            db_table.endurance,
            db_table.first_strike,
            db_table.accuracy,
            db_table.water_resist,
            db_table.air_resist,
            db_table.fire_resist,
            db_table.earth_resist,
            db_table.dotted
        ).filter_by(id=_id)
        # Возвращаем кортеж
        return query.first()

    def get_unit_by_slot(self, slot: int, db_table: AllUnits) -> namedtuple:
        """Метод получающий юнита из переданной таблицы по слоту."""
        query = self.session.query(
            db_table.id,
            db_table.name,
            db_table.level,
            db_table.size,
            db_table.price,
            db_table.exp,
            db_table.curr_exp,
            db_table.exp_per_kill,
            db_table.health,
            db_table.curr_health,
            db_table.armor,
            db_table.immune,
            db_table.ward,
            db_table.attack_type,
            db_table.attack_chance,
            db_table.attack_dmg,
            db_table.dot_dmg,
            db_table.attack_source,
            db_table.attack_ini,
            db_table.attack_radius,
            db_table.attack_purpose,
            db_table.prev_level,
            db_table.desc,
            db_table.photo,
            db_table.gif,
            db_table.slot,
            db_table.subrace,
            db_table.branch,
            db_table.attack_twice,
            db_table.regen,
            db_table.dyn_upd_level,
            db_table.upgrade_b,
            db_table.leadership,
            db_table.leader_cat,
            db_table.nat_armor,
            db_table.might,
            db_table.weapon_master,
            db_table.endurance,
            db_table.first_strike,
            db_table.accuracy,
            db_table.water_resist,
            db_table.air_resist,
            db_table.fire_resist,
            db_table.earth_resist,
            db_table.dotted
        ).filter_by(slot=slot)
        # Возвращаем кортеж
        return query.first()

    def get_units_by_level(self, level: int) -> namedtuple:
        """Метод получения всех юнитов заданного уровня."""
        query = self.session.query(
            self.AllUnits.id,
            self.AllUnits.name,
            self.AllUnits.level,
            self.AllUnits.size,
            self.AllUnits.price,
            self.AllUnits.exp,
            self.AllUnits.curr_exp,
            self.AllUnits.exp_per_kill,
            self.AllUnits.health,
            self.AllUnits.curr_health,
            self.AllUnits.armor,
            self.AllUnits.immune,
            self.AllUnits.ward,
            self.AllUnits.attack_type,
            self.AllUnits.attack_chance,
            self.AllUnits.attack_dmg,
            self.AllUnits.dot_dmg,
            self.AllUnits.attack_source,
            self.AllUnits.attack_ini,
            self.AllUnits.attack_radius,
            self.AllUnits.attack_purpose,
            self.AllUnits.prev_level,
            self.AllUnits.desc,
            self.AllUnits.photo,
            self.AllUnits.gif,
            self.AllUnits.slot,
            self.AllUnits.subrace,
            self.AllUnits.branch,
            self.AllUnits.attack_twice,
            self.AllUnits.regen,
            self.AllUnits.dyn_upd_level,
            self.AllUnits.upgrade_b,
            self.AllUnits.leadership,
            self.AllUnits.leader_cat,
            self.AllUnits.nat_armor,
            self.AllUnits.might,
            self.AllUnits.weapon_master,
            self.AllUnits.endurance,
            self.AllUnits.first_strike,
            self.AllUnits.accuracy,
            self.AllUnits.water_resist,
            self.AllUnits.air_resist,
            self.AllUnits.fire_resist,
            self.AllUnits.earth_resist,
            self.AllUnits.dotted
        ).filter(self.AllUnits.level == level,
                 self.AllUnits.branch != 'hero')
        # Возвращаем список кортежей
        return query.all()

    def show_campaign_units(self) -> List[namedtuple]:
        """Метод возвращающий список юнитов игрока в текущей кампании."""
        db_table = self.campaigns_dict[self.current_faction]

        query = self.session.query(
            db_table.id,
            db_table.name,
            db_table.level,
            db_table.size,
            db_table.price,
            db_table.exp,
            db_table.curr_exp,
            db_table.exp_per_kill,
            db_table.health,
            db_table.curr_health,
            db_table.armor,
            db_table.immune,
            db_table.ward,
            db_table.attack_type,
            db_table.attack_chance,
            db_table.attack_dmg,
            db_table.dot_dmg,
            db_table.attack_source,
            db_table.attack_ini,
            db_table.attack_radius,
            db_table.attack_purpose,
            db_table.prev_level,
            db_table.desc,
            db_table.slot,
            db_table.subrace,
            db_table.branch,
            db_table.attack_twice,
            db_table.regen,
            db_table.dyn_upd_level,
            db_table.upgrade_b,
            db_table.leadership,
            db_table.leader_cat,
            db_table.nat_armor,
            db_table.might,
            db_table.weapon_master,
            db_table.endurance,
            db_table.first_strike,
            db_table.accuracy,
            db_table.water_resist,
            db_table.air_resist,
            db_table.fire_resist,
            db_table.earth_resist,
            db_table.dotted
        ).order_by(db_table.slot)
        # Возвращаем список кортежей
        return query.all()

    def show_player_units(self) -> List[namedtuple]:
        """Метод возвращающий список юнитов игрока."""
        query = self.session.query(
            self.PlayerUnits.id,
            self.PlayerUnits.name,
            self.PlayerUnits.level,
            self.PlayerUnits.size,
            self.PlayerUnits.price,
            self.PlayerUnits.exp,
            self.PlayerUnits.curr_exp,
            self.PlayerUnits.exp_per_kill,
            self.PlayerUnits.health,
            self.PlayerUnits.curr_health,
            self.PlayerUnits.armor,
            self.PlayerUnits.immune,
            self.PlayerUnits.ward,
            self.PlayerUnits.attack_type,
            self.PlayerUnits.attack_chance,
            self.PlayerUnits.attack_dmg,
            self.PlayerUnits.dot_dmg,
            self.PlayerUnits.attack_source,
            self.PlayerUnits.attack_ini,
            self.PlayerUnits.attack_radius,
            self.PlayerUnits.attack_purpose,
            self.PlayerUnits.prev_level,
            self.PlayerUnits.desc,
            self.PlayerUnits.slot,
            self.PlayerUnits.subrace,
            self.PlayerUnits.branch,
            self.PlayerUnits.attack_twice,
            self.PlayerUnits.regen,
            self.PlayerUnits.dyn_upd_level,
            self.PlayerUnits.upgrade_b,
            self.PlayerUnits.leadership,
            self.PlayerUnits.leader_cat,
            self.PlayerUnits.nat_armor,
            self.PlayerUnits.might,
            self.PlayerUnits.weapon_master,
            self.PlayerUnits.endurance,
            self.PlayerUnits.first_strike,
            self.PlayerUnits.accuracy,
            self.PlayerUnits.water_resist,
            self.PlayerUnits.air_resist,
            self.PlayerUnits.fire_resist,
            self.PlayerUnits.earth_resist,
            self.PlayerUnits.dotted
        ).order_by(self.PlayerUnits.slot)
        # Возвращаем список кортежей
        return query.all()

    def show_enemy_units(self) -> List[namedtuple]:
        """Метод возвращающий список юнитов игрока."""
        query = self.session.query(
            self.CurrentDungeon.id,
            self.CurrentDungeon.name,
            self.CurrentDungeon.level,
            self.CurrentDungeon.size,
            self.CurrentDungeon.price,
            self.CurrentDungeon.exp,
            self.CurrentDungeon.curr_exp,
            self.CurrentDungeon.exp_per_kill,
            self.CurrentDungeon.health,
            self.CurrentDungeon.curr_health,
            self.CurrentDungeon.armor,
            self.CurrentDungeon.immune,
            self.CurrentDungeon.ward,
            self.CurrentDungeon.attack_type,
            self.CurrentDungeon.attack_chance,
            self.CurrentDungeon.attack_dmg,
            self.CurrentDungeon.dot_dmg,
            self.CurrentDungeon.attack_source,
            self.CurrentDungeon.attack_ini,
            self.CurrentDungeon.attack_radius,
            self.CurrentDungeon.attack_purpose,
            self.CurrentDungeon.prev_level,
            self.CurrentDungeon.desc,
            self.CurrentDungeon.slot,
            self.CurrentDungeon.subrace,
            self.CurrentDungeon.branch,
            self.CurrentDungeon.attack_twice,
            self.CurrentDungeon.regen,
            self.CurrentDungeon.dyn_upd_level,
            self.CurrentDungeon.upgrade_b,
            self.CurrentDungeon.leadership,
            self.CurrentDungeon.leader_cat,
            self.CurrentDungeon.nat_armor,
            self.CurrentDungeon.might,
            self.CurrentDungeon.weapon_master,
            self.CurrentDungeon.endurance,
            self.CurrentDungeon.first_strike,
            self.CurrentDungeon.accuracy,
            self.CurrentDungeon.water_resist,
            self.CurrentDungeon.air_resist,
            self.CurrentDungeon.fire_resist,
            self.CurrentDungeon.earth_resist,
            self.CurrentDungeon.dotted
        ).order_by(self.CurrentDungeon.slot)
        # Возвращаем список кортежей
        return query.all()

    def choose_player(self, player_name: str) -> None:
        """Метод выбора текущего игрока."""
        self.current_player = self.get_player(player_name)

    def get_player(self, player_name: str) -> namedtuple:
        """Метод получения записи конкретного игрока."""
        query = self.session.query(
            self.Players.id,
            self.Players.name,
            self.Players.email
        ).filter_by(name=player_name)
        # Возвращаем кортеж
        return query.first()

    def get_player_by_id(self, player_id: int) -> str:
        """
        Метод получения имени игрока по его id.
        """

        query = self.session.query(
            self.Players.name
        ).filter_by(id=player_id)
        # Возвращаем число
        return query.first()[-1]

    def show_all_players(self) -> List[namedtuple]:
        """
        Метод получения всех игроков.
        """
        query = self.session.query(
            self.Players.id,
            self.Players.name,
            self.Players.email
        )
        # Возвращаем кортеж
        return query.all()

    def create_player(self,
                      name: str,
                      email: str) -> None:
        """
        Метод регистрации игрока.
        Создаёт запись в таблице Players.
        """
        unit_row = self.Players(
            name,
            email
        )
        self.session.add(unit_row)
        self.session.commit()

    def delete_player(self, name: str) -> None:
        """Метод удаляющий игрока из таблицы Players."""
        if name != 'Erepb-89':
            self.session.query(self.Players).filter_by(name=name).delete()
            self.session.commit()
        else:
            print('Невозможно удалить')

    def update_player(self,
                      player_id: int,
                      player_name: str,
                      email: str) -> None:
        """
        Метод изменения имени, либо e-mail игрока.
        Изменяет запись в таблице Players.
        """

        changes = update(
            self.Players).where(
            self.Players.id == player_id).values(
            name=player_name,
            email=email).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def set_unit_slot(self,
                      new_slot: int,
                      unit: namedtuple,
                      db_table: AllUnits) -> None:
        """Установить новый номер слота юниту"""
        changes = update(
            db_table).where(
            db_table.id == unit.id).values(
            slot=new_slot).execution_options(
            synchronize_session="fetch")
        self.session.execute(changes)
        self.session.commit()

    def update_slot(self,
                    slot: int,
                    new_slot: int,
                    db_table: AllUnits) -> None:
        """Обновление слота у юнита"""
        changed_unit = self.get_unit_by_slot(slot, db_table)
        second_unit = self.get_unit_by_slot(new_slot, db_table)

        if changed_unit is not None:
            self.set_unit_slot(new_slot, changed_unit, db_table)

        if second_unit is not None:
            self.set_unit_slot(slot, second_unit, db_table)

    def update_db_table(self,
                        unit: any,
                        db_table: AllUnits,
                        new_db_table: AllUnits) -> None:
        """Обновление таблицы у юнита"""
        player_unit = new_db_table(*unit)
        self.session.add(player_unit)
        self.session.commit()

        self.delete_unit_by_id(unit.id, db_table)

    def update_slots_between_tables(self,
                                    slot: int,
                                    new_slot: int,
                                    db_table: AllUnits,
                                    new_db_table: AllUnits) -> None:
        """Обновление слота у юнита"""
        changed_unit = self.get_unit_by_slot(slot, db_table)
        second_unit = self.get_unit_by_slot(new_slot, new_db_table)

        if slot == new_slot \
                and changed_unit is not None \
                and second_unit is not None \
                and changed_unit.name not in GUARDS \
                and second_unit.name not in GUARDS:
            self.update_db_table(changed_unit, db_table, new_db_table)
            self.update_db_table(second_unit, new_db_table, db_table)

        else:
            source_unit = None
            new_unit = None

            if changed_unit is not None \
                    and changed_unit.name not in GUARDS:
                source_unit = new_db_table(*changed_unit)
                source_unit.slot = new_slot
                self.delete_player_unit(slot, db_table)

            if second_unit is not None \
                    and second_unit.name not in GUARDS:
                new_unit = db_table(*second_unit)
                new_unit.slot = slot
                self.delete_player_unit(new_slot, new_db_table)

            if source_unit is not None \
                    and source_unit.name not in GUARDS:
                self.session.add(source_unit)
                self.session.commit()

            if new_unit is not None \
                    and new_unit.name not in GUARDS:
                self.session.add(new_unit)
                self.session.commit()

    def get_gold(self,
                 player_name: str,
                 faction: str) -> int:
        """Метод получения количества золота у игрока."""

        query = self.session.query(
            self.PlayerBuildings.gold
        ).filter_by(name=player_name, faction=faction)
        # Возвращаем кортеж
        return query.order_by(self.PlayerBuildings.id.desc()).first()[0]

    def get_buildings(self,
                      player_name: str,
                      faction: str) -> namedtuple:
        """
        Метод получения построек в столице игрока.
        """

        query = self.session.query(
            self.PlayerBuildings.fighter,
            self.PlayerBuildings.mage,
            self.PlayerBuildings.archer,
            self.PlayerBuildings.support,
            self.PlayerBuildings.special,
            self.PlayerBuildings.thieves_guild,
            self.PlayerBuildings.temple,
            self.PlayerBuildings.magic_guild
        ).filter_by(name=player_name, faction=faction)
        # Возвращаем кортеж
        return query.order_by(self.PlayerBuildings.id.desc()).first()

    def clear_units(self,
                    faction: str) -> None:
        """Метод удаления юнитов в базе игрока за данную фракцию."""
        table = self.campaigns_dict[faction]
        table_res = self.res_campaigns_dict[faction]

        self.session.query(table).delete()
        self.session.query(table_res).delete()
        self.session.commit()

    def clear_buildings(self,
                        player_name: str,
                        faction: str) -> None:
        """Метод удаления построек в столице игрока."""

        self.session.query(
            self.PlayerBuildings).filter_by(
            name=player_name,
            faction=faction).delete()
        self.session.commit()

    def get_unit_by_b_name(self, b_name: str) -> str:
        """Получение юнита по названию постройки"""
        query = self.session.query(
            self.AllUnits.name
        ).where(self.AllUnits.upgrade_b == b_name)

        return query.first()[0]

    def get_fighter_branch(self) -> list:
        """
        Метод получения построек ветви бойцов в столице игрока.
        """
        query = self.session.query(
            self.PlayerBuildings.fighter
        ).where(self.PlayerBuildings.faction == self.current_faction)
        building = query[-1][0]
        temp_graph = []
        self.get_building_graph(building, temp_graph, 'fighter')
        # Возвращаем список
        return temp_graph

    def get_mage_branch(self) -> list:
        """
        Метод получения построек ветви магов в столице игрока.
        """
        query = self.session.query(
            self.PlayerBuildings.mage
        ).where(self.PlayerBuildings.faction == self.current_faction)
        building = query[-1][0]
        temp_graph = []
        self.get_building_graph(building, temp_graph, 'mage')
        # Возвращаем список
        return temp_graph

    def get_archer_branch(self) -> list:
        """
        Метод получения построек ветви стрелков в столице игрока.
        """
        query = self.session.query(
            self.PlayerBuildings.archer
        ).where(self.PlayerBuildings.faction == self.current_faction)
        building = query[-1][0]
        temp_graph = []
        self.get_building_graph(building, temp_graph, 'archer')
        # Возвращаем список
        return temp_graph

    def get_support_branch(self) -> list:
        """
        Метод получения построек ветви поддержки в столице игрока.
        """
        query = self.session.query(
            self.PlayerBuildings.support
        ).where(self.PlayerBuildings.faction == self.current_faction)
        building = query[-1][0]
        temp_graph = []
        self.get_building_graph(building, temp_graph, 'support')
        # Возвращаем список
        return temp_graph

    def get_building_graph(self,
                           bname: str,
                           graph: list,
                           branch: str) -> None:
        """Рекурсивное создание графа зданий/построек"""
        for val in FACTIONS.get(self.current_faction)[branch].values():
            if val.bname == bname:
                graph.append(bname)
                if val.prev not in ('', 0):
                    self.get_building_graph(val.prev, graph, branch)
                else:
                    return

    def create_buildings(self,
                         player_name: str,
                         faction: str,
                         gold: int,
                         buildings: list) -> None:
        """
        Метод добавления здания 0 уровня в столице игрока.
        Создаёт запись в таблице PlayerBuildings.
        """
        unit_row = self.PlayerBuildings(
            player_name,
            faction,
            gold,
            buildings[0],
            buildings[1],
            buildings[2],
            buildings[3],
            buildings[4],
            buildings[5],
            buildings[6],
            buildings[7],
        )
        self.session.add(unit_row)
        self.session.commit()

    def update_buildings(self,
                         player_name: str,
                         faction: str,
                         buildings: list) -> None:
        """
        Метод постройки здания в столице игрока (+ уровень).
        Изменяет запись в таблице PlayerBuildings.
        """
        changes = update(
            self.PlayerBuildings).values(
            fighter=buildings[0],
            mage=buildings[1],
            archer=buildings[2],
            support=buildings[3],
            special=buildings[4],
            thieves_guild=buildings[5],
            temple=buildings[6],
            magic_guild=buildings[7]).execution_options(
            synchronize_session="fetch") \
            .filter_by(name=player_name, faction=faction)

        self.session.execute(changes)
        self.session.commit()

    def update_gold(self,
                    player_name: str,
                    faction: str,
                    gold: int) -> None:
        """
        Изменяет запись Gold в таблице PlayerBuildings.
        """
        changes = update(
            self.PlayerBuildings).values(
            gold=gold).execution_options(
            synchronize_session="fetch") \
            .filter_by(name=player_name, faction=faction)

        self.session.execute(changes)
        self.session.commit()

    def transfer_units(self) -> None:
        """Перенос юнитов из CurrentDungeon в запись versus"""
        names_list = []

        # Достаем из базы подземелий имена по слоту,
        # складываем в список
        for slot in range(1, 7):
            try:
                unit_name = self.get_unit_by_slot(
                    slot, self.CurrentDungeon).name
            except AttributeError:
                unit_name = None

            if unit_name is not None:
                names_list.append(unit_name)
            else:
                names_list.append('<null>')

        # удаляем запись 'versus' из таблицы Dungeons
        self.session.query(self.Dungeons).filter_by(name='versus').delete()

        # добавляем запись 'versus' в таблицу Dungeons,
        # заполненную именами текущих юнитов
        enemy_units = self.Dungeons('versus', *names_list)
        self.session.add(enemy_units)
        self.session.commit()

    def add_dungeons(self, dungeons: dict, campaign_level: int):
        """Добавление подземелий в таблицу Dungeons"""
        mission_num = 1
        for dungeon in dungeons.values():
            dungeon_row = self.Dungeons(
                f'{self.current_faction}_'
                f'{campaign_level}_{mission_num}',
                dungeon[1],
                dungeon[2],
                dungeon[3],
                dungeon[4],
                dungeon[5],
                dungeon[6],
            )
            self.session.add(dungeon_row)
            mission_num += 1
        self.session.commit()

    def delete_dungeons(self, faction: str) -> None:
        """Удаление подземелий из таблицы Dungeons для данной фракции"""
        for i in range(1, 16):
            self.session.query(self.Dungeons).filter(
                self.Dungeons.name == f'{faction}_1_{i}'
            ).delete()
            self.session.query(self.Dungeons).filter(
                self.Dungeons.name == f'{faction}_2_{i}'
            ).delete()
            self.session.query(self.Dungeons).filter(
                self.Dungeons.name == f'{faction}_3_{i}'
            ).delete()
            self.session.query(self.Dungeons).filter(
                self.Dungeons.name == f'{faction}_4_{i}'
            ).delete()
            self.session.query(self.Dungeons).filter(
                self.Dungeons.name == f'{faction}_5_{i}'
            ).delete()

        self.session.commit()

    def delete_player_unit(self, slot: int, db_table: any) -> None:
        """Метод удаляющий юнита из выбранной таблицы по слоту."""
        self.session.query(db_table).filter_by(slot=slot).delete()
        self.session.commit()

    def delete_unit_by_id(self, id_: int, db_table: any) -> None:
        """Метод удаляющий юнита из выбранной таблицы по слоту."""
        self.session.query(db_table).filter_by(id=id_).delete()
        self.session.commit()

    def hire_guard(self) -> None:
        """Метод добавления стража в столицу игрока."""
        db_table = self.res_campaigns_dict[self.current_faction]
        unit_row = self.get_unit_by_name(
            self.guards_dict[self.current_faction])

        player_unit = db_table(*unit_row)
        player_unit.slot = 3
        self.session.add(player_unit)
        self.session.commit()

    def hire_unit(self, unit: str, slot: int) -> None:
        """Метод добавления юнита в базу игрока."""
        db_table = self.campaigns_dict[self.current_faction]

        if self.check_slot(
                unit,
                slot,
                self.get_unit_by_slot,
                db_table) is True:
            print('Данный слот занят')
        else:
            unit_row = self.get_unit_by_name(unit)
            if self.is_double(unit_row.name) and slot % 2 == 1:
                slot += 1

            player_unit = db_table(*unit_row)
            player_unit.slot = slot
            self.session.add(player_unit)
            self.session.commit()

    def hire_player_unit(self, unit: str, slot: int, db_table: any) -> None:
        """Метод добавления юнита в таблицу player_units."""
        if self.check_slot(
                unit,
                slot,
                self.get_unit_by_slot,
                db_table) is True:
            print('Данный слот занят')
        else:
            unit_row = self.get_unit_by_name(unit)
            if self.is_double(unit) and slot % 2 == 1:
                slot += 1

            player_unit = db_table(*unit_row)
            player_unit.slot = slot
            self.session.add(player_unit)
            self.session.commit()

    def hire_enemy_unit(self, unit: str, slot: int) -> None:
        """Метод добавления юнита в таблицу current_dungeon."""
        if self.check_slot(
                unit,
                slot,
                self.get_unit_by_slot,
                self.CurrentDungeon) is True:
            print('Данный слот занят')
        else:
            unit_row = self.get_unit_by_name(unit)
            if self.is_double(unit) and slot % 2 == 1:
                slot += 1

            enemy_unit = self.CurrentDungeon(*unit_row)
            enemy_unit.slot = slot
            self.session.add(enemy_unit)
            self.session.commit()

    def check_slot(self,
                   unit: namedtuple,
                   slot: int,
                   func: Callable[[int, any], any],
                   db_table: any
                   ) -> bool:
        """Проверка свободен ли слот для юнита при найме"""
        if func(slot, db_table) is not None:
            result = True

        # Если слот четный и сам юнит двойной
        elif slot % 2 == 0 and self.is_double(unit):
            result = bool(func(slot - 1, db_table))

        # Если слот нечетный и сам юнит двойной
        elif slot % 2 == 1 and self.is_double(unit):
            result = bool(func(slot + 1, db_table))

        # Если (номер слота + 1) - уже занят двойным юнитом
        elif func(slot + 1, db_table) is not None \
                and self.is_double(func(slot + 1, db_table).name):
            result = True

        # Если (номер слота - 1) - уже занят двойным юнитом
        elif slot % 2 == 0 and func(slot - 1, db_table) is not None and \
                self.is_double(func(slot - 1, db_table).name):
            result = True
        else:
            result = False

        return result

    def is_double(self, unit: namedtuple) -> bool:
        """Проверка размера юнита"""
        return self.get_unit_by_name(unit).size == BIG

    def update_unit(self,
                    unit_id: int,
                    params: dict,
                    db_table: any) -> None:
        """
        Метод изменения характеристик юнита игрока.
        Изменяет запись в переданной таблице.
        """

        changes = update(
            db_table).where(
            db_table.id == unit_id).values(
            level=params['level'],
            exp=params['exp'],
            health=params['health'],
            curr_health=params['curr_health'],
            armor=params['armor'],
            curr_exp=params['curr_exp'],
            exp_per_kill=params['exp_per_kill'],
            attack_chance=params['attack_chance'],
            attack_dmg=params['attack_dmg'],
            dot_dmg=params['dot_dmg'],
            dyn_upd_level=params['dyn_upd_level']
        ).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_unit_ini(self,
                        unit_id: int,
                        attack_ini: int,
                        db_table: AllUnits) -> None:
        """
        Метод изменения инициативы юнита игрока.
        Изменяет запись в переданной таблице.
        """

        changes = update(
            db_table).where(
            db_table.id == unit_id).values(
            attack_ini=attack_ini
        ).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_unit_health(self,
                           unit_id: int,
                           health: int,
                           db_table: AllUnits) -> None:
        """
        Метод изменения здоровья юнита игрока.
        Изменяет запись в переданной таблице.
        """

        changes = update(
            db_table).where(
            db_table.id == unit_id).values(
            health=health,
            curr_health=health
        ).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_unit_armor(self,
                          unit_id: int,
                          bonus: int,
                          db_table: AllUnits) -> None:
        """
        Метод изменения брони юнита игрока.
        Изменяет запись в переданной таблице.
        """
        unit = self.get_unit_by_id(unit_id, db_table)
        unit_armor = unit.armor + bonus

        changes = update(
            db_table).where(
            db_table.id == unit_id).values(
            armor=unit_armor
        ).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_unit_dmg(self,
                        unit_id: int,
                        bonus: int,
                        db_table: AllUnits) -> None:
        """
        Метод изменения урона юнита игрока.
        Изменяет запись в переданной таблице.
        """
        unit = self.get_unit_by_id(unit_id, db_table)
        unit_dmg = unit.attack_dmg + unit.attack_dmg * bonus

        changes = update(
            db_table).where(
            db_table.id == unit_id).values(
            armor=unit_dmg
        ).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_ward(self,
                    unit_id: int,
                    element: str,
                    db_table: AllUnits) -> None:
        """
        Метод изменения брони юнита игрока.
        Изменяет запись в переданной таблице.
        """
        unit = self.get_unit_by_id(unit_id, db_table)
        if unit.ward != 'Нет':
            unit_ward = f'{unit.ward}, {element}'
        else:
            unit_ward = element

        changes = update(
            db_table).where(
            db_table.id == unit_id).values(
            ward=unit_ward
        ).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_perks(self,
                     unit_id: int,
                     perks: dict,
                     db_table: AllUnits) -> None:
        """
        Метод изменения героя игрока (перки).
        Изменяет запись в переданной таблице.
        """
        changes = update(
            db_table).where(
            db_table.id == unit_id).values(
            leadership=perks['leadership'],
            nat_armor=perks['nat_armor'],
            might=perks['might'],
            weapon_master=perks['weapon_master'],
            endurance=perks['endurance'],
            first_strike=perks['first_strike'],
            accuracy=perks['accuracy'],
            water_resist=perks['water_resist'],
            air_resist=perks['air_resist'],
            fire_resist=perks['fire_resist'],
            earth_resist=perks['earth_resist']
        ).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_unit_curr_hp(self,
                            slot: int,
                            curr_health: int,
                            db_table: any) -> None:
        """
        Метод изменения здоровья юнита.
        Изменяет запись в переданной таблице.
        """
        changes = update(
            db_table).where(
            db_table.slot == slot).values(
            curr_health=curr_health).execution_options(
            synchronize_session="fetch")
        self.session.execute(changes)
        self.session.commit()

    def update_unit_exp(self,
                        slot: int,
                        curr_exp: int,
                        db_table: any) -> None:
        """
        Метод изменения здоровья юнита.
        Изменяет запись в переданной таблице.
        """
        changes = update(
            db_table).where(
            db_table.slot == slot).values(
            curr_exp=curr_exp).execution_options(
            synchronize_session="fetch")
        self.session.execute(changes)
        self.session.commit()

    def autoregen(self, slot: int, db_table: AllUnits) -> None:
        """
        Метод изменения юнита (здоровье).
        Изменяет запись в переданной таблице.
        Пока сделано автолечение после каждой битвы.
        """

        changes = update(
            db_table).where(
            db_table.slot == slot).values(
            curr_health=db_table.health).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def replace_unit(self,
                     slot: int,
                     new_name: str,
                     db_table: any) -> None:
        """
        Метод замены юнита на другой юнит.
        Изменяет запись в переданной таблице.
        """
        self.delete_player_unit(slot, db_table)

        if db_table in (self.PlayerUnits, self.CurrentDungeon):
            self.hire_player_unit(new_name, slot, db_table)
        else:
            self.hire_unit(new_name, slot)

    def show_dungeon_units(self, name: str) -> namedtuple:
        """Метод возвращающий список имен юнитов подземелья по названию."""
        query = self.session.query(
            self.Dungeons.unit1,
            self.Dungeons.unit2,
            self.Dungeons.unit3,
            self.Dungeons.unit4,
            self.Dungeons.unit5,
            self.Dungeons.unit6
        ).filter_by(name=name)
        # Возвращаем кортеж
        return query.first()

    def show_db_units(self, db_table: AllUnits) -> List[namedtuple]:
        """
        Метод возвращающий список юнитов игрока либо юнитов
        противника в соответствии с переданной таблицей.
        """
        query = self.session.query(
            db_table.id,
            db_table.name,
            db_table.level,
            db_table.size,
            db_table.price,
            db_table.exp,
            db_table.curr_exp,
            db_table.exp_per_kill,
            db_table.health,
            db_table.curr_health,
            db_table.armor,
            db_table.immune,
            db_table.ward,
            db_table.attack_type,
            db_table.attack_chance,
            db_table.attack_dmg,
            db_table.dot_dmg,
            db_table.attack_source,
            db_table.attack_ini,
            db_table.attack_radius,
            db_table.attack_purpose,
            db_table.prev_level,
            db_table.desc,
            db_table.slot,
            db_table.subrace,
            db_table.branch,
            db_table.attack_twice,
            db_table.regen,
            db_table.dyn_upd_level,
            db_table.upgrade_b,
            db_table.leadership,
            db_table.leader_cat,
            db_table.nat_armor,
            db_table.might,
            db_table.weapon_master,
            db_table.endurance,
            db_table.first_strike,
            db_table.accuracy,
            db_table.water_resist,
            db_table.air_resist,
            db_table.fire_resist,
            db_table.earth_resist,
            db_table.dotted
        ).order_by(db_table.slot)
        # Возвращаем список кортежей
        return query.all()

    def show_all_units(self) -> List[namedtuple]:
        """Метод возвращающий список всех известных юнитов."""
        query = self.session.query(
            self.AllUnits.id,
            self.AllUnits.name,
            self.AllUnits.level,
            self.AllUnits.size,
            self.AllUnits.price,
            self.AllUnits.exp,
            self.AllUnits.curr_exp,
            self.AllUnits.exp_per_kill,
            self.AllUnits.health,
            self.AllUnits.curr_health,
            self.AllUnits.armor,
            self.AllUnits.immune,
            self.AllUnits.ward,
            self.AllUnits.attack_type,
            self.AllUnits.attack_chance,
            self.AllUnits.attack_dmg,
            self.AllUnits.dot_dmg,
            self.AllUnits.attack_source,
            self.AllUnits.attack_ini,
            self.AllUnits.attack_radius,
            self.AllUnits.attack_purpose,
            self.AllUnits.prev_level,
            self.AllUnits.desc,
            self.AllUnits.photo,
            self.AllUnits.gif,
            self.AllUnits.slot,
            self.AllUnits.subrace,
            self.AllUnits.branch,
            self.AllUnits.attack_twice,
            self.AllUnits.regen,
            self.AllUnits.dyn_upd_level,
            self.AllUnits.upgrade_b,
            self.AllUnits.leadership,
            self.AllUnits.leader_cat,
            self.AllUnits.nat_armor,
            self.AllUnits.might,
            self.AllUnits.weapon_master,
            self.AllUnits.endurance,
            self.AllUnits.first_strike,
            self.AllUnits.accuracy,
            self.AllUnits.water_resist,
            self.AllUnits.air_resist,
            self.AllUnits.fire_resist,
            self.AllUnits.earth_resist,
            self.AllUnits.dotted
        )
        # Возвращаем список кортежей
        return query.all()

    def set_faction(self,
                    player_id: int,
                    faction: str,
                    campaign_level: int,
                    campaign_mission: int,
                    prev_mission: int,
                    day: int,
                    built: int,
                    difficulty: int) -> None:
        """Метод сохранения выбранной фракции для текущей игровой сессии"""
        game_session_row = self.GameSessions(
            player_id,
            faction,
            campaign_level,
            campaign_mission,
            prev_mission,
            day,
            built,
            difficulty)
        self.current_faction = faction
        self.session.add(game_session_row)
        self.session.commit()

    def update_session(self,
                       session_id: int,
                       campaign_level: int,
                       campaign_mission: int,
                       prev_mission: int,
                       day: int,
                       built: int) -> None:
        """Метод изменения текущей игровой сессии"""
        changes = update(
            self.GameSessions).where(
            self.GameSessions.session_id == session_id
        ).values(
            campaign_level=campaign_level,
            campaign_mission=campaign_mission,
            prev_mission=prev_mission,
            day=day,
            built=built
        ).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_session_built(self,
                             session_id: int,
                             built: int) -> None:
        """Метод изменения флага постройки в текущей игровой сессии"""
        changes = update(
            self.GameSessions).where(
            self.GameSessions.session_id == session_id
        ).values(
            built=built
        ).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_session_difficulty(self,
                                  session_id: int,
                                  difficulty: int) -> None:
        """Метод изменения сложности кампании в текущей игровой сессии"""
        changes = update(
            self.GameSessions).where(
            self.GameSessions.session_id == session_id
        ).values(
            difficulty=difficulty
        ).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def build_default(self, faction: str) -> None:
        """Базовая постройка зданий 0 уровня в столице выбранной фракции"""
        building_levels = [
            FACTIONS[faction]['fighter'][0].bname,
            FACTIONS[faction]['mage'][0].bname,
            FACTIONS[faction]['archer'][0].bname,
            FACTIONS[faction]['support'][0].bname,
            FACTIONS[faction]['special'][0].bname,
            0,
            0,
            0
        ]

        self.create_buildings(
            self.current_player.name,
            faction,
            1000,
            building_levels)


main_db = ServerStorage('../disc2.db')
main_db.show_all_units()

# Отладка
if __name__ == '__main__':
    # for item in main_db.show_all_units():
    #     print(item)

    # заполнение игроков
    # main_db.create_player('Erepb', 'erepbXXX@yandex.ru')
    # main_db.update_player(1, 'Erepb-89', 'erepbXXX@yandex.ru')
    # print(main_db.get_player('Erepb-89'))

    # базовая постройка зданий 0 уровня Empire
    # building_levels = [
    #     FACTIONS['Empire']['fighter'][1].bname,
    #     FACTIONS['Empire']['mage'][1].bname,
    #     FACTIONS['Empire']['archer'][1].bname,
    #     FACTIONS['Empire']['support'][1].bname,
    #     FACTIONS['Empire']['special'][1].bname,
    #     0,
    #     0,
    #     0
    # ]
    #
    # main_db.create_buildings('Erepb-89', 'Empire', 5000, building_levels)

    # all_buildings = main_db.get_buildings('Erepb-89', 'Undead Hordes')
    # print(all_buildings._asdict())

    # print(main_db.get_unit_by_name('Антипаладин'))
    print(1)
