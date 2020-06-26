# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 18:07:14 2020

@author: aovch
"""
import json
from Database.DBHelper import finapp_stocks
import os

database_file = os.path.join(os.getcwd(),'Database','All_tickers.txt')

def form_str(i):
    if i is None:
        return ''
    else:
        return i


def stocks_from_file(js):
    values_tickers = [tuple(i.values())[:-1] for i in js]
    return tuple([x for x in values_tickers])

with open(database_file, 'r') as fh:
    file = json.loads(fh.read())

tuples = stocks_from_file(file)

print(tuples[0])


finapp_stocks.insert_stocks(tuples)