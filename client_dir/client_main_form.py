# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1380, 742)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listAllUnits = QtWidgets.QListView(self.centralwidget)
        self.listAllUnits.setGeometry(QtCore.QRect(560, 40, 256, 641))
        self.listAllUnits.setObjectName("listAllUnits")
        self.listPlayerUnits = QtWidgets.QListView(self.centralwidget)
        self.listPlayerUnits.setEnabled(False)
        self.listPlayerUnits.setGeometry(QtCore.QRect(40, 40, 161, 141))
        self.listPlayerUnits.setObjectName("listPlayerUnits")
        self.iconLabel = QtWidgets.QLabel(self.centralwidget)
        self.iconLabel.setGeometry(QtCore.QRect(340, 40, 186, 133))
        self.iconLabel.setMaximumSize(QtCore.QSize(186, 133))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.iconLabel.setFont(font)
        self.iconLabel.setFrameShape(QtWidgets.QFrame.Panel)
        self.iconLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.iconLabel.setLineWidth(3)
        self.iconLabel.setText("")
        self.iconLabel.setScaledContents(False)
        self.iconLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.iconLabel.setObjectName("iconLabel")
        self.slot1 = QtWidgets.QLabel(self.centralwidget)
        self.slot1.setGeometry(QtCore.QRect(40, 260, 104, 127))
        self.slot1.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot1.setLineWidth(3)
        self.slot1.setMidLineWidth(0)
        self.slot1.setObjectName("slot1")
        self.slot2 = QtWidgets.QLabel(self.centralwidget)
        self.slot2.setGeometry(QtCore.QRect(163, 260, 101, 127))
        self.slot2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.slot2.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot2.setLineWidth(3)
        self.slot2.setMidLineWidth(0)
        self.slot2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.slot2.setObjectName("slot2")
        self.slot3 = QtWidgets.QLabel(self.centralwidget)
        self.slot3.setGeometry(QtCore.QRect(40, 420, 104, 127))
        self.slot3.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot3.setLineWidth(3)
        self.slot3.setMidLineWidth(0)
        self.slot3.setObjectName("slot3")
        self.slot4 = QtWidgets.QLabel(self.centralwidget)
        self.slot4.setGeometry(QtCore.QRect(160, 420, 104, 127))
        self.slot4.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot4.setLineWidth(3)
        self.slot4.setMidLineWidth(0)
        self.slot4.setObjectName("slot4")
        self.slot5 = QtWidgets.QLabel(self.centralwidget)
        self.slot5.setGeometry(QtCore.QRect(40, 560, 104, 127))
        self.slot5.setMinimumSize(QtCore.QSize(104, 127))
        self.slot5.setMaximumSize(QtCore.QSize(224, 127))
        self.slot5.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot5.setLineWidth(3)
        self.slot5.setMidLineWidth(0)
        self.slot5.setObjectName("slot5")
        self.slot6 = QtWidgets.QLabel(self.centralwidget)
        self.slot6.setGeometry(QtCore.QRect(160, 560, 104, 127))
        self.slot6.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot6.setLineWidth(3)
        self.slot6.setMidLineWidth(0)
        self.slot6.setObjectName("slot6")
        self.listPlayerSlots = QtWidgets.QListView(self.centralwidget)
        self.listPlayerSlots.setGeometry(QtCore.QRect(210, 40, 51, 141))
        self.listPlayerSlots.setObjectName("listPlayerSlots")
        self.pushButtonSlot1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot1.setGeometry(QtCore.QRect(40, 260, 104, 127))
        self.pushButtonSlot1.setText("")
        self.pushButtonSlot1.setFlat(True)
        self.pushButtonSlot1.setObjectName("pushButtonSlot1")
        self.pushButtonSlot3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot3.setGeometry(QtCore.QRect(40, 420, 104, 127))
        self.pushButtonSlot3.setText("")
        self.pushButtonSlot3.setFlat(True)
        self.pushButtonSlot3.setObjectName("pushButtonSlot3")
        self.pushButtonSlot5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot5.setGeometry(QtCore.QRect(40, 560, 104, 127))
        self.pushButtonSlot5.setMinimumSize(QtCore.QSize(104, 127))
        self.pushButtonSlot5.setMaximumSize(QtCore.QSize(224, 127))
        self.pushButtonSlot5.setText("")
        self.pushButtonSlot5.setFlat(True)
        self.pushButtonSlot5.setObjectName("pushButtonSlot5")
        self.pushButtonSlot2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot2.setGeometry(QtCore.QRect(160, 260, 104, 127))
        self.pushButtonSlot2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButtonSlot2.setText("")
        self.pushButtonSlot2.setFlat(True)
        self.pushButtonSlot2.setObjectName("pushButtonSlot2")
        self.pushButtonSlot4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot4.setGeometry(QtCore.QRect(160, 420, 104, 127))
        self.pushButtonSlot4.setText("")
        self.pushButtonSlot4.setFlat(True)
        self.pushButtonSlot4.setObjectName("pushButtonSlot4")
        self.pushButtonSlot6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot6.setGeometry(QtCore.QRect(160, 560, 104, 127))
        self.pushButtonSlot6.setText("")
        self.pushButtonSlot6.setFlat(True)
        self.pushButtonSlot6.setObjectName("pushButtonSlot6")
        self.pushButtonCapital = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonCapital.setGeometry(QtCore.QRect(390, 0, 90, 28))
        self.pushButtonCapital.setObjectName("pushButtonCapital")
        self.gifLabel = QtWidgets.QLabel(self.centralwidget)
        self.gifLabel.setGeometry(QtCore.QRect(340, 200, 191, 191))
        self.gifLabel.setFrameShape(QtWidgets.QFrame.Panel)
        self.gifLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gifLabel.setLineWidth(3)
        self.gifLabel.setText("")
        self.gifLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.gifLabel.setIndent(-1)
        self.gifLabel.setObjectName("gifLabel")
        self.pushButtonChooseRace = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonChooseRace.setGeometry(QtCore.QRect(10, 0, 101, 28))
        self.pushButtonChooseRace.setObjectName("pushButtonChooseRace")
        self.currentFaction = QtWidgets.QLabel(self.centralwidget)
        self.currentFaction.setGeometry(QtCore.QRect(115, 7, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.currentFaction.setFont(font)
        self.currentFaction.setObjectName("currentFaction")
        self.capital = QtWidgets.QLabel(self.centralwidget)
        self.capital.setGeometry(QtCore.QRect(0, 0, 61, 61))
        self.capital.setMaximumSize(QtCore.QSize(1600, 900))
        self.capital.setAutoFillBackground(True)
        self.capital.setScaledContents(True)
        self.capital.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.capital.setObjectName("capital")
        self.swap12 = QtWidgets.QPushButton(self.centralwidget)
        self.swap12.setGeometry(QtCore.QRect(120, 227, 71, 28))
        self.swap12.setObjectName("swap12")
        self.pushButtonCampaign = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonCampaign.setEnabled(True)
        self.pushButtonCampaign.setGeometry(QtCore.QRect(880, 0, 90, 28))
        self.pushButtonCampaign.setObjectName("pushButtonCampaign")
        self.EnemySlot2 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlot2.setGeometry(QtCore.QRect(880, 260, 104, 127))
        self.EnemySlot2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.EnemySlot2.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot2.setLineWidth(3)
        self.EnemySlot2.setMidLineWidth(0)
        self.EnemySlot2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.EnemySlot2.setObjectName("EnemySlot2")
        self.EnemySlot6 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlot6.setGeometry(QtCore.QRect(880, 560, 104, 127))
        self.EnemySlot6.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot6.setLineWidth(3)
        self.EnemySlot6.setMidLineWidth(0)
        self.EnemySlot6.setObjectName("EnemySlot6")
        self.EnemySlot5 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlot5.setGeometry(QtCore.QRect(1000, 560, 104, 127))
        self.EnemySlot5.setMinimumSize(QtCore.QSize(104, 127))
        self.EnemySlot5.setMaximumSize(QtCore.QSize(224, 127))
        self.EnemySlot5.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot5.setLineWidth(3)
        self.EnemySlot5.setMidLineWidth(0)
        self.EnemySlot5.setObjectName("EnemySlot5")
        self.EnemySlot1 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlot1.setGeometry(QtCore.QRect(1000, 260, 104, 127))
        self.EnemySlot1.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot1.setLineWidth(3)
        self.EnemySlot1.setMidLineWidth(0)
        self.EnemySlot1.setObjectName("EnemySlot1")
        self.EnemySlot3 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlot3.setGeometry(QtCore.QRect(1000, 420, 104, 127))
        self.EnemySlot3.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot3.setLineWidth(3)
        self.EnemySlot3.setMidLineWidth(0)
        self.EnemySlot3.setObjectName("EnemySlot3")
        self.pushButtonEnSlot4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEnSlot4.setGeometry(QtCore.QRect(880, 420, 104, 127))
        self.pushButtonEnSlot4.setText("")
        self.pushButtonEnSlot4.setFlat(True)
        self.pushButtonEnSlot4.setObjectName("pushButtonEnSlot4")
        self.pushButtonEnSlot3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEnSlot3.setGeometry(QtCore.QRect(1000, 420, 104, 127))
        self.pushButtonEnSlot3.setText("")
        self.pushButtonEnSlot3.setFlat(True)
        self.pushButtonEnSlot3.setObjectName("pushButtonEnSlot3")
        self.pushButtonEnSlot5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEnSlot5.setGeometry(QtCore.QRect(1000, 560, 104, 127))
        self.pushButtonEnSlot5.setMinimumSize(QtCore.QSize(104, 127))
        self.pushButtonEnSlot5.setMaximumSize(QtCore.QSize(224, 127))
        self.pushButtonEnSlot5.setText("")
        self.pushButtonEnSlot5.setFlat(True)
        self.pushButtonEnSlot5.setObjectName("pushButtonEnSlot5")
        self.pushButtonEnSlot1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEnSlot1.setGeometry(QtCore.QRect(1000, 260, 104, 127))
        self.pushButtonEnSlot1.setText("")
        self.pushButtonEnSlot1.setFlat(True)
        self.pushButtonEnSlot1.setObjectName("pushButtonEnSlot1")
        self.EnemySlot4 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlot4.setGeometry(QtCore.QRect(880, 420, 104, 127))
        self.EnemySlot4.setFrameShape(QtWidgets.QFrame.Panel)
        self.EnemySlot4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EnemySlot4.setLineWidth(3)
        self.EnemySlot4.setMidLineWidth(0)
        self.EnemySlot4.setObjectName("EnemySlot4")
        self.listEnemyUnits = QtWidgets.QListView(self.centralwidget)
        self.listEnemyUnits.setEnabled(False)
        self.listEnemyUnits.setGeometry(QtCore.QRect(880, 40, 161, 141))
        self.listEnemyUnits.setObjectName("listEnemyUnits")
        self.listEnemySlots = QtWidgets.QListView(self.centralwidget)
        self.listEnemySlots.setGeometry(QtCore.QRect(1050, 40, 51, 141))
        self.listEnemySlots.setObjectName("listEnemySlots")
        self.pushButtonEnSlot2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEnSlot2.setGeometry(QtCore.QRect(880, 260, 104, 127))
        self.pushButtonEnSlot2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButtonEnSlot2.setText("")
        self.pushButtonEnSlot2.setFlat(True)
        self.pushButtonEnSlot2.setObjectName("pushButtonEnSlot2")
        self.pushButtonEnSlot6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonEnSlot6.setGeometry(QtCore.QRect(880, 560, 104, 127))
        self.pushButtonEnSlot6.setText("")
        self.pushButtonEnSlot6.setFlat(True)
        self.pushButtonEnSlot6.setObjectName("pushButtonEnSlot6")
        self.pushButtonVersus = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonVersus.setGeometry(QtCore.QRect(560, 0, 141, 28))
        self.pushButtonVersus.setObjectName("pushButtonVersus")
        self.pushButtonAddPlayer = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonAddPlayer.setGeometry(QtCore.QRect(1150, 0, 121, 28))
        self.pushButtonAddPlayer.setObjectName("pushButtonAddPlayer")
        self.PlayersList = QtWidgets.QListView(self.centralwidget)
        self.PlayersList.setGeometry(QtCore.QRect(1150, 120, 221, 141))
        self.PlayersList.setObjectName("PlayersList")
        self.PlayerName = QtWidgets.QTextEdit(self.centralwidget)
        self.PlayerName.setGeometry(QtCore.QRect(1200, 40, 171, 31))
        self.PlayerName.setObjectName("PlayerName")
        self.Email = QtWidgets.QTextEdit(self.centralwidget)
        self.Email.setGeometry(QtCore.QRect(1200, 80, 171, 31))
        self.Email.setObjectName("Email")
        self.PlayerNameTxt = QtWidgets.QLabel(self.centralwidget)
        self.PlayerNameTxt.setGeometry(QtCore.QRect(1150, 50, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.PlayerNameTxt.setFont(font)
        self.PlayerNameTxt.setObjectName("PlayerNameTxt")
        self.EmailTxt = QtWidgets.QLabel(self.centralwidget)
        self.EmailTxt.setGeometry(QtCore.QRect(1150, 90, 50, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.EmailTxt.setFont(font)
        self.EmailTxt.setObjectName("EmailTxt")
        self.swap56 = QtWidgets.QPushButton(self.centralwidget)
        self.swap56.setGeometry(QtCore.QRect(120, 690, 71, 28))
        self.swap56.setObjectName("swap56")
        self.swap34 = QtWidgets.QPushButton(self.centralwidget)
        self.swap34.setGeometry(QtCore.QRect(120, 390, 71, 28))
        self.swap34.setObjectName("swap34")
        self.swap13 = QtWidgets.QPushButton(self.centralwidget)
        self.swap13.setGeometry(QtCore.QRect(0, 370, 31, 61))
        self.swap13.setObjectName("swap13")
        self.swap24 = QtWidgets.QPushButton(self.centralwidget)
        self.swap24.setGeometry(QtCore.QRect(275, 370, 31, 61))
        self.swap24.setObjectName("swap24")
        self.swap35 = QtWidgets.QPushButton(self.centralwidget)
        self.swap35.setGeometry(QtCore.QRect(0, 520, 31, 61))
        self.swap35.setObjectName("swap35")
        self.swap46 = QtWidgets.QPushButton(self.centralwidget)
        self.swap46.setGeometry(QtCore.QRect(275, 520, 31, 61))
        self.swap46.setObjectName("swap46")
        self.enSwap35 = QtWidgets.QPushButton(self.centralwidget)
        self.enSwap35.setGeometry(QtCore.QRect(1114, 520, 31, 61))
        self.enSwap35.setObjectName("enSwap35")
        self.enSwap12 = QtWidgets.QPushButton(self.centralwidget)
        self.enSwap12.setGeometry(QtCore.QRect(959, 227, 71, 28))
        self.enSwap12.setObjectName("enSwap12")
        self.enSwap13 = QtWidgets.QPushButton(self.centralwidget)
        self.enSwap13.setGeometry(QtCore.QRect(1114, 370, 31, 61))
        self.enSwap13.setObjectName("enSwap13")
        self.enSwap34 = QtWidgets.QPushButton(self.centralwidget)
        self.enSwap34.setGeometry(QtCore.QRect(959, 390, 71, 28))
        self.enSwap34.setObjectName("enSwap34")
        self.enSwap56 = QtWidgets.QPushButton(self.centralwidget)
        self.enSwap56.setGeometry(QtCore.QRect(959, 690, 71, 28))
        self.enSwap56.setObjectName("enSwap56")
        self.enSwap24 = QtWidgets.QPushButton(self.centralwidget)
        self.enSwap24.setGeometry(QtCore.QRect(840, 370, 31, 61))
        self.enSwap24.setObjectName("enSwap24")
        self.enSwap46 = QtWidgets.QPushButton(self.centralwidget)
        self.enSwap46.setGeometry(QtCore.QRect(840, 520, 31, 61))
        self.enSwap46.setObjectName("enSwap46")
        self.pushButtonFight = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonFight.setGeometry(QtCore.QRect(727, 0, 90, 28))
        self.pushButtonFight.setObjectName("pushButtonFight")
        self.pushButtonDelPlayer = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDelPlayer.setGeometry(QtCore.QRect(1279, 0, 91, 28))
        self.pushButtonDelPlayer.setObjectName("pushButtonDelPlayer")
        self.pushButtonChoosePlayer = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonChoosePlayer.setGeometry(QtCore.QRect(1150, 270, 121, 28))
        self.pushButtonChoosePlayer.setObjectName("pushButtonChoosePlayer")
        self.PlayerSlotTxt_1 = QtWidgets.QLabel(self.centralwidget)
        self.PlayerSlotTxt_1.setGeometry(QtCore.QRect(20, 260, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PlayerSlotTxt_1.setFont(font)
        self.PlayerSlotTxt_1.setObjectName("PlayerSlotTxt_1")
        self.PlayerSlotTxt_2 = QtWidgets.QLabel(self.centralwidget)
        self.PlayerSlotTxt_2.setGeometry(QtCore.QRect(270, 260, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PlayerSlotTxt_2.setFont(font)
        self.PlayerSlotTxt_2.setObjectName("PlayerSlotTxt_2")
        self.PlayerSlotTxt_4 = QtWidgets.QLabel(self.centralwidget)
        self.PlayerSlotTxt_4.setGeometry(QtCore.QRect(270, 440, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PlayerSlotTxt_4.setFont(font)
        self.PlayerSlotTxt_4.setObjectName("PlayerSlotTxt_4")
        self.PlayerSlotTxt_3 = QtWidgets.QLabel(self.centralwidget)
        self.PlayerSlotTxt_3.setGeometry(QtCore.QRect(20, 440, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PlayerSlotTxt_3.setFont(font)
        self.PlayerSlotTxt_3.setObjectName("PlayerSlotTxt_3")
        self.PlayerSlotTxt_6 = QtWidgets.QLabel(self.centralwidget)
        self.PlayerSlotTxt_6.setGeometry(QtCore.QRect(270, 670, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PlayerSlotTxt_6.setFont(font)
        self.PlayerSlotTxt_6.setObjectName("PlayerSlotTxt_6")
        self.PlayerSlotTxt_5 = QtWidgets.QLabel(self.centralwidget)
        self.PlayerSlotTxt_5.setGeometry(QtCore.QRect(20, 670, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PlayerSlotTxt_5.setFont(font)
        self.PlayerSlotTxt_5.setObjectName("PlayerSlotTxt_5")
        self.EnemySlotTxt_6 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_6.setGeometry(QtCore.QRect(860, 670, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_6.setFont(font)
        self.EnemySlotTxt_6.setObjectName("EnemySlotTxt_6")
        self.EnemySlotTxt_5 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_5.setGeometry(QtCore.QRect(1110, 670, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_5.setFont(font)
        self.EnemySlotTxt_5.setObjectName("EnemySlotTxt_5")
        self.EnemySlotTxt_3 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_3.setGeometry(QtCore.QRect(1110, 440, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_3.setFont(font)
        self.EnemySlotTxt_3.setObjectName("EnemySlotTxt_3")
        self.EnemySlotTxt_1 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_1.setGeometry(QtCore.QRect(1110, 260, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_1.setFont(font)
        self.EnemySlotTxt_1.setObjectName("EnemySlotTxt_1")
        self.EnemySlotTxt_2 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_2.setGeometry(QtCore.QRect(860, 260, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_2.setFont(font)
        self.EnemySlotTxt_2.setObjectName("EnemySlotTxt_2")
        self.EnemySlotTxt_4 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_4.setGeometry(QtCore.QRect(860, 440, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_4.setFont(font)
        self.EnemySlotTxt_4.setObjectName("EnemySlotTxt_4")
        self.portraitLabel = QtWidgets.QLabel(self.centralwidget)
        self.portraitLabel.setGeometry(QtCore.QRect(340, 420, 191, 261))
        self.portraitLabel.setFrameShape(QtWidgets.QFrame.Panel)
        self.portraitLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.portraitLabel.setLineWidth(3)
        self.portraitLabel.setText("")
        self.portraitLabel.setScaledContents(True)
        self.portraitLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.portraitLabel.setObjectName("portraitLabel")
        self.pushButtonDeleteEn = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDeleteEn.setGeometry(QtCore.QRect(1000, 190, 104, 28))
        self.pushButtonDeleteEn.setObjectName("pushButtonDeleteEn")
        self.pushButtonHireEn = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonHireEn.setGeometry(QtCore.QRect(880, 190, 104, 28))
        self.pushButtonHireEn.setObjectName("pushButtonHireEn")
        self.pushButtonHire = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonHire.setGeometry(QtCore.QRect(40, 190, 104, 28))
        self.pushButtonHire.setObjectName("pushButtonHire")
        self.pushButtonDelete = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDelete.setGeometry(QtCore.QRect(160, 190, 104, 28))
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.currentPlayer = QtWidgets.QLabel(self.centralwidget)
        self.currentPlayer.setGeometry(QtCore.QRect(990, 7, 149, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.currentPlayer.setFont(font)
        self.currentPlayer.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.currentPlayer.setText("")
        self.currentPlayer.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.currentPlayer.setObjectName("currentPlayer")
        self.capital.raise_()
        self.gifLabel.raise_()
        self.listAllUnits.raise_()
        self.listPlayerUnits.raise_()
        self.iconLabel.raise_()
        self.listPlayerSlots.raise_()
        self.pushButtonCapital.raise_()
        self.pushButtonChooseRace.raise_()
        self.currentFaction.raise_()
        self.slot5.raise_()
        self.slot3.raise_()
        self.slot1.raise_()
        self.swap12.raise_()
        self.pushButtonCampaign.raise_()
        self.EnemySlot5.raise_()
        self.EnemySlot1.raise_()
        self.EnemySlot3.raise_()
        self.listEnemyUnits.raise_()
        self.listEnemySlots.raise_()
        self.pushButtonVersus.raise_()
        self.pushButtonSlot5.raise_()
        self.pushButtonSlot3.raise_()
        self.pushButtonSlot1.raise_()
        self.pushButtonAddPlayer.raise_()
        self.PlayersList.raise_()
        self.PlayerName.raise_()
        self.Email.raise_()
        self.PlayerNameTxt.raise_()
        self.EmailTxt.raise_()
        self.swap56.raise_()
        self.swap34.raise_()
        self.swap13.raise_()
        self.swap24.raise_()
        self.swap35.raise_()
        self.swap46.raise_()
        self.enSwap35.raise_()
        self.enSwap12.raise_()
        self.enSwap13.raise_()
        self.enSwap34.raise_()
        self.enSwap56.raise_()
        self.enSwap24.raise_()
        self.enSwap46.raise_()
        self.pushButtonFight.raise_()
        self.pushButtonDelPlayer.raise_()
        self.EnemySlot2.raise_()
        self.EnemySlot4.raise_()
        self.EnemySlot6.raise_()
        self.pushButtonEnSlot5.raise_()
        self.pushButtonEnSlot3.raise_()
        self.pushButtonEnSlot1.raise_()
        self.pushButtonEnSlot4.raise_()
        self.pushButtonEnSlot2.raise_()
        self.pushButtonEnSlot6.raise_()
        self.pushButtonChoosePlayer.raise_()
        self.slot4.raise_()
        self.slot2.raise_()
        self.slot6.raise_()
        self.pushButtonSlot4.raise_()
        self.pushButtonSlot2.raise_()
        self.pushButtonSlot6.raise_()
        self.PlayerSlotTxt_1.raise_()
        self.PlayerSlotTxt_2.raise_()
        self.PlayerSlotTxt_4.raise_()
        self.PlayerSlotTxt_3.raise_()
        self.PlayerSlotTxt_6.raise_()
        self.PlayerSlotTxt_5.raise_()
        self.EnemySlotTxt_6.raise_()
        self.EnemySlotTxt_5.raise_()
        self.EnemySlotTxt_3.raise_()
        self.EnemySlotTxt_1.raise_()
        self.EnemySlotTxt_2.raise_()
        self.EnemySlotTxt_4.raise_()
        self.portraitLabel.raise_()
        self.pushButtonDeleteEn.raise_()
        self.pushButtonHireEn.raise_()
        self.pushButtonHire.raise_()
        self.pushButtonDelete.raise_()
        self.currentPlayer.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.slot1.setText(_translate("MainWindow", "slot_1"))
        self.slot2.setText(_translate("MainWindow", "slot_2"))
        self.slot3.setText(_translate("MainWindow", "slot_3"))
        self.slot4.setText(_translate("MainWindow", "slot_4"))
        self.slot5.setText(_translate("MainWindow", "slot_5"))
        self.slot6.setText(_translate("MainWindow", "slot_6"))
        self.pushButtonCapital.setText(_translate("MainWindow", "Столица"))
        self.pushButtonChooseRace.setText(_translate("MainWindow", "Выбор фракции"))
        self.currentFaction.setText(_translate("MainWindow", "currentFaction"))
        self.capital.setText(_translate("MainWindow", "capital"))
        self.swap12.setText(_translate("MainWindow", "<>"))
        self.pushButtonCampaign.setText(_translate("MainWindow", "Кампания"))
        self.EnemySlot2.setText(_translate("MainWindow", "slot_2"))
        self.EnemySlot6.setText(_translate("MainWindow", "slot_6"))
        self.EnemySlot5.setText(_translate("MainWindow", "slot_5"))
        self.EnemySlot1.setText(_translate("MainWindow", "slot_1"))
        self.EnemySlot3.setText(_translate("MainWindow", "slot_3"))
        self.EnemySlot4.setText(_translate("MainWindow", "slot_4"))
        self.pushButtonVersus.setText(_translate("MainWindow", "Сравнить две армии"))
        self.pushButtonAddPlayer.setText(_translate("MainWindow", "Добавить игрока"))
        self.PlayerNameTxt.setText(_translate("MainWindow", "Имя"))
        self.EmailTxt.setText(_translate("MainWindow", "E-mail"))
        self.swap56.setText(_translate("MainWindow", "<>"))
        self.swap34.setText(_translate("MainWindow", "<>"))
        self.swap13.setText(_translate("MainWindow", "<>"))
        self.swap24.setText(_translate("MainWindow", "<>"))
        self.swap35.setText(_translate("MainWindow", "<>"))
        self.swap46.setText(_translate("MainWindow", "<>"))
        self.enSwap35.setText(_translate("MainWindow", "<>"))
        self.enSwap12.setText(_translate("MainWindow", "<>"))
        self.enSwap13.setText(_translate("MainWindow", "<>"))
        self.enSwap34.setText(_translate("MainWindow", "<>"))
        self.enSwap56.setText(_translate("MainWindow", "<>"))
        self.enSwap24.setText(_translate("MainWindow", "<>"))
        self.enSwap46.setText(_translate("MainWindow", "<>"))
        self.pushButtonFight.setText(_translate("MainWindow", "Darkest"))
        self.pushButtonDelPlayer.setText(_translate("MainWindow", "Удалить"))
        self.pushButtonChoosePlayer.setText(_translate("MainWindow", "Выбрать игрока"))
        self.PlayerSlotTxt_1.setText(_translate("MainWindow", "1"))
        self.PlayerSlotTxt_2.setText(_translate("MainWindow", "2"))
        self.PlayerSlotTxt_4.setText(_translate("MainWindow", "4"))
        self.PlayerSlotTxt_3.setText(_translate("MainWindow", "3"))
        self.PlayerSlotTxt_6.setText(_translate("MainWindow", "6"))
        self.PlayerSlotTxt_5.setText(_translate("MainWindow", "5"))
        self.EnemySlotTxt_6.setText(_translate("MainWindow", "6"))
        self.EnemySlotTxt_5.setText(_translate("MainWindow", "5"))
        self.EnemySlotTxt_3.setText(_translate("MainWindow", "3"))
        self.EnemySlotTxt_1.setText(_translate("MainWindow", "1"))
        self.EnemySlotTxt_2.setText(_translate("MainWindow", "2"))
        self.EnemySlotTxt_4.setText(_translate("MainWindow", "4"))
        self.pushButtonDeleteEn.setText(_translate("MainWindow", "Уволить"))
        self.pushButtonHireEn.setText(_translate("MainWindow", "Нанять"))
        self.pushButtonHire.setText(_translate("MainWindow", "Нанять"))
        self.pushButtonDelete.setText(_translate("MainWindow", "Уволить"))
