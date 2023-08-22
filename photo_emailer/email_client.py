from googleapiclient.discovery import build
from requests import HTTPError
from email.mime.text import MIMEText
import base64


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
