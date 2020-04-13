import bs4
import urllib.request

def get_soup(url, header):
    req = urllib.request.Request(url, headers=header)
    with urllib.request.urlopen(req) as conn:
        soup = bs4.BeautifulSoup(conn, 'lxml')
    return soup
