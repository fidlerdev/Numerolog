# desc_window.py

# -*- coding: utf-8 -*- 

from PyQt5 import QtWidgets, QtCore


class DescriptionWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("База с описаниями")
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.list_widget_1 = QtWidgets.QListWidget(self)

        self.group_box = QtWidgets.QGroupBox(self)
        self.vertical_layout_1 = QtWidgets.QVBoxLayout(self)
        self.horizontal_layout_1 = QtWidgets.QHBoxLayout(self)
        self.vertical_layout_2 = QtWidgets.QVBoxLayout(self)

        self.btn_add_value = QtWidgets.QPushButton(self)
        self.spin_box = QtWidgets.QSpinBox(self)

        self.label_1 = QtWidgets.QLabel(self)
        self.list_widget_2 = QtWidgets.QListWidget(self)

        self.label_2 = QtWidgets.QLabel(self)
        self.text_edit = QtWidgets.QPlainTextEdit(self)
        self.horizontal_layout_2 = QtWidgets.QHBoxLayout(self)
        self.btn_save_description = QtWidgets.QPushButton(self)
        self.spacer_item = QtWidgets.QSpacerItem(300, 0)
        

        self.horizontal_layout_3 = QtWidgets.QHBoxLayout(self)
        self.btn_close = QtWidgets.QPushButton(self)

        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.list_widget_1)
        self.main_layout.addWidget(self.group_box)

        self.group_box.setLayout(self.vertical_layout_1)
        self.vertical_layout_1.addLayout(self.horizontal_layout_1)
        self.horizontal_layout_1.addWidget(self.btn_add_value)
        self.horizontal_layout_1.addWidget(self.spin_box)
        self.horizontal_layout_1.addLayout(self.vertical_layout_2)
        self.vertical_layout_2.addWidget(self.label_1)
        self.vertical_layout_2.addWidget(self.list_widget_2)
        self.vertical_layout_1.addWidget(self.text_edit)
        self.vertical_layout_1.addLayout(self.horizontal_layout_2)
        self.horizontal_layout_2.addWidget(self.btn_save_description)
        self.horizontal_layout_2.addSpacerItem(self.spacer_item)
        self.main_layout.addLayout(self.horizontal_layout_3)
        self.horizontal_layout_3.addSpacerItem(self.spacer_item)
        self.horizontal_layout_3.addWidget(self.btn_close)

        self.retranslateUi()

    def retranslateUi(self):
        # Добавляем расчёты:
        # calc = QtWidgets.QListWidgetItem("1. Карта Рождения")
        # calc.setData(QtCore.Qt.UserRole, 1)
        # self.list_widget_1.addItem(calc)
        """
        calc = QtWidgets.QListWidgetItem("2. Квадрат Пифагора")
        calc.setData(QtCore.Qt.UserRole)
        self.list_widget_1.addItem(calc)

        calc = QtWidgets.QListWidgetItem("3. Здоро")
        calc.setData(QtCore.Qt.UserRole)
        self.list_widget_1.addItem(calc)

        calc = QtWidgets.QListWidgetItem("1. Карта Рождения")
        calc.setData(QtCore.Qt.UserRole)
        self.list_widget_1.addItem(calc)

        calc = QtWidgets.QListWidgetItem("1. Карта Рождения")
        calc.setData(QtCore.Qt.UserRole)
        self.list_widget_1.addItem(calc)

        calc = QtWidgets.QListWidgetItem("1. Карта Рождения")
        calc.setData(QtCore.Qt.UserRole)
        self.list_widget_1.addItem(calc)

        calc = QtWidgets.QListWidgetItem("1. Карта Рождения")
        calc.setData(QtCore.Qt.UserRole)
        self.list_widget_1.addItem(calc)

        calc = QtWidgets.QListWidgetItem("1. Карта Рождения")
        calc.setData(QtCore.Qt.UserRole)
        self.list_widget_1.addItem(calc)

        calc = QtWidgets.QListWidgetItem("1. Карта Рождения")
        calc.setData(QtCore.Qt.UserRole)
        self.list_widget_1.addItem(calc)

        calc = QtWidgets.QListWidgetItem("1. Карта Рождения")
        calc.setData(QtCore.Qt.UserRole)
        self.list_widget_1.addItem(calc)

        calc = QtWidgets.QListWidgetItem("1. Карта Рождения")
        calc.setData(QtCore.Qt.UserRole)
        self.list_widget_1.addItem(calc)
        """

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = DescriptionWidget()
    window.show()

    sys.exit(app.exec())