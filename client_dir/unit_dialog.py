"""Диалог характеристик юнита/героя"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog

from client_dir.settings import UNIT_FRAME, PORTRAITS
from units_dir.units import main_db


class UnitDialog(QDialog):
    """Диалог характеристик юнита/героя"""

    def __init__(self, unit: any):
        super().__init__()

        self.setFixedSize(914, 826)
        self.setWindowTitle('Характеристики')

        self.background = QtWidgets.QLabel(self)
        self.background.setGeometry(QtCore.QRect(0, 0, 914, 826))
        self.background.setMinimumSize(QtCore.QSize(13, 13))
        self.background.setMaximumSize(QtCore.QSize(914, 826))
        self.background.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.background.setAutoFillBackground(True)
        self.background.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.background.setFrameShadow(QtWidgets.QFrame.Plain)
        self.background.setLineWidth(3)
        self.background.setMidLineWidth(0)
        self.background.setObjectName("background")
        self.portrait = QtWidgets.QLabel(self)
        self.portrait.setGeometry(QtCore.QRect(40, 30, 450, 590))
        self.portrait.setTextFormat(QtCore.Qt.PlainText)
        self.portrait.setScaledContents(True)
        self.portrait.setAlignment(QtCore.Qt.AlignCenter)
        self.portrait.setObjectName("portrait")
        self.unitName = QtWidgets.QLabel(self)
        self.unitName.setGeometry(QtCore.QRect(75, 620, 401, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.unitName.setFont(font)
        self.unitName.setAlignment(QtCore.Qt.AlignCenter)
        self.unitName.setObjectName("unitName")
        self.level = QtWidgets.QLabel(self)
        self.level.setGeometry(QtCore.QRect(660, 76, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.level.setFont(font)
        self.level.setObjectName("level")
        self.exp = QtWidgets.QLabel(self)
        self.exp.setGeometry(QtCore.QRect(660, 102, 171, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.exp.setFont(font)
        self.exp.setObjectName("exp")
        self.health = QtWidgets.QLabel(self)
        self.health.setGeometry(QtCore.QRect(660, 127, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.health.setFont(font)
        self.health.setObjectName("health")
        self.armor = QtWidgets.QLabel(self)
        self.armor.setGeometry(QtCore.QRect(660, 152, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.armor.setFont(font)
        self.armor.setObjectName("armor")
        self.immune = QtWidgets.QLabel(self)
        self.immune.setGeometry(QtCore.QRect(660, 177, 221, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.immune.setFont(font)
        self.immune.setObjectName("immune")
        self.ward = QtWidgets.QLabel(self)
        self.ward.setGeometry(QtCore.QRect(660, 203, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.ward.setFont(font)
        self.ward.setAlignment(QtCore.Qt.AlignLeading |
                               QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ward.setWordWrap(True)
        self.ward.setObjectName("ward")
        self.attackDmg = QtWidgets.QLabel(self)
        self.attackDmg.setGeometry(QtCore.QRect(660, 362, 170, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackDmg.setFont(font)
        self.attackDmg.setObjectName("attackDmg")
        self.attackSource = QtWidgets.QLabel(self)
        self.attackSource.setGeometry(QtCore.QRect(660, 387, 221, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackSource.setFont(font)
        self.attackSource.setObjectName("attackSource")
        self.attackType = QtWidgets.QLabel(self)
        self.attackType.setGeometry(QtCore.QRect(660, 311, 221, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackType.setFont(font)
        self.attackType.setObjectName("attackType")
        self.attackRadius = QtWidgets.QLabel(self)
        self.attackRadius.setGeometry(QtCore.QRect(490, 460, 260, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackRadius.setFont(font)
        self.attackRadius.setObjectName("attackRadius")
        self.attackIni = QtWidgets.QLabel(self)
        self.attackIni.setGeometry(QtCore.QRect(660, 413, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackIni.setFont(font)
        self.attackIni.setObjectName("attackIni")
        self.attackChance = QtWidgets.QLabel(self)
        self.attackChance.setGeometry(QtCore.QRect(660, 337, 170, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackChance.setFont(font)
        self.attackChance.setObjectName("attackChance")
        self.attackPurpose = QtWidgets.QLabel(self)
        self.attackPurpose.setGeometry(QtCore.QRect(660, 485, 131, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackPurpose.setFont(font)
        self.attackPurpose.setObjectName("attackPurpose")
        self.description = QtWidgets.QLabel(self)
        self.description.setGeometry(QtCore.QRect(70, 660, 411, 111))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.description.setFont(font)
        self.description.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.description.setWordWrap(True)
        self.description.setObjectName("description")
        self.leadership = QtWidgets.QLabel(self)
        self.leadership.setGeometry(QtCore.QRect(660, 550, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.leadership.setFont(font)
        self.leadership.setObjectName("leadership")
        self.leadershipText = QtWidgets.QLabel(self)
        self.leadershipText.setGeometry(QtCore.QRect(490, 550, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.leadershipText.setFont(font)
        self.leadershipText.setObjectName("leadershipText")
        self.natArmor = QtWidgets.QLabel(self)
        self.natArmor.setGeometry(QtCore.QRect(490, 580, 160, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.natArmor.setFont(font)
        self.natArmor.setObjectName("natArmor")
        self.might = QtWidgets.QLabel(self)
        self.might.setGeometry(QtCore.QRect(490, 610, 160, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.might.setFont(font)
        self.might.setObjectName("might")
        self.weaponMaster = QtWidgets.QLabel(self)
        self.weaponMaster.setGeometry(QtCore.QRect(490, 640, 160, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.weaponMaster.setFont(font)
        self.weaponMaster.setObjectName("weaponMaster")
        self.endurance = QtWidgets.QLabel(self)
        self.endurance.setGeometry(QtCore.QRect(490, 670, 160, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.endurance.setFont(font)
        self.endurance.setObjectName("endurance")
        self.firstStrike = QtWidgets.QLabel(self)
        self.firstStrike.setGeometry(QtCore.QRect(490, 700, 160, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.firstStrike.setFont(font)
        self.firstStrike.setObjectName("firstStrike")
        self.accuracy = QtWidgets.QLabel(self)
        self.accuracy.setGeometry(QtCore.QRect(490, 730, 160, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.accuracy.setFont(font)
        self.accuracy.setObjectName("accuracy")
        self.airResist = QtWidgets.QLabel(self)
        self.airResist.setGeometry(QtCore.QRect(660, 610, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.airResist.setFont(font)
        self.airResist.setObjectName("airResist")
        self.waterResist = QtWidgets.QLabel(self)
        self.waterResist.setGeometry(QtCore.QRect(660, 580, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.waterResist.setFont(font)
        self.waterResist.setObjectName("waterResist")
        self.fireResist = QtWidgets.QLabel(self)
        self.fireResist.setGeometry(QtCore.QRect(660, 640, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.fireResist.setFont(font)
        self.fireResist.setObjectName("fireResist")
        self.earthResist = QtWidgets.QLabel(self)
        self.earthResist.setGeometry(QtCore.QRect(660, 670, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.earthResist.setFont(font)
        self.earthResist.setObjectName("earthResist")

        unit_frame = QPixmap(UNIT_FRAME)
        portrait_img = QPixmap(f"{PORTRAITS}{unit.name}.gif")
        self.background.setPixmap(unit_frame)
        self.portrait.setPixmap(portrait_img)

        self.unitName.setText(str(unit.name))
        self.level.setText(str(unit.level))
        self.exp.setText(f'{unit.curr_exp} / {unit.exp}')
        self.health.setText(f'{unit.curr_health} / {unit.health}')
        self.armor.setText(f'{unit.armor}')
        self.immune.setText(str(unit.immune))
        self.ward.setText(str(unit.ward))
        self.attackType.setText(str(unit.attack_type))

        self.show_accuracy(unit)
        self.show_damage(unit)

        self.attackSource.setText(str(unit.attack_source))
        self.attackIni.setText(str(unit.attack_ini))
        self.attackRadius.setText(str(unit.attack_radius))
        self.attackPurpose.setText(str(unit.attack_purpose))
        self.description.setText(str(unit.desc))

        # Проверяем видимость перков
        if unit.leadership is not None:
            self.leadership.setText(str(unit.leadership))
            self.check_perk(unit.leadership, self.leadership)
            self.check_perk(unit.leadership, self.leadershipText)
        else:
            self.leadershipText.setVisible(False)

        self.check_perk(unit.nat_armor, self.natArmor)
        self.check_perk(unit.might, self.might)
        self.check_perk(unit.weapon_master, self.weaponMaster)
        self.check_perk(unit.nat_armor, self.natArmor)
        self.check_perk(unit.endurance, self.endurance)
        self.check_perk(unit.first_strike, self.firstStrike)
        self.check_perk(unit.accuracy, self.accuracy)
        self.check_perk(unit.water_resist, self.waterResist)
        self.check_perk(unit.air_resist, self.airResist)
        self.check_perk(unit.fire_resist, self.fireResist)
        self.check_perk(unit.earth_resist, self.earthResist)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def show_accuracy(self, unit):
        """Показать точность юнита"""
        if unit.accuracy:
            bonus = int(int(unit.attack_chance) * 0.2)
            if int(unit.accuracy) + bonus >= 100:
                acc = f'{unit.attack_chance}% + ' \
                      f'{100 - int(unit.attack_chance)}'
                self.attackChance.setText(acc)

            elif int(unit.accuracy) + bonus < 100:
                acc = f'{unit.attack_chance}% + {bonus}'
                self.attackChance.setText(acc)
        else:
            self.attackChance.setText(f'{unit.attack_chance}%')

    def show_damage(self, unit):
        """Показать урон юнита"""
        if unit.dot_dmg:
            damage = unit.attack_dmg
            additional = f"/{unit.dot_dmg}"
        else:
            damage = unit.attack_dmg
            additional = ''

        extra_dmg = int(damage * unit.might * 0.25)

        if damage == 300:
            self.attackDmg.setText(f'300 (Макс.){additional}')
            self.attackDmg.setStyleSheet('color: darkred')

        elif unit.might and damage + extra_dmg >= 300:

            dmg = f'{damage} + {300 - damage} (Макс.){additional}'
            self.attackDmg.setText(dmg)
            self.attackDmg.setStyleSheet('color: darkred')

        elif unit.might and damage + extra_dmg < 300:

            dmg = f'{damage} + {extra_dmg}{additional}'
            self.attackDmg.setText(dmg)
            self.attackDmg.setStyleSheet('color: black')
        else:
            self.attackDmg.setText(f'{damage}{additional}')

    @staticmethod
    def check_perk(unit_perk, ui_obj):
        """Проверка перка с выводом на окно характеристик"""
        if unit_perk:
            ui_obj.setVisible(True)
        else:
            ui_obj.setVisible(False)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.leadershipText.setToolTip(
            _translate(
                "Dialog",
                "Позволяет брать предводителю в группу на одного юнита "
                "больше"))
        self.leadershipText.setText(_translate("Dialog", "Лидерство:"))
        self.natArmor.setToolTip(
            _translate(
                "Dialog",
                "Предводитель поглощает 20% полученного урона"))
        self.natArmor.setText(_translate("Dialog", "Природная броня"))
        self.might.setToolTip(
            _translate(
                "Dialog",
                "Добавляет 25% к урону предводителя"))
        self.might.setText(_translate("Dialog", "Мощь"))
        self.weaponMaster.setToolTip(
            _translate(
                "Dialog",
                "Все юниты в группе предводителя получают на 25% больше "
                "опыта в бою"))
        self.weaponMaster.setText(_translate("Dialog", "Инструктор"))
        self.endurance.setToolTip(
            _translate(
                "Dialog",
                "Добавляет дополнительно 20% очков здоровья предводителю"))
        self.endurance.setText(_translate("Dialog", "Выносливость"))
        self.firstStrike.setToolTip(
            _translate(
                "Dialog",
                "Повышает инициативу предводителя на 50%"))
        self.firstStrike.setText(_translate("Dialog", "Первый удар"))
        self.accuracy.setToolTip(
            _translate(
                "Dialog",
                "Повышает шанс удачной атаки предводителя на 20%"))
        self.accuracy.setText(_translate("Dialog", "Точность"))
        self.airResist.setToolTip(
            _translate(
                "Dialog",
                "Защищает предводителя от первой атаки магии Воздуха в бою"))
        self.airResist.setText(_translate("Dialog", "Защита от Воздуха"))
        self.waterResist.setToolTip(
            _translate(
                "Dialog",
                "Защищает предводителя от первой атаки магии Воды в бою"))
        self.waterResist.setText(_translate("Dialog", "Защита от Воды"))
        self.fireResist.setToolTip(
            _translate(
                "Dialog",
                "Защищает предводителя от первой атаки магии Огня в бою"))
        self.fireResist.setText(_translate("Dialog", "Защита от Огня"))
        self.earthResist.setToolTip(
            _translate(
                "Dialog",
                "Защищает предводителя от первой атаки магии Земли в бою"))
        self.earthResist.setText(_translate("Dialog", "Защита от Земли"))


class UnitNameDialog(QDialog):
    """
    Диалог характеристик юнита/героя.
    Вызывается в меню найма юнитов в столице по имени юнита.
    Юнит в окне найма имеет класс, отличный от обычного юнита.
    """

    def __init__(self, unit: str):
        super().__init__()

        self.setFixedSize(914, 826)
        self.setWindowTitle('Характеристики')

        self.background = QtWidgets.QLabel(self)
        self.background.setGeometry(QtCore.QRect(0, 0, 914, 826))
        self.background.setMinimumSize(QtCore.QSize(13, 13))
        self.background.setMaximumSize(QtCore.QSize(914, 826))
        self.background.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.background.setAutoFillBackground(True)
        self.background.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.background.setFrameShadow(QtWidgets.QFrame.Plain)
        self.background.setLineWidth(3)
        self.background.setMidLineWidth(0)
        self.background.setObjectName("background")
        self.portrait = QtWidgets.QLabel(self)
        self.portrait.setGeometry(QtCore.QRect(40, 30, 450, 590))
        self.portrait.setTextFormat(QtCore.Qt.PlainText)
        self.portrait.setScaledContents(True)
        self.portrait.setAlignment(QtCore.Qt.AlignCenter)
        self.portrait.setObjectName("portrait")
        self.unitName = QtWidgets.QLabel(self)
        self.unitName.setGeometry(QtCore.QRect(75, 620, 401, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.unitName.setFont(font)
        self.unitName.setAlignment(QtCore.Qt.AlignCenter)
        self.unitName.setObjectName("unitName")
        self.level = QtWidgets.QLabel(self)
        self.level.setGeometry(QtCore.QRect(660, 76, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.level.setFont(font)
        self.level.setObjectName("level")
        self.exp = QtWidgets.QLabel(self)
        self.exp.setGeometry(QtCore.QRect(660, 102, 171, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.exp.setFont(font)
        self.exp.setObjectName("exp")
        self.health = QtWidgets.QLabel(self)
        self.health.setGeometry(QtCore.QRect(660, 127, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.health.setFont(font)
        self.health.setObjectName("health")
        self.armor = QtWidgets.QLabel(self)
        self.armor.setGeometry(QtCore.QRect(660, 152, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.armor.setFont(font)
        self.armor.setObjectName("armor")
        self.immune = QtWidgets.QLabel(self)
        self.immune.setGeometry(QtCore.QRect(660, 177, 221, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.immune.setFont(font)
        self.immune.setObjectName("immune")
        self.ward = QtWidgets.QLabel(self)
        self.ward.setGeometry(QtCore.QRect(660, 203, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.ward.setFont(font)
        self.ward.setAlignment(QtCore.Qt.AlignLeading |
                               QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ward.setWordWrap(True)
        self.ward.setObjectName("ward")
        self.attackDmg = QtWidgets.QLabel(self)
        self.attackDmg.setGeometry(QtCore.QRect(660, 362, 121, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackDmg.setFont(font)
        self.attackDmg.setObjectName("attackDmg")
        self.attackSource = QtWidgets.QLabel(self)
        self.attackSource.setGeometry(QtCore.QRect(660, 387, 221, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackSource.setFont(font)
        self.attackSource.setObjectName("attackSource")
        self.attackType = QtWidgets.QLabel(self)
        self.attackType.setGeometry(QtCore.QRect(660, 311, 221, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackType.setFont(font)
        self.attackType.setObjectName("attackType")
        self.attackRadius = QtWidgets.QLabel(self)
        self.attackRadius.setGeometry(QtCore.QRect(490, 460, 260, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackRadius.setFont(font)
        self.attackRadius.setObjectName("attackRadius")
        self.attackIni = QtWidgets.QLabel(self)
        self.attackIni.setGeometry(QtCore.QRect(660, 413, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackIni.setFont(font)
        self.attackIni.setObjectName("attackIni")
        self.attackChance = QtWidgets.QLabel(self)
        self.attackChance.setGeometry(QtCore.QRect(660, 337, 121, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackChance.setFont(font)
        self.attackChance.setObjectName("attackChance")
        self.attackPurpose = QtWidgets.QLabel(self)
        self.attackPurpose.setGeometry(QtCore.QRect(660, 485, 131, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.attackPurpose.setFont(font)
        self.attackPurpose.setObjectName("attackPurpose")
        self.description = QtWidgets.QLabel(self)
        self.description.setGeometry(QtCore.QRect(70, 660, 411, 111))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.description.setFont(font)
        self.description.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.description.setWordWrap(True)
        self.description.setObjectName("description")
        self.leadership = QtWidgets.QLabel(self)
        self.leadership.setGeometry(QtCore.QRect(660, 550, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.leadership.setFont(font)
        self.leadership.setObjectName("leadership")
        self.leadershipText = QtWidgets.QLabel(self)
        self.leadershipText.setGeometry(QtCore.QRect(490, 550, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.leadershipText.setFont(font)
        self.leadershipText.setObjectName("leadershipText")
        self.natArmor = QtWidgets.QLabel(self)
        self.natArmor.setGeometry(QtCore.QRect(490, 580, 160, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.natArmor.setFont(font)
        self.natArmor.setObjectName("natArmor")
        self.might = QtWidgets.QLabel(self)
        self.might.setGeometry(QtCore.QRect(490, 610, 160, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.might.setFont(font)
        self.might.setObjectName("might")
        self.weaponMaster = QtWidgets.QLabel(self)
        self.weaponMaster.setGeometry(QtCore.QRect(490, 640, 160, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.weaponMaster.setFont(font)
        self.weaponMaster.setObjectName("weaponMaster")
        self.endurance = QtWidgets.QLabel(self)
        self.endurance.setGeometry(QtCore.QRect(490, 670, 160, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.endurance.setFont(font)
        self.endurance.setObjectName("endurance")
        self.firstStrike = QtWidgets.QLabel(self)
        self.firstStrike.setGeometry(QtCore.QRect(490, 700, 160, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.firstStrike.setFont(font)
        self.firstStrike.setObjectName("firstStrike")
        self.accuracy = QtWidgets.QLabel(self)
        self.accuracy.setGeometry(QtCore.QRect(490, 730, 160, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.accuracy.setFont(font)
        self.accuracy.setObjectName("accuracy")
        self.airResist = QtWidgets.QLabel(self)
        self.airResist.setGeometry(QtCore.QRect(660, 610, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.airResist.setFont(font)
        self.airResist.setObjectName("airResist")
        self.waterResist = QtWidgets.QLabel(self)
        self.waterResist.setGeometry(QtCore.QRect(660, 580, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.waterResist.setFont(font)
        self.waterResist.setObjectName("waterResist")
        self.fireResist = QtWidgets.QLabel(self)
        self.fireResist.setGeometry(QtCore.QRect(660, 640, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.fireResist.setFont(font)
        self.fireResist.setObjectName("fireResist")
        self.earthResist = QtWidgets.QLabel(self)
        self.earthResist.setGeometry(QtCore.QRect(660, 670, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.earthResist.setFont(font)
        self.earthResist.setObjectName("earthResist")

        unit = main_db.get_unit_by_name(unit)
        unit_frame = QPixmap(UNIT_FRAME)
        portrait_img = QPixmap(f"{PORTRAITS}{unit.name}.gif")
        self.background.setPixmap(unit_frame)
        self.portrait.setPixmap(portrait_img)

        self.unitName.setText(str(unit.name))
        self.level.setText(str(unit.level))
        self.exp.setText(f'{unit.curr_exp} / {unit.exp}')
        self.health.setText(f'{unit.curr_health} / {unit.health}')
        self.unitName.setText(str(unit.name))
        self.level.setText(str(unit.level))
        self.exp.setText(f'{unit.curr_exp} / {unit.exp}')
        self.health.setText(f'{unit.curr_health} / {unit.health}')
        self.armor.setText(f'{unit.armor}')
        self.immune.setText(str(unit.immune))
        self.ward.setText(str(unit.ward))
        self.attackType.setText(str(unit.attack_type))
        self.attackChance.setText(f'{unit.attack_chance}%')
        self.attackDmg.setText(f'{unit.attack_dmg}')
        self.attackSource.setText(str(unit.attack_source))
        self.attackIni.setText(str(unit.attack_ini))
        self.attackRadius.setText(str(unit.attack_radius))
        self.attackPurpose.setText(str(unit.attack_purpose))
        self.description.setText(str(unit.desc))
