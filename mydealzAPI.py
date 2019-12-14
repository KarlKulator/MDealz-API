import bs4
import urllib.request
from Deals import Deal
from Deals import DiscussedDeal
import datetime
import time

deal_dict = {}

iteration = 0
while (True):
    print("Searching for new discussed deals; iteration: %d" % iteration)
    iteration += 1
    # create BeautifulSoup tree from url
    req = urllib.request.Request('https://www.mydealz.de/discussed', headers={'User-Agent': "Firefox 52.0.86"})
    with urllib.request.urlopen(req) as conn:
        soup = bs4.BeautifulSoup(conn, 'lxml')

    # print(soup.prettify())
    # with codecs.open('discussed.html', 'w', 'utf-8-sig') as f:
    #     f.write(soup.prettify())

    # find all deals and save them
    for tag in soup.find_all('article', class_='thread--deal', attrs={'data-track': '{"category":"list deal"}'}):
        thread_id = tag['id']
        href = tag.find('a', class_='vwo-thread-title')['href']

        price_tag = tag.find('span', class_='thread-price')
        if price_tag is not None:
            # remove euro sign and convert to float
            price = float(price_tag.text[0:-1].replace('.', '').replace(',', '.'))
        else:
            price = None

        degrees_string = tag.find('strong', class_='vote-temp').text
        # degrees string might be "Neu" if deal is new
        if degrees_string != "Neu":
            degrees = int(degrees_string[:-1])
        else:
            degrees = 0

        group = tag.find('a', class_='thread-group').text
        title = tag.find('a', class_='vwo-thread-title').text
        username = tag.find('span', class_='thread-username').text
        time_last_comment_string = Deal.parse_mydealz_time_string(
            tag.find('time', class_='cept-time-label').find('span', class_='hide--fromW3').text)
        deal_text = tag.find('div', class_='userHtml').text
        number_of_comments_string = tag.find('a', class_='cept-comment-link').text
        number_of_comments = int([int(s) for s in number_of_comments_string.split() if s.isdigit()][0])
        creation_date = Deal.get_creation_date_from_url(href);

        print(Deal.Deal(thread_id, href, price, degrees, creation_date, group, title, username,
                         time_last_comment_string, deal_text, number_of_comments))

        if creation_date > datetime.timedelta(days=7):
            try:
                discussed_deal = deal_dict[thread_id]
                if number_of_comments > discussed_deal.number_of_comments:
                    discussed_deal.update(thread_id, href, price, degrees, creation_date, group, title, username,
                                            time_last_comment_string, deal_text, number_of_comments)
                    discussed_deal.increase_num_discussed_detected()

            except KeyError:
                # deal was not found before
                discussed_deal = DiscussedDeal.DiscussedDeal(thread_id, href, price, degrees, creation_date, group, title, username,
                                            time_last_comment_string, deal_text, number_of_comments)
                discussed_deal.increase_num_discussed_detected()
                deal_dict[thread_id] = discussed_deal

            print("Potential new old discussed deal found")

            if discussed_deal.get_num_discussed_detected() > 2:
                if not discussed_deal.is_notified():
                    discussed_deal.set_notified()
                    # send email with deal
                    discussed_deal.send_to_email('pirklveit@gmail.com')
                    time.sleep(1)

    # wait 2 minutes before polling again for newly discussed deals
    time.sleep(120)
