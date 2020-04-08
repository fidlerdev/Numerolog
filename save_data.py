# save_data.py

# -*- coding: utf-8 -*-

import json
from os import getcwd, sep
from PyQt5 import QtGui


def save(path, **kwargs):
    """ 
    **kwargs:
        surname
        name
        middle_name
        bonus_list
        date_of_birth
        time_of_birth
        moon_birth
        delete
    """
    data = {
        "surname":          kwargs["surname"],
        "name":             kwargs["name"],
        "middle_name":      kwargs["middle_name"],
        "bonus_list":       kwargs["bonus_list"],
        "date_of_birth":    kwargs["date_of_birth"],
        "time_of_birth":    kwargs["time_of_birth"],
        "moon_birth":       kwargs["moon_birth"],
        "delete":           kwargs["delete"]
    }
    with open(path, "w") as file:
        json.dump(data, file, indent=4)
    return data

def save_settings(create_new=False, **kwargs):
    """
        **kwargs:
            save_chosen_working_dir -> bool
            chosen_working_dir_path -> str

            dictionary_list -> list

            font -> str
            font_size -> int
            icons_set -> int
        """
    data = {}
    # Сохранение пользовательских настроек - 1
    if create_new:
        data = {
            "save_chosen_working_dir":  True,
            "chosen_working_dir_path":  "",

            "dictionary_list":          {},

            "font":                     "Helvetica",
            "font_size":                10,
            "icons_set":                3
        }
    # Cохранение пользовательских настроек
    else:
        
        data = {
            "save_chosen_working_dir":  kwargs["save_chosen_working_dir"],
            "chosen_working_dir_path":  kwargs["chosen_working_dir_path"],

            "dictionary_list":          kwargs["dictionary_list"],

            "font":                     kwargs["font"],
            "font_size":                kwargs["font_size"],
            "icons_set":                kwargs["icons_set"]
        }
    path = getcwd() + sep + "settings.json"
    with open(path, "w") as file:
        json.dump(data, file, indent=4)
    return data