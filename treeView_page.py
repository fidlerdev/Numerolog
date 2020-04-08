# treeView_window.py

# -*- coding: utf-8 -*-

# Модуль, описывающий страницу с иерархией каталогов и файлов
# Именно страницу, т.к. отображение всех экземпляров проводится в пределах одного окна, точнее контейнера


from PyQt5 import QtWidgets, QtCore, QtGui
from user import UserWidget
from dialog_windows import CreateDialog, CloseDialog
from calculate_window import CalculateWidget
from full_list import FullListWidget
import os

class TreeViewWindow(QtWidgets.QTreeView):
    def __init__(self, path, icons, tool_bar, parent=None):
        QtWidgets.QTreeView.__init__(self, parent)

        self.setAnimated(True)
        self.setIndentation(35)

        # itemDelegate = MyItemDelegate(self)
        # self.setItemDelegate(itemDelegate)


        self.tool_bar = tool_bar
        self.edit_user_action = self.tool_bar.actions()[2]
        self.sort_alpha_action = self.tool_bar.actions()[3]
        self.sort_cr_action = self.tool_bar.actions()[4]
        self.open_full_list = self.tool_bar.actions()[5]

        # Сортировка по умолчанию —— А-Я
        self.sortings = {   
                        "alpha":         False,  # True: А-Я             False: Я-А
                        "creation":      True, # True: Новое-Старое    False: Старое-Новое 
                        }


        self.path = path
        self.icons = icons

        # Создаем модель
        self.model = QtWidgets.QFileSystemModel()

        # Передаем выбранную директорию в модель
        self.model.setRootPath(self.path)
        self.model.setReadOnly(False)

        self.model.setFilter(QtCore.QDir.Files | QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)
        self.model.setNameFilters(["*.json"])

        # Drag & Drop
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

        iconProvider = IconProvider(self.icons)

        self.model.setIconProvider(iconProvider)

        self.setIconSize(QtCore.QSize(32, 32))

        self.setModel(self.model)
        self.hideColumn(1)
        self.hideColumn(2)
        self.setHeaderHidden(True)
        self.setRootIndex(self.model.index(path))
        self.sortByColumn(3, QtCore.Qt.DescendingOrder)

        self.setTabKeyNavigation(True)

        # Добавление контекстного меню 
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_menu)

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.doubleClicked.connect(self.open_calculation)    
        self.clicked.connect(self.single_click)

        self.edit_user_action.triggered.connect(lambda: self.edit_file(path=self.model.fileInfo(self.cur_file_clicked).dir().path() + os.sep + self.cur_file_clicked.data(), operation="Редактирование данных"))

        self.sort_alpha_action.triggered.connect(lambda: self.sort(action="alphabetic"))

        self.sort_cr_action.triggered.connect(lambda: self.sort(action="creation"))

        # Какой-то костыль, без него окно с полным списком сразу закрывается :(
        self.open_full_list.triggered.connect(self.open_full_list_action)

    def open_full_list_action(self):
        self.full_list = FullListWidget(path=self.path)
        self.full_list.setWindowModality(QtCore.Qt.ApplicationModal)
        self.full_list.show()

    def sort(self, action):
        if action == "alphabetic":
            self.sortings["alpha"] = not self.sortings["alpha"]
            self.sortings["creation"] = False
            if self.sortings["alpha"]:
                self.sort_alpha_action.setIcon(self.icons["arrow_up"])
                self.sort_alpha_action.setText("Сортировать: А-Я")
                self.sortByColumn(0, QtCore.Qt.AscendingOrder)
            else:
                self.sort_alpha_action.setIcon(self.icons["arrow_down"])
                self.sort_alpha_action.setText("Сортировать: Я-А")
                self.sortByColumn(0, QtCore.Qt.DescendingOrder)

        if action == "creation":
            self.sortings["creation"] = not self.sortings["creation"]
            self.sortings["alpha"] = False
            if self.sortings["creation"]:
                self.sort_cr_action.setIcon(self.icons["arrow_up"])
                self.sortByColumn(3, QtCore.Qt.DescendingOrder)
            else:
                self.sort_cr_action.setIcon(self.icons["arrow_down"])
                self.sortByColumn(3, QtCore.Qt.AscendingOrder)

    def single_click(self, index):
        # Если объект — папка —> открываем или закрываем список дочерних файлов
        if self.model.fileInfo(index).isDir():
            self.edit_user_action.setEnabled(False)
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)
        elif self.model.fileInfo(index).suffix() == "json":
            self.edit_user_action.setEnabled(True)
            self.cur_file_clicked = index
        else:
            self.edit_user_action.setEnabled(False)

    # Drag & Drop functions ——— https://stackoverflow.com/questions/48121711/drag-and-drop-within-pyqt5-treeview
    def dragEnterEvent(self, event):
        m = event.mimeData()
        if m.hasUrls():
            for url in m.urls():
                if url.isLocalFile():
                    event.accept()
                    return
        event.ignore()

    def dropEvent(self, event):
        self.edit_user_action.setEnabled(False)
        if event.source():
            QtWidgets.QTreeView.dropEvent(self, event)
        else:
            ix = self.indexAt(event.pos())
            if not self.model().isDir(ix):
                ix = ix.parent()
            pathDir = self.model().filePath(ix)
            m = event.mimeData()
            if m.hasUrls():
                urlLocals = [url for url in m.urls() if url.isLocalFile()]
                accepted = False
                for urlLocal in urlLocals:
                    path = urlLocal.toLocalFile()
                    info = QtCore.QFileInfo(path)
                    n_path = QtCore.QDir(pathDir).filePath(info.fileName())
                    o_path = info.absoluteFilePath()
                    if n_path == o_path:
                        continue
                    if info.isDir():
                        QtCore.QDir().rename(o_path, n_path)
                    else:
                        qfile = QtCore.QFile(o_path)
                        if QtCore.QFile(n_path).exists():
                            n_path += "(copy)" 
                        qfile.rename(n_path)
                    accepted = True
                if accepted:
                    event.acceptProposedAction()


    def open_calculation(self, index):
        # Если объект — файл —> открываем страницу с рассчетами
        if index.data().endswith(".json"):
            path = self.model.fileInfo(index).dir().path() + os.sep + index.data()
            self.calculation_widget = CalculateWidget(parent=None, path=path)
            self.calculation_widget.show()


    def open_menu(self, position):
        index = self.indexAt(position)

        if not index.isValid():
            return
        if self.model.fileInfo(index).suffix() != "json" and not self.model.fileInfo(index).isDir(): 
            print("WARNING: WRONG FILE FORMAT ({})".format(self.model.fileInfo(index).suffix()))
            return

        context_menu = QtWidgets.QMenu()

        if index.data().endswith(".json"):
            edit_file = QtWidgets.QAction(self.icons["edit_file"], "Редактировать", context_menu)
            calculate_file = QtWidgets.QAction(self.icons["calculate"], "Расчёты", context_menu)
            rename_file = QtWidgets.QAction(self.icons["rename"], "Переименовать клиента", context_menu)
            delete_file = QtWidgets.QAction(self.icons["delete"], "Удалить файл", context_menu)

            ###########################################
            print("———", os.path.abspath(index.data()))
            print("———", self.rootIndex().data())
            print("———", self.indexAbove(index).data())
            ###########################################

            context_menu.addAction(edit_file)
            edit_file.triggered.connect(lambda: self.edit_file(path=self.model.fileInfo(index).dir().path() + os.sep + index.data(), operation="Редактирование данных"))

            context_menu.addAction(calculate_file)
            calculate_file.triggered.connect(lambda: self.open_calculation(index=index))

            context_menu.addSeparator()

            context_menu.addAction(rename_file)
            rename_file.triggered.connect(lambda: self.rename(type=("клиента", ".json"), index=index))

            context_menu.addAction(delete_file)
            delete_file.triggered.connect(lambda: self.delete(index=index))

        # Костыли наше всё
        elif self.model.fileInfo(index).isDir:
            add_folder = QtWidgets.QAction(self.icons["add_folder"], "Создать папку", context_menu)
            add_file = QtWidgets.QAction(self.icons["add_user"], "Создать клиента", context_menu)
            rename_folder = QtWidgets.QAction(self.icons["rename"], "Переименовать папку", context_menu)
            delete_folder = QtWidgets.QAction(self.icons["delete"], "Удалить папку", context_menu)

            context_menu.addAction(add_folder)
            add_folder.triggered.connect(lambda: self.add(type="папки", func=self.add_folder, index=index))

            context_menu.addAction(add_file)
            add_file.triggered.connect(lambda: self.add(type="клиента", func=self.add_file, index=index))

            context_menu.addSeparator()

            context_menu.addAction(rename_folder)
            rename_folder.triggered.connect(lambda: self.rename(type=("папки", ""), index=index))

            context_menu.addAction(delete_folder)
            delete_folder.triggered.connect(lambda: self.delete(index=index))
            
        context_menu.exec(QtGui.QCursor.pos())


    def edit_file(self, path, operation):
        create_widget = UserWidget(operation=operation, user_name=self.path.split(os.sep)[-1], path=path)
        create_widget.setWindowModality(QtCore.Qt.ApplicationModal)
        create_widget.show()
    
    def add(self, type, func, index):
        dialog = CreateDialog(self, type)
        result = dialog.exec()
        if result == QtWidgets.QMessageBox.Accepted:
            path = self.model.fileInfo(index).dir().path() + os.sep + index.data() + os.sep + dialog.lineEdit.text()
            print("———", path)
            func(path)
            
        

    def add_folder(self, path):
        try:
            os.mkdir(path)
            print("———", "Папка успешно создана")
        except FileExistsError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Папка {} уже существует".format(path), defaultButton=QtWidgets.QMessageBox.Ok)

    def add_file(self, path):
        path = path + ".json"
        print("Path {} exists: {}".format(path, os.path.exists(path)))
        if os.path.exists(path):

            dialog = CloseDialog(self)
            dialog.setWindowTitle("Клиент уже существует")
            dialog.label.setText("Вы хотите отредактировать существующие данные?")
            result = dialog.exec()

            if result == QtWidgets.QMessageBox.Accepted:
                self.edit_file(operation="Редактирование данных", path=path)
        else:
            self.edit_file(operation="Создание", path=path)

    def rename(self, type, index):
        dialog = CreateDialog(self, type=type[0])
        result = dialog.exec()
        if result == QtWidgets.QMessageBox.Accepted:
            self.model.setData(index, dialog.getName() + type[1])



    def delete(self, index):
        path = self.model.fileInfo(index).dir().path() + os.sep + index.data()
        if self.model.fileInfo(index).isDir():
            if not os.listdir(path):
                dialog = CloseDialog(self)
                dialog.setWindowTitle("Удалить")
                dialog.label.setText("Вы точно хотите удалить папку?")
                result = dialog.exec()
                if result == QtWidgets.QDialog.Accepted:
                    self.model.remove(index)
            else:
                dialog = QtWidgets.QMessageBox.warning(self, "Предупреждение",
                                "Невозможно удалить папку, так как в ней находятся другие файлы и/или папки",
                                defaultButton = QtWidgets.QMessageBox.Ok)
        elif self.model.fileInfo(index).isFile():
            from load_data import load
            data = load(path)
            if data["delete"]:
                dialog = CloseDialog(self)
                dialog.setWindowTitle("Удалить")
                dialog.label.setText("Вы точно хотите удалить клиента?")
                result = dialog.exec()
                if result == QtWidgets.QDialog.Accepted:
                    self.model.remove(index)
            else:
                dialog = QtWidgets.QMessageBox.warning(self, "Предупреждение",
                                "Чтобы удалить клиента, необходимо изменить значение \"Нельзя удалить клиента\"",
                                defaultButton = QtWidgets.QMessageBox.Ok)


# Класс иконок для элементов списка tree_view
class IconProvider(QtWidgets.QFileIconProvider):
    def __init__(self, icons):
        QtWidgets.QFileIconProvider.__init__(self)
        self.icons = icons

    def icon(self, fileInfo):
        if fileInfo.suffix() == "json":
            return self.icons["user"]
        if fileInfo.isDir():
            return self.icons["folder"]
        else:
            return self.icons["warning"]
        return QtWidgets.QFileIconProvider.icon(self, fileInfo)