import urllib.request
import bs4
import datetime
import dateparser
import sendgmail


class Deal:
    def __init__(self, thread_id, href, price, degrees, creation_date, group, title, username, time_since_comment,
                 deal_text,
                 number_of_comments):
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

    def __str__(self):
        return "Deal %s: Title: %s, URL: %s, Price: %s, Degrees: %s, Creation date: %s, Group: %s, Username: %s, LastCommented: %s, #Comments: %s" % (
            self.thread_id, self.title, self.href, self.price, self.degrees, self.creation_date, self.group,
            self.username,
            self.time_since_comment,
            self.number_of_comments)

    def update(self, thread_id, href, price, degrees, creation_date, group, title, username, time_since_comment,
                    deal_text,
                    number_of_comments):
        self.__init__(thread_id, href, price, degrees, creation_date, group, title, username, time_since_comment,
                      deal_text,
                      number_of_comments)

    def send_to_email(self, recipient_email_adress):
        email_text = str(self)
        subject = "New Old'n'Discussed Deal"
        sendgmail.send_gmail(recipient_email_adress, email_text, subject)


# parse time since last comment string into seconds since last comment
def parse_mydealz_time_string(mydealz_time_string):
    # time_last_comment_string specifies relative time in format "vor %H h, %M m, %s S"
    if mydealz_time_string.startswith("vor"):
        important_tail = mydealz_time_string[4:]
        return datetime.datetime.now() - dateparser.parse(important_tail)

        # old implementation
        # time_dict = dict(
        #     zip([c for c in list(important_tail) if c.isalpha()], [int(d) for d in re.findall('\d+', important_tail)]))
        # time_last_comment_sec = 0
        # for unit, value in time_dict.items():
        #     if unit == 'h':
        #         time_last_comment_sec += value * 3600
        #     elif unit == 'm':
        #         time_last_comment_sec += value * 60
        #     elif unit == 's':
        #         time_last_comment_sec += value
        # return datetime.timedelta(seconds=time_last_comment_sec)

    # time_last_comment_string specifies date of last comment
    return datetime.datetime.now() - dateparser.parse(mydealz_time_string)


# check when a deal was created and return time since creation in
def get_creation_date_from_url(url_to_deal):
    req = urllib.request.Request(url_to_deal, headers={'User-Agent': "Firefox 52.0.86"})
    with urllib.request.urlopen(req) as conn:
        soup = bs4.BeautifulSoup(conn, 'lxml')

    creation_date_string = soup.find(lambda tag: tag.name == 'time').find('span', class_='hide--fromW3').text
    return parse_mydealz_time_string(creation_date_string)


def get_deal_description_from_url(url_to_deal):
    # TODO implement this
    pass
