from copy import deepcopy

class DealsDatabase:
    def __init__(self):
        self._deals = {}

    def has_deal(self, thread_id):
        return thread_id in self._deals

    def update_deal(self, deal):
        if self.has_deal(deal.thread_id):
            self._deals[deal.thread_id].update(deal)
        else:
            self._deals[deal.thread_id] = deal

    def get_deal(self, thread_id):
        return deepcopy(self._deals[thread_id])

    def size(self):
        return len(self._deals)