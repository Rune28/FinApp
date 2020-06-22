# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 09:31:27 2020

@author: aovch
"""
import yfinance as yf
from iexfinance.stocks import Stock
from iexfinance.refdata import get_symbols
from datetime import datetime
import json

class StockInfo:
    def __init__(self,token = "sk_1427456e783248ec8841be2292d08a7d"):
        self.token = token

    def _parse_news(self,dct):
        time = str(datetime.fromtimestamp(dct['datetime']/1000))
        header = dct['headline']
        source =dct['source']
        summary =dct['summary']
        url = dct['url']
        lang = dct['lang']
        pay = dct['hasPaywall']
        return time, header,source,summary, url, lang,pay
    
    def get_news(self, tck,last):
        self.iexf = Stock(tck, token=self.token)
        data = self.iexf.get_news(last=last)
        return [self._parse_news(dct = x) for x in data]
    
    def get_info(self, tck):
        self.yf = yf.Ticker(tck)
        data = self.yf.info
        sector = data['sector']
        industry = data['industry']
        avg200 = data['twoHundredDayAverage']
        avg60 = data['fiftyDayAverage']
        cap = data['marketCap']
        return sector,industry,cap,avg200,avg60
    
    def _records(df): return df.to_records(index=False).tolist()
    
    def parse_symbols(self, output_format):
        all_tcks = get_symbols(output_format=output_format, token=self.token)
        return all_tcks

# all_tck = StockInfo().parse_symbols(output_format = 'json')


# with open('All_tickers.txt', 'w') as fh:
#     fh.write(json.dumps(all_tck))