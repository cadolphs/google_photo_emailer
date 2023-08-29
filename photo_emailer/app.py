from photo_emailer.infrastructure.credentials_loader import CredentialsLoader
from photo_emailer.infrastructure.login_client import LoginClient
from photo_emailer.logic.credentials import Credentials
from googleapiclient.discovery import build
from photo_emailer.utils.events import OutputListener, OutputTracker


class PhotoEmailer:
    def __init__(self, credentials_loader=None, login_client=None):
        if credentials_loader is None:
            self.credentials_loader = CredentialsLoader.create(filename="token.json")
        else:
            self.credentials_loader = credentials_loader
        self.login_client = (
            login_client if login_client else LoginClient.create(credentials=None)
        )

        self.service = None
        self._listener = OutputListener()

    def run(self):
        return self.login()

    def track_output(self):
        return self._listener.create_tracker()

    def login(self):
        creds = Credentials.from_dict(self.credentials_loader.load_credentials())
        self.login_client.credentials = creds
        self.service = self.login_client.login()
