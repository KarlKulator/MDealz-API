import smtplib
from email.mime.text import MIMEText

def send_gmail(recipient_email_adress, email_text, subject):
    sender = 'qwerreq123@gmail.com'
    gmail_password = 'qwerasdf1'
    msg = MIMEText(email_text)
    msg['Subject'] = subject
    msg['To'] = recipient_email_adress
    msg['From'] = sender
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.send_message(msg)
            s.close()
        print("Email successfully sent")
    except Exception as e:
        print("Unable to send the email in Deal.send_to_email.")
        print(e)
