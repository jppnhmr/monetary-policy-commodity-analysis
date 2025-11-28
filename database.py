import sqlite3
from typing import List, Dict

def connect():
    return sqlite3.connect('finance_data.db')

# SETUP #
def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            country_id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_code TEXT NOT NULL,
            country_name TEXT NOT NULL,
            currency_code TEXT NOT NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT NOT NULL,
            unit TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS sources (
            source_id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_id INTEGER NOT NULL,
            metric_id INTEGER NOT NULL,
            source_name TEXT NOT NULL,
            source_url TEXT,
            FOREIGN KEY(country_id) REFERENCES countries(country_id)
            FOREIGN KEY(metric_id) REFERENCES metrics(metric_id)
            UNIQUE(country_id, metric_id)
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS data_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_id INTEGER,
            metric_id INTEGER NOT NULL,
            date DATE NOT NULL,
            value FLOAT NOT NULL,
            FOREIGN KEY(country_id) REFERENCES countries(country_id)
            FOREIGN KEY(metric_id) REFERENCES metrics(metric_id)
            UNIQUE(country_id, metric_id, date)
        )
    ''')

    conn.commit()
    conn.close()

def add_country(country_code, country_name, currency_code):
    conn = connect()
    cur = conn.cursor()
    cur.execute(f'''
        INSERT OR IGNORE INTO countries (country_code, country_name, currency_code)
        VALUES ('{country_code}', 
                '{country_name}', 
                '{currency_code}')    
    ''')
    conn.commit()
    conn.close()

def add_countries():
    add_country('UK', 'United Kingdom', 'GBP')
    add_country('US', 'United States',  'USD')

def add_metric(metric_name, unit):
    conn = connect()
    cur = conn.cursor()

    cur.execute(f'''
        INSERT OR IGNORE INTO metrics (metric_name, unit)
        VALUES ('{metric_name}',
                '{unit}')
    ''')

    conn.commit()
    conn.close()

def add_metrics():
    add_metric('policy interest rate', '%')
    add_metric('global energy index', '')
    add_metric('global all commodities index', '')
    add_metric('global food index', '')

def add_source(country_code, metric_id, source_name, source_url):

    country_id = get_country_id(country_code)
    conn = connect()
    cur = conn.cursor()

    cur.execute('''
        INSERT OR IGNORE INTO sources (country_id, metric_id, source_name, source_url)
        VALUES (?, ?, ?, ?)
    ''', (country_id, metric_id, source_name, source_url,))

    conn.commit()
    conn.close()

def add_sources():
    add_source('UK', 'policy interest rate', 'Bank of England', 'https://www.bankofengland.co.uk/boeapps/database/')
    add_source('US', 'policy interest rate', 'Federal Reserve Bank of St.Louis', 'https://fred.stlouisfed.org/series/DFF')
    add_source('NULL', 'global energy index', 'Federal Reserve Bank of St.Louis', 'https://fred.stlouisfed.org/series/DFF')
    add_source('NULL', 'global all commodities index', 'Federal Reserve Bank of St.Louis', 'https://fred.stlouisfed.org/series/DFF')
    add_source('NULL', 'global food index', 'Federal Reserve Bank of St.Louis', 'https://fred.stlouisfed.org/series/DFF')

# USE #
def insert_data(country_code, metric_name, data: List[Dict]):

    country_id = get_country_id(country_code)
    metric_id = get_metric_id(metric_name)

    conn = connect()
    cur = conn.cursor()

    for record in data:
        cur.execute('''
            INSERT OR IGNORE INTO data_points (country_id, metric_id, date, value)
            VALUES (?, ?, ?, ?)
        ''', 
        (country_id, metric_id, record['date'], record['value']))

    conn.commit()
    conn.close()

def get_country_id(country_code):

    if country_code == 'NULL':
        return 'NULL'

    conn = connect()
    cur = conn.cursor()

    cur.execute('''
        SELECT country_id FROM countries
        WHERE country_code = ?
    ''', (country_code,))

    id = cur.fetchone()[0]
    conn.close()
    return id

def get_metric_id(metric_name):
    conn = connect()
    cur = conn.cursor()

    cur.execute('''
        SELECT metric_id FROM metrics
        WHERE metric_name = ?
    ''', (metric_name,))

    id = cur.fetchone()[0]
    conn.close()
    return id

if __name__ == '__main__':

    print('----- Database Setup -----', end='\r')
    # create
    create_tables()
    # populate
    add_countries()
    add_metrics()
    add_sources()
    print('----- Database Setup: Done -----')