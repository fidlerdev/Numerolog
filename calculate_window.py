# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets, uic
from load_data import load
from load_resources import get_icons
from result_widget import ResultWidget

class CalculateWidget(QtWidgets.QWidget):
    def __init__(self, parent, path):
        QtWidgets.QWidget.__init__(self, parent)
        self.path = path
        self.icons = get_icons()
        self.setupUi()
        self.load_data(path=path)
        
        self.btn_close.clicked.connect(self.close)

        self.list_calculate.itemClicked.connect(self.on_item_clicked)
        self.btn_calculate.clicked.connect(self.calculate)


    def load_data(self, path):
        self.data = load(path)

        self.label_surname.setText("Фамилия:\t\t\t" + self.data["surname"])
        self.label_name.setText("Имя:\t\t\t\t" + self.data["name"])
        self.label_middle_name.setText("Отчество:\t\t\t" + self.data["middle_name"])

        self.label_date_of_birth.setText("Дата рождения:\t\t" + str(self.data["date_of_birth"][0]).rjust(2, "0") + 
                                        "." + str(self.data["date_of_birth"][1]).rjust(2, "0")
                                        + "." + str(self.data["date_of_birth"][2]))
        self.label_time_of_birth.setText("Время рождения:\t\t" + str(self.data["time_of_birth"][0]).rjust(2, "0") + 
                                        ":" + str(self.data["time_of_birth"][1]).rjust(2, "0"))
        self.label_moon_birth.setText("Лунный день рождения:\t" + str(self.data["moon_birth"]).rjust(2, "0"))

    def on_item_clicked(self, item):
        self.selected_item = item
        self.btn_calculate.setEnabled(True)
        self.btn_print.setEnabled(True)

    def calculate(self):
        row = self.list_calculate.row(self.selected_item)
        # Карта Рождения
        if row == 0:
            self.header_text = "Карта Рождения"
            self.value = 0

        # Квадрат Пифагора
        elif row == 1:
            self.header_text = "Квадрат Пифагора"
            self.value = 0

        # Здоровье по Зюрняевой
        elif row == 2:
            self.header_text = "Здоровье по Зюрняевой"
            self.value = self.data["date_of_birth"][0]

        # Финансы по зюрняевой
        elif row == 3:
            self.header_text = "Финансы по Зюрняевой"
            self.value = self.data["date_of_birth"][1] // 10 + self.data["date_of_birth"][1] % 10
        
        # Дата рождения по Розе Петровне
        elif row == 4:
            self.header_text = "Дата Рождения по Розе Петровне"
            self.value = 0
        
        # Числа Ф. И. О.
        elif row == 5:
            self.header_text = "Числа Ф. И. О."
            self.value = 0

        # Карта инклюзий
        elif row == 6:
            self.header_text = "Карта инклюзий"
            self.value = 0
        
        # Число кармического долга
        elif row == 7:
            self.header_text = "Число кармического долга"
            self.value = 0

        # Мандала по Зюрняевой
        elif row == 8:
            self.header_text = "Мандала по Зюрняевой"
            self.value = 0

        # Коды по Кабарухиной
        elif row == 9:
            self.header_text = "Коды по Кабарухиной"
            self.value = 0

        self.result_widget = ResultWidget(
            path=self.path,
            header_text=self.header_text,
            value=self.value,
            row_id=row
            )
        self.result_widget.show()
        
    def setupUi(self):
        self.resize(361, 607)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.btn_print = QtWidgets.QPushButton(self)
        self.btn_print.setEnabled(False)
        self.gridLayout.addWidget(self.btn_print, 5, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(30, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
        self.btn_calculate = QtWidgets.QPushButton(self)
        self.btn_calculate.setEnabled(False)
        self.gridLayout.addWidget(self.btn_calculate, 4, 1, 1, 1)
        self.btn_close = QtWidgets.QPushButton(self)
        self.gridLayout.addWidget(self.btn_close, 7, 1, 1, 1)
        self.list_calculate = QtWidgets.QListWidget(self)
        self.list_calculate.setFrameShape(QtWidgets.QFrame.Box)
        self.list_calculate.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list_calculate.setDragEnabled(False)
        self.list_calculate.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.list_calculate.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.list_calculate.setProperty("isWrapping", False)
        self.list_calculate.setResizeMode(QtWidgets.QListView.Fixed)

        item = QtWidgets.QListWidgetItem()
        self.list_calculate.addItem(item)

        item = QtWidgets.QListWidgetItem()
        self.list_calculate.addItem(item)

        item = QtWidgets.QListWidgetItem()
        self.list_calculate.addItem(item)

        item = QtWidgets.QListWidgetItem()
        self.list_calculate.addItem(item)

        item = QtWidgets.QListWidgetItem()
        self.list_calculate.addItem(item)

        item = QtWidgets.QListWidgetItem()
        self.list_calculate.addItem(item)

        item = QtWidgets.QListWidgetItem()
        self.list_calculate.addItem(item)

        item = QtWidgets.QListWidgetItem()
        self.list_calculate.addItem(item)

        item = QtWidgets.QListWidgetItem()
        self.list_calculate.addItem(item)

        item = QtWidgets.QListWidgetItem()
        self.list_calculate.addItem(item)

        self.gridLayout.addWidget(self.list_calculate, 3, 1, 1, 1)
        self.groupbox_date = QtWidgets.QGroupBox(self)
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupbox_date)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.label_date_of_birth = QtWidgets.QLabel(self.groupbox_date)
        self.verticalLayout_3.addWidget(self.label_date_of_birth)
        self.label_time_of_birth = QtWidgets.QLabel(self.groupbox_date)
        self.verticalLayout_3.addWidget(self.label_time_of_birth)
        self.label_moon_birth = QtWidgets.QLabel(self.groupbox_date)
        self.verticalLayout_3.addWidget(self.label_moon_birth)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupbox_date, 1, 1, 1, 1)
        self.groupbox_name = QtWidgets.QGroupBox(self)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupbox_name)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.label_surname = QtWidgets.QLabel(self.groupbox_name)
        self.verticalLayout_2.addWidget(self.label_surname)
        self.label_name = QtWidgets.QLabel(self.groupbox_name)
        self.verticalLayout_2.addWidget(self.label_name)
        self.label_middle_name = QtWidgets.QLabel(self.groupbox_name)
        self.verticalLayout_2.addWidget(self.label_middle_name)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupbox_name, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 6, 1, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.retranslateUi()



    def retranslateUi(self):
        self.setWindowTitle("Расчёты")
        self.btn_print.setText("Распечатать")
        self.btn_print.setIcon(self.icons["print"])
        self.btn_calculate.setText("Рассчитать")
        self.btn_calculate.setIcon(self.icons["calculate"])
        self.btn_close.setText("Закрыть")
        __sortingEnabled = self.list_calculate.isSortingEnabled()
        self.list_calculate.setSortingEnabled(False)
        item = self.list_calculate.item(0)
        item.setText("1. Карта Рождения")
        item = self.list_calculate.item(1)
        item.setText("2. Квадрат Пифагора")
        item = self.list_calculate.item(2)
        item.setText("3. Здоровье по Зюрняевой")
        item = self.list_calculate.item(3)
        item.setText("4. Финансы по Зюрняевой")
        item = self.list_calculate.item(4)
        item.setText("5. Дата рождения по Розе Петровне")
        item = self.list_calculate.item(5)
        item.setText("6. Числа Ф. И. О.")
        item = self.list_calculate.item(6)
        item.setText("7. Карта инклюзий")
        item = self.list_calculate.item(7)
        item.setText("8. Число кармического долга")
        item = self.list_calculate.item(8)
        item.setText("9. Мандала по Зюрняевой")
        item = self.list_calculate.item(9)
        item.setText("10. Коды по Кабарухиной")
        self.list_calculate.setSortingEnabled(__sortingEnabled)
        self.groupbox_date.setTitle("Даты")
        self.label_date_of_birth.setText("Дата рождения")
        self.label_time_of_birth.setText("Время рождения")
        self.label_moon_birth.setText("Лунный день рождения")
        self.groupbox_name.setTitle("Ф. И. О.")
        self.label_surname.setText("Фамилия")
        self.label_name.setText("Имя")
        self.label_middle_name.setText("Отчество")




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = CalculateWidget(None, r"/Users/fidler/Desktop/Контрагенты/Ваня.json")
    widget.show()
    sys.exit(app.exec())