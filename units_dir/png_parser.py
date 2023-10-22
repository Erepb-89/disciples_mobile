"""town_icons png parser"""
import os

from client_dir.settings import ORIGINAL_PNGS


def read_directory():
    factions = os.listdir(ORIGINAL_PNGS)
    for faction in factions:
        current_path = os.path.join(ORIGINAL_PNGS, faction)
        for folder in os.listdir(current_path):
            folder_path = f'{current_path}/{folder}'
            pics = os.listdir(folder_path)

            for pic in pics:
                print(pic, pics.index(pic))
                os.rename(
                    f'{folder_path}/{pic}',
                    f'{folder_path}/{pics.index(pic) + 1}.png'
                )


# Раскладка по папкам
if __name__ == '__main__':
    read_directory()
