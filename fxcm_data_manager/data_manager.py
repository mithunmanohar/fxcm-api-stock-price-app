# -*- coding: utf-8 -*-
__author__ = "samrohn77[at]gmail[dot]com"

"""
A command line interface for managing fxcm mysql data base
"""

import sys
import argparse
import logging
from source.data_handler import Fxcm



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A command line utility to\
                                      pull fxcm api data to mysql database')

    parser.add_argument("-show_currency_pairs", action="store_true",
                        help="shows all the currency pairs in database")        # if  -show_currency_pairs is used, a True flag is set

    parser.add_argument("-show_time_frames", action="store_true",
                        help="shows all the available time frames in database")

    parser.add_argument("--update_all", action="store_true",
                        help="updates the database with latest data for all\
                        the currency pairs for all the time frames")

    parser.add_argument("--add_currency_pair",
                        help="adds a new currency pair to database. eg usage:\
                        data_manager.py --add_currency_pair USD/EUR\n")

    parser.add_argument("--add_time_frame",
                        help="adds a new time frame to database. eg usage:\
                        data_manager.py --add_time_frame D1")
    parser.add_argument("-reset_all", action="store_true",
                        help="resets the entire database\
                        data_manager.py -reset_all")
    cmd_line_args = parser.parse_args()
    data_handler = Fxcm()

    data_handler.process_inputs(cmd_line_args)
    # sys.exit(0)