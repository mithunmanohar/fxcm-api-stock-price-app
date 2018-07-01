# -*- coding: utf-8 -*-
# Global imports

import warnings
warnings.filterwarnings("ignore")
import sys
import datetime as dt

try:
    import fxcmpy
    from source.database import Database
except ImportError as e:
    print("[EXCEPTION] %s" % e)


class Fxcm:
    def __init__(self):

        #self.api_conn = fxcmpy.fxcmpy(config_file='..\\fxcm.cfg', server='demo')
        #print (self.api_conn.get_candles('GBP/JPY', period='D1',start= dt.datetime(2016, 1, 1),end = dt.datetime(2018, 6, 10)))
        self.db_conn = Database()
        #self.currency_pairs =

    def process_inputs(p_args):
        """Processes the command line arguments and call the required function"""

        #'add_currency_pair', 'add_time_frame', 'show_currency_pairs', 'show_time_frames', 'update_all_data'

        #if p_args.add_currency_pair:

