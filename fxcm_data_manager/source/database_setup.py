__author__ = "mithun manohar mithunmanohar79[at]gmail[dot]com"

import logging
import configparser
from database import Database

log = logging.getLogger("my-logger")
log.info("Hello, world")

conf_parser = configparser.ConfigParser()
conf_parser.read(".\\fxcm.cfg")
database = conf_parser.get("database", "database")
print(database)

def setup_new_database(db):
    try:
        create_database_query = "CREATE DATABASE IF NOT EXISTS %s" % database
        db.execute_query(create_database_query)
        print("[INFO] Database %s created" % database)
    except Exception as e:
        print ("[INFO] %s") % e

def create_currency_table(table_name):
    db = Database(database)
    query = ("""SELECT * FROM
    information_schema.tables
    WHERE
    table_name = '%s'""") % table_name
    if not db.execute_query(query):
        query = """CREATE TABLE %s (
           id int(11) NOT NULL AUTO_INCREMENT,
           currency_pair VARCHAR(100),
           primary key (id)
           )""" % table_name
        if db.execute_query(query):
            print("[INFO] Created table " % table_name)
        else:
            print("[INFO] Unable to create table " % table_name)
    else:
        print("[INFO] Table %s exists already" % table_name)


def create_tf_record_table(table_name):
    db = Database(database)
    query = ("""SELECT * FROM
            information_schema.tables
            WHERE
            table_name = '%s'""") % table_name
    if not db.run_query(query):
        query = """CREATE TABLE %s (
                   id int(11) NOT NULL AUTO_INCREMENT,
                   time_frame VARCHAR(100),
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
               currency_pair VARCHAR(100),date_time DATETIME,bidopen float(8,3),\
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