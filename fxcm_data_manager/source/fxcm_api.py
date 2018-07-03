# -*- coding: utf-8 -*-
# Global imports

import warnings
warnings.filterwarnings("ignore")
import sys
import datetime as dt

try:
    import fxcmpy
    from source.database import Database
except ImportError as e:
    print("[EXCEPTION] %s" % e)


class Fxcm:
    def __init__(self):
        self.db_conn = Database()

    def process_inputs(p_args):
        """Processes the command line arguments and call the required function"""
