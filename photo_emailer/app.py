from photo_emailer.infrastructure.credentials_loader import CredentialsLoader
from photo_emailer.infrastructure.login_client import LoginClient
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
    ):
        self.credentials_loader = (
            credentials_loader
            if credentials_loader is not None
            else CredentialsLoader.create("token.json")
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
