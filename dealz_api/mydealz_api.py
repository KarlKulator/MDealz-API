from dealz_api.util import *
from dealz_api.fresh_deal import FreshDeal
import re
from ctparse import ctparse
from datetime import datetime, timedelta


def parse_time_text(creation_date_text):
    creation_date_string = re.search(r'eingestellt am .* \d\d\d\d', creation_date_text)
    if creation_date_string:
        return ctparse(creation_date_string.group()).resolution.dt

    creation_date_string = re.search(r'eingestellt \d.*\)', creation_date_text)
    if creation_date_string:
        return ctparse(creation_date_string.group(), ts=datetime.now().date().replace(month=1, day=1)).resolution.dt

    creation_date_string = re.search(r'eingestellt vor (?:(\d|\d\d) h, )*(\d|\d\d) m', creation_date_text)
    if creation_date_string:
        return datetime.now() - timedelta(hours=int(creation_date_string.group(1)), minutes=int(creation_date_string.group(2)))



def get_creation_date(soup):
    creation_date_text = str(soup.find(text=re.compile(r'eingestellt (am |vor |)\d')))
    return parse_time_text(creation_date_text)


def get_deal_description(soup):
    pass


class MydealzApi:
    def __init__(self):
        self._fresh_deals_url = 'https://www.mydealz.de/discussed'
        self._request_header = {'User-Agent': "Firefox 52.0.86"}

    def get_fresh_deals(self):
        soup = get_soup(self._fresh_deals_url, self._request_header)
        return self.get_fresh_deals_from_soup(soup, detailed_info=True)

    def get_fresh_deals_from_soup(self, soup, detailed_info=False):
        fresh_deals = []
        for tag in soup.find_all('article', class_='thread--deal'):
            thread_id = tag['id']
            href = tag.find('a', class_='thread-link')['href']

            price_tag = tag.find('span', class_='thread-price')
            if price_tag is not None:
                price = re.compile('[0-9]+,*[0-9]*').search(price_tag.getText(strip=True))
                if price is not None:
                    price = float(price.group().replace('.', '').replace(',', '.'))
            else:
                price = None

            degrees_string = tag.find('div', class_='vote-box').getText(strip=True)
            # degrees string might be "Neu" if deal is new
            if degrees_string != "Neu":
                degrees = int(re.compile(r'([0-9]+)°').search(degrees_string).group(1))
            else:
                degrees = 0

            group = ''
            title = tag.find('a', class_='thread-link').getText(strip=True)
            username = tag.find('span', class_='thread-username').getText(strip=True)
            number_of_comments = int(tag.find('a', class_='cept-comment-link').getText(strip=True))

            if detailed_info:
                deal_soup = get_soup(href, self._request_header)
                deal_text = deal_soup.find('div', class_='userHtml').getText(strip=True)
                creation_date = get_creation_date(deal_soup)
            else:
                deal_text = tag.find('div', class_='cept-description-container').getText(strip=True)
                creation_date = None

            fresh_deal = FreshDeal(thread_id, href, price, degrees, creation_date, group, title, username,
                                   deal_text, number_of_comments)
            fresh_deals.append(fresh_deal)
        return fresh_deals
