import sys
from PyQt5 import QtWidgets


class Dialog(QtWidgets.QDialog):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.main = root
        label = QtWidgets.QLabel('введите что нибудь')
        self.edit = QtWidgets.QLineEdit()
        button = QtWidgets.QPushButton('Нажми чтобы отобразить')
        button.clicked.connect(self.push)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.edit)
        layout.addWidget(button)
        self.setLayout(layout)

    def push(self):
        self.main.label_main.setText(self.edit.text())
        self.close()


class Main(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = Dialog(self)
        layout = QtWidgets.QHBoxLayout()
        self.label_main = QtWidgets.QLabel()
        button = QtWidgets.QPushButton('Нажми')
        button.clicked.connect(self.dialog.exec)
        layout.addWidget(self.label_main)
        layout.addWidget(button)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())