# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'campaign.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CampaignWindow(object):
    def setupUi(self, CampaignWindow):
        CampaignWindow.setObjectName("CampaignWindow")
        CampaignWindow.setEnabled(True)
        CampaignWindow.resize(1500, 827)
        CampaignWindow.setMaximumSize(QtCore.QSize(1500, 827))
        self.centralwidget = QtWidgets.QWidget(CampaignWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ExitButton = QtWidgets.QPushButton(self.centralwidget)
        self.ExitButton.setGeometry(QtCore.QRect(100, 710, 71, 28))
        self.ExitButton.setObjectName("ExitButton")
        self.pushButtonFight = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonFight.setGeometry(QtCore.QRect(20, 710, 71, 28))
        self.pushButtonFight.setObjectName("pushButtonFight")
        self.slot2 = QtWidgets.QLabel(self.centralwidget)
        self.slot2.setGeometry(QtCore.QRect(43, 440, 101, 127))
        self.slot2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.slot2.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot2.setLineWidth(1)
        self.slot2.setMidLineWidth(0)
        self.slot2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.slot2.setObjectName("slot2")
        self.slot4 = QtWidgets.QLabel(self.centralwidget)
        self.slot4.setGeometry(QtCore.QRect(280, 340, 104, 127))
        self.slot4.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot4.setLineWidth(1)
        self.slot4.setMidLineWidth(0)
        self.slot4.setObjectName("slot4")
        self.pushButtonSlot_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_4.setGeometry(QtCore.QRect(280, 340, 104, 127))
        self.pushButtonSlot_4.setText("")
        self.pushButtonSlot_4.setFlat(True)
        self.pushButtonSlot_4.setObjectName("pushButtonSlot_4")
        self.pushButtonSlot_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_2.setGeometry(QtCore.QRect(40, 440, 104, 127))
        self.pushButtonSlot_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButtonSlot_2.setText("")
        self.pushButtonSlot_2.setFlat(True)
        self.pushButtonSlot_2.setObjectName("pushButtonSlot_2")
        self.slot1 = QtWidgets.QLabel(self.centralwidget)
        self.slot1.setGeometry(QtCore.QRect(40, 250, 104, 127))
        self.slot1.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot1.setLineWidth(1)
        self.slot1.setMidLineWidth(0)
        self.slot1.setObjectName("slot1")
        self.pushButtonSlot_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_1.setGeometry(QtCore.QRect(40, 250, 104, 127))
        self.pushButtonSlot_1.setText("")
        self.pushButtonSlot_1.setFlat(True)
        self.pushButtonSlot_1.setObjectName("pushButtonSlot_1")
        self.slot3 = QtWidgets.QLabel(self.centralwidget)
        self.slot3.setGeometry(QtCore.QRect(280, 160, 104, 127))
        self.slot3.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot3.setLineWidth(1)
        self.slot3.setMidLineWidth(0)
        self.slot3.setObjectName("slot3")
        self.pushButtonSlot_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_3.setGeometry(QtCore.QRect(280, 160, 104, 127))
        self.pushButtonSlot_3.setText("")
        self.pushButtonSlot_3.setFlat(True)
        self.pushButtonSlot_3.setObjectName("pushButtonSlot_3")
        self.campaignBG = QtWidgets.QLabel(self.centralwidget)
        self.campaignBG.setGeometry(QtCore.QRect(0, 0, 41, 41))
        self.campaignBG.setScaledContents(True)
        self.campaignBG.setObjectName("campaignBG")
        self.pushButtonSlot_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_5.setGeometry(QtCore.QRect(280, 530, 104, 127))
        self.pushButtonSlot_5.setText("")
        self.pushButtonSlot_5.setFlat(True)
        self.pushButtonSlot_5.setObjectName("pushButtonSlot_5")
        self.slot5 = QtWidgets.QLabel(self.centralwidget)
        self.slot5.setGeometry(QtCore.QRect(280, 530, 104, 127))
        self.slot5.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot5.setLineWidth(1)
        self.slot5.setMidLineWidth(0)
        self.slot5.setObjectName("slot5")
        self.pushButtonSlot_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_6.setGeometry(QtCore.QRect(530, 80, 104, 127))
        self.pushButtonSlot_6.setText("")
        self.pushButtonSlot_6.setFlat(True)
        self.pushButtonSlot_6.setObjectName("pushButtonSlot_6")
        self.slot6 = QtWidgets.QLabel(self.centralwidget)
        self.slot6.setGeometry(QtCore.QRect(530, 80, 104, 127))
        self.slot6.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot6.setLineWidth(1)
        self.slot6.setMidLineWidth(0)
        self.slot6.setObjectName("slot6")
        self.PlayerSlotTxt_1 = QtWidgets.QLabel(self.centralwidget)
        self.PlayerSlotTxt_1.setGeometry(QtCore.QRect(20, 250, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PlayerSlotTxt_1.setFont(font)
        self.PlayerSlotTxt_1.setObjectName("PlayerSlotTxt_1")
        self.PlayerSlotTxt_3 = QtWidgets.QLabel(self.centralwidget)
        self.PlayerSlotTxt_3.setGeometry(QtCore.QRect(260, 160, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PlayerSlotTxt_3.setFont(font)
        self.PlayerSlotTxt_3.setObjectName("PlayerSlotTxt_3")
        self.PlayerSlotTxt_5 = QtWidgets.QLabel(self.centralwidget)
        self.PlayerSlotTxt_5.setGeometry(QtCore.QRect(260, 530, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PlayerSlotTxt_5.setFont(font)
        self.PlayerSlotTxt_5.setObjectName("PlayerSlotTxt_5")
        self.PlayerSlotTxt_2 = QtWidgets.QLabel(self.centralwidget)
        self.PlayerSlotTxt_2.setGeometry(QtCore.QRect(20, 440, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PlayerSlotTxt_2.setFont(font)
        self.PlayerSlotTxt_2.setObjectName("PlayerSlotTxt_2")
        self.PlayerSlotTxt_4 = QtWidgets.QLabel(self.centralwidget)
        self.PlayerSlotTxt_4.setGeometry(QtCore.QRect(260, 340, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PlayerSlotTxt_4.setFont(font)
        self.PlayerSlotTxt_4.setObjectName("PlayerSlotTxt_4")
        self.EnemySlotTxt_6 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_6.setGeometry(QtCore.QRect(510, 80, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_6.setFont(font)
        self.EnemySlotTxt_6.setObjectName("EnemySlotTxt_6")
        self.EnemySlotTxt_7 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_7.setGeometry(QtCore.QRect(510, 250, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_7.setFont(font)
        self.EnemySlotTxt_7.setObjectName("EnemySlotTxt_7")
        self.pushButtonSlot_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_7.setGeometry(QtCore.QRect(530, 250, 104, 127))
        self.pushButtonSlot_7.setText("")
        self.pushButtonSlot_7.setFlat(True)
        self.pushButtonSlot_7.setObjectName("pushButtonSlot_7")
        self.slot7 = QtWidgets.QLabel(self.centralwidget)
        self.slot7.setGeometry(QtCore.QRect(530, 250, 104, 127))
        self.slot7.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot7.setLineWidth(1)
        self.slot7.setMidLineWidth(0)
        self.slot7.setObjectName("slot7")
        self.EnemySlotTxt_8 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_8.setGeometry(QtCore.QRect(510, 420, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_8.setFont(font)
        self.EnemySlotTxt_8.setObjectName("EnemySlotTxt_8")
        self.pushButtonSlot_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_8.setGeometry(QtCore.QRect(530, 420, 104, 127))
        self.pushButtonSlot_8.setText("")
        self.pushButtonSlot_8.setFlat(True)
        self.pushButtonSlot_8.setObjectName("pushButtonSlot_8")
        self.slot8 = QtWidgets.QLabel(self.centralwidget)
        self.slot8.setGeometry(QtCore.QRect(530, 420, 104, 127))
        self.slot8.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot8.setLineWidth(1)
        self.slot8.setMidLineWidth(0)
        self.slot8.setObjectName("slot8")
        self.EnemySlotTxt_9 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_9.setGeometry(QtCore.QRect(510, 600, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_9.setFont(font)
        self.EnemySlotTxt_9.setObjectName("EnemySlotTxt_9")
        self.slot9 = QtWidgets.QLabel(self.centralwidget)
        self.slot9.setGeometry(QtCore.QRect(530, 600, 104, 127))
        self.slot9.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot9.setLineWidth(1)
        self.slot9.setMidLineWidth(0)
        self.slot9.setObjectName("slot9")
        self.pushButtonSlot_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_9.setGeometry(QtCore.QRect(530, 600, 104, 127))
        self.pushButtonSlot_9.setText("")
        self.pushButtonSlot_9.setFlat(True)
        self.pushButtonSlot_9.setObjectName("pushButtonSlot_9")
        self.EnemySlotTxt_10 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_10.setGeometry(QtCore.QRect(740, 160, 23, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_10.setFont(font)
        self.EnemySlotTxt_10.setObjectName("EnemySlotTxt_10")
        self.pushButtonSlot_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_10.setGeometry(QtCore.QRect(770, 160, 104, 127))
        self.pushButtonSlot_10.setText("")
        self.pushButtonSlot_10.setFlat(True)
        self.pushButtonSlot_10.setObjectName("pushButtonSlot_10")
        self.slot10 = QtWidgets.QLabel(self.centralwidget)
        self.slot10.setGeometry(QtCore.QRect(770, 160, 104, 127))
        self.slot10.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot10.setLineWidth(1)
        self.slot10.setMidLineWidth(0)
        self.slot10.setObjectName("slot10")
        self.slot11 = QtWidgets.QLabel(self.centralwidget)
        self.slot11.setGeometry(QtCore.QRect(770, 340, 104, 127))
        self.slot11.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot11.setLineWidth(1)
        self.slot11.setMidLineWidth(0)
        self.slot11.setObjectName("slot11")
        self.EnemySlotTxt_11 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_11.setGeometry(QtCore.QRect(740, 340, 23, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_11.setFont(font)
        self.EnemySlotTxt_11.setObjectName("EnemySlotTxt_11")
        self.pushButtonSlot_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_11.setGeometry(QtCore.QRect(770, 340, 104, 127))
        self.pushButtonSlot_11.setText("")
        self.pushButtonSlot_11.setFlat(True)
        self.pushButtonSlot_11.setObjectName("pushButtonSlot_11")
        self.pushButtonSlot_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_12.setGeometry(QtCore.QRect(770, 530, 104, 127))
        self.pushButtonSlot_12.setText("")
        self.pushButtonSlot_12.setFlat(True)
        self.pushButtonSlot_12.setObjectName("pushButtonSlot_12")
        self.slot12 = QtWidgets.QLabel(self.centralwidget)
        self.slot12.setGeometry(QtCore.QRect(770, 530, 104, 127))
        self.slot12.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot12.setLineWidth(1)
        self.slot12.setMidLineWidth(0)
        self.slot12.setObjectName("slot12")
        self.EnemySlotTxt_12 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_12.setGeometry(QtCore.QRect(740, 530, 23, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_12.setFont(font)
        self.EnemySlotTxt_12.setObjectName("EnemySlotTxt_12")
        self.pushButtonSlot_13 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_13.setGeometry(QtCore.QRect(1010, 250, 104, 127))
        self.pushButtonSlot_13.setText("")
        self.pushButtonSlot_13.setFlat(True)
        self.pushButtonSlot_13.setObjectName("pushButtonSlot_13")
        self.EnemySlotTxt_13 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_13.setGeometry(QtCore.QRect(980, 250, 23, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_13.setFont(font)
        self.EnemySlotTxt_13.setObjectName("EnemySlotTxt_13")
        self.slot13 = QtWidgets.QLabel(self.centralwidget)
        self.slot13.setGeometry(QtCore.QRect(1010, 250, 104, 127))
        self.slot13.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot13.setLineWidth(1)
        self.slot13.setMidLineWidth(0)
        self.slot13.setObjectName("slot13")
        self.slot14 = QtWidgets.QLabel(self.centralwidget)
        self.slot14.setGeometry(QtCore.QRect(1010, 440, 104, 127))
        self.slot14.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot14.setLineWidth(1)
        self.slot14.setMidLineWidth(0)
        self.slot14.setObjectName("slot14")
        self.pushButtonSlot_14 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_14.setGeometry(QtCore.QRect(1010, 440, 104, 127))
        self.pushButtonSlot_14.setText("")
        self.pushButtonSlot_14.setFlat(True)
        self.pushButtonSlot_14.setObjectName("pushButtonSlot_14")
        self.EnemySlotTxt_14 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_14.setGeometry(QtCore.QRect(980, 440, 23, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_14.setFont(font)
        self.EnemySlotTxt_14.setObjectName("EnemySlotTxt_14")
        self.pushButtonSlot_15 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSlot_15.setGeometry(QtCore.QRect(1250, 340, 104, 127))
        self.pushButtonSlot_15.setText("")
        self.pushButtonSlot_15.setFlat(True)
        self.pushButtonSlot_15.setObjectName("pushButtonSlot_15")
        self.EnemySlotTxt_15 = QtWidgets.QLabel(self.centralwidget)
        self.EnemySlotTxt_15.setGeometry(QtCore.QRect(1220, 340, 23, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EnemySlotTxt_15.setFont(font)
        self.EnemySlotTxt_15.setObjectName("EnemySlotTxt_15")
        self.slot15 = QtWidgets.QLabel(self.centralwidget)
        self.slot15.setGeometry(QtCore.QRect(1250, 340, 104, 127))
        self.slot15.setFrameShape(QtWidgets.QFrame.Panel)
        self.slot15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slot15.setLineWidth(1)
        self.slot15.setMidLineWidth(0)
        self.slot15.setObjectName("slot15")
        self.campaignBG.raise_()
        self.ExitButton.raise_()
        self.pushButtonFight.raise_()
        self.slot2.raise_()
        self.slot4.raise_()
        self.slot1.raise_()
        self.slot3.raise_()
        self.slot5.raise_()
        self.slot6.raise_()
        self.PlayerSlotTxt_1.raise_()
        self.PlayerSlotTxt_3.raise_()
        self.PlayerSlotTxt_5.raise_()
        self.PlayerSlotTxt_2.raise_()
        self.PlayerSlotTxt_4.raise_()
        self.EnemySlotTxt_6.raise_()
        self.EnemySlotTxt_7.raise_()
        self.slot7.raise_()
        self.EnemySlotTxt_8.raise_()
        self.slot8.raise_()
        self.EnemySlotTxt_9.raise_()
        self.slot9.raise_()
        self.EnemySlotTxt_10.raise_()
        self.slot10.raise_()
        self.slot11.raise_()
        self.EnemySlotTxt_11.raise_()
        self.slot12.raise_()
        self.EnemySlotTxt_12.raise_()
        self.EnemySlotTxt_13.raise_()
        self.slot13.raise_()
        self.pushButtonSlot_4.raise_()
        self.pushButtonSlot_6.raise_()
        self.pushButtonSlot_12.raise_()
        self.pushButtonSlot_9.raise_()
        self.pushButtonSlot_2.raise_()
        self.pushButtonSlot_1.raise_()
        self.pushButtonSlot_5.raise_()
        self.pushButtonSlot_11.raise_()
        self.pushButtonSlot_7.raise_()
        self.pushButtonSlot_13.raise_()
        self.pushButtonSlot_3.raise_()
        self.pushButtonSlot_10.raise_()
        self.pushButtonSlot_8.raise_()
        self.slot14.raise_()
        self.pushButtonSlot_14.raise_()
        self.EnemySlotTxt_14.raise_()
        self.EnemySlotTxt_15.raise_()
        self.slot15.raise_()
        self.pushButtonSlot_15.raise_()
        CampaignWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CampaignWindow)
        QtCore.QMetaObject.connectSlotsByName(CampaignWindow)

    def retranslateUi(self, CampaignWindow):
        _translate = QtCore.QCoreApplication.translate
        CampaignWindow.setWindowTitle(_translate("CampaignWindow", "CampaignWindow"))
        self.ExitButton.setText(_translate("CampaignWindow", "Выйти"))
        self.pushButtonFight.setText(_translate("CampaignWindow", "В бой!"))
        self.slot2.setText(_translate("CampaignWindow", "slot_2"))
        self.slot4.setText(_translate("CampaignWindow", "slot_4"))
        self.slot1.setText(_translate("CampaignWindow", "slot_1"))
        self.slot3.setText(_translate("CampaignWindow", "slot_3"))
        self.campaignBG.setText(_translate("CampaignWindow", "bg"))
        self.slot5.setText(_translate("CampaignWindow", "slot_5"))
        self.slot6.setText(_translate("CampaignWindow", "slot_6"))
        self.PlayerSlotTxt_1.setText(_translate("CampaignWindow", "1"))
        self.PlayerSlotTxt_3.setText(_translate("CampaignWindow", "3"))
        self.PlayerSlotTxt_5.setText(_translate("CampaignWindow", "5"))
        self.PlayerSlotTxt_2.setText(_translate("CampaignWindow", "2"))
        self.PlayerSlotTxt_4.setText(_translate("CampaignWindow", "4"))
        self.EnemySlotTxt_6.setText(_translate("CampaignWindow", "6"))
        self.EnemySlotTxt_7.setText(_translate("CampaignWindow", "7"))
        self.slot7.setText(_translate("CampaignWindow", "slot_7"))
        self.EnemySlotTxt_8.setText(_translate("CampaignWindow", "8"))
        self.slot8.setText(_translate("CampaignWindow", "slot_8"))
        self.EnemySlotTxt_9.setText(_translate("CampaignWindow", "9"))
        self.slot9.setText(_translate("CampaignWindow", "slot_9"))
        self.EnemySlotTxt_10.setText(_translate("CampaignWindow", "10"))
        self.slot10.setText(_translate("CampaignWindow", "slot_10"))
        self.slot11.setText(_translate("CampaignWindow", "slot_11"))
        self.EnemySlotTxt_11.setText(_translate("CampaignWindow", "11"))
        self.slot12.setText(_translate("CampaignWindow", "slot_12"))
        self.EnemySlotTxt_12.setText(_translate("CampaignWindow", "12"))
        self.EnemySlotTxt_13.setText(_translate("CampaignWindow", "13"))
        self.slot13.setText(_translate("CampaignWindow", "slot_13"))
        self.slot14.setText(_translate("CampaignWindow", "slot_14"))
        self.EnemySlotTxt_14.setText(_translate("CampaignWindow", "14"))
        self.EnemySlotTxt_15.setText(_translate("CampaignWindow", "15"))
        self.slot15.setText(_translate("CampaignWindow", "slot_15"))
