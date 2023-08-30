from email.message import EmailMessage
from photo_emailer.utils.events import OutputListener, OutputTracker
from googleapiclient.discovery import build
from requests import HTTPError
from google.oauth2.credentials import Credentials as GoogleCredentials
import base64


class EmailSender:
    def __init__(self, email_service):
        self.email_service = email_service
        self._listener = OutputListener()

    def track_output(self):
        return self._listener.create_tracker()

    @classmethod
    def create(cls):
        return cls(GoogleEmailService())

    @classmethod
    def create_null(cls):
        return cls(NullEmailService())

    def send_email(self, msg, creds):
        self.email_service.send_email(msg, creds)
        self._listener.track(data={"action": "send_email", "msg": msg, "creds": creds})


class GoogleEmailService:
    def send_email(self, msg, creds):
        g_creds = GoogleCredentials(
            token=creds.token,
            refresh_token=creds.refresh_token,
            token_uri=creds.token_uri,
            client_id=creds.client_id,
            client_secret=creds.client_secret,
            scopes=creds.scopes,
        )
        try:
            service = build("gmail", "v1", credentials=g_creds)
            msg = {"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}
            result = service.users().messages().send(userId="me", body=msg).execute()
            print(f"sent message to {result} Message Id: {result['id']}")
        except HTTPError as error:
            print(f"An error occurred: {error}")


class NullEmailService:
    def send_email(self, msg, creds):
        pass
