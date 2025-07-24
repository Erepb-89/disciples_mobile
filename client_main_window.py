"""Главное окно клиента"""
import asyncio
import os.path
import sys
import multiprocessing

from collections import namedtuple
from typing import Callable, Optional
from threading import Thread as Thread
from multiprocessing import Process, Manager as mgr

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QMimeData, QVariant, QEvent, QTranslator
from PyQt5.QtGui import QPixmap, QStandardItemModel, \
    QStandardItem, QMovie, QDrag, QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, \
    QHBoxLayout, QListView, QLabel, QFrame

from client_dir.windows.capital_window import CapitalWindow
from client_dir.windows.choose_faction_window import ChooseRaceWindow
from client_dir.windows.fight_window import FightWindow
from client_dir.windows.campaign_window import CampaignWindow
from client_dir.forms.client_main_form import Ui_MainWindow
from client_dir.windows.hire_menu_window import HireMenuWindow
from client_dir.windows.question_window import QuestionWindow
from client_dir.settings import UNIT_ICONS, GIF_ANIMATIONS, \
    TOWN_IMG, PLUG, ICON, PORTRAITS, BACKGROUND, BIG, \
    ACTIVE_UNITS
from client_dir.ui_functions import get_unit_image, \
    set_beige_colour, set_borders, ui_lock, ui_unlock, get_cursor
from client_dir.dialogs.unit_dialog import UnitDialog
from server.server import MyThread
from units_dir.models import PlayerUnits, CurrentDungeon
from units_dir.battle_unit import Unit
from units_dir.visual_model import v_model


