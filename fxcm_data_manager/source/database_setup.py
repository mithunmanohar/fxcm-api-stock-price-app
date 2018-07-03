__author__ = "samrohn77[at]gmail[dot]com"

import logging
import configparser
from database import Database

conf_parser = configparser.ConfigParser()
conf_parser.read(".\\fxcm.cfg")
database = conf_parser.get("database", "database")

def setup_new_database(db):
    try:
        create_database_query = "CREATE DATABASE IF NOT EXISTS %s" % database
        db.execute_query(create_database_query)
        print("[INFO] Database %s created" % database)
    except Exception as e:
        print("[ERROR] %s") % e

def create_currency_table(table_name):
    db = Database(database)
    query = ("""SELECT * FROM
    information_schema.tables
    WHERE
    table_name = '%s'""") % table_name.replace("`", "")
    if not db.run_query(query):
        query = """CREATE TABLE %s (id int(11) NOT NULL AUTO_INCREMENT,
        currency_pair VARCHAR(100), primary key (id))""" % table_name
        if db.execute_query(query):
            print("[INFO] Created table %s " % table_name)
        else:
            print("[INFO] Unable to create table: %s" % table_name)
    else:
        print("[INFO] Table %s exists already" % table_name)

def add_to_currency_table(table_name):
    db = Database(database)
    table_name = table_name.replace("`", "")
    query = ("""SELECT * FROM
        t_currency
        WHERE
        currency_pair = '%s'""") % table_name
    if not db.run_query(query):
        query = """INSERT INTO t_currency (currency_pair)
        VALUES ('%s')""" % table_name
        if db.execute_query(query):
            print("[INFO] Added table %s " % table_name)
        else:
            print("[INFO] Unable to add table: %s" % table_name)
    else:
        print("[INFO] Table %s already exists" % table_name)

def add_to_tf_table(table_name):
    db = Database(database)
    table_name = table_name.replace("`", "")
    query = ("""SELECT * FROM
        t_timeframes
        WHERE
        time_frame = '%s'""") % table_name
    if not db.run_query(query):
        query = """INSERT INTO t_timeframes(time_frame)
        VALUES ('%s')""" % table_name
        if db.execute_query(query):
            print("[INFO] Added time frame %s to table t_timeframes" % table_name)
        else:
            print("[INFO] Unable to time frame %s to t_timeframes: %s" % table_name)
    else:
        print("[INFO] Table %s already exists in t_timeframes" % table_name)

def create_tf_record_table(table_name):
    db = Database(database)
    query = ("""SELECT * FROM
            information_schema.tables
            WHERE
            table_name = '%s'""") % table_name
    if not db.run_query(query):
        query = """CREATE TABLE %s (
                   id int(11) NOT NULL AUTO_INCREMENT,
                   time_frame VARCHAR(100) ,
                   primary key (id)
                   )""" % table_name
        if db.execute_query(query):
            print("[INFO] Created table %s" % table_name)
        else:
            print("[INFO] Unable to create table %s" % table_name)
    else:
        print("[INFO] Table %s exists already" % table_name)


def create_tf_tables(table_name):
    db = Database(database)
    query = ("""SELECT * FROM
                information_schema.tables
                WHERE
                table_name = '%s'""") % table_name
    if not db.run_query(query):
        query = """CREATE TABLE %s (
               currency_pair VARCHAR(100),date_time DATETIME UNIQUE,bidopen float(8,3),\
               bidclose float(8,3), bidhigh float(8,3), bidlow float(8,3),\
               askopen float(8,3), askclose  float(8,3), askhigh float(8,3),\
               asklow float(8,3), tickqty int(12))""" % table_name
        if db.execute_query(query):
            print("[INFO] Created table %s" % table_name)
        else:
            print("[INFO] Unable to create table %s" % table_name)
    else:
        print("[INFO] Table already exists")

if __name__ == "__main__":
    db = Database()
    setup_new_database(db)
    create_currency_table("t_currency")
    create_tf_record_table("t_timeframes")
    time_period = ["m15", "H1", "H4", "D1", "W1", "M1"]
    for period in time_period:
        create_tf_tables(period)
        add_to_tf_table(period)

    currency_pairs = ['EUR/USD', 'XAU/USD', 'GBP/USD', 'UK100',
                       'USDOLLAR', 'XAG/USD', 'GER30', 'FRA40',
                       'USD/CNH', 'EUR/JPY', 'USD/JPY', 'GBP/JPY',
                       'AUD/JPY', 'USD/CHF', 'AUD/USD', 'EUR/CHF',
                       'EUR/GBP', 'NZD/USD', 'USD/CAD', 'US30']
    for currency_pair in currency_pairs:
        currency_pair = "`" + currency_pair + "`"
        add_to_currency_table(currency_pair)