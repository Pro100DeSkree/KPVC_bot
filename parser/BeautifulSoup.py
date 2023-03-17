from bs4 import BeautifulSoup as bs


def get_soup(soup_raw):
    soup = bs(soup_raw, 'lxml')
    return soup
