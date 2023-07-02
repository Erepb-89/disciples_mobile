"""units gif parser"""
import os
from copy import copy

from client_dir.settings import ORIGINAL_GIFS, \
    TESTING_UNIT_ATTACKED, FRONT, REAR, TESTING_UNIT_SHADOW_ATTACKED, \
    TESTING_UNIT_ATTACK, TESTING_UNIT_EFFECTS_ATTACK, TESTING_UNIT_SHADOW_ATTACK, \
    TESTING_UNIT_STAND, TESTING_UNIT_SHADOW_STAND, TESTING_UNIT_EFFECTS_AREA, TESTING_UNIT_EFFECTS_TARGET


def read_directory():
    folders = os.listdir(ORIGINAL_GIFS)
    for folder in folders:
        # print(folder)
        if '14' in folder and '_Добавить_' not in folder and 'Hero' not in folder:
            unit_name = folder.split('14')[0]
            print(unit_name)
            current_path = os.path.join(ORIGINAL_GIFS, folder)
            gif_number = os.listdir(current_path)

            os.rename(
                f'{current_path}/{gif_number[0]}',
                f'{TESTING_UNIT_ATTACKED}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[1]}',
                f'{TESTING_UNIT_ATTACKED}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[2]}',
                f'{TESTING_UNIT_SHADOW_ATTACKED}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[3]}',
                f'{TESTING_UNIT_SHADOW_ATTACKED}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[4]}',
                f'{TESTING_UNIT_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[5]}',
                f'{TESTING_UNIT_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[6]}',
                f'{TESTING_UNIT_EFFECTS_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[7]}',
                f'{TESTING_UNIT_EFFECTS_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[8]}',
                f'{TESTING_UNIT_SHADOW_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[9]}',
                f'{TESTING_UNIT_SHADOW_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[10]}',
                f'{TESTING_UNIT_STAND}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[11]}',
                f'{TESTING_UNIT_STAND}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[12]}',
                f'{TESTING_UNIT_SHADOW_STAND}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[13]}',
                f'{TESTING_UNIT_SHADOW_STAND}{REAR}{unit_name}.gif')

        if '15' in folder and 'all' in folder \
                and '_Добавить_' not in folder and 'Hero' not in folder:
            unit_name = folder.split('15')[0]
            print(unit_name)
            current_path = os.path.join(ORIGINAL_GIFS, folder)
            gif_number = os.listdir(current_path)

            os.rename(
                f'{current_path}/{gif_number[0]}',
                f'{TESTING_UNIT_EFFECTS_AREA}{FRONT}{unit_name}.gif')
            print(f'Перенести в REAR: {TESTING_UNIT_EFFECTS_AREA}{FRONT}{unit_name}.gif\n')
            os.rename(
                f'{current_path}/{gif_number[1]}',
                f'{TESTING_UNIT_ATTACKED}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[2]}',
                f'{TESTING_UNIT_ATTACKED}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[3]}',
                f'{TESTING_UNIT_SHADOW_ATTACKED}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[4]}',
                f'{TESTING_UNIT_SHADOW_ATTACKED}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[5]}',
                f'{TESTING_UNIT_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[6]}',
                f'{TESTING_UNIT_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[7]}',
                f'{TESTING_UNIT_EFFECTS_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[8]}',
                f'{TESTING_UNIT_EFFECTS_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[9]}',
                f'{TESTING_UNIT_SHADOW_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[10]}',
                f'{TESTING_UNIT_SHADOW_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[11]}',
                f'{TESTING_UNIT_STAND}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[12]}',
                f'{TESTING_UNIT_STAND}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[13]}',
                f'{TESTING_UNIT_SHADOW_STAND}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[14]}',
                f'{TESTING_UNIT_SHADOW_STAND}{REAR}{unit_name}.gif')

        if '16' in folder and 'all' in folder and 'double' not in folder \
                and '_Добавить_' not in folder and 'Hero' not in folder \
                and 'side' in folder:
            unit_name = folder.split('16')[0]
            print(unit_name)
            current_path = os.path.join(ORIGINAL_GIFS, folder)
            gif_number = os.listdir(current_path)

            os.rename(
                f'{current_path}/{gif_number[0]}',
                f'{TESTING_UNIT_EFFECTS_AREA}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[1]}',
                f'{TESTING_UNIT_EFFECTS_AREA}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[2]}',
                f'{TESTING_UNIT_ATTACKED}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[3]}',
                f'{TESTING_UNIT_ATTACKED}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[4]}',
                f'{TESTING_UNIT_SHADOW_ATTACKED}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[5]}',
                f'{TESTING_UNIT_SHADOW_ATTACKED}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[6]}',
                f'{TESTING_UNIT_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[7]}',
                f'{TESTING_UNIT_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[8]}',
                f'{TESTING_UNIT_EFFECTS_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[9]}',
                f'{TESTING_UNIT_EFFECTS_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[10]}',
                f'{TESTING_UNIT_SHADOW_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[11]}',
                f'{TESTING_UNIT_SHADOW_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[12]}',
                f'{TESTING_UNIT_STAND}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[13]}',
                f'{TESTING_UNIT_STAND}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[14]}',
                f'{TESTING_UNIT_SHADOW_STAND}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[15]}',
                f'{TESTING_UNIT_SHADOW_STAND}{REAR}{unit_name}.gif')

        if '16' in folder and 'every' in folder and 'double' not in folder \
                and '_Добавить_' not in folder and 'Hero' not in folder \
                and 'side' in folder:
            unit_name = folder.split('16')[0]
            print(unit_name)
            current_path = os.path.join(ORIGINAL_GIFS, folder)
            gif_number = os.listdir(current_path)

            os.rename(
                f'{current_path}/{gif_number[0]}',
                f'{TESTING_UNIT_ATTACKED}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[1]}',
                f'{TESTING_UNIT_ATTACKED}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[2]}',
                f'{TESTING_UNIT_SHADOW_ATTACKED}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[3]}',
                f'{TESTING_UNIT_SHADOW_ATTACKED}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[4]}',
                f'{TESTING_UNIT_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[5]}',
                f'{TESTING_UNIT_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[6]}',
                f'{TESTING_UNIT_EFFECTS_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[7]}',
                f'{TESTING_UNIT_EFFECTS_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[8]}',
                f'{TESTING_UNIT_SHADOW_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[9]}',
                f'{TESTING_UNIT_SHADOW_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[10]}',
                f'{TESTING_UNIT_STAND}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[11]}',
                f'{TESTING_UNIT_STAND}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[12]}',
                f'{TESTING_UNIT_SHADOW_STAND}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[13]}',
                f'{TESTING_UNIT_SHADOW_STAND}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[14]}',
                f'{TESTING_UNIT_EFFECTS_TARGET}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[15]}',
                f'{TESTING_UNIT_EFFECTS_TARGET}{REAR}{unit_name}.gif')


        if '15' in folder and 'every' in folder and 'double' not in folder \
                and '_Добавить_' not in folder and 'Hero' not in folder \
                and 'side' not in folder:
            unit_name = folder.split('15')[0]
            print(unit_name)
            current_path = os.path.join(ORIGINAL_GIFS, folder)
            gif_number = os.listdir(current_path)

            os.rename(
                f'{current_path}/{gif_number[0]}',
                f'{TESTING_UNIT_ATTACKED}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[1]}',
                f'{TESTING_UNIT_ATTACKED}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[2]}',
                f'{TESTING_UNIT_SHADOW_ATTACKED}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[3]}',
                f'{TESTING_UNIT_SHADOW_ATTACKED}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[4]}',
                f'{TESTING_UNIT_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[5]}',
                f'{TESTING_UNIT_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[6]}',
                f'{TESTING_UNIT_EFFECTS_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[7]}',
                f'{TESTING_UNIT_EFFECTS_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[8]}',
                f'{TESTING_UNIT_SHADOW_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[9]}',
                f'{TESTING_UNIT_SHADOW_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[10]}',
                f'{TESTING_UNIT_STAND}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[11]}',
                f'{TESTING_UNIT_STAND}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[12]}',
                f'{TESTING_UNIT_SHADOW_STAND}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[13]}',
                f'{TESTING_UNIT_SHADOW_STAND}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[14]}',
                f'{TESTING_UNIT_EFFECTS_TARGET}{FRONT}{unit_name}.gif')
            print(f'Перенести в REAR: {TESTING_UNIT_EFFECTS_TARGET}{FRONT}{unit_name}.gif\n')


        if '12' in folder and 'without_effects' in folder:
            unit_name = folder.split('12')[0]
            print(unit_name)
            current_path = os.path.join(ORIGINAL_GIFS, folder)
            gif_number = os.listdir(current_path)

            os.rename(
                f'{current_path}/{gif_number[0]}',
                f'{TESTING_UNIT_ATTACKED}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[1]}',
                f'{TESTING_UNIT_ATTACKED}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[2]}',
                f'{TESTING_UNIT_SHADOW_ATTACKED}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[3]}',
                f'{TESTING_UNIT_SHADOW_ATTACKED}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[4]}',
                f'{TESTING_UNIT_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[5]}',
                f'{TESTING_UNIT_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[6]}',
                f'{TESTING_UNIT_SHADOW_ATTACK}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[7]}',
                f'{TESTING_UNIT_SHADOW_ATTACK}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[8]}',
                f'{TESTING_UNIT_STAND}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[9]}',
                f'{TESTING_UNIT_STAND}{REAR}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[10]}',
                f'{TESTING_UNIT_SHADOW_STAND}{FRONT}{unit_name}.gif')
            os.rename(
                f'{current_path}/{gif_number[11]}',
                f'{TESTING_UNIT_SHADOW_STAND}{REAR}{unit_name}.gif')

        if 'Hero' in folder:
            print('Hero', folder)


# Раскладка по папкам
if __name__ == '__main__':
    read_directory()
