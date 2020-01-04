class Deal:
    def __init__(self, fresh_deal):
        self.thread_id = fresh_deal.thread_id
        self.href = fresh_deal.href
        self.price = fresh_deal.price
        self.degrees = fresh_deal.degrees
        self.creation_date = fresh_deal.creation_date
        self.group = fresh_deal.group
        self.title = fresh_deal.title
        self.username = fresh_deal.username
        self.deal_text = fresh_deal.deal_text
        self.number_of_comments = fresh_deal.number_of_comments
        self._notified = False

    def update(self, fresh_deal):
        self.thread_id = fresh_deal.thread_id
        self.href = fresh_deal.href
        self.price = fresh_deal.price
        self.degrees = fresh_deal.degrees
        self.creation_date = fresh_deal.creation_date
        self.group = fresh_deal.group
        self.title = fresh_deal.title
        self.username = fresh_deal.username
        self.deal_text = fresh_deal.deal_text
        self.number_of_comments = fresh_deal.number_of_comments

    def setNotified(self):
        _notified = True

    def isNotified(self):
        return self._notified

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if not isinstance(other, Deal):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.thread_id == other.thread_id and \
               self.href == other.href and \
               self.price == other.price and \
               self.degrees == other.degrees and \
               self.creation_date == other.creation_date and \
               self.group == other.group and \
               self.title == other.title and \
               self.username == other.username and \
               self.deal_text == other.deal_text and \
               self.number_of_comments == other.number_of_comments

