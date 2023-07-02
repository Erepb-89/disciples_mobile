"""UI static functions"""

import os
import random

from PyQt5.QtGui import QMovie, QPixmap

from client_dir.settings import UNIT_ICONS, PLUG, ICON, GIF_ANIMATIONS, HIRE_SCREEN


def set_size_by_unit(unit, ui_obj):
    """Установка размера иконки по размеру самого юнита"""
    try:
        if unit.size == "Большой":
            ui_obj.setFixedWidth(225)
            ui_obj.setFixedHeight(127)
        else:
            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)
    except BaseException:
        ui_obj.setFixedWidth(105)
        ui_obj.setFixedHeight(127)


def get_unit_image(unit):
    """Получение иконки юнита"""
    try:
        return os.path.join(
            UNIT_ICONS,
            f"{unit.name} {ICON}")
    except BaseException:
        return os.path.join(
            UNIT_ICONS, PLUG)


def show_gif(unit, gif_label):
    """Установка gif'ки общего вида юнита"""
    try:
        gif = QMovie(os.path.join(
            GIF_ANIMATIONS, f"{unit.name}.gif"))
        gif_label.setMovie(gif)
        gif.start()
    except BaseException:
        gif_label.setPixmap(QPixmap(os.path.join(
            UNIT_ICONS, PLUG)))


def slot_frame_update(unit, slot_frame):
    """Метод выравнивания рамки под размер иконки юнита"""
    if unit.size == "Большой":
        slot_frame.setPixmap(
            QPixmap(
                os.path.join(
                    HIRE_SCREEN,
                    "hire_lbl_big.png")))
        slot_frame.setFixedWidth(246)
        slot_frame.setFixedHeight(149)
    else:
        slot_frame.setPixmap(
            QPixmap(
                os.path.join(
                    HIRE_SCREEN,
                    "hire_lbl_small.png")))
        slot_frame.setFixedWidth(125)
        slot_frame.setFixedHeight(149)

# def slot_update(self, unit, slot):
#     """Установка gif'ки в иконку юнита"""
#     self.set_size_by_unit(unit, slot)
#
#     slot.setPixmap(QPixmap(
#         get_unit_image(unit)).scaled(
#         slot.width(), slot.height()))
#     self.hbox.addWidget(slot)
#     self.setLayout(self.hbox)
