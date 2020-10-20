import csv
import pandas as pd
from collector import Collector
from datetime import datetime as dt
from ta.utils import dropna
from data.features import Features


class Streamer:
    def __init__(self,config,update = False):
        self.df = pd.DataFrame()
        if update:
            cll = Collector(config)
            cll.download_data()
        self.config = config
        self.symbol = self.config['symbol']
        self.timeframe = self.config['timeframe']
        self.all_candles = []
        self.pull_data()
        
        

    def pull_data(self):            
        with open(f'data/{self.symbol}_{self.timeframe}', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                #print(row)
                candle = {
                    "open":float(row[0]),
                    "close":float(row[1]),
                    "high":float(row[2]),
                    "low":float(row[3]),
                    "time": row[4]
                    }
                self.all_candles.append(candle)
        self.df = pd.DataFrame(self.all_candles)
        self.df = dropna(self.df)
        self.add_features()

    def add_features(self):        
        if df.empty:
            raise Exception("empty data in stream")

        features = self.config['features']
        self.df = Features(self.df,features).fill_features()
        

    def next(self,window=1):
        return self.all_candles[self.current_step]

    def prev(self):
        raise NotImplementedError()

    def reset(self):
        self.current_step = 0

    def count(self):
        raise NotImplementedError()
