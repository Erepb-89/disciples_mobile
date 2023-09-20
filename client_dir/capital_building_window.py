"""Окно постройки в столице"""

import os.path

# import pymorphy2
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QMessageBox

from client_dir.capital_building_form import Ui_CapitalBuildingWindow
from client_dir.settings import CAPITAL_BUILDING, UNIT_ICONS, TOWN_ICONS, \
    SCREEN_RECT, DECLINATIONS, INTERF, ICON, COMMON, OTHERS
from client_dir.ui_functions import set_size_by_unit, get_unit_image, \
    slot_frame_update
from client_dir.unit_dialog import UnitDialog
from units_dir.buildings import FACTIONS, BRANCHES


class CapitalBuildingWindow(QMainWindow):
    """
    Класс - окно стройки в столице.
    """

    def __init__(self, database):
        super().__init__()
        # основные переменные
        self.database = database
        self.faction = self.database.current_game_faction
        self.branch = 'archer'
        self.building_name = ''
        self.building_cost = 0
        self.unit = self.get_unit_by_b_slot(1)
        self.graph = []
        self.fighter_graph = []
        self.mage_graph = []
        self.archer_graph = []
        self.support_graph = []
        self.others_graph = []
        # self.morph = pymorphy2.MorphAnalyzer()
        self.icons = True

        self.InitUI()

        self.get_all_branch_units()
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
        return os.path.join(
            CAPITAL_BUILDING,
            f"{self.branch}/{faction}.png")

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

        # Получение всех юнитов ветви
        self.get_all_branch_units()

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
        self.branch = OTHERS
        self.update_capital()

        self.unit = None
        self.ui.slot.setFixedSize(0, 0)
        self.ui.slotFrame1.setFixedSize(0, 0)
        self.ui.pushButtonSlot.setEnabled(False)

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
    def branch_settings(self):
        """Получение настроек ветви"""
        return FACTIONS.get(self.faction)[self.branch]

    def get_all_branch_units(self):
        """Получение всех юнитов ветви"""
        # получаем картинку здания по слоту
        for num, icon_slot in self.town_icons_dict.items():
            self.get_icon_by_slot(num, icon_slot)

        # получаем координаты кнопок
        for num, icon_button in self.icon_buttons_dict.items():
            icon_button.setGeometry(*self.get_coords(num))

    def get_icon_by_slot(self, num, icon_slot):
        """
        Получение картинки здания по слоту.
        Задание координат
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

    def get_coords(self, num):
        """Получение координат"""
        try:
            coords = self.branch_settings[num].coords
            return coords
        except KeyError:
            return [0, 0, 0, 0]

    def get_building_params(self, b_slot):
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

            prev_unit_name = self.get_unit_by_b_name(
                self.branch_settings[b_slot].prev)

            self.ui.prevLevel.setText(prev_unit_name)
            self.ui.nextLevelText.setText('След. уровень:')
            self.ui.prevLevelText.setText('Пред. уровень:')

            # просклонять имя юнита
            # declined_name = self.decline(unit_name)

            self.ui.desc.setText(
                f'{self.branch_settings[b_slot].desc}\n'
                # f'{prev_unit_name} становится {declined_name}')
                f'{prev_unit_name} превращается в {unit_name}')
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
        self.building_possibility()

    def set_text_and_buy_slot(self, text, possibility):
        """
        Задание текста о возможности постройки.
        Вывод рисунка кнопки.
        """
        color = 'black'
        if 'можно' in text:
            color = 'black'
            self.ui.slotBuy.setFixedSize(0, 0)

        elif 'уже' in text:
            color = 'darkgreen'
            self.ui.slotBuy.setFixedSize(59, 60)

        elif 'нельзя' in text or 'нужно' in text:
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

    def get_building_slot_by_name(self, b_name):
        """Получение слота постройки по имени"""
        branch = FACTIONS.get(self.faction)[self.branch]

        for num, val in branch.items():
            if b_name == val.bname:
                return num
        return 0

    def show_already_built(self):
        """Отметить уже построенные здания"""
        self.no_built()
        temp_graph = []

        # получение всех построенных зданий игрока
        buildings = self.database.get_buildings(
            self.database.current_user,
            self.faction)._asdict()

        if self.branch != OTHERS:
            # рекурсивное создание графа уже построенных зданий
            self.get_building_graph(buildings[self.branch], temp_graph)

            # ставим отметки о постройке зданий
            for building in temp_graph:
                if building != '':
                    b_slot = self.get_building_slot_by_name(building)

                    self.builded_dict[b_slot].setPixmap(QPixmap(
                        os.path.join(INTERF, "ok.png")))
                    self.builded_dict[b_slot].setGeometry(
                        *self.get_coords(b_slot))

        elif self.branch == OTHERS:
            branch = FACTIONS.get(self.faction)[self.branch]

            for val in branch.values():
                if val.bname in buildings.values():
                    b_slot = self.get_building_slot_by_name(val.bname)
                    self.builded_dict[b_slot].setPixmap(QPixmap(
                        os.path.join(INTERF, "ok.png")))
                    self.builded_dict[b_slot].setGeometry(
                        *self.get_coords(b_slot))

    def building_possibility(self):
        """Метод определения возможности постройки"""
        temp_graph = []

        # получение всех построенных зданий игрока
        buildings = self.database.get_buildings(
            self.database.current_user,
            self.faction)._asdict()

        if self.branch != OTHERS:
            # рекурсивное создание графа уже построенных зданий
            self.get_building_graph(buildings[self.branch], temp_graph)

            # print('self.graph', self.graph)
            # print('temp_graph', temp_graph)

            # если здание входит в граф построенных
            if self.building_name in temp_graph:
                text = 'Это здание уже построено'
                self.set_text_and_buy_slot(text, False)

            # если граф построенных входит в текущий граф и длина текущего
            # графа отличается от графа построенных более, чем на 1
            elif len(self.graph) - len(temp_graph) > 1 \
                    and set(temp_graph).issubset(self.graph)\
                    and '' not in temp_graph:
                text = 'Сначала нужно построить здание, ' \
                       'предшествующее этому'
                self.set_text_and_buy_slot(text, False)

            elif '' in temp_graph and len(self.graph) < 2:
                text = 'Это здание можно построить'
                self.set_text_and_buy_slot(text, True)

            elif '' in temp_graph and len(self.graph) >= 2:
                text = 'Сначала нужно построить здание, ' \
                       'предшествующее этому'
                self.set_text_and_buy_slot(text, False)

            # если граф построенных не входит в текущий граф
            elif not set(temp_graph).issubset(self.graph) \
                    and '' not in temp_graph:
                text = 'Это здание нельзя построить, поскольку ' \
                       'была выбрана другая ветвь развития'
                self.set_text_and_buy_slot(text, False)

            else:
                text = 'Это здание можно построить'
                self.set_text_and_buy_slot(text, True)

        elif self.branch == OTHERS:
            # если текущее здание уже в построенных
            if self.building_name in buildings.values():
                text = 'Это здание уже построено'
                self.set_text_and_buy_slot(text, False)

            else:
                text = 'Это здание можно построить'
                self.set_text_and_buy_slot(text, True)

    def decline(self, unit_name):
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

    def get_building_graph(self, bname, graph):
        """Рекурсивное создание графа зданий/построек"""
        for val in self.branch_settings.values():
            if val.bname == bname:
                graph.append(bname)
                if val.prev not in ('', 0):
                    self.get_building_graph(val.prev, graph)
                else:
                    return

    def no_built(self):
        """Снятие отметок о постройке зданий"""
        for slot in self.builded_dict.values():
            slot.setGeometry(0, 0, 0, 0)

    def unlight_all_buildings(self):
        """Снятие подсветки зданий"""
        self.ui.labelSelected1.setStyleSheet("border: 0px;")

    def highlight_selected_building(self, num, ui_slot):
        """Подсветка выбранной постройки"""
        ui_slot.setGeometry(*self.get_coords(num))
        ui_slot.setStyleSheet("border: 5px solid yellow;")

    def get_unit_by_b_slot(self, b_slot):
        """Получение юнита по слоту постройки"""
        try:
            unit = self.database.get_unit_by_name(
                self.branch_settings[b_slot].unit_name)
            return unit
        except KeyError:
            return None

    def get_unit_by_b_name(self, b_name):
        """Получение юнита по названию постройки"""
        branch = FACTIONS.get(self.faction)[self.branch]
        for val in branch.values():
            if b_name == val.bname:
                return val.unit_name
        return ''

    def update_unit_by_b_slot(self, b_slot):
        """Обновление юнита согласно выбранному зданию"""
        self.unit = self.get_unit_by_b_slot(b_slot)
        self.slot_update(self.unit, self.ui.slot)
        self.button_update(self.unit, self.ui.pushButtonSlot)
        self.get_building_params(b_slot)
        # if self.unit is not None:
        #     slot_frame_update(self.unit, self.ui.slotFrame1)

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
        if unit is not None:
            slot.setPixmap(QPixmap(
                self.get_unit_face(unit)).scaled(
                slot.width(), slot.height()))
            self.hbox.addWidget(slot)
            self.setLayout(self.hbox)
        else:
            slot.setFixedSize(0, 0)

    def button_update(self, unit, button):
        """Обновление кнопки"""
        set_size_by_unit(unit, button)

        self.hbox.addWidget(button)
        self.setLayout(self.hbox)

    def reverse_icons(self):
        """Смена картинки постройки на лицо юнита"""
        if self.icons:
            for num, icon_slot in self.town_icons_dict.items():
                # icon_slot.setFixedSize(118, 114)
                unit = self.get_unit_by_b_slot(num)
                self.building_face_update(unit, icon_slot)
                self.set_size_by_slot(icon_slot)
            self.icons = False
        else:
            self.get_all_branch_units()
            self.icons = True

    def reverse_update(self):
        """Обновление доступности реверса иконок"""
        if self.branch == OTHERS:
            self.ui.pushButtonReverse.setEnabled(False)
            self.ui.slotReverse.setFixedSize(0, 0)
        else:
            self.ui.pushButtonReverse.setEnabled(True)
            self.ui.slotReverse.setFixedSize(46, 46)

    def buy_building(self):
        """Метод постройки зданий в столице"""
        if self.player_gold < self.building_cost:

            msg = QMessageBox()
            msg.setWindowTitle("Предупреждение")
            msg.setText("Недостаточно золота")
            msg.setIcon(QMessageBox.Warning)

            msg.exec_()
        else:
            changed_buildings = list(
                self.database.get_buildings(
                    self.database.current_user,
                    self.faction))

            # обновление построек в текущей сессии
            if self.building_name == 'Гильдия':
                changed_buildings[5] = self.building_name
            elif self.building_name == 'Храм':
                changed_buildings[6] = self.building_name
            elif self.building_name == 'Башня магии':
                changed_buildings[7] = self.building_name
            else:
                changed_buildings[BRANCHES[self.branch]] = self.building_name

            self.database.update_buildings(
                self.database.current_user,
                self.faction,
                changed_buildings)

            self.player_gold = self.database.get_gold(
                self.database.current_user, self.faction)
            changed_gold = self.player_gold - self.building_cost

            # обновление золота в базе
            self.database.update_gold(
                self.database.current_user,
                self.faction,
                changed_gold)
            self.ui.gold.setText(str(changed_gold))

        self.building_possibility()
        self.show_already_built()

    def slot_detailed(self):
        """Метод создающий окно юнита (слот)."""
        global DETAIL_WINDOW
        DETAIL_WINDOW = UnitDialog(
            self.database,
            self.unit)
        DETAIL_WINDOW.show()

    @staticmethod
    def get_unit_face(unit):
        """Получение лица юнита"""
        return os.path.join(UNIT_ICONS, f"{unit.name} {ICON}")

    def get_icon_image(self, num):
        """Получение иконки здания"""
        icon_path = f"{self.faction}/{self.branch}/{num}.png"
        return os.path.join(TOWN_ICONS, icon_path)

    @staticmethod
    def set_size_by_slot(ui_obj):
        """Установка размеров картинки по слоту здания"""
        ui_obj.setFixedWidth(118)
        ui_obj.setFixedHeight(114)
