import yagmail
import os


GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


class Notifier:

    def __init__(self):
        self.user = GMAIL_USER
        self.app_password = GMAIL_APP_PASSWORD


    def send_email(self, to, subject, content):
        with yagmail.SMTP(self.user, self.app_password) as yag:
            yag.send(to, subject, content)
            print('Sent email successfully')
