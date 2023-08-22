from googleapiclient.discovery import build
from requests import HTTPError
from email.mime.text import MIMEText
import base64


class EmailClient:
    def __init__(self, sender=None):
        self.sender = sender

    @classmethod
    def create(cls, creds):
        sender = GmailSender(creds)
        return cls(sender)

    @classmethod
    def create_null(cls, creds):
        sender = GmailSendStub(creds)
        return cls(sender)

    def send_email(self, to, subject, body):
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

        self.sender.send_email(create_message)


class GmailSender:
    def __init__(self, creds=None):
        self.creds = creds

    def send_email(self, message):
        try:
            service = build("gmail", "v1", credentials=self.creds)
            result = (
                service.users().messages().send(userId="me", body=message).execute()
            )
            print(f"sent message to {result} Message Id: {result['id']}")
        except HTTPError as error:
            print(f"An error occurred: {error}")


class GmailSendStub:
    def __init__(self, creds=None):
        self.messages = []

    def send_email(self, message):
        self.messages.append(message)
