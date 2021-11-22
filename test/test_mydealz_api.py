import datetime

import bs4
from freezegun import freeze_time
import jsonpickle
import unittest
from dealz_api.mydealz_api import MydealzApi
from test.debuggable_test_case import DebuggableTestCase

class TestMydealzApi(DebuggableTestCase):

    def check_consistency(self, fresh_deal):
        self.assertRegex(fresh_deal.thread_id, 'thread_\d+$')
        self.assertIn('https://www.mydealz.de', fresh_deal.href)
        if fresh_deal.price:
            self.assertIsInstance(fresh_deal.price, float)
            self.assertLess(fresh_deal.price, 10000000)
            self.assertGreaterEqual(fresh_deal.price, 0)
        self.assertIsInstance(fresh_deal.degrees, int)
        self.assertLess(fresh_deal.degrees, 200000)
        self.assertGreater(fresh_deal.degrees, -200000)
        if fresh_deal.creation_date:
            self.assertGreater(fresh_deal.creation_date, datetime.datetime(2010, 1, 1))
            self.assertLess(fresh_deal.creation_date, datetime.datetime.now())
        self.assertEqual(fresh_deal.group, '')
        self.assertTrue(fresh_deal.title)
        self.assertTrue(fresh_deal.username, '')
        self.assertTrue(fresh_deal.deal_text, '')
        self.assertIsInstance(fresh_deal.number_of_comments, int)
        self.assertLess(fresh_deal.number_of_comments, 100000)
        self.assertGreaterEqual(fresh_deal.number_of_comments, 0)

    @freeze_time("2020-01-01")
    def test_get_fresh_deals_from_soup_offline(self):
        with open('mydealz_discussed_test.html') as f:
            self.fresh_deals_soup = bs4.BeautifulSoup(f, 'html.parser')
        with open('fresh_deals_pickle_test.json') as f:
            self.fresh_deals_result = jsonpickle.decode(f.read())
        self.api = MydealzApi()
        fresh_deals = self.api.get_fresh_deals_from_soup(self.fresh_deals_soup)
        self.assertEqual(fresh_deals, self.fresh_deals_result)
        for fresh_deal in fresh_deals:
            self.check_consistency(fresh_deal)

    def test_get_fresh_deals(self):
        self.api = MydealzApi()
        fresh_deals = self.api.get_fresh_deals()
        self.assertGreater(len(fresh_deals), 5)
        for fresh_deal in fresh_deals:
            self.check_consistency(fresh_deal)


if __name__ == '__main__':
    unittest.main()
