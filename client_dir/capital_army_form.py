# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'capital_army.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CapitalArmyWindow(object):
    def setupUi(self, CapitalArmyWindow):
        CapitalArmyWindow.setObjectName("CapitalArmyWindow")
        CapitalArmyWindow.resize(1600, 900)
        CapitalArmyWindow.setWindowTitle("CapitalArmyWindow")
        self.centralwidget = QtWidgets.QWidget(CapitalArmyWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.capitalArmyBG = QtWidgets.QLabel(self.centralwidget)
        self.capitalArmyBG.setGeometry(QtCore.QRect(0, 0, 28, 41))
        self.capitalArmyBG.setMinimumSize(QtCore.QSize(13, 13))
        self.capitalArmyBG.setMaximumSize(QtCore.QSize(1600, 900))
        self.capitalArmyBG.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.capitalArmyBG.setAutoFillBackground(True)
        self.capitalArmyBG.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.capitalArmyBG.setFrameShadow(QtWidgets.QFrame.Plain)
        self.capitalArmyBG.setLineWidth(3)
        self.capitalArmyBG.setMidLineWidth(0)
        self.capitalArmyBG.setObjectName("capitalArmyBG")
        self.pushButtonBack = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonBack.setGeometry(QtCore.QRect(1360, 790, 40, 40))
        self.pushButtonBack.setToolTipDuration(3000)
        self.pushButtonBack.setAutoFillBackground(False)
        self.pushButtonBack.setText("")
        self.pushButtonBack.setFlat(True)
        self.pushButtonBack.setObjectName("pushButtonBack")
        self.pushButtonDelete = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDelete.setGeometry(QtCore.QRect(778, 832, 40, 40))
        self.pushButtonDelete.setToolTipDuration(3000)
        self.pushButtonDelete.setAutoFillBackground(False)
        self.pushButtonDelete.setText("")
        self.pushButtonDelete.setFlat(True)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.pushButtonStop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStop.setGeometry(QtCore.QRect(607, 797, 40, 40))
        self.pushButtonStop.setToolTipDuration(3000)
        self.pushButtonStop.setAutoFillBackground(False)
        self.pushButtonStop.setText("")
        self.pushButtonStop.setFlat(True)
        self.pushButtonStop.setObjectName("pushButtonStop")
        self.listPlayerUnits = QtWidgets.QListView(self.centralwidget)
        self.listPlayerUnits.setEnabled(False)
        self.listPlayerUnits.setGeometry(QtCore.QRect(357, 750, 171, 141))
        self.listPlayerUnits.setObjectName("listPlayerUnits")
        self.listPlayerSlots = QtWidgets.QListView(self.centralwidget)
        self.listPlayerSlots.setGeometry(QtCore.QRect(537, 750, 51, 141))
        self.listPlayerSlots.setObjectName("listPlayerSlots")
        self.slot2 = QtWidgets.QLabel(self.centralwidget)
        self.slot2.setGeometry(QtCore.QRect(605, 100, 105, 127))
        self.slot2.setMinimumSize(QtCore.QSize(105, 127))
        self.slot2.setMaximumSize(QtCore.QSize(224, 127))
        self.slot2.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot2.setLineWidth(1)
        self.slot2.setMidLineWidth(0)
        self.slot2.setObjectName("slot2")
        self.slot5 = QtWidgets.QLabel(self.centralwidget)
        self.slot5.setGeometry(QtCore.QRect(488, 420, 105, 127))
        self.slot5.setMinimumSize(QtCore.QSize(105, 127))
        self.slot5.setMaximumSize(QtCore.QSize(224, 127))
        self.slot5.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot5.setLineWidth(1)
        self.slot5.setMidLineWidth(0)
        self.slot5.setObjectName("slot5")
        self.slot6 = QtWidgets.QLabel(self.centralwidget)
        self.slot6.setGeometry(QtCore.QRect(605, 420, 105, 127))
        self.slot6.setMinimumSize(QtCore.QSize(105, 127))
        self.slot6.setMaximumSize(QtCore.QSize(224, 127))
        self.slot6.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot6.setLineWidth(1)
        self.slot6.setMidLineWidth(0)
        self.slot6.setObjectName("slot6")
        self.slot3 = QtWidgets.QLabel(self.centralwidget)
        self.slot3.setGeometry(QtCore.QRect(488, 260, 105, 127))
        self.slot3.setMinimumSize(QtCore.QSize(105, 127))
        self.slot3.setMaximumSize(QtCore.QSize(224, 127))
        self.slot3.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot3.setLineWidth(1)
        self.slot3.setMidLineWidth(0)
        self.slot3.setObjectName("slot3")
        self.slot4 = QtWidgets.QLabel(self.centralwidget)
        self.slot4.setGeometry(QtCore.QRect(605, 260, 105, 127))
        self.slot4.setMinimumSize(QtCore.QSize(105, 127))
        self.slot4.setMaximumSize(QtCore.QSize(224, 127))
        self.slot4.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot4.setLineWidth(1)
        self.slot4.setMidLineWidth(0)
        self.slot4.setObjectName("slot4")
        self.slot1 = QtWidgets.QLabel(self.centralwidget)
        self.slot1.setGeometry(QtCore.QRect(488, 100, 105, 127))
        self.slot1.setMinimumSize(QtCore.QSize(105, 127))
        self.slot1.setMaximumSize(QtCore.QSize(224, 127))
        self.slot1.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot1.setLineWidth(1)
        self.slot1.setMidLineWidth(0)
        self.slot1.setObjectName("slot1")
        self.pushButtonSlot1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot1.setGeometry(QtCore.QRect(490, 100, 104, 127))
        self.pushButtonSlot1.setText("")
        self.pushButtonSlot1.setFlat(True)
        self.pushButtonSlot1.setObjectName("pushButtonSlot1")
        self.pushButtonSlot6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot6.setGeometry(QtCore.QRect(607, 420, 104, 127))
        self.pushButtonSlot6.setText("")
        self.pushButtonSlot6.setFlat(True)
        self.pushButtonSlot6.setObjectName("pushButtonSlot6")
        self.pushButtonSlot4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot4.setGeometry(QtCore.QRect(607, 260, 104, 127))
        self.pushButtonSlot4.setText("")
        self.pushButtonSlot4.setFlat(True)
        self.pushButtonSlot4.setObjectName("pushButtonSlot4")
        self.pushButtonSlot5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot5.setGeometry(QtCore.QRect(490, 420, 104, 127))
        self.pushButtonSlot5.setText("")
        self.pushButtonSlot5.setFlat(True)
        self.pushButtonSlot5.setObjectName("pushButtonSlot5")
        self.pushButtonSlot3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot3.setGeometry(QtCore.QRect(490, 260, 104, 127))
        self.pushButtonSlot3.setText("")
        self.pushButtonSlot3.setFlat(True)
        self.pushButtonSlot3.setObjectName("pushButtonSlot3")
        self.pushButtonSlot2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot2.setGeometry(QtCore.QRect(607, 100, 104, 127))
        self.pushButtonSlot2.setText("")
        self.pushButtonSlot2.setFlat(True)
        self.pushButtonSlot2.setObjectName("pushButtonSlot2")
        self.hpSlot2 = QtWidgets.QLabel(self.centralwidget)
        self.hpSlot2.setGeometry(QtCore.QRect(608, 234, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.hpSlot2.setFont(font)
        self.hpSlot2.setAlignment(QtCore.Qt.AlignCenter)
        self.hpSlot2.setObjectName("hpSlot2")
        self.hpSlot6 = QtWidgets.QLabel(self.centralwidget)
        self.hpSlot6.setGeometry(QtCore.QRect(608, 552, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.hpSlot6.setFont(font)
        self.hpSlot6.setAlignment(QtCore.Qt.AlignCenter)
        self.hpSlot6.setObjectName("hpSlot6")
        self.hpSlot5 = QtWidgets.QLabel(self.centralwidget)
        self.hpSlot5.setGeometry(QtCore.QRect(486, 552, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.hpSlot5.setFont(font)
        self.hpSlot5.setAlignment(QtCore.Qt.AlignCenter)
        self.hpSlot5.setObjectName("hpSlot5")
        self.hpSlot4 = QtWidgets.QLabel(self.centralwidget)
        self.hpSlot4.setGeometry(QtCore.QRect(608, 393, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.hpSlot4.setFont(font)
        self.hpSlot4.setAlignment(QtCore.Qt.AlignCenter)
        self.hpSlot4.setObjectName("hpSlot4")
        self.hpSlot1 = QtWidgets.QLabel(self.centralwidget)
        self.hpSlot1.setGeometry(QtCore.QRect(486, 234, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.hpSlot1.setFont(font)
        self.hpSlot1.setAlignment(QtCore.Qt.AlignCenter)
        self.hpSlot1.setObjectName("hpSlot1")
        self.hpSlot3 = QtWidgets.QLabel(self.centralwidget)
        self.hpSlot3.setGeometry(QtCore.QRect(486, 393, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.hpSlot3.setFont(font)
        self.hpSlot3.setAlignment(QtCore.Qt.AlignCenter)
        self.hpSlot3.setObjectName("hpSlot3")
        self.capitalArmyBG.raise_()
        self.pushButtonBack.raise_()
        self.pushButtonDelete.raise_()
        self.pushButtonStop.raise_()
        self.listPlayerUnits.raise_()
        self.listPlayerSlots.raise_()
        self.hpSlot2.raise_()
        self.hpSlot6.raise_()
        self.hpSlot5.raise_()
        self.hpSlot4.raise_()
        self.hpSlot1.raise_()
        self.hpSlot3.raise_()
        self.slot1.raise_()
        self.slot5.raise_()
        self.slot3.raise_()
        self.slot6.raise_()
        self.slot4.raise_()
        self.slot2.raise_()
        self.pushButtonSlot5.raise_()
        self.pushButtonSlot3.raise_()
        self.pushButtonSlot1.raise_()
        self.pushButtonSlot4.raise_()
        self.pushButtonSlot6.raise_()
        self.pushButtonSlot2.raise_()
        CapitalArmyWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CapitalArmyWindow)
        QtCore.QMetaObject.connectSlotsByName(CapitalArmyWindow)

    def retranslateUi(self, CapitalArmyWindow):
        _translate = QtCore.QCoreApplication.translate
        self.capitalArmyBG.setText(_translate("CapitalArmyWindow", "bg"))
        self.pushButtonBack.setToolTip(_translate("CapitalArmyWindow", "Выход"))
        self.pushButtonDelete.setToolTip(_translate("CapitalArmyWindow", "Уволить воина (D)"))
        self.pushButtonStop.setToolTip(_translate("CapitalArmyWindow", "Заблокировать тип воина (L)"))
        self.slot2.setText(_translate("CapitalArmyWindow", "slot_2"))
        self.slot5.setText(_translate("CapitalArmyWindow", "slot_5"))
        self.slot6.setText(_translate("CapitalArmyWindow", "slot_6"))
        self.slot3.setText(_translate("CapitalArmyWindow", "slot_3"))
        self.slot4.setText(_translate("CapitalArmyWindow", "slot_4"))
        self.slot1.setText(_translate("CapitalArmyWindow", "slot_1"))
        self.hpSlot2.setText(_translate("CapitalArmyWindow", "hpSlot2"))
        self.hpSlot6.setText(_translate("CapitalArmyWindow", "hpSlot6"))
        self.hpSlot5.setText(_translate("CapitalArmyWindow", "hpSlot5"))
        self.hpSlot4.setText(_translate("CapitalArmyWindow", "hpSlot4"))
        self.hpSlot1.setText(_translate("CapitalArmyWindow", "hpSlot1"))
        self.hpSlot3.setText(_translate("CapitalArmyWindow", "hpSlot3"))
