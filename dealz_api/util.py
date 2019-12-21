import bs4
import urllib.request
import datetime
import dateparser


def get_soup(url, header):
    req = urllib.request.Request(url, headers=header)
    soup = bs4.BeautifulSoup()
    with urllib.request.urlopen(req) as conn:
        soup = bs4.BeautifulSoup(conn, 'html.parse')
    return soup


# parse time since last comment string into seconds since last comment
def parse_mydealz_time_string(mydealz_time_string):
    # time_last_comment_string specifies relative time in format "vor %H h, %M m, %s S"
    if mydealz_time_string.startswith("vor"):
        important_tail = mydealz_time_string[4:]
        return datetime.datetime.now() - dateparser.parse(important_tail)

    # time_last_comment_string specifies date of last comment
    return datetime.datetime.now() - dateparser.parse(mydealz_time_string)


def get_creation_date_from_url(url_to_deal, headers):
    req = urllib.request.Request(url_to_deal, headers=headers)
    with urllib.request.urlopen(req) as conn:
        soup = bs4.BeautifulSoup(conn, 'lxml')

    creation_date_string = soup.find(lambda tag: tag.name == 'time').find('span', class_='hide--fromW3').text
    return parse_mydealz_time_string(creation_date_string)


def get_deal_description_from_url(url_to_deal):
    # TODO implement this
    pass
