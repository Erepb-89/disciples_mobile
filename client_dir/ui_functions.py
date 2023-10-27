"""UI static functions"""

import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QMovie, QPixmap

from client_dir.settings import UNIT_ICONS, PLUG, ICON, GIF_ANIMATIONS, \
    HIRE_SCREEN, COMMON, UNIT_STAND, BIG, SPEED
from units_dir.buildings import FACTIONS


def get_image(folder: str, faction: str):
    """Достаем картинку фракции из указанной папки"""
    return os.path.join(folder, f"{faction}.png")


def set_size_by_unit(unit: any, ui_obj: any):
    """Установка размера иконки по размеру самого юнита"""
    try:
        if unit.size == BIG:
            ui_obj.setFixedWidth(225)
            ui_obj.setFixedHeight(127)
        else:
            ui_obj.setFixedWidth(105)
            ui_obj.setFixedHeight(127)
    except (TypeError, AttributeError):
        ui_obj.setFixedWidth(105)
        ui_obj.setFixedHeight(127)


def get_unit_image(unit: any):
    """Получение иконки юнита"""
    try:
        return os.path.join(
            UNIT_ICONS,
            f"{unit.name} {ICON}")
    except AttributeError:
        return os.path.join(
            UNIT_ICONS, PLUG)


def show_gif(unit: any, gif_label: QtWidgets.QLabel):
    """Установка gif'ки общего вида юнита"""
    gif = QMovie(os.path.join(
        GIF_ANIMATIONS, f"{unit.name}.gif"))
    gif_label.setMovie(gif)
    gif.start()


def slot_frame_update(unit: any, slot_frame: QtWidgets.QLabel) -> None:
    """Метод выравнивания рамки под размер иконки юнита"""
    if unit.size == BIG:
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


def slot_update(unit: any, slot: QtWidgets.QLabel) -> None:
    """Метод обновления иконки, либо GIF"""
    set_size_by_unit(unit, slot)

    slot.setPixmap(QPixmap(
        get_unit_image(unit)).scaled(
        slot.width(), slot.height()))


def button_update(unit: any, button: QtWidgets.QPushButton) -> None:
    """Установка размера кнопки на иконке"""
    set_size_by_unit(unit, button)


def show_green_frame(gif_slot: QtWidgets.QLabel) -> None:
    """Обновление зеленой рамки в слоте"""
    gif_slot.setStyleSheet("border: 4px solid green;")


def show_blue_frame(gif_slot: QtWidgets.QLabel) -> None:
    """Обновление зеленой рамки в слоте"""
    gif_slot.setStyleSheet("border: 4px solid blue;")


def show_red_frame(gif_slot: QtWidgets.QLabel) -> None:
    """Обновление красной рамки в слоте"""
    gif_slot.setStyleSheet("border: 4px solid darkred;")


def show_no_frame(gif_slot: QtWidgets.QLabel) -> None:
    """Убрать рамки в слоте"""
    gif_slot.setStyleSheet("border: 0px;")


def show_damage(icon_slot: QtWidgets.QLabel) -> None:
    """Метод показывающий нанесенный урон"""
    icon_slot.setPixmap(QPixmap(os.path.join(COMMON, "fire.gif")))


def show_no_damage(icon_slot: QtWidgets.QLabel) -> None:
    """Метод скрывающий нанесенный урон на иконке"""
    # icon_slot.setText("0")
    icon_slot.setPixmap(QPixmap(os.path.join(COMMON, "transparent.gif")))


def update_unit_health(unit: any, slot: QtWidgets.QLabel) -> None:
    """Обновление здоровья юнита"""
    try:
        slot.setText(f'{unit.curr_health}/{unit.health}')
    except AttributeError:
        slot.setText('')


def get_unit_faction(unit: any) -> str:
    """Получение фракции юнита"""
    try:
        for faction, f_building in FACTIONS.items():
            for branch in f_building.values():
                for building in branch.values():
                    if unit.name == building.unit_name:
                        return faction
        return 'is_dead'
    except AttributeError:
        return ''


def show_gif_side(unit: any,
                  gif_slot: QtWidgets.QLabel,
                  action: str,
                  side: str) -> None:
    """Обновление GIF в слоте"""
    if unit is None:
        gif = QMovie(
            os.path.join(
                UNIT_STAND,
                f"{side}/empty.gif"))
        gif.setSpeed(SPEED)

    # анимация смерти
    elif unit.curr_health == 0:
        unit_faction = get_unit_faction(unit)
        gif = QMovie(
            os.path.join(
                action,
                f"{side}/{unit_faction}.gif"))
        gif.setSpeed(SPEED)
    # if unit.curr_health == 0:
    #     gif = QMovie(os.path.join(COMMON, "skull.png"))

    # анимация действия
    else:
        gif = QMovie(
            os.path.join(
                action,
                f"{side}{unit.name}.gif"))
        gif.setSpeed(SPEED)

    gif_slot.setMovie(gif)
    gif.start()


def set_beige_colour(button: QtWidgets.QPushButton):
    """Подкраска элементов в бежевый цвет"""
    button.setStyleSheet("background-color: rgb(181, 172, 155)")


def set_borders(ui_obj: QtWidgets.QPushButton):
    """Стиль и цвет рамок (коричневый с бежевым)"""
    ui_obj.setStyleSheet("border: 3px solid;"
                         "border-top-color: rgb(65, 3, 2);"
                         "border-left-color: rgb(65, 3, 2);"
                         "border-right-color: rgb(181, 172, 155);"
                         "border-bottom-color: rgb(181, 172, 155)")
