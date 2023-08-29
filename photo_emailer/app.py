from photo_emailer.infrastructure.credentials_loader import CredentialsLoader
from photo_emailer.infrastructure.login_client import LoginClient
from photo_emailer.logic.credentials import Credentials
from googleapiclient.discovery import build
from photo_emailer.infrastructure.email_sender import EmailSender
from email.message import EmailMessage


class PhotoEmailer:
    def __init__(self, credentials_loader=None, login_client=None, email_sender=None):
        if credentials_loader is None:
            self.credentials_loader = CredentialsLoader.create(filename="token.json")
        else:
            self.credentials_loader = credentials_loader
        self.login_client = (
            login_client if login_client else LoginClient.create(credentials=None)
        )

        self.email_sender = email_sender if email_sender else EmailSender.create()

        self.service = None

    def run(self):
        return self.login()

    def login(self):
        creds = Credentials.from_dict(self.credentials_loader.load_credentials())
        self.login_client.credentials = creds
        self.service = self.login_client.login()

    def send_email(self, subject: str, message: str):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg.set_content(message)
        self.email_sender.send_email(msg)
