# -*- coding: utf-8 -*-
# Global imports
import configparser
import datetime as dt
import fxcmpy
import sys
sys.path.insert(0, r"F:\usefuk\fiverr\june 2018\campito\fxcm-api-stock-price-database\fxcm_data_manager")
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

    def update_database(self, currency_pair, time_frame, ts_data):
        data = ts_data
        placeholders = ', '.join(['%s'] * len(data.keys()))
        placeholders = "%s, %s, " + placeholders
        columns = ', '.join(data.keys())
        columns = columns + ", date_time, currency_pair"
        for index, row in data.iterrows():
            k = dict(row)
            str_dt = index.strftime('%d-%m-%Y %H:%m:%S')
            k['date_time'] = "STR_TO_DATE('" + str_dt + "', '%d-%m-%Y %H:%m:%S')"
            k['currency_pair'] = "'" + currency_pair + "'"
            print('[INFO] Updating data : ', time_frame, k['currency_pair'], str_dt )
            query_string = """INSERT IGNORE into %s (%s) VALUES(%s)""" % (time_frame, columns, placeholders)
            query = query_string % tuple(k.values())
            self.db_conn.execute_query(query)

        # for each in data:
        #     print(each)

        # k = zip(data.values())
        # for each in data:
        #     print(each)
        #     placeholders = ', '.join(['%s'] * len(each))
        #     columns = ', '.join(each.keys())
        #     print(placeholders, columns)
        #     break
        # # for each in ts_data:
        # ts_data.insert(0, "currency_pair", currency_pair)
        # ts_data.strftime('%m/%d/%Y')
        # from sqlalchemy import create_engine
        # try:
        #     con = create_engine("mysql://root:admin@localhost:3306/fxcm")# + time_frame
        #
        #     ts_data.to_sql(time_frame, con, if_exists='append'  )
        # except:
        #     import traceback
        #     print(traceback.print_exc())
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
                now = dt.datetime.now()
                strt = dt.datetime(2018, 1, 1)
                query = """select date_time from %s where currency_pair='%s' order by date_time desc limit 1""" % (timeframe, currency_pair)
                date_ = self.db_conn.run_query(query)
                if date_:
                    strt = date_[0]['date_time']# dt.datetime.strptime(date_[0]['date_time'], '%Y-%d-%m %H:%m:%S')

                endd = dt.datetime(now.year, now.month, now.day)
                ts_data = api_conn.get_candles(currency_pair, start=strt, end=endd, period=timeframe)
                self.update_database(currency_pair, timeframe, ts_data)


    def reset_database(self):
        query = """DROP database fxcm"""
        self.db_conn.run_query(query)

    def process_inputs(self, p_args):
        """Processes the command line arguments and call the required function"""

        if p_args.add_currency_pair:
            print(self.add_currency_pairs(p_args.add_currency_pair))
        elif p_args.show_currency_pairs:
            print("[INFO] Currently available currency pairs : %s" % self.get_currency_pairs())
        elif p_args.show_time_frames:
            print("[INFO] Currently available timeframes are  : %s" % self.get_time_frames())
        elif p_args.update_all:
            print(self.update_all_data())
        elif p_args.add_time_frame:
            print("[INFO] Added timeframes : %s" % self.add_time_frame(p_args.add_time_frame))
        elif p_args.reset_all:
            self.reset_database()
            print("[INFO] Reset the data base successfully")
        else:
            "print ([WARNING: Invalid arguments])"

# l = Fxcm().update_all_data()