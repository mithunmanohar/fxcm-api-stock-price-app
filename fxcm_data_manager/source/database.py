__author__ = "mithun manohar mithunmanohar79[at]gmail[dot]com"

import json
import time
import requests
import datetime
import settings
import traceback

import MySQLdb


class Database:

    def __init__(self):
        self.host = settings.host
    	self.user_name = settings.user_name
    	self.password = settings.password
    	self.db = settings.database
        self.connection = MySQLdb.connect(self.host, self.user_name,
        				  self.password, self.db)
        self.cursor = self.connection.cursor()

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print query
            print traceback.print_exc()
            self.connection.rollback()

    def update(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print query
            print traceback.print_exc()
            self.connection.rollback()


    def query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor )
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()


if __name__ == "__main__":
    db = Database()
