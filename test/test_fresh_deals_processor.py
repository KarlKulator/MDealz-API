import unittest
from copy import deepcopy
from mock import Mock, call
import jsonpickle

from dealz_api.action import Action
from dealz_api.fresh_deals_processor import FreshDealsProcessor
from dealz_api.deals_database import DealsDatabase
from dealz_api.fresh_deal import FreshDeal
from dealz_api.deal import Deal
from test.debuggable_test_case import DebuggableTestCase


class TestFreshDealsProcessor(DebuggableTestCase):
    def setUp(self):
        with open('fresh_deals_pickle_test.json') as f:
            self.fresh_deals_test = jsonpickle.decode(f.read())
        self.database = DealsDatabase()
        self.database_mock = Mock(wraps=self.database)
        self.deal_analyzer_mock = Mock(
            wraps=lambda previous_deal, fresh_deal, action_info: (deepcopy(previous_deal), deepcopy(action_info)))
        self.processor = FreshDealsProcessor(self.database_mock)
        self.processor.add_deal_analyzer(self.deal_analyzer_mock)

    def test_process_fresh_deals_from_empty(self):
        self.processor.process_fresh_deals(self.fresh_deals_test)

        self.database_mock.has_deal.assert_has_calls(
            [call(fresh_deal.thread_id) for fresh_deal in self.fresh_deals_test])
        self.database_mock.update_deal.assert_has_calls(
            [call(Deal(fresh_deal)) for fresh_deal in self.fresh_deals_test])
        self.deal_analyzer_mock.assert_has_calls(
            [call(Deal(fresh_deal), fresh_deal, Action()) for fresh_deal in
             self.fresh_deals_test])

    def test_process_fresh_deals_twice(self):
        self.processor.process_fresh_deals(self.fresh_deals_test)
        self.deal_analyzer_mock.reset_mock()
        self.processor.process_fresh_deals(self.fresh_deals_test)

        self.deal_analyzer_mock.assert_not_called()

    def test_process_fresh_deals_new_deals(self):
        self.processor.process_fresh_deals(self.fresh_deals_test)
        self.database_mock.reset_mock()
        self.deal_analyzer_mock.reset_mock()

        new_deals = [
            FreshDeal(123123, 'test1href', 23.3, 666, 0, '', 'test1title', 'test1username', 'test1deal_text', 300),
            FreshDeal(114114, 'test2href', 121.3, 122, 0, '', 'test2title', 'test2username', 'test2deal_text', 200)]
        new_fresh_deals = [self.fresh_deals_test[0], new_deals[0], new_deals[1], self.fresh_deals_test[1]]
        self.processor.process_fresh_deals(new_fresh_deals)

        self.database_mock.has_deal.assert_has_calls([call(new_deal.thread_id) for new_deal in new_deals])
        self.database_mock.update_deal.assert_has_calls([call(Deal(new_deal)) for new_deal in new_deals])
        self.deal_analyzer_mock.assert_has_calls([call(Deal(new_deal), new_deal, Action()) for new_deal in new_deals])

    def test_process_fresh_deals_updated_deals(self):
        self.processor.process_fresh_deals(self.fresh_deals_test)
        self.database_mock.reset_mock()
        self.deal_analyzer_mock.reset_mock()

        updated_fresh_deals = deepcopy(self.fresh_deals_test)
        updated_fresh_deals[0].price = 121.2
        updated_fresh_deals[1].degrees = 432
        updated_fresh_deals[2].title = 'New test title'
        updated_fresh_deals[3].username = 'NewTestUsername'
        updated_fresh_deals[4].deal_text = 'NewDealText'
        updated_fresh_deals[9].number_of_comments = 852

        updated_fresh_deals_onlychanged = [updated_fresh_deals[i] for i in [0, 1, 2, 3, 4, 9]]
        deals_test_onlychanged = [Deal(self.fresh_deals_test[i]) for i in [0, 1, 2, 3, 4, 9]]

        self.processor.process_fresh_deals(updated_fresh_deals)
        self.database_mock.update_deal.assert_has_calls(
            [call(Deal(updated_fresh_deal)) for updated_fresh_deal in updated_fresh_deals_onlychanged])
        self.deal_analyzer_mock.assert_has_calls(
            [call(fresh_deal_test, updated_fresh_deal, Action()) for fresh_deal_test, updated_fresh_deal in
             zip(deals_test_onlychanged, updated_fresh_deals_onlychanged)])

if __name__ == '__main__':
    unittest.main()
