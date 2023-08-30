from photo_emailer.infrastructure.credentials_loader import CredentialsLoader
from photo_emailer.infrastructure.login_client import LoginClient
from photo_emailer.logic.credentials import Credentials
from googleapiclient.discovery import build
from photo_emailer.infrastructure.email_sender import EmailSender
from email.message import EmailMessage


class PhotoEmailer:
    def __init__(self, credentials_loader=None):
        self.credentials_loader = (
            credentials_loader
            if credentials_loader is not None
            else CredentialsLoader.create("token.json")
        )

    def load_credentials(self):
        return self.credentials_loader.load_credentials()
