from photo_emailer.infrastructure.credentials_io import CredentialsIO

from photo_emailer.logic.credentials import Credentials
from googleapiclient.discovery import build
from photo_emailer.infrastructure.email_sender import EmailSender
from photo_emailer.infrastructure.credentials_refresher import CredentialsRefresher
from photo_emailer.infrastructure.browser_authentication import BrowserAuthClient
from email.message import EmailMessage
from google.auth.exceptions import RefreshError


class PhotoEmailer:
    def __init__(
        self,
        credentials_loader=None,
        credentials_refresher=None,
        browser_auth_client=None,
        sender=None,
    ):
        self.credentials_loader = (
            credentials_loader
            if credentials_loader is not None
            else CredentialsIO.create("token.json")
        )

        self.credentials_refresher = (
            credentials_refresher
            if credentials_refresher is not None
            else CredentialsRefresher.create()
        )

        self.browser_auth_client = (
            browser_auth_client
            if browser_auth_client is not None
            else BrowserAuthClient.create()
        )

        self.sender = sender if sender is not None else EmailSender.create()

        self.credentials = None

    def load_credentials(self):
        self.credentials = Credentials.from_dict(
            self.credentials_loader.load_credentials()
        )

    def refresh_if_needed(self):
        try:
            if self.credentials.is_expired():
                self.credentials = self.credentials_refresher.refresh(self.credentials)
        except RefreshError:
            self.credentials = self.browser_auth_client.run_browser_authentication()

    def store_credentials(self):
        self.credentials_loader.store_credentials(self.credentials.to_dict())

    def send_email(self, to):
        msg = self.prepare_email(to)
        self.sender.send_email(msg, self.credentials)

    def prepare_email(self, to):
        msg = EmailMessage()
        msg["Subject"] = ""
        msg["To"] = to
        msg.set_content("Hello World")
        return msg
