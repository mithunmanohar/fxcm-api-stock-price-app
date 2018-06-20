# -*- coding: utf-8 -*-
from source import database
from source import fxcm_api
class Fxcm:

    def __init__(self):
        self.api_conn =
        self.db_conn =
        self.currency_pairs =
def process_inputs(p_args):
    """Processes the command line arguments and call the required function"""

    #'add_currency_pair', 'add_time_frame', 'show_currency_pairs', 'show_time_frames', 'update_all_data'

    if p_args.add_currency_pair:
