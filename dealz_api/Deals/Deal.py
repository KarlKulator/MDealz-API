class Deal:
    def __init__(self, thread_id, href, price, degrees, creation_date, group, title, username, time_since_comment,
                 deal_text, number_of_comments):
        self.thread_id = thread_id
        self.href = href
        self.price = price
        self.degrees = degrees
        self.creation_date = creation_date
        self.group = group
        self.title = title
        self.username = username
        self.time_since_comment = time_since_comment
        self.deal_text = deal_text
        self.number_of_comments = number_of_comments
        self._notified = False

    def __str__(self):
        return str(self.__dict__)

    def update(self, thread_id, href, price, degrees, creation_date, group, title, username, time_since_comment,
               deal_text, number_of_comments):
        self.__init__(thread_id, href, price, degrees, creation_date, group, title, username, time_since_comment,
                      deal_text, number_of_comments)

    def setNotified(self, notified):
        self._notified = False

    def isNotified(self):
        return self._notified
