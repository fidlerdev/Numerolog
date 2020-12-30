# desc_window.py

# -*- coding: utf-8 -*- 

from PyQt5 import QtWidgets, QtCore
import sqlite3, json


# TODO:
# 1. Добавить возможность удаления значений 

class DescriptionWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.setupUi()
        print('desc_window.py')
        self.btn_add_value.setEnabled(False)
        self.btn_save_description.setEnabled(False)
        self.btn_delete.setEnabled(False)

        # Подключаемся к базе данных...
        self.con = sqlite3.connect("desc.db")
        self.cur = self.con.cursor()

        # Загружаем данные из базы данных
        self.load()

        # Подключаем слоты к сигналам
        self.btn_add_value.clicked.connect(self.on_add_value)
        self.btn_save_description.clicked.connect(self.on_save)
        self.btn_close.clicked.connect(self.on_close)
        self.list_widget.itemClicked.connect(self.load_values)
        self.list_widget.currentItemChanged.connect(self.load_values)
        self.combo_box.currentIndexChanged.connect(self.on_value_select)
        self.text_description.textChanged.connect(self.check_text_void)
        self.btn_delete.clicked.connect(self.on_delete_value)
    
    def on_delete_value(self):
        num = self.item.data(QtCore.Qt.UserRole)
        values = json.loads(self.get_values(ind=num)[0][1])
        del values[self.combo_box.currentText()]
        values = json.dumps(values)
        self.cur.execute(
            """
            DELETE FROM descriptions WHERE id=?
            """, (num, )
        )
        self.con.commit()

        self.cur.execute(
            """
            INSERT INTO descriptions VALUES (?, ?)
            """, (num, values)
        )
        self.con.commit()
        self.combo_box.removeItem(self.combo_box.currentIndex())
        self.combo_box.repaint()
        self.text_description.repaint()

    # Вызывается при изменении текста описания
    def check_text_void(self):
        filled = self.text_description.toPlainText()
        if filled.strip() and self.combo_box.count():
            self.btn_save_description.setEnabled(True)
        else:
            self.btn_save_description.setEnabled(False)

    # Вызывается при выборе значения из combo_box
    def on_value_select(self, index):
        self.text_description.setPlainText(self.combo_box.itemData(index, QtCore.Qt.UserRole))
        if self.combo_box.count():
            self.btn_delete.setEnabled(True)
        else:
            self.btn_delete.setEnabled(False)
        self.text_description.update()
        self.combo_box.update()

    # Вызывается при выборе алгоритма
    def load_values(self, curr_item, **kwargs):
        index = curr_item.data(QtCore.Qt.UserRole)
        if index == 22:
            self.radioButton_1.setChecked(True)
            self.radioButton_1.setText('1-я Проблема')
            self.radioButton_2.setText('2-я Проблема')
            self.radioButton_3.setText('3-я Проблема')
            self.radioButton_4.setText('4-я Проблема')
            self.radioButton_1.show()
            self.radioButton_2.show()
            self.radioButton_3.show()
            self.radioButton_4.show()

        elif index == 23:
            self.radioButton_1.setChecked(True)
            self.radioButton_1.setText('1-й Пик')
            self.radioButton_2.setText('2-й Пик')
            self.radioButton_3.setText('3-й Пик')
            self.radioButton_4.setText('4-й Пик')
            self.radioButton_1.show()
            self.radioButton_2.show()
            self.radioButton_3.show()
            self.radioButton_4.show()

        elif index == 24:
            self.radioButton_1.setChecked(True)
            self.radioButton_1.setText('1. Формирующий цикл')
            self.radioButton_2.setText('2. Продуктивный цикл')
            self.radioButton_3.setText('3. Результативный цикл')
            self.radioButton_1.show()
            self.radioButton_2.show()
            self.radioButton_3.show()
            self.radioButton_4.hide()
        else:
            self.radioButton_1.hide()
            self.radioButton_2.hide()
            self.radioButton_3.hide()
            self.radioButton_4.hide()

        self.load()

        self.combo_box.clear()
        self.btn_add_value.setEnabled(True)
        self.item = curr_item
        values = self.get_values(ind=index)
        # Если найдены значения для выбранного алгоритма
        if values:
            values = json.loads(values[0][1])
            for key, value in values.items():
                self.combo_box.addItem(key, value)
        self.combo_box.update()


    def get_values(self, ind):
        return [values for values in self.descriptions if values[0] == ind]


    def load(self):
        self.cur.execute(
            """
            SELECT * FROM descriptions;
            """
            )
        self.descriptions = self.cur.fetchall()
        from pprint import pprint
        pprint(self.descriptions)

    def on_save(self):
        cur_val = self.combo_box.currentText()

        values = self.get_values(ind=self.item.data(QtCore.Qt.UserRole))
        # Если для выбранного алгоритма уже есть значения
        if values:
            values = json.loads(values[0][1])
            values[cur_val] = self.text_description.toPlainText()
            self.cur.execute(
                """
                DELETE FROM descriptions WHERE id=?
                """, (self.item.data(QtCore.Qt.UserRole), )
            )
            self.con.commit()
        else:
            values = {cur_val: self.text_description.toPlainText()}
            
        values = json.dumps(values)
        self.cur.execute(
            """
            INSERT INTO descriptions VALUES (?, ?)
            """, (self.item.data(QtCore.Qt.UserRole), values)
        )
        self.con.commit()
        # Обновляем self.descriptions
        self.load()
        # Добавляем описание в combo_box
        self.combo_box.setItemData(
            self.combo_box.findText(str(cur_val)),  # Index
            self.text_description.toPlainText(),    # Value
            QtCore.Qt.UserRole                      # Role
            )

    # Вызывается при нажатии кнопки "Добавить"
    def on_add_value(self):
        all_items = [self.combo_box.itemText(i) for i in range(self.combo_box.count())]
        if str(self.spin_box.value()) in all_items:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Значение уже существует", defaultButton=QtWidgets.QMessageBox.Ok)
            return
        
        ind = self.item.data(QtCore.Qt.UserRole)
        # Если выбран алгоритм с 23 по 25
        pref = ''
        print(ind in range(22, 24 + 1))
        if ind in range(22, 24 + 1):
            if self.radioButton_1.isChecked():
                pref = '1'
                print(1)
            elif self.radioButton_2.isChecked():
                pref = '2'
                print(2)
            elif self.radioButton_3.isChecked():
                pref = '3'
                print(3)
            if self.radioButton_4.isChecked():
                pref = '4'
                print(4)
            if (pref + ' : ' + str(self.spin_box.value())) in all_items:
                QtWidgets.QMessageBox.warning(self, "Предупреждение", "Значение уже существует", defaultButton=QtWidgets.QMessageBox.Ok)
                return
            self.combo_box.addItem(pref + ' : ' + str(self.spin_box.value()))
            self.combo_box.setCurrentText(pref + ' : ' + str(self.spin_box.value()))
        else:
            self.combo_box.addItem(str(self.spin_box.value()))
            self.combo_box.setCurrentText(str(self.spin_box.value()))
        self.combo_box.repaint()


    def on_close(self):
        self.close()
        self.cur.close()
        self.con.close()

    def setupUi(self):
        self.setWindowTitle("База с описаниями")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.label_1 = QtWidgets.QLabel()
        self.verticalLayout.addWidget(self.label_1)
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setSelectionRectVisible(False)
        self.verticalLayout.addWidget(self.list_widget)
        self.group_box = QtWidgets.QGroupBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.group_box.sizePolicy().hasHeightForWidth())
        self.group_box.setSizePolicy(sizePolicy)
        self.group_box.setMinimumSize(QtCore.QSize(0, 0))
        self.group_box.setBaseSize(QtCore.QSize(0, 0))
        self.group_box.setTitle("")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.group_box)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, -1, -1, 11)
        self.spin_box = QtWidgets.QSpinBox(self.group_box)
        self.spin_box.setWrapping(False)
        self.spin_box.setFrame(True)
        self.spin_box.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.spin_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spin_box.setMaximum(9999)
        self.gridLayout.addWidget(self.spin_box, 0, 1, 1, 1)
        self.btn_add_value = QtWidgets.QPushButton(self.group_box)
        self.gridLayout.addWidget(self.btn_add_value, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.group_box)
        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)
        self.combo_box = QtWidgets.QComboBox(self.group_box)
        self.gridLayout.addWidget(self.combo_box, 1, 3, 1, 1)
        ''' '''
        # Добавляем кнопки выбора типа значения для алгоритмов 23-25
        self.radiobuttonVLayout = QtWidgets.QVBoxLayout()
        self.radioButton_1 = QtWidgets.QRadioButton()
        self.radiobuttonVLayout.addWidget(self.radioButton_1)
        self.radioButton_2 = QtWidgets.QRadioButton()
        self.radiobuttonVLayout.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton()
        self.radiobuttonVLayout.addWidget(self.radioButton_3)
        self.radioButton_4 = QtWidgets.QRadioButton()
        self.radiobuttonVLayout.addWidget(self.radioButton_4)
        self.gridLayout.addLayout(self.radiobuttonVLayout, 1, 0, 1, 1)
        self.radioButton_1.setChecked(True)
        self.radioButton_1.hide()
        self.radioButton_2.hide()
        self.radioButton_3.hide()
        self.radioButton_4.hide()
        ''' '''
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.label_3 = QtWidgets.QLabel(self.group_box)
        self.verticalLayout_2.addWidget(self.label_3)
        self.text_description = QtWidgets.QPlainTextEdit(self.group_box)
        self.verticalLayout_2.addWidget(self.text_description)
        self.label_4 = QtWidgets.QLabel()
        self.verticalLayout_2.addWidget(self.label_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 16)
        self.btn_save_description = QtWidgets.QPushButton(self.group_box)
        self.horizontalLayout_3.addWidget(self.btn_save_description)
        self.btn_delete = QtWidgets.QPushButton(self.group_box)
        self.horizontalLayout_3.addWidget(self.btn_delete)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addWidget(self.group_box)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btn_close = QtWidgets.QPushButton()
        self.horizontalLayout.addWidget(self.btn_close)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        # Добавляем расчёты:
        calc = QtWidgets.QListWidgetItem("1. День Рождения")
        calc.setData(QtCore.Qt.UserRole, 0)
        self.list_widget.addItem(calc)
        
        calc = QtWidgets.QListWidgetItem("2. Число Жизненного Пути")
        calc.setData(QtCore.Qt.UserRole, 1)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("3. Сочетание Дня Рождения и ЧЖП")
        calc.setData(QtCore.Qt.UserRole, 2)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("5. Здоровье по Зюрняевой")
        calc.setData(QtCore.Qt.UserRole, 4)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("6. Ментальное число")
        calc.setData(QtCore.Qt.UserRole, 5)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("7. Финансы по Зюрняевой")
        calc.setData(QtCore.Qt.UserRole, 6)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("8. Таланты")
        calc.setData(QtCore.Qt.UserRole, 7)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("9. Профессии")
        calc.setData(QtCore.Qt.UserRole, 8)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("11. Число судьбы")
        calc.setData(QtCore.Qt.UserRole, 10)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("12. Число души")
        calc.setData(QtCore.Qt.UserRole, 11)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("13. Число Индивидуальности")
        calc.setData(QtCore.Qt.UserRole, 12)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("14. Число Зрелости")
        calc.setData(QtCore.Qt.UserRole, 13)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("15. Число Равновесия")
        calc.setData(QtCore.Qt.UserRole, 14)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("16. Число Активности")
        calc.setData(QtCore.Qt.UserRole, 15)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("17. Число Интеллекта")
        calc.setData(QtCore.Qt.UserRole, 16)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("18. Число Наследственности")
        calc.setData(QtCore.Qt.UserRole, 17)
        self.list_widget.addItem(calc)
        
        calc = QtWidgets.QListWidgetItem("19. Карта Инклюзий")
        calc.setData(QtCore.Qt.UserRole, 18)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("20. Кармические уроки")
        calc.setData(QtCore.Qt.UserRole, 19)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("21. Скрытая страсть (Тайное желание)")
        calc.setData(QtCore.Qt.UserRole, 20)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("22. Подсознательное «Я»")
        calc.setData(QtCore.Qt.UserRole, 21)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem('23. Проблемы, уроки, препятствия')
        calc.setData(QtCore.Qt.UserRole, 22)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem('24. Пики, достижения, вершины')
        calc.setData(QtCore.Qt.UserRole, 23)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem('25. Жизненные циклы')
        calc.setData(QtCore.Qt.UserRole, 24)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("26. Персональный год")
        calc.setData(QtCore.Qt.UserRole, 25)
        self.list_widget.addItem(calc)

        calc = QtWidgets.QListWidgetItem("27. Число Наследственности")
        calc.setData(QtCore.Qt.UserRole, 26)
        self.list_widget.addItem(calc)

        self.label_1.setText("Выберите алгоритм:")
        self.label_2.setText("Выберите значение:")
        self.label_3.setText("Введите описание:")
        self.label_4.setText("*Значения без описания не сохраняются")

        self.btn_add_value.setText("Добавить")
        self.btn_save_description.setText("Сохранить описание")
        self.btn_close.setText("Закрыть")
        self.btn_delete.setText("Удалить описание")

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = DescriptionWidget()
    window.show()

    sys.exit(app.exec())