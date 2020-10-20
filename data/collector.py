from datetime import datetime as dt
from data.utils import truncate, create_folder
from data.api import Client
from termcolor import colored
import csv
import os
import threading

""" Some erroirs still exists """
class Collector():
    def __init__(self,config):        
        self.config = config
        self.timeframe = self.config['timeframe']
        self.symbol = self.config['symbol']
        self.symbol_factor = self.config['symbol_factor']
        self.symbol_truncate = int(self.config['symbol_truncate'])
        self.ohcl_folder = self.config['ohcl_folder']

    def trunc(self,price):
        return truncate(price,decimals=self.symbol_truncate)

    def background_sync(self,interval: int):
        print(colored(f"Starting to sync data every {interval} minutes","green"))
        t = threading.Thread(name='sync data  procs', target=blocker)
        t.setDaemon(True)
        t.start()

        # Prove that we passed through the blocking call
        print("Started")

    def parse_intervals(self):
        start = dt.today()
        if "month" == self.config['interval']:
            start = dt(start.year , start.month- self.config['period'], start.day)
        elif "year" == self.config['interval']:
            start = dt(start.year - self.config['period'], start.month, start.day)
        elif "day" == self.config['interval']:
            start = dt(start.year , start.month, start.day- self.config['period'])

        return start

    def get_data(self):
        ulr = f'data/{self.symbol}_{self.timeframe}'
        df = pd.read_csv(ulr,skiprows=0,names=['open','close','high','low','volume','date'],delimiter=";")
        df["date"] = pd.to_datetime(df["date"])
        df.dropna()
        return df

    def download_batch(self,interval):
        end = dt.today()
        start = dt(end.year , end.month, end.day,hour=end.hour,minute=end.minute-interval)


    def download_data(self,interval=None,period=None):
        create_folder(self.ohcl_folder)
        start =self.parse_intervals()
        date_end = start
        date_start = start
        client = Client()
        interval = self.config['interval'] if not interval else interval
        period = self.config['period'] if not period else period
        try:
            client.login(self.config['xtb_user'], self.config['xtb_pwd'], mode="demo")

            for i in range(period):
                if "month" == interval:
                    date_start= dt(start.year , start.month+ i, start.day)
                    date_end = dt(date_start.year , date_start.month+ 1, date_start.day)
                elif "year" == interval:
                    date_start= dt(start.year + i, start.month, start.day)
                    date_end = dt(date_start.year + 1, date_start.month, date_start.day)
                elif "day" == interval:
                    date_start= dt(start.year, start.month, start.day)
                    date_end = dt(date_start.year , date_start.month, date_start.day + 1)
                elif "minute" == interval:
                    date_start= dt(start.year + i, start.month, start.day)
                    date_end = dt(date_start.year , date_start.month, date_start.day + 1)
                
                print(f"downloading {self.symbol} from {date_start} to {date_end}")
                
                history  =client.get_chart_range_request(self.symbol, self.timeframe, date_start.timestamp(), date_end.timestamp(), 0)
                with open(f'data/{self.symbol}_{self.timeframe}', 'a+', newline='') as csvfile:
                    for h4 in history['rateInfos']:
                        writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        popen = float(h4['open']) / self.symbol_factor
                        close = popen + float(h4['close']) / self.symbol_factor
                        high = popen+ float(h4['high']) / self.symbol_factor
                        low= popen+ float(h4['low']) / self.symbol_factor
                        volume = float(h4['vol'])
                        writer.writerow([self.trunc(popen), self.trunc(close), self.trunc(high), self.trunc(low), volume, h4['ctmString']   ])

            print(colored(f"Done downloading timeframe {self.timeframe} {len(history)} periods...", "green"))

        except Exception as e:
            print(f"{e}")
            return False

