# load_data.py

# -*- coding: utf-8 -*-

import json
from os import getcwd, sep

def load(path):
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
    data = ""
    with open(path, "r") as file:
        data = json.load(file)
    return data
    

def load_settings():
    """
    **kwargs:
        save_chosen_working_dir -> str -> path

        dictionary_list -> list

        font -> str
        font_size -> int
        icons_set -> int
    """
    data = ""
    with open(getcwd()+sep+"settings.json", "r") as file:
        data = json.load(file)
    return data
