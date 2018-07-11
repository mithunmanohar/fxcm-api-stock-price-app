__author__ = "mithun manohar mithunmanohar79[at]gmail[dot]com"

import json
import time
import datetime
import traceback
import MySQLdb
import configparser


class Database:

    def __init__(self, database=None):
        conf_parser = configparser.ConfigParser()
        conf_parser.read(".\\fxcm.cfg")
        self.host = conf_parser.get("database", "host")
        self.user_name = conf_parser.get("database", "user_name")
        self.password = conf_parser.get("database", "password")
        self.db = conf_parser.get("database", "database")
        if database:
            self.connection = MySQLdb.connect(self.host, self.user_name,
                                              self.password, self.db)
        else:
            self.connection = MySQLdb.connect(self.host, self.user_name,
                                              self.password)
        self.cursor = self.connection.cursor()

    def get_con(self):
        return self.connection

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            print(query)
            print(traceback.print_exc())
            self.connection.rollback()
            return False


    def run_query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor )
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()


if __name__ == "__main__":
    db = Database()
