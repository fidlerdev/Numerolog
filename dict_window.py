# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from load_data import load_settings
from save_data import save_settings

class DictWidget(QtWidgets.QWidget):

    def __init__(self, mode="Создание"):
        QtWidgets.QWidget.__init__(self)
        self.setupUi()
        self.input_alpha_name.textEdited.connect(self.check_void)
        self.btn_save.clicked.connect(self.save)
        self.data = load_settings()
        self.saved = False
        if mode == "Изменение":
            pass


    def save(self):
        text = self.txt_alphabet.toPlainText().strip()
        alphabet = [[], [], [], [], [], [], [], [], []]
        if len(text.split()) > 1:
            msg = QtWidgets.QMessageBox.warning(self, "Внимание",
                        "Удалите пробелы между символами алфавита", defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            self.saved = True
            for ind, char in enumerate(text):
                alphabet[ind % 9].append(char)
            alpha = self.data["dictionary_list"]
            alpha[self.input_alpha_name.text()] = alphabet
            save_settings(
                    save_chosen_working_dir=self.data["save_chosen_working_dir"],
                    chosen_working_dir_path=self.data["chosen_working_dir_path"],
                    dictionary_list=alpha,
                    font=self.data["font"],
                    font_size=self.data["font_size"],
                    icons_set=self.data["icons_set"]
                    )
        self.close()

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

    def check_void(self):
        has_txt = True if self.input_alpha_name.text().strip() else False
        self.btn_save.setEnabled(has_txt)


    def setupUi(self):
        self.resize(346, 401)
        """
        Можно поставить фиксированный размер...
        """

        # self.setFixedSize()

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.input_alpha_name = QtWidgets.QLineEdit(self)
        self.input_alpha_name.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.input_alpha_name.customContextMenuRequested.connect(self.custom_context_menu)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.input_alpha_name.setFont(font)
        self.verticalLayout.addWidget(self.input_alpha_name)
        self.txt_alphabet = QtWidgets.QTextEdit(self)
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
        self.verticalLayout.addWidget(self.txt_alphabet)
        label = QtWidgets.QLabel("*Вводите буквы алфавита без пробела")
        self.verticalLayout.addWidget(label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_save = QtWidgets.QPushButton(self)
        self.btn_save.setEnabled(False)
        self.horizontalLayout.addWidget(self.btn_save)
        self.btn_close = QtWidgets.QPushButton(self)
        self.horizontalLayout.addWidget(self.btn_close)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Алфавит"))
        self.input_alpha_name.setPlaceholderText(_translate("self", "Введите название Алфавита"))
        self.btn_save.setText(_translate("self", "Сохранить"))
        self.btn_close.setText(_translate("self", "Закрыть"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    settings = DictWidget()
    settings.show()
    sys.exit(app.exec())