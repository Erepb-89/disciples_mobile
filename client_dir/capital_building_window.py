"""Окно постройки в столице"""

import os.path

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.capital_building_form import Ui_CapitalBuildingWindow
from client_dir.settings import CAPITAL_BUILDING, UNIT_ICONS, \
    TOWN_ICONS, UNIT_FACES, PLUG, ELVEN_PLUG, SCREEN_RECT
from client_dir.ui_functions import set_size_by_unit, get_unit_image, slot_frame_update
from client_dir.unit_dialog import UnitDialog
from units_dir.buildings import FACTIONS, BRANCHES


class CapitalBuildingWindow(QMainWindow):
    """
    Класс - окно выбора фракции.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла capital_building_form.py
    """

    def __init__(self, database):
        super().__init__()
        # основные переменные
        self.database = database
        self.faction = self.database.current_game_faction
        self.branch = 'archer'
        self.branch_settings = self.get_branch_settings()
        self.building = self.branch_settings[1][0]
        self.building_name = ''
        self.building_cost = 0
        self.unit = self.get_unit_by_b_slot(1)

        self.InitUI()

        self.get_all_branch_units(self.branch_settings)
        self.slot_update(self.unit, self.ui.slot)
        self.button_update(self.unit, self.ui.pushButtonSlot)
        self.player_gold = self.database.get_gold(
            self.database.current_user, self.faction)
        self.ui.gold.setText(str(self.player_gold))

    def InitUI(self):
        # Загружаем конфигурацию окна из дизайнера
        self.ui = Ui_CapitalBuildingWindow()
        self.ui.setupUi(self)

        self.hbox = QHBoxLayout(self)

        self.update_capital()
        self.ui.pushButtonBack.clicked.connect(self.back)
        self.ui.pushButtonSlot.clicked.connect(self.slot_detailed)
        self.ui.pushButtonFighters.clicked.connect(
            self.change_branch_fighters)
        self.ui.pushButtonMages.clicked.connect(
            self.change_branch_mages)
        self.ui.pushButtonArchers.clicked.connect(
            self.change_branch_archers)
        self.ui.pushButtonSupport.clicked.connect(
            self.change_branch_support)
        self.ui.pushButtonOthers.clicked.connect(
            self.change_branch_others)

        self.ui.pushButtonSlot_1.clicked.connect(
            self.update_unit_by_b_slot1)
        self.ui.pushButtonSlot_2.clicked.connect(
            self.update_unit_by_b_slot2)
        self.ui.pushButtonSlot_3.clicked.connect(
            self.update_unit_by_b_slot3)
        self.ui.pushButtonSlot_4.clicked.connect(
            self.update_unit_by_b_slot4)
        self.ui.pushButtonSlot_5.clicked.connect(
            self.update_unit_by_b_slot5)
        self.ui.pushButtonSlot_6.clicked.connect(
            self.update_unit_by_b_slot6)
        self.ui.pushButtonSlot_7.clicked.connect(
            self.update_unit_by_b_slot7)
        self.ui.pushButtonSlot_8.clicked.connect(
            self.update_unit_by_b_slot8)
        self.ui.pushButtonSlot_9.clicked.connect(
            self.update_unit_by_b_slot9)

        # self.ui.pushButtonReverse.clicked.connect(self.reverse_icons)
        self.ui.pushButtonBuy.clicked.connect(self.buy_building)

        self.town_icons_dict = {
            1: self.ui.slot_1,
            2: self.ui.slot_2,
            3: self.ui.slot_3,
            4: self.ui.slot_4,
            5: self.ui.slot_5,
            6: self.ui.slot_6,
            7: self.ui.slot_7,
            8: self.ui.slot_8,
            9: self.ui.slot_9,
        }

        self.icon_buttons_dict = {
            1: self.ui.pushButtonSlot_1,
            2: self.ui.pushButtonSlot_2,
            3: self.ui.pushButtonSlot_3,
            4: self.ui.pushButtonSlot_4,
            5: self.ui.pushButtonSlot_5,
            6: self.ui.pushButtonSlot_6,
            7: self.ui.pushButtonSlot_7,
            8: self.ui.pushButtonSlot_8,
            9: self.ui.pushButtonSlot_9,
        }

        self.highlight_selected_building(1, self.ui.labelSelected1)
        # Обновление рамки слота юнита
        slot_frame_update(self.unit, self.ui.slotFrame1)
        self.show()

    def update_capital(self):
        """Обновление картинки замка (фон)"""
        capital_building_bg = self.ui.capitalBuildingBG
        capital_building_bg.setPixmap(
            QPixmap(self.get_image(self.faction))
        )
        capital_building_bg.setGeometry(SCREEN_RECT)
        self.hbox.addWidget(capital_building_bg)
        self.setLayout(self.hbox)

    def get_image(self, faction):
        """Достаем картинку строительства текущей фракции"""
        try:
            return os.path.join(
                CAPITAL_BUILDING,
                f"{self.branch}/{faction}.png")
        except BaseException:
            return os.path.join(CAPITAL_BUILDING, ELVEN_PLUG)

    def back(self):
        """Кнопка возврата"""
        self.close()

    def change_branch(self, branch):
        """Смена ветви"""
        self.branch = branch
        self.update_capital()
        self.unit = self.get_unit_by_b_slot(1)
        self.slot_update(self.unit, self.ui.slot)
        self.button_update(self.unit, self.ui.pushButtonSlot)
        self.ui.pushButtonSlot.setEnabled(True)
        self.branch_settings = self.get_branch_settings()

        # Получение всех юнитов ветви
        self.get_all_branch_units(self.branch_settings)

        # Получение параметров постройки
        self.get_building_params(1)

        # получаем картинку здания по слоту
        for num, icon_slot in self.town_icons_dict.items():
            self.get_building_by_slot(num, icon_slot)

        # обновление рамки под слот юнита
        slot_frame_update(self.unit, self.ui.slotFrame1)

        # Подсветка выбранной постройки
        self.highlight_selected_building(1, self.ui.labelSelected1)

    def change_branch_fighters(self):
        """Смена ветви на fighter"""
        self.change_branch('fighter')

    def change_branch_mages(self):
        """Смена ветви на mage"""
        self.change_branch('mage')

    def change_branch_archers(self):
        """Смена ветви на archer"""
        self.change_branch('archer')

    def change_branch_support(self):
        """Смена ветви на support"""
        self.change_branch('support')

    def change_branch_others(self):
        """Смена ветви на others"""
        self.branch = 'others'
        self.update_capital()

        self.unit = None
        self.ui.slot.setFixedSize(0, 0)
        self.ui.slotFrame1.setFixedSize(0, 0)
        self.ui.pushButtonSlot.setEnabled(False)

        self.branch_settings = self.get_branch_settings()

        # получаем координаты кнопок
        for num, icon_button in self.icon_buttons_dict.items():
            icon_button.setGeometry(*self.get_coords(num))

        # получаем картинку здания по слоту
        for num, icon_slot in self.town_icons_dict.items():
            self.get_building_by_slot(num, icon_slot)

        self.get_building_params(1)
        self.highlight_selected_building(1, self.ui.labelSelected1)

    def get_branch_settings(self):
        """Получение настроек ветви"""
        return FACTIONS.get(self.faction)[self.branch]

    def get_all_branch_units(self, branch):
        """Получение всех юнитов ветви"""
        # получаем юнита по слоту здания
        for b_slot, building in branch.items():
            self.get_unit_by_b_slot(b_slot)
            self.building = building

        # получаем картинку здания по слоту
        for num, icon_slot in self.town_icons_dict.items():
            self.get_building_by_slot(num, icon_slot)

        # получаем координаты кнопок
        for num, icon_button in self.icon_buttons_dict.items():
            icon_button.setGeometry(*self.get_coords(num))

    def get_building_by_slot(self, num, icon_slot):
        """
        Получение картинки здания по слоту.
        Задание координат
        """
        icon_slot.setPixmap(QPixmap(
            self.get_icon_image(num)).scaled(
            icon_slot.width(), icon_slot.height())
        )
        icon_slot.setGeometry(*self.get_coords(num))

    def get_coords(self, num):
        """Получение координат"""
        try:
            coords = self.branch_settings[num].coords
            return coords
        except BaseException:
            return [0, 0, 0, 0]

    def get_building_params(self, b_slot):
        """Получение параметров постройки"""
        self.building_name = self.branch_settings[b_slot].bname
        self.building_cost = self.branch_settings[b_slot].cost

        # Установка названия постройки, стоимости
        self.ui.buildingName.setText(
            str(f'{self.building_name} ({self.building_cost})'))

        # Установка имени юнита, соответствующего постройке
        self.ui.nextLevel.setText(
            str(f'{self.branch_settings[b_slot].unit_name}'))
        if b_slot != 1:
            self.ui.prevLevel.setText(
                str(f'{self.branch_settings[b_slot - 1].unit_name}'))

    # def get_unit_press(self, num):
    #     try:
    #         self.unit = self.get_unit_by_b_slot(num)
    #         self.slot_update(self.unit, self.ui.slot)
    #     except Exception as err:
    #         print(err)

    def unlight_all_buildings(self):
        """Снятие подсветки зданий"""
        self.ui.labelSelected1.setLineWidth(0)
        self.ui.labelSelected1.setStyleSheet("border: 0px;")

    def highlight_selected_building(self, num, ui_slot):
        """Подсветка выбранной постройки"""
        ui_slot.setGeometry(*self.get_coords(num))
        ui_slot.setLineWidth(5)
        ui_slot.setStyleSheet("border: 5px solid yellow;")

    def get_unit_by_b_slot(self, b_slot):
        """Получение юнита по слоту постройки"""
        unit = self.database.get_unit_by_name(
            self.get_branch_settings()[b_slot].unit_name)

        return unit

    def update_unit_by_b_slot(self, b_slot):
        """Обновление юнита согласно выбранному зданию"""
        self.unit = self.get_unit_by_b_slot(b_slot)
        self.slot_update(self.unit, self.ui.slot)
        self.button_update(self.unit, self.ui.pushButtonSlot)
        self.get_building_params(b_slot)

        # подсветка выбранного здания
        self.highlight_selected_building(b_slot, self.ui.labelSelected1)

    def update_unit_by_b_slot1(self):
        """Обновление юнита согласно зданию 1"""
        self.update_unit_by_b_slot(1)

    def update_unit_by_b_slot2(self):
        """Обновление юнита согласно зданию 2"""
        self.update_unit_by_b_slot(2)

    def update_unit_by_b_slot3(self):
        """Обновление юнита согласно зданию 3"""
        self.update_unit_by_b_slot(3)

    def update_unit_by_b_slot4(self):
        """Обновление юнита согласно зданию 4"""
        self.update_unit_by_b_slot(4)

    def update_unit_by_b_slot5(self):
        """Обновление юнита согласно зданию 5"""
        self.update_unit_by_b_slot(5)

    def update_unit_by_b_slot6(self):
        """Обновление юнита согласно зданию 6"""
        self.update_unit_by_b_slot(6)

    def update_unit_by_b_slot7(self):
        """Обновление юнита согласно зданию 7"""
        self.update_unit_by_b_slot(7)

    def update_unit_by_b_slot8(self):
        """Обновление юнита согласно зданию 8"""
        self.update_unit_by_b_slot(8)

    def update_unit_by_b_slot9(self):
        """Обновление юнита согласно зданию 9"""
        self.update_unit_by_b_slot(9)

    def slot_update(self, unit, slot):
        """Обновление слота юнита"""
        set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            get_unit_image(unit)).scaled(
            slot.width(), slot.height()))
        self.hbox.addWidget(slot)
        self.setLayout(self.hbox)

    def building_face_update(self, unit, slot):
        """Обновление лица юнита соответствующего постройке"""
        slot.setPixmap(QPixmap(
            self.get_unit_face(unit)).scaled(
            slot.width(), slot.height()))
        self.hbox.addWidget(slot)
        self.setLayout(self.hbox)

    def button_update(self, unit, button):
        """Обновление кнопки"""
        set_size_by_unit(unit, button)

        self.hbox.addWidget(button)
        self.setLayout(self.hbox)

    def reverse_icons(self):
        """Смена картинки постройки на лицо юнита"""
        for num, icon_slot in self.town_icons_dict.items():
            try:
                unit = self.get_unit_by_b_slot(num)
                self.building_face_update(unit, icon_slot)
                self.set_size_by_slot(icon_slot)
            except BaseException:
                pass

    def buy_building(self):
        """Метод постройки зданий в столице"""
        changed_buildings = list(
            self.database.get_buildings(
                self.database.current_user,
                self.faction))

        # обновление построек в текущей сессии
        changed_buildings[BRANCHES[self.branch]] = self.building_name
        self.database.update_buildings(
            self.database.current_user,
            self.faction,
            changed_buildings)
        print(self.building_name, self.building_cost)

        changed_gold = self.player_gold - self.building_cost

        # обновление золота в базе
        self.database.update_gold(
            self.database.current_user,
            self.faction,
            changed_gold)
        self.ui.gold.setText(str(changed_gold))

    def slot_detailed(self):
        """Метод создающий окно юнита (слот)."""
        try:
            global DETAIL_WINDOW
            DETAIL_WINDOW = UnitDialog(
                self.database,
                self.unit)
            DETAIL_WINDOW.show()
        except Exception as err:
            print(err)

    @staticmethod
    def get_unit_face(unit):
        """Получение лица юнита"""
        try:
            return os.path.join(UNIT_FACES, f"{unit.name}.png")
        except BaseException:
            return os.path.join(
                UNIT_ICONS, PLUG)

    def get_icon_image(self, num):
        """Получение картинки построенного здания"""
        icon_path = f"{self.faction}/{self.branch}/{num}.png"
        try:
            return os.path.join(TOWN_ICONS, icon_path)
        except BaseException:
            return os.path.join(
                UNIT_ICONS, PLUG)

    @staticmethod
    def set_size_by_slot(ui_obj):
        """Установка размеров картинки по слоту здания"""
        ui_obj.setFixedWidth(118)
        ui_obj.setFixedHeight(114)
