from Deals import Deal


class DiscussedDeal(Deal.Deal):
    def __init__(self, thread_id, href, price, degrees, creation_date, group, title, username, time_since_comment,
                 deal_text,
                 number_of_comments):
        Deal.Deal.__init__(self, thread_id, href, price, degrees, creation_date, group, title, username,
                      time_since_comment,
                      deal_text,
                      number_of_comments)
        self._num_discussed_detected = 0

    def increase_num_discussed_detected(self):
        self._num_discussed_detected += 1

    def get_num_discussed_detected(self):
        return self._num_discussed_detected

    def set_notified(self):
        self._notified = True

    def is_notified(self):
        return self._notified