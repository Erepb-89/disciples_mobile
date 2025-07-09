import json
from socket import *

from PyQt5 import QtCore


class MyThread(QtCore.QObject):
    mysignal1 = QtCore.pyqtSignal(str, object)  # !!!

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        self._stopped = True

    def run(self):
        self._stopped = False
        print('server start')
        self.server_main()

    def server_main(self):
        s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
        s.bind(('', 9595))  # Присваивает порт 9595
        s.listen(5)  # Переходит в режим ожидания запросов;
        # Одновременно обслуживает не более
        # 5 запросов.

        while not self._stopped:  # - True: + self._stopped
            client, addr = s.accept()
            data = client.recv(1000000)
            new_dict = json.loads(data.decode('utf-8'))

            print(f"Игрок: {new_dict['client_name']}, IP:{addr} присоединился к игре ")
            msg = f"Приветствуем в игре, {new_dict['client_name']}"
            client.send(msg.encode('utf-8'))
            client.close()

    def handle_echo(self, reader, writer):
        data = reader.read(1024)
        if not data or data == '':
            print("Message is empty")
            writer.close()

        message = data.decode()
        addr = writer.get_extra_info('peername')

        print(f"Received {message!r} from {addr!r}")
        client_params = json.loads(message)
        print(client_params['client_name'], 'присоединился к игре')

        print(f"Send: {client_params!r}")
        writer.write('1'.encode())
        writer.drain()

        print("Close the connection")
        writer.close()
        writer.wait_closed()

    def stop(self):
        self._stopped = True
        # print('server stop')


