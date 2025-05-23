# Code for ETL operations on Country-GDP data

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import sqlite3

url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = 'data/Countries_by_GDP.csv'
table_attribs = ['Country', 'GDP_USD_millions']
log_path = 'data/etl_project_log.txt'


def extract(url, table_attribs):
    ''' This function extracts the required
    information from the website and saves it to a dataframe. The
    function returns the dataframe for further processing. '''

    df = pd.DataFrame(columns=table_attribs)
    html_text = requests.get(url).text

    data = BeautifulSoup(html_text, 'html.parser')
    t_body = data.find_all('tbody')
    rows = t_body[2].find_all('tr')

    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            first_td = col[0]
            third_td = col[2]
            if first_td.find('a', href=True) and  '—' not in third_td:
                data_dict = {
                    'Country': first_td.a.contents[0],
                    'GDP_USD_millions': third_td.contents[0]
                }
                df = pd.concat([df, pd.DataFrame(data_dict, index=[0])], ignore_index=True)

    return df

def transform(df):
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''

    df['GDP_USD_millions'] = df['GDP_USD_millions'].apply(lambda x: float("".join(x.split(','))))
    df['GDP_USD_millions'] = np.round((df['GDP_USD_millions']/1000), 2)
    df.columns = df.columns.map(lambda col_name: col_name.replace('GDP_USD_millions', 'GDP_USD_billions'))    

    return df


def load_to_csv(df, csv_path):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''

    df.to_csv(csv_path)


def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''

    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
    


def run_query(query_statement, sql_connection):
    ''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''

    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)



def log_progress(message):
    ''' This function logs the mentioned message at a given stage of the code 
    execution to a log file. Function returns nothing'''

    timestamp_format = '%Y-%h-%d-%H:%M%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_path, 'a') as f:
        f.write(timestamp + ',' + message + '\n')



log_progress('Preliminaries complete. Initiating ETL process')
df = extract(url, table_attribs)

log_progress('Data extraction complete. Initiating Transformation process')
df = transform(df)

log_progress('Data transformation complete. Initiating loading process')
load_to_csv(df, csv_path)

log_progress('Data saved to CSV file')
sql_connection = sqlite3.connect(db_name)

log_progress('SQL Connection initiated.')
load_to_db(df, sql_connection, table_name)

log_progress('Data loaded to Database as table. Running the query')
query_statement = f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
run_query(query_statement, sql_connection)

log_progress('Process Complete.')
sql_connection.close()