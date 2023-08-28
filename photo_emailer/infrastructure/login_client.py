from photo_emailer.logic.credentials import Credentials
from google.oauth2.credentials import Credentials as GoogleCredentials
from googleapiclient.discovery import build


class LoginClient:
    def __init__(
        self,
        credentials: Credentials,
        google_credentials_factory=GoogleCredentials,
        service_builder=build,
    ):
        self.credentials = credentials
        self.google_credentials_factory
        self.service_builder = build

    def login(self):
        self.refresh_if_needed()
        creds = self.google_credentials_factory(
            token=self.credentials.token,
            refresh_token=self.credentials.refresh_token,
            token_uri=self.credentials.token_uri,
            client_id=self.credentials.client_id,
            client_secret=self.credentials.client_secret,
            scopes=self.credentials.scopes,
        )

        service = self.service_builder("gmail", "v1", credentials=creds)
        return service

    def refresh_if_needed(self):
        if self.credentials.is_expired():
            creds = self.google_credentials_factory(
                token=self.credentials.token,
                refresh_token=self.credentials.refresh_token,
                token_uri=self.credentials.token_uri,
                client_id=self.credentials.client_id,
                client_secret=self.credentials.client_secret,
                scopes=self.credentials.scopes,
            )
            creds.refresh(Request())
            self.credentials = Credentials(
                token=creds.token,
                refresh_token=creds.refresh_token,
                token_uri=creds.token_uri,
                client_id=creds.client_id,
                client_secret=creds.client_secret,
                scopes=creds.scopes,
                expiry=creds.expiry,
            )
