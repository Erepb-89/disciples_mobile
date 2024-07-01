"""Окно постройки в столице"""

import os.path

# import pymorphy2
from collections import namedtuple
from typing import Optional, List

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout

from client_dir.forms.capital_building_form import Ui_CapitalBuildingWindow
from client_dir.windows.question_window import QuestionWindow
from client_dir.settings import CAPITAL_BUILDING, UNIT_ICONS, TOWN_ICONS, \
    SCREEN_RECT, DECLINATIONS, INTERF, ICON, COMMON, OTHERS, ALREADY_BUILT, \
    READY_TO_BUILD, NEED_TO_BUILD_PREV, ANOTHER_BRANCH, NOT_ENOUGH_GOLD, \
    SPECIAL_BUILDINGS
from client_dir.ui_functions import set_size_by_unit, get_unit_image, \
    slot_frame_update, ui_lock, ui_unlock
from client_dir.dialogs.unit_dialog import UnitDialog
from units_dir.buildings import FACTIONS, BRANCHES
from units_dir.ranking import STARTING_FORMS
from units_dir.units import main_db


class CapitalBuildingWindow(QMainWindow):
    """
    Класс - окно стройки в столице.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла capital_building_form.py
    """

    def __init__(self):
        super().__init__()
        # основные переменные
        self.question = False  # Постройка зданий
        self.faction = main_db.current_faction
        self.branch = 'archer'
        self.building_name = ''
        self.building_cost = 0
        self.unit = self.get_unit_by_b_slot(1)
        self.graph = []
        # self.morph = pymorphy2.MorphAnalyzer()
        self.icons = True

        self.InitUI()

        self.show_all_branch_icons()
        self.slot_update(self.unit, self.ui.slot)
        self.button_update(self.unit, self.ui.pushButtonSlot)
        self.player_gold = main_db.get_gold(
            main_db.current_player.name, self.faction)
        self.ui.gold.setText(str(self.player_gold))

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""
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
        self.ui.pushButtonSlot_10.clicked.connect(
            self.update_unit_by_b_slot10)

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
            10: self.ui.slot_10,
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
            10: self.ui.pushButtonSlot_10,
        }

        self.builded_dict = {
            1: self.ui.slotBuilded_1,
            2: self.ui.slotBuilded_2,
            3: self.ui.slotBuilded_3,
            4: self.ui.slotBuilded_4,
            5: self.ui.slotBuilded_5,
            6: self.ui.slotBuilded_6,
            7: self.ui.slotBuilded_7,
            8: self.ui.slotBuilded_8,
            9: self.ui.slotBuilded_9,
            10: self.ui.slotBuilded_10,
        }

        self.highlight_selected_building(1, self.ui.labelSelected1)
        self.ui.slotReverse.setPixmap(
            QPixmap(
                os.path.join(
                    COMMON,
                    'reverse.png')))

        # Обновление рамки слота юнита
        slot_frame_update(self.unit, self.ui.slotFrame1)
        self.get_building_params(1)
        self.show_already_built()

        self.ui.pushButtonReverse.clicked.connect(self.reverse_icons)
        self.ui.pushButtonBuy.clicked.connect(self.buy_building)
        self.show()

    def update_capital(self) -> None:
        """Обновление картинки замка (фон)"""
        capital_building_bg = self.ui.capitalBuildingBG
        capital_building_bg.setPixmap(
            QPixmap(self.get_image(self.faction))
        )
        capital_building_bg.setGeometry(SCREEN_RECT)
        self.hbox.addWidget(capital_building_bg)
        self.setLayout(self.hbox)

    def get_image(self, faction: str) -> str:
        """Достаем картинку строительства текущей фракции"""
        return os.path.join(
            CAPITAL_BUILDING,
            f"{self.branch}/{faction}.png")

    def back(self) -> None:
        """Кнопка возврата"""
        self.close()

    def change_branch(self, branch: str) -> None:
        """Смена ветви"""
        self.branch = branch
        self.update_capital()
        self.unit = self.get_unit_by_b_slot(1)
        self.slot_update(self.unit, self.ui.slot)
        self.button_update(self.unit, self.ui.pushButtonSlot)
        ui_unlock(self.ui.pushButtonSlot)

        # Прорисовка всех иконок и кнопок ветви
        self.show_all_branch_icons()

        # Получение параметров постройки
        self.get_building_params(1)

        # получаем картинку здания по слоту
        for num, icon_slot in self.town_icons_dict.items():
            self.get_icon_by_slot(num, icon_slot)

        # обновление рамки под слот юнита
        slot_frame_update(self.unit, self.ui.slotFrame1)

        # Подсветка выбранной постройки
        self.highlight_selected_building(1, self.ui.labelSelected1)
        self.show_already_built()
        self.reverse_update()
        self.icons = True

    def change_branch_fighters(self) -> None:
        """Смена ветви на fighter"""
        self.change_branch('fighter')

    def change_branch_mages(self) -> None:
        """Смена ветви на mage"""
        self.change_branch('mage')

    def change_branch_archers(self) -> None:
        """Смена ветви на archer"""
        self.change_branch('archer')

    def change_branch_support(self) -> None:
        """Смена ветви на support"""
        self.change_branch('support')

    def change_branch_others(self) -> None:
        """Смена ветви на others"""
        self.branch = OTHERS
        self.update_capital()

        self.unit = None
        self.ui.slot.setFixedSize(0, 0)
        self.ui.slotFrame1.setFixedSize(0, 0)
        ui_lock(self.ui.pushButtonSlot)

        # получаем координаты кнопок
        for num, icon_button in self.icon_buttons_dict.items():
            icon_button.setGeometry(*self.get_coords(num))

        # получаем картинку здания по слоту
        for num, icon_slot in self.town_icons_dict.items():
            self.get_icon_by_slot(num, icon_slot)

        self.get_building_params(1)
        self.highlight_selected_building(1, self.ui.labelSelected1)
        self.show_already_built()
        self.reverse_update()

    @property
    def branch_settings(self) -> dict:
        """Получение настроек ветви"""
        return FACTIONS.get(self.faction)[self.branch]

    def show_all_branch_icons(self) -> None:
        """Прорисовка всех иконок и кнопок ветви"""
        # прорисовка картинок зданий по слоту
        for num, icon_slot in self.town_icons_dict.items():
            self.get_icon_by_slot(num, icon_slot)

        # установка координат кнопок
        for num, icon_button in self.icon_buttons_dict.items():
            icon_button.setGeometry(*self.get_coords(num))

    def get_icon_by_slot(self,
                         num: int,
                         icon_slot: QtWidgets.QLabel) -> None:
        """
        Получение картинки здания по слоту.
        Задание координат.
        """
        icon = self.get_icon_image(num)

        if icon is not None:
            icon_slot.setPixmap(QPixmap(
                icon).scaled(
                icon_slot.width(), icon_slot.height())
            )
            icon_slot.setGeometry(*self.get_coords(num))
        else:
            icon_slot.setGeometry(0, 0)

    def get_coords(self, num: int) -> List[int]:
        """Получение координат"""
        try:
            coords = self.branch_settings[num].coords
            return coords
        except KeyError:
            return [0, 0, 0, 0]

    def get_building_params(self, b_slot: int) -> None:
        """Получение параметров постройки"""
        self.graph = []
        self.building_name = self.branch_settings[b_slot].bname
        self.building_cost = self.branch_settings[b_slot].cost

        # Установка названия постройки, стоимости
        self.ui.buildingName.setText(
            str(f'{self.building_name} ({self.building_cost})'))

        if self.branch != OTHERS:
            # Установка имени юнита, соответствующего постройке
            unit_name = self.branch_settings[b_slot].unit_name
            self.ui.nextLevel.setText(unit_name)

            self.ui.nextLevelText.setText('След. уровень:')
            self.ui.prevLevelText.setText('Пред. уровень:')

            if b_slot < 10:
                prev_unit_name = main_db.get_unit_by_b_name(
                    self.branch_settings[b_slot].prev)

                self.ui.prevLevel.setText(prev_unit_name)

                # просклонять имя юнита
                # declined_name = self.decline(unit_name)

                self.ui.desc.setText(
                    f'{self.branch_settings[b_slot].desc}\n'
                    f'{prev_unit_name} превращается в {unit_name}')
            else:
                self.ui.prevLevel.setText('')

                self.ui.desc.setText(
                    f'{self.branch_settings[b_slot].desc}\n'
                    f'{unit_name}')
        else:
            self.ui.nextLevel.setText('')
            self.ui.prevLevel.setText('')
            self.ui.nextLevelText.setText('')
            self.ui.prevLevelText.setText('')
            self.ui.slot.setFixedSize(0, 0)
            self.ui.desc.setText(self.branch_settings[b_slot].desc)

        # Рекурсивное создание графа до выбранного здания
        self.get_building_graph(self.building_name, self.graph)

        # Метод определения возможности постройки
        self.set_building_possibility()

    def set_text_and_buy_slot(self,
                              text: str,
                              possibility: bool) -> None:
        """
        Задание текста о возможности постройки.
        Вывод рисунка кнопки.
        """
        color = 'black'
        if 'можно' in text:
            color = 'black'
            self.ui.slotBuy.setFixedSize(0, 0)

        elif 'построено' in text:
            color = 'darkgreen'
            self.ui.slotBuy.setFixedSize(59, 60)

        elif 'нельзя' in text or \
                'нужно' in text or \
                'уже' in text or \
                'Недостаточно' in text:
            color = 'darkred'
            self.ui.slotBuy.setFixedSize(59, 60)

        self.ui.slotBuy.setPixmap(QPixmap(
            os.path.join(INTERF, "b_icon_off.png")).scaled(
            self.ui.slotBuy.width(), self.ui.slotBuy.height()))

        self.ui.buildPossib.setText(text)
        self.ui.buildPossib.setStyleSheet(f'color: {color}')
        self.ui.pushButtonBuy.setEnabled(possibility)
        self.hbox.addWidget(self.ui.slotBuy)
        self.setLayout(self.hbox)

    def get_building_slot_by_name(self, b_name: str) -> int:
        """Получение слота постройки по имени"""
        branch = FACTIONS.get(self.faction)[self.branch]

        for num, val in branch.items():
            if b_name == val.bname:
                return num
        return 0

    def show_already_built(self) -> None:
        """Отметить уже построенные здания"""
        self.no_built()
        temp_graph = []

        # получение всех построенных зданий игрока
        buildings = main_db.get_buildings(
            main_db.current_player.name,
            self.faction)._asdict()

        if self.branch != OTHERS:
            # рекурсивное создание графа уже построенных зданий
            self.get_building_graph(buildings[self.branch], temp_graph)

            # ставим отметки о постройке зданий
            for building in temp_graph:
                if building != '' and building not in STARTING_FORMS:

                    b_slot = self.get_building_slot_by_name(building)
                    self.set_ok(b_slot)

            if buildings['special']:
                self.set_ok(10)

        elif self.branch == OTHERS:
            branch = FACTIONS.get(self.faction)[self.branch]

            for val in branch.values():
                if val.bname in buildings.values():

                    b_slot = self.get_building_slot_by_name(val.bname)
                    self.set_ok(b_slot)

    def set_ok(self, b_slot: int) -> None:
        """Установить флажок ОК на здании, обозначить что построено"""
        self.builded_dict[b_slot].setPixmap(QPixmap(
            os.path.join(INTERF, "ok.png")))
        self.builded_dict[b_slot].setGeometry(
            *self.get_coords(b_slot))

    def set_building_possibility(self) -> None:
        """Метод определения возможности постройки"""
        temp_graph = []

        # получение всех построенных зданий игрока
        buildings = main_db.get_buildings(
            main_db.current_player.name,
            self.faction)._asdict()

        if self.branch != OTHERS:
            # рекурсивное создание графа уже построенных зданий
            self.get_building_graph(
                buildings[self.branch],
                temp_graph)

            # если здание входит в граф построенных
            if self.building_name in temp_graph:
                self.set_text_and_buy_slot(ALREADY_BUILT,
                                           False)

            # если здание входит специальные постройки и построено
            elif self.building_name in SPECIAL_BUILDINGS \
                    and buildings['special']:
                self.set_text_and_buy_slot(ALREADY_BUILT,
                                           False)

            # если здание входит специальные постройки и не построено
            elif self.building_name in SPECIAL_BUILDINGS \
                    and not buildings['special'] \
                    and FACTIONS.get(self.faction)['special'][1].prev \
                    not in temp_graph:
                self.set_text_and_buy_slot(NEED_TO_BUILD_PREV,
                                           False)

            # если граф построенных входит в текущий граф и длина текущего
            # графа отличается от графа построенных более, чем на 1
            elif len(self.graph) - len(temp_graph) > 1 \
                    and set(temp_graph).issubset(self.graph) \
                    and '' not in temp_graph:
                self.set_text_and_buy_slot(NEED_TO_BUILD_PREV,
                                           False)

            elif '' in temp_graph \
                    and len(self.graph) < 2 \
                    and main_db.get_gold(
                main_db.current_player.name, self.faction
            ) >= self.building_cost:
                self.set_text_and_buy_slot(READY_TO_BUILD,
                                           True)

            elif '' in temp_graph and len(self.graph) >= 2:
                self.set_text_and_buy_slot(NEED_TO_BUILD_PREV,
                                           False)

            # если граф построенных не входит в текущий граф
            elif not set(temp_graph).issubset(self.graph) \
                    and '' not in temp_graph:
                self.set_text_and_buy_slot(ANOTHER_BRANCH,
                                           False)

            elif main_db.get_gold(
                    main_db.current_player.name, self.faction
            ) >= self.building_cost:
                self.set_text_and_buy_slot(READY_TO_BUILD,
                                           True)

            else:
                self.set_text_and_buy_slot(NOT_ENOUGH_GOLD,
                                           False)

        elif self.branch == OTHERS:
            # если текущее здание уже в построенных
            if self.building_name in buildings.values():
                self.set_text_and_buy_slot(ALREADY_BUILT,
                                           False)

            elif main_db.get_gold(
                    main_db.current_player.name, self.faction
            ) >= self.building_cost:
                self.set_text_and_buy_slot(READY_TO_BUILD,
                                           True)

            else:
                self.set_text_and_buy_slot(NOT_ENOUGH_GOLD,
                                           False)

        if main_db.already_built:
            self.set_text_and_buy_slot(
                'Сегодня уже была совершена постройка', False)

    def decline(self, unit_name: str) -> None:
        """Склонение имен юнитов по падежам"""
        if unit_name in DECLINATIONS.keys():
            declined = DECLINATIONS[unit_name]

        elif 3 > len(unit_name.split(' ')) > 1:
            part_1 = self.morph.parse(unit_name.split()[0])[0]
            part_2 = self.morph.parse(unit_name.split()[1])[0]
            name_1 = part_1.inflect({'ablt'}).word

            if part_2.word != 'огня':
                if part_2.tag.gender == 'masc':
                    name_2 = part_2.inflect({'ablt'}).word
                else:
                    name_2 = part_2.inflect({'gent'}).word
                declined = f'{name_1.capitalize()} {name_2}'
            else:
                declined = f'{name_1.capitalize()} {part_2.word}'

        else:
            name = self.morph.parse(unit_name)[0]
            declined = name.inflect({'ablt'}).word.capitalize()
        return declined

    def get_building_graph(self, bname: str, graph: list) -> None:
        """Рекурсивное создание графа зданий/построек"""
        for val in self.branch_settings.values():
            if val.bname == bname:
                graph.append(bname)
                if val.prev not in ('', 0):
                    self.get_building_graph(val.prev, graph)
                else:
                    return

    def no_built(self) -> None:
        """Снятие отметок о постройке зданий"""
        for slot in self.builded_dict.values():
            slot.setGeometry(0, 0, 0, 0)

    def unlight_all_buildings(self) -> None:
        """Снятие подсветки зданий"""
        self.ui.labelSelected1.setStyleSheet("border: 0px;")

    def highlight_selected_building(self,
                                    num: int,
                                    ui_slot: QtWidgets.QLabel) -> None:
        """Подсветка выбранной постройки"""
        ui_slot.setGeometry(*self.get_coords(num))
        ui_slot.setStyleSheet("border: 5px solid yellow;")

    def get_unit_by_b_slot(self, b_slot: int) -> Optional[namedtuple]:
        """Получение юнита по слоту постройки"""
        try:
            unit = main_db.get_unit_by_name(
                self.branch_settings[b_slot].unit_name)
            return unit
        except KeyError:
            return None

    def update_unit_by_b_slot(self, b_slot: int) -> None:
        """Обновление юнита согласно выбранному зданию"""
        self.unit = self.get_unit_by_b_slot(b_slot)
        self.slot_update(self.unit, self.ui.slot)
        self.button_update(self.unit, self.ui.pushButtonSlot)
        if self.unit is not None:
            slot_frame_update(self.unit, self.ui.slotFrame1)
        self.get_building_params(b_slot)

        # подсветка выбранного здания
        self.highlight_selected_building(b_slot, self.ui.labelSelected1)

    def update_unit_by_b_slot1(self) -> None:
        """Обновление юнита согласно зданию 1"""
        self.update_unit_by_b_slot(1)

    def update_unit_by_b_slot2(self) -> None:
        """Обновление юнита согласно зданию 2"""
        self.update_unit_by_b_slot(2)

    def update_unit_by_b_slot3(self) -> None:
        """Обновление юнита согласно зданию 3"""
        self.update_unit_by_b_slot(3)

    def update_unit_by_b_slot4(self) -> None:
        """Обновление юнита согласно зданию 4"""
        self.update_unit_by_b_slot(4)

    def update_unit_by_b_slot5(self) -> None:
        """Обновление юнита согласно зданию 5"""
        self.update_unit_by_b_slot(5)

    def update_unit_by_b_slot6(self) -> None:
        """Обновление юнита согласно зданию 6"""
        self.update_unit_by_b_slot(6)

    def update_unit_by_b_slot7(self) -> None:
        """Обновление юнита согласно зданию 7"""
        self.update_unit_by_b_slot(7)

    def update_unit_by_b_slot8(self) -> None:
        """Обновление юнита согласно зданию 8"""
        self.update_unit_by_b_slot(8)

    def update_unit_by_b_slot9(self) -> None:
        """Обновление юнита согласно зданию 9"""
        self.update_unit_by_b_slot(9)

    def update_unit_by_b_slot10(self) -> None:
        """Обновление юнита согласно зданию 10 (special)"""
        self.update_unit_by_b_slot(10)

    def slot_update(self,
                    unit: namedtuple,
                    ui_slot: QtWidgets.QLabel) -> None:
        """Обновление слота юнита"""
        set_size_by_unit(unit, ui_slot)

        ui_slot.setPixmap(QPixmap(
            get_unit_image(unit)).scaled(
            ui_slot.width(), ui_slot.height()))
        self.hbox.addWidget(ui_slot)
        self.setLayout(self.hbox)

    def building_face_update(self,
                             unit: namedtuple,
                             ui_slot: QtWidgets.QLabel) -> None:
        """Обновление лица юнита соответствующего постройке"""
        if unit is not None:
            ui_slot.setPixmap(QPixmap(
                self.get_unit_face(unit)).scaled(
                ui_slot.width(), ui_slot.height()))
            self.hbox.addWidget(ui_slot)
            self.setLayout(self.hbox)
        else:
            ui_slot.setFixedSize(0, 0)

    def button_update(self,
                      unit: namedtuple,
                      button: QtWidgets.QPushButton) -> None:
        """Обновление кнопки"""
        set_size_by_unit(unit, button)

        self.hbox.addWidget(button)
        self.setLayout(self.hbox)

    def reverse_icons(self) -> None:
        """Смена картинки постройки на лицо юнита"""
        if self.icons:
            for num, icon_slot in self.town_icons_dict.items():
                unit = self.get_unit_by_b_slot(num)
                self.building_face_update(unit, icon_slot)
                self.set_size_by_slot(icon_slot)
            self.icons = False
        else:
            self.show_all_branch_icons()
            self.icons = True

    def reverse_update(self) -> None:
        """Обновление доступности реверса иконок"""
        if self.branch == OTHERS:
            ui_lock(self.ui.pushButtonReverse)
            self.ui.slotReverse.setFixedSize(0, 0)
        else:
            ui_unlock(self.ui.pushButtonReverse)
            self.ui.slotReverse.setFixedSize(46, 46)

    def buy_building(self) -> None:
        """Метод постройки зданий в столице"""
        global QUESTION_WINDOW
        text = f'{self.building_name} - постройка этого здания будет ' \
               f'стоить {self.building_cost} золотых монет. Продолжить?'
        QUESTION_WINDOW = QuestionWindow(self, text)
        QUESTION_WINDOW.show()

    def confirmation(self) -> None:
        """Подтверждение постройки выбранного здания в столице"""
        # Если ОК
        if self.question:
            # берем из базы уже построенные здания
            changed_buildings = list(
                main_db.get_buildings(
                    main_db.current_player.name,
                    self.faction))

            # определяем текущую постройку
            if self.building_name == 'Гильдия':
                changed_buildings[5] = self.building_name
            elif self.building_name == 'Храм':
                changed_buildings[6] = self.building_name
            elif self.building_name == 'Башня магии':
                changed_buildings[7] = self.building_name
            elif self.building_name in SPECIAL_BUILDINGS:
                changed_buildings[4] = self.building_name
            else:
                changed_buildings[BRANCHES[self.branch]] = \
                    self.building_name

            # обновление построек в текущей сессии
            main_db.update_buildings(
                main_db.current_player.name,
                self.faction,
                changed_buildings)

            # получение текущего количества золота
            self.player_gold = main_db.get_gold(
                main_db.current_player.name, self.faction)
            changed_gold = self.player_gold - self.building_cost

            # обновление золота в базе
            main_db.update_gold(
                main_db.current_player.name,
                self.faction,
                changed_gold)
            self.ui.gold.setText(str(changed_gold))

            # уже строили сегодня
            main_db.already_built = 1

            main_db.update_session_built(
                main_db.game_session_id,
                main_db.already_built)

            self.set_building_possibility()
            self.show_already_built()

    def slot_detailed(self) -> None:
        """Метод создающий окно юнита (слот)."""
        global DETAIL_WINDOW
        DETAIL_WINDOW = UnitDialog(
            self.unit)
        DETAIL_WINDOW.show()

    @staticmethod
    def get_unit_face(unit: namedtuple) -> str:
        """Получение лица юнита"""
        return os.path.join(UNIT_ICONS, f"{unit.name} {ICON}")

    def get_icon_image(self, num: int) -> str:
        """Получение иконки здания"""
        icon_path = f"{self.faction}/{self.branch}/{num}.png"
        return os.path.join(TOWN_ICONS, icon_path)

    @staticmethod
    def set_size_by_slot(ui_obj) -> None:
        """Установка размеров картинки по слоту здания"""
        ui_obj.setFixedWidth(118)
        ui_obj.setFixedHeight(114)
