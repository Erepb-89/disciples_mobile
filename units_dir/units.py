"""Unit classes"""

from sqlalchemy import create_engine, Table, update, Column, Integer, \
    String, MetaData
from sqlalchemy.orm import mapper, sessionmaker


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

    class GameSessions:
        """Класс - игровые сессии."""

        def __init__(self, player_id, faction):
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
                                   Column('desc', String),
                                   Column('photo', String),
                                   Column('gif', String),
                                   Column('slot', Integer)
                                   )

        # Создаём таблицу игроков
        players_table = Table('Players', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('name', String),
                              Column('email', String)
                              )

        # Создаём таблицу игровых сессий
        game_sessions_table = Table('GameSessions', self.metadata,
                                    Column('session_id', Integer, primary_key=True),
                                    Column('player_id', Integer),
                                    Column('faction', String)
                                    )

        # Создаём таблицу всех подземелий
        dungeons = Table('Dungeons', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True),
                         Column('unit1', Integer),
                         Column('unit2', Integer),
                         Column('unit3', Integer),
                         Column('unit4', Integer),
                         Column('unit5', Integer),
                         Column('unit6', Integer)
                         )

        current_dungeon = Table('current_dungeon', self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('name', String),
                                Column('level', Integer),
                                Column('size', String),
                                Column('price', Integer),
                                Column('exp', Integer),
                                Column('curr_exp', Integer),
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
                                Column('desc', Integer),
                                Column('photo', String),
                                Column('gif', String),
                                Column('slot', Integer)
                                )

        # Создаём таблицы
        self.metadata.create_all(self.database_engine)

        # Создаём отображения
        mapper(self.AllUnits, units_table)
        mapper(self.PlayerUnits, player_units_table)
        mapper(self.Players, players_table)
        mapper(self.GameSessions, game_sessions_table)
        mapper(self.Dungeons, dungeons)
        mapper(self.CurrentDungeon, current_dungeon)

        # Создаём сессию
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

    def add_unit(self, id, name, level, size,
                 price, exp, curr_exp, health, curr_health, armor,
                 immune, ward, attack_type, attack_chance, attack_dmg,
                 attack_source, attack_ini, attack_radius, attack_purpose,
                 desc, photo, gif, slot):
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
            self.AllUnits.desc,
            self.AllUnits.photo,
            self.AllUnits.gif,
            self.AllUnits.slot
        ).filter_by(name=name)
        # Возвращаем кортеж
        return query.first()

    # @property
    def current_game_faction(self):
        """Метод получающий текущую фракцию
        (последнюю запись из таблицы GameSessions)."""
        try:
            query = self.session.query(
                self.GameSessions.faction).all()
            # Возвращаем одну запись
            return str(query[-1].faction)
        except:
            return str(1)

    def get_unit_by_id(self, id):
        """Метод получающий юнита из общей базы по id."""
        query = self.session.query(
            self.AllUnits.id,
            self.AllUnits.name,
            self.AllUnits.level,
            self.AllUnits.size,
            self.AllUnits.price,
            self.AllUnits.exp,
            self.AllUnits.curr_exp,
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
            self.AllUnits.desc,
            self.AllUnits.photo,
            self.AllUnits.gif,
            self.AllUnits.slot
        ).filter_by(id=id)
        # Возвращаем кортеж
        return query.first()

    def get_unit_by_slot(self, slot):
        """Метод получающий юнита из базы игрока по слоту."""
        query = self.session.query(
            self.PlayerUnits.id,
            self.PlayerUnits.name,
            self.PlayerUnits.level,
            self.PlayerUnits.size,
            self.PlayerUnits.price,
            self.PlayerUnits.exp,
            self.PlayerUnits.curr_exp,
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
            self.PlayerUnits.desc,
            # self.AllUnits.photo,
            # self.AllUnits.gif,
            self.PlayerUnits.slot
        ).filter_by(slot=slot)
        # Возвращаем кортеж
        return query.first()

    def delete_unit(self, slot):
        """Метод удаляющий юнита из базы игрока по слоту."""
        self.session.query(self.PlayerUnits).filter_by(slot=slot).delete()
        self.session.commit()

    def delete_dungeon_unit(self, slot):
        """Метод удаляющий юнита из базы игрока по слоту."""
        self.session.query(self.CurrentDungeon).filter_by(slot=slot).delete()
        self.session.commit()

    def hire_unit(self, unit, slot):
        """Метод добавления юнита в базу игрока."""
        if self.check_slot(unit, slot) is True:
            print('Данный слот занят')
        else:
            unit_row = self.get_unit_by_name(unit)
            # print(unit_row._asdict())
            if self.is_double(unit_row.name) and slot % 2 == 1:
                slot += 1

            # _id = self.auto_id
            player_unit = self.PlayerUnits(*unit_row[:22], slot)
            # self.auto_id += 1
            self.session.add(player_unit)
            self.session.commit()

    def add_in_dungeon(self, unit, slot, dungeon):
        """Метод добавления юнита в базу выбранного подземелья."""
        if self.check_slot(unit, slot) is True:
            print('Данный слот занят')
        else:
            unit_row = self.get_unit_by_name(unit)
            # print(unit_row._asdict())
            if self.is_double(unit_row.name) and slot % 2 == 1:
                slot += 1

            player_unit = self.PlayerUnits(*unit_row[:22], slot)
            self.session.add(player_unit)
            self.session.commit()

    def check_slot(self, unit, slot):
        if self.get_unit_by_slot(slot) is not None:
            return True
        if slot % 2 == 0 and self.is_double(unit):
            if self.get_unit_by_slot(slot - 1) is not None:
                return True
        elif slot % 2 == 1 and self.is_double(unit):
            if self.get_unit_by_slot(slot + 1) is not None:
                return True
        elif slot % 2 == 0 and self.get_unit_by_slot(slot - 1) is not None and \
                self.is_double(self.get_unit_by_slot(slot - 1).name):
            return True
        else:
            return False

    def is_double(self, unit):
        return self.get_unit_by_name(unit).size == "Большой"

    def update_unit(self, unit_id, curr_health, exp):
        """
        Метод изменения юнита (здоровье и опыт).
        Изменяет запись в таблице PlayersUnits.
        """

        changes = update(
            self.PlayerUnits).where(
            self.PlayerUnits.id == unit_id).values(
            curr_health=curr_health,
            exp=exp).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_dungeon_unit(self, slot, curr_health):
        """
        Метод изменения юнита (здоровье).
        Изменяет запись в таблице current_dungeon.
        """

        changes = update(
            self.CurrentDungeon).where(
            self.CurrentDungeon.slot == slot).values(
            curr_health=curr_health).execution_options(
            synchronize_session="fetch")

        self.session.execute(changes)
        self.session.commit()

    def update_player_unit(self, slot, curr_health):
        """
        Метод изменения юнита (здоровье).
        Изменяет запись в таблице player_units.
        """

        changes = update(
            self.PlayerUnits).where(
            self.PlayerUnits.slot == slot).values(
            curr_health=curr_health).execution_options(
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

    def update_unit_slot(self, self_slot, other_slot):
        """
        Метод изменения юнита (здоровье и опыт).
        Изменяет запись в таблице PlayersUnits.
        """
        self_unit = self.get_unit_by_slot(self_slot)
        other_unit = self.get_unit_by_slot(other_slot)

        try:
            self_unit.slot, other_unit.slot = other_unit.slot, self_unit.slot
        except AttributeError as err:
            print(f'Error: {err}')

        self.session.commit()  # Run the update query for update the record.

        # print(self_slot, other_slot)
        # new_slot = other_slot
        #
        # change_self_slot = update(
        #     self.PlayerUnits).where(
        #     self.PlayerUnits.slot == 1).values(
        #     slot=2).execution_options(
        #     synchronize_session="fetch")
        # self.session.execute(change_self_slot)
        # self.session.commit()

    def replace_unit(self, slot, new_name):
        """
        Метод замены юнита на другой юнит.
        Изменяет запись в таблице AllUnits.
        """
        self.delete_unit(slot)
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
            self.CurrentDungeon.desc,
            # self.AllUnits.photo,
            # self.AllUnits.gif,
            self.CurrentDungeon.slot
        ).filter_by(slot=slot)
        # Возвращаем кортеж
        return query.first()

    def get_dungeon_unit_by_id(self, _id):
        """Метод получающий юнита из базы подземелья по слоту."""
        query = self.session.query(
            self.CurrentDungeon.id,
            self.CurrentDungeon.name,
            self.CurrentDungeon.level,
            self.CurrentDungeon.size,
            self.CurrentDungeon.price,
            self.CurrentDungeon.exp,
            self.CurrentDungeon.curr_exp,
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
            self.CurrentDungeon.desc,
            # self.AllUnits.photo,
            # self.AllUnits.gif,
            self.CurrentDungeon.slot
        ).filter_by(id=_id)
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
            self.PlayerUnits.desc,
            # self.AllUnits.photo,
            # self.AllUnits.gif,
            self.PlayerUnits.slot
        ).order_by(self.PlayerUnits.slot)
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

main_db = ServerStorage('../disc2.db')
main_db.show_all_units()

# Отладка
if __name__ == '__main__':
    for item in main_db.show_all_units():
        print(item)
