from freezegun import freeze_time
import datetime
import unittest
import jsonpickle

from dealz_api.action import Action
from dealz_api.deal import Deal
from dealz_api.fresh_deal import FreshDeal
from dealz_api.hot_deal_analyzer import HotDealAnalyzer
from test.debuggable_test_case import DebuggableTestCase


class TestHotDealAnalyzer(DebuggableTestCase):
    def setUp(self):
        with open('fresh_deals_pickle_test.json') as f:
            self.fresh_deals_test = jsonpickle.decode(f.read())

        self.hotDealAnalyzer = HotDealAnalyzer('config/test_hot_deal_analyzer.json')

        self.creation_date_test = datetime.datetime(2021, 11, 23)

        self.fresh_deal_low_comments = FreshDeal(1, 'testhref.com/1', 23.3, 300, self.creation_date_test, 'testgroup',
                                           'testtitle1',
                                           'testusername1', 'testdealtext1', 1)
        self.fresh_deal_many_comments = FreshDeal(1, 'testhref.com/1', 24.3, 400, self.creation_date_test, 'testgroup',
                                        'testtitle1',
                                        'testusername1', 'testdealtext1', 15)

        self.previous_deal_low_comments = Deal(self.fresh_deal_low_comments)
        self.previous_deal_many_comments = Deal(self.fresh_deal_many_comments)

    def test_deal_becomes_hot(self):
        with freeze_time(self.creation_date_test):
            action: Action = Action()
            previous_deal_analyzed, action_analyzed = self.hotDealAnalyzer(self.previous_deal_low_comments, self.fresh_deal_low_comments, action)
            self.assertFalse(previous_deal_analyzed.hotnessChecked)
            self.assertFalse(action_analyzed.hotness_triggered)
        with freeze_time(self.creation_date_test + datetime.timedelta(minutes=10, seconds=1)):
            action: Action = Action()
            previous_deal_analyzed.update(self.fresh_deal_many_comments)
            previous_deal_analyzed, action_analyzed = self.hotDealAnalyzer(previous_deal_analyzed, self.fresh_deal_many_comments, action)
            self.assertTrue(previous_deal_analyzed.hotnessChecked)
            self.assertTrue(action_analyzed.hotness_triggered)

    def test_deal_becomes_hot_fast(self):
        with freeze_time(self.creation_date_test):
            action: Action = Action()
            previous_deal_analyzed, action_analyzed = self.hotDealAnalyzer(self.previous_deal_low_comments, self.fresh_deal_low_comments, action)
            self.assertFalse(previous_deal_analyzed.hotnessChecked)
            self.assertFalse(action_analyzed.hotness_triggered)
        with freeze_time(self.creation_date_test + datetime.timedelta(seconds=1)):
            action: Action = Action()
            previous_deal_analyzed, action_analyzed = self.hotDealAnalyzer(previous_deal_analyzed, self.fresh_deal_many_comments, action)
            previous_deal_analyzed.update(self.fresh_deal_many_comments)
            self.assertTrue(previous_deal_analyzed.hotnessChecked)
            self.assertTrue(action_analyzed.hotness_triggered)

    def test_deal_stays_cold(self):
        with freeze_time(self.creation_date_test):
            action: Action = Action()
            previous_deal_analyzed, action_analyzed = self.hotDealAnalyzer(self.previous_deal_low_comments, self.fresh_deal_low_comments, action)
            self.assertFalse(previous_deal_analyzed.hotnessChecked)
            self.assertFalse(action_analyzed.hotness_triggered)
        with freeze_time(self.creation_date_test + datetime.timedelta(minutes=10, seconds=1)):
            action: Action = Action()
            previous_deal_analyzed, action_analyzed = self.hotDealAnalyzer(previous_deal_analyzed, self.fresh_deal_low_comments, action)
            previous_deal_analyzed.update(self.fresh_deal_low_comments)
            self.assertTrue(previous_deal_analyzed.hotnessChecked)
            self.assertFalse(action_analyzed.hotness_triggered)
        with freeze_time(self.creation_date_test + datetime.timedelta(minutes=14, seconds=1)):
            action: Action = Action()
            previous_deal_analyzed, action_analyzed = self.hotDealAnalyzer(previous_deal_analyzed, self.fresh_deal_many_comments, action)
            previous_deal_analyzed.update(self.fresh_deal_many_comments)
            self.assertTrue(previous_deal_analyzed.hotnessChecked)
            self.assertFalse(action_analyzed.hotness_triggered)

    def test_deal_is_too_old(self):
        with freeze_time(self.creation_date_test + datetime.timedelta(minutes=15, seconds=1)):
            action: Action = Action()
            previous_deal_analyzed, action_analyzed = self.hotDealAnalyzer(self.previous_deal_low_comments, self.fresh_deal_many_comments, action)
            previous_deal_analyzed.update(self.fresh_deal_many_comments)
            self.assertTrue(previous_deal_analyzed.hotnessChecked)
            self.assertFalse(action_analyzed.hotness_triggered)

if __name__ == '__main__':
    unittest.main()
