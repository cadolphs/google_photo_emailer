from email.message import EmailMessage
from photo_emailer.utils.events import OutputListener, OutputTracker


class EmailSender:
    def __init__(self):
        self._listener = OutputListener()

    def track_output(self):
        return self._listener.create_tracker()

    @classmethod
    def create(cls):
        return cls()

    @classmethod
    def create_null(cls):
        sender = cls()
        sender.connect(NullEmailService())
        return sender

    def connect(self, service):
        self.service = service

    def send_email(self, message: EmailMessage):
        self.service.send_email(message)
        self._listener.track(data={"action": "send_email", "message": message})


class GoogleEmailService:
    def __init__(self, service):
        self.service = service

    def send_email(self, message: EmailMessage):
        self.service.users().messages().send(userId="me", body=message).execute()


class NullEmailService:
    def __init__(self):
        self._listener = OutputListener()

    def send_email(self, message: EmailMessage):
        pass
