# load_icons.py

# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtWidgets
import os
from load_data import load_settings

class Icons(QtGui.QIcon):
    def __init__(self, path):
        QtGui.QIcon.__init__(self, path)

def get_icons():
    _icons_path = os.getcwd() + "{0}resources{0}icons{0}{1}{0}".format(os.sep, load_settings()["icons_set"])
    print("icons_path: {}".format(_icons_path))
    # Записываем иконки в словарь объектов класса Icons
    icons = {
        "MAIN":                 Icons(os.getcwd() + "{0}resources{0}main_icon_100.png".format(os.sep)),
        "main":                 Icons(os.getcwd() + "{0}resources{0}main_icon_32.png".format(os.sep)),
        "add_folder":           Icons(_icons_path + "add_folder.png"),
        "add_user":             Icons(_icons_path + "add_user.png"),
        "open_workspace":       Icons(_icons_path + "open_workspace.png"),
        "close":                Icons(_icons_path + "close.png"),
        "print":                Icons(_icons_path + "print.png"),
        "user":                 Icons(_icons_path + "user.png"),
        "folder":               Icons(_icons_path + "folder.png"),
        "edit_file":            Icons(_icons_path + "edit_file.png"),
        "rename":               Icons(_icons_path + "pencil.png"),
        "calculate":            Icons(_icons_path + "calculate.png"),
        "delete":               Icons(_icons_path + "delete.png"),
        "warning":              Icons(_icons_path + "warning.png"),
        "arrow_up":             Icons(_icons_path + "arrow_up.png"),
        "arrow_down":           Icons(_icons_path + "arrow_down.png"),
        "settings":             Icons(_icons_path + "settings.png"),
        "open_list":            Icons(_icons_path + "open_list.png"),
        "search":               Icons(_icons_path + "search.png")
    }
    return icons

# Определение иконок из класса QFileIconProvider
# icons = QtWidgets.QFileIconProvider()
