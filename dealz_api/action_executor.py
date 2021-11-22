import json

import datetime
from dealz_api.sendgmail import send_gmail
from dealz_api.action import Action
from dealz_api.deal import Deal


def create_email_text(action: Action, deal: Deal):
    email_text = ''
    for keyword_trigger in action.keyword_triggers:
        email_text += f'Keyword trigger for {str(keyword_trigger[-1])}:\r\n {deal.title}\r\n  URL: {deal.href}\r\n\r\n'

    if action.hotness_triggered:
        email_text += f'Hotness triggered:\r\n' \
                      f' {deal.title}\r\n' \
                      f' URL: {deal.href}\r\n' \
                      f' #comments: {deal.number_of_comments}\r\n' \
                      f' #age: {(datetime.datetime.now() - deal.creation_date).total_seconds() / 60.0} minutes\r\n\r\n'
    return email_text


class ActionExecutor:
    def __init__(self, configFile):
        with open(configFile, 'r') as file:
            config = json.load(file)
            self.recipient_email_address_ = config['recipient_email_address']
            self.subject_ = config['subject']
            self.sender_email_address_ = config['sender_email_address']
            self.password_ = config['password']
            self.smtp_address_ = config['smtp_address']

    def __call__(self, action: Action, deal: Deal):
        if action.keyword_triggers or action.hotness_triggered:
            email_text = create_email_text(action, deal)
            send_gmail(self.recipient_email_address_, email_text, self.subject_, self.sender_email_address_,
                       self.password_,
                       self.smtp_address_)
