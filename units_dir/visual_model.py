from collections import namedtuple
from typing import List, Callable

from client_dir.settings import BIG, GUARDS
from units_dir.buildings import FACTIONS
from units_dir.models import AllUnits, CurrentDungeon, Players, PlayerBuildings, GameSessions
from units_dir.units import main_db


class VisualModel:

    @property
    def difficulty(self) -> int:
        """Уровень сложности"""
        return main_db.difficulty

    @staticmethod
    def set_session_difficulty(difficulty):
        """Устанавливает выбранную сложность в БД"""
        main_db.update_session_difficulty(difficulty)

    @property
    def gold(self) -> int:
        """Метод получения количества золота у игрока."""
        return main_db.get_gold()

    @staticmethod
    def set_gold(gold: int) -> None:
        """Изменяет количество золота в БД."""
        main_db.set_gold(gold)

    @property
    def campaign_level(self) -> int:
        """Уровень кампании"""
        return main_db.campaign_level

    @staticmethod
    def set_campaign_level(campaign_level) -> None:
        """Установить уровень кампании в 1"""
        main_db.campaign_level = campaign_level

    @staticmethod
    def set_campaign_level_to_1() -> None:
        """Установить уровень кампании в 1"""
        main_db.campaign_level = 1

    @property
    def current_faction(self) -> str:
        """Текущая игровая фракция"""
        return main_db.current_faction

    @staticmethod
    def set_current_faction(faction_name: str) -> None:
        main_db.current_faction = faction_name

    @staticmethod
    def get_built() -> bool:
        """Получить флаг, строилось ли сегодня здание"""
        return main_db.already_built

    @staticmethod
    def set_built(built: bool) -> None:
        """Получить флаг, строилось ли сегодня здание"""
        main_db.already_built = built

    @staticmethod
    def set_built_to_0():
        """Устанавливает 0 в already_built"""
        main_db.already_built = 0

    @staticmethod
    def set_built_to_1():
        """Устанавливает 1 в already_built"""
        main_db.already_built = 1

    @staticmethod
    def create_buildings(player_name: str,
                         faction: str,
                         gold: int,
                         buildings: list) -> None:
        """
        Метод добавления здания 0 уровня в столице игрока.
        Создаёт запись в таблице PlayerBuildings.
        """
        unit_row = PlayerBuildings(
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
        main_db.create_buildings(unit_row)

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
            main_db.current_player.name,
            faction,
            1000,
            building_levels)

    @staticmethod
    def update_session_built() -> None:
        """Метод изменения флага постройки в текущей игровой сессии"""
        main_db.update_session_built()


    @staticmethod
    def get_unit_by_name(name: str) -> namedtuple:
        """Метод получающий юнита из БД по имени."""
        return main_db.get_unit_by_name(name)

    @staticmethod
    def get_unit_by_slot(slot: int, db_table: AllUnits) -> namedtuple:
        """Метод получающий юнита из переданной таблицы по слоту."""
        return main_db.get_unit_by_slot(slot, db_table)

    @staticmethod
    def get_unit_by_b_name(b_name: str) -> any:
        """Получение юнита по названию постройки"""
        return main_db.get_unit_by_b_name(b_name)

    @staticmethod
    def update_unit(unit_id: int,
                    params: dict,
                    db_table: any) -> None:
        """
        Метод изменения характеристик юнита игрока.
        Изменяет запись в переданной таблице БД.
        """
        main_db.update_unit(unit_id, params, db_table)

    @staticmethod
    def show_all_units() -> List[namedtuple]:
        """Метод возвращающий список всех юнитов из базы."""
        return main_db.show_all_units()

    @staticmethod
    def clear_units(faction: str) -> None:
        """Метод удаления юнитов в базе игрока за данную фракцию."""
        main_db.clear_units(faction)

    @staticmethod
    def set_unit_slot(new_slot: int,
                      unit: namedtuple,
                      db_table: AllUnits) -> None:
        """Установить новый номер слота юниту в БД"""
        main_db.set_unit_slot(new_slot, unit, db_table)

    @staticmethod
    def delete_unit_by_id(id_: int, db_table: any) -> None:
        """Метод удаляющий юнита из выбранной таблицы по слоту."""
        main_db.delete_unit_by_id(id_, db_table)

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

    def transfer_units(self) -> None:
        """Перенос юнитов из CurrentDungeon в запись versus"""
        names_list = []

        # Достаем из базы подземелий имена по слоту,
        # складываем в список
        for slot in range(1, 7):
            try:
                unit_name = self.get_unit_by_slot(
                    slot, CurrentDungeon).name
            except AttributeError:
                unit_name = None

            if unit_name is not None:
                names_list.append(unit_name)
            else:
                names_list.append('<null>')

        for _ in range(6):
            names_list.append('1')

        main_db.transfer_units(names_list)

    def update_db_table(self,
                        unit: any,
                        db_table: AllUnits,
                        new_db_table: AllUnits) -> None:
        """Обновление таблицы у юнита"""
        player_unit = new_db_table(*unit)
        main_db.update_db_table(player_unit)

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
                main_db.update_db_table(source_unit)

            if new_unit is not None \
                    and new_unit.name not in GUARDS:
                main_db.update_db_table(new_unit)

    def is_double(self, unit: namedtuple) -> bool:
        """Проверка размера юнита"""
        return self.get_unit_by_name(unit).size == BIG

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

    def hire_guard(self) -> None:
        """Метод добавления стража в БД столицы игрока."""
        db_table = self.get_res_db_table(self.current_faction)
        unit_row = self.get_unit_by_name(
            self.get_guards(self.current_faction))

        guard_unit = db_table(*unit_row)
        guard_unit.slot = 3

        main_db.hire_unit(guard_unit)

    def replace_unit(self,
                     slot: int,
                     new_name: str) -> None:
        """
        Метод замены юнита на другой юнит.
        Изменяет запись в переданной таблице.
        """
        self.delete_campaign_unit(slot)
        self.hire_unit(new_name, slot)

    def hire_unit_common(self,
                         unit_name: str,
                         slot: int,
                         db_table: any) -> None:
        """Метод добавления юнита в переданную таблицу."""
        if self.check_slot(
                unit_name,
                slot,
                self.get_unit_by_slot,
                db_table) is True:
            print('Данный слот занят')
        else:
            unit_row = self.get_unit_by_name(unit_name)
            if self.is_double(unit_row.name) and slot % 2 == 1:
                slot += 1

            unit = db_table(*unit_row)
            unit.slot = slot

            main_db.hire_unit(unit)

    def hire_unit(self, unit: str, slot: int) -> None:
        """
        Метод добавления юнита в таблицу игрока
        в зависимости от текущей фракции.
        """
        db_table = self.get_db_table(self.current_faction)
        self.hire_unit_common(unit, slot, db_table)

    def hire_enemy_unit(self, unit: str, slot: int) -> None:
        """Метод добавления юнита в таблицу противника CurrentDungeon."""
        self.hire_unit_common(unit, slot, CurrentDungeon)

    @staticmethod
    def update_perks(unit_id: int,
                     perks: dict,
                     db_table: AllUnits) -> None:
        """
        Метод изменения героя игрока (перки).
        Изменяет запись в переданной таблице БД.
        """
        main_db.update_perks(unit_id, perks, db_table)

    def update_unit_armor(self,
                          unit_id: int,
                          bonus: int,
                          db_table: AllUnits) -> None:
        """
        Метод изменения брони юнита игрока.
        Изменяет запись в переданной таблице БД.
        """
        unit = self.get_unit_by_id(unit_id, db_table)
        unit_armor = unit.armor + bonus

        main_db.update_unit_armor(unit_id, unit_armor, db_table)

    def update_unit_dmg(self,
                        unit_id: int,
                        bonus: int,
                        db_table: AllUnits) -> None:
        """
        Метод изменения урона юнита игрока.
        Изменяет запись в переданной таблице БД.
        """
        unit = self.get_unit_by_id(unit_id, db_table)
        unit_dmg = unit.attack_dmg + unit.attack_dmg * bonus

        main_db.update_unit_dmg(unit_id, unit_dmg, db_table)

    @staticmethod
    def update_unit_health(unit_id: int,
                           health: int,
                           db_table: AllUnits) -> None:
        """
        Метод изменения здоровья юнита игрока.
        Изменяет запись в переданной таблице БД.
        """
        main_db.update_unit_health(unit_id, health, db_table)

    @staticmethod
    def update_unit_ini(unit_id: int,
                        attack_ini: int,
                        db_table: AllUnits) -> None:
        """
        Метод изменения инициативы юнита игрока.
        Изменяет запись в переданной таблице БД.
        """
        main_db.update_unit_ini(unit_id, attack_ini, db_table)

    def update_ward(self,
                    unit_id: int,
                    element: str,
                    db_table: AllUnits) -> None:
        """
        Метод изменения варда юнита игрока.
        Изменяет запись в переданной таблице БД.
        """
        unit = self.get_unit_by_id(unit_id, db_table)
        if unit.ward != 'Нет':
            unit_ward = f'{unit.ward}, {element}'
        else:
            unit_ward = element

        main_db.update_ward(unit_id, unit_ward, db_table)

    @staticmethod
    def get_db_table(faction: str) -> any:
        """
        Метод получающий из БД таблицу основных
        юнитов игрока за определенную фракцию.
        """
        return main_db.campaigns_dict.get(faction)

    @staticmethod
    def get_res_db_table(faction: str) -> any:
        """
        Метод получающий из БД таблицу резервных (в столице)
        юнитов игрока за определенную фракцию.
        """
        return main_db.res_campaigns_dict[faction]

    @staticmethod
    def get_guards(faction) -> any:
        """
        Метод получающий из БД таблицу резервных (в столице)
        юнитов игрока за определенную фракцию.
        """
        return main_db.guards_dict.get(faction)

    @property
    def buildings(self) -> namedtuple:
        """Метод получения построек в столице игрока."""
        return main_db.get_buildings()

    @staticmethod
    def set_campaign_day(campaign_day: int) -> None:
        """Устанавливает день кампании"""
        main_db.campaign_day = campaign_day

    def increase_campaign_level(self):
        """Увеличивает уровень кампании"""
        main_db.campaign_level += 1
        main_db.increase_campaign_day()
        self.set_built_to_0()

        main_db.update_session(0, 0)

    def increase_campaign_mission(self,
                                  mission_number: int,
                                  curr_mission: int):
        """Переходит на следующую миссию кампании"""
        main_db.increase_campaign_day()
        self.set_built_to_0()

        main_db.update_session(mission_number,
                               curr_mission)

    @property
    def campaign_units(self) -> List[namedtuple]:
        """Метод возвращающий из БД список юнитов игрока в текущей кампании."""
        return main_db.show_campaign_units()

    @staticmethod
    def clear_buildings(player_name: str) -> None:
        """Метод удаления построек в ДБ столицы игрока."""
        main_db.clear_buildings(player_name)

    @staticmethod
    def update_buildings(player_name: str,
                         faction: str,
                         buildings: list) -> None:
        """Метод постройки здания в столице игрока (+ уровень)."""
        main_db.update_buildings(player_name,
                                 faction,
                                 buildings)

    @staticmethod
    def delete_dungeons() -> None:
        """Удаление подземелий из БД для данной фракции"""
        main_db.delete_dungeons()

    @staticmethod
    def show_all_players() -> List[namedtuple]:
        """Метод получения всех игроков."""
        return main_db.show_all_players()

    @staticmethod
    def create_player(name: str,
                      email: str) -> None:
        """
        Метод регистрации игрока в БД.
        Создаёт запись в таблице Players.
        """
        unit_row = Players(
            name,
            email
        )
        main_db.create_player(unit_row)

    @staticmethod
    def delete_player(name: str) -> None:
        """Метод удаляющий игрока из таблицы Players."""
        main_db.delete_player(name)

    def choose_player(self, player_name: str) -> None:
        """Метод выбора текущего игрока."""
        main_db.current_player = self.get_player(player_name)

    @staticmethod
    def get_player(player_name: str) -> namedtuple:
        """Метод получения записи конкретного игрока."""
        return main_db.get_player(player_name)

    @property
    def current_player(self) -> str:
        """Получение текущего игрока"""
        return main_db.current_player

    @property
    def current_player_name(self) -> str:
        """Получение имени текущего игрока"""
        return main_db.current_player.name

    @staticmethod
    def get_session_by_faction(faction: str) -> any:
        """Метод получающий игровую сессию по игроку и фракции."""
        return main_db.get_session_by_faction(faction)

    @staticmethod
    def set_session_for_faction_to_0(faction: str) -> None:
        """Метод обнуления текущей игровой сессии в БД"""
        game_session_row = GameSessions(
            main_db.current_player.id,
            faction,
            1,
            0,
            0,
            1,
            0,
            2)
        main_db.set_session_for_faction_to_0(game_session_row)

    @staticmethod
    def clear_session() -> None:
        """Метод удаления из БД предыдущей сессии игрока за данную фракцию."""
        main_db.clear_session()

    @staticmethod
    def set_game_session_id(_id):
        """Устанавливает ID данной игровой сессии"""
        main_db.game_session_id = _id

    def update_game_session(self) -> None:
        """Обновить игровую сессию"""
        curr_game_session = None

        if self.current_player is not None:
            curr_game_session = main_db.get_current_game_session(
                self.current_player.id)

        if curr_game_session is not None:
            self.set_current_faction(curr_game_session.faction)
            self.set_campaign_level(curr_game_session.campaign_level)
            self.set_campaign_day(curr_game_session.day)
            self.set_built(curr_game_session.built)
            self.set_game_session_id(curr_game_session.session_id)
            self.set_session_difficulty(curr_game_session.difficulty)
        else:
            self.set_current_faction('')
            self.set_campaign_level_to_1()
            self.set_campaign_day(1)
            self.set_built_to_0()
            self.set_session_difficulty(2)


    @staticmethod
    def get_unit_by_id(_id: int, db_table: AllUnits) -> namedtuple:
        """Метод получающий юнита из общей таблица юнитов по id."""
        return main_db.get_unit_by_id(_id, db_table)

    @staticmethod
    def delete_player_unit(slot: int, db_table: any) -> None:
        """Метод удаляющий юнита из выбранной таблицы БД по слоту."""
        main_db.delete_player_unit(slot, db_table)

    def delete_campaign_unit(self, slot: int) -> None:
        """Метод удаляющий юнита из выбранной таблицы БД по слоту."""
        db_table = self.get_db_table(self.current_faction)
        main_db.delete_player_unit(slot, db_table)

    @staticmethod
    def delete_dungeon_unit(slot: int) -> None:
        """Метод удаляющий юнита из выбранной таблицы БД по слоту."""
        main_db.delete_player_unit(slot, CurrentDungeon)

    def autoregen(self, slot: int) -> None:
        """
        Метод изменения юнита (здоровье).
        Изменяет запись в БД в переданной таблице.
        Автолечение после каждой битвы.
        """
        db_table = self.get_db_table(self.current_faction)
        main_db.autoregen(slot, db_table)

    @staticmethod
    def unit_by_name_set_params(unit: any,
                                name: str,
                                db_table: any) -> namedtuple:
        """
        Метод получающий юнита из таблицы всех юнитов по имени
        с новыми заданными параметрами и слотом.
        """
        return main_db.unit_by_name_set_params(unit, name, db_table)

    def update_unit_exp(self,
                        slot: int,
                        curr_exp: int) -> None:
        """
        Метод изменения здоровья юнита.
        Изменяет запись в переданной таблице БД.
        """
        db_table = self.get_db_table(self.current_faction)

        main_db.update_unit_exp(slot, curr_exp, db_table)

    @staticmethod
    def show_player_units() -> List[namedtuple]:
        """Метод возвращающий список юнитов игрока."""
        return main_db.show_player_units()

    @staticmethod
    def show_enemy_units() -> List[namedtuple]:
        """Метод возвращающий список юнитов противника."""
        return main_db.show_enemy_units()

    @staticmethod
    def show_dungeon_units(dung_name: str) -> namedtuple:
        """
        Метод возвращающий из БД список имен и уровней юнитов
        по названию подземелья.
        """
        return main_db.show_dungeon_units(dung_name)

    @staticmethod
    def add_dungeon_unit(unit: namedtuple) -> None:
        """
        Метод регистрации юнита противника.
        Создаёт запись в БД.
        """
        main_db.add_dungeon_unit(unit)

    @staticmethod
    def add_dungeons(dungeons: dict, campaign_level: int) -> None:
        """Добавление подземелий в БД"""
        main_db.add_dungeons(dungeons, campaign_level)

    @staticmethod
    def get_fighter_branch() -> list:
        """Метод получения построек ветви бойцов в столице игрока."""
        return main_db.get_fighter_branch()

    @staticmethod
    def get_mage_branch() -> list:
        """Метод получения построек ветви магов в столице игрока."""
        return main_db.get_mage_branch()

    @staticmethod
    def get_archer_branch() -> list:
        """Метод получения построек ветви стрелков в столице игрока."""
        return main_db.get_archer_branch()

    @staticmethod
    def get_support_branch() -> list:
        """Метод получения построек ветви поддержки в столице игрока."""
        return main_db.get_support_branch()


v_model = VisualModel()
