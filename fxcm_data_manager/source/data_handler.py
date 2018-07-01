# -*- coding: utf-8 -*-
# Global imports
import configparser
import fxcmpy
from source.database import Database
from source import fxcm_api

class Fxcm:
    def __init__(self):
        print("[INFO] Started script")
        self.db_conn = Database("fxcm")
        print("[INFO] Connected to local database ")
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

    def get_currency_pairs(self):
        query = """select currency_pair from t_currency"""
        data = self.db_conn.run_query(query)
        c_pairs = []
        for each in data:
            c_pairs.append(each["currency_pair"])
        return c_pairs

    def add_time_frame(self, time_frame):
        query = ("""SELECT * FROM
                t_timeframes
                WHERE
                time_frame = '%s'""") % time_frame
        if self.db_conn.run_query(query):
            print("[INFO] Table already exists %s" % time_frame)
        else:
            query = ("""INSERT INTO t_timeframes 
                        (time_frame) VALUES
                        ('%s')""") % time_frame
            self.db_conn.execute_query(query)
            return time_frame

    def get_time_frames(self):
        query = """select time_frame from t_timeframes"""
        data = self.db_conn.run_query(query)
        c_pairs = []
        for each in data:
            c_pairs.append(each["time_frame"])
        return c_pairs

    def update_ts_data(self, data):

        pass

    def update_all_data(self):
        """
        Gets all the currency pairs and timeframes in database and update
        the table with the latest data
        :return:
        """
        print("[INFO] Connecting to fxcm api")
        api_conn = fxcmpy.fxcmpy(config_file=".\\fxcm.cfg", log_level='error')
        print("[INFO] Connected to fxcm api ")
        currency_pairs = self.get_currency_pairs()
        timeframes = self.get_time_frames()
        for currency_pair in currency_pairs:
            for timeframe in timeframes:
                ts_data = api_conn.get_candles(currency_pair, timeframe)
                print("[INFO] Updated data for currency pair %s for time period %s") % currency_pair, timeframe
                print(ts_data)
    def reset_database(self):
        query = """DROP database fxcm"""
        self.db_conn.run_query(query)

    def process_inputs(self, p_args):
        """Processes the command line arguments and call the required function"""

        #'add_currency_pair', 'add_time_frame', 'show_currency_pairs', 'show_time_frames', 'update_all_data'

        if p_args.add_currency_pair:
            print(self.add_currency_pairs(p_args.add_currency_pair))
        elif p_args.show_currency_pairs:
            print("[INFO] Currently available currency pairs : %s" % self.get_currency_pairs())
        elif p_args.show_time_frames:
            print("[INFO] Currently available timeframes are  : %s" % self.get_time_frames())
        elif p_args.update_all:
            print("calling connect")
            print(self.update_all_data())
            print("finish connect")
        elif p_args.add_time_frame:
            print("Added timeframes : %s" % self.add_time_frame(p_args.add_time_frame))
        elif p_args.reset_all:
            self.reset_database()
            print("[INFO] Reset the data base successfully")
        else:
            "print ([WARNING: Invalid arguments])"
