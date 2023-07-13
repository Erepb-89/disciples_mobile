"""База. Классы юнитов"""

from sqlalchemy import create_engine, Table, update, Column, Integer, \
    String, MetaData
from sqlalchemy.orm import mapper, sessionmaker

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
                     slot: int
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
                slot
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
                slot
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
                slot
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
                slot
            )

    class Players:
        """Класс - игроки."""

        def __init__(self, name, email):
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
                     faction: str):
            self.session_id = None
            self.player_id = player_id
            self.faction = faction

    class Dungeons:
        """Класс - подземелья."""

        def __init__(self, name, unit1, unit2, unit3, unit4, unit5, unit6):
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
                slot
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
                slot
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
                            Column('slot', Integer)
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
                                   Column('slot', Integer)
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
                                   Column('slot', Integer)
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
            'game_sessions', self.metadata, Column(
                'session_id', Integer, primary_key=True), Column(
                'player_id', Integer), Column(
                'faction', String))

        # Создаём таблицу всех подземелий
        dungeons_table = Table('dungeons', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True),
                         Column('unit1', Integer),
                         Column('unit2', Integer),
                         Column('unit3', Integer),
                         Column('unit4', Integer),
                         Column('unit5', Integer),
                         Column('unit6', Integer)
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
                                Column('slot', Integer)
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
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.current_player = self.get_player('Erepb-89')

    def add_dungeon_unit(self, id, name, level, size,
                 price, exp, curr_exp, exp_per_kill, health, curr_health,
                 armor, immune, ward, attack_type, attack_chance, attack_dmg,
                 attack_source, attack_ini, attack_radius, attack_purpose,
                 prev_level, desc, photo, gif, slot):
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
            slot
        )
        self.session.add(unit_row)
        self.session.commit()

    def get_unit_by_name(self, name):
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
            self.AllUnits.slot
        ).filter_by(name=name)
        # Возвращаем кортеж
        return query.first()

    @property
    def current_game_session(self):
        """Метод получающий текущую игровую сессию
        (последнюю запись из таблицы GameSessions)."""
        try:
            query = self.session.query(
                self.GameSessions.id,
                self.GameSessions.player_id,
                self.GameSessions.faction,
            )
            # Возвращаем кортеж
            return query[-1]
        except BaseException:
            return str(1)

    @property
    def current_game_faction(self):
        """Метод получающий текущую фракцию
        (последнюю запись из таблицы GameSessions)."""
        try:
            query = self.session.query(
                self.GameSessions.faction).all()
            # Возвращаем одну запись
            return str(query[-1].faction)
        except BaseException:
            return str(1)

    @property
    def current_user(self):
        """Метод получающий текущего Пользователя-игрока
        (последнюю запись из таблицы GameSessions)."""
        try:
            query = self.session.query(
                self.GameSessions.player_id).all()[-1]
            user_name = self.get_player_by_id(query.player_id)
            # Возвращаем одну запись
            return user_name
        except BaseException:
            return str(1)

    def get_unit_by_id(self, _id, database):
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
            database.slot
        ).filter_by(id=_id)
        # Возвращаем кортеж
        return query.first()

    def get_unit_by_slot(self, slot, database):
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
            database.slot
        ).filter_by(slot=slot)
        # Возвращаем кортеж
        return query.first()

    def get_player_unit_by_slot(self, slot):
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
            self.PlayerUnits.slot
        ).filter_by(slot=slot)
        # Возвращаем кортеж
        return query.first()

    def show_player_units(self):
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
            self.PlayerUnits.slot
        ).order_by(self.PlayerUnits.slot)
        # Возвращаем список кортежей
        return query.all()

    def show_enemy_units(self):
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
            self.CurrentDungeon.slot
        ).order_by(self.CurrentDungeon.slot)
        # Возвращаем список кортежей
        return query.all()

    def choose_player(self, player_name):
        """
        Метод выбора текущего игрока.
        """
        self.current_player = self.get_player(player_name)

    def get_player(self, player_name):
        """
        Метод получения записи конкретного игрока.
        """

        query = self.session.query(
            self.Players.id,
            self.Players.name,
            self.Players.email
        ).filter_by(name=player_name)
        # Возвращаем кортеж
        return query.first()

    def get_player_by_id(self, player_id):
        """
        Метод получения имени игрока по его id.
        """

        query = self.session.query(
            self.Players.name
        ).filter_by(id=player_id)
        # Возвращаем число
        return query.first()[-1]

    def show_all_players(self):
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
                      email: str):
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

    def delete_player(self, name):
        """Метод удаляющий игрока из таблицы Players."""
        if name != 'Erepb-89':
            self.session.query(self.Players).filter_by(name=name).delete()
            self.session.commit()
        else:
            print('Невозможно удалить')

    def update_player(self,
                      player_id: int,
                      player_name: str,
                      email: str):
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

    def update_player_slot(self, slot, new_slot):
        """ """

        changed_unit = self.get_player_unit_by_slot(slot)
        if changed_unit is not None:
            changed_unit_id = changed_unit.id

        second_unit = self.get_player_unit_by_slot(new_slot)
        if second_unit is not None:
            second_unit_id = second_unit.id

        changes = update(
            self.PlayerUnits).where(
            self.PlayerUnits.id == changed_unit_id).values(
            slot=new_slot).execution_options(
            synchronize_session="fetch")
        self.session.execute(changes)
        self.session.commit()

        second_changes = update(
            self.PlayerUnits).where(
            self.PlayerUnits.id == second_unit_id).values(
            slot=slot).execution_options(
            synchronize_session="fetch")
        self.session.execute(second_changes)
        self.session.commit()

    def set_unit_slot(self, new_slot, unit, database):
        changes = update(
            database).where(
            database.id == unit.id).values(
            slot=new_slot).execution_options(
            synchronize_session="fetch")
        self.session.execute(changes)
        self.session.commit()

    def update_slot(self, slot, new_slot, database):
        """Обновление слота у юнита"""
        changed_unit = self.get_unit_by_slot(slot, database)
        second_unit = self.get_unit_by_slot(new_slot, database)

        if changed_unit is not None:
            self.set_unit_slot(new_slot, changed_unit, database)

        if second_unit is not None:
            self.set_unit_slot(slot, second_unit, database)

    def get_gold(self,
                      player_name: str,
                      faction: str):
        """
        Метод получения построек в столице игрока (уровень).
        """

        query = self.session.query(
            self.PlayerBuildings.gold
        ).filter_by(name=player_name, faction=faction)
        # Возвращаем кортеж
        return query.order_by(self.PlayerBuildings.id.desc()).first()[0]

    def get_buildings(self,
                      player_name: str,
                      faction: str):
        """
        Метод получения построек в столице игрока (уровень).
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
                        faction: str):
        """
        Метод получения построек в столице игрока (уровень).
        """

        self.session.query(
            self.PlayerBuildings).filter_by(
            name=player_name,
            faction=faction).delete()
        self.session.commit()

    def get_fighter_branch(self,
                           player_name: str,
                           faction: str):
        """
        Метод получения построек ветви в столице игрока.
        """

        query = self.session.query(
            self.PlayerBuildings.fighter
        ).filter_by(name=player_name, faction=faction)
        # Возвращаем кортеж
        return query.all()

    def create_buildings(self,
                         player_name: str,
                         faction: str,
                         gold: int,
                         buildings: list):
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
                         buildings: list):
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
                    gold: int):
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

    def transfer_units(self):
        """Перенос юнитов из CurrentDungeon в запись versus"""
        current_dict = {}
        enemy_dict = {}
        id_list = []

        # Достаем из базы подземелий имена по слоту,
        # складываем в словарь
        for slot in range(1, 7):
            try:
                unit_name = self.get_unit_by_slot(
                    slot, self.CurrentDungeon).name
            except BaseException:
                unit_name = None
            current_dict[slot] = unit_name

        # Достаем из базы существ id по имени существа,
        # складываем в словарь
        for slot, name in current_dict.items():
            try:
                enemy_dict[slot] = self.get_unit_by_name(
                    name).id
            except BaseException:
                enemy_dict[slot] = None

        # Пробегаемся по словарю, если слот не пустой (есть id),
        # добавляем id в список, иначе - добавляем Null
        for slot, _id in enemy_dict.items():
            if _id is not None:
                id_list.append(_id)
            else:
                id_list.append('<null>')

        # удаляем запись 'versus' из таблицы Dungeons
        self.session.query(self.Dungeons).filter_by(name='versus').delete()

        # добавляем запись 'versus' в таблицу Dungeons,
        # заполненную id текущих юнитов
        enemy_unit = self.Dungeons('versus', *id_list)
        self.session.add(enemy_unit)
        self.session.commit()

    def delete_player_unit(self, slot):
        """Метод удаляющий юнита из базы игрока по слоту."""
        self.session.query(self.PlayerUnits).filter_by(slot=slot).delete()
        self.session.commit()

    def delete_dungeon_unit(self, slot):
        """Метод удаляющий юнита из базы текущего подземелья по слоту."""
        self.session.query(self.CurrentDungeon).filter_by(slot=slot).delete()
        self.session.commit()

    def hire_unit(self, unit, slot):
        """Метод добавления юнита в базу игрока."""
        if self.check_slot(
                unit,
                slot,
                self.get_player_unit_by_slot) is True:  # Нужно заменить на get_unit_by_slot
            print('Данный слот занят')
        else:
            unit_row = self.get_unit_by_name(unit)
            # print(unit_row._asdict())
            if self.is_double(unit_row.name) and slot % 2 == 1:
                slot += 1

            player_unit = self.PlayerUnits(*unit_row[:24], slot)
            self.session.add(player_unit)
            self.session.commit()

    def hire_enemy_unit(self, unit, slot):
        """Метод добавления юнита в базу противника."""
        if self.check_slot(
                unit,
                slot,
                self.get_dungeon_unit_by_slot) is True:  # Нужно заменить на get_unit_by_slot
            print('Данный слот занят')
        else:
            # unit_row = self.get_unit_by_name(unit).id
            unit_row = self.get_unit_by_name(unit)
            # print(unit_row._asdict())
            if self.is_double(unit) and slot % 2 == 1:
                slot += 1

            enemy_unit = self.CurrentDungeon(*unit_row[:24], slot)
            # enemy_unit = self.Dungeons(unit_id)
            self.session.add(enemy_unit)
            self.session.commit()

    def check_slot(self, unit, slot, func):
        if func(slot) is not None:
            return True

        # Если слот четный и сам юнит двойной
        if slot % 2 == 0 and self.is_double(unit):
            if func(slot - 1) is not None:
                return True

        # Если слот нечетный и сам юнит двойной
        elif slot % 2 == 1 and self.is_double(unit):
            if func(slot + 1) is not None:
                return True

        # Если (номер слота + 1) - уже занят двойным юнитом
        elif func(slot + 1) is not None and self.is_double(func(slot + 1).name):
            return True

        # Если (номер слота - 1) - уже занят двойным юнитом
        elif slot % 2 == 0 and func(slot - 1) is not None and \
                self.is_double(func(slot - 1).name):
            return True
        else:
            return False

    def is_double(self, unit):
        return self.get_unit_by_name(unit).size == "Большой"

    def update_unit(self, unit_id, curr_health, exp):
        """
        Метод изменения юнита игрока (здоровье и опыт).
        Изменяет запись в таблице PlayerUnits.
        """

        changes = update(
            self.PlayerUnits).where(
            self.PlayerUnits.id == unit_id).values(
            curr_health=curr_health,
            exp=exp).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_unit_hp(self, slot, curr_health, database):
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

    def update_unit_exp(self, slot, curr_exp, database):
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

    def autoregen(self, slot):
        """
        Метод изменения юнита (здоровье).
        Изменяет запись в таблице player_units.
        Пока сделано автолечение после каждой битвы
        """

        changes = update(
            self.PlayerUnits).where(
            self.PlayerUnits.slot == slot).values(
            curr_health=self.PlayerUnits.health).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def replace_unit(self, slot, new_name):
        """
        Метод замены юнита на другой юнит.
        Изменяет запись в таблице AllUnits.
        """
        self.delete_player_unit(slot)
        self.hire_unit(new_name, slot)

    def show_dungeon_units(self, name):
        """Метод возвращающий список юнитов подземелья."""
        query = self.session.query(
            self.Dungeons.unit1,
            self.Dungeons.unit2,
            self.Dungeons.unit3,
            self.Dungeons.unit4,
            self.Dungeons.unit5,
            self.Dungeons.unit6
        ).filter_by(name=name)
        # Возвращаем список кортежей
        return query.first()

    def get_dungeon_unit_by_slot(self, slot):
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
            self.CurrentDungeon.slot
        ).filter_by(slot=slot)
        # Возвращаем кортеж
        return query.first()

    def show_db_units(self, database):
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
            database.slot
        ).order_by(database.slot)
        # Возвращаем список кортежей
        return query.all()

    def show_all_units(self):
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
            self.AllUnits.slot
        )
        # Возвращаем список кортежей
        return query.all()

    def set_faction(self, player_id, faction):
        """
        Метод сохранения выбранной фракции для текущей игровой сессии.
        """
        game_session_row = self.GameSessions(
            player_id,
            faction
        )
        self.session.add(game_session_row)
        self.session.commit()

    def build_default(self, faction):
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

        self.create_buildings(self.current_user, faction, 5000, building_levels)


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

    # базовая постройка зданий 0 уровня Mountain Clans
    # building_levels = [
    #     FACTIONS['Mountain Clans']['fighter'][1].bname,
    #     FACTIONS['Mountain Clans']['mage'][1].bname,
    #     FACTIONS['Mountain Clans']['archer'][1].bname,
    #     FACTIONS['Mountain Clans']['support'][1].bname,
    #     FACTIONS['Mountain Clans']['special'][1].bname,
    #     0,
    #     0,
    #     0
    # ]

    # main_db.create_buildings('Erepb-89', 'Mountain Clans', 5000, building_levels)

    # print(main_db.get_buildings('Erepb-89', 'Empire'))

    # building_levels_2 = [
    #     FACTIONS['Empire']['fighter'][2].bname,
    #     FACTIONS['Empire']['mage'][1].bname,
    #     FACTIONS['Empire']['archer'][1].bname,
    #     FACTIONS['Empire']['support'][1].bname,
    #     FACTIONS['Empire']['special'][1].bname,
    #     0,
    #     0,
    #     0
    # ]

    all_buildings = main_db.get_buildings('Erepb-89', 'Undead Hordes')
    print(all_buildings._asdict())

    #
    # changed_buildings = list(all_buildings)
    # print(changed_buildings)
    # changed_buildings[1] = factions.get('Empire')['fighter'][3].bname
    #
    # player_gold = main_db.get_gold('Erepb-89', 'Empire')
    # changed_gold = player_gold - factions.get('Empire')['fighter'][3].cost

    # main_db.update_buildings('Erepb-89', 'Empire', changed_buildings)
    # main_db.update_gold('Erepb-89', 'Empire', changed_gold)

    # fighter_branch = main_db.get_fighter_branch('Erepb-89', 'Empire')

    # for New Game
    # main_db.clear_buildings('Erepb-89', 'Empire')

