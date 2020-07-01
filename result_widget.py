# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
import sqlite3, json
from load_data import load
from load_resources import get_icons
from save_data import save
from image_gen import TableImage

class ResultWidget(QtWidgets.QWidget):

    def __init__(self, path, header_text, value, row_id, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.icons = get_icons()
        self.row_id = row_id
        self.value = value
        self.setupUi()
        self.header_text = header_text
        self.path=path

        self.con = sqlite3.connect("desc.db")
        self.cur = self.con.cursor()

        
        self.lbl_header.setText(self.header_text)

        try:
            self.load_desc()
            self.input_value.setText(str(self.value))
            self.txt_description.textChanged.connect(self.desc_changed)
            self.input_value.textChanged.connect(self.value_changed)
            self.input_value.setReadOnly(True)
        except AttributeError as err:
            print(err)


        self.btn_close.clicked.connect(self.on_close)
        if self.row_id != 18:
            self.btn_save.clicked.connect(self.on_save)
            self.btn_print.clicked.connect(self.print_out)

    def print_out(self):
        
        self.txt_print_out = QtWidgets.QTextEdit()
        if self.row_id == 18:
            print_out_text: str = "Наименование: {}\nЗначение:".format(
                self.input_nametag.text()
            )
        else:
            print_out_text: str = "Наименование: {}\nЗначение: {}\n\nОписание:\n{}".format(
                self.input_nametag.text(),
                self.value,
                self.txt_description.toPlainText()
            )
        
        self.txt_print_out.setText(print_out_text)
        # printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        printer = QtPrintSupport.QPrinter()
        '''
        if self.row_id == 18:
            painter = QtGui.QPainter()
            painter.begin(printer)
            print(printer.width(), printer.height())
            image = self.table_img.return_image()
            painter.drawPixmap(printer.width() / 2, printer.height() / 2, QtGui.QPixmap.fromImage(image))
        '''
        previewDialog = QtPrintSupport.QPrintPreviewDialog(printer, self)
        previewDialog.setWindowTitle("Предпросмотр")
        previewDialog.paintRequested.connect(self.printPreview)
        previewDialog.exec()


    def printPreview(self, printer):
        self.txt_print_out.print(printer)



    # Debugging
    def value_changed(self, value):
        try:
            self.value = int(value)
            self.btn_save.setEnabled(True)
        except ValueError as err:
            print(err)
            self.btn_save.setEnabled(False)

    def desc_changed(self):
        self.btn_save.setEnabled(True)
        self.btn_save.repaint()

    def load_desc(self):
        custom_desc_list = load(path=self.path)["desc_list"]
        # Проверка на значение None
        if custom_desc_list:
            custom_desc_list = [x[1] for x in custom_desc_list if x[0] == self.row_id]
            # Если нашли значения для выбранного алгоритма
            if custom_desc_list:
                custom_desc_list = custom_desc_list[0]
                # Если для значения установлено уникальное описание
                if str(self.value) in custom_desc_list:
                    txt = custom_desc_list[str(self.value)]
                    self.txt_description.setText(txt)
                # В противном случае ищем описания заданные по умолчанию для данного значения в БАЗЕ
                else:
                    self.not_found_case()
            # Если НЕ нашли значения для выбранного алгоритма
            else:
                self.not_found_case()
        # Проверка на None не пройдена
        else:
            self.not_found_case()

    def not_found_case(self):
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
        self.btn_save.setEnabled(False)
        self.btn_save.repaint()
        usr_desc = self.txt_description.toPlainText()
        descriptions = load(self.path)["desc_list"]
        # Проверка на None
        if descriptions:
            dictionary = [(x[1], ind) for ind, x in enumerate(descriptions) if x[0] == self.row_id]
            # Если нашли массив значений для выбранного алгоритма
            if dictionary:
                dictionary = dictionary[0]
                descriptions[dictionary[1]][1][str(self.value)] = usr_desc
                self.save_desc(descriptions)
            # Если не нашли массив значений для выбранного алгоритма    
            else:
                descriptions.append([self.row_id, {self.value: usr_desc}])
                self.save_desc(descriptions)
        else:   
            self.save_desc([[self.row_id, {self.value: usr_desc}]])
            
            

    
    def save_desc(self, desc_list):
        data = load(self.path)
        save(path=self.path,

            surname=data["surname"],
            name=data["name"],
            middle_name=data["middle_name"],
            bonus_list=data["bonus_list"],
            date_of_birth=data["date_of_birth"],
            time_of_birth=data["time_of_birth"],
            moon_birth=data["moon_birth"],
            delete=data["delete"],
            dictionary=data["dictionary"],
            desc_list=desc_list
        )
        




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
        if self.row_id != 18:
            self.input_value = QtWidgets.QLineEdit(self.group_box_2)
            self.v_layout.addWidget(self.input_value)
        else:
            self.table_img = TableImage(
                values=self.value,
                size=(270, 270),
                ttf='./resources/arial.ttf',
                i_size=18,
                n_size=35,
                fill='#000000',
                alert_fill='#ff4d00'
            )
            self.table_img.prepare_image(line_w=2)
            self.lbl_image = QtWidgets.QLabel()
            image = self.table_img.return_image()
            self.lbl_image.setPixmap(QtGui.QPixmap.fromImage(image))

            self.v_layout.addWidget(self.lbl_image)

        self.group_box_2.setLayout(self.v_layout)
        self.verticalLayout.addWidget(self.group_box_2)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        if self.row_id != 18:
            self.group_box_3 = QtWidgets.QGroupBox()
            self.verticalLayout.addWidget(self.group_box_3)

            self.v_layout = QtWidgets.QVBoxLayout()

            self.txt_description = QtWidgets.QTextEdit(self.group_box_3)

            self.v_layout.addWidget(self.txt_description)

            self.group_box_3.setLayout(self.v_layout)
            self.verticalLayout.addWidget(self.group_box_3)
            self.btn_print = QtWidgets.QPushButton(self)
            self.btn_print.setIcon(self.icons['print'])
            self.btn_save = QtWidgets.QPushButton(self)
            self.horizontalLayout.addWidget(self.btn_print)
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
        self.btn_close.setText("Закрыть")
        self.group_box_1.setTitle("Наименование")
        self.group_box_2.setTitle("Значение")
        try:
            self.btn_save.setText("Сохранить")
            self.group_box_3.setTitle("Описание")
            self.input_value.setPlaceholderText("Значение")
            self.txt_description.setPlaceholderText("Поле для описания")
        except AttributeError as err:
            print(err)
        

