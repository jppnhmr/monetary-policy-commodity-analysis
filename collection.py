import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

from database import get_country_id, get_metric_id, insert_data

# Util
def extract_data(text):
    data = []
    for line in text.splitlines():
        item = line.strip().split(',')
        data.append({'date': item[0].strip(), 'value': item[1].strip()})
    return data

def collect_boe_data():

    url = 'https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp?Travel=NIxAZxSUx&FromSeries=1&ToSeries=50&DAT=RNG&FNY=N&CSVF=TT&html.x=66&html.y=26&SeriesCodes=IUDBEDR&UsingCodes=Y&Filter=N&title=IUDBEDR&VPD=Y#'
    today = datetime.now()
    params = {
        'FD': '1',
        'FM': 'Jan',
        'FY': '2000',
        # get most up to date data
        'TD': today.strftime('%d'),
        'TM': today.strftime('%b'),
        'TY': today.strftime('%Y')
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    html = response.text
    soup = bs(html, 'html.parser')
    rows = soup.find('tbody').find_all('tr')

    data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 2:
            date_str = cells[0].text.strip() # 20 Jan 25
            value_str = cells[1].text.strip()

            date = datetime.strptime(date_str, '%d %b %y').strftime('%Y-%m-%d')
            value = float(value_str)

            data.append({'date': date, 'value': value,})

    insert_data('UK', 'policy interest rate', data)

def collect_fred_data():
    today = datetime.now().strftime('%Y-%m-%d')
    policy_interest_url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DFF&scale=left&cosd=2000-01-01&coed={today}&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily%2C%207-Day&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={today}&revision_date={today}&nd=1954-07-01'
    energy_index_url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1078&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PNRGINDEXM&scale=left&cosd=1992-01-01&coed=2025-06-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={today}&revision_date={today}&nd=2000-01-01'
    all_commodities_index_url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1078&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PALLFNFINDEXQ&scale=left&cosd=2003-01-01&coed=2025-04-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={today}&revision_date={today}&nd=2003-01-01'
    food_index_url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1078&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PFOODINDEXM&scale=left&cosd=1992-01-01&coed=2025-06-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={today}&revision_date={today}&nd=200-01-01'

    # US Interest Rates
    response = requests.get(policy_interest_url)
    insert_data('US','policy interest rate', extract_data(response.text))

    # Global Energy Index
    response = requests.get(energy_index_url)
    insert_data('NULL','global energy index', extract_data(response.text))

    # Global All Commodities Index
    response = requests.get(all_commodities_index_url)
    insert_data('NULL','global all commodities index', extract_data(response.text))

    # Global Food Index
    response = requests.get(food_index_url)
    insert_data('NULL','global food index', extract_data(response.text))

if __name__ == "__main__":
    print('----- Collecting Data: Running -----', end='\r')
    collect_boe_data()
    collect_fred_data() 
    print('----- Collecting Data: Done -----')