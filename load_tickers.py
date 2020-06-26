# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 18:07:14 2020

@author: aovch
"""
import json
from Database.DBHelper import finapp_stocks
import os

database_file = os.path.join(os.getcwd(),'Database','All_tickers.txt')


def format_str(i):
    if i is None:
        return ''
    elif i is True:
        return 'Yes'
    elif i is False:
        return 'No'
    else:
        return i

format_str(True)

def stocks_from_file(js):
    values_tickers = [tuple(format_str(i.values())) for i in js]
    return tuple(values_tickers)

with open(database_file, 'r') as fh:
    file = json.loads(fh.read())

tuples = stocks_from_file(file)

print(tuples)

finapp_stocks.insert_stocks(tuples)