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
        desc_list
    """
    data = {
        "surname":          kwargs["surname"],
        "name":             kwargs["name"],
        "middle_name":      kwargs["middle_name"],
        "bonus_list":       kwargs["bonus_list"],
        "date_of_birth":    kwargs["date_of_birth"],
        "time_of_birth":    kwargs["time_of_birth"],
        "moon_birth":       kwargs["moon_birth"],
        "delete":           kwargs["delete"],
        "dictionary":       kwargs["dictionary"],
        "desc_list":        kwargs["desc_list"]
    }
    with open(path, "w") as file:
        json.dump(data, file, indent=4)
    return data


    data = {
        "surname":          data["surname"],
        "name":             data["name"],
        "middle_name":      data["middle_name"],
        "bonus_list":       data["bonus_list"],
        "date_of_birth":    data["date_of_birth"],
        "time_of_birth":    data["time_of_birth"],
        "moon_birth":       data["moon_birth"],
        "delete":           data["delete"],
        "dictionary":       data["dictionary"],
        "desc_list":        data["desc_list"]
    }

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
    # Добавляем русский язык по умолчанию
    if create_new:
        data = {
            "save_chosen_working_dir":  True,
            "chosen_working_dir_path":  "", 
            "dictionary_list": {"\u0420\u0443\u0441\u0441\u043a\u0438\u0439": [
                                [
                                    "\u0410",
                                    "\u0418",
                                    "\u0421",
                                    "\u042a"
                                ],
                                [
                                    "\u0411",
                                    "\u0419",
                                    "\u0422",
                                    "\u042b"
                                ],
                                [
                                    "\u0412",
                                    "\u041a",
                                    "\u0423",
                                    "\u042c"
                                ],
                                [
                                    "\u0413",
                                    "\u041b",
                                    "\u0424",
                                    "\u042d"
                                ],
                                [
                                    "\u0414",
                                    "\u041c",
                                    "\u0425",
                                    "\u042e"
                                ],
                                [
                                    "\u0415",
                                    "\u041d",
                                    "\u0426",
                                    "\u042f"
                                ],
                                [
                                    "\u0401",
                                    "\u041e",
                                    "\u0427"
                                ],
                                [
                                    "\u0416",
                                    "\u041f",
                                    "\u0428"
                                ],
                                [
                                    "\u0417",
                                    "\u0420",
                                    "\u0429"
                                ]
                            ],
        },

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