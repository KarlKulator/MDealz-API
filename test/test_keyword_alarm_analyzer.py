import unittest

from dealz_api.action_info import ActionInfo
from dealz_api.deal import Deal
from dealz_api.fresh_deal import FreshDeal
from dealz_api.keyword_alarm_analyzer import KeywordAlarmAnalyzer
from test.debuggable_test_case import DebuggableTestCase


class MyTestCase(DebuggableTestCase):
    def setUp(self):
        self.kaa = KeywordAlarmAnalyzer('config/test_keyword_alarm_analyzer.json')

        self.fresh_deal_nokeyword = FreshDeal(1, 'testhref.com/1', 23.3, 300, None, 'testgroup', 'testtitle1',
                                              'testusername1', 'testdealtext1', 1)
        self.fresh_deal_1keyword = FreshDeal(2, 'testhref.com/2', 24.3, 400, None, 'testgroup2', 'testtitle2',
                                             'testusername2', 'Dieser Drucker ist ein Test', 11)
        self.fresh_deal_2keyword = FreshDeal(3, 'testhref.com/2', 25.3, 500, None, 'testgroup3', 'testtitle3',
                                             'testusername3', 'DruckerAral', 1)

        self.previous_deal_no_keyword_triggered = Deal(self.fresh_deal_nokeyword)
        self.previous_deal_keyword_triggered = Deal(self.fresh_deal_nokeyword)
        self.previous_deal_keyword_triggered.triggered_keywords.append('Drucker')

    def test_call_no_keyword_previous_no_keyword_fresh(self):
        action_info = ActionInfo()
        previous_deal_new, action_info_new = self.kaa(self.previous_deal_no_keyword_triggered,
                                                      self.fresh_deal_nokeyword, action_info)
        self.assertFalse(action_info_new.keyword_triggers)
        self.assertEqual(action_info, action_info_new)

    def test_call_no_keyword_previous_1keyword_fresh(self):
        action_info = ActionInfo()
        previous_deal_new, action_info_new = self.kaa(self.previous_deal_no_keyword_triggered, self.fresh_deal_1keyword,
                                                      action_info)
        self.assertListEqual(action_info_new.keyword_triggers, [(['Drucker'], previous_deal_new)])
        self.assertNotEqual(action_info, action_info_new)

    def test_call_no_keyword_previous_2keyword_fresh(self):
        action_info = ActionInfo()
        previous_deal_new, action_info_new = self.kaa(self.previous_deal_no_keyword_triggered, self.fresh_deal_2keyword,
                                                      action_info)
        self.assertListEqual(action_info_new.keyword_triggers,
                             [(['Drucker', 'Aral'], previous_deal_new)])
        self.assertNotEqual(action_info, action_info_new)

    def test_call_keyword_previous_no_keyword_fresh(self):
        action_info = ActionInfo()
        previous_deal_new, action_info_new = self.kaa(self.previous_deal_keyword_triggered, self.fresh_deal_nokeyword,
                                                      action_info)
        self.assertListEqual(action_info_new.keyword_triggers, [])
        self.assertEqual(action_info, action_info_new)

    def test_call_keyword_previous_1keyword_fresh(self):
        action_info = ActionInfo()
        previous_deal_new, action_info_new = self.kaa(self.previous_deal_keyword_triggered, self.fresh_deal_1keyword,
                                                      action_info)
        self.assertListEqual(action_info_new.keyword_triggers, [])
        self.assertEqual(action_info, action_info_new)

    def test_call_keyword_previous_2keyword_fresh(self):
        action_info = ActionInfo()
        previous_deal_new, action_info_new = self.kaa(self.previous_deal_keyword_triggered, self.fresh_deal_2keyword,
                                                      action_info)
        self.assertListEqual(action_info_new.keyword_triggers, [(['Aral'], previous_deal_new)])
        self.assertNotEqual(action_info, action_info_new)

    def test_call_keyword_previous_2keyword_fresh_non_empty_action_info(self):
        action_info = ActionInfo()
        action_info.keyword_triggers.append((['test'], self.previous_deal_no_keyword_triggered))
        previous_deal_new, action_info_new = self.kaa(self.previous_deal_keyword_triggered, self.fresh_deal_2keyword,
                                                      action_info)
        self.assertListEqual(action_info_new.keyword_triggers,
                             [(['test'], self.previous_deal_no_keyword_triggered), (['Aral'], previous_deal_new)])
        self.assertNotEqual(action_info, action_info_new)


if __name__ == '__main__':
    unittest.main()
