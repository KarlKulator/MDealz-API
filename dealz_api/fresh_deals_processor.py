from copy import deepcopy

from dealz_api.action import Action
from dealz_api.deal import Deal
class FreshDealsProcessor:
    def __init__(self, deals_database):
        self._previous_fresh_deals = []
        self._deal_analyzers = []
        self._deals_database = deals_database
        self._action_executor = None

    def process_fresh_deals(self, fresh_deals):
        for fresh_deal in fresh_deals:
            if fresh_deal not in self._previous_fresh_deals:
                if self._deals_database.has_deal(fresh_deal.thread_id):
                    previous_deal = self._deals_database.get_deal(fresh_deal.thread_id)
                else:
                    previous_deal = Deal(fresh_deal)
                action = Action()
                for deal_analyzer in self._deal_analyzers:
                    previous_deal, action = deal_analyzer(previous_deal, fresh_deal, action)

                previous_deal.update(fresh_deal)
                self._deals_database.update_deal(previous_deal)

                if self._action_executor:
                    self._action_executor(action, deepcopy(previous_deal))

        self._previous_fresh_deals = deepcopy(fresh_deals)

    def add_deal_analyzer(self, deal_analyzer):
        self._deal_analyzers.append(deal_analyzer)

    def set_action_executor(self, action_executor):
        self._action_executor = action_executor
