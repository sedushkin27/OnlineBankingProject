import smtplib
from email.message import EmailMessage

sender = ''
password = ''


def send_email(recipient, massage):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender, recipient, massage)

        return 'message sent'
    except Exception as _ex:
        return f'{_ex} you may not have entered a login and password in email_management.py '