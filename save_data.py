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
                                    ("\u0410", 1),
                                    ("\u0418", 1),
                                    ("\u0421", 0),
                                    ("\u042a", 0)
                                ],
                                [
                                    ("\u0411", 0),
                                    ("\u0419", 0),
                                    ("\u0422", 0),
                                    ("\u042b", 1)
                                ],
                                [
                                    ("\u0412", 0),
                                    ("\u041a", 0),
                                    ("\u0423", 1),
                                    ("\u042c", 0)
                                ],
                                [
                                    ("\u0413", 0),
                                    ("\u041b", 0),
                                    ("\u0424", 0),
                                    ("\u042d", 1)
                                ],
                                [
                                    ("\u0414", 0),
                                    ("\u041c", 0),
                                    ("\u0425", 0),
                                    ("\u042e", 1)
                                ],
                                [
                                    ("\u0415", 1),
                                    ("\u041d", 0),
                                    ("\u0426", 0),
                                    ("\u042f", 1)
                                ],
                                [
                                    ("\u0401", 1),
                                    ("\u041e", 1),
                                    ("\u0427", 0)
                                ],
                                [
                                    ("\u0416", 0),
                                    ("\u041f", 0),
                                    ("\u0428", 0)
                                ],
                                [
                                    ("\u0417", 0),
                                    ("\u0420", 0),
                                    ("\u0429", 0)
                                ],
                                True # Последнее значение под инд. [-1] или [9] True, если установлены гласные и согласные
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