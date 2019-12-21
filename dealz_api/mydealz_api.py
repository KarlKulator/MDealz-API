from dealz_api.util import *
from dealz_api.Deals import Deal
import re

class MydealzApi:
    def __init__(self):
        self._fresh_deals_url = 'https://www.mydealz.de/discussed'
        self._request_header = {'User-Agent': "Firefox 52.0.86"}

    def get_fresh_deals(self):
        soup = get_soup(self._fresh_deals_url, self._request_header)
        return self.get_fresh_deals_from_soup(soup)

    def get_fresh_deals_from_soup(self, soup):
        fresh_deals = []
        for tag in soup.find_all('article', class_='thread--deal'):
            thread_id = tag['id']
            href = tag.find('a', class_='thread-link')['href']

            price_tag = tag.find('span', class_='thread-price')
            if price_tag is not None:
                price = re.compile('[0-9]+,*[0-9]*').search(price_tag.getText(strip=True)).group()
                price = float(price.replace('.', '').replace(',', '.'))
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
            time_last_comment_string = parse_mydealz_time_string(tag.find(text=re.compile('.*vor [0-9]+.*')))
            deal_text = tag.find('div', class_='cept-description-container').getText(strip=True)
            number_of_comments = int(tag.find('a', class_='cept-comment-link').getText(strip=True))
            # creation_date = get_creation_date_from_url(href, self._request_header);
            creation_date = 0
            fresh_deal = Deal.Deal(thread_id, href, price, degrees, creation_date, group, title, username,
                            time_last_comment_string, deal_text, number_of_comments)
            print(fresh_deal)
            fresh_deals.append(fresh_deal)
        return fresh_deals