class ClientMainWindow(QMainWindow):
    """
    Класс - основное окно пользователя.
    Содержит всю основную логику работы клиентского модуля.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированного файла client_main_form.py
    """

    class Label(QLabel):
        def __init__(self, title, parent_window):
            super().__init__(title, parent_window)
            self.setAcceptDrops(True)
            self.parent_window = parent_window

        def mouseMoveEvent(self, event) -> None:
            mime_data = QMimeData()
            mime_data.setImageData(QVariant(self.pixmap()))
            pixmap = QWidget.grab(self)

            drag = QDrag(self)
            drag.setMimeData(mime_data)

            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())

            if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
                print('moved')

        def dragEnterEvent(self, event) -> None:
            if event.mimeData().hasImage():
                event.accept()
            else:
                event.ignore()

        def dropEvent(self, event) -> None:
            first = int(self.parent_window.current_label[-1])
            second = int(self.objectName()[-1])

            if "enemy" not in self.parent_window.current_label.lower():
                self.parent_window.check_and_swap(
                    first,
                    second,
                    PlayerUnits)

            else:
                self.parent_window.check_and_swap(
                    first,
                    second,
                    CurrentDungeon)

            # self.parent_window.current_label[-1])

    def __init__(self):
        super().__init__()
        # основные переменные
        self.name = 'ClientMainWindow'
        self.question = False  # увольнение
        self.difficulty = 2
        self.player_units_model = None
        self.player_slots_model = None
        self.enemy_units_model = None
        self.enemy_slots_model = None
        self.faction = ''
        self.factory = None

        self.InitUI()

        self.difficulty = v_model.difficulty

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.hbox = QHBoxLayout(self)

        self.ui.slot1 = self.Label('', self)
        self.ui.slot1.setGeometry(QtCore.QRect(40, 260, 104, 127))
        self.ui.slot1.setFrameShape(QFrame.Panel)
        self.ui.slot1.setFrameShadow(QFrame.Raised)
        self.ui.slot1.setLineWidth(3)
        self.ui.slot1.setMidLineWidth(0)
        self.ui.slot1.setObjectName("slot1")

        self.ui.slot2 = self.Label('', self)
        self.ui.slot2.setGeometry(QtCore.QRect(163, 260, 101, 127))
        self.ui.slot2.setFrameShape(QFrame.Panel)
        self.ui.slot2.setFrameShadow(QFrame.Raised)
        self.ui.slot2.setLineWidth(3)
        self.ui.slot2.setMidLineWidth(0)
        self.ui.slot2.setObjectName("slot2")

        self.ui.slot3 = self.Label('', self)
        self.ui.slot3.setGeometry(QtCore.QRect(40, 420, 104, 127))
        self.ui.slot3.setFrameShape(QFrame.Panel)
        self.ui.slot3.setFrameShadow(QFrame.Raised)
        self.ui.slot3.setLineWidth(3)
        self.ui.slot3.setMidLineWidth(0)
        self.ui.slot3.setObjectName("slot3")

        self.ui.slot4 = self.Label('', self)
        self.ui.slot4.setGeometry(QtCore.QRect(160, 420, 104, 127))
        self.ui.slot4.setFrameShape(QFrame.Panel)
        self.ui.slot4.setFrameShadow(QFrame.Raised)
        self.ui.slot4.setLineWidth(3)
        self.ui.slot4.setMidLineWidth(0)
        self.ui.slot4.setObjectName("slot4")

        self.ui.slot5 = self.Label('', self)
        self.ui.slot5.setGeometry(QtCore.QRect(40, 560, 104, 127))
        self.ui.slot5.setFrameShape(QFrame.Panel)
        self.ui.slot5.setFrameShadow(QFrame.Raised)
        self.ui.slot5.setLineWidth(3)
        self.ui.slot5.setMidLineWidth(0)
        self.ui.slot5.setObjectName("slot5")

        self.ui.slot6 = self.Label('', self)
        self.ui.slot6.setGeometry(QtCore.QRect(160, 560, 104, 127))
        self.ui.slot6.setFrameShape(QFrame.Panel)
        self.ui.slot6.setFrameShadow(QFrame.Raised)
        self.ui.slot6.setLineWidth(3)
        self.ui.slot6.setMidLineWidth(0)
        self.ui.slot6.setObjectName("slot6")

        self.ui.EnemySlot1 = self.Label('', self)
        self.ui.EnemySlot1.setGeometry(QtCore.QRect(1000, 260, 104, 127))
        self.ui.EnemySlot1.setFrameShape(QFrame.Panel)
        self.ui.EnemySlot1.setFrameShadow(QFrame.Raised)
        self.ui.EnemySlot1.setLineWidth(3)
        self.ui.EnemySlot1.setMidLineWidth(0)
        self.ui.EnemySlot1.setObjectName("EnemySlot1")

        self.ui.EnemySlot2 = self.Label('', self)
        self.ui.EnemySlot2.setGeometry(QtCore.QRect(880, 260, 104, 127))
        self.ui.EnemySlot2.setFrameShape(QFrame.Panel)
        self.ui.EnemySlot2.setFrameShadow(QFrame.Raised)
        self.ui.EnemySlot2.setLineWidth(3)
        self.ui.EnemySlot2.setMidLineWidth(0)
        self.ui.EnemySlot2.setObjectName("EnemySlot2")

        self.ui.EnemySlot3 = self.Label('', self)
        self.ui.EnemySlot3.setGeometry(QtCore.QRect(1000, 420, 104, 127))
        self.ui.EnemySlot3.setFrameShape(QFrame.Panel)
        self.ui.EnemySlot3.setFrameShadow(QFrame.Raised)
        self.ui.EnemySlot3.setLineWidth(3)
        self.ui.EnemySlot3.setMidLineWidth(0)
        self.ui.EnemySlot3.setObjectName("EnemySlot3")

        self.ui.EnemySlot4 = self.Label('', self)
        self.ui.EnemySlot4.setGeometry(QtCore.QRect(880, 420, 104, 127))
        self.ui.EnemySlot4.setFrameShape(QFrame.Panel)
        self.ui.EnemySlot4.setFrameShadow(QFrame.Raised)
        self.ui.EnemySlot4.setLineWidth(3)
        self.ui.EnemySlot4.setMidLineWidth(0)
        self.ui.EnemySlot4.setObjectName("EnemySlot4")

        self.ui.EnemySlot5 = self.Label('', self)
        self.ui.EnemySlot5.setGeometry(QtCore.QRect(1000, 560, 104, 127))
        self.ui.EnemySlot5.setFrameShape(QFrame.Panel)
        self.ui.EnemySlot5.setFrameShadow(QFrame.Raised)
        self.ui.EnemySlot5.setLineWidth(3)
        self.ui.EnemySlot5.setMidLineWidth(0)
        self.ui.EnemySlot5.setObjectName("EnemySlot5")

        self.ui.EnemySlot6 = self.Label('', self)
        self.ui.EnemySlot6.setGeometry(QtCore.QRect(880, 560, 104, 127))
        self.ui.EnemySlot6.setFrameShape(QFrame.Panel)
        self.ui.EnemySlot6.setFrameShadow(QFrame.Raised)
        self.ui.EnemySlot6.setLineWidth(3)
        self.ui.EnemySlot6.setMidLineWidth(0)
        self.ui.EnemySlot6.setObjectName("EnemySlot6")

        self.right_slots = [
            self.ui.slot2,
            self.ui.slot4,
            self.ui.slot6,
        ]

        self.ui.listAllUnits.clicked.connect(self.on_list_clicked)

        self.ui.listAllUnits.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn)
        self.ui.listAllUnits.setWordWrap(True)

        self.ui.pushButtonHire.clicked.connect(self.hire_unit_action)
        self.ui.pushButtonHire.setStatusTip('Выберите номер слота для найма')
        self.ui.pushButtonDelete.clicked.connect(self.delete_unit_action)
        self.ui.pushButtonDelete.setStatusTip(
            'Выберите слот, который хотите освободить')
        self.ui.pushButtonCapital.clicked.connect(self.show_capital)
        self.ui.pushButtonChooseRace.clicked.connect(self.show_choose_race)
        self.ui.pushButtonFight.clicked.connect(self.show_fight_window)
        self.ui.pushButtonCampaign.clicked.connect(self.show_campaign_window)
        self.ui.pushButtonVersus.clicked.connect(self.show_versus_window)

        self.ui.pushButtonHireEn.clicked.connect(self.hire_enemy_unit_action)
        self.ui.pushButtonHireEn.setStatusTip(
            'Выберите номер слота для найма')
        self.ui.pushButtonDeleteEn.clicked.connect(
            self.delete_enemy_unit_action)
        self.ui.pushButtonDeleteEn.setStatusTip(
            'Выберите слот, который хотите освободить')

        self.ui.pushButtonUpSlot1.clicked.connect(
            self.upgrade_slot1_unit)
        self.ui.pushButtonDownSlot1.clicked.connect(
            self.downgrade_slot1_unit)

        self.ui.pushButtonUpSlot2.clicked.connect(
            self.upgrade_slot2_unit)
        self.ui.pushButtonDownSlot2.clicked.connect(
            self.downgrade_slot2_unit)

        self.ui.pushButtonUpSlot3.clicked.connect(
            self.upgrade_slot3_unit)
        self.ui.pushButtonDownSlot3.clicked.connect(
            self.downgrade_slot3_unit)

        self.ui.pushButtonUpSlot4.clicked.connect(
            self.upgrade_slot4_unit)
        self.ui.pushButtonDownSlot4.clicked.connect(
            self.downgrade_slot4_unit)

        self.ui.pushButtonUpSlot5.clicked.connect(
            self.upgrade_slot5_unit)
        self.ui.pushButtonDownSlot5.clicked.connect(
            self.downgrade_slot5_unit)

        self.ui.pushButtonUpSlot6.clicked.connect(
            self.upgrade_slot6_unit)
        self.ui.pushButtonDownSlot6.clicked.connect(
            self.downgrade_slot6_unit)

        self.ui.pushButtonUpEnemySlot1.clicked.connect(
            self.upgrade_enemy_slot1_unit)
        self.ui.pushButtonDownEnemySlot1.clicked.connect(
            self.downgrade_enemy_slot1_unit)

        self.ui.pushButtonUpEnemySlot2.clicked.connect(
            self.upgrade_enemy_slot2_unit)
        self.ui.pushButtonDownEnemySlot2.clicked.connect(
            self.downgrade_enemy_slot2_unit)

        self.ui.pushButtonUpEnemySlot3.clicked.connect(
            self.upgrade_enemy_slot3_unit)
        self.ui.pushButtonDownEnemySlot3.clicked.connect(
            self.downgrade_enemy_slot3_unit)

        self.ui.pushButtonUpEnemySlot4.clicked.connect(
            self.upgrade_enemy_slot4_unit)
        self.ui.pushButtonDownEnemySlot4.clicked.connect(
            self.downgrade_enemy_slot4_unit)

        self.ui.pushButtonUpEnemySlot5.clicked.connect(
            self.upgrade_enemy_slot5_unit)
        self.ui.pushButtonDownEnemySlot5.clicked.connect(
            self.downgrade_enemy_slot5_unit)

        self.ui.pushButtonUpEnemySlot6.clicked.connect(
            self.upgrade_enemy_slot6_unit)
        self.ui.pushButtonDownEnemySlot6.clicked.connect(
            self.downgrade_enemy_slot6_unit)

        self.ui.slot1.installEventFilter(self)
        self.ui.slot1.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.slot1.customContextMenuRequested \
            .connect(self.slot1_detailed)

        self.ui.slot2.installEventFilter(self)
        self.ui.slot2.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.slot2.customContextMenuRequested \
            .connect(self.slot2_detailed)

        self.ui.slot3.installEventFilter(self)
        self.ui.slot3.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.slot3.customContextMenuRequested \
            .connect(self.slot3_detailed)

        self.ui.slot4.installEventFilter(self)
        self.ui.slot4.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.slot4.customContextMenuRequested \
            .connect(self.slot4_detailed)

        self.ui.slot5.installEventFilter(self)
        self.ui.slot5.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.slot5.customContextMenuRequested \
            .connect(self.slot5_detailed)

        self.ui.slot6.installEventFilter(self)
        self.ui.slot6.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.slot6.customContextMenuRequested \
            .connect(self.slot6_detailed)

        self.ui.EnemySlot1.installEventFilter(self)
        self.ui.EnemySlot1.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.EnemySlot1.customContextMenuRequested \
            .connect(self.en_slot1_detailed)

        self.ui.EnemySlot2.installEventFilter(self)
        self.ui.EnemySlot2.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.EnemySlot2.customContextMenuRequested \
            .connect(self.en_slot2_detailed)

        self.ui.EnemySlot3.installEventFilter(self)
        self.ui.EnemySlot3.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.EnemySlot3.customContextMenuRequested \
            .connect(self.en_slot3_detailed)

        self.ui.EnemySlot4.installEventFilter(self)
        self.ui.EnemySlot4.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.EnemySlot4.customContextMenuRequested \
            .connect(self.en_slot4_detailed)

        self.ui.EnemySlot5.installEventFilter(self)
        self.ui.EnemySlot5.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.EnemySlot5.customContextMenuRequested \
            .connect(self.en_slot5_detailed)

        self.ui.EnemySlot6.installEventFilter(self)
        self.ui.EnemySlot6.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.ui.EnemySlot6.customContextMenuRequested \
            .connect(self.en_slot6_detailed)

        self.ui.pushButtonAddPlayer.clicked.connect(self.add_player_action)
        self.ui.pushButtonDelPlayer.clicked.connect(self.delete_player_action)
        self.ui.pushButtonChoosePlayer.clicked.connect(
            self.choose_player_action)

        self.ui.pushButtonCreateServer.clicked.connect(self.create_server)
        self.server_thread = QtCore.QThread(self)  # +++
        self.server = MyThread()
        self.server.moveToThread(self.server_thread)
        self.server_thread.started.connect(self.server.run)  # !!!

        # подкраска элементов
        set_beige_colour(self.ui.pushButtonAddPlayer)
        set_beige_colour(self.ui.pushButtonDelPlayer)
        set_beige_colour(self.ui.pushButtonChoosePlayer)
        set_beige_colour(self.ui.pushButtonHire)
        set_beige_colour(self.ui.pushButtonHireEn)
        set_beige_colour(self.ui.pushButtonDelete)
        set_beige_colour(self.ui.pushButtonDeleteEn)
        set_beige_colour(self.ui.pushButtonCapital)
        set_beige_colour(self.ui.pushButtonChooseRace)
        set_beige_colour(self.ui.pushButtonFight)
        set_beige_colour(self.ui.pushButtonCampaign)
        set_beige_colour(self.ui.pushButtonVersus)

        set_beige_colour(self.ui.pushButtonUpSlot1)
        set_beige_colour(self.ui.pushButtonUpSlot2)
        set_beige_colour(self.ui.pushButtonUpSlot3)
        set_beige_colour(self.ui.pushButtonUpSlot4)
        set_beige_colour(self.ui.pushButtonUpSlot5)
        set_beige_colour(self.ui.pushButtonUpSlot6)
        set_beige_colour(self.ui.pushButtonDownSlot1)
        set_beige_colour(self.ui.pushButtonDownSlot2)
        set_beige_colour(self.ui.pushButtonDownSlot3)
        set_beige_colour(self.ui.pushButtonDownSlot4)
        set_beige_colour(self.ui.pushButtonDownSlot5)
        set_beige_colour(self.ui.pushButtonDownSlot6)

        set_beige_colour(self.ui.pushButtonUpEnemySlot1)
        set_beige_colour(self.ui.pushButtonUpEnemySlot2)
        set_beige_colour(self.ui.pushButtonUpEnemySlot3)
        set_beige_colour(self.ui.pushButtonUpEnemySlot4)
        set_beige_colour(self.ui.pushButtonUpEnemySlot5)
        set_beige_colour(self.ui.pushButtonUpEnemySlot6)
        set_beige_colour(self.ui.pushButtonDownEnemySlot1)
        set_beige_colour(self.ui.pushButtonDownEnemySlot2)
        set_beige_colour(self.ui.pushButtonDownEnemySlot3)
        set_beige_colour(self.ui.pushButtonDownEnemySlot4)
        set_beige_colour(self.ui.pushButtonDownEnemySlot5)
        set_beige_colour(self.ui.pushButtonDownEnemySlot6)

        set_beige_colour(self.ui.listAllUnits)
        set_beige_colour(self.ui.listPlayerUnits)
        set_beige_colour(self.ui.listPlayerSlots)
        set_beige_colour(self.ui.listEnemyUnits)
        set_beige_colour(self.ui.listEnemySlots)
        set_beige_colour(self.ui.PlayerName)
        set_beige_colour(self.ui.Email)
        set_beige_colour(self.ui.PlayersList)
        set_beige_colour(self.ui.ServerList)

        set_borders(self.ui.gifLabel)
        set_borders(self.ui.iconLabel)
        set_borders(self.ui.portraitLabel)

        player_name = None
        try:
            player_name = v_model.current_player_name
        except Exception as err:
            print(err)
        self.ui.currentPlayer.setText(player_name)
        self.ui.currentPlayer.setStyleSheet('color: white')

        v_model.update_game_session()

        self.all_players_list_update()
        self.units_list_update()
        self.player_slots_update()
        self.reset()

        self.check_campaign_session()
        self.ui.difficultyText.setStyleSheet('color: white')
        self.ui.languageText.setStyleSheet('color: white')

        self.current_label = ''
        self.source = ''

        self.trans = QTranslator(self)

        self.ui.comboLanguage.currentIndexChanged.connect(self.lang_choice)

        options = ([('Russian', ''),
                    ('English', 'main_en')])

        for i, (text, lang) in enumerate(options):
            self.ui.comboLanguage.addItem(text)
            self.ui.comboLanguage.setItemData(i, lang)
        # self.ui.retranslateUi(ClientMainWindow)

        cursor_standard = QCursor(QPixmap(get_cursor('standard')))
        QApplication.setOverrideCursor(cursor_standard)

        self.show()

    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter:
            self.source = source
            self.current_label = source.objectName()
        return super().eventFilter(source, event)

    def lang_choice(self, index):
        data = self.ui.comboLanguage.itemData(index)
        if data:
            self.trans.load(data)
            app.installTranslator(self.trans)
            self.ui.retranslateUi(self)
        else:
            app.removeTranslator(self.trans)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(ClientMainWindow)
        super(ClientMainWindow, self).changeEvent(event)

    def closeEvent(self, event) -> None:
        """Закрытие всех окон по выходу из главного"""
        self.server.stop()
        self.server.deleteLater()
        self.server_thread.quit()
        os.sys.exit(0)

    def reset(self) -> None:
        """Обновить"""
        self.player_list_update()

        self.get_current_faction()
        self.set_capital_image()

        self.enemy_list_update()
        self.enemy_slots_update()

    def create_server(self):
        """Создание сервера в отдельном потоке"""
        if self.server_thread.isRunning():
            self.server.stop()
            self.ui.pushButtonCreateServer.setText('Создать сервер')
            self.server_thread.quit()
        else:
            self.ui.pushButtonCreateServer.setText('Остановить сервер')
            self.server_thread.start()

        # pass
        # self.thread1 = QtCore.QThread(self)
        # self.thread1.started.connect(asyncio.run(server_main()))
        # self.thread1.start()

        # server_thread = Thread(target=asyncio.run(server_main()),
        #                        name="Server Thread",
        #                        daemon=True)
        # server_thread.start()
        # server_thread.join()

        # with mgr():
        #     p2 = Process(target=asyncio.run(server_main()))
        #     p2.start()

        # asyncio.run(server_main())

    def check_campaign_session(self):
        """Проверка сессии"""
        session = None
        if v_model.current_player is not None:
            session = v_model.get_session_by_faction(self.faction)

        if session is not None:
            self.unlock_campaign()
        else:
            self.lock_campaign()

    def lock_campaign(self):
        """
        Проверка текущей игровой сессии.
        Если отсутствует запись в базе, заблокировать кнопки кампании.
        """
        ui_lock(self.ui.pushButtonCampaign)
        ui_lock(self.ui.pushButtonCapital)

    def unlock_campaign(self):
        """
        Проверка текущей игровой сессии.
        Если есть запись в базе, разблокировать кнопки кампании.
        """
        ui_unlock(self.ui.pushButtonCampaign)
        ui_unlock(self.ui.pushButtonCapital)

    def update_diff_checkbox(self) -> None:
        """Метод заполнения выпадающего списка доступных сложностей."""
        diff_slots = [1, 2, 3]
        self.diff_model = QStandardItemModel()
        for slot in diff_slots:
            item = QStandardItem(str(slot))
            item.setEditable(False)
            self.diff_model.appendRow(item)
        self.ui.comboDifficulty.setModel(self.diff_model)

        self.ui.comboDifficulty.setCurrentIndex(self.difficulty - 1)

        session = None
        if v_model.current_player is not None:
            session = v_model.get_session_by_faction(self.faction)

        if session is not None:
            self.change_difficulty()
            self.ui.comboDifficulty.currentIndexChanged.connect(
                self.change_difficulty)

    def change_difficulty(self) -> None:
        """Устанавливает выбранную сложность"""
        self.difficulty = int(self.ui.comboDifficulty.currentText())
        v_model.set_session_difficulty(self.difficulty)

    @staticmethod
    def button_enabled(button, database, num2):
        """Определяет доступность кнопки по юнитам в слотах"""
        try:
            if v_model.get_unit_by_slot(
                    num2,
                    database).size == BIG:
                ui_lock(button)
            else:
                ui_unlock(button)
        except AttributeError:
            ui_unlock(button)

    def on_list_clicked(self) -> None:
        """Показывает иконку и портрет выбранного из списка юнита"""
        selected = self.ui.listAllUnits.currentIndex().data()
        self.define_hire_active(selected)

        # показываем иконку юнита
        lbl = self.ui.iconLabel
        lbl.setPixmap(QPixmap(
            os.path.join(UNIT_ICONS, f"{selected} {ICON}")))

        # показываем портрет юнита
        prt = self.ui.portraitLabel
        prt.setPixmap(QPixmap(
            os.path.join(PORTRAITS, f"{selected}.gif")))

        self.show_gif(selected)
        self.hbox.addWidget(lbl)
        self.setLayout(self.hbox)

    def set_coords_for_slots(self, ui_obj: any) -> None:
        """Установить координаты для правых слотов"""
        if ui_obj in self.right_slots:
            ui_coords = ui_obj.geometry().getCoords()
            new_coords = list(ui_coords)
            new_coords[0] = 160
            ui_obj.setGeometry(*new_coords)

            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def set_size_by_unit(self, unit, ui_obj: any) -> None:
        """Установка размера иконки по размеру самого юнита"""
        self.set_coords_for_slots(ui_obj)

        try:
            if unit.size == BIG and ui_obj in self.right_slots:
                ui_coords = ui_obj.geometry().getCoords()
                new_coords = list(ui_coords)
                new_coords[0] -= 120
                new_coords[2] = 224
                new_coords[3] = 126
                ui_obj.setGeometry(*new_coords)

            if unit.size == BIG:
                ui_obj.setFixedWidth(225)
                ui_obj.setFixedHeight(127)

            else:
                ui_obj.setFixedWidth(105)
                ui_obj.setFixedHeight(127)
        except AttributeError:
            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)

    def slot_update(self,
                    unit: namedtuple,
                    slot: QLabel) -> None:
        """Установка gif'ки в иконку юнита"""
        self.set_size_by_unit(unit, slot)

        slot.setPixmap(QPixmap(
            get_unit_image(unit)).scaled(
            slot.width(), slot.height()))
        self.hbox.addWidget(slot)
        self.setLayout(self.hbox)

    def get_current_faction(self) -> None:
        """Получение текущей фракции"""
        self.faction = v_model.current_faction
        self.ui.currentFaction.setText(self.faction)
        self.ui.currentFaction.setStyleSheet('color: white')

    def set_capital_image(self) -> None:
        """Установить картинку как в столице"""
        self.ui.capital.setPixmap(QPixmap(BACKGROUND))
        self.ui.capital.setGeometry(QtCore.QRect(0, 0, 1380, 742))

    @staticmethod
    def get_capital_image(faction: str) -> Optional[str]:
        """Отображение городского фона"""
        try:
            return os.path.join(TOWN_IMG, f"{faction}.png")
        except AttributeError:
            return None

    def show_gif(self, unit_name: str) -> None:
        """Отображение gif-файла выбранного юнита"""
        gif_label = self.ui.gifLabel
        try:
            gif = QMovie(os.path.join(GIF_ANIMATIONS, f"{unit_name}.gif"))
            gif_label.setMovie(gif)
            gif.start()
        except AttributeError:
            gif_label.setPixmap(QPixmap(os.path.join(
                UNIT_ICONS, PLUG)))

    def player_slots_update(self) -> None:
        """Метод обновляющий список слотов игрока."""
        player_slots = [1, 2, 3, 4, 5, 6]
        self.player_slots_model = QStandardItemModel()
        for slot in player_slots:
            item = QStandardItem(str(slot))
            item.setEditable(False)
            self.player_slots_model.appendRow(item)
        self.ui.listPlayerSlots.setModel(self.player_slots_model)

    def enemy_slots_update(self) -> None:
        """Метод обновляющий список слотов противника."""
        enemy_slots = [1, 2, 3, 4, 5, 6]
        self.enemy_slots_model = QStandardItemModel()
        for slot in enemy_slots:
            item = QStandardItem(str(slot))
            item.setEditable(False)
            self.enemy_slots_model.appendRow(item)
        self.ui.listEnemySlots.setModel(self.enemy_slots_model)

    def player_list_update(self) -> None:
        """Метод обновляющий список юнитов игрока."""
        self.universal_list_update(
            v_model.show_player_units,
            self.ui.listPlayerUnits)

        self.player_slots_dict = {
            1: self.ui.slot1,
            2: self.ui.slot2,
            3: self.ui.slot3,
            4: self.ui.slot4,
            5: self.ui.slot5,
            6: self.ui.slot6,
        }

        for num, slot in self.player_slots_dict.items():
            self.slot_update(
                self.player_unit_by_slot(num),
                slot)

    def enemy_list_update(self) -> None:
        """Метод обновляющий список юнитов противника."""
        self.universal_list_update(
            v_model.show_enemy_units,
            self.ui.listEnemyUnits)

        self.enemy_slots_dict = {
            1: self.ui.EnemySlot1,
            2: self.ui.EnemySlot2,
            3: self.ui.EnemySlot3,
            4: self.ui.EnemySlot4,
            5: self.ui.EnemySlot5,
            6: self.ui.EnemySlot6,
        }

        for num, slot in self.enemy_slots_dict.items():
            self.slot_update(
                self.enemy_unit_by_slot(num),
                slot)

        # self.ui.listEnemyUnits.setModel(self.enemy_units_model)

    def units_list_update(self) -> None:
        """Метод обновляющий список юнитов."""
        self.universal_list_update(
            v_model.show_all_units,
            self.ui.listAllUnits)

    def check_and_swap(self,
                       num1: int,
                       num2: int,
                       db_table: any) -> None:
        """
        Проверить юниты в слотах на наличие и размер.
        Поменять местами вместе с парным юнитом (соседний слот).
        """
        unit1 = v_model.get_unit_by_slot(num1, db_table)
        unit2 = v_model.get_unit_by_slot(num2, db_table)
        func = self.swap_unit_action

        if db_table == CurrentDungeon:
            func = self.swap_enemy_action

        if unit1 is not None \
                and unit2 is not None \
                and unit1.size == BIG \
                and unit2.size == BIG:
            func(num1, num2)

        elif unit1 is not None \
                and unit1.size == BIG:
            if num2 % 2 != 0:
                func(num2, num1 - 1)
                func(num2 + 1, num1)
            elif num2 % 2 == 0:
                func(num2 - 1, num1 - 1)
                func(num2, num1)

        elif unit1 is not None and unit2 is not None \
                and unit2.size == BIG:
            if num1 % 2 != 0:
                func(num1, num2 - 1)
                func(num1 + 1, num2)
            elif num1 % 2 == 0:
                func(num1 - 1, num2 - 1)
                func(num1, num2)

        elif unit1 is not None:
            func(num1, num2)

    def swap_unit_action(self, slot1: int, slot2: int) -> None:
        """Меняет слоты двух юнитов игрока"""
        v_model.update_slot(
            slot1,
            slot2,
            PlayerUnits)
        self.player_list_update()

    def swap_enemy_action(self, slot1: int, slot2: int) -> None:
        """Меняет слоты двух юнитов подземелья"""
        v_model.update_slot(
            slot1,
            slot2,
            CurrentDungeon)
        self.enemy_list_update()

    def delete_unit_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Уволить' у игрока"""
        selected_slot = self.ui.listPlayerSlots.currentIndex().data()
        unit = v_model.get_unit_by_slot(
            selected_slot,
            PlayerUnits)

        if unit is not None:
            global QUESTION_WINDOW
            text = f'Вы действительно хотите уволить {unit.name}?'
            QUESTION_WINDOW = QuestionWindow(self, text)
            QUESTION_WINDOW.show()

    def confirmation(self):
        """Подтверждение 'Увольнения' юнита игрока"""
        if self.question:
            selected_slot = self.ui.listPlayerSlots.currentIndex().data()
            v_model.delete_player_unit(int(selected_slot), PlayerUnits)
            self.player_list_update()

    def delete_enemy_unit_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Уволить' у противника"""
        try:
            selected_slot = self.ui.listEnemySlots.currentIndex().data()
            v_model.delete_dungeon_unit(int(selected_slot))
            self.enemy_list_update()
        except TypeError:
            print('Выберите слот, который хотите освободить')

    def define_hire_active(self, selected: str) -> None:
        """Определение активности кнопок 'Нанять'"""
        if f'{selected}.gif' not in ACTIVE_UNITS:
            ui_lock(self.ui.pushButtonHire)
            ui_lock(self.ui.pushButtonHireEn)
        else:
            ui_unlock(self.ui.pushButtonHire)
            ui_unlock(self.ui.pushButtonHireEn)

    def hire_unit_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Нанять' для игрока"""
        try:
            selected_slot = self.ui.listPlayerSlots.currentIndex().data()
            selected = self.ui.listAllUnits.currentIndex().data()
            v_model.hire_unit_common(
                selected,
                int(selected_slot),
                PlayerUnits)
            self.player_list_update()
        except TypeError:
            print('Выберите номер слота для найма')

    def hire_enemy_unit_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Нанять' для противника"""
        try:
            selected_slot = self.ui.listEnemySlots.currentIndex().data()
            selected = self.ui.listAllUnits.currentIndex().data()
            v_model.hire_unit_common(
                selected,
                int(selected_slot),
                CurrentDungeon)
            self.enemy_list_update()
        except TypeError:
            print('Выберите номер слота для найма')

    def show_available_units(self, slot: int) -> None:
        """Метод показывающий доступных для покупки
        юнитов данной фракции."""
        global HIRE_WINDOW
        HIRE_WINDOW = HireMenuWindow(slot, self)
        HIRE_WINDOW.show()

        print('Показать доступных для покупки юнитов данной фракции')

    def show_fight_window(self) -> None:
        """Метод создающий окно Битвы."""
        global FIGHT_WINDOW
        FIGHT_WINDOW = FightWindow('darkest', PlayerUnits, self)
        FIGHT_WINDOW.show()

    def show_campaign_window(self) -> None:
        """Метод создающий окно выбора Кампаний."""
        global CAMPAIGN_WINDOW
        CAMPAIGN_WINDOW = CampaignWindow(self)
        CAMPAIGN_WINDOW.show()

    def show_versus_window(self) -> None:
        """Метод создающий окно Битвы."""
        v_model.transfer_units()
        self.reset()

        global FIGHT_WINDOW
        FIGHT_WINDOW = FightWindow('versus', PlayerUnits, self)
        FIGHT_WINDOW.show()

    def show_capital(self) -> None:
        """Метод создающий окно Столицы игрока."""
        if v_model.current_player is not None:
            global CAPITAL_WINDOW
            CAPITAL_WINDOW = CapitalWindow(self)
            CAPITAL_WINDOW.show()
        else:
            print('Сначала выберите игрока')

    def show_choose_race(self) -> None:
        """Метод создающий окно выбора фракции игрока."""
        if v_model.current_player is not None:
            global CHOOSE_WINDOW
            CHOOSE_WINDOW = ChooseRaceWindow(self)
            CHOOSE_WINDOW.show()
        else:
            print('Сначала выберите игрока')

    def all_players_list_update(self) -> None:
        """Обновление списка всех игроков"""
        self.universal_list_update(
            v_model.show_all_players,
            self.ui.PlayersList)

    def universal_list_update(self,
                              function: Callable,
                              ui_items_list: QListView) -> None:
        """Метод обновляющий список чего-нибудь."""
        all_items = function()

        self.items_model = QStandardItemModel()
        for i in all_items:
            item = QStandardItem(i.name)
            item.setEditable(False)
            self.items_model.appendRow(item)
        ui_items_list.setModel(self.items_model)

    def add_player_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Добавить игрока'"""
        v_model.create_player(
            self.ui.PlayerName.toPlainText(),
            self.ui.Email.toPlainText())
        self.all_players_list_update()

    def delete_player_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Удалить игрока'"""
        selected = self.ui.PlayersList.currentIndex().data()
        v_model.delete_player(selected)
        self.all_players_list_update()

    def choose_player_action(self) -> None:
        """Метод обработчик нажатия кнопки 'Выбрать игрока'"""
        selected = self.ui.PlayersList.currentIndex().data()
        v_model.choose_player(selected)

        self.ui.currentPlayer.setText(selected)
        self.ui.currentPlayer.setStyleSheet('color: white')
        self.all_players_list_update()

    def slot_detailed(self, unit: namedtuple, slot_dialog: any) -> None:
        """Метод создающий окно юнита игрока при нажатии на слот."""
        try:
            global DETAIL_WINDOW
            DETAIL_WINDOW = slot_dialog(
                unit)
            DETAIL_WINDOW.show()
        except AttributeError:
            pass

    def slot1_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 1)."""
        unit = v_model.get_unit_by_slot(1, PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot2_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 2)."""
        unit = v_model.get_unit_by_slot(2, PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot3_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 3)."""
        unit = v_model.get_unit_by_slot(3, PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot4_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 4)."""
        unit = v_model.get_unit_by_slot(4, PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot5_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 5)."""
        unit = v_model.get_unit_by_slot(5, PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def slot6_detailed(self) -> None:
        """Метод создающий окно юнита игрока (слот 6)."""
        unit = v_model.get_unit_by_slot(6, PlayerUnits)
        self.slot_detailed(unit, UnitDialog)

    def en_slot1_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 1)."""
        unit = v_model.get_unit_by_slot(1, CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot2_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 2)."""
        unit = v_model.get_unit_by_slot(2, CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot3_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 3)."""
        unit = v_model.get_unit_by_slot(3, CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot4_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 4)."""
        unit = v_model.get_unit_by_slot(4, CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot5_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 5)."""
        unit = v_model.get_unit_by_slot(5, CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    def en_slot6_detailed(self) -> None:
        """Метод создающий окно вражеского юнита (слот 6)."""
        unit = v_model.get_unit_by_slot(6, CurrentDungeon)
        self.slot_detailed(unit, UnitDialog)

    @staticmethod
    def player_unit_by_slot(slot: int) -> namedtuple:
        """Метод получающий юнита игрока по слоту."""
        return v_model.get_unit_by_slot(
            slot,
            PlayerUnits)

    @staticmethod
    def enemy_unit_by_slot(slot: int) -> namedtuple:
        """Метод получающий вражеского юнита по слоту."""
        return v_model.get_unit_by_slot(
            slot,
            CurrentDungeon)

    @staticmethod
    def upgrade_slot1_unit():
        unit = v_model.get_unit_by_slot(1, PlayerUnits)
        if unit is not None:
            Unit(unit).upgrade_stats(PlayerUnits)

    @staticmethod
    def downgrade_slot1_unit():
        unit = v_model.get_unit_by_slot(1, PlayerUnits)
        if unit is not None:
            Unit(unit).downgrade_player_stats()

    @staticmethod
    def upgrade_slot2_unit():
        unit = v_model.get_unit_by_slot(2, PlayerUnits)
        if unit is not None:
            Unit(unit).upgrade_stats(PlayerUnits)

    @staticmethod
    def downgrade_slot2_unit():
        unit = v_model.get_unit_by_slot(2, PlayerUnits)
        if unit is not None:
            Unit(unit).downgrade_player_stats()

    @staticmethod
    def upgrade_slot3_unit():
        unit = v_model.get_unit_by_slot(3, PlayerUnits)
        if unit is not None:
            Unit(unit).upgrade_stats(PlayerUnits)

    @staticmethod
    def downgrade_slot3_unit():
        unit = v_model.get_unit_by_slot(3, PlayerUnits)
        if unit is not None:
            Unit(unit).downgrade_player_stats()

    @staticmethod
    def upgrade_slot4_unit():
        unit = v_model.get_unit_by_slot(4, PlayerUnits)
        if unit is not None:
            Unit(unit).upgrade_stats(PlayerUnits)

    @staticmethod
    def downgrade_slot4_unit():
        unit = v_model.get_unit_by_slot(4, PlayerUnits)
        if unit is not None:
            Unit(unit).downgrade_player_stats()

    @staticmethod
    def upgrade_slot5_unit():
        unit = v_model.get_unit_by_slot(5, PlayerUnits)
        if unit is not None:
            Unit(unit).upgrade_stats(PlayerUnits)

    @staticmethod
    def downgrade_slot5_unit():
        unit = v_model.get_unit_by_slot(5, PlayerUnits)
        if unit is not None:
            Unit(unit).downgrade_player_stats()

    @staticmethod
    def upgrade_slot6_unit():
        unit = v_model.get_unit_by_slot(6, PlayerUnits)
        if unit is not None:
            Unit(unit).upgrade_stats(PlayerUnits)

    @staticmethod
    def downgrade_slot6_unit():
        unit = v_model.get_unit_by_slot(6, PlayerUnits)
        if unit is not None:
            Unit(unit).downgrade_player_stats()

    @staticmethod
    def upgrade_enemy_slot1_unit():
        unit = v_model.get_unit_by_slot(1, CurrentDungeon)
        if unit is not None:
            Unit(unit).upgrade_stats(CurrentDungeon)

    @staticmethod
    def downgrade_enemy_slot1_unit():
        unit = v_model.get_unit_by_slot(1, CurrentDungeon)
        if unit is not None:
            Unit(unit).downgrade_enemy_stats()

    @staticmethod
    def upgrade_enemy_slot2_unit():
        unit = v_model.get_unit_by_slot(2, CurrentDungeon)
        if unit is not None:
            Unit(unit).upgrade_stats(CurrentDungeon)

    @staticmethod
    def downgrade_enemy_slot2_unit():
        unit = v_model.get_unit_by_slot(2, CurrentDungeon)
        if unit is not None:
            Unit(unit).downgrade_enemy_stats()

    @staticmethod
    def upgrade_enemy_slot3_unit():
        unit = v_model.get_unit_by_slot(3, CurrentDungeon)
        if unit is not None:
            Unit(unit).upgrade_stats(CurrentDungeon)

    @staticmethod
    def downgrade_enemy_slot3_unit():
        unit = v_model.get_unit_by_slot(3, CurrentDungeon)
        if unit is not None:
            Unit(unit).downgrade_enemy_stats()

    @staticmethod
    def upgrade_enemy_slot4_unit():
        unit = v_model.get_unit_by_slot(4, CurrentDungeon)
        if unit is not None:
            Unit(unit).upgrade_stats(CurrentDungeon)

    @staticmethod
    def downgrade_enemy_slot4_unit():
        unit = v_model.get_unit_by_slot(4, CurrentDungeon)
        if unit is not None:
            Unit(unit).downgrade_enemy_stats()

    @staticmethod
    def upgrade_enemy_slot5_unit():
        unit = v_model.get_unit_by_slot(5, CurrentDungeon)
        if unit is not None:
            Unit(unit).upgrade_stats(CurrentDungeon)

    @staticmethod
    def downgrade_enemy_slot5_unit():
        unit = v_model.get_unit_by_slot(5, CurrentDungeon)
        if unit is not None:
            Unit(unit).downgrade_enemy_stats()

    @staticmethod
    def upgrade_enemy_slot6_unit():
        unit = v_model.get_unit_by_slot(6, CurrentDungeon)
        if unit is not None:
            Unit(unit).upgrade_stats(CurrentDungeon)

    @staticmethod
    def downgrade_enemy_slot6_unit():
        unit = v_model.get_unit_by_slot(6, CurrentDungeon)
        if unit is not None:
            Unit(unit).downgrade_enemy_stats()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClientMainWindow()
    sys.exit(app.exec_())

    # with mgr():
    #     app = QApplication(sys.argv)
    #     ex = ClientMainWindow()
    #     p1 = Process(target=ex)
    #
    #     p1.start()
    #     sys.exit(app.exec_())
