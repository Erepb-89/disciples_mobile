import sys
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import QtCore


class TableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent)
        self.mouse_press = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mouse_press = "mouse left press"
        elif event.button() == QtCore.Qt.RightButton:
            self.mouse_press = "mouse right press"
        elif event.button() == QtCore.Qt.MidButton:
            self.mouse_press = "mouse middle press"
        super(TableWidget, self).mousePressEvent(event)


class Example(QDialog):
    def __init__(self):
        super().__init__()

        self.tableWidget = TableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)

        # Этот сигнал испускается всякий раз, когда ячейка в таблице нажата.
        # Указанная строка и столбец - это ячейка, которая была нажата.
        self.tableWidget.cellPressed[int, int].connect(self.clickedRowColumn)

        for i in range(4):
            for j in range(2):
                item = QTableWidgetItem("Item {}-{}".format(i, j))
                item.setTextAlignment(QtCore.Qt.AlignHCenter)
                self.tableWidget.setItem(i, j, item)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tableWidget)

    def clickedRowColumn(self, r, c):
        print("{}: row={}, column={}".format(self.tableWidget.mouse_press, r, c))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())