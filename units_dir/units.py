"""База. Классы юнитов"""
import re
from collections import namedtuple
from typing import Callable, List

from sqlalchemy import create_engine, Table, update, Column, Integer, \
    String, MetaData
from sqlalchemy.orm import mapper, sessionmaker

from client_dir.settings import BIG
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
                     earth_resist: int
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

    class PlayerUnits(AllUnits):
        """Класс - отображение таблицы юнитов игрока."""

        def __init__(
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
                earth_resist
        ):
            super().__init__(
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
                earth_resist
            )

    class Player2Units(AllUnits):
        """Класс - отображение таблицы юнитов игрока 2."""

        def __init__(
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
                earth_resist
        ):
            super().__init__(
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
                earth_resist
            )

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
                     day: int,
                     built: int
                     ):
            self.session_id = None
            self.player_id = player_id
            self.faction = faction
            self.campaign_level = campaign_level
            self.day = day
            self.built = built

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

    class CurrentDungeon(AllUnits):
        """Класс - подземелье."""

        def __init__(
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
                earth_resist
        ):
            super().__init__(
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
                earth_resist
            )

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
        # self.auto_id = 10

        units_table = Table('units', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
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
                            Column('attack_source', String),
                            Column('attack_ini', Integer),
                            Column('attack_radius', String),
                            Column('attack_purpose', Integer),
                            Column('prev_level', String),
                            Column('desc', String),
                            Column('photo', String),
                            Column('gif', String),
                            Column('slot', Integer),
                            Column('subrace', Integer),
                            Column('branch', Integer),
                            Column('attack_twice', Integer),
                            Column('regen', Integer),
                            Column('dyn_upd_level', Integer),
                            Column('upgrade_b', Integer),
                            Column('leadership', Integer),
                            Column('leader_cat', Integer),
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
                            )

        player_units_table = Table('player_units', self.metadata,
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
                                   Column('attack_source', String),
                                   Column('attack_ini', Integer),
                                   Column('attack_radius', String),
                                   Column('attack_purpose', Integer),
                                   Column('prev_level', String),
                                   Column('desc', String),
                                   Column('photo', String),
                                   Column('gif', String),
                                   Column('slot', Integer),
                                   Column('subrace', Integer),
                                   Column('branch', Integer),
                                   Column('attack_twice', Integer),
                                   Column('regen', Integer),
                                   Column('dyn_upd_level', Integer),
                                   Column('upgrade_b', Integer),
                                   Column('leadership', Integer),
                                   Column('leader_cat', Integer),
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
                                   )

        player2_units_table = Table('player2_units', self.metadata,
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
                                    Column('attack_source', String),
                                    Column('attack_ini', Integer),
                                    Column('attack_radius', String),
                                    Column('attack_purpose', Integer),
                                    Column('prev_level', String),
                                    Column('desc', String),
                                    Column('photo', String),
                                    Column('gif', String),
                                    Column('slot', Integer),
                                    Column('subrace', Integer),
                                    Column('branch', Integer),
                                    Column('attack_twice', Integer),
                                    Column('regen', Integer),
                                    Column('dyn_upd_level', Integer),
                                    Column('upgrade_b', Integer),
                                    Column('leadership', Integer),
                                    Column('leader_cat', Integer),
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
                                    )

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
            Column('day', Integer),
            Column('built', Integer)
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

        current_dungeon_table = Table('current_dungeon', self.metadata,
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
                                      Column('attack_source', String),
                                      Column('attack_ini', Integer),
                                      Column('attack_radius', String),
                                      Column('attack_purpose', Integer),
                                      Column('prev_level', String),
                                      Column('desc', String),
                                      Column('photo', String),
                                      Column('gif', String),
                                      Column('slot', Integer),
                                      Column('subrace', Integer),
                                      Column('branch', Integer),
                                      Column('attack_twice', Integer),
                                      Column('regen', Integer),
                                      Column('dyn_upd_level', Integer),
                                      Column('upgrade_b', Integer),
                                      Column('leadership', Integer),
                                      Column('leader_cat', Integer),
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

        # Создаём сессию
        session = sessionmaker(bind=self.database_engine)
        self.session = session()

        self.current_player = self.get_player('Erepb-89')

        # текущая игровая сессия
        curr_game_session = self.current_game_session(
            self.current_player.id)
        if curr_game_session is not None:
            self.current_faction = curr_game_session.faction
            self.campaign_level = curr_game_session.campaign_level
            self.campaign_day = curr_game_session.day
            self.already_built = curr_game_session.built
            self.game_session_id = curr_game_session.session_id
        else:
            self.current_faction = 'Empire'
            self.campaign_level = 1
            self.campaign_day = 1
            self.already_built = 0

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
            earth_resist):
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
            earth_resist
        )
        self.session.add(unit_row)
        self.session.commit()

    def get_unit_by_name(self, name: str) -> namedtuple:
        """Метод получающий юнита из общей базы по имени."""
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
            self.AllUnits.earth_resist
        ).filter_by(name=name)
        # Возвращаем кортеж
        return query.first()

    def game_session_by_faction(self, player_id: int, faction: str) -> any:
        """Метод получающий игровую сессию по игроку и фракции."""
        query = self.session.query(
            self.GameSessions.session_id,
            self.GameSessions.player_id,
            self.GameSessions.faction,
            self.GameSessions.campaign_level,
            self.GameSessions.day,
            self.GameSessions.built,
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
            self.GameSessions.day,
            self.GameSessions.built,
        ).filter_by(player_id=player_id)
        # Возвращаем кортеж
        return query.order_by(self.GameSessions.session_id.desc()).first()

    def get_unit_by_id(self, _id: int, database: any) -> namedtuple:
        """Метод получающий юнита из общей базы по id."""
        query = self.session.query(
            database.id,
            database.name,
            database.level,
            database.size,
            database.price,
            database.exp,
            database.curr_exp,
            database.exp_per_kill,
            database.health,
            database.curr_health,
            database.armor,
            database.immune,
            database.ward,
            database.attack_type,
            database.attack_chance,
            database.attack_dmg,
            database.attack_source,
            database.attack_ini,
            database.attack_radius,
            database.attack_purpose,
            database.prev_level,
            database.desc,
            database.photo,
            database.gif,
            database.slot,
            database.subrace,
            database.branch,
            database.attack_twice,
            database.regen,
            database.dyn_upd_level,
            database.upgrade_b,
            database.leadership,
            database.leader_cat,
            database.nat_armor,
            database.might,
            database.weapon_master,
            database.endurance,
            database.first_strike,
            database.accuracy,
            database.water_resist,
            database.air_resist,
            database.fire_resist,
            database.earth_resist
        ).filter_by(id=_id)
        # Возвращаем кортеж
        return query.first()

    def get_unit_by_slot(self, slot: int, database: any) -> namedtuple:
        """Метод получающий юнита из базы игрока по слоту."""
        query = self.session.query(
            database.id,
            database.name,
            database.level,
            database.size,
            database.price,
            database.exp,
            database.curr_exp,
            database.exp_per_kill,
            database.health,
            database.curr_health,
            database.armor,
            database.immune,
            database.ward,
            database.attack_type,
            database.attack_chance,
            database.attack_dmg,
            database.attack_source,
            database.attack_ini,
            database.attack_radius,
            database.attack_purpose,
            database.prev_level,
            database.desc,
            database.photo,
            database.gif,
            database.slot,
            database.subrace,
            database.branch,
            database.attack_twice,
            database.regen,
            database.dyn_upd_level,
            database.upgrade_b,
            database.leadership,
            database.leader_cat,
            database.nat_armor,
            database.might,
            database.weapon_master,
            database.endurance,
            database.first_strike,
            database.accuracy,
            database.water_resist,
            database.air_resist,
            database.fire_resist,
            database.earth_resist
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
            self.AllUnits.earth_resist
        ).filter(self.AllUnits.level == level,
                 self.AllUnits.branch != 'hero')
        # Возвращаем список кортежей
        return query.all()

    def get_player_unit_by_slot(self, slot: int) -> namedtuple:
        """Метод получающий юнита из базы игрока по слоту."""
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
            self.PlayerUnits.earth_resist
        ).filter_by(slot=slot)
        # Возвращаем кортеж
        return query.first()

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
            self.PlayerUnits.earth_resist
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
            self.CurrentDungeon.earth_resist
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
                      database: any) -> None:
        """Установить новый номер слота юниту"""
        changes = update(
            database).where(
            database.id == unit.id).values(
            slot=new_slot).execution_options(
            synchronize_session="fetch")
        self.session.execute(changes)
        self.session.commit()

    def update_slot(self,
                    slot: int,
                    new_slot: int,
                    database: any) -> None:
        """Обновление слота у юнита"""
        changed_unit = self.get_unit_by_slot(slot, database)
        second_unit = self.get_unit_by_slot(new_slot, database)

        if changed_unit is not None:
            self.set_unit_slot(new_slot, changed_unit, database)

        if second_unit is not None:
            self.set_unit_slot(slot, second_unit, database)

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

    def clear_buildings(self,
                        player_name: str,
                        faction: str) -> None:
        """
        Метод удаления построек в столице игрока.
        """

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

    def delete_player_unit(self, slot: int) -> None:
        """Метод удаляющий юнита из базы игрока по слоту."""
        self.session.query(self.PlayerUnits).filter_by(slot=slot).delete()
        self.session.commit()

    def delete_dungeon_unit(self, slot: int) -> None:
        """Метод удаляющий юнита из базы текущего подземелья по слоту."""
        self.session.query(self.CurrentDungeon).filter_by(slot=slot).delete()
        self.session.commit()

    def hire_unit(self, unit: namedtuple, slot: int) -> None:
        """Метод добавления юнита в базу игрока."""
        if self.check_slot(
                unit,
                slot,
                self.get_player_unit_by_slot) is True:  # Нужно заменить на get_unit_by_slot
            print('Данный слот занят')
        else:
            unit_row = self.get_unit_by_name(unit)
            unit_cols_after_slot = main_db.get_unit_by_name(
                unit)[25:43]

            # print(unit_row._asdict())
            if self.is_double(unit_row.name) and slot % 2 == 1:
                slot += 1

            player_unit = self.PlayerUnits(
                *unit_row[:24],
                slot,
                *unit_cols_after_slot)
            self.session.add(player_unit)
            self.session.commit()

    def hire_enemy_unit(self, unit: namedtuple, slot: int) -> None:
        """Метод добавления юнита в базу противника."""
        if self.check_slot(
                unit,
                slot,
                self.get_dungeon_unit_by_slot) is True:  # Нужно заменить на get_unit_by_slot
            print('Данный слот занят')
        else:
            unit_row = self.get_unit_by_name(unit)
            unit_cols_after_slot = main_db.get_unit_by_name(
                unit)[25:43]

            # print(unit_row._asdict())
            if self.is_double(unit) and slot % 2 == 1:
                slot += 1

            enemy_unit = self.CurrentDungeon(
                *unit_row[:24],
                slot,
                *unit_cols_after_slot)
            # enemy_unit = self.Dungeons(unit_id)
            self.session.add(enemy_unit)
            self.session.commit()

    def check_slot(self,
                   unit: namedtuple,
                   slot: int,
                   func: Callable[[int], any]
                   ) -> bool:
        """Проверка свободен ли слот для юнита"""
        result = func(slot) is not None

        # Если слот четный и сам юнит двойной
        if slot % 2 == 0 and self.is_double(unit):
            if func(slot - 1) is not None:
                result = True

        # Если слот нечетный и сам юнит двойной
        elif slot % 2 == 1 and self.is_double(unit):
            if func(slot + 1) is not None:
                result = True

        # Если (номер слота + 1) - уже занят двойным юнитом
        elif func(slot + 1) is not None and self.is_double(func(slot + 1).name):
            result = True

        # Если (номер слота - 1) - уже занят двойным юнитом
        elif slot % 2 == 0 and func(slot - 1) is not None and \
                self.is_double(func(slot - 1).name):
            result = True
        else:
            result = False

        return result

    def is_double(self, unit: namedtuple) -> bool:
        """Проверка размера юнита"""
        return self.get_unit_by_name(unit).size == BIG

    def update_unit(self,
                    unit_id: int,
                    level: int,
                    exp: int,
                    health: int,
                    curr_health: int,
                    curr_exp: int,
                    exp_per_kill: int,
                    attack_chance: str,
                    attack_dmg: int,
                    dyn_upd_level) -> None:
        """
        Метод изменения характеристик юнита игрока.
        Изменяет запись в таблице PlayerUnits.
        """

        changes = update(
            self.PlayerUnits).where(
            self.PlayerUnits.id == unit_id).values(
            level=level,
            exp=exp,
            health=health,
            curr_health=curr_health,
            curr_exp=curr_exp,
            exp_per_kill=exp_per_kill,
            attack_chance=attack_chance,
            attack_dmg=attack_dmg,
            dyn_upd_level=dyn_upd_level
        ).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_perks(self,
                     unit_id: int,
                     perks: dict) -> None:
        """
        Метод изменения героя игрока (перки).
        Изменяет запись в таблице PlayerUnits.
        """
        changes = update(
            self.PlayerUnits).where(
            self.PlayerUnits.id == unit_id).values(
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

    def update_unit_hp(self,
                       slot: int,
                       curr_health: int,
                       database: any) -> None:
        """
        Метод изменения здоровья юнита.
        Изменяет запись в таблице player_units либо в current_dungeon.
        """
        changes = update(
            database).where(
            database.slot == slot).values(
            curr_health=curr_health).execution_options(
            synchronize_session="fetch")
        self.session.execute(changes)
        self.session.commit()

    def update_unit_exp(self,
                        slot: int,
                        curr_exp: int,
                        database: any) -> None:
        """
        Метод изменения здоровья юнита.
        Изменяет запись в таблице player_units либо в current_dungeon.
        """
        changes = update(
            database).where(
            database.slot == slot).values(
            curr_exp=curr_exp).execution_options(
            synchronize_session="fetch")
        self.session.execute(changes)
        self.session.commit()

    def autoregen(self, slot: int) -> None:
        """
        Метод изменения юнита (здоровье).
        Изменяет запись в таблице player_units.
        Пока сделано автолечение после каждой битвы.
        """

        changes = update(
            self.PlayerUnits).where(
            self.PlayerUnits.slot == slot).values(
            curr_health=self.PlayerUnits.health).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def replace_unit(self, slot: int, new_name: str) -> None:
        """
        Метод замены юнита на другой юнит.
        Изменяет запись в таблице AllUnits.
        """
        self.delete_player_unit(slot)
        self.hire_unit(new_name, slot)

    def show_dungeon_units(self, name: str) -> namedtuple:
        """Метод возвращающий список юнитов подземелья."""
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

    def get_dungeon_unit_by_slot(self, slot: int) -> namedtuple:
        """Метод получающий юнита из базы подземелья по слоту."""
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
            self.CurrentDungeon.earth_resist
        ).filter_by(slot=slot)
        # Возвращаем кортеж
        return query.first()

    def show_db_units(self, database: any) -> List[namedtuple]:
        """
        Метод возвращающий список юнитов
        игрока либо юнитов противника.
        """
        query = self.session.query(
            database.id,
            database.name,
            database.level,
            database.size,
            database.price,
            database.exp,
            database.curr_exp,
            database.exp_per_kill,
            database.health,
            database.curr_health,
            database.armor,
            database.immune,
            database.ward,
            database.attack_type,
            database.attack_chance,
            database.attack_dmg,
            database.attack_source,
            database.attack_ini,
            database.attack_radius,
            database.attack_purpose,
            database.prev_level,
            database.desc,
            database.slot,
            database.subrace,
            database.branch,
            database.attack_twice,
            database.regen,
            database.dyn_upd_level,
            database.upgrade_b,
            database.leadership,
            database.leader_cat,
            database.nat_armor,
            database.might,
            database.weapon_master,
            database.endurance,
            database.first_strike,
            database.accuracy,
            database.water_resist,
            database.air_resist,
            database.fire_resist,
            database.earth_resist
        ).order_by(database.slot)
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
            self.AllUnits.earth_resist
        )
        # Возвращаем список кортежей
        return query.all()

    def set_faction(self,
                    player_id: int,
                    faction: str,
                    campaign_level: int,
                    day: int,
                    built: int) -> None:
        """Метод сохранения выбранной фракции для текущей игровой сессии"""
        game_session_row = self.GameSessions(
            player_id,
            faction,
            campaign_level,
            day,
            built)
        self.current_faction = faction
        self.session.add(game_session_row)
        self.session.commit()

    def update_session(self,
                       session_id: int,
                       campaign_level: int,
                       day: int,
                       built: int) -> None:
        """Метод изменения текущей игровой сессии"""
        changes = update(
            self.GameSessions).where(
            self.GameSessions.session_id == session_id
        ).values(
            campaign_level=campaign_level,
            day=day,
            built=built
        ).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_session_built(self,
                             session_id: int,
                             built: int) -> None:
        """Метод изменения текущей игровой сессии"""
        changes = update(
            self.GameSessions).where(
            self.GameSessions.session_id == session_id
        ).values(
            built=built
        ).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def build_default(self, faction: str) -> None:
        """Базовая постройка зданий 1 уровня в выбранной столице"""
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
            500,
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

    print(1)
