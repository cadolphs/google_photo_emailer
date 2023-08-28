from photo_emailer.infrastructure.credentials_loader import CredentialsLoader
from photo_emailer.logic.credentials import Credentials
from googleapiclient.discovery import build


class PhotoEmailer:
    def __init__(self, credentials_loader=None):
        if credentials_loader is None:
            self.credentials_loader = CredentialsLoader.create(filename="token.json")
        else:
            self.credentials_loader = credentials_loader

    def run(self):
        creds = Credentials.from_dict(self.credentials_loader.load_credentials())

        return creds
