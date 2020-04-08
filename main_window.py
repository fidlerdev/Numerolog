# mainwindow.py

# -*- coding: utf-8 -*-

# импорт всех компонентов из модуля QtWidgets
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
# Класс с определением собственных диалоговых окон
from dialog_windows import CloseDialog, CreateDialog, CreateDialog_ext

from treeView_page import *

from load_resources import get_icons
from load_data import load_settings
from save_data import save_settings

from user import UserWidget

from settings import SettingsWidget

import os

# Класс, описыающий стартовое окно с hint'ами
class StartPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # label_greet = QtWidgets.QLabel("Добро пожаловать на главную страницу нумеролога")
        # label_greet.setAlignment(QtCore.Qt.AlignHCenter)
        # label_hint = QtWidgets.QLabel("Подсказки и мануал по эксплуатации в кратком изложении")
        # label_hint.setAlignment(QtCore.Qt.AlignHCenter)

        # vbox = QtWidgets.QVBoxLayout(self)
        # vbox.addWidget(label_greet)
        # vbox.addWidget(label_hint)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, path_default=""):
        super().__init__()

        # TODO:
        # 1. Научиться нормально документировать :) +-
        # 2. Развернуть окно в полноэкранном режиме или растянуть на весь экран (есть отличия) +
        # 3. Проследить изменение размера и положения компонентов при изменении размеров окна +-
        # ...


        # Начальный каталог
        self.path_default = path_default
        
        self.active_dir = False

        # Записываем иконки в словарь c помощью функции из модуля load_resources
        self.icons = get_icons()

        self.min_size = QtCore.QSize(QtWidgets.QApplication.desktop().availableGeometry().width() // 4 * 3,
                                     QtWidgets.QApplication.desktop().availableGeometry().height() // 4 * 3)
        self.setMinimumSize(self.min_size)

        self.setWindowTitle("Нумеролог")

        # Корневой контейнер, в который помещаются все окна, которые отображаются последовательно
        self.stack_cont = QtWidgets.QStackedWidget(parent=self)
        # Делаем stack_cont — корневой контейнер — ЦЕНТРАЛЬНЫМ для главного окна
        self.setCentralWidget(self.stack_cont)
        # Создаем стартовую страницу
        start_page = StartPage()
    
        # Добавляем стартовую страницу в корневой контейер
        self.stack_cont.addWidget(start_page)
        
        data = load_settings()
        # Проверяем на значение True и что путь к папке не пустой
        if data["save_chosen_working_dir"] and data["chosen_working_dir_path"].strip():
            self.path_default = data["chosen_working_dir_path"]
            self.active_dir = True
            self.show_toolbar()
            print("PATH:", data["chosen_working_dir_path"])
            self.tree_view = TreeViewWindow(path=data["chosen_working_dir_path"], icons=self.icons, tool_bar=self.toolBar)
            self.setWindowTitle("Нумеролог —— {}".format(data["chosen_working_dir_path"]))
            self.tree_view.setColumnWidth(0, self.size().width() // 4 * 3)
            
            # Добавляем в конец окно с рабочей директорией и сохраняем его индекс
            i = self.stack_cont.addWidget(self.tree_view)
            # Выводим окно на первую позицию
            self.stack_cont.setCurrentIndex(i)
            

        # Обращение к menu bar главного окна, который оно имеет по умолчанию
        bar = self.menuBar()

        # Добавление пункта в menu bar
        bar_main = bar.addMenu("Главная")
        bar_file = bar.addMenu("Файл")
        # Добавление подпунктов в menu bar
        self.create_wd_action = bar_file.addAction("Выбрать рабочую область",
                                        self.choose_working_dir,
                                        shortcut=QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_O))
        self.create_wd_action.setIcon(QtGui.QIcon(self.icons["open_workspace"]))

        self.settings_action = bar_main.addAction("Настройки",
                                        self.open_settings,
                                        shortcut=QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Comma))
        self.settings_action.setIcon(QtGui.QIcon(self.icons["settings"]))

    
    def open_settings(self):
        data = {}
        try:
            load_settings()
        except FileNotFoundError:
            print("Файл с настройками не найден, создаем новый...")
            save_settings(create_new=True)
        self.settings = SettingsWidget()
        self.settings.setWindowModality(QtCore.Qt.ApplicationModal)
        self.settings.show()
        


    """
    Выбор рабочей области — создание директории или выбор существующей
    """
    def choose_working_dir(self):
        self.path_default = QtWidgets.QFileDialog.getExistingDirectory(parent=self,
                                            caption="Выберите расположение области",
                                            directory=QtCore.QDir.homePath())
        # Если просто закрыли окно — ничего не делаем
        if not self.path_default:
            return
        if self.active_dir:
            self.close_working_dir()
        self.active_dir = True
        self.setWindowTitle("Нумеролог —— {}".format(self.path_default))
        self.show_toolbar()
        print(self.path_default)
        self.tree_view = TreeViewWindow(path=self.path_default, icons=self.icons, tool_bar=self.toolBar)
        self.tree_view.setColumnWidth(0, self.size().width() // 4 * 3)
        
        # Добавляем в конец окно с рабочей директорией и сохраняем его индекс
        i = self.stack_cont.addWidget(self.tree_view)
        # Выводим окно на первую позицию
        self.stack_cont.setCurrentIndex(i)

        # Если запоминаем выбранную рабочую область
        data = load_settings()
        if data["save_chosen_working_dir"]:
            print("PATH ON SAVED:", self.path_default)
            save_settings(
                    save_chosen_working_dir=data["save_chosen_working_dir"],
                    chosen_working_dir_path=self.path_default, #Здесь не меняем ничего
                    dictionary_list=data["dictionary_list"], #Пока что нет функционала
                    font=data["font"],
                    font_size=data["font_size"],
                    icons_set=data["icons_set"]
            )

    def show_toolbar(self):
        # Создание панели инструментов в главном окне
        self.toolBar = self.addToolBar("Панель инструментов") 
        # Устанавливает текст кнопки под ней
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        # Запрещает выносить tool bar за пределы окна
        self.toolBar.setFloatable(False)
        # Добавление на панель инструментов кнопки создания папки с иконкой *папки*
        self.create_dirBtn = self.toolBar.addAction("Создать папку")
        self.create_dirBtn.setIcon(QtGui.QIcon(self.icons["add_folder"]))
        self.create_dirBtn.triggered.connect(lambda: self.create(self.create_dir, "папки"))
        
        self.create_fileBtn = self.toolBar.addAction("Создать клиента")
        self.create_fileBtn.setIcon(self.icons["add_user"])
        self.create_fileBtn.triggered.connect(lambda: self.create(self.create_user, "файла"))

        self.edit_user = self.toolBar.addAction("Редактировать")
        self.edit_user.setIcon(self.icons["edit_file"])
        self.edit_user.setEnabled(False)

        # Сортировать по алфавиту
        self.sort_alpha = self.toolBar.addAction("Сортировать: А-Я")
        self.sort_alpha.setIcon(self.icons["arrow_up"])

        # Сортировать по дате создания
        self.sort_cr = self.toolBar.addAction("Сортировать по дате")
        self.sort_cr.setIcon(self.icons["arrow_up"])

        self.open_full_list = self.toolBar.addAction("Весь список")
        self.open_full_list.setIcon(self.icons["open_list"])

        self.close_wd = self.toolBar.addAction("Закрыть область")
        self.close_wd.setIcon(self.icons["close"])
        self.close_wd.triggered.connect(self.close_working_dir)

    def close_working_dir(self):
        self.toolBar.close()
        self.stack_cont.removeWidget(self.tree_view)
        self.setWindowTitle("Нумеролог")
        save_settings(
                    save_chosen_working_dir=data["save_chosen_working_dir"],
                    chosen_working_dir_path="", #Здесь не меняем ничего
                    dictionary_list=data["dictionary_list"], #Пока что нет функционала
                    font=data["font"],
                    font_size=data["font_size"],
                    icons_set=data["icons_set"]
            )


    def create(self, func, type):
        dialog = CreateDialog_ext(self, type=type, path=self.path_default)
        result = dialog.exec()
        if result == QtWidgets.QMessageBox.Accepted:
            path = dialog.get_path()
            print(path)
            func(path)

    def create_dir(self, path):
        try:
            os.mkdir(path)
            print("Папка успешно создана")
        except FileExistsError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Папка {} уже существует".format(path), defaultButton=QtWidgets.QMessageBox.Ok)

    def create_user(self, path):
        self.path = path + ".json"
        if os.path.exists(self.path):

            dialog = CloseDialog(self)
            dialog.setWindowTitle("Файл уже существует")
            dialog.label.setText("Вы хотите отредактировать существующие данные?")
            result = dialog.exec()

            if result == QtWidgets.QMessageBox.Accepted:
                self.user_window_show(operation="Редактирование данных")
        else:
            self.user_window_show(operation="Создание")

    def user_window_show(self, operation):
        create_widget = UserWidget(operation=operation, user_name=self.path, path=self.path)
        create_widget.setWindowModality(QtCore.Qt.ApplicationModal)
        create_widget.show()


    # Действия при закрытии приложения
    def closeEvent(self, event):
        # Создаем диалоговое окно перед выходом, в кач-ве parent указываем
        # главное окно, чтобы оно центрировалось относительного него
        conf_dialog = CloseDialog(parent=self)

        # Результат будет зависеть от нажатой кнопки
        # 0 - Отмена
        # 1 - ОК
        # Запускаем цикл обработки сигналов
        result = conf_dialog.exec()
        print("Exit status result:", result)
        # Атрибут Accepted класса QDialog будет равен 1.
        # Это же значение возвращает слот accept(), который подключён к кнопке "Да"
        if result == QtWidgets.QDialog.Accepted:
            # Выходим
            event.accept()
        else:
            # Остаёмся
            event.ignore()



# Тестирование модуля
if __name__ == "__main__":
    import sys
    #######################
    data = {}
    try:
        data = load_settings()
    except FileNotFoundError:
        print("Файл с настройками не найден, создаем новый...")
        data = save_settings(create_new=True)
    #######################
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(get_icons()["main"])
    app.setFont(QtGui.QFont(data["font"], data["font_size"]))
    
    m_window = MainWindow()
        
    m_window.show()
    sys.exit(app.exec_())
        
