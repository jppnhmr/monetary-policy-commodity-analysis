import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import Cursor
import pandas as pd
import numpy as np
from datetime import datetime

from typing import List

import database as db

# Make a graph of List[(x_values, y_values)]
def plot_data(data: List[tuple], title, y_axis):
    dates = []
    values = []
    for d in data:
        dates.append(datetime.strptime(d[0],'%Y-%m-%d'))
        values.append(d[1])

    fig, ax = plt.subplots()
    ax.plot(dates, values)
    ax.grid(True)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.ylabel = y_axis
    plt.xlabel = 'date'
    plt.show()

def cli_plot_data():
    print('##### Plot Data #####')

    # Choose Metric
    metrics = [m[0] for m in db.get_metrics()]
    print('Metric Options')
    for metric in metrics:
        print(f' {metric}')
    metric = None

    while metric not in metrics:
        metric = input('Type the metric you want to plot.\n>>')
    print(f' - Selected: {metric} - ')
    is_global = 'global' in str(metric)

    if not is_global:
        # Choose Country
        countires = db.get_countires()
        country_codes = []
        print('Country Options')
        for country_code, country_name in countires:
            country_codes.append(country_code)
            print(f' {country_name} - {country_code}')
        country = None
        while country not in country_codes:
            country = input('Type the country code you want to plot.\n>>')
        print(f' - Selected: {country} - ')

    # Get data from database
    if is_global and metric != None:
        data = db.get_data_global_metric(
            db.get_metric_id(metric))
    else:
        data = db.get_data_country_metric(
            db.get_country_id(country), 
            db.get_metric_id(metric))
        
    # Plot Data
    title = f'{metric}' if is_global else f"{country} {metric}"
    plot_data(data, title, y_axis=metric)

    print('##### Done #####')

if __name__ == "__main__":
    cli_plot_data()