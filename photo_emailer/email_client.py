from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
from email.mime.text import MIMEText
import base64
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


class EmailClient:
    def __init__(self, mail_api, credentials):
        self.api = mail_api(credentials)

    @classmethod
    def create(cls, credentials=None):
        return cls(GmailSendClient, credentials)

    @classmethod
    def create_null(cls, credentials):
        return cls(GmailSendStub, credentials)

    def send_email(self, to, subject, body):
        self.api.send_email(to, subject, body)


class AuthClient:
    def __init__(self, auth_api=None):
        self.api = auth_api()

    @classmethod
    def create(cls):
        return cls(GoogleAuthAPI)

    @classmethod
    def create_null(cls):
        return cls(AuthStub)

    def get_credentials(self):
        return self.api.get_credentials()


class GoogleAuthAPI:
    def run_browser_authentication(self):
        SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        return flow.run_local_server(port=0)

    def get_credentials(self):
        stored_creds = self.load_credentials("token.json")

        if stored_creds and stored_creds.expired and stored_creds.refresh_token:
            print("Refreshing expired credentials...")
            stored_creds.refresh(Request())
            self.store_credentials(stored_creds)
            return stored_creds
        elif not stored_creds.expired:
            print("Reusing stored credentials...")
            return stored_creds
        else:
            print("No reusable credentials found; authenticating again...")
            creds = self.run_browser_authentication()
            self.store_credentials(creds)
            return creds

    def store_credentials(self, creds):
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    def load_credentials(self, json):
        return Credentials.from_authorized_user_file(json)


class AuthStub:
    def get_credentials(self):
        creds = {
            "token": "TOKEN",
            "refresh_token": "REFRESH TOKEN",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": "CLIENTID",
            "client_secret": "CLIENTSECRET",
            "scopes": ["https://www.googleapis.com/auth/gmail.send"],
            "expiry": "EXPIRY",
        }
        return creds


class GmailSendClient:
    def __init__(self, creds=None):
        self.creds = creds

    def send_email(self, to, subject, body):
        service = build("gmail", "v1", credentials=self.creds)
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

        try:
            message = (
                service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            print(f"sent message to {message} Message Id: {message['id']}")
        except HTTPError as error:
            print(f"An error occurred: {error}")
            message = None


class GmailSendStub:
    def __init__(self, creds=None):
        self.messages = []
        self.creds = creds

    def send_email(self, to, subject, body):
        self.messages.append({"to": to, "subject": subject, "body": body})
