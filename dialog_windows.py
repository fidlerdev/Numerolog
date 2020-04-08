# dialog_windos.py

# -*- coding: utf-8 -*-

# Класс, в котором определены все необходимые диалоговые окна

from PyQt5 import QtWidgets, QtCore, QtGui
from os import sep

# Локальные константы длины и высоты 
# Переменные с символом "_" не будут импортироваться
_WIDTH = 300
_HEIGHT = 100

class CloseDialog(QtWidgets.QDialog):
    """
    В конструктор передаётся родительское окно
    """
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint |QtCore.Qt.WindowCloseButtonHint)
        self.setup_Ui()
        # Слот accept() закрывает модальное окно и устанавливает код возврата равным значению
        # атрибута Accepted (1) класса QDialog
        self.btnYES.clicked.connect(self.accept)
        # Слот reject() закрывает модальное окно и устанавливает код возврата равным значению
        # атрибута Rejected (0) класса QDialog
        self.btnNO.clicked.connect(self.reject)
    
    # Расстановка элементов
    def setup_Ui(self):

        # Устанавливаем фиксированный размер
        # self.setFixedSize(_WIDTH, _HEIGHT)

        # Подгоняем размер окна под содержимое
        self.adjustSize()
        self.setWindowTitle("Выход")

        # Создаем компоненты диалогового окна
        self.label = QtWidgets.QLabel("Вы точно хотите выйти?")
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.btnYES = QtWidgets.QPushButton("Да")
        self.btnNO = QtWidgets.QPushButton("Нет")

        # Grid Layout
        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.label, 0, 0, 1, 2)
        self.grid.addWidget(self.btnYES, 1, 0)
        self.grid.addWidget(self.btnNO, 1, 1)
        self.setLayout(self.grid)

class CreateDialog(QtWidgets.QDialog):

    def __init__(self, parent, type=""):
        QtWidgets.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(_WIDTH, _HEIGHT + 50)
        self.setWindowTitle(" ")
        label = QtWidgets.QLabel("Введите название " + type)
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setPlaceholderText("Название " + type)
        self.lineEdit.textChanged.connect(self.check_void)
        self.confirmBtn = QtWidgets.QPushButton("ОК")
        self.confirmBtn.setEnabled(False)
        self.confirmBtn.clicked.connect(self.accept)
        cancelBtn = QtWidgets.QPushButton("Назад")
        cancelBtn.clicked.connect(self.reject)

        # Layout
        grid = QtWidgets.QGridLayout()
        grid.addWidget(label, 0, 0, 1, 3, alignment=QtCore.Qt.AlignHCenter)
        grid.addWidget(self.lineEdit, 1, 0, 1, 3)
        grid.addWidget(self.confirmBtn, 2, 0, 1, 2)
        grid.addWidget(cancelBtn, 2, 2, 1, 1)

        self.setLayout(grid)
    
    def check_void(self):
        if self.lineEdit.text().strip() != "":
            self.confirmBtn.setEnabled(True)
        else:
            self.confirmBtn.setEnabled(False)
            
    def getName(self):
        path = self.lineEdit.text()
        return path

class CreateDialog_ext(QtWidgets.QDialog):

    def __init__(self, parent, path, type=""):
        QtWidgets.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowCloseButtonHint)
        self.type = type
        self.path = path
        print("PAAATH: ",self.path)
        self.setupUi()
        self.input_name.setFocus()
        self.index = None
        self.treeView.clicked.connect(self.dir_clicked)
        self.btn_create.clicked.connect(self.accept)
        self.btn_close.clicked.connect(self.reject)

    def dir_clicked(self, index):
        self.index = index
        # self.btn_create.setEnabled(True)

    def btn_create_clicked(self):
        self.accept()
    
    def get_path(self):
        if self.index:
            return self.model.fileInfo(self.index).path() + sep + self.model.fileInfo(self.index).fileName() + sep + self.input_name.text()
        else:
            return self.path + sep + self.input_name.text()


    def setupUi(self):
        self.resize(572, 316)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(self.path)
        self.model.setReadOnly(True)
        self.model.setFilter(QtCore.QDir.Dirs | QtCore.QDir.AllDirs | QtCore.QDir.NoDotDot) # QtCore.QDir.NoDotAndDotDot
        self.treeView = QtWidgets.QTreeView(self)
        self.treeView.setModel(self.model)
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)
        self.treeView.setHeaderHidden(True)
        self.treeView.setRootIndex(self.model.index(self.path))
        self.treeView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.verticalLayout.addWidget(self.treeView)
        self.input_name = QtWidgets.QLineEdit()
        if self.type == "папки":
            self.input_name.setPlaceholderText("Название папки")
        elif self.type == "файла":
            self.input_name.setPlaceholderText("Имя клиента")
        self.verticalLayout.addWidget(self.input_name)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_create = QtWidgets.QPushButton(self)
        # self.btn_create.setEnabled(False)
        self.horizontalLayout.addWidget(self.btn_create)
        self.btn_close = QtWidgets.QPushButton(self)
        self.horizontalLayout.addWidget(self.btn_close)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("dialog", "Выберите расположение " + self.type))
        self.btn_create.setText(_translate("dialog", "Создать"))
        self.btn_close.setText(_translate("dialog", "Отмена"))

    def check_void(self):
        if self.lineEdit.text().strip() != "":
            self.confirmBtn.setEnabled(True)
        else:
            self.confirmBtn.setEnabled(False)
            
    def getName(self):
        path = self.lineEdit.text()
        return path
    



# Тестирование модуля
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    self = CreateDialog(None, "папки")
    d = CloseDialog(None)
    d.show()
    self.show()
    sys.exit(app.exec())