import csv

import requests
from bs4 import BeautifulSoup

# static header for the files because I'm too lazy to parse the table for them
header_list = ['Rk', 'Team', 'Rec', 'FBS', 'FEI', 'OFEI', 'OFEI_Rk', 'DFEI', 'DFEI_Rk', 'NDE', 'NDE_Rk', 'NPD', 'NPD_Rk', 'NAY', 'NAY_Rk', 'NPP', 'NPP_Rk', 'ELS', 'ELS_Rk', 'GLS', 'GLS_Rk', 'ALS', 'ALS_Rk']

def is_not_header_row(x):
    return x != header_list


def parse_fei(url):
    page = requests.get(url)  # fetch from link
    soup = BeautifulSoup(page.text, 'html.parser')  # Get HTML content

    data = []
    table = soup.find('table', attrs={'cellpadding': 0, 'cellspacing':0 } )  # sloppy table select
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        data.append([ele for ele in cols if ele])  # strip empty padding row
    data.pop(0)  # drop off the junk top level header
    filtered_data = list(filter(None, data))  # filter empty rows
    filtered_data = list(filter(is_not_header_row, filtered_data))  # filter out all repeat header rows

    filtered_data.insert(0, header_list)  # push header back on the top
    return filtered_data


def write_fei_file(path, data):
    out_file = open(path, 'w+', newline='')

    with out_file:
        write = csv.writer(out_file)
        write.writerows(data)



def fetch_fei_data():
    years = [2012,2013,2014,2015,2016,2017,2018,2019,2021,2022]

    for year in years:
        path = f'fei-data/{year}-fei.csv'
        url = f'https://www.bcftoys.com/{year}-fei/'
        data = parse_fei(url)
        write_fei_file(path,data)


fetch_fei_data()