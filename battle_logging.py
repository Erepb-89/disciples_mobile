"""Логирование"""
from client_dir.settings import BATTLE_LOG


def logging(line):
    with open(BATTLE_LOG, 'r+', encoding='utf-8') as file:
        log_data = file.read()
        file.seek(0, 0)
        file.write(f'{line}{log_data}')
