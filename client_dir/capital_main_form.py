# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'capital_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CapitalWindow(object):
    def setupUi(self, CapitalWindow):
        CapitalWindow.setObjectName("CapitalWindow")
        CapitalWindow.resize(1600, 900)
        CapitalWindow.setWindowTitle("CapitalWindow")
        self.centralwidget = QtWidgets.QWidget(CapitalWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.capitalBG = QtWidgets.QLabel(self.centralwidget)
        self.capitalBG.setGeometry(QtCore.QRect(0, 0, 41, 41))
        self.capitalBG.setMinimumSize(QtCore.QSize(13, 13))
        self.capitalBG.setMaximumSize(QtCore.QSize(1600, 900))
        self.capitalBG.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.capitalBG.setAutoFillBackground(True)
        self.capitalBG.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.capitalBG.setFrameShadow(QtWidgets.QFrame.Plain)
        self.capitalBG.setLineWidth(3)
        self.capitalBG.setMidLineWidth(0)
        self.capitalBG.setObjectName("capitalBG")
        self.pushButtonBack = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonBack.setGeometry(QtCore.QRect(1349, 843, 40, 40))
        self.pushButtonBack.setAutoFillBackground(False)
        self.pushButtonBack.setText("")
        self.pushButtonBack.setFlat(True)
        self.pushButtonBack.setObjectName("pushButtonBack")
        self.pushButtonArmy = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonArmy.setGeometry(QtCore.QRect(1260, 659, 40, 40))
        self.pushButtonArmy.setAutoFillBackground(False)
        self.pushButtonArmy.setText("")
        self.pushButtonArmy.setFlat(True)
        self.pushButtonArmy.setObjectName("pushButtonArmy")
        self.pushButtonBuild = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonBuild.setGeometry(QtCore.QRect(1313, 688, 40, 40))
        self.pushButtonBuild.setToolTipDuration(-1)
        self.pushButtonBuild.setAutoFillBackground(False)
        self.pushButtonBuild.setText("")
        self.pushButtonBuild.setFlat(True)
        self.pushButtonBuild.setObjectName("pushButtonBuild")
        self.animation = QtWidgets.QLabel(self.centralwidget)
        self.animation.setGeometry(QtCore.QRect(200, 0, 960, 900))
        self.animation.setFrameShape(QtWidgets.QFrame.Panel)
        self.animation.setFrameShadow(QtWidgets.QFrame.Raised)
        self.animation.setLineWidth(0)
        self.animation.setMidLineWidth(0)
        self.animation.setText("")
        self.animation.setScaledContents(True)
        self.animation.setAlignment(QtCore.Qt.AlignCenter)
        self.animation.setObjectName("animation")
        CapitalWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CapitalWindow)
        QtCore.QMetaObject.connectSlotsByName(CapitalWindow)

    def retranslateUi(self, CapitalWindow):
        _translate = QtCore.QCoreApplication.translate
        self.capitalBG.setText(_translate("CapitalWindow", "bg"))
        self.pushButtonBack.setToolTip(_translate("CapitalWindow", "Закрыть"))
        self.pushButtonArmy.setToolTip(_translate("CapitalWindow", "Экран армии (P)"))
        self.pushButtonBuild.setToolTip(_translate("CapitalWindow", "Построить здание (S)"))
