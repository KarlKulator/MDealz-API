import bs4
import unittest
from dealz_api.mydealz_api import MydealzApi
from test.debuggable_test_case import DebuggableTestCase

class TestMydealzApi(DebuggableTestCase):
    def test_get_fresh_deals_from_soup(self):
        with open('mydealz_discussed_test.html') as f:
            self.fresh_deals_soup = bs4.BeautifulSoup(f, 'html.parser')
        self.api = MydealzApi()
        self.fresh_deals_result = [{'test': 1}]

        fresh_deals = self.api.get_fresh_deals_from_soup(self.fresh_deals_soup)
        self.assertEqual(self.fresh_deals_result, fresh_deals)


if __name__ == '__main__':
    unittest.main()
