__author__ = "mithun manohar mithunmanohar79[at]gmail[dot]com"

import logging
import configparser
from database import Database

log = logging.getLogger("my-logger")
log.info("Hello, world")


def setup_new_database():
    conf_parser = configparser.ConfigParser()
    conf_parser.read("..\\fxcm.cfg")
    host = conf_parser.get("database", "host")
    user_name = conf_parser.get("database", "user_name")
    password = conf_parser.get("database", "password")
    db = Database(host, user_name, password)

    database = conf_parser.get("database", "database")
    create_database_query = "CREATE DATABASE %s" % database
    db.create(create_database_query)

if __name__ == "__main__":
    db = setup_new_database()
