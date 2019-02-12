import requests
from bs4 import BeautifulSoup


def dollar_cbr():
    resp = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    soup = BeautifulSoup(resp.content, 'xml')
    return soup.find(ID='R01235').Value.string


def euro_cbr():
    resp = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    soup = BeautifulSoup(resp.content, 'xml')
    return soup.find(ID='R01239').Value.string
