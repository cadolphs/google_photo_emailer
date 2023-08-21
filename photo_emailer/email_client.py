from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
from email.mime.text import MIMEText
import base64


class EmailClient:
    def __init__(self, mail_api=None):
        self.api = mail_api()

    @classmethod
    def create(cls):
        return cls(GmailAPI)

    @classmethod
    def create_null(cls):
        return cls(GmailStub)

    def authenticate(self):
        self.api.authenticate()

    def send_email(self, to, subject, body):
        self.api.send_email(to, subject, body)


class GmailAPI:
    def __init__(self):
        self.creds = None

    def authenticate(self):
        SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        self.creds = flow.run_local_server(port=0)

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


class GmailStub:
    def authenticate(self):
        pass

    def send_email(self, to, subject, body):
        self.last_message = {"to": to, "subject": subject, "body": body}
        print(self.last_message)
