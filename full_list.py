# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from os import walk, sep
from load_resources import get_icons
from calculate_window import CalculateWidget

class FullListWidget(QtWidgets.QWidget):

    def __init__(self, path, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.path = path
        self.icons = get_icons()
        self.setupUi()
        self.listWidget.itemDoubleClicked.connect(self.on_item_clicked)
        self.input_search_field.textChanged.connect(self.search)

    def search(self, text):
        self.hide_all()
        for row in range(self.listWidget.count()):
            item = self.listWidget.item(row)
            if text.lower() in item.text().lower():
                item.setHidden(False)

    def hide_all(self):
        for row in range(self.listWidget.count()):
            self.listWidget.item(row).setHidden(True)

    def on_item_clicked(self, item):
        calc = CalculateWidget(None, item.data(QtCore.Qt.UserRole))
        calc.show()

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

    def setupUi(self):
        self.resize(494, 604)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.input_search_field = QtWidgets.QLineEdit(self)
        self.input_search_field.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.input_search_field.customContextMenuRequested.connect(self.custom_context_menu)
        self.verticalLayout.addWidget(self.input_search_field)
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.verticalLayout.addWidget(self.listWidget)
        self.fill_list()
        self.retranslateUi()

    def fill_list(self):
        for dir_path in walk(self.path):
            for name in dir_path[2]:
                if not name.startswith("._"):
                    user = QtWidgets.QListWidgetItem(name[:-5])
                    user.setData(QtCore.Qt.UserRole, dir_path[0] + sep + name)
                    user.setIcon(self.icons["user"])
                    self.listWidget.addItem(user)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle("Полный список")
        self.input_search_field.setPlaceholderText("Введите название файла для поиска...")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = FullListWidget("C:\\Users\\fidler\\Desktop\\Контрагенты")
    window.show()
    sys.exit(app.exec())