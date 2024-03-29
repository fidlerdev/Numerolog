# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtPrintSupport
from load_data import load, load_settings
from load_resources import get_icons
from result_widget import ResultWidget
import sqlite3
import json

class CalculateWidget(QtWidgets.QWidget):
    def __init__(self, parent, path):
        QtWidgets.QWidget.__init__(self, parent)
        self.path = path
        self.icons = get_icons()
        self.headers = [
            "День Рождения",
            "Число жизненного пути",
            "Сочетание Дня Рождения и ЧЖП",
            "Здоровье по Зюрняевой",
            "Ментальное число",
            "Финансы по Зюрняевой",
            "Таланты",
            "Профессии",
            "Число судьбы",
            "Число души",
            "Число Индивидуальности",
            "Число Зрелости",
            "Число Равновесия",
            "Число Активности",
            "Число Интеллекта",
            "Число Наследственности",
            "Карта Инклюзий",
            "Кармические уроки",
            "Скрытая страсть (Тайное желание)",
            "Подсознательное «Я»",
            "Проблемы, уроки, препятствия",
            "Пики, достижения, вершины",
            "Жизненные циклы",
            "Персональный год",
            "Персональный месяц"
        ]
        self.setupUi()
        self.load_data(path=path)
        
        self.btn_close.clicked.connect(self.close)

        self.list_calculate.currentItemChanged.connect(self.on_item_clicked)
        self.list_calculate.itemClicked.connect(self.on_item_clicked)
        self.btn_calculate.clicked.connect(self.on_result_create)


    def load_data(self, path):
        self.data = load(path)
        self.settings = load_settings()

        self.label_surname.setText("Фамилия:\t\t\t" + self.data["surname"])
        self.label_name.setText("Имя:\t\t\t\t" + self.data["name"])
        self.label_middle_name.setText("Отчество:\t\t\t" + self.data["middle_name"])

        self.label_date_of_birth.setText("Дата рождения:\t\t" + str(self.data["date_of_birth"][0]).rjust(2, "0") + 
                                        "." + str(self.data["date_of_birth"][1]).rjust(2, "0")
                                        + "." + str(self.data["date_of_birth"][2]))
        self.label_time_of_birth.setText("Время рождения:\t\t" + str(self.data["time_of_birth"][0]).rjust(2, "0") + 
                                        ":" + str(self.data["time_of_birth"][1]).rjust(2, "0"))
        self.label_moon_birth.setText("Лунный день рождения:\t" + str(self.data["moon_birth"]).rjust(2, "0"))

    def on_item_clicked(self, item):
        self.selected_item = item
        self.btn_calculate.setEnabled(True)

    def on_result_create(self):
        # algo_data[0] -> номер алгоритма
        # algo_data[1] -> порядковый номер [0...1]
        algo_data = self.selected_item.data(QtCore.Qt.UserRole)
        header = self.headers[algo_data[1]]

        if algo_data[0] in range(10, 13): # Если выбран алгоритм с 11 по 13
                if not self.settings["dictionary_list"][self.data["dictionary"]][-1]: # Если не были определены гласные и согласные
                    QtWidgets.QMessageBox.warning(
                        "Предупреждение",
                        "Гласные и согласные буквы не были\n\
                        установлены для данного алфавита.",
                        defaultButton=QtWidgets.QMessageBox.Ok
                        )
                    return
        # Если все значения установлены
        value = self.calculate(algo_data[0])

        self.result_widget = ResultWidget(
            path=self.path,
            header_text=header,
            value=value,
            row_id=algo_data[0]
            )
        self.result_widget.show()

    def calculate(self, algo):
        if algo in range(27):
            print('ALGO:', algo)
            return eval("self.algo_{}()".format(algo))
        return -1

    def algo_0(self):
        return self.data["date_of_birth"][0]

    def algo_1(self):
        day = self.data["date_of_birth"][0]
        month = self.data["date_of_birth"][1]
        year = self.data["date_of_birth"][2]
        
        value = int("{}{}{}".format(day, month, year).strip("0"))
        print(value)
        total = 0
        while True:
            while value:
                total += value % 10
                value //= 10
            print(total)
            if total <= 9 or total == 11 or total == 22 or \
                total == 33 or total == 44:
                break
            value = total
            total = 0

        return total

    def algo_2(self):
        return int(str(self.algo_0()) + str(self.algo_1()))

    def algo_3(self):
        pass

    def algo_4(self):
        return self.algo_0()

    def algo_5(self):
        year = self.data["date_of_birth"][2]
        year = str(year).strip("0")
        return int(year[0]) + int(year[-1]) # sum(first and (last!=0))

    def algo_6(self):
        month = self.data["date_of_birth"][1]
        total = 0
        while month:
            total += month % 10
            month //= 10
        return total

    def algo_7(self):
        day = self.data["date_of_birth"][0]
        total = 0
        while True:
            while day:
                total += day % 10
                day //= 10
            if total <= 9: 
                break
            day = total
            total = 0
        return total

    def algo_8(self):
        return self.algo_7()

    def algo_9(self):
        pass

    def algo_10(self):
        return self.algo_10__12(algo=10)

    def algo_11(self):
        return self.algo_10__12(algo=11)

    def algo_12(self):
        return self.algo_10__12(algo=12)

    def algo_13(self):
        value = self.algo_1() + self.algo_10()
        total = 0
        while True:
            while value:
                total += value % 10
                value //= 10
            print(total)
            if total < 9 or total == 11 or total == 22 or \
               total == 33:
                break
            value = total
            total = 0

        return total

    def algo_14(self):
        al_name = self.data["dictionary"]
        alphabet = self.settings['dictionary_list'][al_name][:-1]
        surname = self.data['surname']
        name = self.data['name']
        middle_name = self.data['middle_name']
        pers_data = [name[0]]
        try:
            pers_data.append(surname[0])
        except IndexError:
            pass
        try:
            pers_data.append(middle_name[0])
        except IndexError:
            pass
        value = 0
        for letter in pers_data:
            for ind, arr in enumerate(alphabet):
                val = ind + 1
                for alpha_letter in arr:
                    if alpha_letter[0].lower() == letter.lower():
                        value += val
                        print(val)
        total = 0
        if value > 9 and value != 11 and value != 22:
            total = 0
            while True:
                while value:
                    total += value % 10
                    value //= 10
                if total < 10 or total in [11, 22]:
                    break
                value = total
                total = 0
        else:
            total = value

        return total

    def algo_15(self):
        return self.algo_10__12(algo=15)
    
    def algo_16(self):
        date_of_birth = self.algo_0()
        value = self.algo_15()
        for i in str(date_of_birth):
            value += int(i)
        total = 0
        while True:
            while value:
                total += value % 10
                value //= 10
            print(total)
            if total < 9 or total == 11 or total == 22 or \
               total == 33:
                break
            value = total
            total = 0

        return total

    def algo_17(self):
        return self.algo_10__12(algo=17)

    def algo_18(self):
        al_name = self.data['dictionary']
        alphabet = self.settings["dictionary_list"][al_name][:-1] # Данные в формате tuple(Символ unicode, 1/0) + искл. посл. 
        surname = self.data["surname"]                       # 1 -> гласная буква
        name = self.data["name"]                             # 0 -> согласная буква
        middle_name = self.data["middle_name"]
        pers_data = [surname, name, middle_name] # Записываем Фам, Им, Отч
        # values = [0, 0, 0] # Значения сумм для Фам, Им и Отч
        total = ['Нет'] * 9
        for word in pers_data:
            if word:
                for letter in word:
                    for ind, arr in enumerate(alphabet):
                        # val = ind + 1
                        for alpha_letter in arr:
                            if alpha_letter[0].lower() == letter.lower():
                                if total[ind] == 'Нет':
                                    total[ind] = 1
                                else:
                                    total[ind] += 1
        return total

    def algo_19(self):
        arr = self.algo_18()
        total = 0
        for elem in arr:
            if elem == 'Нет':
                total += 1

        return total

    def algo_20(self):
        arr = self.algo_18()
        total = 0
        K = 3
        for elem in arr:
            try:
                if elem > K:
                    total += 1
            except TypeError:
                continue

        return total
    
    def algo_21(self):
        return (9 - self.algo_19())

    def algo_22(self):
        value = (
'''
1-я Проблема = {}
2-я Проблема = {}
3-я Проблема = {}
4-я Проблема = {}
''')
        # Начальные значения из .json файла
        day     = str(self.data['date_of_birth'][0])
        month   = str(self.data['date_of_birth'][1])
        year    = str(self.data['date_of_birth'][2])

        # Суммируем цифры в каждом числе, пока в каждом не останется по одной
        while len(day) + len(month) + len(year) > 3:
            day     = str(sum([int(x) for x in day]))
            month   = str(sum([int(x) for x in month]))
            year    = str(sum([int(x) for x in year]))

        day     = int(day)
        month   = int(month)
        year    = int(year)

        val_1 = abs(month - day)
        val_2 = abs(day - year)
        val_3 = abs(val_1 - val_2)
        val_4 = abs(month - year)
        
        
        return value.format(val_1, val_2, val_3, val_4)


    def algo_23(self):
        value = (
'''
1-й Пик = {}
2-й Пик = {}
3-й Пик = {}
4-й Пик = {}
''')
        # Начальные значения из .json файла
        day     = str(self.data['date_of_birth'][0])
        month   = str(self.data['date_of_birth'][1])
        year    = str(self.data['date_of_birth'][2])

        # Суммируем цифры в каждом числе, пока в каждом не останется по одной
        while len(day) + len(month) + len(year) > 3:
            day     = str(sum([int(x) for x in day]))
            month   = str(sum([int(x) for x in month]))
            year    = str(sum([int(x) for x in year]))

        day     = int(day)
        month   = int(month)
        year    = int(year)

        print('''
        day:    {}
        month:  {}
        year:   {}
        '''.format(day, month, year))


        val_1 = str(month + day)
        val_2 = str(day + year)
        val_3 = str(abs(month - year))
        val_4 = str(month + year)

        v_1 = False
        v_2 = False
        v_3 = False
        v_4 = False

        while True:

            if val_1 != '11' and val_1 != '22':
                val_1    = str(sum([int(x) for x in val_1]))
            else:
                v_1 = True

            print('pre_val_12:', val_2)
            if val_2 != '11' and val_2 != '22':
                print(val_2 != 11, val_2 != 22)
                val_2    = str(sum([int(x) for x in val_2]))
            else:
                v_2 = True

            if val_3 != '11' and val_3 != '22':
                val_3    = str(sum([int(x) for x in val_3]))
            else:
                v_3 = True

            if val_4 != '11' and val_4 != '22':
                val_4    = str(sum([int(x) for x in val_4]))
            else:
                v_4 = True
            
            if (v_1 or len(val_1) == 1) and (v_2 or len(val_2) == 1) and \
                (v_3 or len(val_3) == 1) and (v_4 or len(val_4) == 1):
                break

        print('val_2:', val_2)
        return value.format(val_1, val_2, val_3, val_4)

    def algo_24(self):
        value = (
'''
Формирующий цикл    = {}
Продуктивный цикл   = {}
Результативный цикл = {}
''')
        # Начальные значения из .json файла
        day     = str(self.data['date_of_birth'][0])
        month   = str(self.data['date_of_birth'][1])
        year    = str(self.data['date_of_birth'][2])

        while len(day) + len(month) + len(year) > 3:
            day     = str(sum([int(x) for x in day]))
            month   = str(sum([int(x) for x in month]))
            year    = str(sum([int(x) for x in year]))
        
        return value.format(month, day, year)




    def algo_25(self):
        import datetime

        year = [int(x) for x in str(datetime.datetime.now().year)]

        day = [int(x) for x in str(self.data['date_of_birth'][0])]

        month = [int(x) for x in str(self.data['date_of_birth'][1])]

        print('year:', year)
        print('month:', day)
        print('day:', month)

        arr = year + day + month

        print('arr:', arr)

        total = 0

        for i in arr:
            total += i
        
        print('total:', total)

        summary = 0
        while True:
            summary += total % 10
            total //= 10
            if total == 0:
                print('summary:', summary)
                if summary < 10:
                    break
                if summary > 10:
                    total = summary
                    summary = 0

        return summary

    def algo_26(self):
        import datetime
        pers_year = self.algo_25()
        month = str(datetime.datetime.now().month)

        try:
            total = int(month[0]) + int(month[1]) + pers_year
        except IndexError:
            total = int(month[0]) + pers_year

        summary = 0
        while True:
            summary += total % 10
            total //= 10
            if total == 0:
                if summary < 10:
                    break
                if summary > 10:
                    total = summary
                    summary = 0

        return summary

    def algo_10__12(self, algo):
        al_name = self.data["dictionary"]
        alphabet = self.settings["dictionary_list"][al_name][:-1] # Данные в формате tuple(Символ unicode, 1/0) + искл. посл. знач.
        surname = self.data["surname"]                       # 1 -> гласная буква
        name = self.data["name"]                             # 0 -> согласная буква
        middle_name = self.data["middle_name"]
        pers_data = [surname, name, middle_name] # Записываем Фам, Им, Отч
        values = [0, 0, 0] # Значения сумм для Фам, Им и Отч
        alpha_type = None # 1 -> гласные 0 -> согласные
        if algo == 11: alpha_type = 1
        if algo == 12: alpha_type = 0
        # Производим вычисление для Ф, И и О
        for word, ind_val in zip(pers_data, range(len(values))):
            # находим значение для каждого символа слова
            # если слово не пустая строка (Оптимизация)
            if word:
                for letter in word:
                    # Проходимся по всему алфавиту, учитывая индекс+1=Вес символа
                    for ind, arr in enumerate(alphabet):
                        val = ind + 1
                        # Проходимся по списку символов с одинаковым весом
                        for alpha_letter in arr:
                            if alpha_letter[0].lower() == letter.lower():
                                if (algo == 11) or (algo == 12):
                                    if alpha_letter[1] == alpha_type:
                                        values[ind_val] += val
                                else:
                                    values[ind_val] += val
            else: continue # Если Ф или И или О не было введено -> пропускаем

        # Складываем значения имени, фамилии и отчества до однознач. числа
        for ind, val in enumerate(values):
            total = 0
            value = val
            while True:
                while value:
                    total += value % 10
                    value //= 10
                if total < 10:
                    break
                value = total
                total = 0
            values[ind] = total

        if algo == 15:
            value = values[1]
        elif algo == 17:
            value = values[0]
        else:
            value = sum(values) # суммируем все значения 
        if value > 9 and value != 11 and value != 22:
            total = 0
            while True:
                while value:
                    total += value % 10
                    value //= 10
                if total < 10 or total in [11, 22]:
                    break
                value = total
                total = 0
        else:
            total = value

        return total



        
    def setupUi(self):
        self.resize(361, 607)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        spacerItem = QtWidgets.QSpacerItem(30, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
        self.btn_calculate = QtWidgets.QPushButton(self)
        self.btn_calculate.setEnabled(False)
        self.gridLayout.addWidget(self.btn_calculate, 4, 1, 1, 1)
        self.btn_close = QtWidgets.QPushButton(self)
        self.gridLayout.addWidget(self.btn_close, 7, 1, 1, 1)
        self.list_calculate = QtWidgets.QListWidget(self)
        self.list_calculate.setFrameShape(QtWidgets.QFrame.Box)
        self.list_calculate.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list_calculate.setDragEnabled(False)
        self.list_calculate.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.list_calculate.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.list_calculate.setProperty("isWrapping", False)
        self.list_calculate.setResizeMode(QtWidgets.QListView.Fixed)

        # Создаем 24 ячейки в таблице
        for _ in range(25):
            item = QtWidgets.QListWidgetItem()
            self.list_calculate.addItem(item)

        self.gridLayout.addWidget(self.list_calculate, 3, 1, 1, 1)
        self.groupbox_date = QtWidgets.QGroupBox(self)
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupbox_date)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.label_date_of_birth = QtWidgets.QLabel(self.groupbox_date)
        self.verticalLayout_3.addWidget(self.label_date_of_birth)
        self.label_time_of_birth = QtWidgets.QLabel(self.groupbox_date)
        self.verticalLayout_3.addWidget(self.label_time_of_birth)
        self.label_moon_birth = QtWidgets.QLabel(self.groupbox_date)
        self.verticalLayout_3.addWidget(self.label_moon_birth)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupbox_date, 1, 1, 1, 1)
        self.groupbox_name = QtWidgets.QGroupBox(self)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupbox_name)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.label_surname = QtWidgets.QLabel(self.groupbox_name)
        self.verticalLayout_2.addWidget(self.label_surname)
        self.label_name = QtWidgets.QLabel(self.groupbox_name)
        self.verticalLayout_2.addWidget(self.label_name)
        self.label_middle_name = QtWidgets.QLabel(self.groupbox_name)
        self.verticalLayout_2.addWidget(self.label_middle_name)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupbox_name, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 6, 1, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.retranslateUi()



    def retranslateUi(self):
        self.setWindowTitle("Расчёты")
        self.btn_calculate.setText("Рассчитать")
        self.btn_calculate.setIcon(self.icons["calculate"])
        self.btn_close.setText("Закрыть")
        __sortingEnabled = self.list_calculate.isSortingEnabled()
        self.list_calculate.setSortingEnabled(False)
        # Редактируем ячейки списка
        values = [0, 1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        for num in zip(values, range(25)):
            item = self.list_calculate.item(num[1])
            # item.data == (Номер алгоритма, порядковый номер в self.headers)
            print(num)
            item.setData(QtCore.Qt.UserRole, (num[0], num[1]))
            item.setText("{id}. {name}".format(
                id=num[0] + 1,
                name=self.headers[num[1]]
                ))
        
        self.list_calculate.setSortingEnabled(__sortingEnabled)
        self.groupbox_date.setTitle("Даты")
        self.label_date_of_birth.setText("Дата рождения")
        self.label_time_of_birth.setText("Время рождения")
        self.label_moon_birth.setText("Лунный день рождения")
        self.groupbox_name.setTitle("Ф. И. О.")
        self.label_surname.setText("Фамилия")
        self.label_name.setText("Имя")
        self.label_middle_name.setText("Отчество")




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = CalculateWidget(None, r"/Users/fidler/Desktop/КОНТРАГЕНТЫ/Benjamin.json")
    widget.show()
    sys.exit(app.exec())