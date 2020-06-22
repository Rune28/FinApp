# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:45:38 2020

@author: aovch
"""


from Investment.InvestFuncs import StockInfo
import json

all_tck = StockInfo().parse_symbols(output_format = 'json')


with open('All_tickers.txt', 'w') as fh:
    fh.write(json.dumps(all_tck))