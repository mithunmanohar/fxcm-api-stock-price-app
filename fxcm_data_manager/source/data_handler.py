# -*- coding: utf-8 -*-
# Global imports
import configparser

from source.database import Database
from source import fxcm_api



class Fxcm:
    def __init__(self):
        self.api_conn = ""
        self.db_conn = Database("fxcm")
        self.currency_pairs = ""

    def add_currency_pairs(self, currency_pair):
        query = """select * from t_currency where currency_pair = '%s' """ % currency_pair
        data = self.db_conn.run_query(query)
        if data:
            return "[INFO] The currency pair %s already exist in database." % currency_pair
        query = """INSERT into t_currency (currency_pair)
                    VALUES ('%s')""" % currency_pair
        if self.db_conn.execute_query(query):
            return "[INFO] Inserted currency pair %s to database" % currency_pair
        else:
            return "[ERROR] Unable to insert currency pair %s to database" % currency_pair

    def show_currency_pairs(self):
        query = """select currency_pair from t_currency"""
        data = self.db_conn.run_query(query)
        c_pairs = []
        for each in data:
            c_pairs.append(each["currency_pair"])
        return c_pairs

    def show_time_frames(self):
        query = """select time_frame from t_timeframes"""
        data = self.db_conn.run_query(query)
        c_pairs = []
        for each in data:
            c_pairs.append(each["time_frame"])
        return c_pairs

    def update_all_data(self):
        pass

    def add_time_frame(self):
        pass



    def process_inputs(self, p_args):
        """Processes the command line arguments and call the required function"""

        #'add_currency_pair', 'add_time_frame', 'show_currency_pairs', 'show_time_frames', 'update_all_data'

        if p_args.add_currency_pair:
            print(self.add_currency_pairs(p_args.add_currency_pair))
        elif p_args.show_currency_pairs:
            print("Currently available currency pairs : %s" % self.show_currency_pairs())
        elif p_args.show_timeframes:
            print("Currently available timeframes are  : %s" % self.show_time_frames())
        elif p_args.update_all_data:
            print()
        else:
            "print ([WARNING: Invalid arguments])"
