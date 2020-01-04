from application.deals_database import DealsDatabase
import jsonpickle
import unittest
from test.debuggable_test_case import DebuggableTestCase
from dealz_api.deal import Deal

class TestDealsDatabase(DebuggableTestCase):
    def setUp(self):
        with open('fresh_deals_pickle_test.json') as f:
            self.fresh_deals_test = jsonpickle.decode(f.read())

    def test_size(self):
        database = DealsDatabase()
        for deal in self.fresh_deals_test:
            database.update_deal(Deal(deal))
        self.assertEqual(database.size(), len(self.fresh_deals_test))

    def test_insert_and_has(self):
        database = DealsDatabase()
        for deal in self.fresh_deals_test:
            database.update_deal(Deal(deal))
        for deal in self.fresh_deals_test:
            self.assertTrue(database.has_deal(deal.thread_id))

    def test_insert_and_get(self):
        database = DealsDatabase()
        for deal in self.fresh_deals_test:
            database.update_deal(Deal(deal))
        for deal in self.fresh_deals_test:
            self.assertEqual(database.get_deal(deal.thread_id), Deal(deal))

    def test_update_and_get(self):
        database = DealsDatabase()
        for deal in self.fresh_deals_test:
            database.update_deal(Deal(deal))
        modifiedDeal = self.fresh_deals_test[0]
        modifiedDeal.degrees = 10000
        database.update_deal(modifiedDeal)

if __name__ == '__main__':
    unittest.main()
