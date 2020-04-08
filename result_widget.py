# -*- coding: utf-8 -*-

#  implementation generated from reading ui file 'resultWidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class ResultWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi()
        

    def setupUi(self):
        self.resize(659, 355)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.lbl_header = QtWidgets.QLabel()
        self.lbl_header.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.lbl_header)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label = QtWidgets.QLabel()
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.input_nametag = QtWidgets.QLineEdit()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_nametag.sizePolicy().hasHeightForWidth())
        self.input_nametag.setSizePolicy(sizePolicy)
        self.input_nametag.setText("")
        self.input_nametag.setMaxLength(50)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.input_nametag)
        self.label_2 = QtWidgets.QLabel()
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.input_value = QtWidgets.QLineEdit()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(7)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_value.sizePolicy().hasHeightForWidth())
        self.input_value.setSizePolicy(sizePolicy)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.input_value)
        self.label_3 = QtWidgets.QLabel()
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.txt_description = QtWidgets.QTextEdit()
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txt_description)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("", "Расчёты"))
        self.lbl_header.setText(_translate("", "Header"))
        self.label.setText(_translate("", "Наименование:"))
        self.input_nametag.setPlaceholderText(_translate("", "Наименование"))
        self.label_2.setText(_translate("", "Значение:"))
        self.input_value.setPlaceholderText(_translate("", "Значение"))
        self.label_3.setText(_translate("", "Описание:"))
        self.txt_description.setPlaceholderText(_translate("", "Поле для описания"))
