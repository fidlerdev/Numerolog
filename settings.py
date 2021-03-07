# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from os import sep, getcwd, path
from load_data import load_settings
from save_data import save_settings
from dialog_windows import CloseDialog
from desc_window import DescriptionWidget
from alpha_window import AlphaWindow
import sqlite3, io, os, shutil

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.closing = False
        self.data = load_settings()
        self.setupUi(self)
        self.load_alphabs()
        self.btn_save.clicked.connect(lambda: save_settings(
                    save_chosen_working_dir=self.check_save_wd.isChecked(),
                    chosen_working_dir_path=self.data["chosen_working_dir_path"], #Здесь не меняем ничего
                    dictionary_list=self.data["dictionary_list"],
                    font=self.fontComboBox.currentFont().family(),
                    font_size=self.spinBox_fontSize.value(),
                    icons_set=self.comboBox_icons.currentIndex() + 1))
        self.btn_close.clicked.connect(self.quit_action)
        self.btn_delete.clicked.connect(self.delete_item)
        self.input_alpha_name.textChanged.connect(self.on_text_changed)
        self.btn_save_dict.clicked.connect(self.save_dict)
        self.listWidget_dicts.itemClicked.connect(self.itemClicked)
        self.listWidget_dicts.itemDoubleClicked.connect(self.open_alpha_window)
        self.btn_new_dict.clicked.connect(self.new_dict_clicked)
        self.btn_descriptions.clicked.connect(self.open_descriptions)
        self.btn_import_desc.clicked.connect(self.import_desc)
        self.btn_export_desc.clicked.connect(self.export_desc)

    def import_desc(self):
        '''
        Импорт базы данных с описаниями в корневую директорию проекта
        desc.db – обязательное имя файла с базой данных
        '''
        db_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Импортировать базу с описаниями')[0]
        # Если отменили выбор
        if not db_file:
            return
        os.remove('desc.db')
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute('begin immediate')
        shutil.copyfile(db_file, '.' + os.sep + 'desc.db')
        print('Импорт осуществлен успешно')
        conn.rollback()

    def export_desc(self):
        '''
        desc.db – обязательное имя базы данных
        '''
        backup_db = QtWidgets.QFileDialog.getSaveFileName(self, 'Экспортировать базу с описаниями')[0]
        # Если отменили выбор
        if not backup_db:
            return
        backup_db += '.db'
        conn = sqlite3.connect('desc.db')
        cur = conn.cursor()
        # Lock database before making a backup
        cur.execute('begin immediate')
        shutil.copyfile('desc.db', backup_db)
        print('Экспорт осуществлен успешно')
        print('Сохранено как', backup_db)
        conn.rollback()

    def open_alpha_window(self, item):
        self.alpha_name = item.data(QtCore.Qt.UserRole)
        self.alpha_window = AlphaWindow(alphabet=self.alpha_name)
        self.alpha_window.show()
        self.alpha_window.saved.connect(self.alpha_window_saved)
    
    def alpha_window_saved(self, alphabet):
        print(alphabet)
        self.data["dictionary_list"][self.alpha_name] = alphabet
        self.btn_save.click()
        self.load_alphabs()


    def load_alphabs(self):
        self.listWidget_dicts.clear()
        for alphab in self.data["dictionary_list"]:
            string = ""
            if self.data["dictionary_list"][alphab][-1]:
                string = "\t———\tнастроен"
            else:
                string = "\t———\tНЕ настроен"
            item = QtWidgets.QListWidgetItem()
            item.setData(QtCore.Qt.UserRole, alphab)
            item.setText(alphab + string)
            self.listWidget_dicts.addItem(item)
        # self.listWidget_dicts.addItems(self.data["dictionary_list"])

    def open_descriptions(self):
        # Проверка на наличие базы данных с описаниями
        self.check_db()
        self.description_widget = DescriptionWidget()
        self.description_widget.show()

    def check_db(self):
        if path.exists("desc.db"):
            print("База с описаниями найдена")
        else:
            with open("desc.db", "w"):
                print("База с описаниями создана")
            con = sqlite3.connect("desc.db")
            cur = con.cursor()
            cur.execute(
            """
            CREATE TABLE descriptions (
                id INTEGER UNIQUE,
                desc_list TEXT
                );
            """
            )
            con.commit()
            cur.close()
            con.close()


    def delete_item(self):
        selected_item = self.listWidget_dicts.item(self.selected_row)
        name = selected_item.data(QtCore.Qt.UserRole)
        self.listWidget_dicts.takeItem(self.selected_row)
        del self.data["dictionary_list"][name]
        self.btn_delete.setEnabled(False)
        self.input_alpha_name.setText("")
        self.txt_alphabet.setText("")
        self.listWidget_dicts.setCurrentRow(-1)
        self.listWidget_dicts.repaint()


    def new_dict_clicked(self):
        self.txt_alphabet.clear()
        self.input_alpha_name.clear()

    def itemClicked(self, item):
        self.selected_row = self.listWidget_dicts.row(item)
        self.btn_delete.setEnabled(True)
        name = item.data(QtCore.Qt.UserRole)
        self.input_alpha_name.setText(name)
        alpha = self.data["dictionary_list"][name][:-1]
        # print(alpha)
        count = 0

        # Получаем количество букв в алфавите
        for group in alpha:
            count += len(group)
        
        alphabet = ", ".join([str(i) for i in range(count)]) + ", "
        # print(alphabet)
        for index_of_group, group in enumerate(alpha):
            for index_of_el, el in enumerate(group):
                alphabet = alphabet.replace(str(index_of_group + index_of_el * 9) + ", ", el[0], 1)
                # print(alphabet)
                # print(str(index_of_group + index_of_el * 9))

        if count > 0:
            self.txt_alphabet.setText(alphabet)
        else:
            self.txt_alphabet.setText("")


    def on_text_changed(self, text):
        if text.strip():
            self.btn_save_dict.setEnabled(True)
        else:
            self.btn_save_dict.setEnabled(False)

    def save_dict(self):
        text = self.txt_alphabet.toPlainText().strip()
        alphabet = [[], [], [], [], [], [], [], [], []]
        if len(text.split()) > 1:
            QtWidgets.QMessageBox.warning(self, "Внимание",
                        "Удалите пробелы между символами алфавита", defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            if len(self.listWidget_dicts.findItems(self.input_alpha_name.text(), QtCore.Qt.MatchExactly)) > 0:
                QtWidgets.QMessageBox.warning(self, "Внимание",
                        "Алфавит с таким именем уже существует", defaultButton=QtWidgets.QMessageBox.Ok)
                

            else:
                for ind, char in enumerate(text):
                    alphabet[ind % 9].append([char, 0])
                # По умолчанию алфавит не настроен
                alphabet.append(False)
                self.data["dictionary_list"][self.input_alpha_name.text()] = alphabet
                self.load_alphabs()
                # self.listWidget_dicts.addItem(self.input_alpha_name.text())
                self.input_alpha_name.clear()
                self.txt_alphabet.clear()
                self.btn_save.click()


    def on_close(self):
        dialog = CloseDialog(self)
        # Переопределяем надпись в модальном окне
        dialog.label.setText("Вы действительно хотите закрыть окно?\nВсе несохраненные данные будут утеряны")

        return dialog.exec()

    def closeEvent(self, event):
        if not self.closing:
            result = self.on_close()
            if result == QtWidgets.QMessageBox.Accepted:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def quit_action(self):
        result = self.on_close()
        self.closing = True
        if result == QtWidgets.QMessageBox.Accepted:
            self.close()
        else: self.closing = False



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

        path_icons = getcwd() + sep + "resources" + sep + "icons" + sep

        Form.resize(800, 700)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.btn_descriptions = QtWidgets.QPushButton(self.groupBox)
        self.btn_import_desc = QtWidgets.QPushButton(self.groupBox)
        self.btn_export_desc = QtWidgets.QPushButton(self.groupBox)
        self.verticalLayout_4.addWidget(self.btn_descriptions)
        self.verticalLayout_4.addWidget(self.btn_import_desc)
        self.verticalLayout_4.addWidget(self.btn_export_desc)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.verticalLayout_4.addWidget(self.label)
        self.listWidget_dicts = QtWidgets.QListWidget(self.groupBox)
        self.verticalLayout_4.addWidget(self.listWidget_dicts)
        self.label_hint_alpha = QtWidgets.QLabel(self.groupBox)
        self.verticalLayout_4.addWidget(self.label_hint_alpha)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 10, -1, -1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_delete = QtWidgets.QPushButton(self.groupBox)
        self.btn_delete.setEnabled(False)
        self.horizontalLayout.addWidget(self.btn_delete)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.check_save_wd = QtWidgets.QCheckBox(self.groupBox_3)
        self.verticalLayout_3.addWidget(self.check_save_wd)
        self.gridLayout_2.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(40)
        sizePolicy.setVerticalStretch(40)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(40, 40))
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_2)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.fontComboBox = QtWidgets.QFontComboBox(self.groupBox_2)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fontComboBox)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.spinBox_fontSize = QtWidgets.QSpinBox(self.groupBox_2)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox_fontSize)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        lbl_hint = QtWidgets.QLabel("*Необходим перезапуск")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, lbl_hint)
        self.comboBox_icons = QtWidgets.QComboBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_icons.sizePolicy().hasHeightForWidth())
        self.comboBox_icons.setSizePolicy(sizePolicy)
        self.comboBox_icons.setBaseSize(QtCore.QSize(40, 40))
        self.comboBox_icons.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox_icons.setIconSize(QtCore.QSize(40, 40))

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(path_icons + "1/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox_icons.addItem(icon1, "")
        self.comboBox_icons.setItemText(0, "Windows 10")


        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(path_icons + "2/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox_icons.addItem(icon2, "")
        self.comboBox_icons.setItemText(1, "Pastel")


        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(path_icons + "3/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox_icons.addItem(icon3, "")
        self.comboBox_icons.setItemText(2, "Office")


        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(path_icons + "4/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox_icons.addItem(icon4, "")
        self.comboBox_icons.setItemText(3, "Dotted")


        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_icons)
        self.gridLayout_2.addWidget(self.groupBox_2, 0, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.input_alpha_name = QtWidgets.QLineEdit(self.groupBox_4)
        self.input_alpha_name.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.input_alpha_name.customContextMenuRequested.connect(self.custom_context_menu)

        font = QtGui.QFont()
        font.setPointSize(13)
        self.input_alpha_name.setFont(font)
        self.verticalLayout_5.addWidget(self.input_alpha_name)
        self.txt_alphabet = QtWidgets.QTextEdit(self.groupBox_4)
        self.txt_alphabet.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.txt_alphabet.customContextMenuRequested.connect(self.custom_context_menu)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.txt_alphabet.setFont(font)
        self.txt_alphabet.setFrameShadow(QtWidgets.QFrame.Raised)
        self.txt_alphabet.setLineWidth(1)
        self.txt_alphabet.setDocumentTitle("")
        self.txt_alphabet.setLineWrapColumnOrWidth(0)
        self.verticalLayout_5.addWidget(self.txt_alphabet)

        label = QtWidgets.QLabel("*Вводите буквы алфавита без пробела")
        self.verticalLayout_5.addWidget(label)

        horizontalLayout = QtWidgets.QHBoxLayout()

        self.btn_new_dict = QtWidgets.QPushButton(self.groupBox_4)
        horizontalLayout.addWidget(self.btn_new_dict)

        self.btn_save_dict = QtWidgets.QPushButton(self.groupBox_4)
        self.btn_save_dict.setEnabled(False)
        horizontalLayout.addWidget(self.btn_save_dict)

        self.verticalLayout_5.addLayout(horizontalLayout)
        self.gridLayout_2.addWidget(self.groupBox_4, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.btn_save = QtWidgets.QPushButton(Form)
        self.horizontalLayout_2.addWidget(self.btn_save)
        self.btn_close = QtWidgets.QPushButton(Form)
        self.horizontalLayout_2.addWidget(self.btn_close)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        # Подгружаем пользовательские значения в настройки
        self.check_save_wd.setChecked(self.data["save_chosen_working_dir"])
        self.fontComboBox.setCurrentFont(QtGui.QFont(self.data["font"]))
        self.spinBox_fontSize.setValue(self.data["font_size"])
        self.comboBox_icons.setCurrentIndex(self.data["icons_set"] - 1)
            

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Настройки"))
        self.groupBox.setTitle(_translate("Form", "Расчёты"))
        self.label.setText(_translate("Form", "Список алфавитов:"))
        self.btn_descriptions.setText("База с описаниями")
        self.btn_import_desc.setText("Импорт базы")
        self.btn_export_desc.setText("Экспорт базы")
        self.btn_delete.setText(_translate("Form", "Удалить"))
        self.groupBox_3.setTitle(_translate("Form", "Основные"))
        self.check_save_wd.setText(_translate("Form", "Запоминать выбранную рабочую область"))
        self.groupBox_2.setTitle(_translate("Form", "Внешний вид"))
        self.label_2.setText(_translate("Form", "Шрифт:"))
        self.label_3.setText(_translate("Form", "Размер шрифта:"))
        self.label_4.setText(_translate("Form", "Набор иконок:"))
        self.btn_save.setText(_translate("Form", "Сохранить"))
        self.btn_close.setText(_translate("Form", "Закрыть"))
        self.input_alpha_name.setPlaceholderText(_translate("self", "Введите название Алфавита"))
        self.btn_save_dict.setText(_translate("self", "Сохранить Алфавит"))
        self.groupBox_4.setTitle(_translate("self", "Алфавит"))
        self.btn_new_dict.setText(_translate("self", "Новый Алфавит"))
        hint = "Если алфавит не был настроен, алгоритмы 11-13\nне будут доступны\n\n" + \
            "*Дважды нажмите на имя алфавита, чтобы настроить..."

        self.label_hint_alpha.setText(_translate("self", hint))
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    settings = SettingsWidget()
    settings.show()
    sys.exit(app.exec())