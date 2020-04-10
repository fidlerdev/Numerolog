# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from dialog_windows import CloseDialog
from save_data import save
from load_data import load
from load_data import load_settings

class UserWidget(QtWidgets.QWidget):

    def __init__(self, operation, user_name, path):
        QtWidgets.QWidget.__init__(self, parent=None)
        self.setupUi(self)

        self.label_head.setText(operation + " клиента")
        self.closing = False

        # Список дополнительных имен, который изменяется во время обработки сигналов окна
        self.bonus_list = []
        # Заголовок
        self.label_head = QtWidgets.QLabel(operation + " клиента")

        for dictionary in load_settings()["dictionary_list"]:
            self.combobox_main_dictionary.addItem(dictionary)
            self.combobox_bonus_dictionary.addItem(dictionary)

        self.combobox_bonus_dictionary.setCurrentText("Русский")
        self.combobox_main_dictionary.setCurrentText("Русский")

        # Если данные редактируем, то нужно их загрузить из файла
        if operation == "Редактирование данных":
            data = load(path=path)
            self.bonus_list = data["bonus_list"]

            self.input_surname.setText(data["surname"])
            self.input_name.setText(data["name"])
            self.input_middle_name.setText(data["middle_name"])
            self.input_date_birth.setDate(QtCore.QDate(data["date_of_birth"][-1],
                                                        data["date_of_birth"][-2],
                                                        data["date_of_birth"][-3]))
            self.input_time_birth.setTime(QtCore.QTime(data["time_of_birth"][0],
                                                        data["time_of_birth"][1]))
            self.input_moon_birth.setValue(data["moon_birth"])

            # Обратная совместимость с версиями, в которых нет даты добавления доп. Ф. И. О
            for item in data["bonus_list"]:
                if "time" in item.keys():
                    self.list_widget.addItem("{surname} {name} {middle_name}\t\tДобавлено: {day}.{month}.{year}".format(surname=item["surname"],
                                                                                    name=item["name"],
                                                                                    middle_name=item["middle_name"],
                                                                                    day=item["time"].split(".")[0].rjust(2, "0"),
                                                                                    month=item["time"].split(".")[1].rjust(2, "0"),
                                                                                    year=item["time"].split(".")[2]).strip())
                else:
                    self.list_widget.addItem("{surname} {name} {middle_name}".format(surname=item["surname"],
                                                                                    name=item["name"],
                                                                                    middle_name=item["middle_name"]))
            self.check_for_delete.setChecked(not data["delete"])
            self.combobox_main_dictionary.setCurrentText(data["dictionary"])
            self.check_void_main()
            

        self.input_name.textChanged.connect(self.check_void_main)
        self.input_bonus_name.textChanged.connect(self.check_void_bonus)

        self.btn_add_user_to_list.clicked.connect(self.add_bonus)

        # При нажатии на ячейку доп имён актвируем кнопку удаления
        self.list_widget.itemClicked.connect(lambda: self.btn_delete_selected_item.setEnabled(True))

        self.btn_delete_selected_item.clicked.connect(self.delete_bonus)
        
        self.btn_quit.clicked.connect(self.quit_action)
        self.btn_save.clicked.connect(lambda: self.save(path))

    def check_void_main(self):
        # Проверка полей на наличие данных
        filled = self.input_name.text().strip()
        if filled:
            self.btn_save.setEnabled(True)
        else:
            self.btn_save.setEnabled(False)
        
    def check_void_bonus(self):
        filled = self.input_bonus_name.text().strip()
        if filled:
            self.btn_add_user_to_list.setEnabled(True)
        else:
            self.btn_add_user_to_list.setEnabled(False)

    def add_bonus(self):
        surname = self.input_bonus_surname.text()
        name = self.input_bonus_name.text()
        middle_name = self.input_bonus_middle_name.text()
        print("——— {surname} {name} {middle_name} добавлен".format(surname=surname, name=name, middle_name=middle_name))
        day = self.input_bonus_date.date().day()
        month = self.input_bonus_date.date().month()
        year = self.input_bonus_date.date().year()
        self.bonus_list.append({"surname": surname,
                                "name": name,
                                "middle_name": middle_name,
                                "time": "{day}.{month}.{year}".format(
                                    day=day,
                                    month=month,
                                    year=year
                                ),
                                "dictionary": self.combobox_bonus_dictionary.currentText()})

        self.list_widget.addItem("{surname} {name} {middle_name}\t\tДобавлено: {time}".format(surname=surname,
                                                                            name=name,
                                                                            middle_name=middle_name,
                                                time="{day}.{month}.{year}".format(
                                                    day=str(day).rjust(2, "0"),
                                                    month=str(month).rjust(2, "0"),
                                                    year=str(year).rjust(2, "0")
                                                )).strip())

        self.input_bonus_surname.clear()
        self.input_bonus_name.clear()
        self.input_bonus_middle_name.clear()
        self.input_bonus_date.clear()

    def delete_bonus(self, index): 
        del self.bonus_list[self.list_widget.currentRow()]
        del_item = self.list_widget.takeItem(self.list_widget.currentRow())
        if self.list_widget.count() == 0: self.btn_delete_selected_item.setEnabled(False)
        else: self.btn_delete_selected_item.setEnabled(True)
        self.btn_delete_selected_item.update()
        print("——— {name} удалён".format(name=del_item.text()))

    def on_close(self):
        dialog = CloseDialog(self)
        # Переопределяем надпись в модальном окне
        dialog.label.setText("Вы действительно хотите закрыть окно?\nВсе несохраненные данные будут утеряны")

        return dialog.exec()

    def quit_action(self):
        result = self.on_close()
        self.closing = True
        if result == QtWidgets.QMessageBox.Accepted:
            self.close()

    # Сохраняем данные в файл по указанному пути
    def save(self, path):
        delete = False if self.check_for_delete.isChecked() else True
        save(path=path,
            surname=self.input_surname.text(),
            name=self.input_name.text(),
            middle_name=self.input_middle_name.text(),
            bonus_list=self.bonus_list,
            date_of_birth=(self.input_date_birth.date().day(),
                    self.input_date_birth.date().month(),
                    self.input_date_birth.date().year()),
            time_of_birth=(self.input_time_birth.time().hour(),
                    self.input_time_birth.time().minute()),
            moon_birth=self.input_moon_birth.value(),
            delete=delete,
            dictionary=self.combobox_main_dictionary.currentText())

    def closeEvent(self, event):
        if not self.closing:
            result = self.on_close()
            if result == QtWidgets.QMessageBox.Accepted:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def custom_context_menu(self, pos):
        menu = QtWidgets.QMenu(self)
        # Cut
        cut = QtWidgets.QAction("Вырезать")
        cut.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_X)
        cut.triggered.connect(lambda: self.focusWidget().cut())
        menu.addAction(cut)

        # Copy
        copy = QtWidgets.QAction("Скопировать")
        copy.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_C)
        copy.triggered.connect(lambda: self.focusWidget().copy())
        menu.addAction(copy)


        # Paste
        paste = QtWidgets.QAction("Вставить")
        paste.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_V)
        paste.triggered.connect(lambda: self.focusWidget().paste())
        menu.addAction(paste)


        menu.addSeparator()

        # Select All
        select_all = QtWidgets.QAction("Выделить все")
        select_all.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_A)
        select_all.triggered.connect(lambda: self.focusWidget().selectAll())
        menu.addAction(select_all)


        menu.exec(self.mapToGlobal(pos))

    def setupUi(self, Form):
        self.name_font = QtGui.QFont("Helvetica", 11, italic=True)
        Form.resize(800, 667)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.label_head = QtWidgets.QLabel(Form)
        self.label_head.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_2.addWidget(self.label_head)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_surname = QtWidgets.QLabel(self.groupBox)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_surname)
        self.input_surname = QtWidgets.QLineEdit(self.groupBox)
        self.input_surname.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.input_surname.customContextMenuRequested.connect(self.custom_context_menu)
        self.input_surname.setFont(self.name_font)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.input_surname)
        self.label_name = QtWidgets.QLabel(self.groupBox)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_name)
        self.input_name = QtWidgets.QLineEdit(self.groupBox)
        self.input_name.setFont(self.name_font)
        self.input_name.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.input_name.customContextMenuRequested.connect(self.custom_context_menu)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.input_name)
        self.label_middle_name = QtWidgets.QLabel(self.groupBox)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_middle_name)
        self.input_middle_name = QtWidgets.QLineEdit(self.groupBox)
        self.input_middle_name.setFont(self.name_font)
        self.input_middle_name.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.input_middle_name.customContextMenuRequested.connect(self.custom_context_menu)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.input_middle_name)
        self.verticalLayout_2.addWidget(self.groupBox)
        # Выбор основного алфавита  
        self.label_main_dictionary = QtWidgets.QLabel()
        self.verticalLayout_2.addWidget(self.label_main_dictionary)
        self.combobox_main_dictionary = QtWidgets.QComboBox()
        self.verticalLayout_2.addWidget(self.combobox_main_dictionary)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setCheckable(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_date_birth = QtWidgets.QLabel(self.groupBox_2)
        self.label_date_birth.setObjectName("label_date_birth")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_date_birth)
        self.input_date_birth = QtWidgets.QDateEdit(self.groupBox_2)
        self.input_date_birth.setWrapping(False)
        self.input_date_birth.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.input_date_birth.setSpecialValueText("")
        self.input_date_birth.setAlignment(QtCore.Qt.AlignRight)
        self.input_date_birth.setAccelerated(False)
        self.input_date_birth.setCurrentSection(QtWidgets.QDateTimeEdit.DaySection)
        self.input_date_birth.setCalendarPopup(True)
        self.input_date_birth.setObjectName("input_date_birth")
        self.input_date_birth.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.input_date_birth.customContextMenuRequested.connect(self.custom_context_menu)
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.input_date_birth)
        self.label_time_birth = QtWidgets.QLabel(self.groupBox_2)
        self.label_time_birth.setObjectName("label_time_birth")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_time_birth)
        self.input_time_birth = QtWidgets.QTimeEdit(self.groupBox_2)
        self.input_time_birth.setAlignment(QtCore.Qt.AlignRight)
        self.input_time_birth.setMinimumSize(QtCore.QSize(68, 0))
        self.input_time_birth.setObjectName("input_time_birth")
        self.input_time_birth.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.input_time_birth.customContextMenuRequested.connect(self.custom_context_menu)
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.input_time_birth)
        self.label_moon_birth = QtWidgets.QLabel(self.groupBox_2)
        self.label_moon_birth.setObjectName("label_moon_birth")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_moon_birth)
        self.input_moon_birth = QtWidgets.QSpinBox(self.groupBox_2)
        self.input_moon_birth.setAlignment(QtCore.Qt.AlignRight)
        self.input_moon_birth.setMinimumSize(QtCore.QSize(48, 0))
        self.input_moon_birth.setMaximumSize(QtCore.QSize(48, 16777215))
        self.input_moon_birth.setObjectName("input_moon_birth")
        self.input_moon_birth.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.input_moon_birth.customContextMenuRequested.connect(self.custom_context_menu)
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.input_moon_birth)
        self.horizontalLayout_5.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, 50)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.formLayout_4 = QtWidgets.QFormLayout(self.groupBox_3)
        self.formLayout_4.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_4.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_bonus_surname = QtWidgets.QLabel(self.groupBox_3)
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_bonus_surname)
        self.input_bonus_surname = QtWidgets.QLineEdit(self.groupBox_3)
        self.input_bonus_surname.setFont(self.name_font)
        self.input_bonus_surname.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.input_bonus_surname.customContextMenuRequested.connect(self.custom_context_menu)
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.input_bonus_surname)
        self.label_bonus_name = QtWidgets.QLabel(self.groupBox_3)
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_bonus_name)
        self.input_bonus_name = QtWidgets.QLineEdit(self.groupBox_3)
        self.input_bonus_name.setFont(self.name_font)
        self.input_bonus_name.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.input_bonus_name.customContextMenuRequested.connect(self.custom_context_menu)
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.input_bonus_name)
        self.label_bonus_midle_name = QtWidgets.QLabel(self.groupBox_3)
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_bonus_midle_name)
        self.input_bonus_middle_name = QtWidgets.QLineEdit(self.groupBox_3)
        self.input_bonus_middle_name.setFont(self.name_font)
        self.input_bonus_middle_name.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.input_bonus_middle_name.customContextMenuRequested.connect(self.custom_context_menu)
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.input_bonus_middle_name)
        # Дата добавления дополнительных Ф. И. О. по документам
        self.label_bonus_date = QtWidgets.QLabel(self.groupBox_3)
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_bonus_date)
        self.input_bonus_date = QtWidgets.QDateEdit(self.groupBox_3)
        self.input_bonus_date.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.input_bonus_date.customContextMenuRequested.connect(self.custom_context_menu)
        self.input_bonus_date.setCalendarPopup(True)
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.input_bonus_date)
        # Алфавит для дополнительных Ф. И. О.
        self.label_bonus_dictionary = QtWidgets.QLabel(self.groupBox_3)
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_bonus_dictionary)
        self.combobox_bonus_dictionary = QtWidgets.QComboBox(self.groupBox_3)
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.combobox_bonus_dictionary)
        self.btn_add_user_to_list = QtWidgets.QPushButton(self.groupBox_3)
        self.btn_add_user_to_list.setEnabled(False)
        self.btn_add_user_to_list.setAutoDefault(False)
        self.formLayout_4.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.btn_add_user_to_list)
        self.horizontalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.list_widget = QtWidgets.QListWidget(self.groupBox_4)
        self.verticalLayout.addWidget(self.list_widget)
        self.delete_layout = QtWidgets.QVBoxLayout()
        self.btn_delete_selected_item = QtWidgets.QPushButton(self.groupBox_4)
        self.btn_delete_selected_item.setEnabled(False)
        self.btn_delete_selected_item.setFlat(False)
        self.verticalLayout.addWidget(self.btn_delete_selected_item)
        self.verticalLayout_2.addLayout(self.delete_layout)
        self.horizontalLayout_4.addWidget(self.groupBox_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.check_for_delete = QtWidgets.QCheckBox()
        self.verticalLayout_2.addWidget(self.check_for_delete)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_save = QtWidgets.QPushButton(Form)
        self.btn_save.setEnabled(False)
        self.horizontalLayout.addWidget(self.btn_save)
        self.btn_quit = QtWidgets.QPushButton(Form)
        self.horizontalLayout.addWidget(self.btn_quit)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Редактирование")
        self.label_head.setText("code::type")
        self.groupBox.setTitle("Ф. И. О. ")
        self.label_surname.setText("Фамилия:")
        self.check_for_delete.setText("Нельзя удалить клиента")
        self.label_name.setText("Имя:")
        self.label_middle_name.setText("Отчество:")
        self.label_main_dictionary.setText("Выберите алфавит:")
        self.label_bonus_dictionary.setText("Выберите алфавит:")
        self.groupBox_2.setTitle("Даты и время")
        self.label_date_birth.setText("Дата рождения:")
        self.label_time_birth.setText("Время рождения:")
        self.label_moon_birth.setText("Лунный день рождения")
        self.groupBox_3.setTitle("Изменение Ф. И. О.")
        self.label_bonus_surname.setText("Фамилия:")
        self.label_bonus_name.setText("Имя:")
        self.label_bonus_midle_name.setText("Отчество:")
        self.label_bonus_date.setText("Дата добавления:")
        self.btn_add_user_to_list.setText("Добавить")
        self.groupBox_4.setTitle("Список измененных Ф. И. О.")
        self.btn_delete_selected_item.setText("Удалить")
        self.btn_save.setText("Сохранить")
        self.btn_quit.setText("Закрыть")
