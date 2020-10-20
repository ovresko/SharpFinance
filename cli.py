import argparse
import json
from data.collector import Collector

class Cli:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='SharpFinance, to the moon...')
        self.setup()

        # handle download data
        if "download" in self.args.action:
            collector = Collector(self.config)
            collector.download_data()

        if "sync" in self.args.action:
            interval = self.args.interval
            collector = Collector(self.config)
            collector.background_sync(interval=interval)


    def setup(self):
        # parse args
        # Same main parser as usual
        parser =  self.parser

        subparsers = parser.add_subparsers(help='Desired action to perform', dest='action')
        parser_download = subparsers.add_parser("download", help='download data')
        parent_parser = argparse.ArgumentParser(add_help=False)
        parser_sync = subparsers.add_parser("sync", parents=[parent_parser],
                                            help='sync data')
        parser_sync.add_argument("--interval",type=int,required=1)

        parser_train = subparsers.add_parser("train", parents=[parent_parser],
                                            help='train')
        parser_train.add_argument("algorithm")
        # Add some arguments exclusively for parser_update 


        self.args = (self.parser.parse_args())

        # load config file
        with open("config.json") as json_data_file:
            self.config = json.load(json_data_file)