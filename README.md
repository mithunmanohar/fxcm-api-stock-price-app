# fxcm-api-stock-price-app

FXCM, also known as Forex Capital Markets, is a retail foreign exchange broker. This A python fxcm api wrapper that connects to fxcm api and stores data in a local mysql data base. This database can be used coonect to excel using excel-MySql connector to do further analysis.

# Environment setup

After installing Mysql Database, run the database_setup.py file. This creates the required tables in database for the tool to run. The API credentials can be updated in fxcm.cfg file

#Usage of the command line options

- TO show all the currency pairs in the database

  python.exe data_manager.py -show_currency_pairs  - 

- To show all the timeframes in the database

  python.exe data_manager.pt -show_time_frames

- Reset database, all the tables, data and resets to default state. Sets everything to default state!

  python.exe data_manager.py -reset_all

Re-run  detabase_setup.py file to recreate the database and tables

- To add a new currency to the database

  python.exe data_manager.py --add_currency_pair	{currency pair name}
  
- To add a  new time frame to database

  python.exe data_managerpy --add_time_frame {time_frame_name}

- Update all data for all time frames and currency pairs

  python.exe data_manager.py --update_all_data 

Custom updates:  
Use these methods to update individual timeframe and currency pair

- To update one time frame one time frame : 

  python.exe data_manager.py --update --t_f "m15" --c_p "EUR/USD" --s_d "2018-02-25" --e_d "2018-03-25"

- To update one time frame, multiple currecy pair: 

  python.exe data_manager.py --update --t_f "m15" --c_p "EUR/USD,XAG/USD" --s_d "2018-02-25" --e_d "2018-03-25"

- To update  multiple time frame, one currecy pair:

  python.exe data_manager.py --update --t_f "m15,H4" --c_p "EUR/USD" --s_d "2018-02-25" --e_d "2018-03-25"

- To update multiple time frame, multiple currency:

  python.exe data_manager.py --update --t_f "m15,H4" --c_p "NZD/USD,GBP/USD" --s_d "2018-02-25" --e_d "2018-03-25"


Requirements:

- Python version : 3.x (tested on python3.5)

- fxcm api : pip install fxcmpy

- MySql python connector : pip install MySQL-python
