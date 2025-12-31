import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import Cursor
from matplotlib.ticker import MaxNLocator, LinearLocator
import pandas as pd
import numpy as np
from datetime import datetime

from typing import List, Dict, Optional

import src.database as db

# Data Gathering #
def get_pir_datas():
    metric = 'policy interest rate'
    pir_datas = []

    pir_datas.append(db.get_data_country_metric(
        db.get_country_id('US'),
        db.get_metric_id(metric)))
    pir_datas.append(db.get_data_country_metric(
        db.get_country_id('UK'),
        db.get_metric_id(metric)))
    
    return pir_datas

def get_idx_datas():
    idx_datas = []

    idx_datas.append(db.get_data_global_metric(db.get_metric_id('global food index')))
    idx_datas.append(db.get_data_global_metric(db.get_metric_id('global energy index')))
    idx_datas.append(db.get_data_global_metric(db.get_metric_id('global all commodities index')))

    return idx_datas

def get_all_datas() -> Dict[str, pd.Series]:

    datas = {
        'Food': db.get_series('global food index'),
        'Energy': db.get_series('global energy index'),
        'All Commodities': db.get_series('global all commodities index'), 
        'US': db.get_series('policy interest rate', 'US'),
        'UK': db.get_series('policy interest rate', 'UK'),
    }

    return datas

# Data Handling #
def data_to_lines(datas: List[List[tuple]]):
    lines = []
    for data in datas:
        line = []
        for row in data:
            date = datetime.strptime(row[0],'%Y-%m-%d')
            value = row[1]
            line.append((date, value))
        lines.append(line)
    return lines

# Plotting #
def plot_data(data: List[tuple], title, y_axis, y_unit):
    dates = []
    values = []
    for d in data:
        dates.append(datetime.strptime(d[0],'%Y-%m-%d'))
        values.append(d[1])

    fig, ax = plt.subplots()
    ax.plot(dates, values)
    ax.grid(True)

    # Major tick per year, Minor tick per month
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))

    # Minor ticks evenly spaced
    y_min, y_max = np.min(values), np.max(values)
    ax.set_ylim(y_min, y_max)
    ax.yaxis.set_major_locator(MaxNLocator(nbins='auto',steps=[10]))

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.ylabel(y_axis)
    plt.xlabel('date')

    plt.title(title)
    plt.show()

def plot_multi_data(datas: List[List[tuple]], title, y_axis, y_unit):
    
    lines = []
    for data in datas:
        line = []
        for row in data:
            date = datetime.strptime(row[0],'%Y-%m-%d')
            value = row[1]
            line.append((date,value))
        lines.append(line)

    fig, ax = plt.subplots(figsize=(10,6))
    for line in lines:
        dates = [point[0] for point in line]
        values = [point[1] for point in line]
        ax.plot(dates, values)
    ax.grid(True)

    # Major tick per year, Minor tick per month
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))

    # Minor ticks evenly spaced
    all_values = [point[1] for line in lines for point in line]
    y_min = np.min(all_values)
    y_max = np.max(all_values)
    ax.set_ylim(y_min, y_max)
    ax.yaxis.set_major_locator(MaxNLocator(nbins='auto',steps=[5]))

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.ylabel(y_axis)
    plt.xlabel('date')

    plt.title(title)
    plt.show()

def plot_interest_against_index(pir_datas: List[List[tuple]], 
                                idx_datas: List[List[tuple]]):
    
    pir_lines = data_to_lines(pir_datas)
    idx_lines = data_to_lines(idx_datas)

    fig, ax1 = plt.subplots(figsize=(10,6))
    for line in pir_lines:
        dates = [point[0] for point in line]
        values = [point[1] for point in line]
        ax1.plot(dates, values, label='interest rate', color='blue')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Interest Rate (%)', color='tab:blue')
    
    ax2 = ax1.twinx()
    for line in idx_lines:
        dates = [point[0] for point in line]
        values = [point[1] for point in line]
        ax2.plot(dates, values, label='index', color='red')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Index Values', color='tab:red')

    plt.title('Interest Rates vs Indices')
    ax1.grid(True, which='major', axis='x', alpha=0.3)

    plt.show()

def plot_datas(datas: Dict[str,pd.Series], 
            pir_cols: List[str], idx_cols: List[str],
            v_shading: Optional[List[tuple]] = None):

    fig, ax1 = plt.subplots(figsize=(10,6))
    ax2 = ax1.twinx()

    idx_colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(idx_cols)))
    pir_colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(pir_cols)))

    elements = []

    for i, col in enumerate(idx_cols):
        ln = ax2.plot(datas[col].index, datas[col], label=col+' Index', color=idx_colors[i])
        elements += ln   

    for i, col in enumerate(pir_cols):
        ln = ax1.plot(datas[col].index, datas[col], label=col+' Interest Rate', color=pir_colors[i])
        elements += ln

    if v_shading:
        for start, end, label in v_shading:
            patch = ax1.axvspan(pd.to_datetime(start), pd.to_datetime(end),
                        color='gray', alpha=0.2, label=label)
            elements.append(patch)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Interest Rate (%)', color='tab:blue', fontweight='bold')
    ax2.set_ylabel('Index Values', color='tab:red', fontweight='bold')
    plt.title('Policy Interest Rates vs Indices',fontsize=14)

    labs = [l.get_label() for l in elements]
    ax1.legend(elements, labs, loc='upper left', frameon=True, fontsize='small')

    ax1.grid(True, which='major', axis='both', alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.setp(ax1.get_xticklabels(), rotation=45)

    plt.tight_layout()
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
    m_unit = db.get_metric_unit(metric)

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
    plot_data(data, title, y_axis=metric, y_unit=m_unit)

    print('##### Done #####')

def plot_rolling_corr(datas: Dict[str, pd.Series], window: int, pir: str, idx: str):
    rolling_corr = datas[pir].rolling(window=window).corr(datas[idx])

    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(rolling_corr,color='purple')
    ax.set_title(f"{window}-Month Rolling Correlation: {pir} Rates vs {idx} Index")
    ax.set_ylim([-1.1,1.1])
    ax.axhline(0, color='black', linestyle='--')

    plt.show()


# Analysis #
def analysis():
    datas = get_all_datas()

    # Downsample to Monthly data points
    for col in ['UK','US']:
        # Ensure index is datetime object
        datas[col].index = pd.to_datetime(datas[col].index)

        #Forward fill incase of missing values
        daily_series = datas[col].resample('D').ffill()

        # Resample to Month Start
        datas[col] = daily_series.resample('MS').mean()

    # Forward sample All Commodities (from quaterly to monthly)
    datas['All Commodities'] = datas['All Commodities'].resample('MS').ffill()

    # Vertical Shading for recessions.
    recessions = [
        ('2007-12-01', '2009-06-01', 'Great Recession'),
        ('2020-02-01', '2020-04-01', 'COVID-19')
    ]

    plot_datas(
        datas = datas, 
        pir_cols = ['UK','US'], 
        idx_cols = ['Food', 'Energy', 'All Commodities'],
        v_shading= recessions
    )

    plot_rolling_corr(datas, 36, 'US', 'Energy')
    plot_rolling_corr(datas, 36, 'US', 'Food')
    plot_rolling_corr(datas, 36, 'US', 'All Commodities')


if __name__ == "__main__":
    cli_plot_data()