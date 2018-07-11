# -*- coding: utf-8 -*-
# Global imports
import datetime as dt
import fxcmpy
import sys
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
            str_dt = index.strftime('%d/%m/%Y %H:%M:%S')
            k['date_time'] = "STR_TO_DATE('" + str_dt + "', '%d/%m/%Y %T')"

            k['currency_pair'] = "'" + currency_pair + "'"
            print('[INFO] Updating data : ', time_frame, k['currency_pair'], str_dt)
            query_string = """INSERT IGNORE into %s (%s) VALUES(%s)""" % (time_frame, columns, placeholders)
            # query_string = """INSERT into %s (%s) VALUES(%s)""" % (time_frame, columns, placeholders)
            query = query_string % tuple(k.values())
            try:
                self.db_conn.execute_query(query)
            except Exception as e:
                print("[INFO] Error in running query %s" % query)


    def update_all_data(self, t_f=None, c_p=None, s_date=None, e_date=None):
        """
        Gets all the currency pairs and timeframes in database and update
        the table with the latest data
        :return:
        """
        if not (c_p and t_f and s_date and e_date):
            print("[INFO] Connecting to fxcm api")
            api_conn = fxcmpy.fxcmpy(config_file=".\\fxcm.cfg", log_level='error', server='real')
            print("[INFO] Connected to fxcm api ")
            currency_pairs = self.get_currency_pairs()
            timeframes = self.get_time_frames()
            for currency_pair in currency_pairs:
                try:
                    for timeframe in timeframes:
                        try:
                            now = dt.datetime.now()
                            strt = dt.datetime(2000, 1, 1)
                            query = """select date_time from %s where currency_pair='%s' order by date_time desc limit 1""" % (timeframe, currency_pair)
                            date_ = self.db_conn.run_query(query)
                            if date_:
                                strt = date_[0]['date_time']# dt.datetime.strptime(date_[0]['date_time'], '%Y-%d-%m %H:%m:%S')

                            endd = dt.datetime(now.year, now.month, now.day)
                            try:
                                ts_data = api_conn.get_candles(currency_pair, start=strt, end=endd, period=timeframe)
                                self.update_database(currency_pair, timeframe, ts_data)
                            except Exception as e:
                                print("[ERROR] Error occured. Resetting api connection %s for %s, %s" % (e, currency_pair, timeframe))
                                try:
                                    api_conn = fxcmpy.fxcmpy(config_file=".\\fxcm.cfg", log_level='error', server='real')
                                    continue
                                except:
                                    api_conn = fxcmpy.fxcmpy(config_file=".\\fxcm.cfg", log_level='error', server='real')
                                    continue
                        except Exception as e:
                            continue
                except Exception as e:
                    continue
        else:
            print("[INFO] Connecting to fxcm api")
            api_conn = fxcmpy.fxcmpy(config_file=".\\fxcm.cfg", log_level='error', server='real')
            print("[INFO] Connected to fxcm api ")
            # s_date = dt.datetime.strptime(s_date, '%Y-%m-%d %H:%M')
            s_date = dt.datetime.strptime(s_date, '%Y-%m-%d')

            s_date = dt.datetime(s_date.year, s_date.month, s_date.day)
            #
            # e_date = dt.datetime.strptime(e_date, '%Y-%m-%d %H:%M')
            e_date = dt.datetime.strptime(e_date, '%Y-%m-%d')
            e_date = dt.datetime(e_date.year, e_date.month, e_date.day)

            print(s_date, e_date)
            if s_date > e_date:
                print("[ERROR] Input error. Start date greater than end date !!")
            else:
                try:
                    print("[INFO] Updating database for % s, %s, %s, %s" % (c_p, t_f, s_date, e_date))
                    ts_data = api_conn.get_candles(c_p, start=s_date, end=e_date, period=t_f)
                    self.update_database(c_p, t_f, ts_data)
                except Exception as e:
                    print("[ERROR] Error occured. Error in api connection %s for %s, %s" % (e, c_p, t_f))


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
        elif p_args.update:
            print(self.update_all_data(p_args.t_f, p_args.c_p, p_args.s_d, p_args.e_d))
        else:
            "print ([WARNING: Invalid arguments])"
