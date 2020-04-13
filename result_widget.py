# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3, json
from load_data import load

class ResultWidget(QtWidgets.QWidget):

    def __init__(self, path, header_text, value, row_id, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi()
        self.value = value
        self.header_text = header_text
        self.row_id = row_id
        self.path=path

        self.con = sqlite3.connect("desc.db")
        self.cur = self.con.cursor()

        self.load_desc()
        
        self.lbl_header.setText(self.header_text)
        self.input_value.setText(str(self.value))


        self.btn_close.clicked.connect(self.on_close)
        self.btn_save.clicked.connect(self.on_save)

    """ 
    Это, наверное, самый костыльный костыль из костылей, что я делал 
    Нужно хотя бы оптимизировать это д***мо и подогнать к DIY
    """

    def load_desc(self):
        custom_desc_list = load(path=self.path)["desc_list"]
        # Проверка на значение None
        if custom_desc_list:
            print(custom_desc_list)
            custom_desc_list = [x[1] for x in custom_desc_list if x[0] == self.row_id]
            # Если нашли значения для выбранного алгоритма
            if custom_desc_list:
                custom_desc_list = custom_desc_list[0]
                print("custom_desc_list", custom_desc_list)
                print("self.value:", self.value)
                print(str(self.value) in custom_desc_list)
                # Если для значения установлено уникальное описание
                if str(self.value) in custom_desc_list:
                    self.txt_description.setText(custom_desc_list[str(self.value)].encode('utf-8').decode('unicode-escape'))
                # В противном случае ищем описания заданные по умолчанию для данного значения в БАЗЕ
                else:
                    self.cur.execute(
                        """
                        SELECT desc_list FROM descriptions WHERE id=?
                        """, (self.row_id, )
                    )
                    values = self.cur.fetchall()
                    # Если есть значения, заданные в базе
                    if values:
                        values = json.loads(values[0][0])
                        # Если в базе есть описание для данного значения
                        if str(self.value) in values:
                            self.txt_description.setText(values[str(self.value)])
                        # Если в базе нет описания для полученного значения
                        else:
                            self.txt_description.setText("Значение по умолчанию не задано")
                    # Если в базе нет значений, т.е fetchall() вернул []
                    else:
                        self.txt_description.setText("Значение по умолчанию не задано")
            # Если НЕ нашли значения для выбранного алгоритма
            else:
                self.cur.execute(
                        """
                        SELECT desc_list FROM descriptions WHERE id=?
                        """, (self.row_id, )
                    )
                values = self.cur.fetchall()
                # Если есть значения, заданные в базе
                print("VALUES:", values)
                if values:
                    values = json.loads(values[0][0])
                    # Если в базе есть описание для данного значения
                    if str(self.value) in values:
                        self.txt_description.setText(values[str(self.value)])
                    # Если в базе нет описания для полученного значения
                    else:
                        self.txt_description.setText("Значение по умолчанию не задано")
                # Если в базе нет значений, т.е fetchall() вернул []
                else:
                    self.txt_description.setText("Значение по умолчанию не задано")
        # Проверка на None не пройдена
        else:
            self.cur.execute(
                        """
                        SELECT desc_list FROM descriptions WHERE id=?
                        """, (self.row_id, )
                    )
            values = self.cur.fetchall()
            # Если есть значения, заданные в базе
            if values:
                values = json.loads(values[0][0])
                # Если в базе есть описание для данного значения
                if str(self.value) in values:
                    self.txt_description.setText(values[str(self.value)])
                # Если в базе нет описания для полученного значения
                else:
                    self.txt_description.setText("Значение по умолчанию не задано")
            # Если в базе нет значений, т.е fetchall() вернул []
            else:
                self.txt_description.setText("Значение по умолчанию не задано")



    def on_close(self):
        self.cur.close()
        self.con.close()
        self.close()


    def on_save(self):
        pass


    def setupUi(self):
        self.resize(659, 355)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.lbl_header = QtWidgets.QLabel()
        self.lbl_header.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.lbl_header)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.group_box_1 = QtWidgets.QGroupBox()
        self.verticalLayout.addWidget(self.group_box_1)
        self.v_layout = QtWidgets.QVBoxLayout()
        self.input_nametag = QtWidgets.QLineEdit(self.group_box_1)
        self.input_nametag.setMaxLength(50)
        self.v_layout.addWidget(self.input_nametag)
        self.group_box_1.setLayout(self.v_layout)
        self.verticalLayout.addWidget(self.group_box_1)

        self.group_box_2 = QtWidgets.QGroupBox()
        self.verticalLayout.addWidget(self.group_box_2)
        self.v_layout = QtWidgets.QVBoxLayout()
        self.input_value = QtWidgets.QLineEdit(self.group_box_2)
        self.v_layout.addWidget(self.input_value)
        self.group_box_2.setLayout(self.v_layout)
        self.verticalLayout.addWidget(self.group_box_2)

        self.group_box_3 = QtWidgets.QGroupBox()
        self.verticalLayout.addWidget(self.group_box_3)
        self.v_layout = QtWidgets.QVBoxLayout()
        self.txt_description = QtWidgets.QTextEdit(self.group_box_3)
        self.v_layout.addWidget(self.txt_description)
        self.group_box_3.setLayout(self.v_layout)
        self.verticalLayout.addWidget(self.group_box_3)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.btn_save = QtWidgets.QPushButton(self)
        self.horizontalLayout.addWidget(self.btn_save)
        self.horizontalLayout.addSpacerItem(QtWidgets.QSpacerItem(200, 0))
        self.btn_close = QtWidgets.QPushButton(self)
        self.horizontalLayout.addWidget(self.btn_close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("Расчёты")
        self.lbl_header.setText("Header")
        self.input_nametag.setPlaceholderText("Наименование")
        self.input_value.setPlaceholderText("Значение")
        self.txt_description.setPlaceholderText("Поле для описания")
        self.btn_save.setText("Сохранить")
        self.btn_close.setText("Закрыть")
        self.group_box_1.setTitle("Наименование")
        self.group_box_2.setTitle("Значение")
        self.group_box_3.setTitle("Описание")

