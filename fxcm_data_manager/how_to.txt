After setting up the Mysql Database, run the database_setup.py file. The API credentials can be updated in fxcm.cfg file

data_manager.py -show_currency_pairs  - shows all the currency pairs in the database
data_manager.pt -show_time_frames   - shows all the timeframes in the database
data_manager.py -reset_all - Wipes out database, all the tables, data and resets to default state. Run  detabase_setup.py file to recreate the database and tables

data_manager.py --add_currency_pair	{currency pair name}  - add a new currency to the database
data_managerpy --add_time_frame {time_frame_name}  - adds a new time frame to database

data_manager.py --update_all_data - Updates all the data in the data base for all time-periods and currency pairs with latest available data

