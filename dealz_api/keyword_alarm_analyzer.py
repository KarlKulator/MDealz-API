import copy
import json

from dealz_api.action import Action
from dealz_api.fresh_deal import FreshDeal
from dealz_api.deal import Deal

class KeywordAlarmAnalyzer:
    def __init__(self, configFile):
        with open(configFile, 'r') as file:
            config = json.load(file)
            self._keywords = config['keywords']

    def __call__(self, previous_deal: Deal, fresh_deal: FreshDeal, action: Action):
        previous_deal_new = copy.deepcopy(previous_deal)
        action_new = copy.deepcopy(action)

        text = fresh_deal.title + " " + fresh_deal.deal_text

        new_triggered_keywords = [keyword for keyword in self._keywords if
                                  keyword in text and keyword not in previous_deal.triggered_keywords]
        previous_deal_new.triggered_keywords.extend(new_triggered_keywords)
        if new_triggered_keywords:
            action_new.keyword_triggers.append((new_triggered_keywords, previous_deal_new))

        return previous_deal_new, action_new

