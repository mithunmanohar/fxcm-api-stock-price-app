FXCM, also known as Forex Capital Markets, is a retail foreign exchange broker. 

*What does this code do*
This command line tool uses fxcm api to store historical stock prices to a local MySql data base. This database can be used coonect to excel using excel-MySql connector to do further analysis.

*Installation steps:*
After installing Mysql Database, run the database_setup.py file. The API credentials can be updated in fxcm.cfg file

*Usage of the command line options*

python.exe data_manager.py -show_currency_pairs  - shows all the currency pairs in the database
python.exe data_manager.pt -show_time_frames   - shows all the timeframes in the database
python.exe data_manager.py -reset_all - Wipes out database, all the tables, data and resets to default state. Run  detabase_setup.py file to recreate the database and tables

python.exe data_manager.py --add_currency_pair	{currency pair name}  - add a new currency to the database
python.exe data_managerpy --add_time_frame {time_frame_name}  - adds a new time frame to database

python.exe data_manager.py --update_all_data - Updates all the data in the data base for all time-periods and currency pairs with latest available data

Custom update:  use these methods to update individual timeframe and currency pair

one time frame one time frame : 
python.exe data_manager.py --update --t_f "m15" --c_p "EUR/USD" --s_d "2018-02-25" --e_d "2018-03-25"

one time frame, multiple currecy pair: 
python.exe data_manager.py --update --t_f "m15" --c_p "EUR/USD,XAG/USD" --s_d "2018-02-25" --e_d "2018-03-25"

multiple time frame, one currecy pair:
python.exe data_manager.py --update --t_f "m15,H4" --c_p "EUR/USD" --s_d "2018-02-25" --e_d "2018-03-25"

multiple time frame, multiple currency:
python.exe data_manager.py --update --t_f "m15,H4" --c_p "NZD/USD,GBP/USD" --s_d "2018-02-25" --e_d "2018-03-25"



