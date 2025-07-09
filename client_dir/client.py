# Программа клиента для отправки приветствия серверу и получения ответа
import json
from socket import *

from PyQt5 import QtCore


class MyThread(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        self._stopped = True

    def run(self):
        self._stopped = False
        print('client start')
        self.client_connect()

    def client_connect(self):
        while not self._stopped:
            try:
                s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
                s.connect(('localhost', 9595))  # Соединиться с сервером

                msg_json = {
                    'client_name': 'Erepb',
                    'IP': '127.0.0.1'
                }

                s.send((json.dumps(msg_json,
                                   indent=4,
                                   ensure_ascii=False)).encode())
                data = s.recv(1000000)
                print(f"Сообщение от сервера: {data.decode('utf-8')} длиной {len(data)} байт")
                s.close()

            except ConnectionRefusedError:
                print(f'Невозможно подключиться к 127.0.0.1')

    def stop(self):
        self._stopped = True
        print('server stop')