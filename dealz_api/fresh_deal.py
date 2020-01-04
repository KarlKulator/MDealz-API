class FreshDeal:
    def __init__(self, thread_id, href, price, degrees, creation_date, group, title, username,
                 deal_text, number_of_comments):
        self.thread_id = thread_id
        self.href = href
        self.price = price
        self.degrees = degrees
        self.creation_date = creation_date
        self.group = group
        self.title = title
        self.username = username
        self.deal_text = deal_text
        self.number_of_comments = number_of_comments

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if not isinstance(other, FreshDeal):
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
