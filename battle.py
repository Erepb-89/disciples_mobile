"""Battle"""
import operator
import random


class Battle:
    """Класс битвы"""

    def __init__(self, database):
        # super().__init__()
        # основные переменные
        self.database = database
        self.autofight = False
        self.units_deque = None
        self.target_slot = None
        self.current_target = 0
        self.player_slots = []
        self.player_ids = []
        self.enemy_slots = []
        self.enemy_ids = []
        self.current_faction = self.database.current_game_faction()

        self.player_unit_1 = self.database.get_unit_by_slot(1)
        self.player_unit_2 = self.database.get_unit_by_slot(2)
        self.player_unit_3 = self.database.get_unit_by_slot(3)
        self.player_unit_4 = self.database.get_unit_by_slot(4)
        self.player_unit_5 = self.database.get_unit_by_slot(5)
        self.player_unit_6 = self.database.get_unit_by_slot(6)

        self.dungeon_units = self.database.show_dungeon_units('darkest')
        # self.dungeon_units = self.database.show_dungeon_units('mirror')

        self.add_dung_units()

        # self.unit_1 = self.database.get_unit_by_id(self.dungeon_units[0])

        # self.database.add_unit(*self.unit_1[:18], 1, 0)

        self.enemy_unit_1 = self.database.get_dungeon_unit_by_slot(1)
        self.enemy_unit_2 = self.database.get_dungeon_unit_by_slot(2)
        self.enemy_unit_3 = self.database.get_dungeon_unit_by_slot(3)
        self.enemy_unit_4 = self.database.get_dungeon_unit_by_slot(4)
        self.enemy_unit_5 = self.database.get_dungeon_unit_by_slot(5)
        self.enemy_unit_6 = self.database.get_dungeon_unit_by_slot(6)

        # self.enemy_unit_1 = self.database.get_unit_by_id(self.dungeon_units[0])

        self.player_units = [
            self.player_unit_1,
            self.player_unit_2,
            self.player_unit_3,
            self.player_unit_4,
            self.player_unit_5,
            self.player_unit_6
        ]

        for unit in self.player_units:
            if unit is not None and unit.curr_health != 0:
                self.player_slots.append(unit.slot)
                self.player_ids.append(unit.id)

        self.enemy_units = [
            self.enemy_unit_1,
            self.enemy_unit_2,
            self.enemy_unit_3,
            self.enemy_unit_4,
            self.enemy_unit_5,
            self.enemy_unit_6
        ]

        for unit in self.enemy_units:
            if unit is not None and unit.curr_health != 0:
                self.enemy_slots.append(unit.slot)
                self.enemy_ids.append(unit.id)

        self.new_round()

    def add_dung_units(self):
        self.clear_dungeon()
        for unit_slot in range(6):
            try:
                self.database.add_unit(
                    *self.database.get_unit_by_id(
                        self.dungeon_units[unit_slot])[:22], unit_slot + 1)
            except Exception as err:
                print(err)

    def enemy_unit_by_slot(self, slot):
        return self.database.get_dungeon_unit_by_slot(slot)

    def player_unit_by_slot(self, slot):
        return self.database.get_unit_by_slot(slot)

    def new_round(self):
        # unsorted_units_ini = []
        unsorted_units_ini = {}
        all_units = self.player_units + self.enemy_units
        # all_units_ids = self.player_ids + self.enemy_ids

        # for unit in all_units:
        #     try:
        #         if unit is not None and unit.curr_health != 0:
        #             unsorted_units_ini.append(unit)
        #     except:
        #         pass

        for unit in all_units:
            try:
                if unit is not None and unit.curr_health != 0:
                    unsorted_units_ini[unit.id] = unit.attack_ini
            except:
                pass

        sorted_units_by_ini = sorted(unsorted_units_ini.items(), key=operator.itemgetter(1))

        self.units_dict = {k: v for k, v in sorted_units_by_ini}

    def attack(self, unit):
        print('ходит:', unit.name)
        self.target_slot = self.auto_choose_target(unit)
        print('target_slot:', self.target_slot)

        try:
            if unit.id in self.player_ids:
                target = self.enemy_unit_by_slot(self.target_slot)
                target_hp = target.curr_health
                try:
                    damage = int(unit.attack_dmg.split('/')[0]) + random.randrange(5)
                except:
                    damage = int(unit.attack_dmg) + random.randrange(5)
                # self.current_target = self.database.get_dungeon_unit_by_slot(self.target_slot)
                self.current_target_id = self.database.get_dungeon_unit_by_slot(self.target_slot).id
                target_hp -= damage
                if target_hp < 0:
                    target_hp = 0
                    # self.units_deque.remove(self.current_target)
                    self.units_dict.pop(self.current_target_id)
                    self.enemy_slots.remove(self.target_slot)
                    self.enemy_ids.remove(target.id)
                    if self.enemy_slots == []:
                        print('You won!')
                self.database.update_dungeon_unit(self.target_slot, target_hp)

                print(f"{unit.name} наносит урон {damage} воину "
                      f"{self.enemy_unit_by_slot(self.target_slot).name} осталось ХП: {target_hp}")

            elif unit.id in self.enemy_ids:
                target = self.player_unit_by_slot(self.target_slot)
                target_hp = target.curr_health
                try:
                    damage = int(unit.attack_dmg.split('/')[0]) + random.randrange(5)
                except:
                    damage = int(unit.attack_dmg) + random.randrange(5)
                self.current_target = self.database.get_unit_by_slot(self.target_slot)
                self.current_target_id = self.database.get_unit_by_slot(self.target_slot).id
                target_hp -= damage
                if target_hp < 0:
                    target_hp = 0
                    # self.units_deque.remove(self.current_target)
                    self.units_dict.pop(self.current_target_id)
                    self.player_slots.remove(self.target_slot)
                    self.player_ids.remove(target.id)
                    if self.player_slots == []:
                        print('You lose!')
                self.database.update_player_unit(self.target_slot, target_hp)

                print(f"{unit.name} наносит урон {damage} воину "
                      f"{self.player_unit_by_slot(self.target_slot).name} осталось ХП: {target_hp}")

        except AttributeError as err:
            print(err)

    def auto_fight(self):
        self.autofight = True
        # if self.units_deque:
        if self.units_dict:
            # self.current_unit = self.units_deque.popleft()
            # print(self.units_dict.popitem())
            self.current_unit = self.database.get_dungeon_unit_by_id(self.units_dict.popitem()[0])
            self.attack(self.current_unit)
            print()
            # for item in self.units_deque:
            for item in self.units_dict:
                print(item)

        # self.units_deque.append(self.current_unit)
        else:
            self.new_round()

    def clear_dungeon(self):
        self.database.delete_dungeon_unit(1)
        self.database.delete_dungeon_unit(2)
        self.database.delete_dungeon_unit(3)
        self.database.delete_dungeon_unit(4)
        self.database.delete_dungeon_unit(5)
        self.database.delete_dungeon_unit(6)

    def regen(self):
        self.database.autoregen(1)
        self.database.autoregen(2)
        self.database.autoregen(3)
        self.database.autoregen(4)
        self.database.autoregen(5)
        self.database.autoregen(6)

    # def priority_target(self, unit):

    def define_closest_slot(self, unit, target_slots):
        if unit.slot == 2:
            if 2 in target_slots and 4 in target_slots:
                return [2, 4]
            elif 2 in target_slots:
                return [2, ]
            elif 4 in target_slots:
                return [4, ]
            elif 2 not in target_slots and 4 not in target_slots and 6 in target_slots:
                return [6, ]
            elif 2 not in target_slots and 4 not in target_slots and 6 not in target_slots:
                if 1 in target_slots and 3 in target_slots:
                    return [1, 3]
                elif 1 in target_slots:
                    return [1, ]
                elif 3 in target_slots:
                    return [3, ]
                elif 1 not in target_slots and 3 not in target_slots and 5 in target_slots:
                    return [5, ]

        elif unit.slot == 4:
            if 2 in target_slots and 4 in target_slots and 6 in target_slots:
                return [2, 4, 6]
            elif 2 in target_slots:
                return [2, ]
            elif 4 in target_slots:
                return [4, ]
            elif 6 in target_slots:
                return [6, ]
            elif 2 not in target_slots and 4 not in target_slots and 6 not in target_slots:
                if 1 in target_slots and 3 in target_slots and 5 in target_slots:
                    return [1, 3, 5]
                elif 1 in target_slots:
                    return [1, ]
                elif 3 in target_slots:
                    return [3, ]
                elif 5 in target_slots:
                    return [5, ]

        elif unit.slot == 6:
            if 6 in target_slots and 4 in target_slots:
                return [6, 4]
            elif 6 in target_slots:
                return [6, ]
            elif 4 in target_slots:
                return [4, ]
            elif 2 not in target_slots and 4 not in target_slots and 2 in target_slots:
                return [2, ]
            elif 2 not in target_slots and 4 not in target_slots and 6 not in target_slots:
                if 5 in target_slots and 3 in target_slots:
                    return [5, 3]
                elif 5 in target_slots:
                    return [5, ]
                elif 3 in target_slots:
                    return [3, ]
                elif 5 not in target_slots and 3 not in target_slots and 1 in target_slots:
                    return [1, ]

    def auto_choose_target(self, unit):
        print('enemy_slots', self.enemy_slots)
        print('player_slots', self.player_slots)
        print('enemy_ids', self.enemy_ids)
        print('player_ids', self.player_ids)
        if unit in self.player_units:
            if unit.attack_radius == 'Ближайший юнит':
                target = random.choice(self.define_closest_slot(unit, self.enemy_slots))
                print(target)
                return target
            elif unit.attack_radius == 'Любой юнит':
                target = random.choice(self.enemy_slots)
                return target
        elif unit in self.enemy_units:
            if unit.attack_radius == 'Ближайший юнит':
                target = random.choice(self.define_closest_slot(unit, self.player_slots))
                print(target)
                return target
            elif unit.attack_radius == 'Любой юнит':
                target = random.choice(self.player_slots)
                return target
