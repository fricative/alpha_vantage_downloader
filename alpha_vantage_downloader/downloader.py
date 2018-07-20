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
    
    if not len(logger.handlers):
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
                 output_size:str ='full'):
        self.key = key
        self.datatype = datatype
        self.output_size = output_size
        # time between each api call, be 
        # gentle to alpha vantage server :)
        self.wait_time = 1    
        self.logger = get_logger()
        
        
    def intraday(self, symbols, granularity: str) -> dict:
        """
        download intraday price
        """
        base_url = self.get_url('intraday') + "&interval=" + granularity
        return self._download(symbols, base_url)
        
        
    def daily(self, symbols) -> dict:
        """
        download daily price
        """
        base_url = self.get_url('daily')
        return self._download(symbols, base_url)
    
    
    def daily_adjusted(self, symbols) -> dict:
        """
        download daily adjusted price
        """
        base_url = self.get_url('daily_adjusted')
        return self._download(symbols, base_url)


    def weekly(self, symbols) -> dict:
        """
        download weekly price
        """
        base_url = self.get_url('weekly')
        return self._download(symbols, base_url)
    
    
    def weekly_adjusted(self, symbols) -> dict:
        """
        download weekly adjusted
        """
        base_url = self.get_url('weekly_adjusted')
        return self._download(symbols, base_url)
        
    
    def _download(self, symbols:[str], base_url: str) -> dict:
        """
        make multithreaded call to alpha vantage api to speed 
        up downloading for large number of symbols
        """
        
        data = dict()
        exception_symbols = dict()
        working_queue = list()
        
        if not isinstance(symbols, list):
            symbols = [symbols]
        
        def download(symbol, url) -> None:
            try:
                self.logger.info('Downloading %s', symbol)
                df = pd.read_csv(url)
                # alpha vantage delivers its error message via
                # returning a 2 * 1 dataframe
                if df.shape != (2, 1):
                    data[symbol] = df
                # dynamically adjust API call interval and retry
                elif "consider optimizing" in df.iloc[0, 0]:
                    symbols.append(symbol)
                    self.wait_time += .1
                    self.logger.info("""hitting API limit, adjusting waiting time to %s""", 
                                     round(self.wait_time, 1))
                else:
                    exception_symbols[symbol] = df
            except Exception as ex:
                self.logger.exception('Error occurred when downloading %s', symbol)
                error_msg = traceback.format_exc()
                self.logger.exception(error_msg)
                exception_symbols[symbol] = error_msg 
            finally:
                working_queue.remove(symbol)
                
        threads = []
        while len(symbols) or len(working_queue):
            if len(symbols):
                symbol = symbols.pop(0)
                working_queue.append(symbol)
                url = base_url + '&symbol=' + symbol
                t = threading.Thread(target=download, args=(symbol, url))
                time.sleep(self.wait_time)
                t.start()
                threads.append(t)
        
        for t in threads:
            t.join()
            
        return data, exception_symbols