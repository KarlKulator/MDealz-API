import smtplib
from email.mime.text import MIMEText


def send_gmail(recipient_email_adress, email_text, subject, sender_email_address, password, smtp_address):
    msg = MIMEText(email_text)
    msg['Subject'] = subject
    msg['To'] = recipient_email_adress
    msg['From'] = sender_email_address
    try:
        with smtplib.SMTP(smtp_address, 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender_email_address, password)
            s.send_message(msg)
            s.close()
        print("Email successfully sent")
    except Exception as e:
        print("Unable to send the email in Deal.send_to_email.")
        print(e)
