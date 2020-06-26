# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 18:07:14 2020

@author: aovch
"""
import json
from Database.DBHelper import finapp_stocks
import os

database_file = os.path.join(os.getcwd(),'Database','All_tickers.txt')



def stocks_from_file(js):
    values_tickers = [tuple(i.values()) for i in js]
    return tuple(values_tickers)

with open(database_file, 'r') as fh:
    file = json.loads(fh.read())

tuples = stocks_from_file(file)


finapp_stocks.insert_stocks(tuples)