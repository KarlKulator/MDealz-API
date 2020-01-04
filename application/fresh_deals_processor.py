from dealz_api.deal import Deal
from copy import deepcopy
class FreshDealsProcessor:
    def __init__(self, deals_database):
        self._previous_fresh_deals = []
        self._deal_analyzers = []
        self._deals_database = deals_database

    def process_fresh_deals(self, fresh_deals):
        for fresh_deal in fresh_deals:
            if fresh_deal not in self._previous_fresh_deals:
                previous_deal = None
                if self._deals_database.has_deal(fresh_deal.thread_id):
                    previous_deal = self._deals_database.get_deal(fresh_deal.thread_id)
                for deal_analyzer in self._deal_analyzers:
                    deal_analyzer(previous_deal, fresh_deal)
                self._deals_database.update_deal(Deal(fresh_deal))
        self._previous_fresh_deals = deepcopy(fresh_deals)

    def add_deal_analyzer(self, deal_analyzer):
        self._deal_analyzers.append(deal_analyzer)
