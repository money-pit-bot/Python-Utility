#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Stefano Giostra"
__maintainer__ = "Stefano Giostra"
__license__ = "GPL"
__version__ = "1.0.0"

from datetime import datetime, timedelta
from functools import reduce
import operator
import os
import sys
import platform

# ----------------------------------------------------------------------------------------------------------------------
# ----- DICT UTILS -----
# With this utils You can dynamically generate a multilevel dictionary


def getFromDict(dataDict, mapList):
    """
    given a dict and a key list, this utility return the sub object
    :param dataDict: the dictionary
    :param mapList: the list of keys
    :return: value or dict
    """
    assert isinstance(dataDict, dict)
    assert isinstance(mapList, list)
    return reduce(operator.getitem, mapList, dataDict)


def incDictKeyValue(dataDict, mapList, value):
    """
    If the key exists, the utility increments the value index by the key tree, else, if the key don't exist
    add the pair key value up to the root, if necessary
    In the list You must pass all the keys, rom to root to key to update
    Es:
        d = {'a':
            {'v': 1,
             'b': {'v': 1,
                   'c': {'v': 1}}
             }}
        k = ['a', 'b', 'v']
        x = incDictKeyValue(d,k,1)
        print(d)
    
        k = ['a', 'b', 'v']
        x = incDictKeyValue(d,k,1)
        print(d)
    :param dataDict: the dictionary
    :param mapList: the list of keys
    :param value: the inc of the vaule
    :return: None
    """
    assert isinstance(dataDict, dict)
    assert isinstance(mapList, list)
    try:
        if isinstance(value, dict):
            reduce(operator.getitem, mapList[:-1], dataDict)[mapList[-1]] = value
        else:
            # You can make the inc only a leave level
            reduce(operator.getitem, mapList[:-1], dataDict)[mapList[-1]] += value
    except KeyError:
        incDictKeyValue(dataDict, mapList[:-1], {mapList[-1]: value})


def setDictKeyValue(dataDict, mapList, value):
    """
    If the key exists, the utility set the value associated at the last key of the tree, else, if the key don't exist,
    add the pair key value up to the root, if necessary
    :param dataDict: the dictionary
    :param mapList: the list of keys
    :param value: the value to set
    :return: None
    """
    assert isinstance(dataDict, dict)
    assert isinstance(mapList, list)
    try:
        reduce(operator.getitem, mapList[:-1], dataDict)[mapList[-1]] = value
    except KeyError:
        incDictKeyValue(dataDict, mapList[:-1], {mapList[-1]: value})


'''
#test
giorno = '12/Mar/2018'
inform = '1 BOOT'
model = 'VOX30'
keys = [giorno,'inform',inform,'model']
inform_dict = {"accepted": {'giorno': {}}, "dropped": {'giorno': {}}}
incDictKeyValue(inform_dict["accepted"]["giorno"], keys, {model:1})
print(inform_dict)
keys.append(model)
incDictKeyValue(inform_dict["accepted"]["giorno"], keys, 1)
print(inform_dict)
setDictKeyValue(inform_dict["accepted"]["giorno"], keys, 10)
print(inform_dict)
'''


# ----------------------------------------------------------------------------------------------------------------------
def json_to_csv(json_buf, p_row_key, p_column_keys, csv_filename, separator='|'):
    """
    Questo metodo prende in ingresso un buffer json e lo converte in un csv, mettendo come prima colonna
    la chiave del json scelta e come altre colonne le chiavi passate nella lista p_column_keys

    :param json_buf: il buffer json da convertire
    :param p_row_key: Nome da dare alla colonna che corrisponde alla chiave del dizionario
    :param p_column_keys: le chiavi del dizionario che si volgiono visualizzare come colonne del csv
    :param csv_filename: nome del file in cui salvare i dati
    :param separator: i separatore da usare, di default è il |
    :return: path completo del file CSV generato
    """
    assert isinstance(p_column_keys, list)
    csv_buf = '%s%s%s' % (p_row_key, separator, separator.join(p_column_keys))
    for key in json_buf:
        csv_buf = "%s\n%s" % (csv_buf, key)
        for col_key in p_column_keys:
            try:
                csv_buf = "%s%s%s" % (csv_buf, separator, json_buf[key][col_key])
            except KeyError:
                csv_buf += "%s0" % separator

    f = open(csv_filename, 'w')
    f.write(csv_buf)
    f.close()
    return os.path.abspath(csv_filename)


# ----------------------------------------------------------------------------------------------------------------------
def get_utility_fullpath():
    """
    When You generate an Exe using PyInstaller, os.path.dirname is not the path of the exe
    :return: the complete path of the utility that call me
    """
    if platform.system() == 'Windows':
        cmd = 'python.exe'
    else:
        cmd = 'python'
    if cmd in sys.executable:
        lpath = os.path.dirname(__file__)
    else:
        lpath = os.path.dirname(sys.executable)
    return lpath


# ----------------------------------------------------------------------------------------------------------------------
def get_day_at_00(passed_days=0):
    """
    :param passed_days: positive passed days, negative nxt days
    :return: the day at midnight
    """
    today = datetime.today()
    return datetime(today.year, today.month, today.day) - timedelta(days=passed_days)
