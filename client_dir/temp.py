import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5 import QtWidgets


class Button(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)


    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)


    def mousePressEvent(self, e):

        QPushButton.mousePressEvent(self, e)

        if e.button() == Qt.LeftButton:
            print('press')


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setAcceptDrops(True)

        self.button = Button('Button', self)
        self.button.move(100, 65)

        self.setWindowTitle('Click or Move')
        self.setGeometry(800, 600, 880, 600)

        self.label = QLabel('text', self)
        self.setGeometry(500, 500, 280, 150)
        self.label.setFrameShape(QtWidgets.QFrame.Panel)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setLineWidth(3)


    def dragEnterEvent(self, e):

        e.accept()


    def dropEvent(self, e):

        label_pos = self.label.pos()
        print(label_pos)
        position = e.pos()
        if position == label_pos:
            print('yes')
        self.button.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()

# from typing import List
#
#
# class Solution:
#     def twoSum(self, nums: List[int], target: int) -> List[int]:
#         for num1, i in enumerate(nums):
#             for num2, j in enumerate(nums):
#                 if i + j == target and num1 != num2:
#                     return [num1, num2]
#
# sol = Solution
# result = sol.twoSum(sol, [3, 3], 6)
# print(result)
