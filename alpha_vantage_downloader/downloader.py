# -*- coding: utf-8 -*-

import logging
import sys
import threading
import time
import traceback

import pandas as pd

from alpha_vantage_downloader.config import api_map


def get_logger():
    logger = logging.getLogger('AlphaVantage Downloader')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


class downloader():
    
  
    
    def get_url(self, periodicity):
        config = '&apikey=' + self.key + '&datatype=' + self.datatype \
                    + '&outputsize=' + self.output_size
        return api_map[periodicity] + config
    
    
    def __init__(self, key: str, datatype: str='csv', 
                 output_size:str ='full', wait_time:float = 2.0):
        self.key = key
        self.datatype = datatype
        self.output_size = output_size
        # time between each api call, be gentle to alpha vantage server :)
        self.wait_time = wait_time    
        self.data = {key: {} for key in api_map.keys()}
        self.logger = get_logger()
        
        
    def intraday(self, symbols, granularity: str) -> dict:
        """
        download intraday price
        """
        base_url = self.get_url('intraday') + "&interval=" + granularity
        return self._download(symbols, base_url, 'intraday')
        
        
    def daily(self, symbols) -> dict:
        """
        download daily price
        """
        base_url = self.get_url('daily')
        return self._download(symbols, base_url, 'daily')
    
    
    def daily_adjusted(self, symbols) -> dict:
        """
        download daily adjusted price
        """
        base_url = self.get_url('daily_adjusted')
        return self._download(symbols, base_url, 'daily_adjusted')


    def weekly(self, symbols) -> dict:
        """
        download weekly price
        """
        base_url = self.get_url('weekly')
        return self._download(symbols, base_url, 'weekly')
    
    
    def weekly_adjusted(self, symbols) -> dict:
        """
        download weekly adjusted
        """
        base_url = self.get_url('weekly_adjusted')
        return self._download(symbols, base_url, 'weekly_adjusted')
        
    
    def _download(self, symbols:[str], base_url: str, caller: str) -> dict:
        """
        make multithreaded call to alpha vantage api to speed up downloading for 
        large number of symbols
        """
        
        if not isinstance(symbols, list):
            symbols = [symbols]
        
        def download(symbol, url, caller) -> None:
            try:
                self.logger.info('Downloading %s', symbol)
                df = pd.read_csv(url)
                self.data[caller].update({symbol: df})
            except Exception as ex:
                self.logger.exception('Error occurred when downloading %s', symbol)
                self.logger.exception(traceback.format_exc())
                self.data[caller].update({symbol: str(ex)})
                
        threads = []
        for symbol in symbols:
            url = base_url + '&symbol=' + symbol
            t = threading.Thread(target=download, args=(symbol, url, caller))
            time.sleep(self.wait_time)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        return self.data[caller]
    
