__author__ = "mithun manohar mithunmanohar79[at]gmail[dot]com"

import json
import time
import datetime
import traceback
import MySQLdb
import configparser


class Database:

    def __init__(self, host, user_name, password, db_name=""):
        conf_parser = configparser.ConfigParser()
        conf_parser.read("..\\fxcm.cfg")
        # with open ("..\\fxcm.cfg" , 'r') as f:
        #     for each in f:
        #         print (each)
        self.host = host
        self.user_name =user_name
        self.password = password
        self.db = db_name
        if db_name:
            self.connection = MySQLdb.connect(self.host, self.user_name,
                                       self.password, self.db)
        else:
            self.connection = MySQLdb.connect(self.host, self.user_name,
                                              self.password)
        self.cursor = self.connection.cursor()

    def create(self, query):
        try:
            print ("ffffffff")
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            print (query)
            print (traceback.print_exc())
            self.connection.rollback()
            return False

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            print (query)
            print (traceback.print_exc())
            self.connection.rollback()
            return False

    def update(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            print (query)
            print (traceback.print_exc())
            self.connection.rollback()
            return False

    def query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor )
        cursor.execute(query)
        return cursor.fetchall()

    # def __del__(self):
    #     self.connection.close()


if __name__ == "__main__":
    conf_parser = configparser.ConfigParser()
    conf_parser.read("..\\fxcm.cfg")
    host = conf_parser.get("database", "host")
    user_name = conf_parser.get("database", "user_name")
    password = conf_parser.get("database", "password")
    data_base = conf_parser.get("database", "database")
    db = Database(host, user_name, password, data_base)
