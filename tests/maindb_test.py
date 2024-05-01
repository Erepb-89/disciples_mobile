from unittest import TestCase, main

from units_dir.models import PlayerUnits, CurrentDungeon, AllUnits
from units_dir.units import main_db


class MainDBTest(TestCase):

    def test_get_unit_by_name(self):
        self.assertEqual(
            main_db.get_unit_by_name('Антипаладин').desc,
            'Демоны овладели душой этого некогда святого воина, '
            'их добродетельное прошлое было забыто.')

        self.assertIsNone(main_db.get_unit_by_name('Кадабра'), None)

    def test_get_unit_by_id(self):
        self.assertEqual(
            main_db.get_unit_by_id(
                1, AllUnits).name, 'Адепт')

    def test_get_unit_by_slot(self):
        unit = main_db.get_unit_by_slot(2, PlayerUnits)
        self.assertIsNone(unit)

    def test_is_double(self):
        self.assertEqual(main_db.is_double('Горный гигант'), True)

        self.assertIsNot(main_db.is_double('Сквайр'), True)

    def test_check_slot(self):
        self.assertEqual(main_db.check_slot('Лучник',
                                            2,
                                            main_db.get_unit_by_slot,
                                            PlayerUnits),
                         True)

        self.assertEqual(main_db.check_slot('Горный гигант',
                                            1,
                                            main_db.get_unit_by_slot,
                                            PlayerUnits),
                         True)

        self.assertEqual(main_db.check_slot('Стрелок',
                                            2,
                                            main_db.get_unit_by_slot,
                                            CurrentDungeon),
                         True)

    def test_hire_unit(self):
        main_db.hire_player_unit('Антипаладин', 2)
        self.assertEqual(main_db.get_unit_by_slot(2, PlayerUnits).name,
                         'Антипаладин')

        main_db.hire_enemy_unit('Сквайр', 2)
        self.assertEqual(
            main_db.get_unit_by_slot(
                2,
                CurrentDungeon).name,
            'Сквайр')

    def test_show_enemy_units(self):
        units = main_db.show_enemy_units()
        self.assertEqual(units[0].name, 'Сквайр')

    def test_replace_unit(self):
        main_db.replace_unit(2, 'Адский рыцарь', PlayerUnits)
        self.assertEqual(main_db.get_unit_by_slot(2, PlayerUnits).name,
                         'Адский рыцарь')

    def test_show_player_units(self):
        units = main_db.show_player_units()
        self.assertEqual(units[0].name, 'Адский рыцарь')

    def test_delete_player_unit(self):
        main_db.delete_player_unit(2)
        self.assertIsNone(main_db.get_unit_by_slot(2, PlayerUnits))

    def test_delete_dungeon_unit(self):
        main_db.delete_dungeon_unit(2)
        self.assertIsNone(main_db.get_unit_by_slot(2, CurrentDungeon))


if __name__ == '__main__':
    main()
