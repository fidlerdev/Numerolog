# load_icons.py

# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtWidgets
import os
from load_data import load_settings

class Icons(QtGui.QIcon):
    def __init__(self, path):
        QtGui.QIcon.__init__(self, path)

def get_icons():
    
    _root_folder = os.path.dirname(os.path.dirname(__file__))
    _icons_path = os.path.join(_root_folder, 'resources', 'icons', str(load_settings()['icons_set']))
    # _icons_path = os.getcwd() + "{0}resources{0}icons{0}{1}{0}".format(os.sep, load_settings()["icons_set"])
    print("icons_path: {}".format(_icons_path))
    # Записываем иконки в словарь объектов класса Icons
    '''
        TODO: 
            -- Убрать ненужные иконки с os.getcwd()
            -- Проработать навигацию папки resources
            
    '''
    icons = {
        "MAIN":                 Icons(os.getcwd() + "{0}resources{0}main_icon_100.png".format(os.sep)),
        "main":                 Icons(os.getcwd() + "{0}resources{0}main_icon_32.png".format(os.sep)),
        "main_beta_1":          Icons(os.getcwd() + "{0}resources{0}main_icon.png".format(os.sep)),
        "main_beta_2":          Icons(os.getcwd() + "{0}resources{0}main_beta_2.png".format(os.sep)),
        "add_folder":           Icons(os.path.join(_icons_path, "add_folder.png")),
        "add_user":             Icons(os.path.join(_icons_path, "add_user.png")),
        "open_workspace":       Icons(os.path.join(_icons_path, "open_workspace.png")),
        "close":                Icons(os.path.join(_icons_path, "close.png")),
        "print":                Icons(os.path.join(_icons_path, "print.png")),
        "user":                 Icons(os.path.join(_icons_path, "user.png")),
        "folder":               Icons(os.path.join(_icons_path, "folder.png")),
        "edit_file":            Icons(os.path.join(_icons_path, "edit_file.png")),
        "rename":               Icons(os.path.join(_icons_path, "pencil.png")),
        "calculate":            Icons(os.path.join(_icons_path, "calculate.png")),
        "delete":               Icons(os.path.join(_icons_path, "delete.png")),
        "warning":              Icons(os.path.join(_icons_path, "warning.png")),
        "arrow_up":             Icons(os.path.join(_icons_path, "arrow_up.png")),
        "arrow_down":           Icons(os.path.join(_icons_path, "arrow_down.png")),
        "settings":             Icons(os.path.join(_icons_path, "settings.png")),
        "open_list":            Icons(os.path.join(_icons_path, "open_list.png")),
        "search":               Icons(os.path.join(_icons_path, "search.png"))
    }
    return icons

# Определение иконок из класса QFileIconProvider
# icons = QtWidgets.QFileIconProvider()
