import json

from dealz_api.sendgmail import send_gmail
from dealz_api.action_info import ActionInfo


def create_email_text(action_info: ActionInfo):
    email_text = ''
    for keyword_trigger in action_info.keyword_triggers:
        email_text += 'Keyword trigger for {}:\r\n {}.\r\n  URL: {}\r\n\r\n'.format(str(keyword_trigger[0]),
                                                                                    keyword_trigger[1].title,
                                                                                    keyword_trigger[1].href)
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

    def __call__(self, action_info: ActionInfo):
        if action_info.keyword_triggers:
            email_text = create_email_text(action_info)
            send_gmail(self.recipient_email_address_, email_text, self.subject_, self.sender_email_address_,
                       self.password_,
                       self.smtp_address_)
