import matplotlib.pyplot as plt
import pandas as pd

from typing import List

import database as db

# Make a graph of List[(x_values, y_values)]
def plot_data(data: List[tuple]):
    df = pd.DataFrame(data).rename(columns={0: 'date', 1: 'value'})

    df.plot(kind='line', x='date', y='value')
    plt.axes
    plt.ylabel = 'value'
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
    plot_data(data)

    print('##### Done #####')

if __name__ == "__main__":
    cli_plot_data()