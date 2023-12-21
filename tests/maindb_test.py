from unittest import TestCase, main

from units_dir.units import main_db


class MainDBTest(TestCase):

    def test_get_unit_by_name(self):
        self.assertEqual(main_db.get_unit_by_name('Антипаладин').desc,
                         'Демоны овладели душой этого некогда святого воина, их добродетельное прошлое было забыто.')

        self.assertIsNone(main_db.get_unit_by_name('Кадабра'), None)

    def test_get_unit_by_id(self):
        self.assertEqual(main_db.get_unit_by_id(1, main_db.AllUnits).name, 'Адепт')

    def test_get_units_by_level(self):
        units = main_db.get_units_by_level(8)
        for unit in units:
            self.assertEqual('Ашган', unit.name)

    # def test_get_unit_by_slot(self):
    #     unit = main_db.get_unit_by_slot(1, main_db.PlayerUnits)
    #     self.assertEqual('Ашган', unit.name)


if __name__ == '__main__':
    main()
