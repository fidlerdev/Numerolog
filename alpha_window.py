from PyQt5 import QtWidgets, QtCore
from load_data import load_settings
from dialog_windows import CloseDialog
from save_data import save_settings

class AlphaWindow(QtWidgets.QWidget):
    saved = QtCore.pyqtSignal(list)

    def __init__(self, alphabet, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.alphabet = load_settings()["dictionary_list"][alphabet]
        self.closing = False
        # print(self.alphabet)
        self.setupUi()
        self.load_letters()
        self.btn_close.clicked.connect(self.quit_action)
        self.btn_save.clicked.connect(self.save)

    def save(self):
        alphabet = [[], [], [], [], [], [], [], [], []]
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            letter_type = None
            if item.radio_consonant.isChecked():
                letter_type = 0
            else:
                letter_type = 1
            alphabet[index % 9].append([item.letter, letter_type])
        alphabet.append(True)
        
        # print(alphabet)
        self.saved.emit(alphabet)
        self.btn_save.setEnabled(False)
        self.btn_save.repaint()

    def on_close(self):
        if not self.btn_save.isEnabled():
            return QtWidgets.QMessageBox.Accepted
        dialog = CloseDialog(self)
        # Переопределяем надпись в модальном окне
        dialog.label.setText("Вы действительно хотите закрыть окно?\nВсе несохраненные данные будут утеряны")

        return dialog.exec()

    def closeEvent(self, event):
        if not self.btn_save.isEnabled():
            event.accept()
            return

        if not self.closing:
            result = self.on_close()
            if result == QtWidgets.QMessageBox.Accepted:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def quit_action(self):
        if not self.btn_save.isEnabled():
            self.close()
            return
        result = self.on_close()
        self.closing = True
        if result == QtWidgets.QMessageBox.Accepted:
            self.close()
        else:
            self.closing = False


    def load_letters(self):
        from functools import reduce
        count = reduce(lambda prev, now: prev + len(now), self.alphabet[:-1], 0)
        ord_letters = [0] * count
        for group_weight, group in enumerate(self.alphabet[:-1]):
            for letter_weight, letter in enumerate(group):
                ord_letters[group_weight + letter_weight * 9] = letter
        
        for letter in ord_letters:
            AlphaListWidgetItem(
                parent=self.list_widget,
                letter=letter[0],
                val=letter[1]
            )


    def setupUi(self):
        self.resize(400, 600)
        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.vertical_layout)
        self.list_widget = QtWidgets.QListWidget(self)
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.btn_save = QtWidgets.QPushButton(self)
        self.btn_close = QtWidgets.QPushButton(self)

        self.vertical_layout.addWidget(self.list_widget)
        self.vertical_layout.addWidget(self.btn_save)
        self.vertical_layout.addWidget(self.btn_close)

        self.retranslateUi()

    def retranslateUi(self):
        self.btn_close.setText("Закрыть")
        self.btn_save.setText("Сохранить")



class AlphaListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, parent, letter, val):
        QtWidgets.QListWidgetItem.__init__(self, parent=parent)
        self.parent = parent
        self.letter = letter
        self.setupUi()
        self.set_letter_type(val)
        parent.addItem(self)
        parent.setItemWidget(self, self.widget)
        self.setData(QtCore.Qt.UserRole, val)
        self.radio_consonant.clicked.connect(self.on_value_change)
        self.radio_vowel.clicked.connect(self.on_value_change)

    def on_value_change(self, checked):
        self.parent.parentWidget().btn_save.setEnabled(True)
        self.parent.parentWidget().btn_save.repaint()

    def set_letter_type(self, val):
        if val: self.radio_vowel.setChecked(True)
        else: self.radio_consonant.setChecked(True)

    def setupUi(self):
        self.widget = QtWidgets.QWidget()
        horizontal_layout = QtWidgets.QHBoxLayout()
        self.label_letter = QtWidgets.QLabel()
        self.radio_vowel = QtWidgets.QRadioButton()
        self.radio_consonant = QtWidgets.QRadioButton()
        
        horizontal_layout.addStretch()
        horizontal_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        horizontal_layout.addWidget(self.label_letter)
        horizontal_layout.addWidget(self.radio_consonant)
        horizontal_layout.addWidget(self.radio_vowel)
        self.widget.setLayout(horizontal_layout)
        self.widget.show()
        self.setSizeHint(self.widget.sizeHint())

        self.retranslateUi()


    def retranslateUi(self):
        self.label_letter.setText(self.letter + ":\t")
        self.radio_consonant.setText("Согласная")
        self.radio_vowel.setText("Гласная")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = AlphaWindow(alphabet="Русский")
    window.show()
    sys.exit(app.exec())
