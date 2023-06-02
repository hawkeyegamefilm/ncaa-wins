import csv

import requests
from bs4 import BeautifulSoup

# static header for the files because I'm too lazy to parse the table for them
headers = ['team', 'conference', 'w-l', 'fpi', 'fpi_rank','fpi_trend', 'proj_w-l', 'win_out_perc', 'six_win_perc', 'win_div_perc', 'win_conf_perc', 'playoff_perc', 'nc_perc', 'win_nc']


def parse_fpi(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser') # Get HTML content
    team_data = []
    team_table = soup.find('table', attrs={'class': 'Table Table--align-right Table--fixed Table--fixed-left'})
    team_table_body = team_table.find('tbody')
    team_rows = team_table_body.find_all('tr')

    for row in team_rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        team_data.append([ele for ele in cols if ele])  # strip empty padding row

    metrics_data = []
    table = soup.find('table', attrs={'class': 'Table Table--align-right'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        metrics_data.append([ele for ele in cols if ele])  # strip empty padding row

    combined_data = list(map(list.__add__, team_data, metrics_data))
    combined_data.insert(0, headers)

    return combined_data


def write_fpi_file(path, data):
    out_file = open(path, 'w+', newline='', encoding='utf-8')

    with out_file:
        write = csv.writer(out_file)
        write.writerows(data)


def fetch_fpi_data():
    years = [2012,2013,2014,2015,2016,2017,2018,2019,2021,2022]

    for year in years:
        path = f'fpi-data/{year}-fpi.csv'
        url = f'https://www.espn.com/college-football/fpi/_/season/{year}'
        data = parse_fpi(url)
        write_fpi_file(path,data)


fetch_fpi_data()
