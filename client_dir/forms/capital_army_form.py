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
        self.gold = QtWidgets.QLabel(self.centralwidget)
        self.gold.setGeometry(QtCore.QRect(280, 550, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.gold.setFont(font)
        self.gold.setObjectName("gold")
        self.heroFace = QtWidgets.QLabel(self.centralwidget)
        self.heroFace.setGeometry(QtCore.QRect(180, 30, 241, 241))
        self.heroFace.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.heroFace.setFrameShadow(QtWidgets.QFrame.Raised)
        self.heroFace.setLineWidth(0)
        self.heroFace.setMidLineWidth(0)
        self.heroFace.setText("")
        self.heroFace.setObjectName("heroFace")
        self.hpSlot2_2 = QtWidgets.QLabel(self.centralwidget)
        self.hpSlot2_2.setGeometry(QtCore.QRect(889, 234, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.hpSlot2_2.setFont(font)
        self.hpSlot2_2.setAlignment(QtCore.Qt.AlignCenter)
        self.hpSlot2_2.setObjectName("hpSlot2_2")
        self.hpSlot5_2 = QtWidgets.QLabel(self.centralwidget)
        self.hpSlot5_2.setGeometry(QtCore.QRect(1001, 552, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.hpSlot5_2.setFont(font)
        self.hpSlot5_2.setAlignment(QtCore.Qt.AlignCenter)
        self.hpSlot5_2.setObjectName("hpSlot5_2")
        self.resSlot_2 = QtWidgets.QLabel(self.centralwidget)
        self.resSlot_2.setGeometry(QtCore.QRect(886, 100, 105, 127))
        self.resSlot_2.setMinimumSize(QtCore.QSize(105, 127))
        self.resSlot_2.setMaximumSize(QtCore.QSize(224, 127))
        self.resSlot_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.resSlot_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.resSlot_2.setLineWidth(1)
        self.resSlot_2.setMidLineWidth(0)
        self.resSlot_2.setObjectName("resSlot_2")
        self.hpSlot1_2 = QtWidgets.QLabel(self.centralwidget)
        self.hpSlot1_2.setGeometry(QtCore.QRect(1001, 234, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.hpSlot1_2.setFont(font)
        self.hpSlot1_2.setAlignment(QtCore.Qt.AlignCenter)
        self.hpSlot1_2.setObjectName("hpSlot1_2")
        self.resSlot_5 = QtWidgets.QLabel(self.centralwidget)
        self.resSlot_5.setGeometry(QtCore.QRect(1003, 420, 105, 127))
        self.resSlot_5.setMinimumSize(QtCore.QSize(105, 127))
        self.resSlot_5.setMaximumSize(QtCore.QSize(224, 127))
        self.resSlot_5.setFrameShape(QtWidgets.QFrame.Panel)
        self.resSlot_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.resSlot_5.setLineWidth(1)
        self.resSlot_5.setMidLineWidth(0)
        self.resSlot_5.setObjectName("resSlot_5")
        self.hpSlot6_2 = QtWidgets.QLabel(self.centralwidget)
        self.hpSlot6_2.setGeometry(QtCore.QRect(889, 552, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.hpSlot6_2.setFont(font)
        self.hpSlot6_2.setAlignment(QtCore.Qt.AlignCenter)
        self.hpSlot6_2.setObjectName("hpSlot6_2")
        self.resSlot_1 = QtWidgets.QLabel(self.centralwidget)
        self.resSlot_1.setGeometry(QtCore.QRect(1003, 100, 105, 127))
        self.resSlot_1.setMinimumSize(QtCore.QSize(105, 127))
        self.resSlot_1.setMaximumSize(QtCore.QSize(224, 127))
        self.resSlot_1.setFrameShape(QtWidgets.QFrame.Panel)
        self.resSlot_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.resSlot_1.setLineWidth(1)
        self.resSlot_1.setMidLineWidth(0)
        self.resSlot_1.setObjectName("resSlot_1")
        self.resSlot_4 = QtWidgets.QLabel(self.centralwidget)
        self.resSlot_4.setGeometry(QtCore.QRect(886, 260, 105, 127))
        self.resSlot_4.setMinimumSize(QtCore.QSize(105, 127))
        self.resSlot_4.setMaximumSize(QtCore.QSize(224, 127))
        self.resSlot_4.setFrameShape(QtWidgets.QFrame.Panel)
        self.resSlot_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.resSlot_4.setLineWidth(1)
        self.resSlot_4.setMidLineWidth(0)
        self.resSlot_4.setObjectName("resSlot_4")
        self.resSlot_6 = QtWidgets.QLabel(self.centralwidget)
        self.resSlot_6.setGeometry(QtCore.QRect(886, 420, 105, 127))
        self.resSlot_6.setMinimumSize(QtCore.QSize(105, 127))
        self.resSlot_6.setMaximumSize(QtCore.QSize(224, 127))
        self.resSlot_6.setFrameShape(QtWidgets.QFrame.Panel)
        self.resSlot_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.resSlot_6.setLineWidth(1)
        self.resSlot_6.setMidLineWidth(0)
        self.resSlot_6.setObjectName("resSlot_6")
        self.hpSlot4_2 = QtWidgets.QLabel(self.centralwidget)
        self.hpSlot4_2.setGeometry(QtCore.QRect(889, 393, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.hpSlot4_2.setFont(font)
        self.hpSlot4_2.setAlignment(QtCore.Qt.AlignCenter)
        self.hpSlot4_2.setObjectName("hpSlot4_2")
        self.hpSlot3_2 = QtWidgets.QLabel(self.centralwidget)
        self.hpSlot3_2.setGeometry(QtCore.QRect(1001, 393, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.hpSlot3_2.setFont(font)
        self.hpSlot3_2.setAlignment(QtCore.Qt.AlignCenter)
        self.hpSlot3_2.setObjectName("hpSlot3_2")
        self.resSlot_3 = QtWidgets.QLabel(self.centralwidget)
        self.resSlot_3.setGeometry(QtCore.QRect(1003, 260, 105, 127))
        self.resSlot_3.setMinimumSize(QtCore.QSize(105, 127))
        self.resSlot_3.setMaximumSize(QtCore.QSize(224, 127))
        self.resSlot_3.setFrameShape(QtWidgets.QFrame.Panel)
        self.resSlot_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.resSlot_3.setLineWidth(1)
        self.resSlot_3.setMidLineWidth(0)
        self.resSlot_3.setObjectName("resSlot_3")
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
        self.gold.raise_()
        self.hpSlot2_2.raise_()
        self.hpSlot5_2.raise_()
        self.resSlot_2.raise_()
        self.hpSlot1_2.raise_()
        self.resSlot_5.raise_()
        self.hpSlot6_2.raise_()
        self.resSlot_1.raise_()
        self.resSlot_4.raise_()
        self.resSlot_6.raise_()
        self.hpSlot4_2.raise_()
        self.hpSlot3_2.raise_()
        self.resSlot_3.raise_()
        self.heroFace.raise_()
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
        self.gold.setText(_translate("CapitalArmyWindow", "gold"))
        self.hpSlot2_2.setText(_translate("CapitalArmyWindow", "hpSlot2"))
        self.hpSlot5_2.setText(_translate("CapitalArmyWindow", "hpSlot5"))
        self.resSlot_2.setText(_translate("CapitalArmyWindow", "slot_2"))
        self.hpSlot1_2.setText(_translate("CapitalArmyWindow", "hpSlot1"))
        self.resSlot_5.setText(_translate("CapitalArmyWindow", "slot_5"))
        self.hpSlot6_2.setText(_translate("CapitalArmyWindow", "hpSlot6"))
        self.resSlot_1.setText(_translate("CapitalArmyWindow", "slot_1"))
        self.resSlot_4.setText(_translate("CapitalArmyWindow", "slot_4"))
        self.resSlot_6.setText(_translate("CapitalArmyWindow", "slot_6"))
        self.hpSlot4_2.setText(_translate("CapitalArmyWindow", "hpSlot4"))
        self.hpSlot3_2.setText(_translate("CapitalArmyWindow", "hpSlot3"))
        self.resSlot_3.setText(_translate("CapitalArmyWindow", "slot_3"))
